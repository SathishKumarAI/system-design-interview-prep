---
title: Flashcards
type: drill
track: universal
status: drafted
updated: 2026-09-02
tags: [recall, numbers]
---

# Flashcards

Recall these **without thinking**. Cover the right column. Ten minutes a day; test yourself
blind once a week and only revisit what you miss.

## Numbers

| Prompt | Answer |
|---|---|
| Seconds in a day | 86,400 ≈ 1e5 |
| L1 / DRAM reference | ~1 ns / ~100 ns |
| NVMe 4 KB random read | ~15 µs |
| Same-datacenter round trip | ~500 µs |
| Cross-continent RTT | ~150 ms |
| Read 1 MB from memory / NVMe | ~5 µs / ~80 µs |
| 1 Gbps in MB/s | 125 MB/s |
| 1M rows × 1 KB | 1 GB |
| 1 TB/day in MB/s | ~12 MB/s |
| Redis throughput per node | ~100k ops/s |
| Postgres reads / writes per node | ~10k qps / ~5k tps |
| Kafka broker | 100k–1M msg/s |
| WebSocket connections per tuned node | 50k–200k |
| 99.9% downtime per month | 43 minutes |
| 99.99% downtime per month | 4.3 minutes |
| vCPU cost per month | ~$30 |
| Internet egress per GB | ~$0.05–0.09 |
| Object storage per GB-month | ~$0.023 |
| H100-class GPU per hour | ~$2–5 |
| Embedding, 768-dim fp32 | 3 KB (768 B at int8) |
| HyperLogLog size / error | ~12 KB / 0.81% |

## Trade-offs (say buys → costs)

| Prompt | Answer |
|---|---|
| Cache | Latency + DB load ← staleness, invalidation bugs, memory |
| Replica | Read throughput + availability ← replication lag, split-brain risk |
| Shard | Write throughput + dataset size ← cross-shard queries, hot shards, rebalancing |
| Queue | Burst absorption + decoupling ← latency, duplicates, ordering, lag |
| Index | Read speed ← write speed, storage |
| CDN | Latency + egress cost ← invalidation, staleness |
| Consensus | Correctness under partition ← latency, availability, ops pain |
| Denormalisation | Read speed ← write amplification, consistency risk |
| Microservices | Team autonomy ← network hops, partial failure, ops surface |
| LSM vs B-tree | Write throughput ← compaction cost and latency spikes |
| Fanout on write | Fast reads ← celebrity problem, wasted work |
| Fanout on read | Cheap writes ← slow reads for users following many accounts |
| Erasure coding vs 3x replication | ~2x storage saving ← reconstruction CPU + read amplification |
| Streaming vs batch | Freshness ← state, watermarks, exactly-once complexity, debugging |

## Definitions you must state precisely

| Prompt | Answer |
|---|---|
| CAP | During a **partition**, choose availability or consistency. Says nothing about normal operation |
| PACELC | If Partition: A or C; Else: Latency or Consistency |
| Linearizable | Reads see the most recent completed write; behaves like a single copy |
| Read-your-writes | A user always sees their own writes; a session guarantee, cheap to provide |
| Write skew | Two transactions each read, each decide, together they break an invariant. Snapshot isolation does **not** prevent it |
| Exactly-once delivery | Impossible in general. Achieve exactly-once **effects** = at-least-once delivery + idempotent consumer |
| Idempotency key | Client-generated per *intent* (not per attempt); enforced with a unique constraint in the same transaction as the effect |
| Fencing token | Monotonic token from the lock service; storage rejects stale tokens. Fixes the GC-pause zombie-lock problem |
| Quorum | R + W > N. Typical N=3, W=2, R=2 |
| Consensus quorum | Majority: 2f+1 nodes tolerate f failures — 3 or 5, never 4 |
| Outbox pattern | Write the event to a table in the same transaction as the state change; a relay/CDC publishes it |
| Saga | Sequence of local transactions with compensating actions. Compensation ≠ rollback |
| Back-pressure | Explicitly slowing/rejecting producers instead of buffering unboundedly |
| Error budget | 100% − SLO; the failure you're allowed to spend before features freeze |
| Cell architecture | Shard the whole stack per tenant group so blast radius is 1/N |
| Consistent hashing | Keys and nodes on a ring; adding a node moves ~1/N of keys. Needs virtual nodes |
| Bloom filter | Probabilistic set membership; no false negatives, tunable false positives |

## Frontend

| Prompt | Answer |
|---|---|
| LCP / INP / CLS thresholds | < 2.5 s / < 200 ms / < 0.1 |
| What replaced FID, and when | INP, March 2024 |
| Long task threshold | 50 ms |
| Initial JS budget | < 150–200 KB compressed |
| Three kinds of state | Server state, client state, URL state |
| Why cursor pagination | Offsets duplicate and skip when the list mutates underneath |
| CRDT vs OT | CRDT converges without a central server (good offline); OT needs a server and correct transform functions |

## Data

| Prompt | Answer |
|---|---|
| Event time vs processing time | Aggregate on event time; processing time gives wrong answers when anything is delayed |
| Watermark | "No events older than X expected"; triggers window firing |
| Exactly-once into a table | Streaming checkpoints + transactional sink (2-phase commit into Iceberg) |
| Target Parquet file size | 128–512 MB |
| Merge-on-read vs copy-on-write | MoR: cheap writes, slower reads (CDC). CoW: expensive writes, fast reads |
| Medallion layers | Bronze raw immutable → silver cleaned → gold marts |
| Write-audit-publish | Write to a branch, run checks, then atomically publish |

## ML / GenAI

| Prompt | Answer |
|---|---|
| Why not accuracy on imbalanced data | 99.9% accuracy by predicting "never fraud". Use PR-AUC and an operating point |
| Training–serving skew | Feature computed differently in training vs serving. Fix with one definition + logging served values |
| Point-in-time correctness | As-of join on (entity, timestamp), respecting TTL **and** feature availability lag |
| Two-stage ranking | Candidate generation (millions → hundreds, cheap) then ranking (hundreds → ordered, expensive) |
| Data vs concept drift | Input distribution moved vs input→label relationship moved. Different fixes |
| Highest-value ML alert | Feature null / default rate |
| Continuous batching | Schedule at iteration level; finished sequences leave, new ones join. Big throughput win |
| PagedAttention | Page the KV cache in blocks like virtual memory; removes fragmentation, enables prefix sharing |
| PD disaggregation | Separate GPU pools for prefill (compute-bound) and decode (bandwidth-bound); KV transferred between them |
| Biggest RAG quality win | Hybrid retrieval (dense + BM25, fused) plus a reranker |
| LLM-as-judge failure modes | Position bias, verbosity bias, self-preference, drift when the judge changes |
| Biggest GenAI cost lever | Model routing (small model for the easy majority), then caching, then context size |

## Sentences to have ready

- "This is a read-heavy problem, so the design is a cache and CDN problem, not a database problem."
- "At-least-once delivery with idempotent processing, which gives exactly-once effects."
- "None of these dependencies may take checkout down; here is each one's degraded mode."
- "The SLO is X, which gives us an error budget of Y minutes a month — that's what justifies Z."
- "Egress dominates the bill, so the CDN is the first thing I'd build, not the last."
- "I'd start with the boring version and add complexity only where a requirement forces it."
