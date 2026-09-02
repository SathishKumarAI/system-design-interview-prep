---
title: Design a distributed rate limiter
type: case
track: backend
difficulty: intro
status: drafted
sources: [Alex Xu v1 ch.4, AWS Builders Library]
updated: 2026-09-02
tags: [rate-limit, token-bucket, redis, hot-key]
---

# Design a distributed rate limiter

> Cap how many requests a caller may make per unit time, across a fleet of servers.
> **The hard part:** enforcing a global limit without a global bottleneck, and deciding how
> much inaccuracy you'll accept to keep it fast.

## 1. Clarify

| Question | Assumed answer |
|---|---|
| Limit by what? | API key, user ID, IP, and endpoint class — multiple dimensions, composable |
| Hard or soft limit? | Hard for abuse protection; soft (queue/throttle) for internal traffic |
| Accuracy required? | Approximate is fine (±10%) for quotas; exact for billing-relevant limits |
| Where enforced? | Gateway/edge, before any expensive work |
| What on breach? | 429 + `Retry-After` + `X-RateLimit-*` headers |
| Scale? | 1M rps across the fleet, 10M distinct keys |
| Multi-region? | Yes — and per-region limits are acceptable |

**Non-goals:** billing/metering (adjacent but different — that one must be exact), bot
detection.

## 2. Requirements

**Functional**
- Enforce N requests per window per key, with different rules per tier and endpoint
- Return standard headers: `X-RateLimit-Limit/Remaining/Reset`, `Retry-After`
- Rules configurable without a deploy

**Non-functional**

| Target | Value |
|---|---|
| Added latency | < 1 ms p99 (it's on every request) |
| Availability | Must **fail open or closed by policy**, per rule |
| Accuracy | ±10% acceptable for quotas |
| Scale | 1M rps, 10M keys |

## 3. Estimates

```
1M rps × 1 counter op = 1M Redis ops/s        → ~10–20 Redis nodes (100k ops/s each)
                                                or far fewer with local buckets + sync
10M keys × ~100 B     = 1 GB of counter state → trivial
Hot key: one abusive client at 100k rps hits ONE key → single-node hotspot   ← the design
```

> [!info] The scary number
> Not the total ops — the **hot key**. A distributed rate limiter's failure mode is that
> the thing you're limiting is by definition concentrated on one key.

## 4. API / contract

```
Internal: allow(key, rule_id, cost=1) -> {allowed: bool, remaining: int, reset_at: ts}

Response on breach:
  HTTP 429
  Retry-After: 12
  X-RateLimit-Limit: 1000
  X-RateLimit-Remaining: 0
  X-RateLimit-Reset: 1735689600
```

Rules as config (hot-reloaded):
```yaml
- id: api_v1_write
  match: {tier: free, endpoint_class: write}
  limit: 100
  window: 60s
  algorithm: token_bucket
  burst: 20
  on_error: fail_open        # or fail_closed for abuse-critical rules
```

## 5. Data model

| Entity | Key | Where | Serves |
|---|---|---|---|
| Counter/bucket | `rl:{rule_id}:{key}:{window}` | Redis (or local memory) | The decision |
| Rules | `rule_id` | Config store + in-process cache | Which limit applies |
| Overrides | `(customer_id, rule_id)` | Config store | Enterprise customers with custom limits |

Counter TTL = window length × 2. Never let counters accumulate.

## 6. Architecture

Three placements, and you should name all three:

```
1. Edge/CDN          — crude IP limits, absorbs volumetric abuse before it costs you anything
2. API gateway       — the main enforcement point: per key, per rule    ← primary
3. Service-local     — protects a specific expensive downstream (bulkhead-style)
```

### Deep dive A — algorithm choice

| Algorithm | State | Behaviour | Verdict |
|---|---|---|---|
| Fixed window counter | 1 int | Allows 2× the limit across a window boundary | Only for rough quotas |
| Sliding window log | Sorted set of timestamps | Exact | Memory O(N) per key — too expensive at 1M rps |
| **Sliding window counter** | 2 ints (this window + previous, weighted) | Good approximation, tiny state | **Great default for quotas** |
| **Token bucket** | tokens + last-refill timestamp | Allows bursts up to bucket size, smooth steady rate | **Best for API limits** — matches how clients actually behave |
| Leaky bucket (queue) | Queue | Constant outflow, smooths spikes | Traffic shaping toward a fragile downstream |

Pick **token bucket** for user-facing API limits (clients burst legitimately: a page load
fires 20 requests) and say why fixed-window is wrong (the boundary doubling).

Redis implementation must be **atomic** — a Lua script (or `INCR`+`EXPIRE` pipelined
carefully), otherwise concurrent servers race and the limit leaks:

```lua
-- token bucket, atomic: returns {allowed, remaining}
local tokens = tonumber(redis.call('HGET', KEYS[1], 'tokens')) or capacity
local last   = tonumber(redis.call('HGET', KEYS[1], 'ts')) or now
tokens = math.min(capacity, tokens + (now - last) * refill_rate)
local allowed = tokens >= cost
if allowed then tokens = tokens - cost end
redis.call('HSET', KEYS[1], 'tokens', tokens, 'ts', now)
redis.call('EXPIRE', KEYS[1], ttl)
return {allowed and 1 or 0, math.floor(tokens)}
```

### Deep dive B — centralised vs local, the real trade

| Approach | Accuracy | Latency | Failure behaviour |
|---|---|---|---|
| **Central Redis, every request** | Exact-ish | +0.5–1 ms per request, and Redis is now on your critical path | Redis down = every request must fail open or closed |
| **Local buckets, no coordination** | Up to N× the limit (N = node count) | 0 | Perfect availability |
| **Local buckets + periodic sync** (each node gets a share of the budget, rebalanced every ~1 s) | ±10% | ~0 | Degrades to local-only |

**Recommendation:** local token buckets holding a per-node share of the global budget,
resynchronised every second against Redis. That's ~1000x fewer Redis operations, sub-microsecond
decisions, and it degrades gracefully to "each node enforces its own share" when Redis is
unreachable. Reserve exact central counting for the few rules where over-admitting costs money.

> [!tip] Interview line
> "I'll trade exactness for availability: 10% over-admission on a 1000/min limit is
> harmless, but a rate limiter that takes the API down when Redis blips is a much worse
> outcome. For the billing-relevant limit I'd use the central path and fail closed."

### Deep dive C — hot key

The abusive client *is* a hot key by definition. Mitigations:
- Local buckets already absorb this — the decision never leaves the node.
- If central: shard the key (`rl:{key}:{node_shard}`) with each shard holding budget/N.
- Add an **early-reject cache**: once a key is over limit, remember it locally for the rest
  of the window and reject without touching Redis at all.

## 7. Scale & failure

| Breaks first at 10x | Fix |
|---|---|
| Redis ops volume | Local buckets + sync (already the design) |
| One key's traffic | Local early-reject cache |
| Rule evaluation cost per request | Compile rules into a lookup keyed by (tier, endpoint class) |

| Component fails | Blast radius | Degraded behaviour |
|---|---|---|
| Redis | Loses global coordination | Local enforcement continues at per-node share (fail-open per policy) |
| Config store | Rules can't update | Last-known-good rules stay in memory; alert |
| Clock skew between nodes | Windows misalign | Use Redis server time for central path; monotonic clocks locally |

**Fail open vs fail closed is a product decision, per rule.** Free-tier abuse protection:
fail closed. Paying customer's normal traffic: fail open. Say that you'd tag each rule.

## 8. Ops & cost

- **SLO:** limiter adds < 1 ms at p99; false-rejection rate < 0.1%.
- **Alert on:** 429 rate by tier (a spike = either an attack or a misconfigured rule that's
  hurting real customers), Redis latency, sync failure rate, rule reload failures.
- **Rollout:** every new rule ships in **shadow mode** first — evaluate and log what *would*
  have been rejected, look at the numbers, then enforce. Never enable a new limit blind.
- **Cost:** trivial. A dozen Redis nodes ≈ $3–5k/month, and it *saves* far more by shedding
  abusive load before it reaches expensive services.
- **First thing I'd cut:** central sync frequency (1 s → 5 s), which trades accuracy for cost.

## Referenced by

- [Backend cases index](README.md)
- [Design a notification system](notification-system.md)
- [Engineering blogs and case studies](../10-resources/engineering-blogs.md)
- [Question bank](../07-drills/question-bank.md)
- [Reliability patterns](../02-primitives/reliability-patterns.md)
- [Repo index](../../INDEX.md)

## Sources & further reading

- Local book: Alex Xu vol. 1 ch.4 (rate limiter)
- [AWS Builders' Library — Using load shedding to avoid overload](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/)
- [Stripe — Scaling your API with rate limiters](https://stripe.com/blog/rate-limiters)
- [Cloudflare — How we built rate limiting capable of scaling to millions of domains](https://blog.cloudflare.com/counting-things-a-lot-of-different-things/)
- Primitives: [reliability-patterns](../02-primitives/reliability-patterns.md), [caching](../02-primitives/caching.md)
