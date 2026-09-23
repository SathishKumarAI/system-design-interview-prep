---
title: Networking and the edge
type: primitive
track: universal
difficulty: core
status: drafted
sources: [system-design-primer, HTTP/3 RFC 9114]
updated: 2026-09-02
tags: [dns, cdn, tls, http3, websocket, grpc]
---

# Networking and the edge

## What it is

Everything between the user's finger and your first server. It sets your floor latency —
you cannot be faster than the speed of light plus TLS handshakes — and it is where the
cheapest wins live, because work you never send to origin costs nothing to run.

## The path, in order

```
user → DNS resolution → anycast/edge PoP → TLS handshake → CDN (hit? done)
     → regional LB → API gateway → your service
```

Each hop is a place to cut latency and a place to fail.

## DNS

| Concept | What matters in a design |
|---|---|
| TTL | Low TTL = fast failover, more DNS queries. 60s is a common failover compromise |
| GeoDNS / latency-based routing | Sends users to the nearest region. Cheap multi-region routing, but caches badly at ISPs |
| Anycast | One IP announced from many PoPs; the network routes to the nearest. Better than GeoDNS for failover — no TTL wait |
| Health-checked failover | DNS failover is minutes, not seconds. **Never claim sub-minute failover via DNS** |

> [!warning] Trap
> "We'll fail over with DNS" as your only answer for a 99.99% SLA. Resolver TTL
> disobedience means minutes of stale routing. Real answer: anycast + connection draining,
> with DNS as the slow backstop.

## CDN

Cache static assets and increasingly dynamic responses at the edge.

- **Push CDN**: you upload; good for small, rarely changing catalogues.
- **Pull CDN**: first request populates the edge; the default for most systems.
- **Cache key** design matters: including a query param you didn't intend fragments the
  cache and your hit rate collapses. Normalise the key.
- **Invalidation**: versioned URLs (`/asset.<hash>.js`) beat purges. Purges are slow,
  rate-limited, and the source of "why is production still serving the old bundle".
- **Edge compute** (Workers/Lambda@Edge): personalise at the edge without going to origin —
  A/B assignment, auth checks, redirects, header rewriting.

**Why it's usually the biggest single win:** it removes both latency *and* egress cost.
See [cost-engineering.md](cost-engineering.md).

## TLS and connection setup

| | Round trips before first byte |
|---|---|
| TCP + TLS 1.2 | 3 RTT |
| TCP + TLS 1.3 | 2 RTT |
| TLS 1.3 session resumption (0-RTT) | 1 RTT (replay risk — never for non-idempotent requests) |
| QUIC/HTTP3 (new connection) | 1 RTT |
| QUIC resumption | 0 RTT |

At a 150 ms cross-continent RTT, dropping one round trip is 150 ms of user-visible time.
This is why terminating TLS at the edge PoP (near the user) and reusing a warm connection
back to origin is standard.

## HTTP versions and protocols

| Protocol | Use when | Watch out |
|---|---|---|
| HTTP/1.1 | Simplicity, legacy | Head-of-line blocking, 6 connections/host |
| HTTP/2 | Default for web | Multiplexed, but TCP-level head-of-line blocking under loss |
| HTTP/3 (QUIC/UDP) | Mobile, lossy networks | Solves HOL blocking, faster handshake; some corporate networks block UDP |
| **WebSocket** | Bidirectional, low-latency push (chat, presence, live dashboards) | Stateful connections = LB stickiness, connection-count capacity planning, reconnect storms |
| **SSE** | Server→client stream only (notifications, token streaming from an LLM) | Simpler than WS, works over plain HTTP, auto-reconnect built in |
| **Long polling** | Fallback where WS/SSE unavailable | Wastes connections; fine as a degradation path |
| **gRPC (HTTP/2)** | Internal service-to-service, strict schemas, streaming | Poor browser support without a proxy; harder to debug than JSON |
| **WebRTC** | Peer-to-peer audio/video, sub-100ms | NAT traversal, TURN relays, its own whole design problem |

> [!tip] Interview line
> "Feed reads are plain HTTP behind a CDN. The unread-count and typing indicators go over
> a WebSocket, which means I need a connection tier sized by *concurrent connections*,
> not rps — roughly 100k connections per node with tuned file descriptors, so 10M
> concurrent users is ~100 nodes plus headroom."

## Capacity units that differ from rps

- **Concurrent connections** (WebSocket, gRPC streams): memory + FD bound, ~50k–200k/node.
- **New connections/second**: TLS handshake CPU bound; a reconnect storm after a deploy can
  be 100x steady state. Stagger reconnects with jitter.
- **Bandwidth**: for media, this — not CPU — is what you buy.

## Failure modes

| Failure | Symptom | Mitigation |
|---|---|---|
| CDN cache miss storm (purge or cold PoP) | Origin traffic spikes 20x | Staged purge, origin shield layer, request coalescing at edge |
| DNS TTL disobedience | Traffic keeps hitting the dead region | Anycast, health-checked LB, don't rely on DNS for fast failover |
| Reconnect storm after a WS tier deploy | Thundering herd, tier can't come up | Jittered backoff, connection draining, capacity for 3x steady state |
| Slow client (mobile, poor network) | Connections pile up, threads exhausted | Async IO, per-connection timeouts, backpressure |
| Cross-AZ chatter | Latency + surprise egress bill | Zone-aware routing, colocate the chatty pair |

## Interview lines

> [!tip] Say this
> "Before I add servers: what fraction of these requests can be answered at the edge?
> If it's 90%, the origin design gets 10x easier and the egress bill drops by roughly the
> same factor."

> [!tip] Say this
> "p99 for our EU users is bounded below by ~150 ms if the write has to reach us-east.
> Either we accept it, or we put a write-capable replica in EU and take on conflict
> resolution. Which does the product need?"

## Numbers

| Quantity | Order of magnitude |
|---|---|
| Cross-continent RTT | 150 ms |
| Same-region RTT | 0.5 ms |
| TLS 1.3 handshake | 1 extra RTT |
| WebSocket connections per tuned node | 50k–200k |
| CDN hit ratio, well-designed static site | 95%+ |
| CDN egress vs origin egress | ~2–5x cheaper |

## Sources & further reading

- Vendor: `10-resources/vendor/system-design-primer/README.md` — DNS, CDN sections
- Vendor: `10-resources/vendor/system-design-101/` — networking diagrams
- Repo notes: [../../basic/prep/DNS.md](../../basic/prep/DNS.md), [../../basic/prep/CDN.md](../../basic/prep/CDN.md), [../../basic/prep/TCP%20UDP.md](../../basic/prep/TCP%20UDP.md)
- [RFC 9114 — HTTP/3](https://www.rfc-editor.org/rfc/rfc9114.html)
