---
title: Reliability patterns
type: primitive
track: universal
difficulty: core
status: drafted
sources: [AWS Builders Library, Google SRE book]
updated: 2026-09-02
tags: [timeouts, retries, circuit-breaker, load-shedding, dr]
---

# Reliability patterns

The section that 2026 rubrics score explicitly as "operational maturity". Bring it up
**unprompted** — that is the whole point.

## The core insight

Most large outages are not caused by a component failing. They're caused by the **system's
reaction** to a component being slow: retries amplify, queues grow, threads exhaust,
health checks flap, and the blast radius expands until everything is down.

**Slow is worse than down.** A dead dependency fails fast and you route around it. A
dependency at 5 seconds holds every one of your threads.

## Timeouts

- Every network call has a timeout. No exceptions. A missing timeout is an unbounded
  resource leak.
- **Timeout budget**: the caller's timeout must exceed the sum of what the callee will do,
  and each layer inward gets a *smaller* budget. Propagate the remaining deadline in a
  header (gRPC does this natively) so nobody works on a request the client already gave up on.
- Set timeouts from the **latency distribution**, not from hope: ~p99.9 of healthy traffic.
  Too tight = you fail healthy requests. Too loose = you hold resources for a dead call.

## Retries — the double-edged one

Retries turn a 1% error rate into a 3% load increase, and a 50% error rate into a
death spiral.

| Rule | Why |
|---|---|
| Only retry **idempotent** operations | Or use an idempotency key so it's safe |
| **Exponential backoff + full jitter** | Without jitter, retries synchronise into waves |
| **Retry budget** — cap retries at e.g. 10% of requests | Turns amplification into a bounded cost |
| Never retry at every layer | 3 layers × 3 retries = 27x load. Retry at **one** layer, usually the edge-most that can |
| Don't retry 4xx, or 503-with-Retry-After you haven't waited for | Retrying a client error is pure waste |
| Fail fast when the circuit is open | See below |

## Circuit breaker

Closed (normal) → **Open** after an error threshold: fail immediately without calling →
**Half-open** after a cooldown: let a few probes through → close if they succeed.

Buys: the failing dependency gets breathing room to recover, and your threads aren't parked
on it. Costs: you must define the degraded behaviour when the circuit is open — a circuit
breaker with no fallback just fails faster.

## Bulkheads

Isolate resource pools so one problem can't consume everything: separate thread/connection
pools per dependency, separate instance pools per tenant class, separate queues per priority.
Named after ship compartments: a hull breach floods one compartment, not the ship.

## Load shedding and admission control

When you're over capacity, serving 100% of traffic badly is worse than serving 80% well.

- Shed **cheaply and early** (at the LB/gateway), before you've spent work on the request.
- Shed by **priority**: health checks and paying customers before batch and prefetch traffic.
- Return 429 with `Retry-After`, and make the client respect it.
- **Queue depth is your signal**; if a request has been queued longer than its timeout,
  drop it without processing — completing work nobody is waiting for is pure waste.

## Graceful degradation

Name the degraded mode for every dependency:

| Dependency down | Degraded behaviour |
|---|---|
| Recommendation service | Serve the non-personalised popular list |
| Search | Serve the browse/category page |
| Avatar service | Serve initials |
| Cache | Serve from DB with admission control, or serve stale from a local snapshot |
| Payment provider | Queue the intent, tell the user "processing", reconcile later |

> [!tip] Interview line
> "None of these dependencies are allowed to take the checkout down. Recommendations degrade
> to a static list, and the fraud check has a 200 ms timeout with a fail-open-and-flag policy
> — the business decided a slow fraud check is a bigger loss than a delayed review."

## Rate limiting (protecting yourself and others)

| Algorithm | Behaviour | Use |
|---|---|---|
| Fixed window | Simple; burst at window edges (2x limit across boundary) | Rough quotas |
| Sliding window log | Exact; memory per request | Low volume, strict |
| Sliding window counter | Good approximation, cheap | **Common default** |
| Token bucket | Allows bursts up to bucket size, steady refill | **API rate limits — the usual answer** |
| Leaky bucket | Smooths to a constant outflow | Traffic shaping, downstream protection |

Distributed enforcement: centralised counter (Redis, exact-ish, adds a hop) vs local buckets
with periodic sync (fast, approximate, may allow N×limit briefly). Say which you chose and
why the approximation is acceptable.

## Multi-region and disaster recovery

| Strategy | RTO / RPO | Cost |
|---|---|---|
| Backup & restore | Hours / hours | Cheapest |
| Pilot light | ~10s of min / minutes | Low |
| Warm standby | Minutes / seconds | Medium |
| Active-active | Seconds / ~zero | Highest — and you own conflict resolution |

**RTO** = how long to recover. **RPO** = how much data you can lose. Both come from the
business, not from engineering taste — ask for them.

Active-active traps to name: data residency law, write conflicts, cross-region latency for
anything synchronous, and the fact that **failover you never test does not work**. Game days
and regular region evacuation drills are the answer.

## Failure modes (meta)

| Failure | Symptom | Mitigation |
|---|---|---|
| Retry amplification | Dependency's load triples during its own incident | Budgets, backoff, circuit breaker |
| Thundering herd on recovery | Everything reconnects at once and re-kills it | Jitter, staged re-entry |
| Cascading failure through health checks | Whole fleet marked unhealthy | Shallow checks for routing, min-healthy floor |
| Metastable failure | Load drops below normal but the system stays broken | Shed load to break the loop; capacity for the recovery, not just steady state |
| Correlated failure | "Independent" replicas share an AZ, deploy, or cert | Spread across AZs, staged deploys, cert expiry alerts |
| Config push outage | Everything down at once, no code changed | Treat config as code: canary, validate, roll back |

## Numbers

| Quantity | Typical |
|---|---|
| Backoff base / max | 100 ms / 10–30 s |
| Retry budget | ≤ 10% of request volume |
| Circuit break threshold | 50% errors over 10 s window |
| Health check | Every 1–5 s, eject after 2–3 failures |
| Deploy canary | 1% → 10% → 50% → 100%, with bake time at each |

## Referenced by

- [Consensus — Raft and Paxos](../fundamentals/consensus-raft-paxos.md)
- [Design a distributed rate limiter](../03-backend-cases/rate-limiter.md)
- [Design a notification system](../03-backend-cases/notification-system.md)
- [Leases, locks and fencing](../fundamentals/leases-locks-and-fencing.md)
- [Primitives index](README.md)

## Sources & further reading

- [AWS Builders' Library — Timeouts, retries and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
- [AWS Builders' Library — Using load shedding to avoid overload](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/)
- [Google SRE Book — Handling overload, Addressing cascading failures](https://sre.google/sre-book/handling-overload/)
- Repo notes: [../../basic/prep/Availability.md](../../basic/prep/Availability.md)
- Case: [../03-backend-cases/rate-limiter.md](../03-backend-cases/rate-limiter.md)
