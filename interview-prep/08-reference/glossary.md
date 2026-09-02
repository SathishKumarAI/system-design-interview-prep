---
title: Glossary
type: reference
track: universal
status: drafted
updated: 2026-09-02
tags: [glossary]
---

# Glossary

Terms you should be able to define in one sentence, precisely. Grouped, not alphabetised —
you look these up by topic.

## Scaling and distribution

| Term | Definition |
|---|---|
| **Vertical scaling** | Bigger machine. Simple, has a ceiling, single point of failure |
| **Horizontal scaling** | More machines. Needs statelessness or partitioning |
| **Replication** | Same data on several nodes. Buys availability + read throughput |
| **Partitioning / sharding** | Different data on different nodes. Buys write throughput + capacity |
| **Consistent hashing** | Keys and nodes on a ring; adding a node moves ~1/N of keys. Needs virtual nodes |
| **Virtual nodes** | Many ring positions per physical node, so load spreads evenly |
| **Hot key / hot shard** | One key or partition receiving disproportionate traffic |
| **Scatter-gather** | Query fans out to all shards and merges; latency = slowest shard |
| **Cell architecture** | Shard the entire stack per tenant group so a failure hits 1/N of users |
| **Federation** | Split databases by function (users DB, orders DB) rather than by key |

## Consistency

| Term | Definition |
|---|---|
| **CAP** | During a network partition, choose availability or consistency |
| **PACELC** | If Partition: A or C; Else: Latency or Consistency |
| **Linearizability** | Reads return the most recent completed write; behaves like one copy |
| **Sequential consistency** | All nodes see operations in the same order, not necessarily real time |
| **Causal consistency** | Causally related operations are ordered; concurrent ones may differ |
| **Eventual consistency** | Replicas converge if writes stop |
| **Read-your-writes** | A user always sees their own writes |
| **Monotonic reads** | A user never sees time go backwards |
| **Replication lag** | How far behind a follower is, in time or bytes |
| **Split brain** | Two nodes both believe they're the leader |
| **Fencing token** | Monotonic token from a lock service; storage rejects stale ones |
| **Quorum** | R + W > N guarantees read/write overlap |
| **Raft / Paxos** | Consensus algorithms producing a totally ordered replicated log |
| **HLC / vector clock** | Logical clocks used to order events without trusting wall clocks |
| **CRDT** | Data type that converges under any merge order; enables offline collaboration |
| **OT** | Operational transform — transforms concurrent edits; needs a central server |

## Transactions

| Term | Definition |
|---|---|
| **ACID** | Atomicity, Consistency, Isolation, Durability |
| **Isolation levels** | Read uncommitted → read committed → snapshot/repeatable read → serializable |
| **Write skew** | Two transactions each read, decide, and together violate an invariant. Snapshot isolation doesn't prevent it |
| **Lost update** | Concurrent read-modify-write; one write disappears |
| **Optimistic concurrency** | Version column + compare-and-set; retry on conflict |
| **2PC** | Two-phase commit. Correct but blocking; avoid across services |
| **Saga** | Sequence of local transactions with compensating actions |
| **TCC** | Try-Confirm-Cancel: reserve, then confirm or cancel |
| **Outbox pattern** | Event row written in the same transaction as the state change; a relay publishes it |
| **Idempotency key** | Client-generated key per intent so retries don't duplicate effects |
| **Double-entry ledger** | Append-only entries summing to zero per transaction; balance = sum |

## Messaging

| Term | Definition |
|---|---|
| **Queue vs log** | Queue deletes on consume; a log retains and lets consumers replay by offset |
| **Consumer group** | Set of consumers sharing partitions; max parallelism = partition count |
| **Consumer lag** | How far behind the log a consumer is |
| **At-least-once / at-most-once** | Duplicates possible / losses possible |
| **Exactly-once effects** | At-least-once delivery + idempotent processing |
| **Log compaction** | Keep only the latest value per key — turns a topic into a table |
| **DLQ** | Dead-letter queue for messages that repeatedly fail |
| **Back-pressure** | Explicitly slowing or rejecting producers instead of buffering unboundedly |
| **Watermark** | "No events older than X expected"; drives window firing |
| **Event time vs processing time** | When it happened vs when you saw it |

## Reliability

| Term | Definition |
|---|---|
| **SLI / SLO / SLA** | Measurement / internal target / contractual promise |
| **Error budget** | 100% − SLO; the failure allowance for a period |
| **Circuit breaker** | Fail fast after an error threshold; probe before closing |
| **Bulkhead** | Isolated resource pools so one failure can't consume everything |
| **Load shedding** | Deliberately rejecting work to stay healthy |
| **Backoff + jitter** | Exponential retry delays with randomness to avoid synchronised waves |
| **Retry budget** | Cap on the fraction of traffic that may be retries |
| **Graceful degradation** | Reduced functionality instead of failure |
| **Blast radius** | How much breaks when one thing breaks |
| **RTO / RPO** | Time to recover / data you can afford to lose |
| **Metastable failure** | System stays broken after load returns to normal |
| **Thundering herd** | Many clients acting simultaneously after an event |
| **Cache stampede** | Many requests recompute the same expired key at once |

## Storage

| Term | Definition |
|---|---|
| **B-tree** | In-place updates, predictable reads; used by most relational engines |
| **LSM tree** | Append + compaction; high write throughput, compaction cost |
| **WAL** | Write-ahead log; durability and crash recovery |
| **Covering index** | Index containing every column a query needs |
| **Materialised view** | Precomputed query result, refreshed on a schedule or by changelog |
| **CDC** | Change data capture — streaming a database's changelog |
| **Erasure coding** | Data + parity fragments; durability at ~1.4x instead of 3x |
| **Bloom filter** | Probabilistic membership; no false negatives |
| **Tombstone** | Deletion marker in an append-only store |
| **Compaction** | Merging/rewriting files to reclaim space and speed reads |

## Frontend

| Term | Definition |
|---|---|
| **LCP / INP / CLS** | Core Web Vitals: load, responsiveness, visual stability |
| **Hydration** | Attaching JS behaviour to server-rendered HTML |
| **SSR / SSG / ISR** | Render per request / at build / rebuild on demand |
| **Islands** | Hydrate only the interactive parts of a page |
| **Virtualization** | Render only visible list items |
| **Optimistic update** | Apply locally before the server confirms; roll back on failure |
| **BFF** | Backend for frontend — a gateway shaped for one client type |

## ML / GenAI

| Term | Definition |
|---|---|
| **Training–serving skew** | Features differ between training and serving |
| **Point-in-time correctness** | Training rows contain only values available at prediction time |
| **Data drift / concept drift** | Input distribution moved / input→label relationship moved |
| **Candidate generation** | Cheap high-recall retrieval before expensive ranking |
| **Two-tower model** | Separate user and item encoders; item side precomputed, served by ANN |
| **ANN** | Approximate nearest neighbour search (HNSW, IVF-PQ) |
| **Calibration** | Predicted probabilities matching observed frequencies |
| **Multi-task head** | One trunk, several prediction heads combined into a value score |
| **Shadow mode** | Run a model on live traffic without serving its output |
| **Holdback** | A cohort permanently kept on the old system for long-run comparison |
| **RAG** | Retrieve documents, put them in the prompt, generate a grounded answer |
| **Hybrid retrieval** | Dense (embedding) + lexical (BM25), fused (e.g. reciprocal rank fusion) |
| **Reranker** | Cross-encoder that reorders retrieved candidates by joint relevance |
| **Groundedness** | Fraction of claims supported by the cited sources |
| **KV cache** | Cached attention keys/values; grows per token and limits concurrency |
| **Continuous batching** | Iteration-level scheduling so finished sequences leave the batch immediately |
| **PagedAttention** | Paged KV cache memory; removes fragmentation, enables prefix sharing |
| **Chunked prefill** | Interleaving prompt processing with decoding to smooth latency |
| **PD disaggregation** | Separate GPU pools for prefill and decode |
| **Speculative decoding** | Small draft model proposes tokens; large model verifies several at once |
| **Quantisation** | Lower-precision weights/activations (fp8/int8/int4) for memory and speed |
| **LLM-as-judge** | Using a model to score outputs; watch position/verbosity/self-preference bias |
