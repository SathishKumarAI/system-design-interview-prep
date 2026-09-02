---
title: "ADR-0001: Split bundled primitives into atomic fundamentals pages"
type: adr
status: Accepted
proposed_by: Claude (drafted) / Sathish Kumar (decided)
date: 2026-09-02
supersedes:
superseded_by:
tags: [adr, structure, docs]
---

# ADR-0001: Split bundled primitives into atomic fundamentals pages

**Status:** Accepted · **Proposed by:** drafted by assistant, decided by Sathish Kumar · **Date:** 2026-09-02

## Decision

We split `interview-prep/02-primitives/` into `interview-prep/fundamentals/`, one page per
mechanism, and add `patterns/` and `comparisons/` as sibling folders. Case-study files are
rewritten **in place**; no existing file is renamed or moved. Scope of the rewrite is all 123
topics in the manifest, written P0 first, five files per branch.

## Context and problem statement

The set was 75 files that read as competent interview prep and stop exactly where a staff-level
reader needs help: the internals, the arithmetic, the failure modes, and the argument between three
defensible options.

The cause was structural, not effort. Twelve `02-primitives/` files each carry three to six
distinct topics. `consistency-and-consensus.md` alone covered CAP, PACELC, isolation levels, Raft,
distributed locks, clocks and CRDTs in 168 lines — roughly 20 lines per topic. No amount of
rewriting makes 20 lines carry MVCC internals plus a write-skew interleaving plus SSI abort
behaviour. The repo's own conventions cap a file at ~300 lines for good reasons, so "make the
existing files longer" was never available.

A second problem forced the decision now: cross-cutting trade-off matrices (SQL vs NoSQL vs NewSQL,
Kafka vs Pulsar vs SQS, Iceberg vs Delta vs Hudi) have no correct home inside any single topic
file, and `08-reference/tech-selection.md` had become one mega-table nobody could maintain.

## Considered options

1. **Option A — split into atomic pages, add `patterns/` and `comparisons/`** (chosen)
2. **Option B — deepen the twelve files in place**
3. **Option C — do nothing; the set is adequate for its original purpose**

### Option A — split into atomic pages

| Pros | Cons |
|---|---|
| Each page can carry internals + numbers + failure modes + trade-offs without exceeding the line ceiling | ~47 fundamentals files instead of 12; more files to keep linked and indexed |
| Duplicate risk is controlled by the manifest's canonical-name + alias list | Requires discipline: check the manifest before creating any file, forever |
| Cross-topic matrices get a home in `comparisons/` | Two more folders in the tree |
| A page is independently reviewable and independently finishable | The split must be staged — the source file cannot be deleted until every topic it holds has landed |

### Option B — deepen the twelve files in place

| Pros | Cons |
|---|---|
| Zero structural churn; every inbound link keeps working | Each file would run 1500+ lines to hit staff depth, against a 500-line ceiling |
| No manifest discipline needed | The reader still cannot find "write skew" — it is buried in a file named for something else |
| Cheapest option today | Guarantees the same shallowness for the topics that lose the space fight |

### Option C — do nothing

| Pros | Cons |
|---|---|
| Free | The stated goal — staff/principal-level depth — is not met, and the set stays a glossary |

## Why we chose Option A

The failure being fixed is *depth per topic*, and depth per topic is bounded by space per topic.
Option B keeps the binding constraint and only changes the effort spent inside it. Option A removes
the constraint: a page about transaction isolation can spend 40 lines on MVCC visibility rules and
another 40 on an SSI abort state machine because it is not competing with Raft for the same file.

The duplicate risk that normally makes people avoid many-small-files (`caching.md` and
`cache-strategies.md` both existing, both half-written) is already mitigated: the manifest was
written first and lists a canonical path plus forbidden aliases for every topic.

## Trade-offs we are accepting

- **Manifest discipline is now load-bearing.** If someone creates a file without checking, the set
  gets a semantic duplicate that no script can detect — `lint_docs.py` compares filenames, so it
  would catch `caching.md` vs `cache-strategies.md` and be blind to `rate-limiting.md` vs
  `throttling.md`. Only a human reading both pages catches that class.
- **A long transitional period.** `02-primitives/` and `fundamentals/` coexist until every topic is
  split. During that window two files discuss the same subject at different depths, which is
  exactly the duplication we claim to prevent. Mitigation: the primitive file gets a banner naming
  its successor pages, and is deleted the moment its last topic lands.
- **More link surface.** ~120 files with See-also and backlink sections means the link check and
  backlink pass move from "nice to have" to mandatory before any commit claims done.
- **Chosen scope is all 123 topics, not the recommended 63 P0.** This roughly doubles the work
  against a recommendation to stop at P0 and reassess after drilling. Accepted knowingly; batch
  order still runs P0 first, so stopping early remains possible at any batch boundary.

## Consequences

- Immediately: `interview-prep/fundamentals/` exists with batch 1 (the consistency cluster);
  `02-primitives/consistency-and-consensus.md` carries a pointer banner and stays until
  `clocks-and-ordering.md` and `crdts-and-conflict-resolution.md` also exist.
- `patterns/` and `comparisons/` are created when their first batch is written (batches 6–8), not
  before — empty folders are noise.
- `08-reference/tech-selection.md` is retired into `comparisons/` once those files exist, replaced
  by a stub. Not before, or its content is unreachable.
- Every batch is one branch, one PR, with `check_links.py` output quoted in the PR body.
- Revisit at the end of P0 (batch 13): if drilling shows P1/P2 topics are not being reached for,
  stop there rather than completing all 123 on principle.

## References

- [interview-prep/topics/manifest.md](../../interview-prep/topics/manifest.md) — the canonical topic list, tiers, aliases and split provenance
- [interview-prep/CONVENTIONS.md](../../interview-prep/CONVENTIONS.md) — file format contract
- [CLAUDE.md](../../CLAUDE.md) — section contract and ADR anti-pattern rules
- [docs/WORKLOG.md](../WORKLOG.md) — session-level reasoning

## Referenced by

- [Caching](../../interview-prep/02-primitives/caching.md)
- [Consistency and consensus](../../interview-prep/02-primitives/consistency-and-consensus.md)
- [File conventions](../../interview-prep/CONVENTIONS.md)
- [Fundamentals index](../../interview-prep/fundamentals/README.md)
- [Messaging and streams](../../interview-prep/02-primitives/messaging-and-streams.md)
- [Next session — start here](../NEXT-SESSION.md)
- [Primitives index](../../interview-prep/02-primitives/README.md)
- [Replication and partitioning](../../interview-prep/02-primitives/replication-and-partitioning.md)
- [STATUS](../../STATUS.md)
- [Storage and databases](../../interview-prep/02-primitives/storage-and-databases.md)
- [Topic manifest](../../interview-prep/topics/manifest.md)
- [Transactions, sagas and idempotency](../../interview-prep/02-primitives/transactions-and-idempotency.md)
- [Worklog](../WORKLOG.md)
