---
title: Load balancing and gateways
type: primitive
track: universal
difficulty: core
status: drafted
sources: [system-design-primer]
updated: 2026-09-02
tags: [load-balancer, gateway, proxy, mesh]
---

# Load balancing and gateways

## What it is

The layer that decides *which* of your identical servers handles a request, plus the layer
that does the cross-cutting work (auth, rate limiting, routing) so services don't each
reimplement it badly.

## L4 vs L7

| | L4 (transport) | L7 (application) |
|---|---|---|
| Sees | IP, port, TCP | HTTP path, headers, cookies, gRPC method |
| Can do | Connection distribution, TLS passthrough | Path routing, header rewriting, retries, canary by header, response caching |
| Cost | Very cheap, millions of conns | More CPU, TLS termination |
| Use for | Raw throughput, non-HTTP protocols, DDoS absorption | Everything user-facing |

Typical stack: anycast → L4 (absorbs, spreads) → L7 (routes, authenticates) → service.

## Algorithms

| Algorithm | Good for | Fails when |
|---|---|---|
| Round robin | Uniform, stateless, equal-cost requests | Request costs vary wildly |
| **Least connections / least outstanding requests** | Mixed request costs — the sane default | Needs accurate in-flight tracking |
| Weighted | Heterogeneous instance sizes, gradual rollout | Weights go stale |
| Consistent hashing on key | Cache affinity, sticky shards | Hot key; rebalancing on membership change |
| Power of two choices | Near-least-connections at almost no coordination cost | — |
| Latency-aware / EWMA | Avoids the slow node automatically | Can oscillate; needs damping |

> [!tip] Interview line
> "Round robin is wrong here because request cost varies 100x between a cold render and a
> cache hit. Least-outstanding-requests routes around the node that's stuck on the
> expensive one — same hardware, better p99."

## Health checks

- **Liveness** (is the process up) vs **readiness** (should it get traffic *now*).
  Conflating them is why deploys drop requests.
- **Shallow** check = process responds. **Deep** check = dependencies reachable. Deep checks
  cascade: DB blips → every node marks itself unhealthy → all capacity removed → outage.
  Rule: deep checks inform *alerts*, shallow checks inform *routing*, and never let a
  dependency failure remove 100% of your fleet.
- **Outlier detection**: eject a node returning errors, re-admit gradually.
- **Connection draining** on shutdown: stop accepting, finish in-flight, then exit. Without
  it, every deploy is a small outage.

## Sticky sessions

Avoid. Every argument for stickiness is an argument for moving state out of the server.

| If you need | Do this instead |
|---|---|
| Session data | External store (Redis) or signed cookie / JWT |
| Cache warmth | Consistent hashing, but accept misses on membership change |
| WebSocket connection | Stickiness is inherent — plan for it, route by connection ID, keep the state in Redis so a reconnect can land anywhere |

## API gateway — what belongs there

| Belongs in the gateway | Belongs in the service |
|---|---|
| TLS termination | Business logic (always) |
| AuthN (validate token), coarse AuthZ (scope) | Fine-grained AuthZ (does *this user* own *this row*) |
| Rate limiting / quota | Domain validation |
| Request routing, versioning, canary split | |
| Request/response logging, trace ID injection | |
| Schema validation, payload size limits | |

> [!warning] Trap
> Putting business logic in the gateway recreates the ESB. It becomes a shared deploy
> bottleneck every team is scared to touch. Say this if the interviewer pushes work into it.

**BFF (Backend for Frontend)**: one gateway per client type (web, iOS, Android, partner API)
so each can shape payloads for its own needs without a lowest-common-denominator API.
Costs: more code to maintain, versioning per client. See
[../04-frontend-cases/frontend-playbook.md](../04-frontend-cases/frontend-playbook.md).

## Service mesh (sidecar or ambient)

Moves retries, mTLS, circuit breaking, traffic splitting and telemetry out of the app and
into infrastructure.

- **Buys:** uniform policy across polyglot services, per-service observability for free,
  mTLS everywhere without app changes.
- **Pays with:** extra hop latency (~0.5–2 ms), significant operational complexity, a new
  control plane to debug at 3am.
- **Say:** "A mesh is worth it above roughly 20–30 services with mixed languages. For five
  Python services, a shared client library is the cheaper answer and I'd start there."

## Failure modes

| Failure | Symptom | Mitigation |
|---|---|---|
| LB is a single point of failure | Total outage | Redundant LBs, anycast VIP, health-checked |
| Retry storm through the LB | Backend collapse amplified 3x | Retry budget (cap % of traffic), backoff + jitter, no retry on 5xx from an overloaded pool |
| Deep health checks flap | Whole fleet marked down at once | Shallow for routing; min-healthy-percent floor |
| No connection draining | 5xx on every deploy | Drain + preStop hook + readiness gate |
| Hot shard via consistent hashing | One node at 100%, rest idle | Bounded loads, virtual nodes, key salting |

## Interview lines

> [!tip] Say this
> "I'll put rate limiting at the gateway because it must protect *every* service, and I'll
> put ownership checks in the service because only it knows the data model."

> [!tip] Say this
> "The LB is stateless, so scaling it is easy — the risk is the health check policy.
> I'd cap it so we can never remove more than 50% of the fleet automatically."

## Numbers

| Quantity | Order of magnitude |
|---|---|
| Envoy/Nginx throughput | 50k–100k rps/node |
| Added latency, L7 proxy | 0.1–1 ms |
| Added latency, mesh sidecar (both sides) | 0.5–2 ms |
| Safe health check interval | 1–5 s, 2–3 failures to eject |

## Referenced by

- [Consistent hashing](../fundamentals/consistent-hashing.md)
- [Primitives index](README.md)

## Sources & further reading

- Repo notes: [../../basic/prep/Load%20Balancer.md](../../basic/prep/Load%20Balancer.md), [../../basic/prep/Reverse%20proxy%20%28web%20server%29.md](../../basic/prep/Reverse%20proxy%20%28web%20server%29.md)
- Vendor: `10-resources/vendor/system-design-primer/README.md` — load balancer, reverse proxy
- [AWS Builders' Library — Using load shedding to avoid overload](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/)
