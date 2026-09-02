---
title: Design feed ranking (engagement prediction)
type: case
track: ml
difficulty: advanced
status: drafted
sources: [Meta/Twitter ranking systems, Designing ML Systems]
updated: 2026-09-02
tags: [ranking, multi-task, real-time-features, calibration]
---

# Design feed ranking

> The ML half of [../03-backend-cases/news-feed.md](../03-backend-cases/news-feed.md): given a few
> hundred candidate posts, order them.
> **The hard part:** real-time features (a post minutes old with no engagement history), multi-
> objective optimisation, and doing it in ~50 ms.

## 1. Clarify

| Question | Assumed answer |
|---|---|
| Optimise for what? | A weighted combination of meaningful interactions, not raw clicks |
| Candidate set size? | ~500 per request after retrieval |
| Latency for ranking? | 50 ms of a 200 ms page budget |
| Feature freshness? | Post-level engagement counters within seconds |
| Do we control retrieval? | Yes, but it's a separate stage (see the backend case) |

**Non-goals:** fanout/storage, ads auction, integrity/moderation models (mentioned as a filter).

## 2. Requirements

**Functional**
- Score ~500 candidates and return an ordered list
- Multi-objective: predict several engagement types, combine into one value score
- Apply diversity, freshness, integrity and "already seen" constraints after scoring

**Non-functional**

| Target | Value |
|---|---|
| Ranking p99 | < 50 ms for 500 candidates |
| Throughput | 150k rps peak (from the backend case) |
| Feature freshness | Post counters < 10 s; user features < 5 min |
| Availability | 99.99% — **must** degrade to chronological |

## 3. Estimates

```
150k rps × 500 candidates = 75M item-scorings/second      ← the number that shapes everything
   A 1 ms/item model is 75,000 cores. So: batch all 500 in one forward pass,
   keep the model small, and push heavy computation offline into embeddings.
Features: 500 candidates × 150 features = 75k values per request, batched fetch ~10 ms
Model: ~10 ms for 500 items batched on CPU (small NN / GBDT) or a shared GPU tier
Training: 1B impressions/day, downsampled to ~100M rows for daily retraining
```

> [!info] The scary number
> **75M scorings/second.** Everything in this design — embedding precomputation, batching,
> model size, candidate cap — exists to make that arithmetic work.

## 4. API / contract

```
rank(user_id, candidates[500], context) → [(post_id, score, per_head_scores)]

Logged per impression:
  request_id, model_version, user_id, post_id, position, per_head_predictions,
  feature_snapshot_ref, and the eventual outcomes (click, dwell_ms, like, share, hide, report)
```

Logging the **feature values actually served** (or a reference to them) is what makes
training–serving skew detectable and gives you unbiased training data. Say it.

## 5. Data model

**Features, by freshness tier:**

| Tier | Examples | Where |
|---|---|---|
| Static | Author ID, media type, language | In the candidate payload |
| Daily | User's long-term topic affinity embedding, author quality | Batch → online KV store |
| Minutes | User's session activity, recent topics | Streaming aggregation |
| **Seconds** | This post's likes/comments/hides in the last 10 min, velocity | **Streaming counters — the hardest tier** |

The seconds tier is the interesting one: a post that is 3 minutes old has almost no history, so
early engagement velocity is the strongest signal you have, and it must reach the ranker in
seconds. That means a streaming aggregation path (Kafka → Flink → online store), not a batch job.

**Labels:** multi-headed and each with its own delay — click (instant), dwell (seconds), like
(minutes), hide/report (rare, valuable), long-term retention (weeks, unusable as a direct label).
Negatives are impressions without engagement, corrected for position and viewport.

## 6. Architecture

```
candidates (500) ─┐
user features ────┼→ batched feature assembly (one columnar fetch, not 500 lookups)
post features ────┘
                  → ranking model (multi-task): p(click), p(like), p(share), p(hide), E[dwell]
                  → value = Σ wᵢ · pᵢ         (weights set by the product, not by the model)
                  → re-rank: diversity, author cap, freshness boost, integrity demotion
                  → top N + logging
```

### Deep dive A — multi-task scoring

One model, several heads sharing a trunk. Buys: shared representation, one forward pass, and
better estimates for rare events (hide/report) via shared learning.

The combination is where product and ML meet:

```
value = w_click·p(click) + w_dwell·E[dwell] + w_share·p(share) − w_hide·p(hide) − …
```

Say clearly: **the weights are a product decision**, tuned by A/B test, not learned end-to-end —
because the thing you actually care about (long-term retention) is unobservable at ranking time.
Negative weights on hide/report are what stop the system optimising into engagement bait, and
volunteering that is the strongest signal you can give in this case.

**Calibration** matters because the heads are combined: p(click) must mean an actual probability
or the weighted sum is meaningless. Use Platt scaling / isotonic regression, and monitor
calibration drift, not just AUC.

### Deep dive B — real-time features without a stampede

- Streaming counters per post keyed `post:{id}:{window}` with time-decayed windows (1 min, 10 min,
  1 h) maintained in Flink and written to the online store.
- **Hot posts are hot keys** — a viral post is read by millions of ranking requests per minute.
  Cache it locally in each ranker process with a 1–5 s TTL; the staleness is irrelevant at that
  timescale and it removes the hotspot entirely.
- **Cold-start posts**: no engagement history, so lean on author features, content embeddings,
  and an exploration boost. Without a deliberate boost, new posts never get impressions and never
  accumulate the signal they need — a self-fulfilling ranking failure worth naming.

### Deep dive C — making 50 ms work

| Technique | Saving |
|---|---|
| Precompute item and user embeddings offline; the ranker consumes vectors, not raw text | Huge |
| One batched forward pass over 500 items, not 500 calls | 10–50x |
| Feature fetch as a single multi-get, columnar, in one round trip | ~40 ms → ~10 ms |
| Quantised model / distilled student | 2–4x |
| Early exit: cheap model prunes 500 → 150, expensive model ranks the rest | 2–3x |
| Cap candidates by budget: adaptive N under load | Graceful degradation |

### Deep dive D — the feedback loop

The ranker decides what gets seen, which decides what gets trained on. Mitigations:
log propensities, reserve a small random-exposure slice for unbiased evaluation, and keep a
**chronological holdback** cohort — it's the only honest baseline for "is ranking actually
helping?" and it answers a question interviewers love to ask.

## 7. Scale & failure

| Breaks first at 10x | Fix |
|---|---|
| Model compute | Distillation, early exit, fewer candidates, GPU batching tier |
| Feature fetch volume | Local caches, embedding compression, fewer features (measure importance) |
| Streaming counter volume | Sampling for low-engagement posts, coarser windows |
| Training data volume | Downsample negatives, incremental training |

| Component fails | Blast radius | Degraded behaviour |
|---|---|---|
| Ranker down | No personalised order | **Chronological feed** — worse, still a product |
| Real-time features stale | Slightly worse ranking | Serve with older windows; alert on feature age |
| One head misbehaving after a deploy | Skewed value scores | Per-head monitoring + automatic rollback on guardrail breach |
| Feature nulls spike | Silent quality collapse | Alert on default rate per feature — **the most important ML alert there is** |

## 8. Ops & cost

- **SLO:** ranking p99 < 50 ms; feature default rate < 0.5%; no guardrail metric regressed.
- **Alert on:** per-head prediction distributions, calibration error, feature null rates, feature
  age, per-segment CTR/hide rate, model-version split.
- **Rollout:** offline (NDCG + per-head AUC, sliced by segment) → shadow → 1% → 5% → 50% with
  guardrails (hide rate, report rate, session length, next-day return). Automatic rollback.
- **Cost:** ranking compute dominates, then the feature store. Distillation and candidate caps
  are the biggest levers. Quote a $/1k-requests figure.
- **First thing I'd cut:** candidate count and the number of features (feature importance is
  extremely long-tailed — half of them usually earn nothing).

## Sources & further reading

- Vendor: `10-resources/vendor/applied-ml/README.md` — ranking/feed case studies
- [Meta engineering — how the feed is ranked](https://engineering.fb.com/)
- Local book: `DE/Warehouse-ETL/Designing machine learning systems — Chip Huyen.pdf` — ch. on features and monitoring
- Backend counterpart: [../03-backend-cases/news-feed.md](../03-backend-cases/news-feed.md)
