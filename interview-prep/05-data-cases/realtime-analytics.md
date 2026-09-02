---
title: Design real-time analytics (ad click aggregation)
type: case
track: data
difficulty: advanced
status: drafted
sources: [Alex Xu v2 ch. ad click aggregation, Pinot/Druid docs]
updated: 2026-09-02
tags: [streaming, olap, windows, exactly-once, cardinality]
---

# Design real-time analytics / ad click aggregation

> Count ad clicks and impressions per campaign per minute, serve those counts to advertisers
> within seconds, and be exactly right — because this is billing.
> **The hard part:** exactly-once counting under duplicates and late events, with an OLAP
> serving layer fast enough for interactive queries.

## 1. Clarify

| Question | Assumed answer |
|---|---|
| Volume? | 10B ad events/day (~120k/s avg, 500k/s peak) |
| Query patterns? | "Clicks for campaign X per minute, last 24 h", filtered by country/device/creative |
| Freshness? | Dashboards < 1 min; billing recomputed daily and authoritative |
| Correctness? | **Billing-grade** — duplicates cost money in both directions |
| Late events? | Yes, minutes typical, hours possible from mobile |
| Retention? | Minute granularity 30 days, hourly 1 year, daily forever |

**Non-goals:** ad serving/auction, fraud detection model, the advertiser UI.

## 2. Requirements

**Functional**
- Ingest click/impression events, deduplicate, aggregate by (campaign, minute, dimensions)
- Serve aggregates with sub-second query latency
- Support backfill/restatement when late or corrected data arrives
- Distinct-user counts per campaign (reach)

**Non-functional**

| Target | Value |
|---|---|
| End-to-end freshness | < 1 min p95 |
| Query latency | p99 < 500 ms |
| Accuracy | Exact for billing; approximate acceptable for reach (HyperLogLog) |
| Availability | 99.9% query; ingest must not lose events |

## 3. Estimates

```
10B events/day ≈ 120k/s avg, 500k/s peak; event ~500 B → 5 TB/day raw
Aggregate rows: 100k campaigns × 1,440 min × ~20 dimension combos = 2.9B rows/day
   ← the aggregate can be BIGGER than the input if you cross too many dimensions
   → pre-aggregate only the combinations that are actually queried
At 1 min granularity, 30 days: 100k × 43,200 × 20 = 86B rows → must roll up aggressively
Dedup state: 500k/s × 300 s window = 150M keys in state ≈ 10–20 GB of RocksDB
Distinct users per campaign: exact = enormous sets; HLL = 12 KB/campaign, 0.81% error
```

> [!info] The scary number
> **Dimensional explosion.** Naive "aggregate by every combination" produces more rows than
> the raw events. Choosing which cuboids to materialise is the design.

## 4. API / contract

```
ingest: Kafka topic `ads.events`, key = ad_id
  {event_id, event_type: "impression"|"click", ad_id, campaign_id, user_id,
   ts_event, country, device, creative_id, cost_micros}

query:
GET /v1/reports?campaign_id=&from=&to=&granularity=minute&group_by=country,device
  → { rows: [{ts, country, device, impressions, clicks, spend_micros, reach_approx}] }
```

`event_id` is generated at ad-serve time and carried through the click redirect — that's the
deduplication key, and it must be signed so a bot cannot mint clicks.

## 5. Data model

| Layer | Store | Content |
|---|---|---|
| Raw | Kafka → Iceberg `bronze.ad_events` | Every event, replayable, the audit trail |
| Real-time aggregates | Pinot / Druid / ClickHouse | (campaign, minute, country, device) → counts |
| Batch aggregates | Iceberg `gold.ad_metrics_daily` | Recomputed nightly, **authoritative for billing** |
| Sketches | Same OLAP store | HLL per (campaign, day) for reach |

**Pre-aggregation strategy:** materialise the cuboids that are queried
(`campaign×minute`, `campaign×country×minute`, `campaign×creative×hour`) and compute the rest
on the fly from the finest materialised level. Roll up minute → hour → day on a schedule.

> [!tip] Say this
> "I'd materialise three or four cuboids based on actual query logs, not all 2^n. Then roll
> up minute data to hourly after 7 days. Storage and query cost are both dominated by that
> decision, so I'd instrument query patterns before choosing."

## 6. Architecture

```
ad server → Kafka(ads.events) ──┬──→ Flink: dedupe (event_id, 5 min–1 h window)
                                │         → windowed aggregate (event time, watermark)
                                │         → upsert into Pinot/Druid (real-time segments)
                                │         → HLL sketches per campaign
                                │
                                └──→ Iceberg bronze (raw, exactly-once via checkpoint+2PC)
                                            │
                                     nightly Spark/Flink batch:
                                     full recompute for D-1 (and D-3, D-7 restatements)
                                            → gold.ad_metrics_daily  (billing truth)
                                            → backfill OLAP historical segments

query API → OLAP store (recent, real-time segments) ∪ (historical, batch-corrected segments)
```

This is a **Lambda architecture**, deliberately — and here it's justified, which is worth
saying explicitly since Lambda is usually the wrong default:

> [!tip] Say this
> "I'd normally argue for Kappa, but billing needs an authoritative recomputation that can
> incorporate week-late events and fraud reversals, and the streaming path needs sub-minute
> latency. Those are genuinely different requirements, so two paths with a documented
> handover boundary — real-time for anything under 24 hours, batch-corrected beyond — is
> honest rather than lazy."

### Deep dive A — exactly-once counting

Three independent duplicate sources, and you need an answer for each:

| Source of duplicates | Mitigation |
|---|---|
| Client/network retries on the click redirect | Signed `event_id`, deduplicated in Flink state over a bounded window |
| Kafka at-least-once producer | Idempotent producer + transactional writes |
| Flink restart replaying from checkpoint | Checkpointed state + transactional sinks; the aggregate commit is part of the checkpoint |

Dedup window is bounded (say 1 hour) because state cannot grow forever. Anything later than
the window slips through the streaming path — and is **caught by the nightly batch recompute**,
which deduplicates over the full day from bronze. That's exactly why the batch path exists.

### Deep dive B — event time, watermarks, late data

- Aggregate on `ts_event`, never on arrival time. A minute bucket is defined by when the click
  happened.
- Watermark = max observed event time − allowed lateness (e.g. 2 min). A window fires when the
  watermark passes its end.
- Allowed lateness after firing (e.g. 1 h) → emit an **update** (upsert into the OLAP store,
  which is why the store must support upserts).
- Beyond that: side output → included in the nightly recompute. Never silently dropped;
  count them and alert if the rate rises (a rising late-event rate usually means an SDK or a
  region is broken).

### Deep dive C — the OLAP serving layer

| Store | Strength |
|---|---|
| **Apache Pinot** | Real-time ingestion from Kafka + upserts, built for user-facing analytics at high QPS |
| **Druid** | Similar; strong time-series rollups |
| **ClickHouse** | Fastest raw scan performance, simpler ops, weaker native upsert story (ReplacingMergeTree with eventual dedup) |

Choose by whether you need **upserts on real-time segments** (Pinot/Druid) or raw scan speed
(ClickHouse). Say the trade rather than naming a favourite.

Query performance levers: partition by time, sort by campaign, star-tree/pre-aggregated
indexes for common group-bys, bitmap indexes on low-cardinality dimensions, and a result cache
for dashboard queries (which repeat constantly).

### Deep dive D — approximate counts where exactness isn't required

- **HyperLogLog** for unique reach: 12 KB per sketch, ~0.8% error, and **mergeable** — so
  daily sketches roll up into weekly without touching raw data. Exact distinct counts across
  100k campaigns would be orders of magnitude more expensive.
- **Theta sketches** when you need set intersections (audience overlap).
- **t-digest** for percentile metrics.
- Rule to state: **approximate for exploration, exact for billing.** Two numbers, clearly
  labelled in the UI, is honest; one number that's sometimes wrong is a lawsuit.

## 7. Scale & failure

| Breaks first at 10x | Fix |
|---|---|
| Flink dedup state | Shorter window, key sharding, RocksDB tuning; rely more on batch dedup |
| OLAP row count | Fewer materialised cuboids, faster rollup, shorter minute-granularity retention |
| Query QPS from advertiser dashboards | Result cache, pre-computed reports, per-tenant quotas |
| Kafka throughput | More partitions (key by ad_id keeps ordering), compression |

| Component fails | Blast radius | Degraded behaviour |
|---|---|---|
| Flink job down | Real-time numbers freeze | Restart from checkpoint; show "data as of HH:MM"; **batch path still produces correct billing** |
| OLAP node down | Partial query results | Replication; better to return an explicit error than silently partial billing data |
| Kafka lag | Freshness degrades | Autoscale consumers; alert |
| Bad aggregation deploy | Wrong numbers, already served | Restate from bronze — the reason raw is retained. Version the aggregation logic so restatements are reproducible |

## 8. Ops & cost

- **SLA:** freshness p95 < 1 min; billing numbers final at D+1 06:00; streaming vs batch
  discrepancy < 0.1% (measured, graphed, and alerted — this is the health metric of a Lambda
  architecture and the reason to keep the two paths honest).
- **Alert on:** streaming/batch divergence, late-event rate, dedup state size, watermark
  stalls (a stuck watermark silently freezes all windows — the sneakiest failure here), OLAP
  ingestion lag.
- **Rollout:** aggregation changes run in shadow against the batch path for a full day before
  cutover.
- **Cost:** OLAP storage/memory dominates, then Flink state, then Kafka. Rolling up minute
  data after 7 days is usually the single biggest saving.
- **First thing I'd cut:** materialised cuboids nobody queries (measure with query logs), and
  minute-granularity retention 30 → 7 days.

## Referenced by

- [Batch vs streaming](../comparisons/batch-vs-streaming.md)
- [Data platform cases index](README.md)
- [Question bank](../07-drills/question-bank.md)
- [Repo index](../../INDEX.md)
- [Stream processing semantics](../fundamentals/stream-processing-semantics.md)

## Sources & further reading

- Local book: Alex Xu vol. 2 — ad click event aggregation chapter (`AI/ML-Foundations/`)
- [Apache Pinot — real-time upserts](https://docs.pinot.apache.org/)
- [Flink — event time and watermarks](https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/)
- [HyperLogLog paper](https://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf)
- Related: [../03-backend-cases/metrics-monitoring.md](../03-backend-cases/metrics-monitoring.md)
