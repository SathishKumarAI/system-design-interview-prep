---
title: Messaging and streams
type: primitive
track: universal
difficulty: core
status: drafted
sources: [DDIA ch.11, Kafka docs]
updated: 2026-09-02
tags: [kafka, queue, streaming, backpressure, delivery-semantics]
---

# Messaging and streams

## What it is

A buffer between producer and consumer that decouples them in **time** (bursts), in
**availability** (consumer down ≠ producer fails), and in **rate** (fast producer, slow
consumer).

Pays with: added latency, duplicates, ordering constraints, lag as a new failure mode, and
one more system to operate.

## Queue vs log — the distinction to get right

| | **Queue** (SQS, RabbitMQ, Celery) | **Log** (Kafka, Pulsar, Kinesis, Redpanda) |
|---|---|---|
| Message after consumption | Deleted | Retained for a window; consumers hold offsets |
| Consumers | Compete for messages | Independent groups replay the same stream |
| Ordering | Per-queue, weak (SQS FIFO is a special mode) | Strict **per partition** |
| Replay | No | Yes — reset the offset |
| Fan-out to N systems | N queues, producer knows them | One topic, N consumer groups. Producer knows nobody |
| Use for | Task dispatch, work distribution, retries with DLQ | Event backbone, CDC, stream processing, rebuilding derived stores |

> [!tip] Interview line
> "I want a log, not a queue, because search, analytics and the feed builder all need the
> same events, and I want to rebuild the search index by replaying rather than backfilling
> from the database."

## Kafka mental model (the parts that come up)

- **Topic → partitions**; ordering is guaranteed **only within a partition**. Partition key
  choice is the same problem as a shard key — see
  [replication-and-partitioning.md](replication-and-partitioning.md).
- **Consumer group**: each partition assigned to exactly one consumer in the group.
  **Max useful parallelism = partition count.** Over-partition slightly at creation, because
  increasing partitions later breaks key→partition stability.
- **Offsets** are the consumer's bookmark; commit *after* processing for at-least-once,
  *before* for at-most-once.
- **Rebalance**: a consumer joining/leaving reassigns partitions and pauses consumption.
  Frequent rebalances (slow processing exceeding `max.poll.interval.ms`) look like an outage.
  Use cooperative sticky assignment.
- **Retention**: time-based or size-based; **log compaction** keeps only the latest value per
  key — which makes a topic a durable, replayable *table*.
- **Durability knobs**: `acks=all` + `min.insync.replicas=2` + RF 3. `acks=1` is faster and
  loses data on leader failure. Say which you chose and why.

## Delivery semantics

| Semantic | Reality |
|---|---|
| At-most-once | Commit before processing. Loses messages. Fine for metrics samples |
| **At-least-once** | Commit after processing. Duplicates on retry. **The default you should assume** |
| Exactly-once *delivery* | Impossible across a network in general |
| Exactly-once *effect* | Achievable: at-least-once delivery + **idempotent consumer**, or transactional writes within one system (Kafka transactions, Flink checkpoint + 2PC sink) |

> [!warning] Trap
> Saying "we'll use exactly-once." Say **"at-least-once delivery with idempotent
> processing, which gives exactly-once *effects*"** — then explain the dedup key. That one
> phrase is a senior signal.

See [transactions-and-idempotency.md](transactions-and-idempotency.md).

## Backpressure and lag

- **Consumer lag** (messages or seconds behind) is the health metric for the whole async
  side of your system. Alert on it, graph it, and know the recovery rate.
- If consumers can't keep up: scale consumers (up to partition count), batch, make processing
  cheaper, or **shed** (drop low-priority events knowingly rather than fall over).
- **Backpressure** must be explicit. An unbounded in-memory buffer between a fast producer
  and a slow consumer is an OOM with extra steps.
- **Priority**: separate topics per priority beats a priority queue — a slow low-priority
  consumer then can't block high-priority work.

## Poison messages and DLQ

- Retries with backoff, then move to a **dead-letter queue** after N attempts. Without a DLQ,
  one malformed message blocks its partition forever.
- The DLQ needs an owner, an alert and a replay tool. A DLQ nobody looks at is just a slow
  data-loss mechanism.

## Stream processing

| Concept | What to say |
|---|---|
| **Event time vs processing time** | Always aggregate on event time; processing time gives wrong answers when anything is delayed |
| **Watermark** | "We assume no events older than 5 minutes; later ones go to a late-data path" |
| **Windows** | Tumbling (fixed), hopping (overlapping), sliding, session (gap-based) |
| **State** | Local state store (RocksDB) + checkpoints; state size drives your instance sizing |
| **Checkpointing** | Flink checkpoints + a 2PC sink give exactly-once into Iceberg/JDBC |
| **Stream–table duality** | A compacted log *is* a table; a table's changelog *is* a stream |

Engines: Flink (rich state, event time, exactly-once sinks), Kafka Streams (library, no
cluster), Spark Structured Streaming (micro-batch, good if you already run Spark).
See [../05-data-cases/](../05-data-cases/README.md).

## Outbox pattern (say this whenever a design writes to DB *and* publishes an event)

Writing to the database and publishing to Kafka are two systems: the process can die between
them. Fix: write the event into an `outbox` table **in the same transaction** as the state
change; a relay (or CDC on that table) publishes it. At-least-once, no lost events, no 2PC.

## Failure modes

| Failure | Symptom | Mitigation |
|---|---|---|
| Consumer lag grows unbounded | Downstream data hours stale | Alert on lag; autoscale to partition count; shed |
| Rebalance storm | Consumption stalls repeatedly | Cooperative rebalancing, raise poll interval, make processing faster |
| Hot partition | One consumer at 100% | Better partition key, salting; accept ordering loss where allowed |
| Duplicate processing | Double charges, double emails | Idempotency key + dedup store |
| Broker disk full | Producers blocked, cluster wedged | Retention policy, disk alerts, quotas |
| Schema change breaks consumers | Deserialization failures across the fleet | Schema registry + compatibility rules (backward by default) |

## Interview lines

> [!tip] Say this
> "Partition by `user_id` so a user's events stay ordered, and accept that global ordering
> doesn't exist. Nothing in the requirements needs global order — only per-user order."

> [!tip] Say this
> "Kafka here is the durability boundary: once the write is acknowledged into the log, the
> API can return 202 and everything downstream is replayable. That converts a distributed
> transaction problem into a retry problem."

## Numbers

| Quantity | Order of magnitude |
|---|---|
| Kafka broker throughput | 100k–1M msg/s, 100+ MB/s |
| Kafka end-to-end latency | 5–50 ms typical |
| Partitions per cluster | Thousands fine; tens of thousands is a tuning project |
| SQS | Effectively unlimited, ~10–100 ms, 256 KB max message |
| Typical retention | 7 days (replay window = how long you can be wrong for) |

## Referenced by

- [Books already on this machine](../10-resources/books-on-this-machine.md)
- [Data engineering design playbook](../05-data-cases/data-playbook.md)
- [Design a news feed](../03-backend-cases/news-feed.md)
- [Design a notification system](../03-backend-cases/notification-system.md)
- [Design search and typeahead](../03-backend-cases/search-typeahead.md)
- [Primitives index](README.md)
- [Storage and databases](storage-and-databases.md)

## Sources & further reading

- Local book: `DE/System-Design/Designing Data Intensive Applications.pdf` — ch.11 (stream processing), ch.10 (batch)
- Repo notes: [../../basic/prep/Asynchronism.md](../../basic/prep/Asynchronism.md), [../../data%20engineering/](../../data%20engineering/) (Kafka, Kinesis, Event Hub notes)
- Vendor: `10-resources/vendor/system-design-primer/README.md` — asynchronism
- [Kafka documentation — design](https://kafka.apache.org/documentation/#design)
- [Confluent — exactly-once semantics](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/)
