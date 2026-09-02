---
title: Storage and databases
type: primitive
track: universal
difficulty: core
status: drafted
sources: [DDIA ch.2-3, system-design-primer]
updated: 2026-09-02
tags: [sql, nosql, lsm, btree, indexes]
---

# Storage and databases

## What it is

The choice that is hardest to reverse. Pick by **access pattern**, never by popularity.

## The one question that picks the store

> *"What are my top three queries, and what is the write pattern?"*

| Access pattern | Store | Why |
|---|---|---|
| Arbitrary joins, transactions, moderate scale | **Relational** (Postgres, MySQL) | ACID, mature, joins are free. Default until proven insufficient |
| Huge write volume, known key, no joins | **Wide-column** (Cassandra, Scylla, Bigtable) | LSM writes, linear scale, tunable consistency |
| Key → blob, sub-ms, ephemeral | **KV** (Redis, DynamoDB) | Simplest possible contract |
| Flexible/nested documents, per-document access | **Document** (MongoDB, DocumentDB) | Schema flexibility; joins are your problem |
| Full-text, faceting, relevance | **Search** (Elasticsearch/OpenSearch) | Inverted index. Never your source of truth |
| Analytics over columns, scans of billions of rows | **Columnar/OLAP** (ClickHouse, BigQuery, Snowflake, Redshift, DuckDB) | Column pruning + compression = 10–100x on aggregates |
| Relationships as first-class (friends-of-friends, fraud rings) | **Graph** (Neo4j) | Traversals cheap; scaling is genuinely hard |
| Time-ordered metrics, high ingest, downsampling | **Time-series** (Prometheus, InfluxDB, Timescale) | Time partitioning + rollups built in |
| Vector similarity for embeddings | **Vector** (pgvector, Pinecone, Milvus, Qdrant) | ANN index; see [../06-ml-cases/rag-assistant.md](../06-ml-cases/rag-assistant.md) |
| Large immutable blobs | **Object store** (S3-class) | 11 nines durability, cheap, ~100 ms first byte |

> [!tip] Interview line
> "Postgres does all of this at our scale — 10k writes/s and 2 TB. I'd start there and
> keep the option to move the event table to Cassandra when writes cross ~50k/s. Choosing
> Cassandra now buys us scale we don't need and costs us joins we do."

## B-tree vs LSM — the trade-off behind every store

| | B-tree (Postgres, MySQL InnoDB) | LSM tree (Cassandra, RocksDB, Scylla) |
|---|---|---|
| Writes | In-place update, random IO, write to WAL first | Append to memtable + WAL, flush sorted files |
| Write throughput | Lower | **Much higher** |
| Reads | Predictable, ~log n, one place | May check several SSTables; Bloom filters help |
| Space | Fragmentation | Better compression, but compaction rewrites |
| The pain | Write amplification from page splits | **Compaction**: background IO storms, disk 2x headroom, read latency spikes |

**Say this:** "LSM buys write throughput and pays with compaction. If our write pattern is
bursty, compaction debt accumulates during the burst and we get a latency cliff after it —
so I'd want compaction throughput monitored as a first-class metric."

## Indexes

- An index is a **write tax paid for a read discount**. Every index slows every write.
- **Composite index order matters**: `(user_id, created_at)` serves "this user's posts,
  newest first" and "this user's posts". It does *not* serve "all posts newest first".
- **Covering index** = query answered from the index alone, no table lookup. Big win.
- **Cardinality**: an index on a boolean is usually useless (the planner will ignore it).
- **Partial index** for the 2% of rows you actually query (`WHERE status='pending'`) — tiny
  and hot.
- Say the index next to each API endpoint in the data model section. That's the level of
  concreteness interviewers score.

## Normalisation vs denormalisation

| | Normalise | Denormalise |
|---|---|---|
| Optimises | Write correctness, storage, one place to update | Read latency, fewer joins/round trips |
| Costs | Joins at read time | Write amplification, consistency risk, fan-out updates |
| Use for | Transactional core (orders, accounts) | Read-heavy views (feed entries, product cards) |

Standard resolution: **normalised source of truth + denormalised derived views**, kept in
sync asynchronously via the changelog. This is the pattern behind feeds, search indexes,
and OLAP tables alike. See [messaging-and-streams.md](messaging-and-streams.md).

## Schema evolution

- Additive changes only, in this order: add nullable column → backfill → dual-write →
  switch reads → stop writing old → drop column. Each step deployable and revertible alone.
- Never a blocking `ALTER` on a big table in a hot path — `pg_repack`/`gh-ost`-style online
  migrations, or add-and-backfill.
- Forward and backward compatibility at the *encoding* layer (Protobuf/Avro field numbers)
  because during a rollout both versions run at once. This is DDIA ch.4 and it comes up
  constantly in real work, less often in interviews — mentioning it reads as experience.

## Failure modes

| Failure | Symptom | Mitigation |
|---|---|---|
| Connection exhaustion | "too many clients"; app-wide stall | Connection pooler (PgBouncer), cap per service |
| Long-running transaction | Bloat, vacuum can't advance, replication lag | Statement timeouts, no user input inside a transaction |
| Hot partition | One shard at 100% | Better partition key, salting; see [replication-and-partitioning.md](replication-and-partitioning.md) |
| Unbounded table growth | Queries degrade slowly, then a cliff | Partition by time, TTL/archive policy from day one |
| Failover loses writes | Data loss on promotion | Synchronous replication for the critical table, or accept and document RPO |
| Backup never restored | Discover at the worst moment | Restore drills on a schedule; an untested backup is not a backup |

## Interview lines

> [!tip] Say this
> "Source of truth is Postgres. Search, feed and analytics are **derived** stores fed from
> its changelog — so they can be rebuilt from scratch, and a bug in the derived path is
> never a data-loss bug."

> [!tip] Say this
> "That query needs `(tenant_id, created_at DESC)`. Without it we scan the tenant's whole
> history for every page load, which is fine at 1k rows and fatal at 10M."

## Numbers

| Quantity | Order of magnitude |
|---|---|
| Postgres indexed read | 0.1–1 ms; ~10k qps/node |
| Postgres write (fsync) | ~1 ms; 1k–10k tps |
| Cassandra write | ~1 ms; 10k–100k/s/node |
| Columnar scan | 100 M–1 B rows/s/node on a few columns |
| Object store first byte | ~100 ms; throughput ~GB/s parallel |
| Practical single-node relational dataset | Low TB before sharding hurts |

## Sources & further reading

- Local book: `DE/System-Design/Designing Data Intensive Applications.pdf` — ch.2 (data models), ch.3 (storage engines), ch.4 (encoding)
- Local book: `DE/SQL-Databases/Database Design and Modeling with PostgreSQL and MySQL ...pdf`
- Repo notes: [../../basic/prep/SQL%20or%20NoSQL.md](../../basic/prep/SQL%20or%20NoSQL.md), [../../basic/prep/Denormalization.md](../../basic/prep/Denormalization.md), [../../basic/prep/SQL%20tuning.md](../../basic/prep/SQL%20tuning.md)
- Vendor: `10-resources/vendor/system-design-primer/README.md` — SQL/NoSQL section
