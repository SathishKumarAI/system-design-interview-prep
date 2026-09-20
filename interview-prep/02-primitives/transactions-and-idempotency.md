---
title: Transactions, sagas and idempotency
type: primitive
track: universal
difficulty: advanced
status: drafted
sources: [DDIA ch.7, ch.9]
updated: 2026-09-02
tags: [idempotency, saga, outbox, ledger, 2pc]
---

# Transactions, sagas and idempotency

> [!info] Nearly fully split — staff-level versions live in `fundamentals/` and `patterns/`
> ([ADR-0001](../../docs/adr/0001-split-primitives-into-atomic-fundamentals.md))
> [idempotency](../fundamentals/idempotency.md) ·
> [outbox-pattern](../patterns/outbox-pattern.md) ·
> [saga-pattern](../patterns/saga-pattern.md) ·
> [distributed-transactions](../patterns/distributed-transactions.md).
> Still only here: **ledgers and double-entry** — this file stays until
> `ledgers-and-double-entry.md` exists, then it is retired.
> Use this page as the fast revision sheet; use the split pages to learn the mechanism.

The primitive that decides whether your system can charge a card twice. Any design touching
money, inventory, bookings or notifications needs this section explicitly.

## Idempotency — the workhorse

**Definition:** doing it twice has the same effect as doing it once.

Retries exist at every layer (client, LB, queue, your own code). Therefore **every mutating
operation will eventually run more than once**. Design for it or find out in production.

**Implementation, the standard shape:**

```
1. Client generates an idempotency key (UUID) per logical intent — not per attempt.
2. Server: INSERT the key into a dedup table with a UNIQUE constraint,
   in the same transaction as the effect.
3. Conflict on insert → return the stored prior response, do not re-execute.
4. TTL the keys (24h–7d) so the table doesn't grow forever.
```

Details interviewers probe:
- **Store the response**, not just the key — a retry must get the same answer, not a 409.
- **Key scope**: per-user + per-endpoint, so keys can't collide across tenants.
- **In-flight case**: request 1 still running when request 2 arrives → return 409 "in
  progress" and let the client poll, or block on the row lock. Say which.
- **Natural idempotency is better than a key**: `SET status='paid'` is idempotent;
  `balance = balance - 10` is not. Prefer absolute over relative operations.

> [!tip] Interview line
> "The client sends `Idempotency-Key`. We insert it with a unique constraint inside the same
> transaction that debits the account, so a retry can never double-charge — the DB enforces
> it, not our code path."

## Distributed transactions

| Approach | How | Reality |
|---|---|---|
| **2PC** | Coordinator: prepare → all vote → commit/abort | Correct, but **blocking**: coordinator dies after prepare and participants hold locks indefinitely. Latency cost. Avoid across services |
| **Saga** | A sequence of local transactions, each with a compensating action | The practical answer. No isolation — intermediate states are visible |
| **Try-Confirm-Cancel (TCC)** | Reserve → confirm/cancel | Saga with an explicit reservation step. Good for inventory/seats |
| **Single-shard design** | Arrange the data so the transaction is local | **The best answer when available.** Say this first |

**Saga shapes:**
- *Choreography*: each service emits events others react to. No central coordinator; hard
  to see the whole flow; good for 2–3 steps.
- *Orchestration*: a workflow service drives the steps and compensations (Temporal,
  Step Functions, Cadence). Visible state, retries and timeouts for free. **Default above
  ~3 steps.**

**Compensation is not rollback.** You can't un-send an email; you send an apology. You can't
un-ship a box; you accept a return. Name the compensating action for each step, and admit
where a true compensation doesn't exist (that's the point where you need a reservation
instead of an undo).

## The dual-write problem

Writing to your DB *and* publishing an event/calling another service is two writes with no
atomicity. Solutions:

| Solution | Notes |
|---|---|
| **Transactional outbox** | Event row written in the same DB transaction; a relay/CDC publishes it. At-least-once, no lost events. **Default answer** |
| **Listen-to-yourself** | Publish first, consume your own event to update your DB | Inverts the problem; the event is the source of truth |
| **CDC from the DB log** | Debezium reads the WAL; no application change | Couples consumers to your schema unless you project |
| 2PC across DB and broker | Technically possible, operationally miserable | Don't |

## Money: the ledger pattern

Never store a mutable `balance` as the source of truth.

```
ledger_entries(id, account_id, amount_signed, currency, txn_id, created_at, ...)
   -- append-only, immutable
   -- every transfer writes at least two rows summing to zero (double-entry)
   -- balance = SUM(amount) for the account, materialised into a cache/snapshot table
```

Buys: full auditability, reconstructable balances, natural idempotency on `txn_id`, disputes
answerable. This is how real payment systems work and saying it is a strong signal.

Also expect: currency as integer minor units (never floats), a state machine for payment
status (`created → authorized → captured → settled | failed | refunded`) with only legal
transitions, and reconciliation against the provider's daily file.

## Isolation reminders that bite

- **Lost update**: read-modify-write from two transactions. Fix: atomic DB operation
  (`UPDATE ... SET n = n + 1`), `SELECT FOR UPDATE`, or compare-and-set with a version column.
- **Write skew**: both transactions read, both decide, together they break the invariant.
  Snapshot isolation does not save you. See
  [consistency-and-consensus.md](consistency-and-consensus.md).
- **Optimistic concurrency (version column)** scales better than locks when conflicts are
  rare — which they usually are. Return 409 and let the client retry with fresh state.

## Failure modes

| Failure | Symptom | Mitigation |
|---|---|---|
| Retry storm double-charges | Duplicate payments, angry users | Idempotency keys enforced at the DB |
| Saga stalls mid-flight | Order stuck in `pending` forever | Orchestrator with timeouts + a stuck-workflow alert; reconciliation job |
| Compensation itself fails | Inconsistent state, silently | Compensations must also be idempotent and retried; DLQ + human runbook |
| Outbox relay lags | Downstream stale, users complain | Monitor outbox depth and age |
| Dedup table unbounded | Storage growth, slow inserts | TTL + partition by day |

## Interview lines

> [!tip] Say this
> "I'd try to make this a single-partition transaction first — put the order and its items in
> the same partition keyed by order ID. Distributed transactions you avoid are free."

> [!tip] Say this
> "Booking is TCC: hold the seat with a 10-minute reservation, confirm on payment, cancel on
> timeout. That gives us correctness without holding a database lock across a payment
> provider call, which would be a 3-second lock."

## Numbers

| Quantity | Order of magnitude |
|---|---|
| Idempotency key TTL | 24 h–7 days |
| Saga step timeout | Seconds to minutes; workflow overall, hours |
| 2PC latency penalty | 2+ extra round trips per participant |
| Optimistic retry conflict rate, healthy | < 1% |

## Referenced by

- [Delivery semantics](../fundamentals/delivery-semantics.md)
- [Design a chat / messaging system](../03-backend-cases/chat-messaging.md)
- [Design a notification system](../03-backend-cases/notification-system.md)
- [Design a payments system / ledger](../03-backend-cases/payments-ledger.md)
- [Design ride-hailing / proximity matching (Uber)](../03-backend-cases/ride-hailing.md)
- [Idempotency](../fundamentals/idempotency.md)
- [Leases, locks and fencing](../fundamentals/leases-locks-and-fencing.md)
- [Messaging and streams](messaging-and-streams.md)
- [Microsoft, Apple, Netflix and other big tech](../09-company-styles/microsoft-apple-netflix.md)
- [Primitives index](README.md)
- [Replication and partitioning](replication-and-partitioning.md)
- [Transaction isolation levels](../fundamentals/transaction-isolation-levels.md)

## Sources & further reading

- Local book: `DE/System-Design/Designing Data Intensive Applications.pdf` — ch.7 (transactions), ch.9 (distributed)
- [Stripe — designing robust and predictable APIs with idempotency](https://stripe.com/blog/idempotency)
- [microservices.io — Saga pattern](https://microservices.io/patterns/data/saga.html)
- [microservices.io — Transactional outbox](https://microservices.io/patterns/data/transactional-outbox.html)
- Case using all of it: [../03-backend-cases/payments-ledger.md](../03-backend-cases/payments-ledger.md)
