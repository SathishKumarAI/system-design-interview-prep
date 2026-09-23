---
title: Design a CDC pipeline (operational DB to analytics)
type: case
track: data
difficulty: advanced
status: drafted
sources: [Debezium docs, DDIA ch.11]
updated: 2026-09-23
tags: [cdc, debezium, upsert, schema-evolution, backfill]
---

# Design a CDC pipeline

> Replicate 200 tables from production Postgres/MySQL into the lakehouse, continuously,
> without touching the application and without breaking when someone runs a migration.
> **The hard part:** the snapshot-to-stream handover, upsert semantics on an append-oriented
> lake, and surviving schema changes you don't control.

## 1. Clarify

| Question | Assumed answer |
|---|---|
| Sources? | 20 Postgres + 5 MySQL databases, ~200 tables total |
| Freshness? | < 5 min for analytics; < 1 min for a few operational tables |
| Deletes? | Must propagate (GDPR + correctness) |
| Load on production? | **Strictly bounded** — this is someone else's production database |
| Schema changes? | Frequent, and we don't control them |
| History? | Keep the full change history, not just current state |

**Non-goals:** the application, dual-writes, replacing the source database.

## 2. Requirements

**Functional**
- Initial snapshot of every table, then continuous change capture
- Inserts, updates and deletes reflected in target tables within the SLA
- Handle schema evolution without a pipeline outage
- Re-snapshot a single table on demand (correction path)

**Non-functional**

| Target | Value |
|---|---|
| Freshness | p95 < 5 min end to end |
| Source impact | < 5% additional load; **zero blocking locks** |
| Correctness | Target matches source; verifiable by row-count and checksum reconciliation |
| Availability | Recover from any component failure without data loss |

## 3. Estimates

```
200 tables, 5B rows total, 50M changes/day ≈ 580 changes/s avg, ~5k/s peak
Change event ~2 KB (before + after images + metadata) → ~100 GB/day into Kafka
Initial snapshot: 5B rows × 500 B = 2.5 TB, at 50 MB/s ≈ 14 hours   ← plan for it, chunk it
WAL retention on source: must exceed max connector downtime.
   At 100 GB/day of WAL, a 24 h buffer = 100 GB of disk on a production DB — negotiate this
   with the DBA before designing anything else.
```

> [!info] The scary number
> **WAL retention.** If the connector is down longer than the source retains its log, you
> cannot resume — you must re-snapshot. That single operational constraint drives the whole
> reliability design.

## 4. API / contract

Debezium-style change event (know this shape):

```json
{
  "op": "c|u|d|r",                  // create, update, delete, read(=snapshot)
  "before": { ...row... },          // null for inserts
  "after":  { ...row... },          // null for deletes
  "source": { "db":"orders","table":"line_items","lsn":42983,"ts_ms":...,"snapshot":"false" },
  "ts_ms": 1735689600000
}
```

Kafka topic per table (`cdc.orders.line_items`), **key = primary key** — which gives per-row
ordering, and makes log compaction produce a current-state snapshot for free.

## 5. Data model

| Layer | Table | Semantics |
|---|---|---|
| Bronze | `cdc_raw.<table>` | Every change event, append-only, partitioned by ingest day |
| Silver | `dw.<table>` | **Current state** — upsert/merge target, mirrors the source |
| Silver | `dw.<table>_history` | SCD Type 2: `valid_from`, `valid_to`, `is_current` |

Keeping both is deliberate: analysts want current state, but "what was this customer's plan
on the day they churned" needs history, and you cannot reconstruct history you didn't keep.

**Iceberg merge-on-read vs copy-on-write** — the key operational choice:

| | Copy-on-write | Merge-on-read |
|---|---|---|
| Write | Rewrites whole data files on update | Writes small delete + data files |
| Read | Fast | Slower — merges deletes at query time |
| Fits | Low update rate, read-heavy | **High update rate — CDC** |

Use merge-on-read for CDC targets, with **frequent compaction** to keep read amplification
bounded. That compaction schedule is not optional.

## 6. Architecture

Drawn out, the reconciliation loop back to the connector is the piece that makes this operable:

```mermaid
flowchart LR
    pg[("Postgres x 20<br/>logical replication slot")]
    my[("MySQL x 5<br/>binlog, ROW format")]
    dbz["Debezium connectors<br/>Kafka Connect cluster"]
    sh[["Schema history topic<br/>the connector's own state"]]
    k[["Kafka, one topic per table<br/>key = primary key, 200 topics"]]
    br["Bronze sink"]
    sl["MERGE job"]
    bronze[("cdc_raw tables<br/>append-only, by ingest day")]
    silver[("dw tables + SCD2 history<br/>merge-on-read")]
    cmp["Compaction + snapshot expiry"]
    rec["Nightly reconciliation<br/>row counts + sampled checksum"]
    q["Trino, warehouse, ML feature pipelines"]

    pg ==> |"WAL, under 5% added load, zero blocking locks"| dbz
    my ==> |"binlog"| dbz
    dbz -.-> |"one entry per DDL, versioned"| sh
    dbz --> |"op c/u/d/r, before + after, LSN — ~2 KB, 5k/s peak"| k
    k ==> |"every event, unchanged"| br
    br --> |"raw, replayable"| bronze
    k ==> |"keyed by PK, so per-row order holds"| sl
    sl --> |"upsert current state, close the SCD2 row"| silver
    silver --> |"read amplification stays bounded"| cmp
    cmp --> |"p95 freshness under 5 min"| q
    silver -.-> |"counts and checksums against the source"| rec
    rec -.-> |"drift over threshold triggers a per-table re-snapshot"| dbz

    classDef service fill:#fff,stroke:#5f6368,color:#111
    classDef store fill:#fef7e0,stroke:#f9ab00,color:#111
    classDef queue fill:#f3e8fd,stroke:#a142f4,color:#111
    classDef external fill:#f1f3f4,stroke:#9aa0a6,color:#111,stroke-dasharray:4 3
    class dbz,br,sl,cmp,rec,q service
    class bronze,silver store
    class k,sh queue
    class pg,my external
```

### Deep dive A — snapshot to stream, without losing or duplicating

The classic failure is a gap or an overlap between the initial snapshot and the stream.

- **Naive**: lock the table, snapshot, start streaming. Correct, and unacceptable — you just
  locked production.
- **Standard**: open the replication slot **first** (so changes accumulate from LSN X), then
  snapshot with a consistent read, then replay the stream from X. Changes during the snapshot
  are applied on top. Requires upsert-idempotent targets, which you have.
- **Incremental snapshotting (Debezium DDD-3 / watermark-based)**: chunk the table by primary
  key and interleave chunks with the live stream, using low/high watermarks to resolve
  conflicts between a chunk row and a concurrent change. **No long transaction, no lock,
  resumable, and re-snapshottable per table on demand.** This is the answer for a 2.5 TB
  source.

> [!tip] Say this
> "Incremental snapshotting by key range, interleaved with the live stream and resolved with
> watermarks. It never holds a long transaction on production, it resumes after a failure,
> and it lets me re-snapshot one table without touching the other 199."

### Deep dive B — schema evolution you don't control

Someone drops a column at 2am. The pipeline must not page you.

- Debezium keeps a **schema history topic**; events carry their schema version.
- Sink rules: **new column → add it (nullable)**; dropped column → keep it, stop populating
  (never delete history); **type change → the dangerous one**: land into a new column
  (`col_v2`) and reconcile, rather than failing or silently coercing.
- Incompatible changes route to a **dead-letter topic** with an alert instead of crashing the
  connector. A stopped connector risks the WAL-retention cliff, which is far worse than a few
  quarantined rows.
- **Data contracts** are the real fix: schema changes on replicated tables go through a review
  that includes the data team, and the producer's CI checks compatibility. Say this — it's an
  organisational answer to an organisational problem, and staff-level candidates give it.

Following one such change through, with the two tempting wrong answers marked:

```mermaid
sequenceDiagram
    autonumber
    participant A as App team
    participant S as Source DB
    participant C as Connector
    participant K as Kafka topic
    participant M as Sink MERGE job
    participant T as Target table

    Note over A,S: 02:00 — ALTER TABLE line_items ALTER amount TYPE numeric
    A->>S: the migration lands. Nobody told the data team.
    S->>C: DDL arrives on the WAL like any other change
    C->>C: record the new schema version in the schema history topic
    Note over C: this is why the connector carries its own state:<br/>events before and after this point describe<br/>DIFFERENT shapes of the same table.
    C->>K: events now carry amount as numeric, schema v7

    rect rgb(255,240,240)
    Note over M,T: the two tempting wrong answers
    M--xM: fail the connector. The WAL now accumulates on a<br/>production disk, and the retention cliff is a far<br/>worse outage than a few bad rows.
    M--xT: coerce numeric into the old bigint column. Silent<br/>precision loss, green pipeline, nobody alerted.
    end

    rect rgb(240,255,240)
    Note over M,T: the rule set
    M->>T: new column, add it nullable. Dropped column, keep it<br/>and stop populating — never delete history.
    M->>T: type change, land into amount_v2 and reconcile
    M-->>K: anything genuinely incompatible goes to a dead-letter<br/>topic with an alert, and the connector keeps running.
    end

    Note over A,T: none of which is the real fix. The real fix is a data<br/>contract that fails the PRODUCER's CI, so 02:00 never happens.
```

### Deep dive C — deletes, tombstones and GDPR

- A delete event carries `before` and a null `after`. Apply as a delete in the current-state
  table; in the history table, close the SCD2 row (`valid_to = now`, `is_current = false`).
- **Hard delete for GDPR erasure** must reach: bronze raw events, silver current, history,
  every downstream mart, the search index, and backups. Design the deletion path *before* you
  need it — this is where append-only lakes hurt most, and Iceberg row-level deletes plus a
  documented backup expiry policy are the answer.
- **Soft deletes in the source** look like updates — don't assume `op:"d"` is the only way a
  row dies.

### Deep dive D — verification

CDC that silently drifts is worse than no CDC, because people trust it.

- Nightly reconciliation: row counts per table, plus a checksum over a sampled key range
  (`sum(hash(pk || updated_at))`) compared source vs target.
- Alert on drift; auto-trigger a per-table incremental re-snapshot when drift exceeds a
  threshold. **Having a cheap re-snapshot button is the single most valuable operational
  feature of a CDC platform.**
- Track end-to-end lag as `now - source.ts_ms` at the sink, not connector-internal metrics.

## 7. Scale & failure

| Breaks first at 10x | Fix |
|---|---|
| Single Kafka Connect worker per DB | Distributed Connect cluster, tasks per table group |
| MERGE cost on wide tables | Merge-on-read + compaction; batch merges every N minutes |
| Replication slot lag on the source | Alert on slot lag **in bytes** (this can fill the production disk and take down the app — the highest-severity failure in this whole design) |
| Topic count (200+) | Group small tables into shared topics with a table field |

| Component fails | Blast radius | Degraded behaviour |
|---|---|---|
| Connector down < WAL retention | Lag grows | Resume from stored offset; no loss |
| Connector down > WAL retention | **Cannot resume** | Re-snapshot that table (incremental, hours) — and treat as an incident |
| Source failover to a replica | LSN/binlog position changes | Connector must handle failover (`pg_failover_slots`, GTID for MySQL); may need a re-snapshot |
| Sink job fails | Target stale | Restart from checkpoint; bronze retains everything |
| Bad schema change | Quarantined events | DLQ + alert; fix mapping, replay from bronze |

## 8. Ops & cost

- **SLA:** freshness p95 < 5 min per table, published; drift = 0 verified nightly.
- **Alert on:** replication slot lag in bytes (page-worthy — it threatens production),
  end-to-end lag per table, DLQ depth, reconciliation drift, snapshot job progress.
- **Rollout:** new tables onboard through a template (connector config + sink job + tests +
  SLA entry). Onboarding a table should be a config change, not a project.
- **Cost:** Kafka storage and merge compute dominate. Levers: exclude columns nobody queries
  (especially large JSON/blob columns — often most of the bytes), longer merge intervals for
  cold tables, compaction tuning.
- **First thing I'd cut:** history (SCD2) for tables where nobody has ever queried it —
  measure before assuming.

## On AWS and Azure

| | AWS | Azure |
|---|---|---|
| **The shape** | AWS DMS CDC tasks, or Debezium on MSK Connect → MSK/Kinesis (topic per table, key = PK) → Glue/EMR merge job → **S3 Tables** (Iceberg) with Glue Data Catalog; Athena and Redshift read it | **No first-party Debezium host.** Run the connector yourself on Container Apps or AKS → Event Hubs (Kafka protocol) → Fabric or Databricks merge job → Delta/Iceberg in ADLS Gen2. Data Factory and Fabric cover the batch-shaped extraction, not the log-shaped one |
| **What you turn on first** | **`rds.logical_replication` in the DB *cluster* parameter group. "This static parameter requires a reboot of the DB instance to take effect"** — so the "zero impact on production" requirement starts with a scheduled restart. Setting it also raises `wal_level`, `max_wal_senders`, `max_replication_slots` and `max_connections`, which increases WAL generation | `wal_level = logical`, `max_worker_processes` to **at least 16** (or you get `WARNING: out of background worker slots`), then `ALTER ROLE <admin> WITH REPLICATION`, then **restart the server** |
| **The default that bites** | DMS ships `HeartbeatEnable` specifically to stop an idle slot pinning old WAL — and its **default value is `false`**. A CDC task that is caught up and quiet lets `restart_lsn` sit still, which is the storage-full scenario this case's WAL-retention estimate is about, arriving through inactivity rather than lag | The platform intervenes, and that is worse in one exact way: the server **"automatically switches to read-only mode when the storage usage reaches 95 percent, or when the available capacity is less than 5 GiB"**, and an unused slot is then **automatically dropped**. That saves the database and silently amputates your pipeline — your resume point is gone and the answer is a full re-snapshot |
| **The one nobody expects** | Streams have their own retention; a relay down over a long weekend against a 24-hour retention has lost events with no error anywhere | **On PostgreSQL 16 and earlier, "logical replication slots aren't preserved during failover events"** on an HA-enabled flexible server. A routine failover re-snapshots 5 B rows unless you run the PG Failover Slots extension; PostgreSQL 17+ syncs slots natively, and only for slots created with the failover option |
| **The merge target** | **S3 Tables run maintenance for you** — "S3 continuously performs automatic maintenance operations, such as compaction, snapshot management, and unreferenced file removal." The merge-on-read compaction schedule this case calls mandatory becomes a configuration rather than a job you operate | Compaction on Delta/Iceberg in ADLS is yours: `OPTIMIZE`/`VACUUM` on a schedule you own and monitor |

The WAL-retention risk this case names as *the* operational constraint appears on both clouds with
opposite failure modes, and that contrast is the thing to carry into a room: **AWS lets the slot
fill the disk and gives you an off-by-default heartbeat to prevent it; Azure protects the disk by
deleting your slot.** One is a storage incident, the other is a silent data-loss incident, and the
runbook is different for each.

## In an LLM deployment

CDC is the correct substrate for keeping a vector index current, and the case's existing shape
needs almost nothing added: the change event already carries `op`, `before` and `after`, so
`c`/`u` re-embeds the row and `d` deletes the vector. That last one matters more than it looks —
**an embedding derived from a deleted row is a copy of that row**, so a GDPR erasure that does not
propagate to the index has not erased anything. This case's §Deep dive C on deletes and tombstones
becomes a compliance requirement for a second store.

Two economics changes. A re-embed is a **billed model call**, so the at-least-once delivery that
costs you a duplicate row today costs money tomorrow — key the vector on
`(primary_key, source_lsn, model_version)` and the upsert is naturally idempotent, since
embeddings are deterministic for a fixed model and input. And the **re-snapshot path stops being
cheap**: a correction path that re-reads 5 B rows currently costs 14 hours of I/O; if every row
must be re-embedded it is 5 B inference calls, which is a budget line, not an afternoon.

The schema-evolution problem you do not control gets a new edge too. A column added upstream does
not break the pipeline, but it silently changes what the embedded text *means* if your template
concatenates columns. Pin the template to an explicit column list, version it alongside the model,
and treat a template change as a full re-embed — because that is what it is.

## Referenced by

- [Cache invalidation](../fundamentals/cache-invalidation.md)
- [Data platform cases index](README.md)
- [Log vs queue](../fundamentals/log-vs-queue.md)
- [Materialized views and derived data](../patterns/materialized-views-and-derived-data.md)
- [Outbox pattern](../patterns/outbox-pattern.md)
- [Question bank](../07-drills/question-bank.md)
- [Repo index](../../INDEX.md)

## Sources

- [Debezium — incremental snapshots (DDD-3)](https://debezium.io/documentation/reference/stable/connectors/postgresql.html)
- [Netflix — DBLog: a generic change-data-capture framework](https://netflixtechblog.com/dblog-a-generic-change-data-capture-framework-69351fb9099b)
- Local book: `DE/System-Design/Designing Data Intensive Applications.pdf` — ch.11 (change data capture)
- [Apache Iceberg — row-level deletes, merge-on-read](https://iceberg.apache.org/docs/latest/)

Cloud claims in §On AWS and Azure (all verified 2026-09-21):

- [AWS — using a PostgreSQL database as an AWS DMS source](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.PostgreSQL.html) — `rds.logical_replication` is a static cluster parameter requiring a reboot and raises `wal_level`/`max_wal_senders`/`max_replication_slots`/`max_connections`; `HeartbeatEnable` defaults to `false` and keeps `restart_lsn` moving
- [AWS — working with Amazon S3 Tables and table buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables.html) — Iceberg table buckets with continuous automatic compaction, snapshot management and unreferenced file removal
- [Azure — logical replication and logical decoding on PostgreSQL flexible server](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-logical) — `wal_level = logical`, `max_worker_processes` ≥ 16, `ALTER ROLE … WITH REPLICATION` and a restart; read-only at 95% storage or under 5 GiB free; automatic drop of unused slots; slots not preserved across HA failover on PostgreSQL 16 and earlier
- [AWS — DynamoDB Streams](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html) — 24-hour stream retention, for the managed change-feed alternative
