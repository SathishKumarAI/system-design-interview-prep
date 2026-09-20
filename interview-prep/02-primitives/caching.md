---
title: Caching
type: primitive
track: universal
difficulty: core
status: drafted
sources: [system-design-primer, DDIA]
updated: 2026-09-02
tags: [cache, redis, invalidation, hot-key]
---

# Caching

> [!info] Being split — staff-level versions live in `fundamentals/`
> Three of the four topics here now have their own page with internals, arithmetic and cited
> incidents ([ADR-0001](../../docs/adr/0001-split-primitives-into-atomic-fundamentals.md)):
> [caching-strategies](../fundamentals/caching-strategies.md) ·
> [cache-invalidation](../fundamentals/cache-invalidation.md) ·
> [cache-failure-modes](../fundamentals/cache-failure-modes.md).
> Still only here: **Redis internals** — this file stays until `redis-internals.md` exists.
> Use this page as the fast revision sheet; use `fundamentals/` to learn the mechanism.

## What it is

Keeping a copy of an answer closer to the asker than the source of truth. Buys latency and
load reduction; pays with **staleness** and a whole class of bugs that only appear under
concurrency.

## Where to cache — cheapest first

| Layer | Latency | Invalidation difficulty | Use for |
|---|---|---|---|
| Client / browser | 0 | Hardest (you can't reach it) | Immutable assets with versioned URLs |
| CDN edge | 10–50 ms | Hard (purge is slow) | Static + cacheable dynamic responses |
| Reverse proxy (Varnish/Nginx) | ~1 ms | Medium | Full-page, per-path |
| **Application cache (Redis/Memcached)** | 0.5–2 ms | Easy | Objects, query results, computed views |
| Local in-process (LRU) | ~100 ns | Hard (N copies to invalidate) | Tiny hot config, feature flags, tokenizers |
| Database buffer pool | µs | Automatic | Free; already there |

Rule: cache as far out as the freshness requirement allows. Every layer outward is 10x
cheaper and 10x harder to invalidate.

## Patterns

| Pattern | How | Trade-off |
|---|---|---|
| **Cache-aside** (lazy) | App checks cache; on miss reads DB and populates | Default. Simple. First request always slow; stale window on writes |
| **Read-through** | Cache library fetches on miss | Same as above, hidden in the library |
| **Write-through** | Write goes to cache and DB synchronously | Cache always fresh; slower writes |
| **Write-behind** | Write to cache, flush to DB async | Fast writes; **data loss on cache node death** |
| **Refresh-ahead** | Refresh hot keys before TTL expiry | Hides latency; wasted work on cold keys |

**Invalidation strategies, in order of preference:**
1. **TTL** — simplest, self-healing, bounded staleness. Start here, always.
2. **Versioned key** (`user:42:v7`) — write bumps the version; old entries fall out by TTL.
   No delete needed, no race.
3. **Explicit delete on write** — races with concurrent reads repopulating stale data.
4. **Event-driven invalidation** off the DB changelog (CDC) — correct and scalable; more moving parts.

> [!warning] Trap
> Delete-on-write has a real race: reader misses → reads DB (old) → writer updates DB →
> writer deletes cache → reader writes its stale value into the cache, where it stays for a
> full TTL. Fixes: versioned keys, or set-with-TTL-only-if-absent, or delayed double-delete.

## The four cache disasters

| Disaster | What happens | Fix |
|---|---|---|
| **Stampede / dogpile** | Popular key expires; 10k requests hit the DB simultaneously | Request coalescing (single-flight), probabilistic early expiry, lock-and-refresh, stale-while-revalidate |
| **Hot key** | One key (celebrity, viral post) exceeds one node's capacity | Key replication across nodes (`key:{0..9}`), client-side local cache for that key, or a dedicated tier |
| **Cache penetration** | Requests for keys that don't exist bypass cache every time — often an attack | Cache the negative result with a short TTL; Bloom filter of existing keys |
| **Cold start after restart** | Empty cache; DB sees 100% of traffic and dies | Warm on deploy, rolling restarts, admission control, or make the DB survivable at full load |

## Eviction

| Policy | Best for |
|---|---|
| LRU | General purpose default |
| LFU | Skewed popularity that persists (Redis `allkeys-lfu`) |
| TTL/random | Simple, avoids LRU's scan pollution |
| FIFO | Rarely right |

**Sizing:** the hit rate curve is logarithmic — going from 50% → 90% hit rate is cheap,
90% → 99% often doubles the memory. Estimate the working set (hot 20% of a day's data) and
size for that, not for the whole dataset.

## Redis specifics worth knowing

- Single-threaded for commands: one slow `KEYS *` or a big `ZRANGE` blocks everything. Never
  run O(N) commands on production keys.
- Data structures earn their keep: sorted sets for leaderboards and feeds, hashes for objects,
  HyperLogLog for cardinality (~12 KB for billions of items, 0.81% error), streams for queues,
  bitmaps for daily-active flags.
- Persistence: RDB snapshots (fast restart, may lose minutes) vs AOF (durable, slower).
  A cache usually needs neither — but say that out loud, because if you use Redis as a
  *store* the answer changes.
- Cluster mode shards by hash slot; multi-key operations must be in the same slot
  (`{user42}:feed`, `{user42}:profile` — hash tags force colocation).

## Failure modes

| Failure | Symptom | Mitigation |
|---|---|---|
| Cache tier down | DB takes 100% of load and dies | Design the DB to survive it, or shed load / serve degraded |
| Stale data served after a write | User doesn't see their own post | Read-your-writes: route the writer's reads to the primary, or write to cache on write |
| Memory pressure → mass eviction | Hit rate collapses, latency spike | Alert on eviction rate and hit ratio, not just memory used |
| Serialization format change | Poison entries, deserialization errors | Version the key namespace on every schema change |

## Interview lines

> [!tip] Say this
> "TTL of 60 seconds gives us a bounded staleness window and removes the entire class of
> invalidation races. The product question is whether 60 seconds of stale data is
> acceptable here — for the feed yes, for the account balance absolutely not."

> [!tip] Say this
> "The celebrity account is a hot key, not a capacity problem. I'd replicate that one key
> across 10 slots and pick randomly at read time — same infra, 10x the ceiling."

## Numbers

| Quantity | Order of magnitude |
|---|---|
| Redis op | 0.5–2 ms over the network, ~100k ops/s/node |
| Local in-process cache | ~100 ns |
| Realistic hit rate, well-chosen keys | 90–99% |
| Memory for 100M small objects (200 B) | ~20 GB + overhead (~1.5x) |
| HyperLogLog | ~12 KB, 0.81% error |

## Referenced by

- [Cache invalidation](../fundamentals/cache-invalidation.md)
- [Caching strategies](../fundamentals/caching-strategies.md)
- [Consistent hashing](../fundamentals/consistent-hashing.md)
- [Design a distributed rate limiter](../03-backend-cases/rate-limiter.md)
- [Design a news feed](../03-backend-cases/news-feed.md)
- [Design a URL shortener](../03-backend-cases/url-shortener.md)
- [Hot shard mitigation](../fundamentals/hot-shard-mitigation.md)
- [Primitives index](README.md)
- [Replication lag and session guarantees](../fundamentals/replication-lag-and-session-guarantees.md)

## Sources & further reading

- Repo notes: [../../basic/prep/Cache.md](../../basic/prep/Cache.md), [../../basic/prep/Caching.md](../../basic/prep/Caching.md)
- Vendor: `10-resources/vendor/system-design-primer/README.md` — caching section
- Local book: `DE/System-Design/Designing Data Intensive Applications.pdf` — ch.1, ch.11 (derived data)
- [Redis docs — eviction policies](https://redis.io/docs/latest/operate/oss_and_stack/management/config/)
