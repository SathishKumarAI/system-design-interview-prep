---
title: Comparisons index
type: index
track: universal
tier: P0
status: drafted
updated: 2026-09-02
tags: [index, comparisons, selection]
---

# Comparisons — cross-cutting trade-off matrices

A [fundamentals](../fundamentals/README.md) page explains one mechanism. A
[patterns](../patterns/README.md) page explains one shape. A comparison page answers **"which of
these do I pick, and what do I regret?"** — and it has its own bar:

> **Every column is a real decision axis** (write path, consistency, failure behaviour, ops cost),
> **not a feature checklist** — and every page **commits to a recommendation**.

A comparison that lists capabilities without naming the choice people get wrong is a table, not a
document. Vendors already publish tables.

These pages **reference topic pages rather than re-explaining them**: the mechanics live in
`fundamentals/`, the arguments live here.

## Where to look

| Question | File |
|---|---|
| Do I need NoSQL, or do I need to shard Postgres? | [sql-vs-nosql-vs-newsql.md](sql-vs-nosql-vs-newsql.md) |
| Postgres, MySQL, Cassandra, Scylla or DynamoDB — and what breaks first in each? | [oltp-database-matrix.md](oltp-database-matrix.md) |
| Kafka, Pulsar, SQS, RabbitMQ or Kinesis? | [messaging-matrix.md](messaging-matrix.md) |
| What does each system's **default** actually guarantee? | [consistency-model-matrix.md](consistency-model-matrix.md) |
| Batch, micro-batch or true streaming? Lambda or Kappa? | [batch-vs-streaming.md](batch-vs-streaming.md) |

## The recommendations these pages commit to

Stated here so the position is visible without opening five files. Each page carries the argument
and the conditions under which it flips:

| Question | This set's answer |
|---|---|
| SQL or NoSQL? | **Relational until you can name the property that rules it out.** Notion and Figma both scaled Postgres rather than migrating |
| Which OLTP engine? | **Postgres**, unless a named constraint rules it out. Compare on *what breaks first*, not features |
| Which messaging system? | **SQS**, unless you can name a second consumer or a replay requirement |
| Which consistency setting? | **Per operation, written down and tested.** Defaults are weaker than everyone assumes, and the end-to-end model is the weakest link on the path |
| Batch or streaming? | **Batch → micro-batch → streaming**, and only move a step when someone names a decision that the extra freshness changes |

The through-line: **every one of these defaults to the boring option, and the interesting work is
naming the specific property that overrides it.**

## Written / planned

The full plan — 18 comparison pages with canonical names and forbidden aliases — is in
[../topics/manifest.md](../topics/manifest.md) §3. **Read the manifest before creating any file
here.**

| Batch | Files | State |
|---|---|---|
| 8 | sql-vs-nosql-vs-newsql · oltp-database-matrix · messaging-matrix · consistency-model-matrix · batch-vs-streaming | **done** |
| 9+ | row-vs-columnar · lakehouse-table-formats · stream-engine-matrix · api-protocol-matrix · realtime-transport-matrix · crdt-vs-ot · erasure-coding-vs-replication · monolith-vs-microservices · compute-platform-matrix · retrieval-strategy-matrix · vector-store-matrix · llm-build-vs-buy · ranking-model-matrix | planned |

**5 of 18 comparisons written.** This folder **retires**
[../08-reference/tech-selection.md](../08-reference/tech-selection.md), whose single mega-table
became these pages.

## See also

- [../fundamentals/README.md](../fundamentals/README.md) — the mechanisms these pages compare
- [../patterns/README.md](../patterns/README.md) — the shapes built from them
- [../topics/manifest.md](../topics/manifest.md) — canonical topic list
- [../CONVENTIONS.md](../CONVENTIONS.md) — file format contract

## Referenced by

- [Fundamentals index](../fundamentals/README.md)
- [Interview prep index](../README.md)
- [Patterns index](../patterns/README.md)
- [Repo index](../../INDEX.md)
- [Technology selection tables](../08-reference/tech-selection.md)
