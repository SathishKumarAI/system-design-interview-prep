---
title: ML and GenAI cases index
type: index
track: ml
status: drafted
updated: 2026-09-02
tags: [index, ml, genai]
---

# ML / GenAI system design

The round that changed most in 2026: **GenAI design entered the standard question pool**, and
operational depth — cost, latency, monitoring, evaluation — is scored explicitly rather than
treated as a bonus.

## Where to look

| Question | File |
|---|---|
| How do I run an ML design round? The 6-step framework | [ml-playbook.md](ml-playbook.md) |
| Design a recommender (candidate gen → ranking) | [recommender.md](recommender.md) |
| Rank a feed / predict engagement, with real-time features | [feed-ranking.md](feed-ranking.md) |
| Real-time fraud detection under a 100 ms budget | [fraud-detection.md](fraud-detection.md) |
| Feature store: offline/online parity, point-in-time correctness | [feature-store.md](feature-store.md) |
| RAG assistant over company documents | [rag-assistant.md](rag-assistant.md) |
| Serve LLMs at scale: batching, KV cache, PD disaggregation | [llm-serving-platform.md](llm-serving-platform.md) |
| Monitoring, drift, retraining, and evaluation in production | [ml-monitoring-and-eval.md](ml-monitoring-and-eval.md) |

## What makes an ML design round different

| Backend round | ML round |
|---|---|
| Correctness is deterministic | Correctness is **statistical** — you argue about metrics, not tests |
| Latency budget | Latency budget **plus** a quality budget you can trade against it |
| Schema migration | **Training–serving skew** and feature versioning |
| Deploy = ship code | Deploy = ship code **and** a model, with a shadow/canary/holdback plan |
| Bug = wrong output | Bug = **slow degradation** nobody notices for six weeks |
| Cost = servers | Cost = **GPUs and tokens**, often 10x the rest of the system |

## The 2026 additions you must be ready for

1. **GenAI is in the standard pool.** "Design a RAG assistant", "design an LLM serving platform",
   "add an AI feature to X" are now as common as "design a recommender".
2. **Evaluation methodology is the new system design.** Interviewers care more about how you'd
   know the system is good — offline eval sets, LLM-as-judge with its failure modes, online A/B,
   guardrail metrics — than about the boxes in your diagram.
3. **Cost and latency reasoning is scored.** Tokens, GPU hours, batching, caching, model routing.
4. **Recommenders now often mean embeddings + vector stores + a generative layer**, not just
   collaborative filtering.

## The shape that generalises

Nearly every ML design is the same five stages. Learn the stages and new problems stop being new:

```
1. Framing      business goal → ML task → the metric you'll actually optimise
2. Data         sources, labels, leakage, freshness, privacy
3. Features     offline (training) and online (serving) from ONE definition
4. Model        baseline → candidate generation → ranking → re-rank/business rules
5. Serving      latency budget, batching, caching, fallback when the model is unavailable
6. Loop         monitoring, drift, feedback collection, retraining, evaluation, rollout
```

> [!tip] Opening line for any ML round
> "Before choosing a model: what business metric are we moving, what's the latency budget, and
> where do the labels come from? Those three answers determine most of the design."

## Referenced by

- [Interview prep index](../README.md)
- [Repo index](../../INDEX.md)
