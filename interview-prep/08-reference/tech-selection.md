---
title: Technology selection tables
type: reference
track: universal
status: drafted
updated: 2026-09-02
tags: [reference, selection]
---

# Technology selection

Pick by **access pattern and constraint**, never by popularity. Each row is a defensible
interview answer; the "avoid when" column is what earns the points.

## Databases

| Need | Pick | Avoid when |
|---|---|---|
| Transactions, joins, moderate scale | **PostgreSQL / MySQL** | Sustained writes far beyond a single primary and sharding is unacceptable |
| Massive writes, known access key, no joins | **Cassandra / ScyllaDB** | You need ad-hoc queries or strong multi-key transactions |
| Managed KV with predictable latency | **DynamoDB** | Complex queries; cost at very high read volume without careful key design |
| Sub-ms cache / ephemeral structures | **Redis** | As a durable source of truth without a deliberate persistence design |
| Flexible nested documents | **MongoDB** | You actually need relational integrity across entities |
| Analytics over columns, billions of rows | **ClickHouse / BigQuery / Snowflake / DuckDB** | High-frequency single-row updates |
| Full-text + relevance + facets | **Elasticsearch / OpenSearch** | As the source of truth (it's a derived store) |
| Time-series with rollups | **Prometheus / Timescale / InfluxDB** | High-cardinality labels (that's a logs/traces problem) |
| Vectors / semantic search | **pgvector, Qdrant, Milvus, Pinecone** | Small corpora where a brute-force scan is fine |
| Relationship traversal | **Neo4j** | Scale-out is required and traversals are shallow — do it in SQL |
| Global strong consistency | **Spanner / CockroachDB** | Latency-critical single-region workloads (you pay for the coordination) |
| Big immutable blobs | **S3-class object storage** | Low-latency small random reads |

## Messaging

| Need | Pick | Avoid when |
|---|---|---|
| Replayable event backbone, multiple consumers | **Kafka / Redpanda** | Simple task queue — the operational cost isn't worth it |
| Simple managed task queue | **SQS** | You need replay or strict ordering across a topic |
| Rich routing, per-message ack, priorities | **RabbitMQ** | Very high throughput streaming |
| Managed streaming on a cloud | **Kinesis / Pub-Sub / Event Hubs** | You need Kafka-ecosystem tooling specifically |
| Task scheduling with retries in-app | **Celery / Sidekiq / Temporal** | Complex multi-step workflows → use Temporal, not a queue |
| Long-running orchestrated workflows | **Temporal / Step Functions** | A single async job — that's a queue |

## Stream and batch processing

| Need | Pick |
|---|---|
| Rich state, event time, exactly-once sinks | **Flink** |
| Already running Spark, micro-batch is fine | **Spark Structured Streaming** |
| Lightweight, no cluster, JVM app | **Kafka Streams** |
| Large batch ETL | **Spark** |
| SQL transforms with tests and lineage | **dbt / SQLMesh** |
| Orchestration | **Airflow** (mature) / **Dagster** (asset-oriented) / **Prefect** |

## Storage formats and table formats

| Need | Pick |
|---|---|
| Columnar file format | **Parquet** (+ zstd) |
| ACID tables on object storage | **Apache Iceberg** (also Delta, Hudi) |
| Row format for streaming records | **Avro** with a schema registry |
| Service-to-service payloads | **Protobuf** |

## Caching and edge

| Need | Pick |
|---|---|
| Application cache, data structures | **Redis** |
| Pure memcache, simplest possible | **Memcached** |
| Static + dynamic edge caching | **CloudFront / Fastly / Cloudflare** |
| Full-page HTTP cache at origin | **Varnish / Nginx** |
| Edge compute (auth, A/B, rewrite) | **Cloudflare Workers / Lambda@Edge** |

## Compute

| Need | Pick | Avoid when |
|---|---|---|
| Long-running services, control | **Kubernetes** | A team of five with three services — use a PaaS |
| Simple containers, low ops | **ECS / Cloud Run / Fly / Render** | You need deep custom scheduling |
| Spiky, event-driven, low sustained volume | **Lambda / Cloud Functions** | Sustained high rps (often 3–10x the cost) or strict cold-start budgets |
| Batch / training | **Spot instances + checkpointing** | Latency-critical interactive work |
| GPU inference | **vLLM / SGLang / TensorRT-LLM** on reserved GPUs | Spiky low volume — use a hosted API |

## Observability

| Need | Pick |
|---|---|
| Metrics | **Prometheus / Mimir / Datadog** |
| Logs | **Loki / OpenSearch / Datadog** (sample aggressively) |
| Traces | **OpenTelemetry + Tempo / Jaeger / Datadog** |
| Dashboards | **Grafana** |
| Errors | **Sentry** |

## ML / GenAI

| Need | Pick |
|---|---|
| Tabular models | **XGBoost / LightGBM** — still the default, and usually the right one |
| Deep learning | **PyTorch** |
| Experiment tracking + registry | **MLflow / Weights & Biases** |
| Feature store | **Feast** (OSS) / **Tecton** (managed) / build on Redis + Iceberg |
| Serving classic models | **BentoML / Triton / plain FastAPI** |
| Serving LLMs | **vLLM / SGLang / TensorRT-LLM** |
| Hosted frontier LLM | **Anthropic Claude** (`claude-opus-5`, `claude-sonnet-5`, `claude-haiku-4-5`) or another provider — compare on quality, latency, price and data policy |
| Vector search | **pgvector** if already on Postgres; **Qdrant/Milvus** at larger scale |
| Orchestration for LLM apps | Thin custom code first; frameworks only when they earn it |

## The meta-rule

> [!tip] Say this when asked "why X?"
> "X, because our requirement is R and X's trade-off matches it. The alternative Y would buy us
> B, which we don't need, and cost us C, which we do care about. If R changes to R', I'd revisit."

And the rule underneath that one: **boring, well-understood technology, plus one deliberate
exotic choice where a requirement forces it.** A design with five novel components has five
things nobody on the team can debug at 3am.

## Referenced by

- [Reference index](README.md)
- [Repo index](../../INDEX.md)
