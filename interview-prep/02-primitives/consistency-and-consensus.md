---
title: Consistency and consensus
type: primitive
track: universal
difficulty: advanced
status: drafted
sources: [DDIA ch.7-9]
updated: 2026-09-02
tags: [cap, pacelc, isolation, raft, clocks]
---

# Consistency and consensus

The part candidates quote and don't understand. Get precise here and you separate yourself
immediately.

## CAP, stated correctly

CAP is about **what happens during a network partition**. Partitions happen, so you don't
"choose" P — you choose what to do when one occurs:

- **CP**: refuse to serve (error/timeout) rather than return possibly-stale data.
- **AP**: serve whatever you have, reconcile later.

> [!warning] Trap
> "We'll pick CA" — there is no CA in a distributed system. Also: CAP says nothing about
> normal operation, which is 99.99% of the time. That's what PACELC adds.

**PACELC**: *if* **P**artition, choose **A** or **C**; **E**lse (normal operation), choose
**L**atency or **C**onsistency. The everyday trade is latency vs consistency, and that's the
one you actually design around.

| System | PACELC |
|---|---|
| Postgres (single leader, sync replica) | PC/EC |
| DynamoDB (default eventually consistent reads) | PA/EL |
| Cassandra (tunable) | PA/EL, moves toward EC as you raise R and W |
| Spanner / CockroachDB | PC/EC (pays with latency; TrueTime/HLC) |

## The consistency ladder

Strongest at the top, most expensive at the top.

| Model | Guarantee | Cost |
|---|---|---|
| **Linearizable** | Looks like a single copy; a read sees the latest completed write | Consensus round trip on every write; unavailable during partition |
| **Sequential** | All nodes see operations in the same order (not necessarily real-time) | Cheaper than linearizable |
| **Causal** | Related operations ordered; concurrent ones may differ | No coordination for unrelated writes — the sweet spot for many apps |
| **Read-your-writes / monotonic** | Session guarantees for one user | Routing tricks only. Cheap. Usually enough |
| **Eventual** | Converges if writes stop | Free. Requires conflict resolution |

> [!tip] Interview line
> "Balances need linearizability, so those go through the primary. The feed only needs causal
> +read-your-writes, which we get from session routing at no coordination cost."

## Transaction isolation (single-node, still gets asked)

| Level | Prevents | Still allows |
|---|---|---|
| Read uncommitted | — | Dirty reads |
| Read committed | Dirty reads | Non-repeatable reads, phantoms, lost updates |
| **Snapshot / repeatable read** (Postgres "repeatable read") | Non-repeatable reads | Write skew, phantoms in some engines |
| Serializable | Everything | Nothing — costs throughput (SSI aborts, or locks) |

**Write skew** is the one worth being able to explain: two transactions each read a state,
each decide their write is safe, and together they violate an invariant (two doctors both
going off-call because each saw the other on-call). Snapshot isolation does not prevent it.
Fixes: `SELECT ... FOR UPDATE`, an explicit lock row, a constraint, or serializable isolation.

## Consensus

Needed whenever a group must agree on one value despite failures: leader election,
membership, config, distributed locks, ordering.

| Algorithm | Notes |
|---|---|
| **Raft** | Understandable, the default for new systems (etcd, Consul, TiKV, CockroachDB) |
| **Paxos / Multi-Paxos** | Older, harder, still underpins Chubby/Spanner |
| **ZAB** | ZooKeeper's |
| **Byzantine (PBFT etc.)** | Only when nodes may lie — blockchains, not your API |

**Properties to name:** needs a majority quorum (2f+1 nodes tolerate f failures — so 3, 5,
never 4), gives you a totally ordered replicated log, and every write costs at least one
round trip to a majority. **Consensus is expensive; use it for metadata, not for data plane
throughput.**

> [!tip] Interview line
> "I'd keep consensus off the hot path: etcd holds shard-to-node assignments and leader
> leases — kilobytes, low write rate — while the data plane does quorum writes without
> consensus per request."

## Distributed locks (and why they're dangerous)

A lock with a TTL doesn't stop the holder from pausing (GC, VM stall) past its expiry, then
acting as though it still holds it. Two workers act at once and corrupt state.

Fixes: **fencing tokens** — the lock service issues a monotonically increasing token; the
storage layer rejects any write with a stale token. Say "fencing token" and you've shown
you've read past the blog posts.

Redlock (Redis multi-node locking) is contested; the safe interview answer is: *"For
mutual exclusion where correctness matters, I'd use a real consensus store with fencing
tokens, not a TTL lock in a cache. For best-effort deduplication, a Redis lock is fine."*

## Clocks

- Wall-clock time across machines is **not** ordered — NTP drift, leap seconds, VM pauses.
  Never resolve write conflicts with `if (t1 > t2)` unless you accept silent data loss.
- **Logical clocks** (Lamport) give happens-before; **vector clocks** detect concurrency.
- **Hybrid logical clocks (HLC)** — physical time bounded by logical — are what modern
  distributed SQL uses.
- **Spanner's TrueTime** uses GPS/atomic clocks to bound uncertainty and *waits out* the
  interval to give external consistency. That's why Spanner has commit latency: it's paying
  in milliseconds for a global order.

## Conflict resolution (multi-leader / offline clients)

| Strategy | Use when |
|---|---|
| Last-write-wins (LWW) | Loss is acceptable — presence, caches. Silently drops data |
| Application merge | You know the semantics (union sets, max counter) |
| **CRDTs** | Convergent by construction: counters, sets, sequences. Collaborative editing, offline-first |
| **OT (operational transform)** | Text editing with a central server (Google Docs lineage) |
| Keep both, ask the user | Version conflicts in file sync (Dropbox) |

See [../04-frontend-cases/collaborative-editor.md](../04-frontend-cases/collaborative-editor.md).

## Failure modes

| Failure | Symptom | Mitigation |
|---|---|---|
| Split brain | Two leaders, divergent history | Quorum election + fencing tokens |
| Quorum loss (2 of 3 nodes down) | Cluster is read-only or fully down | 5-node clusters for critical metadata; multi-AZ placement |
| Clock skew | Reordered writes, expired-too-early tokens | Logical clocks, generous token windows, monitor drift |
| GC pause > lease | Zombie leader keeps acting | Fencing, short leases, pause monitoring |
| Consensus on the hot path | Throughput ceiling, latency floor | Move it to the control plane |

## Interview lines

> [!tip] Say this
> "This needs linearizability only for the 'reserve seat' step. Everything else is
> eventually consistent. So I'll do one small strongly-consistent operation and keep the
> other 99% of traffic cheap."

> [!tip] Say this
> "During a partition I'd rather reject the write than accept a double booking — this is a
> CP problem. For the presence indicator on the same page, I'd rather show stale data than
> nothing, so that path is AP. Different consistency for different data in the same product
> is normal."

## Numbers

| Quantity | Order of magnitude |
|---|---|
| Raft commit, same region | 1–5 ms |
| Raft commit, cross-region | 50–150 ms |
| etcd write throughput | ~10k/s — metadata scale, not data scale |
| Typical NTP drift | ms; can be seconds when broken |
| Spanner commit wait | ~single-digit ms |

## Sources & further reading

- Local book: `DE/System-Design/Designing Data Intensive Applications.pdf` — ch.7 (transactions), ch.8 (trouble with distributed systems), ch.9 (consistency & consensus). **The single best 150 pages in this whole curriculum.**
- Repo notes: [../../basic/prep/CAP%20theorem.md](../../basic/prep/CAP%20theorem.md), [../../basic/prep/Consistency.md](../../basic/prep/Consistency.md), [../../basic/prep/Availability.md](../../basic/prep/Availability.md)
- [Raft paper — In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf)
- [Martin Kleppmann — How to do distributed locking](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)
- [Jepsen — consistency models](https://jepsen.io/consistency)
