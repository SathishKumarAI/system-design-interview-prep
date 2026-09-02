---
title: Design a payments system / ledger
type: case
track: backend
difficulty: advanced
status: drafted
sources: [Stripe engineering, DDIA ch.7-9]
updated: 2026-09-02
tags: [idempotency, ledger, saga, reconciliation, exactly-once]
---

# Design a payments system / ledger

> Take money from a customer, record it correctly forever, pay out, handle refunds and
> disputes.
> **The hard part:** correctness under retries and partial failure. This is the case where
> "eventually consistent, it's fine" is a wrong answer, and where saying **idempotency key**,
> **double-entry ledger** and **reconciliation** unprompted marks you as senior.

## 1. Clarify

| Question | Assumed answer |
|---|---|
| Are we the payment processor or using one? | Using external PSPs (Stripe/Adyen), but we own the ledger |
| Currencies? | Multi-currency, no FX conversion inside a transaction |
| Payouts? | Yes — marketplace model, hold then pay out on a schedule |
| Refunds/partial refunds/disputes? | Yes, all three |
| Scale? | 10M transactions/day, peak 5x on sale days |
| Compliance? | PCI (tokenise, never store PANs), audit retention 7 years |

**Non-goals:** fraud model internals, tax calculation, the checkout UI.

## 2. Requirements

**Functional**
- Authorise, capture, refund, void; multiple payment methods
- Immutable ledger of every money movement, queryable balances
- Payouts to sellers with holds and fees
- Webhook ingest from PSPs; reconciliation against their settlement files

**Non-functional**

| Target | Value |
|---|---|
| Correctness | **Zero double-charges. Zero lost money. Non-negotiable** |
| Auditability | Every cent traceable to a source event, forever |
| Payment API p99 | < 2 s (a PSP call dominates) |
| Availability | 99.99% — and *degrade to queued* rather than lose an intent |

## 3. Estimates

```
10M txn/day ≈ 116/s avg, ~600/s peak       ← low volume; this case is NOT about scale
Ledger entries: double-entry → ≥ 2 rows per transaction, more with fees/taxes/FX
   10M × 6 = 60M rows/day → 22B rows/year × 200 B ≈ 4.4 TB/year, retained 7 years ≈ 30 TB
Webhooks in: ~3 per transaction = 30M/day ≈ 350/s, bursty and out-of-order
PSP latency: 200 ms – 2 s, and occasionally it just times out with unknown outcome
```

> [!info] The scary number
> There isn't one — the volume is small. **The difficulty is entirely correctness**, and
> saying that out loud early ("this isn't a scale problem, it's a consistency problem") is
> itself a strong signal.

## 4. API / contract

```http
POST /v1/payment_intents
  Idempotency-Key: <required>
  { amount_minor: 4999, currency: "USD", customer_id, payment_method_id, metadata }
  → 201 { id: "pi_...", status: "requires_confirmation" }

POST /v1/payment_intents/{id}/confirm     Idempotency-Key
  → 200 { status: "succeeded" | "requires_action" | "processing" | "failed", ... }

POST /v1/refunds  { payment_intent_id, amount_minor }   Idempotency-Key
GET  /v1/balances/{account_id}          → { available, pending, currency }
POST /v1/payouts  { account_id, amount_minor }          Idempotency-Key
POST /webhooks/psp/{provider}                            (signed, verified, idempotent)
```

Every mutating endpoint takes an idempotency key. Retrying with the same key returns the
**same stored response**, never a new charge. Amounts are integers in minor units — never
floats, ever.

## 5. Data model

```sql
-- append-only, never UPDATE, never DELETE
ledger_entries(
  id, account_id, amount_minor,     -- signed: + credit, - debit
  currency, transaction_id,         -- entries of one transaction sum to zero
  entry_type, created_at, metadata
)
accounts(id, type, owner_id, currency)        -- customer, platform, seller, fee, escrow
transactions(id, kind, external_ref, state, idempotency_key UNIQUE, created_at)
payment_attempts(id, transaction_id, psp, psp_ref, state, request, response, created_at)
idempotency_keys(key PK, scope, response_json, state, created_at)   -- TTL 7d+
balance_snapshots(account_id, as_of, balance_minor)   -- materialised, rebuildable
```

**Double-entry:** every movement writes at least two rows summing to zero.
A $49.99 charge with a $1.50 fee:

| account | amount |
|---|---|
| customer_receivable | −4999 |
| seller_payable | +4849 |
| platform_fee_revenue | +150 |

Sum = 0. **This invariant is checkable, continuously, in production** — and "I'd run a job
that asserts every transaction's entries sum to zero and alerts on any that don't" is one of
the highest-signal sentences you can say in this interview.

**Balance = SUM(amount) over the account**, materialised into snapshots for speed and
recomputable from scratch at any time. Never a mutable `balance` column as the source of truth.

## 6. Architecture

```
checkout → payment API (idempotency check, create intent, ledger: pending)
              → PSP adapter (with idempotency key passed through)
                    ├── success  → ledger: captured, publish payment.succeeded
                    ├── failure  → ledger: failed (still recorded — failures are data)
                    └── TIMEOUT  → state: unknown → reconciler resolves it
              → Kafka: payment events → notifications, analytics, seller balances

PSP webhooks → verify signature → idempotent handler (dedupe by event id) → state machine
Daily settlement file from PSP → reconciliation job → discrepancy report → ops queue
Payout scheduler → saga: check balance → create payout → PSP transfer → confirm/compensate
```

### Deep dive A — the ambiguous outcome (the actual hard problem)

You call the PSP; the connection times out. Did the charge happen? **You do not know, and
you cannot find out synchronously.**

Handling:
1. Record `payment_attempts` row as `unknown` **before** calling out, with the exact
   idempotency key you sent. Never call an external system without a durable record that
   you were about to.
2. Never blindly retry a charge. Retry **with the same PSP idempotency key** — every serious
   PSP supports this, and it makes the retry a lookup rather than a second charge.
3. If the key isn't supported: query the PSP for the transaction by your reference before
   retrying.
4. A **reconciler** sweeps `unknown` attempts on a schedule, queries the PSP, resolves the
   state, and writes the ledger entries. Until resolved, the user sees "processing" — a
   truthful, deliberate state, not a bug.
5. The daily settlement file is the final arbiter. Anything that disagrees goes to an ops
   queue with a human.

> [!tip] Say this
> "The system is at-least-once end to end. Correctness comes from idempotency keys at every
> boundary plus a reconciliation loop that treats the provider's settlement file as the
> source of truth. I'd never rely on a webhook arriving, or arriving once, or arriving in order."

### Deep dive B — payout saga

Payouts span your ledger and the PSP, so no single transaction covers it:

```
1. Reserve   — ledger: debit seller_payable, credit payout_pending  (local, atomic)
2. Create    — PSP transfer with idempotency key                    (external)
3. Confirm   — on PSP webhook: payout_pending → paid_out            (local)
   Compensate — on PSP failure: reverse step 1, notify, retry later
   Stuck      — timeout alarm: if no terminal state in 24 h, alert a human
```

Orchestrated (Temporal/Step Functions), not choreographed, because you need visibility of
every in-flight payout and a queryable "what is stuck" list. Compensations must themselves be
idempotent.

### Deep dive C — webhooks

- **Verify the signature** — an unauthenticated webhook endpoint that moves money is a
  vulnerability, not an integration.
- Dedupe on the provider's event ID (they *will* redeliver).
- Events arrive **out of order** — `succeeded` can land after `refunded`. The handler must be
  a state machine that ignores illegal or stale transitions, keyed by the PSP's own sequence
  or timestamp, not by arrival order.
- Return 200 fast and process async, or the provider's retries pile up on a slow handler.

## 7. Scale & failure

| Breaks first at 10x | Fix |
|---|---|
| Ledger table size | Partition by month; archive to cold storage; snapshots for balance reads |
| Balance reads (SUM over millions of rows) | `balance_snapshots` + delta since snapshot |
| Reconciliation job runtime | Incremental by day, parallel by account range |
| Webhook burst after a PSP outage | Queue and process async; never process inline |

| Component fails | Blast radius | Degraded behaviour |
|---|---|---|
| PSP down | Can't charge | Queue intents, show "processing", retry with backoff; **never** silently fail a payment the user believes succeeded |
| Ledger DB down | No new payments | **Fail closed.** Refusing a payment is recoverable; recording it wrongly is not |
| Kafka down | Downstream stale | Payments unaffected — the ledger is the source of truth, events are derived |
| Reconciler broken | Discrepancies accumulate silently | Alert on reconciler *not running* — a silent reconciler is the most dangerous failure here |

## 8. Ops & cost

- **SLO:** 99.99% payment API availability; **0** unreconciled transactions older than 48 h;
  0 ledger imbalances.
- **Alert on:** ledger imbalance (any), unknown-state attempts older than 1 h, reconciliation
  discrepancy count and value, PSP error rate by method, webhook lag, payout stuck count.
- **Rollout:** money paths get shadow mode and dual-run comparison, not canaries alone. New
  ledger logic runs alongside the old, results compared, before it becomes authoritative.
- **Cost:** negligible infrastructure; **PSP fees (~2.9% + $0.30) dwarf everything.** The
  engineering levers that matter are payment-method routing (ACH vs card), retry strategy for
  soft declines, and reducing chargebacks — all business outcomes, not infra ones. Saying this
  shows you understand what the system is *for*.
- **First thing I'd cut:** nothing on the correctness path. Cut analytics retention instead.

## Referenced by

- [Backend cases index](README.md)
- [Consistency models](../fundamentals/consistency-models.md)
- [Design real-time fraud detection](../06-ml-cases/fraud-detection.md)
- [Design ride-hailing / proximity matching (Uber)](ride-hailing.md)
- [Engineering blogs and case studies](../10-resources/engineering-blogs.md)
- [Idempotency](../fundamentals/idempotency.md)
- [Leases, locks and fencing](../fundamentals/leases-locks-and-fencing.md)
- [Microsoft, Apple, Netflix and other big tech](../09-company-styles/microsoft-apple-netflix.md)
- [Question bank](../07-drills/question-bank.md)
- [Repo index](../../INDEX.md)
- [Saga pattern](../patterns/saga-pattern.md)
- [Transaction isolation levels](../fundamentals/transaction-isolation-levels.md)
- [Transactions, sagas and idempotency](../02-primitives/transactions-and-idempotency.md)

## Sources & further reading

- [Stripe — Designing robust and predictable APIs with idempotency](https://stripe.com/blog/idempotency)
- [Stripe — Online migrations at scale](https://stripe.com/blog/online-migrations)
- [Martin Kleppmann — Designing Data-Intensive Applications](https://dataintensive.net/) — local copy at `DE/System-Design/`
- [microservices.io — Saga pattern](https://microservices.io/patterns/data/saga.html)
- Primitives: [transactions-and-idempotency](../02-primitives/transactions-and-idempotency.md), [consistency-and-consensus](../02-primitives/consistency-and-consensus.md)
