---
title: Patterns index
type: index
track: universal
tier: P0
status: drafted
updated: 2026-09-02
tags: [index, patterns]
---

# Patterns — composed solutions, not mechanisms

A [fundamentals](../fundamentals/README.md) page explains **how a mechanism works**. A patterns
page explains **a shape you assemble from mechanisms**, and it must answer two questions a
mechanism page never has to:

> **When does this pattern earn its complexity, and what does applying it too early cost?**

That is the bar for every page here. A patterns page without those two answers is a mechanism page
in the wrong folder — patterns are adopted far more often than they are justified, and the failure
mode of this whole category is a team running a workflow engine to coordinate two tables in one
database.

## Where to look

| Question | File |
|---|---|
| How do I write to my database and publish an event atomically? | [outbox-pattern.md](outbox-pattern.md) |
| How do I coordinate a multi-step process across services without a distributed transaction? | [saga-pattern.md](saga-pattern.md) |
| When is 2PC actually the right answer, and where does it block? | [distributed-transactions.md](distributed-transactions.md) |
| Which of my stores can I safely delete and rebuild? | [materialized-views-and-derived-data.md](materialized-views-and-derived-data.md) |
| How do I change a schema or move a store with no downtime and a revert at every step? | [expand-contract-migration.md](expand-contract-migration.md) |
| Precompute timelines or merge at read? Where does the celebrity threshold sit? | [fanout-write-vs-read.md](fanout-write-vs-read.md) |
| How do I stop one tenant, or one bad deploy, from affecting everyone? | [cell-based-architecture.md](cell-based-architecture.md) |
| What does my product do when a dependency is down? | [graceful-degradation.md](graceful-degradation.md) |
| How do I stop spending threads on a dependency that is already failing? | [circuit-breaker.md](circuit-breaker.md) |
| I have to recompute six weeks of wrong data. How, without breaking production? | [backfill-and-reprocessing.md](backfill-and-reprocessing.md) |

## The through-line

These five are one argument about **atomicity you cannot have**:

1. You cannot atomically write to two systems → [outbox](outbox-pattern.md) moves the second write
   into the first system.
2. You cannot hold a transaction across services →
   [saga](saga-pattern.md) trades isolation for progress, and pays in compensations.
3. You *can* have real atomicity across partitions — [2PC](distributed-transactions.md) — but it
   blocks, and its availability is the product of every participant's.
4. Once data is spread across stores, most of them are
   [derived](materialized-views-and-derived-data.md) and rebuildable. Knowing which is which
   decides backups, paging and incident severity.
5. Changing any of it in production is
   [expand–contract](expand-contract-migration.md): a sequence of revertible steps, verified with
   real traffic.

**The answer that beats all five is a single-partition design.** Every page here says so, because
the cheapest distributed transaction is the one the data model made unnecessary.

## Written / planned

The full plan — 20 patterns pages with canonical names, tiers and forbidden aliases — is in
[../topics/manifest.md](../topics/manifest.md) §2. **Read the manifest before creating any file
here.**

| Batch | Files | State |
|---|---|---|
| 6 | outbox-pattern · saga-pattern · distributed-transactions · materialized-views-and-derived-data · expand-contract-migration | **done** |
| 7 | fanout-write-vs-read · cell-based-architecture · graceful-degradation · circuit-breaker · backfill-and-reprocessing | **done** |
| 8 | [comparisons/](../comparisons/README.md) (new folder): sql-vs-nosql-vs-newsql · oltp-database-matrix · messaging-matrix · consistency-model-matrix · batch-vs-streaming | **done** |
| 9+ | cqrs · event-sourcing · change-data-capture · bulkhead · leader-election · scatter-gather · strangler-fig · write-audit-publish · pagination-patterns · api-versioning | planned |

**10 of 20 patterns written.** Batch 6 covered atomicity you cannot have; batch 7 covers **blast
radius** — who is affected, for how long, and what they see while it lasts.

## How to use these

Read a pattern page **after** you have felt the problem it solves — the "when it earns its
complexity" paragraph only lands once you have the constraint in hand. Read it **before** you
adopt one, because every page's most useful section is the one describing what the pattern costs
when it was not needed.

Each page ends with **Staff-level follow-ups**: multi-part questions with no definitional answer.

## See also

- [../fundamentals/README.md](../fundamentals/README.md) — the mechanisms these patterns compose
- [../comparisons/README.md](../comparisons/README.md) — choosing the technology underneath a pattern
- [../topics/manifest.md](../topics/manifest.md) — canonical topic list; check before creating a file
- [../diagrams/components.md](../diagrams/components.md) — shared Mermaid vocabulary
- [../CONVENTIONS.md](../CONVENTIONS.md) — file format contract

## Referenced by

- [Comparisons index](../comparisons/README.md)
- [Fundamentals index](../fundamentals/README.md)
- [Interview prep index](../README.md)
- [Primitives index](../02-primitives/README.md)
- [Repo index](../../INDEX.md)
