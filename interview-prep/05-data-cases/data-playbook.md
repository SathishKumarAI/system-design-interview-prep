---
title: Data engineering design playbook
type: playbook
track: data
difficulty: core
status: drafted
sources: [DDIA ch.10-11, Iceberg docs]
updated: 2026-09-02
tags: [playbook, lakehouse, batch, streaming]
---

# Data engineering design playbook

## The clock

| Minutes | Phase | Output |
|---|---|---|
| 0–5 | Clarify: who consumes this, and how fresh must it be? | Consumer list + freshness SLA per consumer |
| 5–10 | Volume, velocity, variety; batch vs stream decision | Numbers, and the choice defended |
| 10–20 | Ingest → storage → transform → serve, with the table layout | The pipeline diagram + partitioning |
| 20–35 | Deep dive: exactly-once, late data, schema evolution, or backfill | Concrete mechanics |
| 35–45 | Quality, lineage, SLAs, cost | Checks, alerts, $/TB |

## The questions that change a data design

| Question | Changes |
|---|---|
| **Who consumes this and what decision do they make with it?** | Freshness, granularity, and whether this pipeline should exist at all |
| Freshness SLA — daily, hourly, minutes, seconds? | Batch vs micro-batch vs streaming |
| Is the data correctable? (restatements allowed?) | Immutable append vs upsert/merge semantics |
| Is late data possible, and how late? | Watermarks, reprocessing windows |
| Is it PII? Regulated? Residency constrained? | Encryption, masking, deletion path, region placement |
| Volume today and in two years? | File formats, partitioning, engine choice |
| Who owns the source schema? | Contracts, or you'll be broken by someone else's deploy |

> [!tip] Opening line
> "Before I design a pipeline: who reads the output, how fresh does it need to be, and what
> happens if it's wrong for an hour? Those three answers decide batch versus streaming, and
> most of the rest follows."

## Batch vs streaming — decide it explicitly

| Choose **batch** when | Choose **streaming** when |
|---|---|
| Freshness of hours is fine | Seconds/minutes matter to a decision (fraud, bidding, live ops) |
| Logic is complex, changes often | Logic is stable and incremental |
| Reprocessing must be easy | Continuous, unbounded input |
| Cost matters more than latency | Latency is the product |

**Streaming costs you:** state management, watermarks, out-of-order handling, checkpointing,
exactly-once sinks, and a much harder debugging story. Say those costs out loud. Many "real
time" requirements are satisfied by micro-batch every 5 minutes at a fraction of the
complexity — proposing that is a senior move, not a lazy one.

**Kappa vs Lambda:** Lambda runs a batch path and a streaming path with reconciliation
(duplicate logic, two places to fix a bug). Kappa uses one streaming path and replays the log
for reprocessing. Kappa is the modern default; Lambda survives where batch and streaming
genuinely need different logic.

## Layering (medallion, or whatever you call it)

| Layer | Contains | Rules |
|---|---|---|
| **Bronze / raw** | Source data as-received, append-only, schema-on-read | **Never modify.** It's your ability to reprocess |
| **Silver / cleaned** | Deduplicated, typed, conformed, PII handled | Business-agnostic. One row = one real-world event |
| **Gold / marts** | Aggregates, dimensional models, feature tables | Consumer-shaped, documented, SLA'd |

Keeping raw forever is what makes bugs recoverable: fix the transform, replay. This is the
data equivalent of "derived stores must be rebuildable" — and it's the same idea as event
sourcing in [../02-primitives/messaging-and-streams.md](../02-primitives/messaging-and-streams.md).

## Table layout — where data engineers win or lose

| Decision | Guidance |
|---|---|
| **Partitioning** | By the column most queries filter on — usually event date. Avoid over-partitioning (a partition per hour per customer = millions of tiny partitions) |
| **File size** | Target 128–512 MB Parquet files. Small files kill query planners and object-store throughput |
| **Compaction** | Scheduled, non-negotiable when streaming into a table |
| **Sort/cluster order** | Sort by the second most common filter → better min/max pruning |
| **Column pruning** | Parquet reads only the columns you select. `SELECT *` is a cost decision |
| **Snapshot expiry** | Time travel is not free; expire old snapshots or storage grows forever |

**Iceberg specifics worth naming:** hidden partitioning (queries don't need to know the
partition scheme), schema evolution by field ID (renames don't break history), snapshot
isolation for concurrent writers, time travel, and branch/tag semantics for write-audit-publish.

## Correctness mechanics

- **Exactly-once into a table**: streaming engine checkpoints + a transactional sink (Flink's
  two-phase commit into Iceberg). Not magic — the sink participates in the checkpoint.
- **Idempotent batch**: a job re-run for the same partition must produce the same result.
  Overwrite the partition, don't append; key on `(entity, event_date)`.
- **Deduplication**: on a stable event ID over a bounded window; state has to expire or it
  grows forever.
- **Late data**: watermark + allowed lateness + a side output for anything later than that,
  plus a documented restatement policy. "We drop it" is an acceptable answer *if you say it*.
- **Backfill**: same code path as the live pipeline, parameterised by time range. If backfill
  needs a different script, the design is wrong.

## Serving

| Consumer | Serve from |
|---|---|
| BI dashboards | Gold tables in a warehouse or via Trino, with pre-aggregates |
| Product features (in-app analytics) | A real-time OLAP store (ClickHouse, Pinot, Druid) |
| ML training | Point-in-time-correct feature tables — see [../06-ml-cases/feature-store.md](../06-ml-cases/feature-store.md) |
| ML serving | Low-latency KV store, populated from the same definitions |
| Reverse ETL to SaaS tools | A dedicated sync with its own SLA |

## Quality, lineage, governance (the last 10 minutes)

- **Data contracts** between producer and consumer: schema, semantics, freshness, volume
  expectations, and an owner. Enforced in the producer's CI, not discovered in your dashboard.
- **Tests as gates**: not-null, uniqueness, referential integrity, accepted ranges, row-count
  anomaly vs the last 7 days. Run *before* publishing (write-audit-publish: write to a branch,
  validate, then commit).
- **Lineage** column-level where possible: when a number is wrong, you need to know its
  upstreams in seconds.
- **SLAs per table**, published: freshness, completeness, and who to page.
- **PII**: tagged columns, masked by default, deletion propagated to every derived table and
  to backups. GDPR deletion in an append-only lake is a real design problem — Iceberg's
  row-level deletes or partition rewrite are the answer.

## Cost

Cost per query and per TB scanned. Levers: partition pruning, file sizing, columnar formats,
compression (zstd), materialising expensive repeated queries, separating compute from storage
so idle warehouses cost nothing, and killing the dashboards nobody opens (measure query usage
per table — typically a large fraction of pipelines feed nothing).

## Referenced by

- [8-week study plan](../07-drills/8-week-plan.md)
- [Data platform cases index](README.md)
- [Design a feature store](../06-ml-cases/feature-store.md)
- [Interview playbook](../00-interview-playbook.md)

## Sources & further reading

- Local book: `DE/System-Design/Designing Data Intensive Applications.pdf` — ch.10 (batch), ch.11 (streaming)
- Local book: `DE/Fundamentals/Big Book of Data Engineering.pdf`
- Local book: `DE/Fundamentals/Practical Data Quality ...pdf`
- Local book: `DE/Warehouse-ETL/Architecting a Modern Data Warehouse for Large Enterprises ...pdf`
- Local book: `DE/Warehouse-ETL/Apache Airflow Best Practices ...pdf`
- [Apache Iceberg — spec and docs](https://iceberg.apache.org/)
- [40 data engineering system design interview questions (2026)](https://datavidhya.com/blog/data-engineering-system-design-interview-questions/)
- Repo notes: [../../data%20engineering/](../../data%20engineering/)
