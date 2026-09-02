---
title: Fundamentals index
type: index
track: universal
tier: P0
status: drafted
updated: 2026-09-02
tags: [index, fundamentals]
---

# Fundamentals — one mechanism per file

Atomic mechanism pages, written to the staff contract: internals, real arithmetic, failure modes
with cited incidents, and the trade-off against the alternatives. **No 101 sections.** If you want
the shorter interview-layer version of a topic, the older bundled notes are still in
[../02-primitives/](../02-primitives/README.md) until each one is fully split.

This folder replaces `02-primitives/` file by file, per
[ADR-0001](../../docs/adr/0001-split-primitives-into-atomic-fundamentals.md). A primitive file is
deleted only once every topic it carries has a page here.

## Where to look

| Question | File |
|---|---|
| What does "strongly consistent" actually cost, in round trips? CAP stated correctly, PACELC, session guarantees, read paths | [consistency-models.md](consistency-models.md) |
| Why did snapshot isolation let two doctors go off call? MVCC internals, write skew, SSI aborts, the MySQL/Postgres split | [transaction-isolation-levels.md](transaction-isolation-levels.md) |
| How does a group agree despite failures? Raft internals, membership-change bugs, quorum placement across regions | [consensus-raft-paxos.md](consensus-raft-paxos.md) |
| Why is my distributed lock not mutual exclusion? Leases, the zombie holder, fencing tokens, Redlock | [leases-locks-and-fencing.md](leases-locks-and-fencing.md) |
| What does `R + W > N` really promise? Sloppy quorums, read repair, Merkle repair, tombstone resurrection | [quorums-and-anti-entropy.md](quorums-and-anti-entropy.md) |
| Which key do I shard on, and which query did I just make expensive? Scatter-gather maths, secondary indexes | [partitioning-strategies.md](partitioning-strategies.md) |
| How much data does a failover lose? Sync/semi-sync/async dial, RPO and RTO arithmetic, multi-leader conflicts | [replication-topologies.md](replication-topologies.md) |
| Why did the user's own comment disappear? The three anomalies, position-token routing, remote markers | [replication-lag-and-session-guarantees.md](replication-lag-and-session-guarantees.md) |
| One shard is at 100% and the cluster is at 20% | [hot-shard-mitigation.md](hot-shard-mitigation.md) |
| Ring, virtual nodes, bounded loads, rendezvous vs Maglev vs jump hash | [consistent-hashing.md](consistent-hashing.md) |
| B-tree vs LSM internals, compaction, write stalls, amplification arithmetic | [storage-engines.md](storage-engines.md) |
| Why is the planner ignoring my index? Composite order, cardinality errors, reading a plan | [indexing-and-query-planning.md](indexing-and-query-planning.md) |
| Where to cache, which pattern, how big, and what the miss path costs | [caching-strategies.md](caching-strategies.md) |
| The stale-set race, versioned keys, leases, CDC-driven invalidation | [cache-invalidation.md](cache-invalidation.md) |
| Stampede, hot key, penetration, cold start — and why they don't self-recover | [cache-failure-modes.md](cache-failure-modes.md) |
| Queue or log? Replay, fan-out, per-message retry, retention as a recovery bound | [log-vs-queue.md](log-vs-queue.md) |
| ISR, `acks`, `min.insync.replicas`, rebalance protocols, compaction, KRaft | [kafka-internals.md](kafka-internals.md) |
| Why exactly-once delivery is impossible and exactly-once *effects* are not | [delivery-semantics.md](delivery-semantics.md) |
| Event time, watermarks, checkpoints, late data, state as your real RTO | [stream-processing-semantics.md](stream-processing-semantics.md) |
| Idempotency keys, the unknown outcome, foreign state mutations | [idempotency.md](idempotency.md) |
| Little's law, the utilisation knee, why 80% is the ceiling | [queueing-theory-basics.md](queueing-theory-basics.md) |
| Fan-out amplification, hedged and tied requests, why averages lie | [tail-latency.md](tail-latency.md) |
| Deadline propagation, retry budgets, jitter, the 27× amplifier | [timeouts-retries-backoff.md](timeouts-retries-backoff.md) |
| Goodput collapse, CoDel, adaptive LIFO, criticality classes | [load-shedding-and-admission-control.md](load-shedding-and-admission-control.md) |
| Why the system stays down after the trigger is gone | [cascading-and-metastable-failures.md](cascading-and-metastable-failures.md) |

## Written / planned

Batch 1 (the consistency cluster) is written. The full plan — 47 fundamentals pages with canonical
names, tiers and forbidden aliases — is in [../topics/manifest.md](../topics/manifest.md) §1.
**Read the manifest before creating any file here.**

| Batch | Files | State |
|---|---|---|
| 1 | consistency-models · transaction-isolation-levels · consensus-raft-paxos · leases-locks-and-fencing · quorums-and-anti-entropy | **done** |
| 2 | partitioning-strategies · replication-topologies · replication-lag-and-session-guarantees · hot-shard-mitigation · consistent-hashing | **done** |
| 3 | storage-engines · indexing-and-query-planning · caching-strategies · cache-invalidation · cache-failure-modes | **done** |
| 4 | log-vs-queue · kafka-internals · delivery-semantics · stream-processing-semantics · idempotency | **done** |
| 5 | timeouts-retries-backoff · load-shedding-and-admission-control · cascading-and-metastable-failures · tail-latency · queueing-theory-basics | **done** |
| 6 | patterns/: outbox · saga · distributed-transactions · materialized-views-and-derived-data · expand-contract-migration | next — **creates `patterns/`** |

**25 of 47 fundamentals written.** The batches build on each other: batch 1 is what correctness
costs, batch 2 is what splitting and copying data costs instead, batch 3 is the single node
underneath, batch 4 is what happens once the work is asynchronous, and batch 5 is what happens
when any of it is overloaded — five pages that are one argument: queueing explains the knee, tail
latency explains why fan-out hits it, retries explain how load multiplies past it, shedding is the
control, and metastability is what happens without one.

## How to use these

Design a case first ([../03-backend-cases/](../03-backend-cases/README.md)), notice the mechanism
you hand-waved, then read that page — specifically its **Numbers that matter** and **Failure
modes** sections. Those are the two that change how you answer, and the two that are missing from
every blog post on the same topic.

Each page ends with **Staff-level follow-ups**: multi-part questions with no definitional answer.
If you cannot answer them out loud in two minutes, the page is not finished with you yet.

## See also

- [../topics/manifest.md](../topics/manifest.md) — canonical topic list; check before creating a file
- [../diagrams/components.md](../diagrams/components.md) — shared Mermaid vocabulary
- [../CONVENTIONS.md](../CONVENTIONS.md) — file format contract
- [../02-primitives/README.md](../02-primitives/README.md) — the bundled notes being split

## Referenced by

- [Interview prep index](../README.md)
- [Primitives index](../02-primitives/README.md)
- [Repo index](../../INDEX.md)
