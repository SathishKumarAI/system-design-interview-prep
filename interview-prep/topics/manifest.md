---
title: Topic manifest
type: index
track: universal
tier: P0
status: drafted
sources: [existing repo inventory, 2026 staff-level curricula]
updated: 2026-09-02
tags: [manifest, index, canonical]
---

# Topic manifest — the canonical list

**Read this before creating any file.** One topic, one canonical filename. The *aliases* column
lists names that must **never** become their own file — if you were about to create one, you
wanted the canonical file instead.

Not in the manifest? Add it here first, then create the file.

## How to read this

| Column | Meaning |
|---|---|
| **Canonical file** | The only permitted path for this topic |
| **Tier** | `P0` write first · `P1` write next · `P2` nice to have |
| **Aliases — never create** | Names that would be duplicates |
| **Action** | `rewrite` existing file to the staff contract · `split` from an existing file · `new` · `retire` |

**Action legend for `split`:** the source file today bundles several staff-depth topics into
one page. At principal level those are separate pages with their own failure modes and
trade-offs — that is the structural change, not "make it longer".

---

## 0. Structural change proposed

Today's `02-primitives/` has 12 files that each bundle 3–6 staff-level topics.
`consistency-and-consensus.md` alone covers CAP, PACELC, isolation levels, Raft, leases,
clocks and CRDTs — each of which is a page. The proposal:

```
interview-prep/
  topics/manifest.md          ← this file
  diagrams/components.md      ← shared Mermaid vocabulary (written)
  fundamentals/               ← 02-primitives/ split into atomic mechanism pages
  patterns/                   ← NEW: architectural patterns, extracted from primitives+cases
  comparisons/                ← NEW: cross-cutting matrices; retires 08-reference/tech-selection.md
  03-backend-cases/  04-frontend-cases/  05-data-cases/  06-ml-cases/   ← rewritten in place
  07-drills/ 08-reference/ 09-company-styles/ 10-resources/            ← unchanged (meta, not topics)
```

`02-primitives/` becomes `fundamentals/`. Existing primitive files are **not deleted** until
their content has landed in the split pages — each row below names its source.

> **Decided 2026-09-02 — D1–D4 approved, scope set to all 123 topics.**
> Recorded in [ADR-0001](../../docs/adr/0001-split-primitives-into-atomic-fundamentals.md).
> `patterns/` and `comparisons/` are created when their first batch is written, not before.

---

## 1. Fundamentals — mechanisms

`fundamentals/`. Atomic. Each page = one mechanism with its own internals, numbers and failure modes.

### 1.1 Network and edge

| Canonical file | Tier | Aliases — never create | Scope | Action |
|---|---|---|---|---|
| `dns-and-anycast.md` | P1 | dns.md, geodns.md, anycast.md | Resolution, TTL semantics, why DNS failover is minutes not seconds, anycast withdrawal | split ← networking-and-edge |
| `cdn-and-edge-caching.md` | P0 | cdn.md, edge-cache.md, pop.md | Pull vs push, cache-key design, purge vs versioned URLs, origin shield, edge compute | split ← networking-and-edge |
| `tls-and-connection-setup.md` | P1 | tls.md, quic.md, handshake.md | RTT ladder 1.2/1.3/0-RTT/QUIC, replay risk, termination placement, session resumption | split ← networking-and-edge |
| `application-protocols.md` | P1 | http2.md, http3.md, grpc.md, rest-protocol.md | h1/h2/h3 head-of-line behaviour, gRPC streaming, when UDP is blocked | split ← networking-and-edge |
| `long-lived-connections.md` | P0 | websockets.md, sse.md, connection-tier.md | Capacity as *connections* not rps, reconnect storms, draining, presence fan-out | split ← networking-and-edge |

### 1.2 Traffic management

| Canonical file | Tier | Aliases — never create | Scope | Action |
|---|---|---|---|---|
| `load-balancing-algorithms.md` | P0 | load-balancer.md, l4-vs-l7.md, lb.md | L4/L7, least-outstanding, power-of-two, EWMA, oscillation and damping | split ← load-balancing-and-gateways |
| `health-checking-and-draining.md` | P0 | health-checks.md, readiness.md | Liveness vs readiness, deep-check cascade, min-healthy floor, connection draining | split ← load-balancing-and-gateways |
| `api-gateway-and-bff.md` | P1 | gateway.md, bff.md, edge-api.md | What belongs at the edge vs the service; the ESB anti-pattern; per-client gateways | split ← load-balancing-and-gateways |
| `service-mesh.md` | P2 | sidecar.md, istio.md, envoy.md, ambient-mesh.md | Sidecar vs ambient, added latency, control-plane failure, when 20+ services justifies it | split ← load-balancing-and-gateways |
| `rate-limiting-algorithms.md` | P0 | throttling.md, token-bucket.md, quota.md | Token/leaky bucket, sliding window, local-vs-central accuracy trade, hot-key limiter | split ← 03/rate-limiter case |

### 1.3 Caching

| Canonical file | Tier | Aliases — never create | Scope | Action |
|---|---|---|---|---|
| [`caching-strategies.md`](../fundamentals/caching-strategies.md) ✅ | P0 | cache.md, cache-strategies.md, cache-patterns.md, caching.md | Aside/through/behind/refresh-ahead, layer placement economics | **written** ← caching |
| [`cache-invalidation.md`](../fundamentals/cache-invalidation.md) ✅ | P0 | invalidation.md, ttl.md, cache-coherence.md | TTL vs versioned keys vs CDC-driven; the delete-on-write race, proven | **written** ← caching |
| [`cache-failure-modes.md`](../fundamentals/cache-failure-modes.md) ✅ | P0 | stampede.md, dogpile.md, hot-key.md, cache-penetration.md | Stampede, hot key, penetration, cold start; single-flight, probabilistic expiry | **written** ← caching |
| `redis-internals.md` | P1 | redis.md, memcached.md | Single-threaded command loop, O(N) command hazards, cluster hash slots, hash tags, persistence | split ← caching |

### 1.4 Storage engines and data

| Canonical file | Tier | Aliases — never create | Scope | Action |
|---|---|---|---|---|
| [`storage-engines.md`](../fundamentals/storage-engines.md) ✅ | P0 | btree.md, lsm.md, lsm-tree.md, storage-internals.md | B-tree vs LSM internals, write/read/space amplification, compaction debt and latency cliffs | **written** ← storage-and-databases |
| [`indexing-and-query-planning.md`](../fundamentals/indexing-and-query-planning.md) ✅ | P0 | indexes.md, index-design.md, sql-tuning.md | Composite order, covering, partial, cardinality; why the planner ignores your index | **written** ← storage-and-databases |
| `serialization-and-schema-evolution.md` | P1 | protobuf.md, avro.md, encoding.md, schema-registry.md | Field-number compatibility, rolling deploys with both versions live, registry rules | new |
| `object-storage-internals.md` | P1 | s3-internals.md, blob-storage.md, erasure-coding.md | Erasure coding vs replication, durability arithmetic, scrubbing, first-byte latency | split ← storage-and-databases |
| `bloom-filters-and-sketches.md` | P1 | hyperloglog.md, hll.md, count-min.md, t-digest.md | Space/error trade, mergeability, where sketches silently mislead | new |
| `geospatial-indexing.md` | P1 | h3.md, s2.md, geohash.md, quadtree.md | Geohash edge problem, S2 vs H3 neighbour geometry, moving-object update cost | split ← 03/ride-hailing |
| `vector-search-and-ann.md` | P0 | ann.md, hnsw.md, ivf-pq.md, embeddings-index.md | HNSW vs IVF-PQ, recall@k vs exact, quantisation, filtered search correctness | split ← 06/rag-assistant |

### 1.5 Replication and partitioning

| Canonical file | Tier | Aliases — never create | Scope | Action |
|---|---|---|---|---|
| [`replication-topologies.md`](../fundamentals/replication-topologies.md) ✅ | P0 | replication.md, leader-follower.md, multi-leader.md | Single/multi-leader/leaderless, sync vs semi-sync vs async, RPO arithmetic | **written** ← replication-and-partitioning |
| [`replication-lag-and-session-guarantees.md`](../fundamentals/replication-lag-and-session-guarantees.md) ✅ | P0 | read-your-writes.md, monotonic-reads.md, stale-reads.md | The three anomalies, LSN-aware routing, why "read from replica" quietly breaks products | **written** ← replication-and-partitioning |
| [`partitioning-strategies.md`](../fundamentals/partitioning-strategies.md) ✅ | P0 | sharding.md, partitioning.md, shard-key.md | Range/hash/directory/geo; the three tests a partition key must pass | **written** ← replication-and-partitioning |
| [`consistent-hashing.md`](../fundamentals/consistent-hashing.md) ✅ | P1 | hash-ring.md, vnodes.md, rendezvous-hashing.md | Ring mechanics, virtual nodes, bounded loads, rendezvous as the alternative | **written** ← replication-and-partitioning |
| `rebalancing-and-resharding.md` | P1 | resharding.md, rebalance.md | Fixed-partition vs dynamic splitting, rate limiting, rebalance storms, online resharding | split ← replication-and-partitioning |
| [`hot-shard-mitigation.md`](../fundamentals/hot-shard-mitigation.md) ✅ | P0 | hot-partition.md, celebrity-problem.md, key-salting.md | Salting, splitting, dedicated shards, read-path caching; detection before it pages you | **written** ← replication-and-partitioning |

### 1.6 Consistency, coordination, time

| Canonical file | Tier | Aliases — never create | Scope | Action |
|---|---|---|---|---|
| [`consistency-models.md`](../fundamentals/consistency-models.md) ✅ | P0 | cap.md, cap-theorem.md, pacelc.md, eventual-consistency.md, linearizability.md | The ladder, CAP stated correctly, PACELC as the everyday trade, per-database placement | **written** ← consistency-and-consensus |
| [`transaction-isolation-levels.md`](../fundamentals/transaction-isolation-levels.md) ✅ | P0 | isolation.md, acid.md, write-skew.md, mvcc.md | MVCC mechanics, write skew proven, SSI abort behaviour, lost update | **written** ← consistency-and-consensus |
| [`consensus-raft-paxos.md`](../fundamentals/consensus-raft-paxos.md) ✅ | P0 | raft.md, paxos.md, zab.md, consensus.md | Election, log replication, membership change, why 3/5 not 4, cost per write | **written** ← consistency-and-consensus |
| [`leases-locks-and-fencing.md`](../fundamentals/leases-locks-and-fencing.md) ✅ | P0 | distributed-lock.md, redlock.md, fencing-token.md | The GC-pause zombie holder, fencing tokens, why a TTL lock is not mutual exclusion | **written** ← consistency-and-consensus |
| `clocks-and-ordering.md` | P1 | lamport-clock.md, vector-clocks.md, hlc.md, truetime.md | Logical vs vector vs hybrid, TrueTime commit wait, NTP failure modes | split ← consistency-and-consensus |
| `crdts-and-conflict-resolution.md` | P1 | crdt.md, lww.md, conflict-resolution.md | G/PN-counter, OR-set, RGA; tombstone growth; what CRDTs do *not* solve | split ← consistency-and-consensus |
| [`quorums-and-anti-entropy.md`](../fundamentals/quorums-and-anti-entropy.md) ✅ | P1 | quorum.md, read-repair.md, hinted-handoff.md, merkle-tree.md, gossip.md | R+W>N, sloppy quorums, read repair, Merkle-tree anti-entropy, gossip convergence | **written** |

### 1.7 Messaging and streams

| Canonical file | Tier | Aliases — never create | Scope | Action |
|---|---|---|---|---|
| [`log-vs-queue.md`](../fundamentals/log-vs-queue.md) ✅ | P0 | message-queue.md, queues.md, pubsub.md | Retention/replay/consumer-group semantics; when a queue is the correct smaller answer | **written** ← messaging-and-streams |
| [`kafka-internals.md`](../fundamentals/kafka-internals.md) ✅ | P0 | kafka.md, partitions.md, isr.md | ISR, `acks`/`min.insync.replicas`, rebalance protocols, compaction, tiered storage | **written** ← messaging-and-streams |
| [`delivery-semantics.md`](../fundamentals/delivery-semantics.md) ✅ | P0 | exactly-once.md, at-least-once.md, message-dedup.md | Why exactly-once delivery is impossible and exactly-once *effects* are not | **written** ← messaging-and-streams |
| [`stream-processing-semantics.md`](../fundamentals/stream-processing-semantics.md) ✅ | P0 | watermarks.md, event-time.md, windowing.md, flink.md | Event vs processing time, watermarks, late data, checkpoints, state size | **written** ← messaging-and-streams |
| `backpressure-and-consumer-lag.md` | P1 | backpressure.md, lag.md | Lag as the async-system health metric; shedding vs buffering; priority topics | split ← messaging-and-streams |

### 1.8 Transactions and correctness

| Canonical file | Tier | Aliases — never create | Scope | Action |
|---|---|---|---|---|
| [`idempotency.md`](../fundamentals/idempotency.md) ✅ | P0 | idempotency-keys.md, dedup.md, retry-safety.md | Key scope, in-flight collisions, storing the response, natural vs synthetic idempotence | **written** ← transactions-and-idempotency |
| `distributed-transactions.md` | P0 | 2pc.md, two-phase-commit.md, tcc.md, xa.md | 2PC blocking window, TCC reservations, single-partition avoidance as the real answer | split ← transactions-and-idempotency |
| `ledgers-and-double-entry.md` | P1 | ledger.md, double-entry.md, accounting.md | Append-only entries, balance materialisation, continuous invariant checking | split ← transactions-and-idempotency |

### 1.9 Reliability

| Canonical file | Tier | Aliases — never create | Scope | Action |
|---|---|---|---|---|
| [`timeouts-retries-backoff.md`](../fundamentals/timeouts-retries-backoff.md) ✅ | P0 | retries.md, backoff.md, jitter.md, timeout-budget.md | Deadline propagation, retry budgets, layered-retry amplification arithmetic | **written** |
| [`load-shedding-and-admission-control.md`](../fundamentals/load-shedding-and-admission-control.md) ✅ | P0 | load-shedding.md, admission-control.md, overload.md | Shed early and cheap, priority classes, queue-age drop, 429 semantics | **written** |
| [`cascading-and-metastable-failures.md`](../fundamentals/cascading-and-metastable-failures.md) ✅ | P0 | cascading-failure.md, metastable.md, retry-storm.md | Why load returning to normal doesn't recover the system; breaking the loop | **written** |
| [`tail-latency.md`](../fundamentals/tail-latency.md) ✅ | P0 | p99.md, hedged-requests.md, tail-at-scale.md | Fan-out amplification maths, hedged and tied requests, why averages lie | **written** |
| [`queueing-theory-basics.md`](../fundamentals/queueing-theory-basics.md) ✅ | P0 | littles-law.md, utilisation.md, capacity-math.md | Little's law, the utilisation/latency knee, why 80% utilisation is the ceiling | **written** |
| `capacity-planning.md` | P1 | headroom.md, autoscaling.md, peak-factor.md | Peak factors, headroom for failover, autoscaling lag, pre-warming | new |
| `multi-region-and-dr.md` | P1 | dr.md, active-active.md, failover.md, rto-rpo.md | Strategy ladder vs RTO/RPO, conflict resolution, evacuation drills, data residency | split ← reliability-patterns |

### 1.10 Operations

| Canonical file | Tier | Aliases — never create | Scope | Action |
|---|---|---|---|---|
| `slos-and-error-budgets.md` | P0 | slo.md, sli.md, sla.md, error-budget.md | Measuring at the edge, burn-rate alerting, budget as a release gate | split ← observability-and-delivery |
| `metrics-logs-traces.md` | P0 | observability.md, telemetry.md, tracing.md, cardinality.md | Signal economics, cardinality control, head vs tail sampling | split ← observability-and-delivery |
| `deployment-strategies.md` | P0 | canary.md, blue-green.md, feature-flags.md, rollout.md | Deploy ≠ release, automated abort criteria, flag debt | split ← observability-and-delivery |
| `incident-response.md` | P2 | oncall.md, postmortem.md, runbook.md | Blast radius, rollback rehearsal, blameless postmortems that actually close | split ← observability-and-delivery |

### 1.11 Security and tenancy

| Canonical file | Tier | Aliases — never create | Scope | Action |
|---|---|---|---|---|
| `authn-and-authz.md` | P0 | auth.md, jwt.md, oauth.md, rbac.md, zanzibar.md | Token lifetimes vs revocation lag, RBAC→ABAC→ReBAC, where each check belongs | split ← security-and-multitenancy |
| `multi-tenancy-isolation.md` | P0 | tenancy.md, noisy-neighbour.md | Isolation ladder, RLS as enforcement, whale tenants, per-tenant quotas | split ← security-and-multitenancy |
| `secrets-and-key-management.md` | P2 | kms.md, secrets.md, envelope-encryption.md | Envelope encryption, rotation, short-lived dynamic credentials | split ← security-and-multitenancy |
| `abuse-and-ddos.md` | P1 | ddos.md, bot-defence.md, scraping.md | Volumetric vs application-layer, edge absorption, enumeration defence | split ← security-and-multitenancy |
| `privacy-and-data-deletion.md` | P1 | gdpr.md, pii.md, right-to-erasure.md | Deletion across derived stores, backups and logs; residency in replication topology | new |

### 1.12 Cost

| Canonical file | Tier | Aliases — never create | Scope | Action |
|---|---|---|---|---|
| `cost-modelling.md` | P0 | cost.md, finops.md, cost-optimisation.md | Unit cost per request/user/token, dominant-term analysis, the lever ladder | rewrite ← cost-engineering |
| `01-numbers.md` *(stays at root)* | P0 | latency-numbers.md, back-of-envelope.md, estimation.md | Latency table, capacity arithmetic, availability maths, cost anchors | rewrite in place |

---

## 2. Patterns

`patterns/`. Composed solutions, not mechanisms. Each page: the shape, when it earns its
complexity, and the failure mode of applying it too early.

| Canonical file | Tier | Aliases — never create | Scope | Action |
|---|---|---|---|---|
| `outbox-pattern.md` | P0 | dual-write.md, transactional-outbox.md | The dual-write problem; relay vs CDC; ordering and dedup downstream | split ← transactions-and-idempotency |
| `saga-pattern.md` | P0 | saga.md, compensating-transaction.md | Choreography vs orchestration, compensation ≠ rollback, stuck-workflow detection | split ← transactions-and-idempotency |
| `cqrs.md` | P1 | command-query-separation.md | Read/write model split, when it's over-engineering, sync lag as product behaviour | new |
| `event-sourcing.md` | P1 | event-store.md | Append-only truth, projections, snapshotting, schema evolution over years of events | new |
| `change-data-capture.md` | P0 | cdc.md, debezium.md, binlog.md | Log-based capture, snapshot→stream handover, WAL-retention cliff | split ← 05/cdc-pipeline |
| `materialized-views-and-derived-data.md` | P0 | derived-data.md, read-models.md | Rebuildable derived stores as the core scaling idea; staleness contracts | new |
| `fanout-write-vs-read.md` | P0 | fanout.md, timeline-fanout.md, push-vs-pull-feed.md | The hybrid threshold, active-user-only fanout, cost arithmetic both ways | split ← 03/news-feed |
| `two-stage-retrieval-and-ranking.md` | P0 | candidate-generation.md, retrieve-and-rank.md | Recall/precision split, candidate budget vs latency, where it's wrongly skipped | split ← 06/recommender |
| `circuit-breaker.md` | P0 | breaker.md | State machine, threshold tuning, the missing-fallback anti-pattern | split ← reliability-patterns |
| `bulkhead.md` | P1 | resource-isolation.md, thread-pool-isolation.md | Pool-per-dependency, priority tiers, sizing under partial failure | split ← reliability-patterns |
| `graceful-degradation.md` | P0 | fallback.md, degraded-mode.md | Naming a degraded mode per dependency; when fallbacks make outages worse | split ← reliability-patterns |
| `cell-based-architecture.md` | P0 | cells.md, shuffle-sharding.md, blast-radius.md | Cells, shuffle sharding, per-cell deploys, the router as the new SPOF | new |
| `leader-election.md` | P1 | leader-lease.md | Election on top of consensus, lease renewal, split-brain prevention | new |
| `scatter-gather.md` | P1 | fan-out-fan-in.md | Latency = slowest shard, partial results, hedging, fan-out caps | new |
| `expand-contract-migration.md` | P0 | schema-migration.md, online-migration.md, dual-write-migration.md | Add-nullable → backfill → dual-write → switch → drop; revertible at every step | split ← storage-and-databases |
| `strangler-fig-migration.md` | P1 | strangler.md, legacy-migration.md | Routing façade, per-endpoint cutover, verification by shadow comparison | new |
| `backfill-and-reprocessing.md` | P0 | backfill.md, replay.md, restatement.md | Same code path as live, idempotent partitions, restatement policy | split ← 05/clickstream-lakehouse |
| `write-audit-publish.md` | P0 | wap.md, data-gating.md | Write to a branch, validate, atomic publish; stale beats wrong | split ← 05/data-quality-and-contracts |
| `pagination-patterns.md` | P1 | cursor-pagination.md, keyset-pagination.md, offset.md | Cursor vs keyset vs offset, stability under mutation, deep-page cost | new |
| `api-versioning.md` | P2 | versioning.md, backward-compatibility.md | Compatibility rules, sunset policy, client-version skew during rollout | new |

---

## 3. Comparisons

`comparisons/`. Cross-cutting matrices that reference topic pages instead of living inside one.
**Retires** `08-reference/tech-selection.md`, whose single mega-table becomes these.

| Canonical file | Tier | Aliases — never create | Scope | Action |
|---|---|---|---|---|
| `sql-vs-nosql-vs-newsql.md` | P0 | sql-or-nosql.md, database-selection.md | Access-pattern-first selection, where NewSQL's latency cost lands | new (retires part of tech-selection) |
| `oltp-database-matrix.md` | P0 | postgres-vs-mysql.md, dynamodb-vs-cassandra.md | Postgres/MySQL/Cassandra/Scylla/DynamoDB on write path, consistency, ops cost | new |
| `messaging-matrix.md` | P0 | kafka-vs-rabbitmq.md, sqs-vs-kafka.md, pulsar.md | Kafka/Pulsar/SQS/RabbitMQ/Kinesis on retention, ordering, delivery, ops | new |
| `row-vs-columnar.md` | P1 | oltp-vs-olap.md, parquet-vs-row.md | Layout, compression, predicate pushdown, why one store rarely serves both | new |
| `lakehouse-table-formats.md` | P0 | iceberg-vs-delta.md, hudi.md | Iceberg/Delta/Hudi on MoR vs CoW, catalogs, concurrent writers, engine support | new |
| `stream-engine-matrix.md` | P1 | flink-vs-spark.md, kafka-streams.md | Flink/Spark Structured Streaming/Kafka Streams on state, event time, exactly-once sinks | new |
| `api-protocol-matrix.md` | P1 | rest-vs-grpc.md, graphql.md | REST/gRPC/GraphQL on schema, streaming, caching, client cost, debuggability | new |
| `realtime-transport-matrix.md` | P1 | websocket-vs-sse.md, long-polling.md | WebSocket/SSE/long-poll/WebRTC on direction, infra cost, reconnect semantics | new |
| `crdt-vs-ot.md` | P1 | ot-vs-crdt.md | Convergence guarantees, offline support, metadata growth, server dependence | split ← 04/collaborative-editor |
| `erasure-coding-vs-replication.md` | P1 | ec-vs-replication.md | Durability per stored byte, reconstruction cost, hot vs cold tiering | split ← 03/object-storage-sync |
| `consistency-model-matrix.md` | P0 | pacelc-table.md, database-consistency.md | Per-system PACELC placement and what each buys at what latency | new |
| `monolith-vs-microservices.md` | P0 | microservices.md, modular-monolith.md | Team-topology-driven, not scale-driven; the distributed-monolith failure | rewrite ← 02/…, legacy basic/prep/Microservices.md |
| `compute-platform-matrix.md` | P1 | k8s-vs-serverless.md, lambda-vs-ecs.md | K8s/managed containers/serverless/VMs on cost curve, cold start, ops surface | new |
| `retrieval-strategy-matrix.md` | P0 | hybrid-search.md, bm25-vs-embeddings.md | Lexical vs dense vs hybrid vs reranked, with measured recall trade-offs | split ← 06/rag-assistant |
| `vector-store-matrix.md` | P1 | pinecone-vs-qdrant.md, pgvector.md | pgvector/Qdrant/Milvus/Pinecone on filtered search, scale, ops | new |
| `llm-build-vs-buy.md` | P0 | self-host-vs-api.md, inference-cost.md | Break-even arithmetic in tokens/month; quality, latency, data-policy axes | split ← 06/llm-serving-platform |
| `batch-vs-streaming.md` | P0 | lambda-vs-kappa.md, kappa-architecture.md | Freshness vs complexity, when micro-batch wins, Lambda's reconciliation tax | split ← 05/data-playbook |
| `ranking-model-matrix.md` | P2 | gbdt-vs-neural.md | GBDT vs neural rankers on tabular features, latency, iteration speed | new |

---

## 4. Case studies

Existing 26 stay where they are and are **rewritten in place** to the staff contract. Gaps below
are new. Case studies are expected to run long.

### 4.1 Backend — `03-backend-cases/` (existing, rewrite)

| Canonical file | Tier | Aliases — never create | Action |
|---|---|---|---|
| `url-shortener.md` | P1 | tinyurl.md, link-shortener.md | rewrite |
| `rate-limiter.md` | P0 | throttler.md | rewrite (mechanism moves to fundamentals) |
| `news-feed.md` | P0 | timeline.md, twitter.md, feed.md | rewrite (fanout moves to patterns) |
| `chat-messaging.md` | P0 | whatsapp.md, messenger.md, slack.md | rewrite |
| `notification-system.md` | P1 | push-notifications.md | rewrite |
| `search-typeahead.md` | P0 | autocomplete.md, search.md | rewrite |
| `object-storage-sync.md` | P1 | dropbox.md, google-drive.md, file-sync.md | rewrite + split out `s3-like-object-store.md` |
| `video-streaming.md` | P1 | youtube.md, netflix.md | rewrite |
| `ride-hailing.md` | P0 | uber.md, lyft.md, proximity-service.md | rewrite (geo index moves to fundamentals) |
| `payments-ledger.md` | P0 | payments.md, stripe.md | rewrite |
| `metrics-monitoring.md` | P0 | prometheus.md, time-series.md, observability-backend.md | rewrite |

### 4.2 Backend — new

| Canonical file | Tier | Aliases — never create | Scope |
|---|---|---|---|
| `ticket-booking.md` | P0 | ticketmaster.md, seat-reservation.md, inventory-reservation.md | Strong-consistency reservation under contention; the case that punishes eventual consistency |
| `distributed-job-scheduler.md` | P0 | cron-at-scale.md, scheduler.md, task-queue.md | Exactly-once-ish execution, leader election, clock skew, long jobs |
| `s3-like-object-store.md` | P1 | object-store.md, blob-store.md | Split from object-storage-sync: placement, EC, repair, index scaling |
| `web-crawler.md` | P2 | crawler.md, spider.md | Politeness, frontier, dedup at 10^10 URLs, trap detection |
| `feature-flag-service.md` | P1 | config-service.md, flags.md | Global config with millisecond reads and no thundering herd on change |
| `multi-region-active-active.md` | P1 | global-deployment.md, geo-replication.md | Case-study form: conflict resolution, residency, evacuation |
| `ad-serving-and-auction.md` | P2 | ads.md, rtb.md | Sub-100ms auction, budget pacing, exactly-once billing events |
| `log-search-platform.md` | P2 | log-aggregation.md, elk.md | Ingest vs query economics, retention tiers, cardinality |
| `experimentation-platform.md` | P1 | ab-testing.md, experiments.md | Assignment, exposure logging, sequential testing, guardrail aborts |

### 4.3 Frontend — `04-frontend-cases/` (existing, rewrite)

| Canonical file | Tier | Aliases — never create | Action |
|---|---|---|---|
| `frontend-playbook.md` | P1 | radio.md | rewrite |
| `collaborative-editor.md` | P0 | google-docs.md, figma.md, multiplayer.md | rewrite (CRDT vs OT moves to comparisons) |
| `infinite-feed.md` | P1 | virtualized-list.md, feed-ui.md | rewrite |
| `realtime-dashboard.md` | P1 | trading-ui.md, live-charts.md | rewrite |
| `component-design-system.md` | P2 | design-system.md, component-library.md | rewrite |

### 4.4 Data — `05-data-cases/` (existing, rewrite) + gaps

| Canonical file | Tier | Aliases — never create | Action |
|---|---|---|---|
| `data-playbook.md` | P1 | de-playbook.md | rewrite (batch-vs-streaming moves to comparisons) |
| `clickstream-lakehouse.md` | P0 | event-ingestion.md, clickstream.md | rewrite |
| `cdc-pipeline.md` | P0 | debezium-pipeline.md | rewrite (CDC mechanism moves to patterns) |
| `realtime-analytics.md` | P0 | ad-click-aggregation.md, olap-serving.md | rewrite |
| `data-quality-and-contracts.md` | P1 | data-contracts.md, data-quality.md | rewrite |
| `metrics-and-semantic-layer.md` | P2 | semantic-layer.md, metrics-store.md | new |

### 4.5 ML / GenAI — `06-ml-cases/` (existing, rewrite) + gaps

| Canonical file | Tier | Aliases — never create | Action |
|---|---|---|---|
| `ml-playbook.md` | P1 | mlsd-playbook.md | rewrite |
| `recommender.md` | P0 | recsys.md, recommendations.md | rewrite |
| `feed-ranking.md` | P0 | engagement-prediction.md, ctr-prediction.md | rewrite |
| `fraud-detection.md` | P0 | abuse-detection.md, risk-scoring.md | rewrite |
| `feature-store.md` | P0 | feature-platform.md, feast.md | rewrite |
| `rag-assistant.md` | P0 | rag.md, retrieval-augmented-generation.md | rewrite (ANN + retrieval matrices move out) |
| `llm-serving-platform.md` | P0 | inference-platform.md, vllm.md, gpu-serving.md | rewrite |
| `ml-monitoring-and-eval.md` | P0 | drift.md, model-monitoring.md, evaluation.md | rewrite |
| `agentic-llm-platform.md` | P0 | agents.md, tool-calling.md, agent-platform.md | **new** — 2026 gap: tool loops, sandboxing, cost ceilings, eval of multi-step traces |
| `content-moderation.md` | P1 | moderation.md, trust-and-safety.md | new — human+model hybrid, appeals, latency asymmetry |
| `training-platform.md` | P2 | distributed-training.md, ml-training.md | new — data loading, checkpointing, spot interruption, multi-node |

---

## 5. Not topics — leave as is

`07-drills/`, `08-reference/glossary.md`, `09-company-styles/`, `10-resources/` are meta:
process, lookup and sourcing. They keep their current format and are **excluded** from the
staff-level section contract.

`08-reference/tech-selection.md` is the exception — it is **retired** into `comparisons/`
once those files exist, and replaced by a stub pointing there.

---

## 6. Counts and the honest recommendation

| Category | P0 | P1 | P2 | Total |
|---|---:|---:|---:|---:|
| Fundamentals | 27 | 17 | 3 | 47 |
| Patterns | 10 | 8 | 2 | 20 |
| Comparisons | 8 | 8 | 2 | 18 |
| Case studies | 18 | 14 | 6 | 38 |
| **Total** | **63** | **47** | **13** | **123** |

**123 files is more than you need.** The recommendation: write the **63 P0 files** and stop.
That set covers every mechanism a staff design round probes, every pattern worth naming, the
eight matrices that carry the trade-off arguments, and the 18 case studies that recombine them.
P1 fills gaps you'll notice from drill logs; P2 is optional.

At batches of 5 with a spot-check between, P0 is ~13 batches.

**Suggested batch order** (each batch is self-contained and immediately useful):

| Batch | Files |
|---|---:|
| 1 | consistency-models · transaction-isolation-levels · consensus-raft-paxos · leases-locks-and-fencing · quorums-and-anti-entropy |
| 2 | partitioning-strategies · replication-topologies · replication-lag-and-session-guarantees · hot-shard-mitigation · consistent-hashing |
| 3 | storage-engines · indexing-and-query-planning · caching-strategies · cache-invalidation · cache-failure-modes |
| 4 | log-vs-queue · kafka-internals · delivery-semantics · stream-processing-semantics · idempotency |
| 5 | timeouts-retries-backoff · load-shedding-and-admission-control · cascading-and-metastable-failures · tail-latency · queueing-theory-basics |
| 6 | outbox-pattern · saga-pattern · distributed-transactions · materialized-views-and-derived-data · expand-contract-migration |
| 7 | fanout-write-vs-read · cell-based-architecture · graceful-degradation · circuit-breaker · backfill-and-reprocessing |
| 8 | comparisons: sql-vs-nosql-vs-newsql · oltp-database-matrix · messaging-matrix · consistency-model-matrix · batch-vs-streaming |
| 9 | cases: news-feed · chat-messaging · ride-hailing · payments-ledger · ticket-booking |
| … | remaining P0 cases, then ML/GenAI, then the rest |

---

## 7. Decisions — settled 2026-09-02

Recorded in [ADR-0001](../../docs/adr/0001-split-primitives-into-atomic-fundamentals.md).
This section is history now; do not re-litigate it here — supersede the ADR instead.

| # | Decision | Outcome |
|---|---|---|
| **D1** | Rename `02-primitives/` → `fundamentals/` and split its 12 files into ~47 atomic pages? | **Approved.** Split is staged: a primitive file survives until every topic it carries has a successor page |
| **D2** | Add `patterns/` and `comparisons/`, retiring `08-reference/tech-selection.md` into the latter? | **Approved.** Folders are created with their first batch (6–8), not in advance; `tech-selection.md` is retired only once `comparisons/` exists |
| **D3** | Scope: write all 123, or P0 only (63)? | **All 123**, P0-first batch order retained. Reassess at the end of P0 (batch 13) |
| **D4** | Rewrite case files in place, or move under `case-studies/`? | **In place.** No renames, no moves — that is how the inbound links broke last time |

## 8. Progress

| Batch | Files | State |
|---|---|---|
| 1 | consistency-models · transaction-isolation-levels · consensus-raft-paxos · leases-locks-and-fencing · quorums-and-anti-entropy | ✅ written, link-checked, `docs/fundamentals-batch-1` |
| 2 | partitioning-strategies · replication-topologies · replication-lag-and-session-guarantees · hot-shard-mitigation · consistent-hashing | ✅ written, link-checked, `docs/fundamentals-batch-2` |
| 3 | storage-engines · indexing-and-query-planning · caching-strategies · cache-invalidation · cache-failure-modes | ✅ written, link-checked, `docs/fundamentals-batch-3` |
| 4 | log-vs-queue · kafka-internals · delivery-semantics · stream-processing-semantics · idempotency | ✅ written, link-checked, `docs/fundamentals-batch-4` |
| 5 | timeouts-retries-backoff · load-shedding-and-admission-control · cascading-and-metastable-failures · tail-latency · queueing-theory-basics | ✅ written, link-checked, `docs/fundamentals-batch-5` |
| 6 | **patterns/** (folder created here): outbox-pattern · saga-pattern · distributed-transactions · materialized-views-and-derived-data · expand-contract-migration | next |
| 7–13 | see §6 batch order | planned |

**25 / 123 written.** Fundamentals 25/47 · Patterns 0/20 · Comparisons 0/18 · Cases 0/38 rewritten.

## See also

- [../CONVENTIONS.md](../CONVENTIONS.md) — file format contract
- [../diagrams/components.md](../diagrams/components.md) — shared Mermaid vocabulary
- [../../CLAUDE.md](../../CLAUDE.md) — repo rules, section contract, definition of done

## Referenced by

- [ADR-0001: Split bundled primitives into atomic fundamentals pages](../../docs/adr/0001-split-primitives-into-atomic-fundamentals.md)
- [CLAUDE.md — system-design-prep](../../CLAUDE.md)
- [Diagram component library](../diagrams/components.md)
- [Docs index](../../docs/README.md)
- [Fundamentals index](../fundamentals/README.md)
- [STATUS](../../STATUS.md)

## Sources

- Repo inventory: 75 files under `interview-prep/`, 2026-09-02
- [Educative — advanced system design for principal engineers](https://www.educative.io/blog/advanced-system-design-for-principal-engineers)
- [daily.dev — best system design resources, beginner to staff level (2026)](https://daily.dev/blog/best-system-design-resources-beginner-to-staff-level/)
- [Algoroq — distributed systems interview questions for senior engineers (2026)](https://www.algoroq.io/interview-questions/distributed-systems/)
- [Distributed Computing From First Principles (arXiv 2506.12959)](https://arxiv.org/html/2506.12959v3)
