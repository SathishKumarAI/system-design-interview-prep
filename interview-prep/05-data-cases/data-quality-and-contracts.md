---
title: Design data quality, contracts and SLAs
type: case
track: data
difficulty: core
status: drafted
sources: [Practical Data Quality (local), dbt/Great Expectations docs]
updated: 2026-09-02
tags: [data-quality, contracts, lineage, sla, observability]
---

# Design data quality, contracts and SLAs

> A platform-level system that stops bad data reaching consumers, and tells you which
> upstream broke a dashboard.
> **The hard part:** it's mostly an *organisational* design. The tests are easy; getting
> producers to own their output is the system.

## 1. Clarify

| Question | Assumed answer |
|---|---|
| Scale of the estate? | 2,000 tables, 300 pipelines, 40 producing teams |
| Who consumes? | BI, ML training/serving, finance reporting, external customer-facing metrics |
| Blast radius of bad data? | Finance and customer-facing metrics = incident. Exploratory tables = annoyance |
| Do we control producers? | Same company, different teams — influence, not authority |
| Existing tooling? | Airflow/dbt, Iceberg lakehouse |

**Non-goals:** master data management, a full data catalogue product, org restructuring.

## 2. Requirements

**Functional**
- Declare expectations per table (schema, freshness, volume, semantics) and enforce them
- Block bad data from being published to consumers, not just detect it afterwards
- Column-level lineage to answer "what upstream caused this?" in minutes
- Per-table SLAs with owners and a paging path

**Non-functional**

| Target | Value |
|---|---|
| Detection latency | < 1 pipeline run after a defect appears |
| False positive rate | Low enough that people don't mute the alerts (**the real constraint**) |
| Overhead | Checks < 10% of pipeline runtime |
| Coverage | 100% of tier-1 tables; best effort below |

## 3. Estimates

Organisational, not computational:

```
2,000 tables × ~6 checks = 12,000 checks per full cycle
   If 1% flake → 120 false alarms/day → everyone mutes everything → the system is worthless
   ⇒ tier tables and only page on tier-1; everything else is a dashboard/ticket   ← the design
Tier 1 (finance, customer-facing): ~50 tables → ~300 checks. Page on these.
Check cost: a full-table uniqueness check on 5B rows is expensive → sample or use
   incremental checks on the new partition only.
```

> [!info] The scary number
> **Alert fatigue.** A quality system whose alerts get muted is worse than none, because it
> creates false confidence. Every design decision below flows from that.

## 4. API / contract

A data contract, versioned in the **producer's** repo:

```yaml
table: orders.line_items
owner: team-checkout            # a team, never a person
tier: 1                         # 1 = page, 2 = ticket, 3 = dashboard only
sla:
  freshness: 30m                # max age of the newest row
  completeness: 99.99%          # vs the source system's own count
schema:
  - {name: order_id,   type: string, nullable: false, unique: true}
  - {name: amount_minor, type: long, nullable: false, min: 0}
  - {name: currency,   type: string, accepted: [USD, EUR, GBP]}
semantics:
  grain: "one row per line item per order"
  pii: [customer_email]         # masked in silver, deleted on erasure request
tests:
  - row_count_anomaly: {vs: 7d_median, tolerance: 0.25}
  - referential: {column: order_id, references: orders.orders.id}
consumers: [finance.revenue_daily, ml.demand_forecast]   # who breaks if this breaks
```

**The contract lives with the producer and is checked in the producer's CI.** That is the
whole idea: schema changes fail the *producer's* build, not your 3am pager.

## 5. Data model

| Entity | Content |
|---|---|
| `contracts` | The YAML above, versioned |
| `check_results` | (table, check, run_id, status, observed, expected, ts) — a time series |
| `lineage_edges` | (upstream_column → downstream_column, transform_ref) |
| `incidents` | Detected defect → impact set (via lineage) → owner → resolution |
| `table_metadata` | Tier, owner, SLA, freshness, last good run |

`check_results` as a time series is what lets you do anomaly detection on the *checks*
themselves (this check has flaked 40 times this month → fix or delete it).

## 6. Architecture

```
producer CI ──schema/contract compatibility check──→ blocks incompatible merges
                                                              (the cheapest possible gate)
pipeline run:
   extract → transform → WRITE to an Iceberg branch (not the main table)
                              ↓
                        AUDIT: run checks against the branch
                              ↓
                 pass → PUBLISH (fast-forward the branch into main, atomic)
                 fail → do NOT publish; alert owner; consumers keep the last good snapshot
                              ↓
                        check_results → quality dashboard + SLA tracking
lineage: parsed from dbt manifests / SQL ASTs / Spark plans → graph store
incident: failed tier-1 check → page owner + notify downstream consumer owners automatically
```

### Deep dive A — write-audit-publish

The single most valuable pattern here. Instead of "write, then test, then apologise":

1. **Write** the new data to an Iceberg branch (or a staging table).
2. **Audit** — run the contract's checks against the branch.
3. **Publish** — atomically fast-forward into the main table only if checks pass.

Consumers never see bad data; they see *stale* data, which is almost always the better
failure. Say that trade explicitly: **stale beats wrong**, for every consumer except a few
real-time ones who should be told which they're getting.

### Deep dive B — what to check

| Class | Examples | Cost |
|---|---|---|
| **Schema** | Column exists, type, nullability | Free — metadata only |
| **Freshness** | max(updated_at) within SLA | Cheap |
| **Volume** | Row count within N% of the 7-day median for this weekday | Cheap, and catches the most real incidents |
| **Uniqueness / referential** | PK unique, FKs resolve | Expensive on big tables → run on the new partition only |
| **Distribution** | Null rate, category share, numeric range drift | Medium; the class that catches subtle upstream logic changes |
| **Reconciliation** | Totals match the source system or the finance ledger | Expensive, and non-negotiable for tier 1 |
| **Business rules** | `discount ≤ price`, `refund ≤ payment` | Cheap and high-value — ask domain experts for these |

> [!warning] Trap
> Only checking "did the job run?" Job success is not data success. The most damaging
> incidents are green pipelines producing wrong numbers — an upstream filter change that
> silently drops 30% of rows leaves every job green.

### Deep dive C — lineage and impact analysis

- Parse lineage automatically from dbt manifests, SQL ASTs and Spark logical plans. **Manual
  lineage documentation is always stale** — don't design a process that depends on it.
- Column-level, not just table-level: "revenue is wrong" should resolve to the one upstream
  column, not to a list of 40 tables.
- Use it in both directions: **upstream** for root cause, **downstream** for impact ("this
  broken table feeds the CFO's dashboard and two production ML models — notify those owners
  now"). Automating that notification is what turns a data platform from reactive to
  trustworthy.

### Deep dive D — making people actually care

The technical part is a week; this is the system.

- **Tiering** so paging is rare and meaningful.
- **Ownership at team level**, published, with a rota — orphaned tables get deprecated and
  deleted, not adopted by the platform team.
- **Producer CI checks** so most breakage never ships.
- **A quality score per team**, visible, discussed in reviews. Visibility changes behaviour
  far more reliably than a policy document.
- **Deprecation process**: mark, notify consumers, wait, delete. An estate that only grows is
  an estate nobody can keep correct.

## 7. Scale & failure

| Breaks first at 10x | Fix |
|---|---|
| Check runtime | Incremental checks on new partitions; sample big tables; parallelise |
| Alert volume | Stricter tiering, grouping, suppression during known upstream incidents |
| Lineage graph size | Column-level only for tier 1–2; table-level below |
| Contract sprawl | Templates and defaults by table type; generate, don't hand-write |

| Failure | Symptom | Mitigation |
|---|---|---|
| Checks themselves are wrong | False alarms, then muting | Track per-check flake rate; auto-demote flaky checks to non-paging |
| Quality system down | No gate | **Fail open with a loud warning** — blocking every pipeline because the checker is down is a worse outage than shipping unchecked data for an hour |
| Publish step partially applied | Consumers see half a load | Atomic branch fast-forward — this is exactly what Iceberg gives you |
| Owner left the company | Nobody responds | Team ownership, quarterly ownership audit |

## 8. Ops & cost

- **SLA:** tier-1 tables meet freshness + completeness 99.9% of days; time-to-detect < 1 run;
  time-to-notify-consumers < 5 min (automated from lineage).
- **Alert on:** tier-1 check failures (page), SLA breaches, check flake rate, tables with no
  owner, contract-less tier-1 tables.
- **Rollout:** start with the 50 tier-1 tables, prove the value with real caught incidents,
  then expand. A big-bang rollout across 2,000 tables generates exactly the alert storm that
  kills the initiative.
- **Cost:** compute for checks (keep under ~10% of pipeline cost) plus the platform team.
  Justify against incident cost: one wrong revenue report to the board pays for the year.
- **First thing I'd cut:** distribution checks on tier-3 tables, and full-table checks in
  favour of partition-scoped ones.

## Sources & further reading

- Local book: `DE/Fundamentals/Practical Data Quality ... Robert Hawker, Nicola Askham.pdf`
- Local book: `DE/Warehouse-ETL/Apache Airflow Best Practices ...pdf`
- [dbt — tests and contracts](https://docs.getdbt.com/docs/build/data-tests)
- [Great Expectations](https://greatexpectations.io/)
- [Iceberg — branching and write-audit-publish](https://iceberg.apache.org/docs/latest/branching/)
- Repo notes: [../../data%20engineering/AWS/data%20testing/](../../data%20engineering/AWS/data%20testing/)
