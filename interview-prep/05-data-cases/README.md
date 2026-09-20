---
title: Data platform cases index
type: index
track: data
status: drafted
updated: 2026-09-02
tags: [index, data-engineering]
---

# Data platform system design

The data engineering variant of the round. Same eight sections, different vocabulary:
throughput and freshness instead of rps and p99, correctness of *aggregates* instead of
correctness of *transactions*.

## Where to look

| Question | File |
|---|---|
| How do I run a data design round? What's scored? | [data-playbook.md](data-playbook.md) |
| Ingest clickstream at scale into a lakehouse | [clickstream-lakehouse.md](clickstream-lakehouse.md) |
| Replicate an operational DB into analytics, correctly | [cdc-pipeline.md](cdc-pipeline.md) |
| Sub-second analytics on live data (dashboards, ad counting) | [realtime-analytics.md](realtime-analytics.md) |
| Data quality, contracts, SLAs, lineage | [data-quality-and-contracts.md](data-quality-and-contracts.md) |

## The 2026 baseline stack (know why each piece exists)

| Layer | Typical | Exists because |
|---|---|---|
| Ingest | Kafka / Kinesis / Pub-Sub, Debezium for CDC | Decouple producers from consumers, replayable |
| Stream processing | Flink (rich state, event time), Spark Structured Streaming | Aggregate before storage, exactly-once sinks |
| Table format | **Apache Iceberg** (also Delta, Hudi) | ACID, schema evolution, time travel on object storage |
| Storage | S3/GCS/ADLS + Parquet | Cheap, decoupled from compute |
| Catalog | Iceberg REST catalog, Unity, Glue, Polaris | One source of truth for tables across engines |
| Query | Trino/Spark/DuckDB/Snowflake/BigQuery/ClickHouse | Different engines, same tables — that's the point |
| Orchestration | Airflow / Dagster / Prefect | Dependencies, retries, backfills, SLAs |
| Transform | dbt / SQLMesh | Versioned, tested, documented SQL |
| Quality | Great Expectations / dbt tests / Soda | Catch bad data before consumers do |

**The 2026 shape in one sentence:** a streaming hot tier for seconds-fresh data, Iceberg
tables on object storage for warm and cold, a REST catalog for governance, and any engine you
like reading the same tables.

## What's scored differently from a backend round

| Backend round asks | Data round asks |
|---|---|
| p99 latency | **Freshness SLA** — how stale may this table be? |
| Availability | **Completeness** — did we get every event, and can we prove it? |
| Transactions | **Idempotent, restartable batches** and exactly-once sinks |
| Schema migration | **Schema evolution** across producers and years of history |
| Debugging a request | **Lineage** — which upstream broke this dashboard? |
| Cost per request | **Cost per query and per TB scanned** (partitioning, file sizes) |

## Universal traps to name unprompted

- **Late and out-of-order events** — watermarks, an explicit late-data path, and a restatement
  policy. Never silently drop.
- **Small files** — streaming into Iceberg creates thousands of tiny files; compaction is a
  first-class scheduled job, not an afterthought.
- **Backfills** — the pipeline must support "reprocess 6 months" without a bespoke script, and
  without double-counting.
- **Time zones and event time vs ingest time** — one of the top causes of wrong numbers.
- **Silent failure** — a pipeline that produces *zero* rows usually looks green. Alert on
  row-count anomalies, not just on job failures.

## Referenced by

- [Books already on this machine](../10-resources/books-on-this-machine.md)
- [Interview prep index](../README.md)
- [Messaging and streams](../02-primitives/messaging-and-streams.md)
- [Microsoft, Apple, Netflix and other big tech](../09-company-styles/microsoft-apple-netflix.md)
- [Repo index](../../INDEX.md)
