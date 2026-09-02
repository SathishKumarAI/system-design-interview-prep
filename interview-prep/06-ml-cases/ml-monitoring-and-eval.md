---
title: Design ML monitoring, evaluation and retraining
type: case
track: ml
difficulty: core
status: drafted
sources: [Designing ML Systems, MLOps practice]
updated: 2026-09-02
tags: [drift, monitoring, retraining, ab-testing, eval]
---

# Design ML monitoring, evaluation and retraining

> The platform layer that keeps 50 production models honest: detects degradation, evaluates
> changes, retrains safely, and rolls back fast.
> **The hard part:** the ground truth arrives late or never, so you have to detect problems from
> inputs and outputs alone — and then prove a fix actually helped.

## 1. Clarify

| Question | Assumed answer |
|---|---|
| How many models, owned by whom? | ~50 models, 15 teams |
| Label delay? | Varies: seconds (clicks) to 90 days (chargebacks); some have no labels at all |
| Retraining cadence? | Per-model: daily to monthly, plus drift-triggered |
| Who is on call for model quality? | The owning team; the platform provides detection |
| Do we run online experiments? | Yes — a shared A/B platform exists |

**Non-goals:** the models, the feature store ([feature-store.md](feature-store.md)), the training
compute platform.

## 2. Requirements

**Functional**
- Log every prediction with features, model version and context
- Detect data drift, concept drift and skew per model; alert the owner
- Compute delayed-label metrics as labels arrive
- Run offline evaluation on every candidate model, sliced by segment
- Support shadow, canary, A/B and holdback deployment patterns; one-click rollback
- Maintain a model registry with lineage: data → features → code → model → deployment

**Non-functional**

| Target | Value |
|---|---|
| Detection latency | Drift detected within 1 hour of onset |
| Logging overhead | < 5 ms added to prediction latency |
| False alarms | Low enough that alerts aren't muted — **the binding constraint** |
| Retention | Predictions 90 days; aggregates 2 years |

## 3. Estimates

```
50 models × avg 2k rps = 100k predictions/s
   Full logging: 100k/s × 2 KB (features + prediction + context) = 200 MB/s = 17 TB/day  ← too much
   → sample: 100% of metadata (cheap), 1–10% of full feature vectors, 100% for money/safety models
   → ~1–2 TB/day, tiered to object storage
Drift computation: per model × per feature × per hour
   50 models × 200 features × 24 = 240k distribution comparisons/day — trivial in aggregate,
   but a naive per-feature alert would page someone 240k times. Aggregate first.       ← the design
```

> [!info] The scary number
> Not the data volume — the **alert volume**. 50 models × 200 features is 10,000 things that can
> individually "drift". Alerting per feature guarantees the system gets muted within a week.

## 4. API / contract

```python
# instrumentation (in the serving path, async, non-blocking)
monitor.log_prediction(
    model="fraud_v7", request_id=..., features={...},
    prediction=0.83, decision="review", latency_ms=42, ts=...,
)
monitor.log_label(request_id=..., label=1, source="chargeback", ts=...)

# registry
registry.register(model, metrics=..., training_data_ref=..., feature_refs=..., code_sha=...)
registry.promote("fraud_v8", stage="canary", traffic_pct=5)
registry.rollback("fraud")            # must be one command, and rehearsed
```

Logging is **async and fire-and-forget** — monitoring must never add latency to, or take down,
the prediction path.

## 5. Data model

| Store | Content | Retention |
|---|---|---|
| Prediction log | request_id, model_version, features (sampled), prediction, decision, context | 90 days |
| Label store | request_id → label, source, arrival timestamp | 2 years |
| Metrics store (time-series) | Per-model, per-feature distributions and summary stats | 2 years aggregated |
| Model registry | Versions, lineage, eval results, deployment state, owner | Forever |
| Eval sets | Golden/held-out sets, versioned | Forever |

Joining predictions to labels on `request_id` is the whole point of the schema — without a shared
ID assigned at prediction time, you cannot compute a single delayed metric.

## 6. Architecture

```
serving → async prediction log → Kafka
                                   ├→ real-time aggregator (Flink): distributions, latency, null rates
                                   ├→ lakehouse: full logs for analysis and training
                                   └→ drift jobs (hourly): compare live vs reference window
labels (various sources, various delays) → label store → join on request_id
                                   → delayed metrics (AUC, precision@k, business KPI)
alerts → owning team + dashboard
registry ← training pipeline ← retraining trigger (schedule | drift | metric decay)
```

### Deep dive A — what to monitor, in priority order

The ordering is the answer: you almost never have fresh labels, so monitor inputs and outputs
first.

| Priority | Signal | Detects |
|---|---|---|
| 1 | **Feature null / default rate** | Broken upstream pipeline. **The highest-value ML alert there is** — models degrade silently and immediately when features go missing |
| 2 | **Prediction distribution shift** | Something changed: input drift, a bad deploy, or an upstream bug. Cheap, needs no labels |
| 3 | **Feature distribution drift** | Input drift, per feature, aggregated to a model-level score |
| 4 | **Serving latency / error rate** | Ordinary reliability |
| 5 | **Business metric by segment** | The thing you actually care about, but noisy and slow |
| 6 | **Delayed-label metrics** | Ground truth — most trustworthy, arrives last |

**Drift tests:** PSI or KL divergence for numeric features, chi-square for categorical, and a
KS test for continuous distributions. Compare a rolling live window against a **fixed reference**
(the training distribution) *and* against last week (seasonality-aware). Report a per-model
drift score built from feature importances so the alert says "this model has drifted", not
"feature 147 moved" — that aggregation is what keeps alert volume survivable.

**Skew vs drift** — different root causes, different fixes:
- *Data drift*: the input distribution moved. Retraining usually helps.
- *Concept drift*: the input→label relationship moved. Retraining on **recent** data helps;
  retraining on everything doesn't.
- *Training–serving skew*: a bug. Retraining does nothing; fix the pipeline.

Saying which of the three you'd suspect from which symptom is a strong deep-dive answer.

### Deep dive B — evaluation before deployment

1. **Offline eval** on a time-split held-out set, **sliced by segment** — new users, each region,
   mobile, high-value customers. An aggregate improvement that hides a segment regression is the
   classic silent failure, and slicing is what catches it.
2. **Backtesting** on a historical window with point-in-time-correct features.
3. **Shadow mode**: run the candidate on live traffic, serve nothing, compare predictions and
   latency against the champion. Catches skew and performance problems with zero user risk.
4. **Online A/B** with proper sample-size math, a fixed duration decided in advance (no peeking
   until significance), guardrail metrics that can abort the test, and per-segment results.
5. **Holdback**: keep a small permanent cohort on the old model to measure long-run effects an
   A/B test can't see (novelty decay, ecosystem effects).

### Deep dive C — retraining

| Trigger | Use when |
|---|---|
| Scheduled (daily/weekly) | Stable domains, cheap training |
| **Drift-triggered** | Volatile domains — retrain when the drift score crosses a threshold |
| Metric-decay-triggered | You have reasonably fresh labels |
| Data-volume-triggered | Cold-start systems accumulating their first data |

Non-negotiables to state: the pipeline is **reproducible** (pinned data snapshot, code SHA,
config, seed), the new model must **beat the incumbent on the eval suite** before it can be
promoted, and promotion is automated but **gated** — auto-train, auto-evaluate, *human or
metric-gated* promotion for anything that touches money or safety.

**Continuous training pitfall to raise:** a model retrained on data its predecessor generated
locks in its own biases. Keep exploration traffic and a random-exposure slice so you retain an
unbiased sample to train and evaluate on.

### Deep dive D — keeping alerts trustworthy

- **Tier models**: revenue/safety-critical models page; experimental models write to a dashboard.
- Aggregate feature-level signals into one model-level drift score before alerting.
- Every alert names the owning team and links a runbook. No owner → the model gets deprecated.
- Track per-alert **precision** (did it correspond to a real problem?) and retire alerts that
  never do. An alert nobody acts on is worse than no alert — it manufactures false confidence.

## 7. Scale & failure

| Breaks first at 10x | Fix |
|---|---|
| Prediction log volume | Sample harder (keep 100% of metadata, less of features), compress, tier |
| Drift job runtime | Sketches (t-digest, HLL) instead of raw distributions; incremental computation |
| Alert volume | Stricter tiering, aggregation, suppression during known incidents |
| Registry/experiment metadata | Standard database scaling; not the hard part |

| Component fails | Blast radius | Degraded behaviour |
|---|---|---|
| Logging pipeline down | Blind to quality | **Serving unaffected** (async by design); alert on log-arrival rate |
| Label pipeline broken | Metrics silently freeze | Alert on **label arrival rate** — a frozen metric looks like a healthy metric |
| Drift job fails | No detection | Alert on job absence; a monitoring system must monitor itself |
| Registry down | Can't deploy or roll back | Cache last-known-good deployment state locally so rollback still works |

## 8. Ops & cost

- **SLO:** drift detected < 1 h; alert precision > 50%; 100% of tier-1 models have an owner, a
  runbook and a rollback path.
- **Alert on:** feature null rates, model drift scores, prediction distribution shifts, delayed
  metrics vs baseline, label arrival rate, monitoring job health.
- **Rollout:** shadow → canary → A/B → full, with automatic rollback on guardrail breach. Rollback
  must be **one command and rehearsed** — an untested rollback is not a rollback.
- **Cost:** log storage and drift compute. Levers: sampling rates, retention tiers, sketch-based
  statistics. Keep it well under the cost of the models it protects, and say what fraction that is.
- **First thing I'd cut:** full feature logging for non-critical models (metadata only), and raw
  prediction retention 90 → 30 days.

## Referenced by

- [ML and GenAI cases index](README.md)
- [Question bank](../07-drills/question-bank.md)
- [Repo index](../../INDEX.md)

## Sources & further reading

- Local book: `DE/Warehouse-ETL/Designing machine learning systems — Chip Huyen.pdf` — the monitoring and continual-learning chapters
- Local book: `AI/MLOps/2023-10-EB-Big-Book-of-MLOps-2nd-Edition.pdf`
- Local book: `DE/System-Design/Implementing MLOps in the Enterprise.pdf`
- Related: [feature-store.md](feature-store.md), [../02-primitives/observability-and-delivery.md](../02-primitives/observability-and-delivery.md)
