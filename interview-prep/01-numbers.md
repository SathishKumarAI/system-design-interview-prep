---
title: Numbers — latency, capacity, cost
type: primitive
track: universal
difficulty: core
status: drafted
sources: [latency gist 2026, DDIA ch.1, Alex Xu v1 ch.2]
updated: 2026-09-02
tags: [estimation, latency, capacity, cost]
---

# Numbers

Back-of-envelope is not arithmetic homework. It is how you find out **which constraint
is the design**, in five minutes, before you draw anything. Memorise the orders of
magnitude, not the digits.

---

## 1. Latency, 2026 hardware

| Operation | Latency | In "1 ns = 1 second" human time |
|---|---|---|
| CPU register / L1 cache reference | ~1 ns | 1 second |
| Branch mispredict | ~3 ns | 3 seconds |
| L2 cache reference | ~4 ns | 4 seconds |
| Mutex lock/unlock (uncontended) | ~17 ns | 17 seconds |
| Main memory (DRAM) reference | ~100 ns | 1.5 minutes |
| Send 2 KB over 10 Gbps network | ~2 µs | 33 minutes |
| Read 1 MB sequentially from memory | ~5 µs | 1.5 hours |
| **NVMe SSD random read (4 KB)** | **~15 µs** | 4 hours |
| Read 1 MB sequentially from NVMe | ~80 µs | 22 hours |
| **Round trip in same datacenter** | **~500 µs** | 6 days |
| HDD seek | ~10 ms | 4 months |
| Read 1 MB sequentially from HDD | ~25 ms | 10 months |
| **Round trip CA ↔ Netherlands** | **~150 ms** | 5 years |

> [!warning] The 2026 shift that changes designs
> NVMe collapsed the memory→disk gap by three orders of magnitude. A same-datacenter
> network round trip (500 µs) is now **slower** than reading a megabyte off local NVMe
> (80 µs). "Disk is slow, network is fast" is a 2005 belief. In 2026 the expensive
> things are **network round trips and cross-region hops**, not local IO.

**Consequences you can say out loud:**
- Chatty service-to-service calls cost more than the disk reads they avoid. Batch, or colocate.
- N+1 query patterns across a network are ~500 µs × N; at N=100 that's your entire p99 budget.
- Cross-region synchronous writes cost 150 ms *minimum*. Any design promising 50 ms p99 with a
  synchronous cross-continent quorum is arithmetically impossible — say so; it's a classic trap.
- Caching in RAM buys ~100 ns vs ~15 µs NVMe vs ~500 µs remote. The big win is skipping the
  **network**, not skipping the disk.

---

## 2. Throughput per box (order of magnitude, commodity cloud instance)

| Component | Rough ceiling per node | Notes |
|---|---|---|
| Stateless API service (JSON, light logic) | 1k–10k rps/core-bound instance | Falls off fast with blocking IO |
| Nginx/Envoy proxy | 50k–100k rps | Connection-bound, not CPU-bound |
| Redis / Memcached | ~100k ops/s single-threaded, ~1M with pipelining | Single hot key kills it |
| PostgreSQL — simple indexed reads | 5k–20k qps | With connection pooling; more with replicas |
| PostgreSQL — writes | 1k–10k tps | fsync-bound; group commit helps |
| Cassandra/Scylla per node | 10k–100k ops/s | Scales linearly by adding nodes |
| Kafka broker | 100k–1M msg/s, 100+ MB/s | Sequential IO, page-cache bound |
| Elasticsearch/OpenSearch | 1k–10k queries/s per node | Depends brutally on query shape |
| Object store (S3-class) | Effectively unbounded, ~100 ms first-byte | Per-prefix limits are historical |

**Network:** 1 Gbps = 125 MB/s, 10 Gbps = 1.25 GB/s, 25 Gbps = 3.1 GB/s.
**NVMe:** 500k–1M IOPS, 3–7 GB/s sequential per drive.

> [!tip] Interview line
> "One Postgres primary gets us to roughly 10k writes/s. We need 40k, so either we
> shard by tenant now, or we absorb writes into Kafka and batch them. I'd start with
> the queue because it's reversible."

---

## 3. The arithmetic, in four lines

```
seconds/day    = 86,400  ≈ 1e5      (round; say you're rounding)
peak_rps       = DAU × actions_per_day / 1e5 × peak_factor      peak_factor = 3–5
storage/year   = writes/day × bytes/write × 365 × RF(3) × 1.3   (indexes + overhead)
bandwidth      = rps × bytes/response                            (then price the egress)
```

Powers of two, for byte math:

| | Bytes | Rough |
|---|---|---|
| KB | 10³ | thousand |
| MB | 10⁶ | million |
| GB | 10⁹ | billion |
| TB | 10¹² | trillion |
| PB | 10¹⁵ | — |

Useful anchors: 1M items × 1 KB = 1 GB · 1B items × 1 KB = 1 TB · 1 TB/day ≈ 12 MB/s ≈ 100 Mbps.

**Object sizes you should not have to ask about:**

| Thing | Size |
|---|---|
| UUID | 16 B |
| Timestamp | 8 B |
| Tweet/post row (text + metadata) | ~300 B–1 KB |
| User profile row | ~1 KB |
| Thumbnail | ~10 KB |
| Web page (HTML+CSS+JS, compressed) | ~1–3 MB |
| Photo (phone, JPEG) | ~3–5 MB |
| 1 min 1080p video (H.264) | ~50 MB |
| 1 min 1080p video (transcoded set, all renditions) | ~150 MB |
| Embedding, 768-dim float32 | 3 KB (768 B at int8) |

---

## 4. A worked example, minute by minute

*"Design Twitter."* 300M MAU, 150M DAU.

```
Writes: 150M DAU × 2 posts/day        = 300M posts/day
                                       ≈ 3,000 writes/s avg, ~10k peak
Reads:  150M DAU × 30 feed views/day  = 4.5B reads/day
                                       ≈ 45k reads/s avg, ~150k peak   ← the design
Ratio:  15:1 read-heavy

Storage: 300M × 500 B = 150 GB/day of post text
         × 365 × 3 (replication) ≈ 165 TB/year  ← boring; a few dozen machines
         Media: 10% of posts × 3 MB = 90 TB/day  ← NOT boring, this dominates

Cache:   hot 20% of a day's posts = 30 GB. Fits in RAM easily.
         Precomputed feeds: 150M users × 800 entries × 20 B ≈ 2.4 TB across a Redis fleet.

Bandwidth: 150k reads/s × 50 KB = 7.5 GB/s egress = 60 Gbps  ← CDN or you go bankrupt
```

Conclusion sentence — say exactly this shape: *"Text storage is a rounding error. This is a
**read-fanout and media-egress** problem. I'll spend my time on feed construction and on
keeping media off the origin."*

---

## 5. Availability arithmetic

| SLA | Downtime/year | Downtime/month | What it forces |
|---|---|---|---|
| 99% | 3.65 days | 7.2 h | Nothing. Single box |
| 99.9% | 8.77 h | 43 min | Redundancy + monitoring |
| 99.99% | 52.6 min | 4.3 min | Multi-AZ, automated failover, no manual steps |
| 99.999% | 5.26 min | 26 s | Multi-region active-active, and it will still be the humans who break it |

**Series vs parallel** — the thing candidates get wrong:
- Components in series (request must traverse all): availabilities **multiply**.
  Five 99.9% services in a chain = 99.5%. Adding services *lowers* availability.
- Redundant components in parallel: unavailability multiplies.
  Two 99% replicas = 99.99% — *if* failures are independent, which they are not
  (same AZ, same deploy, same config push, same cert expiry).

> [!tip] Interview line
> "Our chain is gateway → auth → service → DB. At 99.9% each that's 99.6% ceiling —
> below our target. So auth has to be cacheable and the DB path needs a degraded read
> mode, or we're promising something the topology can't deliver."

---

## 6. Cost anchors

Order-of-magnitude, US regions, on-demand list, 2026. **For interview arithmetic only** —
never quote these in a real design doc without the calculator.

| Resource | ~Unit cost | Rule of thumb |
|---|---|---|
| vCPU (general purpose VM) | ~$0.04/vCPU-hr | **~$30/vCPU-month** |
| RAM | ~$0.005/GB-hr | ~$4/GB-month |
| Block storage (SSD) | ~$0.08/GB-month | 1 TB ≈ $80/month |
| Object storage (standard) | ~$0.023/GB-month | 1 PB ≈ $23k/month |
| Object storage (archive) | ~$0.001–0.004/GB-month | 10–20x cheaper, hours to restore |
| **Egress to internet** | **~$0.05–0.09/GB** | **1 PB out ≈ $50–90k. This kills designs** |
| Cross-AZ traffic | ~$0.01–0.02/GB each way | Chatty services across AZs cost real money |
| CDN egress | ~$0.01–0.05/GB | Cheaper than origin egress *and* faster |
| Managed Kafka | ~$0.10/GB ingest + broker hrs | |
| GPU (H100-class, on-demand) | ~$2–5/GPU-hr | ~$2–4k/month reserved-ish |
| Serverless function | ~$0.20/M invocations + GB-s | Cheap until it isn't; ~1M rps is not its home |

**Cost sentences that score:**
- "Egress dominates: 60 Gbps sustained is ~600 TB/month ≈ $40k. Putting a CDN in front
  moves ~95% of it to $0.02/GB and cuts the bill by roughly 4x. That's the single biggest
  lever in this design."
- "Three replicas of 165 TB is 500 TB of SSD ≈ $40k/month. Tiering posts older than 30
  days to object storage takes it to about $12k for the same durability."
- "The GPU fleet is $180k/month at 60% utilisation. Batching and a smaller distilled model
  for the 80% easy queries is worth more than any infra tuning here."

---

## 7. Percentiles, because averages lie

- p50 is what you feel, **p99 is what you're paged for**, p99.9 is what your biggest
  customer experiences on every page load (they make 1000 requests, so they hit p99.9).
- A page making 20 parallel calls to a 99th-percentile-100ms service has a ~18% chance of
  at least one slow call. **Tail latency compounds with fan-out.** Mitigations: hedged
  requests, tied requests, fewer dependencies, timeouts shorter than the tail.
- Retries under load turn a partial outage into a full one. Retry budgets + jitter, always.

---

## 8. Numbers to have literally memorised

```
86,400 s/day ≈ 1e5          1M rows × 1 KB = 1 GB
1 Gbps = 125 MB/s           1 TB/day ≈ 12 MB/s
DRAM ~100 ns                NVMe 4K read ~15 µs
DC round trip ~500 µs       Cross-continent RTT ~150 ms
Redis ~100k ops/s           Postgres ~10k reads/s, ~5k writes/s
vCPU ≈ $30/month            Egress ≈ $0.05–0.09/GB
99.9% = 43 min/month down   99.99% = 4.3 min/month
```

---

## Referenced by

- [8-week study plan](07-drills/8-week-plan.md)
- [Cost engineering](02-primitives/cost-engineering.md)
- [Drills index](07-drills/README.md)
- [Interview playbook](00-interview-playbook.md)
- [Interview prep index](README.md)
- [Reference index](08-reference/README.md)
- [Repo index](../INDEX.md)
- [Resources index](10-resources/README.md)
- [System Design Interview Preparation](../README.md)

## Sources & further reading

- [Latency numbers every programmer should know — 2026 edition (gist)](https://gist.github.com/andreasbros/87fec32cf97aa41a1cbb64cc4dbdcd43)
- [Jeff Dean's original latency numbers (jboner gist)](https://gist.github.com/jboner/2841832)
- [Latency Numbers You Should Know in 2026 — Omar Bohsali](https://omarish.com/latency-numbers-you-should-know)
- Local book: `DE/System-Design/Designing Data Intensive Applications.pdf` — ch.1 (percentiles, SLOs)
- Local book: `AI/ML-Foundations/Alex Xu_ Sahn Lam - System Design Interview – An Insider's Guide_ Volume 2.epub` — back-of-envelope sections
- Vendor: `10-resources/vendor/system-design-primer/README.md` → "Powers of two" and "Latency numbers"
- Cloud pricing must be checked live: AWS / GCP / Azure calculators
