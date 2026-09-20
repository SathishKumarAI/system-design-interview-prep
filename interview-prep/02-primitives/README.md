---
title: Primitives index
type: index
track: universal
status: drafted
updated: 2026-09-02
tags: [index]
---

# Primitives — the building blocks

Twelve files. Each one answers: *what is it, when do I reach for it, what does it cost me,
how does it fail, what do I say about it in an interview.*

> [!info] Being split into [../fundamentals/](../fundamentals/README.md)
> Each file here bundles 3–6 topics, which caps how deep any of them goes. They are being
> replaced by one page per mechanism, written to the staff contract
> ([ADR-0001](../../docs/adr/0001-split-primitives-into-atomic-fundamentals.md)). A file here is
> deleted only when every topic it carries has a successor page. Split so far:
> `consistency-and-consensus.md`, `replication-and-partitioning.md`, `caching.md` and
> `storage-and-databases.md` → fifteen pages in `fundamentals/`. All four source files stay —
> each still holds at least one topic with no successor yet (clocks/CRDTs, rebalancing, Redis
> internals, store selection and schema evolution respectively).

## Where to look

| Question | File |
|---|---|
| How does the request reach me at all? DNS, anycast, CDN, TLS, HTTP/3, WebSocket, gRPC | [networking-and-edge.md](networking-and-edge.md) |
| L4 vs L7, gateways, service mesh, routing, sticky sessions | [load-balancing-and-gateways.md](load-balancing-and-gateways.md) |
| Where to cache, eviction, invalidation, stampedes, hot keys | [caching.md](caching.md) — **split**, see [../fundamentals/](../fundamentals/README.md) |
| SQL vs NoSQL, B-tree vs LSM, which store for which access pattern | [storage-and-databases.md](storage-and-databases.md) — **partly split**, see [../fundamentals/](../fundamentals/README.md) |
| Leader/follower, quorums, sharding, consistent hashing, rebalancing | [replication-and-partitioning.md](replication-and-partitioning.md) — **split**, see [../fundamentals/](../fundamentals/README.md) |
| CAP/PACELC, isolation levels, Raft, leases, clocks | [consistency-and-consensus.md](consistency-and-consensus.md) — **split**, see [../fundamentals/](../fundamentals/README.md) |
| Queues vs logs, Kafka, delivery semantics, ordering, backpressure | [messaging-and-streams.md](messaging-and-streams.md) |
| Idempotency, sagas, outbox, exactly-once *effects*, ledgers | [transactions-and-idempotency.md](transactions-and-idempotency.md) |
| Timeouts, retries, circuit breakers, bulkheads, load shedding, DR | [reliability-patterns.md](reliability-patterns.md) |
| SLOs, RED/USE, tracing, canary, feature flags, on-call | [observability-and-delivery.md](observability-and-delivery.md) |
| AuthN/AuthZ, secrets, tenancy isolation, abuse, privacy | [security-and-multitenancy.md](security-and-multitenancy.md) |
| Where the money goes and how to cut it | [cost-engineering.md](cost-engineering.md) |

## How to study these

Don't read them front to back. **Design a case first**
([03-backend-cases/](../03-backend-cases/README.md)), notice the component you fumbled,
then read that primitive. Knowledge you had to reach for sticks; knowledge you skimmed doesn't.

The concept notes in [../../basic/prep/](../../basic/prep/) are the longer background reading
(sourced from system-design-primer). These files are the **interview layer**: what to say,
what it costs, how it breaks.

## The meta-rule for all twelve

Every primitive here exists to trade one resource for another. Name the trade every time
you place a box:

| Primitive | Buys | Pays with |
|---|---|---|
| Cache | Latency, DB load | Staleness, invalidation bugs, memory cost |
| Replica | Read throughput, availability | Replication lag, split-brain risk |
| Shard | Write throughput, dataset size | Cross-shard queries, rebalancing, hot shards |
| Queue | Burst absorption, decoupling | Latency, duplicates, ordering complexity, lag |
| Index | Read speed | Write speed, storage |
| CDN | Latency, egress cost | Invalidation, cost of misses, staleness |
| Consensus | Correctness under partition | Latency, availability, operational pain |
| Denormalisation | Read speed | Write amplification, consistency risk |
| Microservice | Team autonomy, scaling in isolation | Network hops, partial failure, ops surface |

If you can't say what a box pays with, you don't yet understand why it's there.

## Referenced by

- [Fundamentals index](../fundamentals/README.md)
- [Interview prep index](../README.md)
- [Repo index](../../INDEX.md)
