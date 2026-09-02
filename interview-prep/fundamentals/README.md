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

## Written / planned

Batch 1 (the consistency cluster) is written. The full plan — 47 fundamentals pages with canonical
names, tiers and forbidden aliases — is in [../topics/manifest.md](../topics/manifest.md) §1.
**Read the manifest before creating any file here.**

| Batch | Files | State |
|---|---|---|
| 1 | consistency-models · transaction-isolation-levels · consensus-raft-paxos · leases-locks-and-fencing · quorums-and-anti-entropy | **done** |
| 2 | partitioning-strategies · replication-topologies · replication-lag-and-session-guarantees · hot-shard-mitigation · consistent-hashing | **done** |
| 3 | storage-engines · indexing-and-query-planning · caching-strategies · cache-invalidation · cache-failure-modes | next |
| 4 | log-vs-queue · kafka-internals · delivery-semantics · stream-processing-semantics · idempotency | planned |

**10 of 47 fundamentals written.** The two batches pair deliberately: batch 1 is what correctness
costs, batch 2 is what happens when you split and copy data to avoid paying it.

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
