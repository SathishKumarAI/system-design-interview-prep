---
title: Design real-time fraud detection
type: case
track: ml
difficulty: advanced
status: drafted
sources: [Designing ML Systems, payments practice]
updated: 2026-09-02
tags: [fraud, imbalance, delayed-labels, streaming-features, thresholds]
---

# Design real-time fraud detection

> Score every transaction in under 100 ms and decide approve / review / decline.
> **The hard part:** extreme class imbalance, labels that arrive 60 days late, an adversary who
> adapts to your model, and a threshold decision that is a business decision, not an ML one.

## 1. Clarify

| Question | Assumed answer |
|---|---|
| Decision or score? | Score + policy → approve / step-up (3DS/OTP) / review / decline |
| Latency budget? | < 100 ms p99 — it's inline in the payment flow |
| Volume? | 10k transactions/s peak; fraud rate ~0.1% |
| Cost asymmetry? | A missed fraud costs the transaction value; a false decline costs the sale **and** the customer |
| Labels? | Chargebacks (30–90 days), manual review outcomes (hours), customer reports |
| Adversarial? | Yes — fraudsters probe and adapt continuously |

**Non-goals:** the payment rails ([../03-backend-cases/payments-ledger.md](../03-backend-cases/payments-ledger.md)),
the manual review tooling, AML/sanctions screening (adjacent, rule-driven, different system).

## 2. Requirements

**Functional**
- Score each transaction with entity features (card, device, IP, merchant, account)
- Emit a decision plus a reason code (regulatory and operational necessity)
- Support rules alongside the model — instant blocking of a known-bad pattern
- Feed manual review outcomes back as fast labels

**Non-functional**

| Target | Value |
|---|---|
| p99 latency | < 100 ms including feature fetch |
| Availability | 99.99% — **fail-open or fail-closed is a business policy per segment** |
| Auditability | Every decision reproducible: model version, features, rules fired |
| Fairness | No disparate impact on protected attributes; documented and monitored |

## 3. Estimates

```
10k tps × 100 ms budget:
   feature fetch (entity aggregates, ~50 features)     ~25 ms
   model inference (GBDT, batched where possible)      ~10 ms
   rules engine                                        ~5 ms
   network + orchestration                             ~20 ms
   slack                                               ~40 ms                ← keep it
Labels: 10k tps × 86,400 = 864M txns/day, ~0.1% fraud = 864k positives/day
   but chargeback labels lag 30–90 days → today's model trains on ~2-month-old fraud   ← the design
Features: entity counters (card: txns in 1h/24h/7d; device: distinct cards; IP: velocity)
   → streaming aggregation, 100s of millions of keys, TTL'd
Cost of errors: false negative = txn value (avg $80); false decline = lost sale + churn risk
```

> [!info] The scary number
> The **label delay**, not the throughput. You are always training on a stale picture of an
> adversary who has already moved. Every design choice below follows from that.

## 4. API / contract

```http
POST /v1/risk/evaluate
  { txn_id, amount_minor, currency, card_token, merchant_id, device_fingerprint,
    ip, email_hash, billing_address_hash, ts }
  → 200 { decision: "approve"|"step_up"|"review"|"decline",
          score: 0.0-1.0, reason_codes: ["velocity_card_1h", "new_device"],
          model_version, rules_fired: [...], evaluation_id }

POST /v1/risk/label  { txn_id, label: "fraud"|"legit", source: "chargeback"|"review"|"report", ts }
```

`evaluation_id` + a stored feature snapshot make every decision auditable and disputable — a
regulatory requirement in most jurisdictions, and a strong thing to volunteer.

## 5. Data model

| Store | Content | Purpose |
|---|---|---|
| Online feature store | Entity aggregates keyed by card/device/IP/account/merchant | Sub-25 ms fetch |
| Streaming aggregator | Windowed counters (1 m, 1 h, 24 h, 7 d, 30 d) | Velocity features |
| Graph store (optional) | Entity links: shared device/card/address | Ring detection |
| Decision log | Every evaluation + features + outcome | Audit, training, backtesting |
| Label store | txn_id → label + source + timestamp | Training, with maturity windows |

**Feature families** — say these by name, they're the substance of the case:

| Family | Examples |
|---|---|
| **Velocity** | Transactions per card per hour; distinct cards per device per day; amount sum per account per 24 h |
| **Deviation** | Amount vs this account's historical distribution; new country/merchant category |
| **Entity reputation** | Merchant chargeback rate; IP/ASN risk; email domain age |
| **Graph** | Number of accounts sharing this device; is this card in a component with known fraud |
| **Context** | Time of day vs the account's normal, checkout latency, keystroke/behavioural signals |

## 6. Architecture

```
payment request → risk API
      ├→ rules engine (fast, deterministic, human-authored — blocklists, hard limits)
      ├→ feature fetch: online store (entity aggregates) + inline features
      ├→ model: GBDT ensemble → calibrated probability
      ├→ policy layer: score + rules + segment → decision + reason codes
      └→ decision log → Kafka

Kafka → streaming aggregator (Flink) → online feature store  [seconds]
      → lakehouse (decisions, features, outcomes)            [training + backtesting]
labels (chargebacks, review outcomes) → label store → training pipeline → registry → canary
```

### Deep dive A — imbalance, thresholds, and the business

- **Never optimise accuracy.** Use PR-AUC and, above all, the **operating point**: what
  precision/recall do we get at the threshold we'd actually ship?
- **The threshold is an economic decision:**
  `expected_cost(t) = FN(t)·avg_txn_value + FP(t)·(margin + churn_cost)`. Choose *t* to minimise
  it. Say this explicitly — it converts a modelling question into a business one, which is
  exactly the seniority signal here.
- **Different thresholds per segment**: a $5 digital good and a $5,000 electronics order deserve
  different bars. Segment by amount, merchant category and customer tenure.
- **Three outcomes, not two.** The middle band ("step up" — 3DS, OTP, or manual review) is where
  most value lives: it converts a hard binary decision into a cheap extra check, and it also
  generates *fast labels*.
- Handle imbalance in training with class weights or focal loss and careful negative sampling —
  but note that **resampling changes calibration**, so recalibrate afterwards.

### Deep dive B — delayed labels

- **Label maturity**: a transaction isn't confidently "legit" until the chargeback window closes.
  Training on immature labels teaches the model that recent fraud is legitimate — a
  quietly catastrophic bug.
- **Practical approach:** train the main model on matured labels (90 days old), and run a second,
  fast-adapting model on **fast labels** (manual review outcomes within hours, customer reports,
  hard declines) to catch new attack patterns quickly.
- **Backtesting must be time-based**, always. Random splits leak future information and make
  offline numbers meaningless.
- **Rules exist for the gap**: when a new attack pattern appears today, a human writes a rule
  today. The model catches up at the next retrain. **Rules and models are complements, not
  competitors** — say this; candidates who dismiss rules as unsophisticated get marked down.

### Deep dive C — adversarial adaptation

- Fraudsters probe with small transactions to learn your thresholds. Randomised thresholds within
  a band, and rate-limiting per entity, blunt this.
- **Concept drift is adversarial and fast** — weekly or continuous retraining, drift monitors on
  feature distributions and score distributions, and an on-call analyst workflow.
- Prefer features that are **expensive for the attacker to change** (behavioural, graph, funding
  history) over cheap ones (user agent, email address).
- Don't expose granular reason codes to end users — they're a free tutorial for the adversary.
  Detailed codes go to internal tooling; users see a generic message.

## 7. Scale & failure

| Breaks first at 10x | Fix |
|---|---|
| Feature store QPS | Local caching for hot merchants, fewer features, colocation |
| Streaming aggregator state (100M+ keys) | TTLs, coarser windows, key sharding, approximate counters |
| Graph features latency | Precompute component-level risk offline; skip graph on the hot path |
| Model latency at higher feature counts | Feature pruning by importance, quantised GBDT |

| Component fails | Blast radius | Degraded behaviour |
|---|---|---|
| Model service down | No score | **Policy decision, per segment**: fail-open (approve, flag for review) below an amount threshold, fail-closed above it. Never a global default — state the trade |
| Feature store down | Degraded features | Score with defaults + widen rules; alert loudly; consider raising step-up rate |
| Streaming lag | Stale velocity features | Alert on feature age; velocity gaps are exactly what attackers exploit |
| Label pipeline broken | Model silently rots | Alert on **label arrival rate**, not just job status |

## 8. Ops & cost

- **SLO:** p99 < 100 ms; 99.99% availability; fraud $ loss rate under target; false-decline rate
  under target. Both error rates are business SLOs and both must be graphed.
- **Alert on:** score distribution shift, approval-rate shift by segment, feature null/age,
  chargeback rate by cohort, review-queue depth, rule hit rates (a rule that suddenly fires 100x
  more is either an attack or a bug).
- **Rollout:** shadow scoring first (score everything, act on nothing, compare), then a champion/
  challenger split with a permanent holdback. Model changes here move money — treat rollouts
  like payments rollouts, not like feed rollouts.
- **Cost:** inference is cheap; the real cost is **fraud loss + false declines + manual review
  labour**. Optimising the review queue's precision is usually worth more than any infrastructure
  saving. Say that — it reframes cost around what the system is for.
- **First thing I'd cut:** graph features on the synchronous path (precompute instead), and
  low-importance features.

**Fairness and compliance, briefly but unprompted:** monitor decision rates across protected
segments, avoid proxies for protected attributes, keep reason codes explainable (SHAP or a
monotonic model where regulation requires it), and retain decisions for audit.

## Referenced by

- [ML and GenAI cases index](README.md)
- [Question bank](../07-drills/question-bank.md)
- [Repo index](../../INDEX.md)

## Sources & further reading

- Local book: `DE/Warehouse-ETL/Designing machine learning systems — Chip Huyen.pdf` — imbalance, delayed labels, drift
- Vendor: `10-resources/vendor/applied-ml/README.md` — fraud/abuse case studies
- Related: [feature-store.md](feature-store.md), [../03-backend-cases/payments-ledger.md](../03-backend-cases/payments-ledger.md)
