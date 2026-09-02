---
title: Design a feature store
type: case
track: ml
difficulty: advanced
status: drafted
sources: [Designing ML Systems, Feast/Tecton docs, Uber Michelangelo]
updated: 2026-09-02
tags: [feature-store, point-in-time, skew, online-offline]
---

# Design a feature store

> One place to define features once and get them **both** in training (historical, correct as of
> a past moment) and in serving (fresh, in milliseconds).
> **The hard part:** point-in-time correctness and online/offline parity. Everything else is
> plumbing.

## 1. Clarify

| Question | Assumed answer |
|---|---|
| Who uses it? | 30 ML teams, ~50 models in production |
| Feature count? | ~2,000 features across ~100 entities |
| Serving latency? | p99 < 20 ms for a batch of 200 entities |
| Freshness tiers? | Batch (daily), streaming (seconds), on-demand (request-time) |
| Backfill? | Yes — a new feature must be computable over 2 years of history |

**Non-goals:** the models themselves, experiment tracking, the training orchestrator.

## 2. Requirements

**Functional**
- Define a feature once (transformation + entity + freshness) and serve both paths from it
- **Point-in-time-correct** historical retrieval for training sets
- Low-latency online retrieval by entity key, batched
- Feature discovery, ownership, lineage and versioning
- Monitoring: drift, null rate, freshness, and **online/offline value parity**

**Non-functional**

| Target | Value |
|---|---|
| Online p99 | < 20 ms for 200 entities × 50 features |
| Online availability | 99.99% — it's on every model's critical path |
| Offline correctness | Zero future leakage, provable |
| Freshness | Streaming features < 10 s; batch by SLA |

## 3. Estimates

```
Online store: 100M entities × 50 features × 20 B = 100 GB, hot subset in RAM
   QPS: 50 models × 5k rps × 1 batched call = 250k feature-fetch calls/s
        each returning 200 × 50 = 10k values → ~10 M values/s          ← columnar or bust
Offline store: 2,000 features × 100M entities × 2 years of daily snapshots
   = huge. Store as event-time rows in Iceberg, not snapshots per day.
Backfill: recomputing one feature over 2 years ≈ hours of Spark. Must be routine, not a project.
```

> [!info] The scary number
> 10M feature values per second on the online path. That forces batched, columnar reads and a
> memory-resident hot set — not per-feature KV round trips.

## 4. API / contract

**Definition** (the artefact that makes parity possible — one definition, two runtimes):

```python
@feature_view(
    entities=["user_id"],
    source=stream("transactions"),
    mode="streaming",
    ttl="7d",
    owner="team-risk",
)
def user_txn_velocity(txns):
    return {
        "txn_count_1h":  count(txns, window="1h"),
        "txn_amount_24h": sum_(txns.amount, window="24h"),
    }
```

**Serving:**
```python
# online — serving
store.get_online_features(
    features=["user_txn_velocity:txn_count_1h", "user_profile:tenure_days"],
    entity_rows=[{"user_id": u} for u in batch],      # batched, one round trip
)

# offline — training, point-in-time correct
store.get_historical_features(
    entity_df=labels_df,        # MUST include an event_timestamp column
    features=[...],
)
```

## 5. Data model

| Layer | Store | Content |
|---|---|---|
| Registry | Postgres / Git | Feature definitions, entities, owners, versions, lineage |
| **Offline** | Iceberg on object storage | `(entity_id, event_timestamp, feature values…)` — append-only |
| **Online** | Redis / DynamoDB / Scylla | `entity_id → latest feature values`, TTL'd |
| Streaming | Kafka + Flink | Windowed aggregations feeding the online store |
| Monitoring | Time-series | Distributions, nulls, freshness, parity samples |

**The offline table stores event-time rows, not daily snapshots.** Snapshots are what break
point-in-time correctness — with a snapshot you can only ask "what was true at midnight", and
your training rows are at arbitrary timestamps.

## 6. Architecture

```
definitions (versioned, in Git, reviewed) ──compile──┐
                                                     ├→ batch job (Spark)  → offline store
                                                     └→ streaming job (Flink) → online store
                                                                              └→ offline store
                                                                                 (for training)
training:  labels + event timestamps → point-in-time join over the offline store → training set
serving:   model → get_online_features(batch) → features → prediction
                                              └→ log served values → parity monitor
```

The single compiled definition is the whole point: two code paths written by hand *will* diverge,
and the divergence is invisible until model quality quietly drops.

### Deep dive A — point-in-time correctness (the core of the case)

You have a label event at time `T`. The training row must contain feature values **as they were
just before T**, never later.

```
Naive (WRONG):  JOIN features ON entity_id                 → uses today's values. Leakage.
Correct:        AS-OF JOIN on (entity_id, event_timestamp) → last value with
                feature_ts <= label_ts, respecting TTL
```

Two subtleties worth raising unprompted:

1. **Feature availability lag.** A feature computed by a job that finishes at 02:00 was *not*
   available to a 01:30 prediction, even though its `event_timestamp` is 01:00. Model the
   *availability* time as well as the event time, or you leak.
2. **TTL.** A value from 30 days ago probably shouldn't be joined onto today's label — expiry is
   part of the definition, and it must be applied identically in both paths.

> [!tip] Interview line
> "Point-in-time joins are an as-of join on entity plus timestamp, respecting both TTL and the
> feature's availability lag. Getting this wrong is the single most common cause of a model that
> looks excellent offline and mediocre in production."

### Deep dive B — online/offline parity

Even with one definition, values can diverge: different execution engines, floating-point
differences, late data, or a streaming job that fell behind.

**How you'd actually detect it** (this is the answer that separates people who've operated one):

- **Log the served feature vector** on a sample of requests (say 1%).
- Recompute those same features offline for the same entities and timestamps.
- Alert on distributional divergence and on per-feature mismatch rate.

That parity monitor is more valuable than any amount of pipeline code review.

### Deep dive C — the three freshness modes

| Mode | Path | Example | Cost |
|---|---|---|---|
| **Batch** | Spark → online store | 30-day spend, lifetime orders | Cheap; stale by up to a day |
| **Streaming** | Flink → online store | Clicks in the last 5 minutes | Medium; seconds fresh |
| **On-demand** | Computed at request time from request payload + fetched values | `amount / avg_amount_30d`, distance between request IP and home | Free to store; must be defined once so training reproduces it exactly |

On-demand features are where skew loves to hide — they're often written twice (once in the
serving app, once in the training notebook). The definition must own them too.

### Deep dive D — governance at 30 teams

- **Ownership** per feature view, with an on-call. Unowned features get deprecated.
- **Versioning**: changing a feature's logic creates `v2`; models pin a version. Silently
  changing a feature under a live model is a production incident.
- **Discovery**: search by entity, owner, freshness, and *usage* — the feature catalogue is only
  useful if people can find what already exists instead of writing their own copy.
- **Cost attribution** per feature view: some features are enormously expensive and used by one
  model that no longer ships.

## 7. Scale & failure

| Breaks first at 10x | Fix |
|---|---|
| Online store QPS/memory | Shard by entity hash, tier cold entities, compress (int8/fp16) |
| Point-in-time join runtime | Partition + sort offline tables by (entity, time), incremental training sets |
| Streaming job state | TTLs, key sharding, coarser windows |
| Registry contention / sprawl | Feature deprecation policy driven by usage metrics |

| Component fails | Blast radius | Degraded behaviour |
|---|---|---|
| Online store down | **Every model degrades at once** — the shared-fate risk of a feature store | Per-model default/imputed values + local cache; models must have a no-feature fallback |
| Streaming job lags | Stale fresh-tier features | Serve stale with an age flag; alert on feature age, not just job health |
| Batch job fails | Yesterday's values persist | Serve last-known-good; alert on staleness against the feature's declared SLA |
| Bad feature definition shipped | Silent quality drop across models | Parity + drift monitors, staged rollout of definition changes, version pinning |

## 8. Ops & cost

- **SLO:** online p99 < 20 ms, 99.99% availability, freshness per declared tier, parity mismatch
  rate < 0.1%.
- **Alert on:** per-feature null/default rate, feature age vs SLA, parity divergence, online store
  latency and hit rate, streaming lag, definition-deploy failures.
- **Rollout:** definition changes are code — reviewed, versioned, canaried against parity checks
  before models consume them.
- **Cost:** online store memory and streaming compute dominate. The biggest lever is **deleting
  unused features** — usage tracking typically reveals a large fraction of features feed nothing.
- **First thing I'd cut:** unused feature views, and the freshness tier of features whose models
  don't actually need seconds.

## Sources & further reading

- Local book: `DE/Warehouse-ETL/Designing machine learning systems — Chip Huyen.pdf` — features and skew
- [Uber — Michelangelo ML platform](https://www.uber.com/blog/michelangelo-machine-learning-platform/)
- [Feast — feature store docs](https://docs.feast.dev/)
- Related: [ml-playbook.md](ml-playbook.md), [../05-data-cases/data-playbook.md](../05-data-cases/data-playbook.md)
