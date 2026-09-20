---
title: ML system design playbook
type: playbook
track: ml
difficulty: core
status: drafted
sources: [Designing ML Systems (Huyen), AI Engineering (Huyen), Exponent 2026 guide]
updated: 2026-09-02
tags: [playbook, ml, framework]
---

# ML system design playbook

## The clock (45–60 min)

| Minutes | Step | Output |
|---|---|---|
| 0–6 | **Frame** | Business goal → ML task → offline + online metrics → constraints |
| 6–12 | **Data** | Sources, labels, volume, leakage risks, privacy |
| 12–20 | **Features + model** | Feature list, baseline, candidate gen → ranking architecture |
| 20–28 | **Serving** | Latency budget breakdown, batching, caching, fallback |
| 28–40 | **Deep dive** | The hard part — usually features or eval |
| 40–50 | **Evaluate, monitor, iterate** | Offline eval, A/B design, drift, retraining |
| 50+ | **Cost + wrap** | $/prediction, biggest lever, what I'd cut |

Budget ~8 minutes per step and save 5 to wrap. Say the plan out loud at minute 5.

## 1. Frame — the step candidates rush and interviewers score hardest

Three questions before any modelling:

| Question | Why |
|---|---|
| **What business metric moves?** | Revenue, retention, fraud loss, support deflection. The model exists to move *this* |
| **What is the ML task?** | Binary classification? Ranking? Retrieval? Generation? Regression? Reframing a problem well is half the interview |
| **What is the prediction latency and volume?** | Batch overnight vs 50 ms online is a completely different system |

Then the metrics, in two columns — and **say both**:

| Offline (what you optimise) | Online (what you ship on) |
|---|---|
| AUC, log loss, NDCG@k, recall@k, MAE | CTR, conversion, watch time, fraud $ prevented, deflection rate |
| Cheap, fast, reproducible | Slow, noisy, but it's what actually matters |

**Also name a guardrail metric** — the thing that must not get worse (latency p99, diversity,
complaint rate, false-positive rate on a protected segment). Recommenders that maximise CTR
alone reliably degrade the product; saying so is a senior signal.

> [!warning] Trap
> Answering "we'd optimise accuracy". On a 0.1%-positive fraud problem, a model predicting
> "never fraud" is 99.9% accurate. Use precision/recall at a fixed operating point, PR-AUC, or
> a cost-weighted metric — and say *why*.

## 2. Data and labels

- **Where do labels come from?** Explicit (ratings, reports), implicit (clicks, dwell — biased),
  delayed (chargebacks arrive 60 days later), or weak/LLM-generated.
- **Delayed labels are a real design constraint**: you cannot train on last week's fraud because
  you don't know yet. Say how you'd handle the label-maturity window.
- **Leakage** is the #1 way ML systems look great offline and fail live: a feature computed
  *after* the label event, or a target-encoded field, or a train/test split that isn't
  time-based. **Always split by time for anything temporal.**
- **Class imbalance**: don't just oversample — set the threshold from the business cost of the
  two error types.
- **Privacy**: PII handling, consent, deletion propagating into training sets, and per-region
  training data. See [../02-primitives/security-and-multitenancy.md](../02-primitives/security-and-multitenancy.md).
- **Feedback loops**: the model's own outputs shape tomorrow's training data (you only observe
  clicks on items you showed). Mitigate with exploration (epsilon-greedy, bandits) and
  logging propensities.

## 3. Features

The dominant cause of production ML failure is **training–serving skew**: the feature computed
in training differs from the one computed at serving.

Fixes to name: one definition compiled to both paths (a feature store), logging the *served*
feature values and training on those, and **point-in-time correct** joins so training never
sees a value that wasn't available at prediction time. See
[feature-store.md](feature-store.md).

| Feature freshness | Serving pattern |
|---|---|
| Static (user's country) | Cached, refreshed daily |
| Slow (30-day spend) | Batch job, loaded into a KV store |
| Fast (clicks in the last 5 min) | Streaming aggregation into the online store |
| Real-time (this request's context) | Computed inline |

## 4. Model

- **Start with a baseline and say so**: popularity ranking, logistic regression, gradient-boosted
  trees. Many production systems never beat a well-tuned GBDT on tabular data, and proposing a
  transformer for a 50k-row tabular problem is a negative signal.
- **The two-stage pattern** is the answer to nearly every large-scale ranking problem:
  1. **Candidate generation** — cheap, high recall, millions → hundreds (ANN over embeddings,
     co-occurrence, popularity, rules).
  2. **Ranking** — expensive, high precision, hundreds → ordered list (GBDT or a neural ranker
     over rich features).
  3. **Re-rank / business rules** — diversity, freshness, dedup, policy, ads blending.
- Say the **model size vs latency** trade: distillation, quantisation, feature pruning.

## 5. Serving

- **Break the latency budget down out loud**: 200 ms total = 20 ms network + 30 ms feature fetch
  + 15 ms candidate gen + 60 ms ranking + 20 ms hydration + slack. If it doesn't add up, cut
  candidates or shrink the model — that arithmetic *is* the design.
- **Batch vs online vs streaming**: precompute recommendations nightly for cheap, compute
  on-demand for fresh, or hybrid (precompute candidates, rank live).
- **Cache** predictions where the input is stable; cache features aggressively.
- **Fallback is mandatory**: model service down/slow → serve popularity or last-known-good.
  A design where the ML failure takes down the product is an incorrect design.
- **Shadow mode** first: run the new model on live traffic without serving its output, compare.

## 6. Evaluate, monitor, iterate

**The 2026 emphasis.** Cover all four:

| Layer | What |
|---|---|
| **Offline eval** | Held-out set split by time; slice metrics by segment (new users, mobile, each region) — an aggregate win hiding a segment regression is the classic failure |
| **Online eval** | A/B test with sample-size math, guardrail metrics, and a **holdback** group kept on the old model for long-run comparison |
| **Monitoring** | Prediction distribution, feature distribution (drift), null/default rate per feature, latency, and **delayed-label metrics** once labels arrive |
| **Retraining** | Cadence (scheduled vs drift-triggered), reproducible pipeline, model registry with versions, rollback path |

**Drift vocabulary:** *data drift* (input distribution moved), *concept drift* (the relationship
between input and label moved), *training–serving skew* (a bug, not drift). Say which you'd
alert on and what the alert's action is.

## 7. Cost

- **$/prediction** or **$/1k requests**, and the dominant term.
- Levers: batching, smaller/distilled models, quantisation, caching, precomputing for the head
  and computing on demand for the tail, GPU utilisation, spot instances for training.
- For GenAI: tokens dominate — see [llm-serving-platform.md](llm-serving-platform.md) and
  [../02-primitives/cost-engineering.md](../02-primitives/cost-engineering.md).

## Questions to ask in the first five minutes

1. What business metric are we moving, and what's the current baseline?
2. Real-time or batch? What's the latency budget at p99?
3. Where do labels come from, and how delayed are they?
4. Scale: users, items, requests/second, feature count?
5. What's the cost of a false positive vs a false negative?
6. Is there an existing system, and what's wrong with it? (This question alone often reveals
   the whole intended answer.)

## Referenced by

- [8-week study plan](../07-drills/8-week-plan.md)
- [Books already on this machine](../10-resources/books-on-this-machine.md)
- [Design a feature store](feature-store.md)
- [Interview playbook](../00-interview-playbook.md)
- [ML and GenAI cases index](README.md)

## Sources & further reading

- Local book: `DE/Warehouse-ETL/Designing machine learning systems — Chip Huyen.pdf` — **the single
  best book for this round**
- Local book: `AI/LLM-Apps/AI Engineering — Chip Huyen (2025).pdf` — the GenAI half
- Local book: `AI/MLOps/Machine Learning Production Systems (O'Reilly 2025).epub`
- Local book: `AI/MLOps/The Machine Learning Solutions Architect Handbook — David Ping.epub`
- Vendor: `10-resources/vendor/machine-learning-systems-design/` (Chip Huyen's question set)
- Vendor: `10-resources/vendor/Machine-Learning-Interviews/src/MLSD/ml-system-design.md`
- Vendor: `10-resources/vendor/applied-ml/README.md` — real company ML case studies by topic
- [Exponent — ML system design interview guide 2026](https://www.tryexponent.com/blog/machine-learning-system-design-interview-guide)
