---
title: Design a clickstream ingestion pipeline into a lakehouse
type: case
track: data
difficulty: core
status: drafted
sources: [Iceberg docs, Flink docs]
updated: 2026-09-02
tags: [kafka, flink, iceberg, compaction, late-data]
---

# Design a clickstream pipeline into a lakehouse

> Every page view, click and impression from web and mobile, landing in queryable tables for
> analytics, ML features and product dashboards.
> **The hard part:** exactly-once into the table, late events, and not drowning in small files.

## 1. Clarify

| Question | Assumed answer |
|---|---|
| Volume? | 50B events/day (~600k/s average, 2M/s peak) |
| Freshness? | Dashboards: 5 min. ML training: daily. Real-time product features: seconds |
| Retention? | Raw 90 days, aggregates 3 years |
| Late events? | Mobile offline buffering — up to 7 days late |
| Consumers? | BI, ML training, real-time personalisation, finance (revenue attribution) |
| Correctness bar? | Finance needs exact counts; product analytics tolerates ±0.1% |

**Non-goals:** the SDKs, consent management UI, the ML models themselves.

## 2. Requirements

**Functional**
- Ingest events from web/mobile/server SDKs; validate against a schema registry
- Land raw immutable events; produce cleaned and aggregated tables
- Support backfill and reprocessing without double counting
- Serve seconds-fresh aggregates for real-time features

**Non-functional**

| Target | Value |
|---|---|
| Ingest availability | 99.99% — a dropped event is unrecoverable |
| Completeness | ≥ 99.99% of accepted events land in the table, provably |
| Freshness | Bronze < 1 min; silver < 5 min; gold hourly/daily |
| Cost | < $X per billion events (make it an explicit budget) |

## 3. Estimates

```
50B events/day ≈ 600k/s avg, 2M/s peak
Event ~1 KB JSON → 50 TB/day raw
   Parquet + zstd typically 5–10× → 5–10 TB/day stored, ~500 TB–1 PB for 90 days
Kafka: 600k/s × 1 KB = 600 MB/s → ~10–20 brokers with headroom, RF3
   7-day retention = 50 TB × 7 × 3 = ~1 PB of broker storage (or tiered to object storage)
Files: if we commit to Iceberg every minute × 200 partitions = 288,000 files/day
   → 250 KB average files. Query planning dies.        ← compaction is mandatory, not optional
Cost: object storage ~1 PB ≈ $23k/month, plus compute. Egress internal, so cheap.
```

> [!info] The scary number
> **288,000 files/day** from naive streaming commits. Small-file management is the operational
> heart of a streaming lakehouse, and it's what separates people who've run one from people
> who've read about one.

## 4. API / contract

```
SDK → POST /v1/collect  (batched, gzipped, ~100 events per request)
      { events: [{event_id, event_name, ts_event, user_id, session_id, props{}, sdk_version}] }
      → 202 (accept fast; validate async)  — never make the client wait on the pipeline

Schema registry: every event_name has a registered Avro/Protobuf schema.
   Producers fail CI on an incompatible change (backward compatibility enforced).
```

`event_id` is client-generated (UUID) — the deduplication key. `ts_event` is client time,
`ts_ingest` is server time; **store both**, always. Client clocks are wrong and you'll need to
detect it.

## 5. Data model

```
bronze.events_raw      -- exactly as received + ingest metadata, append-only
   partition: days(ts_ingest)          -- ingest time: guarantees a partition is "done"
silver.events          -- deduplicated, typed, PII-handled, bot-filtered
   partition: days(ts_event), bucket(user_id, 64)
gold.sessions          -- sessionised
gold.daily_metrics     -- DAU/MAU, funnels, revenue attribution
```

**Why bronze partitions by ingest time and silver by event time:** ingest-time partitions are
append-only and immutable once the hour passes, so raw is a clean, replayable log. Silver
partitions by event time because every analytical query filters on when the event *happened* —
which means a late event rewrites an old partition, and that's exactly what Iceberg's
snapshot isolation and merge-on-read exist for.

Bucketing silver by `user_id` gives cheap user-level joins and a bounded file count per
partition.

## 6. Architecture

```
SDKs → edge collector (validate, enrich: geo/IP, UA parse, consent check) → Kafka (raw topic)
                                                                              │
                          ┌───────────────────────────────────────────────────┤
                          ▼                                                   ▼
              Flink: bronze sink                                    Flink: real-time aggregates
              (checkpoint + 2PC → Iceberg bronze)                   (windowed counts → ClickHouse/Pinot)
                          │                                                   └→ product features
                          ▼
              Flink/Spark: dedupe, clean, enrich → Iceberg silver
                          │
                          ▼
              dbt/Spark scheduled: gold marts, sessionisation, attribution
                          │
                     Trino / warehouse ← BI      ML training ← silver/gold
                          ▲
              compaction + snapshot expiry jobs (continuous)
```

### Deep dive A — exactly-once into Iceberg

- Flink checkpoints periodically; the Iceberg sink is **transactional**: files are written
  during the interval, and the Iceberg commit happens as part of the checkpoint's two-phase
  commit. A failure before commit leaves orphan files (cleaned by an orphan-file job), never
  duplicate rows.
- Checkpoint interval is the **freshness vs file-count knob**: 1 minute gives 1-minute
  freshness and lots of small files; 5 minutes gives fewer, bigger files. Say this trade —
  it's the design decision, not a config detail.
- Kafka consumer offsets are part of the same checkpoint, so restart resumes exactly where
  the last committed snapshot ended.
- **Dedup for at-least-once producers**: the SDK retries, so the same `event_id` can arrive
  twice. Deduplicate in the bronze→silver step over a bounded window (7 days, matching the
  late-arrival window) using a state store keyed by `event_id`, with TTL.

### Deep dive B — late and out-of-order events

- Mobile clients buffer offline for up to 7 days. Watermark for real-time aggregates is
  minutes (you cannot wait 7 days for a dashboard), so:
  - Real-time path: watermark ~5 min, allowed lateness ~1 h, anything later goes to a **side
    output**.
  - Batch path: the daily silver rebuild for day D re-runs at D+1, D+3 and D+7, restating the
    partition. Iceberg makes this an atomic partition overwrite.
- **Publish a restatement policy**: "numbers for a day are provisional for 7 days, final
  after." Consumers who care (finance) read the final table; dashboards read the provisional
  one. Saying this out loud is the mature answer — the alternative is finance and product
  quietly reporting different numbers forever.
- Detect nonsense client clocks (`ts_event` far from `ts_ingest`) and quarantine rather than
  corrupting partitions from 2035.

### Deep dive C — small files and maintenance

Four scheduled jobs that must exist from day one:

| Job | Cadence | Purpose |
|---|---|---|
| **Compaction** (rewrite data files) | Hourly per hot partition, daily for the rest | 250 KB files → 256 MB files |
| **Snapshot expiry** | Daily | Time travel is storage; keep 7 days |
| **Orphan file cleanup** | Weekly | Remove files from failed commits |
| **Manifest rewrite** | Weekly | Keeps query planning fast as the table grows |

Without these, query latency degrades gradually for months and then everyone blames the query
engine.

### Deep dive D — schema evolution and contracts

- Schema registry with **backward compatibility** enforced in producer CI: new fields must be
  optional; removing or retyping a field fails the build.
- Iceberg column IDs mean a rename doesn't rewrite history and old readers keep working.
- Unknown fields land in a `props` map in bronze so nothing is lost while the schema catches
  up — you can always promote a map key to a column later, but you can't recover data you
  dropped.

## 7. Scale & failure

| Breaks first at 10x | Fix |
|---|---|
| Kafka storage/throughput | Tiered storage, more partitions, shorter hot retention |
| Flink state (dedup keys) | Shorter dedup window, RocksDB state backend, key sharding |
| File count / query planning | More aggressive compaction, larger checkpoint interval |
| Gold job runtime | Incremental models (dbt/SQLMesh), process only changed partitions |

| Component fails | Blast radius | Degraded behaviour |
|---|---|---|
| Collector down | **Events lost forever** — the only unrecoverable failure | Multi-AZ, autoscaled, SDK-side retry + local buffering, accept-fast/validate-async |
| Kafka partition unavailable | Ingest stalls | RF3 + producer retries; SDK buffers |
| Flink job crashes | Freshness lag | Restart from checkpoint, no data loss; alert on lag |
| Compaction falls behind | Queries slow down | Alert on file count per partition, not just on job status |
| Bad schema deployed | Garbage in silver | Registry blocks it; if it lands, replay bronze after fixing — **this is why bronze is immutable** |

## 8. Ops & cost

- **SLA per table**, published: bronze < 1 min, silver < 5 min, gold by 06:00 daily.
- **Alert on:** ingest rate anomaly vs the same hour last week (catches silent SDK breakage —
  the most common real incident), Flink checkpoint failures, consumer lag, file count per
  partition, dedup state size, row-count deviation per table.
- **Rollout:** pipeline changes run in shadow against the same input and outputs are diffed
  before cutover. Write-audit-publish (write to an Iceberg branch, validate, then commit).
- **Cost:** object storage ~$23k/month per PB, Kafka brokers, and Flink/Spark compute. Levers:
  drop unused event types (audit which columns are actually queried), zstd, cheaper checkpoint
  cadence, spot instances for batch.
- **First thing I'd cut:** raw retention 90 → 30 days for high-volume, low-value events, and
  the real-time path for metrics nobody watches live.

## Referenced by

- [Data platform cases index](README.md)
- [Question bank](../07-drills/question-bank.md)
- [Repo index](../../INDEX.md)
- [Storage engines — B-tree vs LSM](../fundamentals/storage-engines.md)

## Sources & further reading

- [Apache Iceberg — maintenance and compaction](https://iceberg.apache.org/docs/latest/maintenance/)
- [Flink — Iceberg connector and exactly-once sinks](https://iceberg.apache.org/docs/latest/flink/)
- [The state of streaming to Apache Iceberg (2026)](https://dev.to/alexmercedcoder/the-state-of-streaming-to-apache-iceberg-in-july-2026-every-path-its-latency-and-what-to-do-when-i6p)
- Repo notes: [../../data%20engineering/AWS/Clickstream%20data%20ingestion/](../../data%20engineering/AWS/Clickstream%20data%20ingestion/)
- Local book: `DE/Fundamentals/Big Book of Data Engineering.pdf`
