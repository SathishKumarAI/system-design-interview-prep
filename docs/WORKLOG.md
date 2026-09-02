---
title: Worklog
type: worklog
status: current
updated: 2026-09-02
tags: [history, decisions]
---

# Worklog

Dated entries. Newest first. Each entry records **what changed, how, why, and the trade-off** —
the reasoning is the part that isn't recoverable from the diff.

---

## 2026-09-02 — Batch 8: comparisons, and a backlog file

Branch: `docs/comparisons-batch-8` · PRs open: #1 (plan), #2–#9 (batches 1–8)

### What

`interview-prep/comparisons/` created — the second and last new folder — with five pages:
`sql-vs-nosql-vs-newsql`, `oltp-database-matrix`, `messaging-matrix`,
`consistency-model-matrix`, `batch-vs-streaming`. **40 of 123** written (fundamentals 25/47,
patterns 10/20, comparisons 5/18).

Also added `docs/BACKLOG.md` for unscheduled ideas, seeded with one: an
Excalidraw + `@excalidraw/mermaid-to-excalidraw` canvas that turns this vault's Mermaid diagrams
into editable elements. Filed rather than started, with the two questions that decide whether it is
worth doing at all.

### The bar that makes a comparison page different

Fundamentals explain a mechanism; patterns explain a shape; comparisons answer **"which do I pick,
and what do I regret?"** The folder README states the bar: **every column is a real decision axis —
write path, consistency, what breaks first, ops cost — not a feature checklist, and every page
commits to a recommendation.** A page that lists capabilities without naming the choice people get
wrong is a table, and vendors already publish tables.

Every one of the five defaults to the boring option, which is the honest through-line:

| Question | The answer this set commits to |
|---|---|
| SQL or NoSQL? | Relational until you can name the property that rules it out |
| Which OLTP engine? | Postgres unless a named constraint rules it out; compare on *what breaks first* |
| Which messaging system? | SQS unless you can name a second consumer or a replay requirement |
| Which consistency setting? | Per operation, written down and tested — defaults are weaker than assumed |
| Batch or streaming? | Batch → micro-batch → streaming, one step at a time, each justified by a decision that the freshness changes |

### Incidents and primary sources

| Page | Anchor |
|---|---|
| sql-vs-nosql-vs-newsql | **Notion (2021)** — sharded Postgres into **480 logical shards over 32 instances** rather than migrating to NoSQL, with "**shard earlier**" as the stated lesson |
| sql-vs-nosql · oltp-matrix | **Figma (2024)** — ~100× growth on RDS Postgres; vertical partitioning as a deliberate **stepping stone**, then a ~9-month horizontal sharding project. Binding constraints were **RDS IOPS and vacuum on multi-TB tables**, not the query engine |
| messaging-matrix | **Slack (2016 incident, 2017 redesign)** — a Redis-backed job queue hit its memory limit and **wedged in both directions**: new jobs could not be enqueued *and* existing jobs could not be dequeued, because dequeuing also needed memory. Fixing the original database contention did not release it. The fix was **Kafka in front of Redis**, not instead of it, at ~33 k jobs/s |
| batch-vs-streaming | **Uber (SIGMOD 2021)** real-time platform as the case where seconds are genuinely justified; Kreps for the Kappa reprocessing recipe |
| consistency-model-matrix | Vendor defaults themselves: MongoDB's `w: majority` with `readConcern: local`, Cassandra's `ONE`, DynamoDB's eventually-consistent reads, and **S3's move to strong read-after-write in Dec 2020** |

### The arguments worth keeping

- **Notion and Figma both scaled Postgres rather than leaving it.** That is the strongest available
  counter to "we need NoSQL for scale": 100 k writes/s is ~20 shards at a conservative per-shard
  rate, which is a tractable project, not a rewrite.
- **Vertical partitioning is a stepping stone, not a detour.** Figma's account is explicit that it
  bought runway cheaply *and* built the tooling and operational muscle the harder horizontal
  project then needed.
- **A memory-bound queue has a cliff and a metastable failure at it; a disk-backed log degrades
  into a backlog.** Slack's wedge is the cleanest published example, and it is why "durable buffer"
  beats "fast buffer" for anything that can fall behind.
- **Durability is not visibility.** `w: majority` makes a write durable; a `local` read concern can
  still return data that has not been majority-committed. The two dials are separate in every
  system that has them.
- **The end-to-end consistency model is the weakest link on the path** — a strictly serializable
  database behind a 60-second cache is a 60-second-stale system.
- **The window size dominates the streaming framework choice.** A 5-minute window with 30 s
  lateness and 60 s checkpoints gives ~5.5-minute end-to-end latency, which a 5-minute micro-batch
  matches with a fraction of the operational surface.

### A deviation from the plan, recorded

The manifest says `08-reference/tech-selection.md` is **retired into `comparisons/`** once those
files exist. It was **not** retired: only 5 of 18 comparison pages exist, and that file still
uniquely covers 13 decisions with no successor (columnar, table formats, protocols, transports,
vector stores, LLM build-vs-buy, and the rest). Retiring it now would delete reachable content —
exactly the failure the "delete only when empty of unique topics" rule exists to prevent.

It gained a banner instead, naming the five successors and stating that it becomes a stub when the
remaining 13 land. Same treatment as the seven primitive files.

### Verification

```
$ python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .
checked 1858 relative links; broken: 4          # the {rel_path} placeholders, unchanged
$ python ~/.claude/skills/staff-technical-docs/scripts/gen_backlinks.py .   # run twice
226 files scanned, 861 inbound links mapped, 0 changed
```

All 40 topic pages carry two Mermaid diagram types.

---

## 2026-09-02 — Batch 7: blast radius

Branch: `docs/patterns-batch-7` · PRs open: #1 (plan), #2–#8 (batches 1–7)

### What

Five more `patterns/` pages: `fanout-write-vs-read`, `cell-based-architecture`,
`graceful-degradation`, `circuit-breaker`, `backfill-and-reprocessing`. Patterns is now 10 of 20;
the manifest total is **35 of 123**.

Batch 6 was about atomicity you cannot have. Batch 7 is about **blast radius** — who is affected
when something fails, for how long, and what they see while it lasts.

### Incidents and primary sources

| Page | Anchor |
|---|---|
| graceful-degradation | **AWS S3, 28 Feb 2017** — a mistyped playbook input removed capacity supporting the index and placement subsystems; ~3 hours in us-east-1, recovery bounded by a full subsystem restart that had not been exercised at that scale for years. **The Service Health Dashboard could not be updated because it was hosted on S3**, so status moved to Twitter |
| cell-based-architecture | **AWS Route 53** — 2 048 virtual name servers, 4 per customer domain, **≈ 730 billion shuffle shards**; routing pushed to DNS so there is no request-path router to fail |
| fanout-write-vs-read | **Krikorian, Timelines at Scale** — Redis-materialised timelines capped at ~800 entries, celebrity accounts excluded from fanout and merged at read, ~300 k deliveries/s |
| circuit-breaker | Hystrix's defaults (20 requests / 10 s, 50%, 5 s sleep) and resilience4j's (100-call window, 60 s wait); Envoy outlier detection as the fleet-scale alternative |
| backfill-and-reprocessing | **Kreps, Questioning the Lambda Architecture** — second job from the start of retained history, new output table, higher parallelism, switch when caught up |

### The arguments worth keeping

- **Fan-out on write is the read-optimised one, not "the scalable one".** Its cost is unbounded on
  the follower distribution's tail. And the threshold everyone names (celebrity follower count) is
  usually *less* valuable than the one nobody does — **fan out only to recently active followers**,
  which on a mature graph removes most of the work.
- **Store ids, not posts.** 16 B vs 1–2 KB is ~100× the memory, and with ids a deleted or edited
  post is corrected everywhere at read time for free.
- **A cell that shares a database is not a cell.** The architecture's real blast radius is its
  most-shared component, so the exercise that matters is enumerating every dependency and asking
  "if this fails, how many cells go down?"
- **Shuffle sharding requires client retry across the assigned shard.** Without it, partial overlap
  becomes full impact and the combinatorics buy far less than the arithmetic suggests.
- **A breaker converts a slow failure into a fast one** — an improvement only if there is a
  fallback. And the fallback must be *strictly more local* than the primary, or it fails in the
  incident it exists for.
- **Successful degradation is invisible.** The request returns 200, latency is fine, error rate is
  zero — and a dependency has been dead for a week. Every fallback must emit a metric.
- **Availability arithmetic justifies the work**: six required 99.9% dependencies give ~99.4%
  (~3.6 h/month); making four optional gives ~99.8% (~86 min).
- **A backfill must run the production code path, write to a new output, be idempotent per
  partition, and be throttled** — and silent restatement destroys trust far longer than the
  original bug did.

### Trade-offs

- `reliability-patterns.md` is down to **bulkheads and multi-region DR**; it retires when
  `bulkhead.md` and `multi-region-and-dr.md` land.
- Two case files gained pointer banners rather than edits: `03-backend-cases/news-feed.md` →
  `fanout-write-vs-read`, `05-data-cases/clickstream-lakehouse.md` → `backfill-and-reprocessing`.
  The cases are rewritten in place in a later batch; a banner is the cheap correct move until then.
- Batch 8 creates `comparisons/` and retires `08-reference/tech-selection.md` into it — the second
  and last new folder, and the worklog entry for batch 6 records what folder creation costs.

### Verification

```
$ python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .
checked 1725 relative links; broken: 4          # the {rel_path} placeholders, unchanged
$ python ~/.claude/skills/staff-technical-docs/scripts/gen_backlinks.py .   # run twice
219 files scanned, 803 inbound links mapped, 0 changed
```

All 35 topic pages carry two Mermaid diagram types.

---

## 2026-09-02 — Batch 6: patterns, and the first new folder

Branch: `docs/patterns-batch-6` · PRs open: #1 (plan), #2–#7 (batches 1–6)

### What

`interview-prep/patterns/` created — the first new folder since the restructure began — with five
pages: `outbox-pattern`, `saga-pattern`, `distributed-transactions`,
`materialized-views-and-derived-data`, `expand-contract-migration`. **30 of 123** written
(fundamentals 25/47, patterns 5/20).

### The bar that makes a patterns page different

A fundamentals page explains how a mechanism works. A patterns page must additionally answer
**"when does this earn its complexity, and what does applying it too early cost?"** — stated as a
rule in the folder README and enforced in every page's Core concept.

The reason is that this category's failure mode is adoption without justification: a workflow
engine coordinating two tables in one database, an outbox for a consumer that lives in the same
schema. Every page therefore names the smaller answer explicitly, and all five converge on the same
one: **a single-partition design beats every distributed-atomicity pattern**, because the cheapest
distributed transaction is the one the data model made unnecessary.

### Incidents and primary sources

| Page | Anchor |
|---|---|
| distributed-transactions | **Jepsen: MongoDB 4.2.6** — snapshot-isolation violations *at the strongest read and write concerns*, plus "retrocausal" transactions; Jepsen's recommendation to say "snapshot isolated" rather than "ACID" |
| expand-contract-migration | **Stripe, Online migrations at scale (2017)** — ~100 M subscription objects; dual-write → backfill → move reads → stop old writes, with the transformation run **offline in Hadoop** and **dual reads comparing old vs new on every request** before the switch |
| materialized-views-and-derived-data | **Noria (OSDI 2018)** — partially-stateful dataflow: views that evict like caches and *discard writes to evicted state*, scaling to tens of millions of reads/s |
| outbox-pattern | Debezium's outbox router; Postgres logical decoding and the replication-slot behaviour |
| saga-pattern | Garcia-Molina & Salem (1987) — written about long-lived transactions in *one* database, decades before microservices |

### The arguments worth keeping

- **The outbox's real trap is the polling relay's id gap.** `bigserial` is allocated at INSERT, not
  at commit, so a relay ordering by id can advance past a row whose transaction commits a moment
  later — the event is never published, nothing errors. Fix by marking on ack, re-scanning a
  trailing window, or using CDC (commit-ordered by construction). This is the strongest argument
  for CDC over a hand-rolled relay and it is missing from most write-ups.
- **A stopped CDC connector fills the producer's disk.** Postgres retains WAL until every
  replication slot consumes it, so adopting CDC as a "read-only integration" acquires a new way to
  take down the primary.
- **Compensation is not rollback.** A refund appears on the statement next to the charge; an email
  cannot be unsent. That forces two design moves people skip: reorder sagas so irreversible steps
  are **last**, and build the *failed-compensation* state with an alert, a queue and a human owner.
- **2PC-over-consensus and XA-over-two-databases are not the same story.** Same protocol, entirely
  different availability. "Spanner uses 2PC" is not an argument for XA between your database and
  your broker.
- **Naming which stores are derived is worth more than the view pattern itself.** It decides backup
  policy, incident severity, and whether a corrupted index is a rebuild or a disaster — and the
  rebuild is only a real capability if it has been run recently.
- **Migrations are 5–7 revertible deploys.** Dual-write must precede backfill (or rows written
  during the copy are lost) and must outlive the read switch (or the switch has no revert).

### Trade-offs

- `transactions-and-idempotency.md` is now **nearly empty**: only ledgers/double-entry remains
  unique to it. It is retired the moment `ledgers-and-double-entry.md` (P1) lands. Its banner says
  so.
- `storage-and-databases.md` loses schema evolution to `expand-contract-migration`; it still holds
  store selection, object-storage internals and normalisation.
- Creating a folder costs more than five pages: a folder README, a root `INDEX.md` row, an
  `interview-prep/README.md` row, and a cross-link from `fundamentals/README.md`. Recorded here so
  batch 8 (`comparisons/`) budgets for it.

### Verification

```
$ python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .
checked 1630 relative links; broken: 4          # the {rel_path} placeholders, unchanged
$ python ~/.claude/skills/staff-technical-docs/scripts/gen_backlinks.py .   # run twice
214 files scanned, 758 inbound links mapped, 0 changed
```

All 30 topic pages carry two Mermaid diagram types.

---

## 2026-09-02 — Batch 5: reliability under overload

Branch: `docs/fundamentals-batch-5` · PRs open: #1 (plan), #2–#6 (batches 1–5)

### What

Five pages: `timeouts-retries-backoff` and `load-shedding-and-admission-control` split from
`reliability-patterns.md`; `cascading-and-metastable-failures`, `tail-latency` and
`queueing-theory-basics` **written from scratch** — the first batch that is mostly new pages
rather than splits. Fundamentals 25 of 47; manifest total 25 of 123.

### Written as one argument, not five essays

This is the structural choice worth recording. The five pages interlock deliberately:

1. `queueing-theory-basics` — the utilisation knee (`ρ/(1−ρ)`) and Little's law.
2. `tail-latency` — why fan-out drags every request into the knee (`1 − 0.99^100 = 63%`).
3. `timeouts-retries-backoff` — how retries multiply offered load past it (3 layers × 3 = **27×**).
4. `load-shedding-and-admission-control` — the control that keeps you left of the knee.
5. `cascading-and-metastable-failures` — what happens with no control: the system stays down after
   the trigger is gone.

Each page's "Numbers that matter" feeds the next page's argument, and all five cross-link back to
the same arithmetic rather than restating it.

### Incidents and primary sources

| Page | Anchor |
|---|---|
| queueing-theory-basics · load-shedding | **Facebook, Fail at Scale (ACM Queue 2015)** — CoDel plus adaptive LIFO in HHVM: bound queue *age*, and once a backlog forms serve the **newest** request first, because the oldest one's user has already left |
| tail-latency | **Dean & Barroso, The Tail at Scale (CACM 2013)** — hedging after a 10 ms delay cut BigTable's p99.9 from **1 800 ms to 74 ms for 2% more requests** |
| timeouts-retries-backoff · cascading | **AWS Kinesis, 25 Nov 2020** — a routine capacity addition pushed a full-mesh front-end fleet past the OS thread limit; ~17 hours, and recovery was bounded by *staged bootstrap*, not by the fix |
| cascading | **Bronson et al., HotOS 2021** — the vocabulary: stable, vulnerable, metastable; trigger vs sustaining effect |
| timeouts-retries-backoff | AWS's full-jitter comparison; Google SRE's client-side adaptive throttling (`max(0, (requests − 2×accepts)/(requests+1))`) |

### The arguments these pages make that the tutorials don't

- **"60% CPU" is not headroom.** The binding resource is usually a pool or a dependency, and
  utilisation targets exist because of `ρ/(1−ρ)`, not superstition. Also: targets must be set from
  the **post-failure** state — 5 nodes at 80% become 100% when one dies.
- **The tail is the common case.** At fan-out 100, a per-server p99 makes 63% of user requests
  slow. You must design each backend against p99.99, or reduce fan-out.
- **An attempt limit does not bound load; a retry budget does.** Three attempts still triples
  offered load when everything fails. 10% budgets and client-side throttling bound the system.
- **Shedding is not failure — goodput collapse is.** Accepting 15 k rps into a 10 k rps service
  produces 15 k timeouts at 100% utilisation: zero goodput, full cost.
- **If removing the trigger doesn't restore service, adding capacity won't either.** The exits are
  reduce the input or break the loop — both must be built before the incident.

### Trade-offs

- `reliability-patterns.md` kept and banner-marked: it still holds circuit breakers, bulkheads,
  graceful degradation and multi-region DR. The first three become `patterns/` pages in batch 7.
- Facebook's *Fail at Scale* is cited on two pages (queueing and shedding) for two different
  mechanisms; the 2010 Facebook outage from batch 3 is referenced as a cross-link, not re-told.
- Batch 6 creates `patterns/` — the first new folder since the restructure began.

### Verification

```
$ python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .
checked 1489 relative links; broken: 4          # the {rel_path} placeholders, unchanged
$ python ~/.claude/skills/staff-technical-docs/scripts/gen_backlinks.py .   # run twice
207 files scanned, 697 inbound links mapped, 0 changed
```

All 25 fundamentals pages carry two Mermaid diagram types.

---

## 2026-09-02 — Batch 4: messaging and delivery

Branch: `docs/fundamentals-batch-4` · PRs open: #1 (plan), #2–#5 (batches 1–4)

### What

Five pages: `log-vs-queue`, `kafka-internals`, `delivery-semantics`,
`stream-processing-semantics` from `messaging-and-streams.md`, and `idempotency` from
`transactions-and-idempotency.md`. Fundamentals 20 of 47; manifest total 20 of 123.

### Incidents and primary sources

| Page | Anchor |
|---|---|
| kafka-internals | Vanlightly's *How to lose messages on a Kafka cluster*: with `acks=all` and the **default** `min.insync.replicas=1`, an ISR shrunk to the leader still acknowledges writes — a subsequent leader failure loses acknowledged data with no error anywhere |
| delivery-semantics | **Jepsen: Redpanda 21.10.1** — three liveness and seven safety issues, including a single transaction processing *some but not all* of its records twice, and an off-by-one advancing the last stable offset past committed messages |
| stream-processing-semantics | **Pinterest** — slowed watermark progression in an inner join produced backpressure then checkpoint failures, because one high-volume topic starved another; fixed with per-topic rate limiting |
| idempotency | **Brandur / Stripe** — idempotency keys with foreign state mutations, atomic phases and recovery points; 24-hour key retention; the provider's record as the arbiter for unknown outcomes |
| log-vs-queue | Kafka's own `__consumer_offsets` as a compacted topic — the log used as a table, by the log itself |

### Why this framing

- **Exactly-once delivery is impossible; exactly-once effects are not.** Every vendor feature is
  the second thing, and it holds only inside a boundary that vendor controls. The moment a step
  calls a payment API the guarantee ends — so the honest sentence is "EOS inside Kafka,
  at-least-once at the edges, idempotent effects where it matters".
- **`acks=all` is half a durability setting.** Without `min.insync.replicas=2` it silently
  degrades to `acks=1` exactly when the cluster is unhealthy. Stated as the production baseline:
  RF=3, `min.insync.replicas=2`, `acks=all`, idempotent producer, unclean leader election off —
  *and* the cost that comes with it (two broker losses stop writes).
- **The watermark is only as fast as your slowest source partition.** An idle partition freezes
  the whole job's watermark: windows stop firing across every key while CPU and throughput look
  healthy. This is the streaming failure people lose a day to.
- **Idempotency is not deduplication.** Dedup handles the request that arrives twice; the
  expensive case is the request that died halfway, which needs a state machine with an explicit
  **unknown** state and a reconciler — not a cache of responses.
- **The log is not the upgrade over a queue.** A queue gives per-message retry, visibility
  timeouts and DLQs for free; on a log those are your code, and diverting a poison message to a
  retry topic silently reorders it after its successors.

### Trade-offs

- Both source files kept and banner-marked. `messaging-and-streams.md` still uniquely holds
  backpressure/consumer-lag; `transactions-and-idempotency.md` still holds 2PC, outbox, sagas and
  ledgers — those become `patterns/` pages in batch 6, so this file survives longest.
- `idempotency` was pulled into a messaging batch rather than waiting for its own, because
  `delivery-semantics` is incoherent without it: at-least-once is only safe if the effect is
  idempotent, and splitting them across branches would have left a dangling argument.

### Verification

```
$ python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .
checked 1386 relative links; broken: 4          # the {rel_path} placeholders, unchanged
$ python ~/.claude/skills/staff-technical-docs/scripts/gen_backlinks.py .   # run twice
202 files scanned, 654 inbound links mapped, 0 changed
```

All 20 fundamentals pages carry two Mermaid diagram types.

---

## 2026-09-02 — Batch 3: storage engines and caching

Branch: `docs/fundamentals-batch-3` · PRs open: #1 (plan), #2 (batch 1), #3 (batch 2), #4 (this)

### What

Five pages, and the first batch to split **two** source primitives at once:
`storage-engines` and `indexing-and-query-planning` from `storage-and-databases.md`;
`caching-strategies`, `cache-invalidation` and `cache-failure-modes` from `caching.md`.
Fundamentals is now 15 of 47; the manifest total is 15 of 123.

### Incidents and primary sources

| Page | Anchor |
|---|---|
| storage-engines | RocksDB write stalls — `level0_stop_writes_trigger` blocking writes **indefinitely** as designed backpressure; Uber's 2016 Postgres→MySQL write-amplification argument, **with** the HOT-update caveat that the usual retelling omits |
| indexing-and-query-planning | The same Uber case read as an indexing story (`ctid` vs primary-key pointers); Postgres extended statistics for correlated columns; Markus Winand's rebuttal |
| caching-strategies · cache-failure-modes | **Facebook, 23 Sept 2010** — invalid config value, every client self-repairing, error-as-invalidation feedback loop, 4 h, recovery required taking the site offline |
| cache-invalidation | **Meta, "Cache made consistent" (2022)** — Polaris measuring cache consistency from outside the service; TAO from six nines to **ten nines**; consistency tracing |
| cache-failure-modes | Facebook memcache **leases**; XFetch probabilistic early expiry (VLDB 2015); the HotOS 2021 metastable-failures framing |

### Why this framing

- **An LSM defers work, and deferred work arrives at a time you do not choose.** Write stalls are
  the engine braking on purpose — p99 goes from 1 ms to seconds with no error, no CPU saturation
  and no traffic change. Most write-ups describe compaction; almost none say the stall is the
  designed behaviour and name the trigger to alert on.
- **A cache's value is set by the miss path, not the hit path.** At 99% hit rate an empty cache is
  a **100×** database load multiplier, so the cache tier is a hard dependency whether or not the
  diagram admits it. The cold-start refill arithmetic (working set ÷ spare DB capacity) is the
  number to compute before a restart, not during one.
- **Invalidation's hard part is a race, not coverage.** The stale-set interleaving happens with
  *correct* code that fires the invalidation. That reorders the strategy ranking: versioned keys
  and leases (no race exists) above delete-on-write (a race you must win).
- **The planner ignores your index because its estimate is wrong.** Fix the estimate, not the
  join method — everything downstream of a bad row estimate is a bad decision.

### Trade-offs

- Both source files kept and banner-marked. `caching.md` still uniquely holds Redis internals;
  `storage-and-databases.md` still holds store selection, object-storage internals, normalisation
  and schema evolution. Same staging rule as batches 1–2.
- The Uber Postgres case is cited on **two** pages, deliberately, read two different ways —
  storage-engine amplification and index-pointer design. It is also the one place this set argues
  *against* its own source: the HOT-update caveat and Robert Haas's response are included, because
  citing the blog post uncritically is the common failure.
- Facebook 2010 appears in both `caching-strategies` (as the incident) and `cache-failure-modes`
  (as the mechanism). Same event, different lesson; cross-linked rather than duplicated.

### Verification

```
$ python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .
checked 1286 relative links; broken: 4          # the {rel_path} placeholders, unchanged
$ python ~/.claude/skills/staff-technical-docs/scripts/gen_backlinks.py .   # run twice
197 files scanned, 608 inbound links mapped, 0 changed
```

All 15 fundamentals pages carry two Mermaid diagram types.

---

## 2026-09-02 — Batch 2: the replication cluster

Branch: `docs/fundamentals-batch-2` · PRs open: #1 (plan), #2 (batch 1), #3 (this)

### What

Five pages split from `02-primitives/replication-and-partitioning.md`:
`partitioning-strategies`, `replication-topologies`, `replication-lag-and-session-guarantees`,
`hot-shard-mitigation`, `consistent-hashing`. Fundamentals is now 10 of 47; the manifest total is
10 of 123.

### Incidents and primary sources used

| Page | Anchor |
|---|---|
| replication-topologies | GitLab 2017-01-31 — lag treated as a nuisance, `rm -rf` on the primary, **five backup mechanisms all failed for five different reasons**; ~18 h down, permanent loss of 6 h of writes |
| partitioning-strategies · hot-shard-mitigation | Discord 2023 — hot partitions cascading latency on Cassandra; `(channel_id, bucket)` composite key; request coalescing in a Rust data-services tier; migration stalled at 99.9999% on tombstone-dense token ranges |
| hot-shard-mitigation | DynamoDB hard per-partition ceilings (3 000 RCU / 1 000 WCU), split-for-heat, and the fact that an **LSI blocks splitting** |
| replication-lag-and-session-guarantees | Facebook memcache (NSDI 2013) remote markers — mark the known-stale keys and redirect only those reads to the master region |
| consistent-hashing | Consistent Hashing with Bounded Loads (Google/Thorup); Vimeo runs it in HAProxy at `c = 1.25`; Cassandra's vnode default dropped 256 → 16 |

### Why this framing

Three arguments in these pages are the ones that change behaviour, and none of them are the
textbook version of the topic:

- **RPO is not a setting, it is `lag × write rate`.** At 5 000 writes/s and 800 ms p99 lag, an
  async failover loses ~4 000 committed writes. Teams can quote replica counts and cannot quote
  this.
- **Sharding fixes volume; it does nothing for skew.** A hot *key* hashes to one partition no
  matter how many partitions exist. Separating "hot key" from "hot partition" is the whole of
  `hot-shard-mitigation`, because the standard reflex (salting) is correct for write-hot keys and
  actively harmful for read-hot ones.
- **Consistent hashing bounds movement, not load.** Balance comes from vnodes; *load* balance
  needs bounded loads. The page also argues the unpopular position that a fixed logical-partition
  map beats a ring wherever membership changes under human control — which is what Redis, Kafka
  and Elasticsearch all chose.

### Trade-offs

- `replication-and-partitioning.md` kept and banner-marked: it still uniquely holds
  `rebalancing-and-resharding` (P1, later batch). Same staging rule as batch 1.
- Semi-sync's silent 10 s fallback to async and MySQL's `Seconds_Behind_Master` reporting 0 on a
  stalled IO thread are both documented as failure modes rather than footnotes — they are the
  reason "we have replication" and "we have durability" are different claims.
- `consistent-hashing` is P1 but was written in this batch because the other four pages reference
  it constantly; deferring it would have left four dangling explanations.

### Verification

```
$ python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .
checked 1186 relative links; broken: 4          # the {rel_path} placeholders, unchanged
$ python ~/.claude/skills/staff-technical-docs/scripts/gen_backlinks.py .   # run twice
192 files scanned, 563 inbound links mapped, 0 changed
```

All five pages carry two Mermaid diagram types. The `lint_docs.py --contract` "missing: Follow-up
questions" line is the known naming mismatch recorded in STATUS.md, not a gap.

---

## 2026-09-02 — Batch 1: the consistency cluster, and the decisions that unblocked it

Branch: `docs/fundamentals-batch-1` · PR for the plan branch: #1

### What

D1–D4 answered (all four recommendations approved; scope set to **all 123 topics**, not the
recommended 63 P0), recorded as
[ADR-0001](adr/0001-split-primitives-into-atomic-fundamentals.md). Then batch 1 written:
`interview-prep/fundamentals/` with five pages, ~250–280 lines each —
`consistency-models`, `transaction-isolation-levels`, `consensus-raft-paxos`,
`leases-locks-and-fencing`, `quorums-and-anti-entropy` — plus a folder README, manifest progress
section, and pointer banners on the primitive file being split.

### How

Each page was researched against 2–3 independent sources before assertion, and each carries a
**documented production incident** rather than a generic failure list:

| Page | Incident / primary finding |
|---|---|
| consistency-models | GitHub 2018-10-21 — 43 s partition, 24 h 11 m degradation; Orchestrator held quorum, async MySQL replication did not |
| transaction-isolation-levels | Jepsen PostgreSQL 12.3 — real G2-item under `SERIALIZABLE`; XID misattribution in conflict detection; present since SSI shipped in 2011, fixed Aug 2020 |
| consensus-raft-paxos | Raft single-server membership-change safety bug (2015); Roblox 2021 — 73 h outage from Consul streaming + BoltDB freelist pathology |
| leases-locks-and-fencing | Kleppmann vs antirez on Redlock; Chubby sequencers and `lock-delay`; GFS chunk leases + version numbers |
| quorums-and-anti-entropy | Tombstone resurrection when repair misses `gc_grace_seconds`; Cassandra Merkle depth 2^15 causing overstreaming; DynamoDB's move *away* from leaderless |

### Why these five first

They are the highest-value pages in the set and they exercise every part of the section contract —
so if the contract were wrong, it would show on batch 1 rather than batch 9. They also all split
from one source file, which meant the split mechanics got tested end to end immediately.

### Trade-offs and things worth knowing

- **`02-primitives/consistency-and-consensus.md` was kept, not deleted.** It still uniquely holds
  clocks and CRDTs (both P1, batches later). It now carries a banner naming its successor pages.
  The cost is a transitional period where two files discuss the same subject at different depths —
  accepted knowingly and recorded in ADR-0001.
- **Scope decision went against the written recommendation.** The manifest recommends stopping at
  63 P0 files; all 123 were chosen. Batch order still runs P0 first, so stopping early stays
  available at any batch boundary.
- **Found and fixed a real tooling trap.** `gen_backlinks.py` matches `## Referenced by` and
  `## Sources` **textually, including inside code fences** — it injected generated backlink lists
  into the section-contract examples in `CLAUDE.md` and `CONVENTIONS.md`. Both were converted from
  fenced snippets to tables, and the trap is now documented in each file. Second and third runs of
  the script report `0 changed`, so the pass is idempotent again.
- **Fixed 4 pre-existing links** in `main.md` that used raw spaces and backslashes
  (`basic\prep\SQL or NoSQL.md`). Percent-encoded with forward slashes — the files were **not**
  renamed, per the standing rule.
- **Known lint false positive:** `lint_docs.py --contract` reports "missing: Follow-up questions"
  for all five pages. The skill's generic contract names that section `Follow-up questions`; this
  repo's contract (CLAUDE.md) names it `Staff-level follow-ups`. Repo convention wins; expect this
  line on every future page.

### Verification

```
$ python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .
checked 1089 relative links; broken: 4          # the 4 {rel_path} placeholders, unchanged
$ python ~/.claude/skills/staff-technical-docs/scripts/gen_backlinks.py .   # run twice
187 files scanned, 519 inbound links mapped, 0 changed
```

Before this session the same check reported 501 links; the growth is the new pages plus the
regenerated backlink sections. No raw-space GitHub warnings remain.

---

## 2026-09-02 — Staff-level restructure groundwork + `staff-technical-docs` skill

Branch: `docs/staff-level-restructure` (not merged)

### What

Two threads, one feeding the other.

**1. Built the interview-prep curriculum, then rebuilt its plan for a staff audience.**
75 files under `interview-prep/` (~10,400 lines): playbook, numbers, 12 primitives, 26 worked
cases across backend/frontend/data/ML, drills, reference, company styles, resources. Then —
after feedback that it read as prep material rather than staff-level content — produced
`interview-prep/topics/manifest.md`: 123 canonical topics with aliases, tiers and split
provenance, plus `diagrams/components.md` (shared Mermaid vocabulary) and a rewritten `CLAUDE.md`
carrying the staff section contract and the ADR anti-patterns.

**2. Extracted the method into a reusable skill.** `~/.claude/skills/staff-technical-docs/` —
SKILL.md, three references, two asset packs, three verification scripts, an eval set. Benchmarked
against a no-skill baseline across 3 cases, 6 parallel runs.

### How

- Cloned 10 upstream reference repos into a gitignored `vendor/` (~100 MB) rather than committing
  other people's git history; a `fetch-references.sh` refreshes them.
- Mapped 243 local books to specific chapters per topic, so "read DDIA" became "read ch. 5–9".
- Wrote link-verification, backlink-generation and lint scripts, then bundled them into the skill
  because the same link checker had been written inline three times in one session.
- Ran the skill against a no-skill baseline: 3 evals × 2 configurations, 25 assertions, graded
  mechanically where possible and by evidence where not.

### Results

| | with skill | baseline |
|---|---|---|
| Assertion pass rate | 100% (25/25) | 76% (19/25) |
| Tokens | 2.1× baseline | — |
| Wall-clock | 2.3× baseline | — |

### Trade-offs found — the part worth keeping

**Bundled topic pages vs atomic pages.** The existing `02-primitives/` had 12 files each carrying
3–6 staff-depth topics; `consistency-and-consensus.md` alone covered CAP, isolation, Raft, leases,
clocks and CRDTs. A page covering six topics cannot go deep on any — they compete for the same
space. Depth is a *structural* fix (split into ~47 pages), not a "write more words" fix. This was
the single most valuable insight of the session and it generalises to any doc set that feels thin.

**Renaming vs percent-encoding a broken link.** The largest measured behavioural difference. The
baseline fixed links whose targets contained spaces and parens by *renaming the files* — for a
user whose stated problem was "I moved files around and links broke". Both configurations reached
zero broken links; only one avoided recreating the original problem. Encoding is local and
reversible; renaming is a migration wearing a tidy-up's clothes.

**Manifest-first vs write-first.** A manifest costs a review cycle before any prose exists. It
buys permanent duplicate prevention via an aliases column. Worth it above ~10 pages; overhead
below that.

**Completeness bar vs word count.** Word caps produce either padding or truncation. "Every section
carries something a principal engineer didn't already know" is unbounded but checkable, and it
lets case studies run long without licensing filler.

**Skill overhead is real.** 2.1× tokens. Justified on a multi-file set; on a single-page rewrite
the measured gains were mostly stylistic. The skill now says so and tells the reader to skip the
machinery for one-page jobs — a skill that doesn't know when to stand down gets switched off.

**Semantic duplicates cannot be scripted.** `lint_docs.py` catches `caching.md` vs
`cache-strategies.md` and is structurally blind to `rate-limiting.md` vs `throttling.md`. It was
printing "no duplicate topics" over a vault containing exactly that. A clean report that
overstates its scope is worse than no report; the script now states what it did not check.

**Verify the verifier.** `gen_backlinks.py` had a Windows path-separator bug: it printed
"262 links mapped, 0 changed" and exited 0 while writing nothing — indistinguishable from success.
I ran it on this repo and read that as working. An eval agent caught it. Scripts that report
success by default are worse than scripts that crash.

**You cannot credibly grade your own skill.** I wrote both the skill and the assertions that
scored it; assertions derived from the skill's own section contract structurally favour it. The
100% is a ceiling artefact, not a triumph. 11 of 25 assertions passed in *both* configurations and
measured nothing. v2 of the eval set drops them and adds harder ones.

**Eval prompts leak instructions.** Eval-0's prompt said "figure out the topic list before you
start writing" — handing the baseline the skill's central mechanism. The baseline still lost, but
the comparison was unfair in my favour. Fixed in v2.

### Verification

```
relative links across repo:  478 checked, 4 broken (all template placeholders in
                             markdown files/md_blacklinks.md — pre-existing, not real links)
frontmatter:                 all 77 interview-prep files complete
longest file:                244 lines (ceiling 500)
scripts:                     compile clean; gen_backlinks regression-tested across
                             forward-slash, backslash and relative roots
```

Also fixed two pre-existing bugs found in passing: 5 links broken by unescaped parentheses in
`INDEX.md` and 3 case files, and 2 image links in `how we've scaled Dropbox.md` pointing at moved
assets.

### Skill iteration, after the benchmark

Every change below traces to something the runs surfaced, not to a hunch:

| Change | Triggered by |
|---|---|
| `gen_backlinks.py` path canonicalisation | Silent no-op on Windows; regression-tested across forward-slash, backslash and relative roots |
| `lint_docs.py` now prints what it did **not** check | It was reporting "no duplicate topics" over a vault that had one |
| New **"Fix the link, not the filename"** section, promoted out of a bullet | The largest measured behavioural difference between configurations |
| New **"When not to use this"** | 2.1× token cost; on a single page the gains were mostly stylistic. A skill that can't stand down gets switched off |
| Manifest section: semantic duplicates can't be scripted | The eval-2 trap didn't trap — both configs caught it by reading, neither by tooling |
| Eval set v2 | Removed the prompt leak, dropped 11 non-discriminating assertions, added harder ones plus a set-level eval |

Iteration-1 caveats are recorded inside `evals/evals.json` rather than in a message, including
that the skill's author also wrote its assertions.

### Open

`D1–D4` in `interview-prep/topics/manifest.md` §7 — the structural decisions (rename
`02-primitives/` → `fundamentals/` and split; add `patterns/` and `comparisons/`; P0-only scope;
rewrite cases in place). Recommendations are recorded; none executed. Writing the 63 P0 pages is
the next substantial block of work and needs a scope decision first.

Also open: no PR; eval v2 written but never run; eval-3's fixture unbuilt; and **no human has
reviewed the iteration-1 outputs** — the skill was graded by its author against that author's
assertions, which is the weakest evidence produced this session.

### See also

- [NEXT-SESSION.md](NEXT-SESSION.md) — the handoff: blocking decision, first commands, batch 1
- [sessions/2026-09-02-staff-restructure-and-skill.md](sessions/2026-09-02-staff-restructure-and-skill.md) — the full narrative, including what went wrong
- [../STATUS.md](../STATUS.md) — stop point and traps

## Referenced by

- [ADR-0001: Split bundled primitives into atomic fundamentals pages](adr/0001-split-primitives-into-atomic-fundamentals.md)
- [CLAUDE.md — system-design-prep](../CLAUDE.md)
- [Docs index](README.md)
- [Repo index](../INDEX.md)
- [Session record — fundamentals batches 1–5](sessions/2026-09-02-fundamentals-batches-1-5.md)
- [STATUS](../STATUS.md)
