---
title: Design a recommender system
type: case
track: ml
difficulty: core
status: drafted
sources: [Designing ML Systems, Netflix/YouTube papers]
updated: 2026-09-02
tags: [recsys, two-tower, ann, ranking, cold-start]
---

# Design a recommender system

> "Recommended for you" on a catalogue of 100M items for 200M users.
> **The hard part:** you cannot score 100M items in 100 ms, so the whole design is
> **candidate generation → ranking**, plus cold start and the feedback loop that biases your
> training data.

## 1. Clarify

| Question | Assumed answer |
|---|---|
| What are we recommending, and where? | Homepage rows + "more like this" on an item page |
| Business metric? | Long-term engagement (watch time / repeat visits), not raw CTR |
| Catalogue size / user base? | 100M items, 200M users, 20M DAU |
| Latency? | p99 < 200 ms for the homepage |
| Freshness? | New items discoverable within an hour; user actions reflected within minutes |
| Personalisation depth? | Yes, plus context (device, time of day, session) |

**Non-goals:** the content ingestion pipeline, ads, pricing.

## 2. Requirements

**Functional**
- Return a ranked, deduplicated, diverse list of N items per user per surface
- Handle new users and new items (cold start)
- Support "because you watched X" explanations

**Non-functional**

| Target | Value |
|---|---|
| p99 latency | < 200 ms end to end |
| Throughput | 20M DAU × 20 requests/day ≈ 5k rps, 15k peak |
| Freshness | User signal < 5 min; new item < 1 h |
| Availability | 99.9% — degrade to popularity, never fail the page |

**Guardrails:** diversity (not 10 near-identical items), freshness (not all catalogue classics),
and a hard rule that engagement optimisation must not tank long-term retention.

## 3. Estimates

```
Scoring cost: 15k rps × 100M items = impossible. Two-stage is not optional.
   Candidate generation: 100M → ~1,000 via ANN + heuristics    ~10 ms
   Ranking: 1,000 items × ~200 features, GBDT/small NN         ~50 ms
Embeddings: 100M items × 128 dims × 4 B = 51 GB (fp32) → 13 GB at int8   ← fits in RAM
   200M user embeddings × 128 × 4 B = 102 GB → sharded, or computed at request time
Feature fetch: 1,000 items × 200 features = 200k values per request
   → must be a batched, columnar lookup, not 1,000 KV round trips           ← the real risk
Training data: 20M DAU × 50 impressions = 1B rows/day. Sample negatives.
```

> [!info] The scary number
> Feature fetch for 1,000 candidates inside a 50 ms slice. This, not model accuracy, is what
> makes or breaks the latency budget — and it's the part most candidates forget.

## 4. API / contract

```http
GET /v1/recommendations?surface=home&user_id=&context={device,locale}&limit=20
  → 200 { items: [{item_id, score, reason: "because you watched X", debug_id}], model_version }

POST /v1/feedback  { user_id, item_id, event: "impression"|"click"|"complete"|"dismiss", ts, request_id }
```

**`request_id` on both sides** ties impressions to the exact model version, candidate set and
feature values used — without it you cannot debug ranking or train unbiased models.

## 5. Data model

| Store | Content | Why |
|---|---|---|
| Vector index (ANN) | 100M item embeddings | Candidate generation by similarity |
| Online feature store (KV) | User features, item features, counters | Ranking-time lookup, < 10 ms batched |
| Offline feature store (lakehouse) | Point-in-time-correct historical features | Training without leakage |
| Interaction log | Every impression + outcome + context + request_id | Training labels and offline eval |
| Model registry | Versioned models + metadata + eval results | Rollout and rollback |

**Labels:** implicit and biased. A click is positive; a non-click on something shown is a
"negative" only if it was actually seen (log viewport/position). Correct for **position bias** —
item 1 gets clicked because it's item 1 — with position as a training feature that's set to a
constant at inference, or with inverse-propensity weighting.

## 6. Architecture

```
OFFLINE (daily/hourly)
interactions → feature pipelines → training data (point-in-time joins)
             → two-tower model training → item embeddings → ANN index build
             → ranker training (GBDT / DNN) → model registry → shadow eval

ONLINE (per request)
request → user features (online store)
        → candidate generation (parallel sources):
             ANN over user embedding      (personalised)
             co-visitation / item-to-item (session-based)
             trending / popular by segment (cold start + coverage)
             editorial / business rules
        → merge + dedup + filter (already seen, unavailable, blocked)  → ~1,000
        → batched feature fetch for candidates
        → ranking model → scores
        → re-rank: diversity (MMR), freshness, business constraints
        → top 20 + reasons → response + impression log
```

### Deep dive A — candidate generation

| Source | Mechanism | Covers |
|---|---|---|
| **Two-tower embeddings** | User tower and item tower trained to place engaged pairs close; serve with ANN (HNSW/IVF-PQ) | The personalised bulk |
| **Item-to-item co-visitation** | "Users who watched X also watched Y", precomputed | Session context, new users |
| **Trending / popular** | Time-decayed counts per segment | Cold start, coverage, fallback |
| **Rules / editorial** | Curated rows, new releases | Business needs, launch content |

**Two-tower is the workhorse and worth explaining precisely:** the item tower runs offline (embed
the whole catalogue nightly, incrementally for new items), and only the *user* tower runs at
request time — one small forward pass, then an ANN lookup. That asymmetry is what makes
100M-item retrieval feasible at 10 ms.

**ANN trade-offs to name:** HNSW gives excellent recall/latency at high memory; IVF-PQ compresses
hard (int8/PQ) at some recall cost. Say you'd measure **recall@k against exact search** — an ANN
index silently losing 20% recall is a common, invisible failure.

### Deep dive B — ranking

- Features: user (history, demographics, long-term preference embeddings), item (metadata,
  quality, age, popularity), **user×item interaction** (has the user watched this genre, past
  engagement with this creator), and context (device, hour, session position).
- Model: **GBDT is a strong default** for tabular; a DNN wins when you need embeddings and
  multi-task heads. **Multi-task** matters: predict click *and* completion *and* long-term value,
  then combine — optimising click alone produces clickbait, which is exactly the guardrail
  failure the interviewer wants you to anticipate.
- Calibration matters if scores are combined with business values (expected revenue = p(click) ×
  value). Uncalibrated scores make blending meaningless.

### Deep dive C — cold start

| Cold | Approach |
|---|---|
| **New user** | Popularity by inferred segment (locale, device, referrer), onboarding preference picker, fast adaptation within the first session using in-session signals |
| **New item** | Content-based embedding from metadata/text/image (no interaction data needed), plus **deliberate exploration** — give new items forced impressions and measure |
| **New user + new item** | Content features on both sides; two-tower handles this naturally if towers use content features, not just IDs |

**Exploration is a design requirement, not a nicety:** without it you only ever learn about items
you already show, and the catalogue's tail stays permanently invisible. Epsilon-greedy or
Thompson sampling on a small traffic slice, with logged propensities so you can train unbiased
models later.

### Deep dive D — diversity and the feedback loop

- **MMR / determinantal-style re-ranking**: trade relevance against dissimilarity so the list
  isn't ten variations of one thing.
- **Filter bubbles / popularity bias**: popular items get shown, get more interactions, get more
  popular. Counter with exploration, popularity-debiased training (down-weight by exposure), and
  diversity constraints in the re-rank.

## 7. Scale & failure

| Breaks first at 10x | Fix |
|---|---|
| Feature fetch for candidates | Fewer candidates, feature caching, colocated feature service, int8 features |
| ANN index memory | Quantisation (PQ/int8), sharded index, tiered by item popularity |
| Ranking latency | Smaller model, distillation, early-exit, fewer candidates |
| Training data volume | Negative sampling, downsampling impressions, incremental training |

| Component fails | Blast radius | Degraded behaviour |
|---|---|---|
| Ranking service | No personalisation | **Serve candidate order / popularity** — always have this path |
| Feature store slow | Ranking degrades | Serve with default/imputed features, and **alert on the default rate** — silent feature nulls are the classic invisible quality regression |
| ANN index stale | Missing new items | Fall back to co-visitation + trending; alert on index age |
| Model registry deploy bad model | Quality drop across the product | Canary + automatic rollback on guardrail metrics |

## 8. Ops & cost

- **SLO:** p99 < 200 ms; recommendation availability 99.9%; feature default rate < 1%.
- **Alert on:** prediction score distribution shift, feature null/default rates, ANN recall
  proxy, CTR by segment, index freshness, model-version traffic split.
- **Rollout:** offline eval (NDCG/recall on a time-split set, sliced by segment) → shadow →
  1% A/B with guardrails → ramp. Keep a **permanent holdback** on the old model so you can
  measure long-run effects that A/B tests miss.
- **Cost:** ranking compute and the feature store dominate; the ANN index is memory-heavy but
  cheap per query. Levers: candidate count, model size, caching recommendations for low-activity
  users, precomputing the head and computing the tail live.
- **First thing I'd cut:** candidate count (1,000 → 400) and recomputation frequency for
  inactive users.

## Referenced by

- [Design video streaming (YouTube / Netflix)](../03-backend-cases/video-streaming.md)
- [ML and GenAI cases index](README.md)
- [Question bank](../07-drills/question-bank.md)
- [Repo index](../../INDEX.md)

## Sources & further reading

- Local book: `DE/Warehouse-ETL/Designing machine learning systems — Chip Huyen.pdf`
- Vendor: `10-resources/vendor/applied-ml/README.md` — recommendation case studies from real companies
- [YouTube — Deep Neural Networks for YouTube Recommendations](https://research.google/pubs/pub45530/)
- [Netflix Tech Blog — recommendations](https://netflixtechblog.com/)
- Related: [feed-ranking.md](feed-ranking.md), [feature-store.md](feature-store.md)
