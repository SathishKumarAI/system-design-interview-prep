---
title: Replication and partitioning
type: primitive
track: universal
difficulty: core
status: drafted
sources: [DDIA ch.5-6]
updated: 2026-09-02
tags: [replication, sharding, consistent-hashing, hot-shard]
---

# Replication and partitioning

Two different problems that candidates constantly merge:

- **Replication** = the same data on several nodes. Buys availability + read throughput.
- **Partitioning (sharding)** = different data on different nodes. Buys write throughput +
  dataset size.

Most real systems need both: shard, then replicate each shard.

## Replication topologies

| Topology | How | Buys | Costs |
|---|---|---|---|
| **Single leader** | All writes to one node, async/sync copy to followers | Simple, no write conflicts | Leader is a write bottleneck + failover event |
| **Multi-leader** | Writes accepted in several regions, replicated both ways | Local write latency, region survives isolation | **Write conflicts** — you must define resolution |
| **Leaderless (quorum)** | Client writes to W nodes, reads from R | No failover step, tunable | Read repair, anti-entropy, R+W>N reasoning |

**Sync vs async replication** is the RPO question:
- Async: fast writes, **lose the tail on failover** (RPO > 0). Almost everyone's default.
- Sync: no data loss, but a slow/down replica stalls writes. Usually semi-sync: one
  synchronous replica, the rest async.

**Replication lag** is a design input, not a detail. Three anomalies to name:

| Anomaly | User sees | Fix |
|---|---|---|
| Read-your-writes | Posts a comment, refresh, it's gone | Route that user's reads to the leader for N seconds, or read from a replica caught up past their write LSN |
| Monotonic reads | Sees a comment, refreshes, it disappears | Pin a user to one replica (hash their ID) |
| Consistent prefix | Sees the answer before the question | Route causally related writes to the same partition |

> [!tip] Interview line
> "Reads go to replicas, except for the 5 seconds after a user's own write, which go to the
> primary. That gives read-your-writes without giving up replica scaling."

## Partitioning strategies

| Strategy | How | Good | Bad |
|---|---|---|---|
| **Range** | Shard by key ranges (dates, alphabetical) | Range scans are cheap | Hot shard on "today" or "A" |
| **Hash** | `hash(key) % N` or hash ranges | Even distribution | Range scans hit every shard |
| **Consistent hashing** | Keys and nodes on a ring; a node joining moves only 1/N of keys | Cheap rebalancing | Uneven without virtual nodes |
| **Directory / lookup table** | Explicit map key→shard | Total flexibility, easy rebalance | The map is a new SPOF and a hot path |
| **Geo / tenant** | Shard by region or customer | Data residency, isolation, blast radius | Uneven tenant sizes (the whale problem) |

**Virtual nodes**: each physical node owns many ring positions (100–256). Without them,
consistent hashing distributes badly and losing a node dumps its entire load on one neighbour.

**Choosing the partition key — the highest-signal decision in the whole interview.**
Test the candidate key against three questions:

1. Does it spread writes evenly? (Any timestamp prefix: no.)
2. Does it colocate the data one query needs? (Else every read is a scatter-gather.)
3. Does one value ever get disproportionately large? (Celebrity, whale tenant, `null`.)

| Bad key | Why | Better |
|---|---|---|
| `created_at` | All of today's writes hit one shard | `hash(entity_id)`, time as a *sort* key within the partition |
| `country` | Nigeria and Vatican City on equal shards | `hash(user_id)`, keep country as an attribute |
| `tenant_id` alone | One whale tenant = one melted shard | `(tenant_id, bucket)` with more buckets for big tenants |
| Monotonic ID | Hot tail on writes | Hash it, or use a scattered ID scheme |

## Hot shards and skew

Fixes, cheapest first:
1. **Salting**: `key#{0..N}` split across N sub-partitions; reads fan out to N.
2. **Split the hot partition** (dynamic splitting — DynamoDB and Bigtable do this for you).
3. **Cache in front** of the hot key.
4. **Dedicated shard** for the whale tenant.
5. **Change the key** — the real fix, the expensive one.

## Rebalancing

- **Never `hash % N`** — changing N remaps almost everything.
- Fixed number of partitions (e.g. 1024) assigned to nodes: adding a node moves whole
  partitions, not individual keys. Simple and what Kafka/Elasticsearch effectively do.
- Dynamic splitting: partitions split when they exceed a size threshold (HBase, DynamoDB).
- Rebalancing is IO-heavy — rate limit it, or you cause the outage you were preventing.
- **Automatic vs manual**: automatic rebalancing + a flapping health check = cascading
  rebalance storms. Semi-automatic (propose, human approves) is what many mature systems do.

## Cross-shard problems (say these before you're asked)

| Problem | Handling |
|---|---|
| Query spans shards | Scatter-gather: latency = slowest shard. Cap fan-out; consider a denormalised secondary index |
| Transaction spans shards | Avoid by design; else 2PC (blocking, slow) or a saga (see [transactions-and-idempotency.md](transactions-and-idempotency.md)) |
| Secondary index | Local index (per shard, scatter-gather reads) vs global index (extra store, async, eventually consistent) |
| Uniqueness constraint across shards | Needs a dedicated single-shard registry, or accept eventual detection |
| Join | Do it in a derived store, not at request time |

## Failure modes

| Failure | Symptom | Mitigation |
|---|---|---|
| Split brain (two leaders) | Divergent writes, lost data | Fencing tokens, quorum-based election, STONITH |
| Replication lag spike | Stale reads, failover would lose lots | Alert on lag seconds *and* bytes; shed read traffic |
| Rebalance storm | Latency spike during "routine" scaling | Rate-limit moves, off-peak, one node at a time |
| Whale tenant | One shard hot forever | Split/salt/dedicate — plan for it before it exists |

## Interview lines

> [!tip] Say this
> "Partition key is `hash(conversation_id)`, sort key `(timestamp, message_id)`. That
> colocates a conversation so pagination is a single-partition scan, and it spreads writes
> because conversation IDs are random. The known weakness is one enormous group chat, which
> I'd handle by splitting the conversation into time buckets."

> [!tip] Say this
> "I want 1024 fixed partitions from day one even though 8 nodes serve them. Then growth is
> moving partitions, never rehashing keys."

## Numbers

| Quantity | Order of magnitude |
|---|---|
| Virtual nodes per physical node | 100–256 |
| Practical partition size | 10–100 GB (rebalance time) |
| Replication factor | 3 (2 tolerates zero failures during maintenance) |
| Quorum | R + W > N; typical N=3, W=2, R=2 |
| Typical async replication lag | ms–seconds; minutes under load or long transactions |

## Sources & further reading

- Local book: `DE/System-Design/Designing Data Intensive Applications.pdf` — ch.5 (replication), ch.6 (partitioning)
- Repo notes: [../../basic/prep/Sharding.md](../../basic/prep/Sharding.md), [../../basic/prep/Database%20replication.md](../../basic/prep/Database%20replication.md), [../../basic/prep/Database%20partitioning.md](../../basic/prep/Database%20partitioning.md), [../../basic/prep/Federation.md](../../basic/prep/Federation.md)
- Vendor: `10-resources/vendor/system-design-primer/README.md` — sharding, federation
- [Amazon Dynamo paper (2007)](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
