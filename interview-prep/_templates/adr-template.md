---
title: "ADR-NNNN: <short decision title>"
type: adr
status: Draft          # Draft | Proposed | Accepted | Rejected | Superseded by ADR-NNNN
proposed_by: <name>
date: YYYY-MM-DD
supersedes:            # ADR-NNNN, if any
superseded_by:         # ADR-NNNN, if any
tags: [adr]
---

# ADR-NNNN: <short decision title>

**Status:** Draft · **Proposed by:** <name> · **Date:** YYYY-MM-DD

## Decision

One or two sentences. The decision itself, stated plainly, in the present tense.

> We will use X for Y.

## Context and problem statement

What forced a decision now? Constraints that matter: scale, latency, team skills, budget,
deadlines, compliance, existing systems. Write this for someone who joins in two years and has
none of today's context.

## Considered options

1. **Option A** — one line
2. **Option B** — one line
3. **Option C — do nothing** (always consider it)

### Option A — <name>

| Pros | Cons |
|---|---|
| | |

### Option B — <name>

| Pros | Cons |
|---|---|
| | |

### Option C — <name>

| Pros | Cons |
|---|---|
| | |

## Why we chose <option>

The reasoning, tied to the constraints above — not a restatement of the pros.

## Trade-offs we are accepting

Be explicit and honest. Operational complexity, skill gaps, cost, what this locks us out of,
what becomes harder to change later. **An ADR with no costs listed is a sales pitch, not a record.**

## Consequences

- What changes immediately
- What we must build or operate as a result
- What we will need to revisit, and roughly when

## References

- Links to benchmarks, spikes, docs, prior ADRs, external sources

---

<!--
Rules (see ../../CLAUDE.md → Architecture Decision Records):
- ONE decision per ADR.
- Never edit an accepted ADR to change the decision — write a new one and mark this
  "Superseded by ADR-NNNN".
- Always record rejected alternatives and the trade-offs accepted.
- Write it while the context is fresh; if reconstructed later, say so here.
- Get it reviewed by a human before status becomes Accepted.
-->

## Referenced by

- [CLAUDE.md — system-design-prep](../../CLAUDE.md)
- [Docs index](../../docs/README.md)
