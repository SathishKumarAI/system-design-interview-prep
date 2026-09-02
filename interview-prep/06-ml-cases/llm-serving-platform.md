---
title: Design an LLM serving platform
type: case
track: ml
difficulty: advanced
status: drafted
sources: [vLLM docs/blog 2025-2026, PD disaggregation papers, Anthropic API pricing]
updated: 2026-09-02
tags: [llm, vllm, kv-cache, batching, gpu, cost]
---

# Design an LLM serving platform

> Serve open-weight LLMs to internal products: chat, code assistance, batch summarisation.
> **The hard part:** GPU memory is the bottleneck and it's consumed by the **KV cache**, which
> grows with every token of every concurrent request. Everything here is about keeping GPUs busy
> without running out of memory.

## 1. Clarify

| Question | Assumed answer |
|---|---|
| Self-hosted or API? | Self-hosted open-weight models, plus a hosted-API path for the hardest queries |
| Models? | One 70B-class chat model, one 8B fast model, one embedding model |
| Traffic? | 500 rps peak, mixed prompt lengths (200 to 100k tokens) |
| Latency? | Interactive: TTFT < 500 ms, > 30 tokens/s per stream. Batch: throughput only |
| Multi-tenant? | Yes — many internal teams, need quotas and isolation |
| SLO tiers? | Interactive vs batch, with different guarantees |

**Non-goals:** training/fine-tuning infrastructure, the applications themselves.

## 2. Requirements

**Functional**
- OpenAI-compatible chat/completions API with streaming
- Multiple models, versioned; routing by tier and task
- Per-tenant quotas, rate limits, and usage accounting
- Batch endpoint for offline jobs at lower priority

**Non-functional**

| Target | Value |
|---|---|
| TTFT (interactive) | p95 < 500 ms |
| Inter-token latency | < 30 ms (≈ 33 tok/s) |
| GPU utilisation | > 70% — **this is the cost metric** |
| Availability | 99.9%, degrade to a smaller model |

## 3. Estimates

```
Model weights: 70B params × 2 B (fp16) = 140 GB → doesn't fit one 80 GB GPU
   → tensor parallelism across 2–4 GPUs, or fp8/int8 quantisation (70 GB / 35 GB)

KV cache — the thing that actually limits concurrency:
   ≈ 2 (K and V) × layers × heads_kv × head_dim × 2 B × tokens
   For a 70B-class model, roughly 0.1–0.5 MB per token of context (GQA reduces this a lot).
   At ~0.2 MB/token:
      one 8k-token conversation ≈ 1.6 GB of KV
      80 GB GPU − 70 GB weights (fp8) = ~10 GB free → ~6 concurrent 8k conversations  ← ouch
      Quantise weights to int4 (~35 GB) → ~45 GB for KV → ~28 concurrent            ← the lever

Throughput: prefill is compute-bound (parallel over tokens), decode is memory-bandwidth-bound
   (one token at a time). They have opposite bottlenecks — which is why they get separated.

Cost: H100-class GPU ≈ $2–5/hour on demand.
   16 GPUs ≈ $30–60k/month. Utilisation is the whole game.
Comparison anchor: a hosted frontier API (e.g. Claude Opus 5 at $5/M input, $25/M output)
   — always compute the break-even before assuming self-hosting is cheaper.
```

> [!info] The scary number
> **KV cache per concurrent request.** It, not FLOPs, sets your concurrency ceiling, and it's why
> PagedAttention exists.

## 4. API / contract

```http
POST /v1/chat/completions
  { model, messages, max_tokens, stream: true, temperature, tenant_id }
  → SSE token stream, then usage {prompt_tokens, completion_tokens, cached_tokens}

POST /v1/batch          # lower priority, higher throughput, no latency SLO
GET  /v1/models
GET  /v1/usage?tenant=  # accounting and chargeback
```

Return `cached_tokens` — tenants can only optimise prompt reuse if you tell them it's happening.

## 5. Architecture

```
clients → gateway (auth, per-tenant rate limit + quota, routing, usage metering)
        → router: model choice by tier/task; queue by priority (interactive > batch)
        → inference tier (vLLM / SGLang / TensorRT-LLM):
              prefill workers  ──KV cache transfer──▶  decode workers   (PD disaggregation)
              continuous batching + PagedAttention + chunked prefill
              prefix cache (shared system prompts, RAG contexts)
        → response stream
        observability: TTFT, ITL, queue depth, KV utilisation, tokens/s/GPU, $/1k tokens
```

### Deep dive A — the four techniques that make this affordable

| Technique | Problem it solves | Effect |
|---|---|---|
| **Continuous batching** | Static batching wastes slots: the batch waits for its slowest sequence | Schedule at the *iteration* level — finished sequences leave, new ones join immediately. Large throughput gain; the foundational trick (from Orca) |
| **PagedAttention** | KV cache fragmentation — reserving worst-case contiguous memory per request wastes most of it | Page the KV cache like virtual memory, in fixed blocks. Near-zero waste, enables prefix sharing |
| **Chunked prefill** | A long prefill blocks all decodes, spiking inter-token latency for everyone | Split prefill into chunks and interleave with decode steps. Smooth ITL under mixed loads |
| **Prefix caching** | The same system prompt / RAG context is re-prefilled per request | Reuse KV blocks for shared prefixes — big saving for RAG and agents, where prefill dominates |

Together these are why a modern serving stack handles several times the traffic of a naive
`model.generate()` loop on identical hardware.

### Deep dive B — prefill/decode disaggregation

Prefill and decode have **opposite bottlenecks**: prefill is compute-bound and parallel over the
prompt; decode is memory-bandwidth-bound and strictly sequential. Co-locating them means each
interferes with the other — a long prefill stalls everyone's token stream.

**PD disaggregation** puts them on separate GPU pools: prefill nodes process prompts and transfer
the resulting KV cache over the network to decode nodes.

- **Buys:** independent scaling (RAG workloads are prefill-heavy; chat is decode-heavy),
  predictable inter-token latency, better hardware fit per pool.
- **Costs:** KV cache transfer bandwidth between pools, a scheduler that must place and track
  requests across two tiers, and more operational surface.
- **Status:** by 2026 this is the industry-standard architecture, supported across the major
  serving frameworks (vLLM, SGLang, TensorRT-LLM, LMDeploy, NVIDIA Dynamo) and deployed at scale
  by large providers. Say it by name — it's the current state of the art and a strong signal.

> [!tip] Interview line
> "I'd start co-located with continuous batching and chunked prefill, and move to prefill/decode
> disaggregation when the workload mix makes interference the dominant latency problem — which
> for RAG-heavy traffic it will, because prefill is most of the work."

### Deep dive C — memory and quantisation

Order of levers when you run out of GPU memory:

1. **Quantise weights** — fp16 → fp8 → int4. 2–4x memory freed for KV cache, small measured
   quality cost. Gate on an eval set, not vibes.
2. **KV cache quantisation** (fp8/int8) — directly multiplies concurrency.
3. **GQA / MQA models** — grouped-query attention shrinks KV per token dramatically; a model
   architecture choice with an enormous serving consequence.
4. **Tensor parallelism** across GPUs for weights; **pipeline parallelism** across nodes when a
   model doesn't fit a single node.
5. **Cap max context per tier** — a 200k-token context request consumes the KV budget of dozens of
   normal ones. Price and quota it accordingly.
6. **Preemption/eviction**: under memory pressure, evict a low-priority sequence's KV cache and
   recompute later. Better than OOM-killing the server.

### Deep dive D — routing and quality/cost trade

- **Model routing**: a small model handles the easy majority; escalate hard queries to the large
  model or a hosted frontier API. Typically the largest single cost lever, often 5–10x.
- **Speculative decoding**: a small draft model proposes tokens, the large model verifies several
  at once — 1.5–3x decode speedup with identical output distribution when done correctly.
- **Structured output / constrained decoding** for JSON, so downstream parsing doesn't need retries.
- **Semantic answer caching** upstream of the model — the cheapest token is the one never generated.
- **Build vs buy:** compute honestly. Self-hosting wins on sustained high volume with a fixed
  model; a hosted API wins on spiky traffic, frontier quality, and zero ops. Saying "here's the
  break-even in tokens/month" is a much better answer than picking a side.

## 6. Data model / state

Mostly stateless per request, but three pieces of state matter:

| State | Where | Note |
|---|---|---|
| KV cache | GPU memory, paged | The scarce resource; sized and monitored |
| Prefix cache | GPU + optional CPU/host tier | Shared system prompts and RAG contexts |
| Conversation history | **Client/application side**, resent per request | The serving tier stays stateless and horizontally scalable |
| Usage records | Warehouse | Per-tenant accounting and chargeback |

## 7. Scale & failure

| Breaks first at 10x | Fix |
|---|---|
| KV cache memory | Quantisation, GQA models, context caps, PD disaggregation |
| Prefill compute (long RAG prompts) | More prefill nodes, prefix caching, shorter contexts |
| Queue depth for interactive traffic | Priority queues, admission control, autoscaling, shed batch first |
| GPU availability/cost | Spot for batch, reservations for interactive, multi-region |

| Component fails | Blast radius | Degraded behaviour |
|---|---|---|
| A GPU node dies | In-flight requests on it fail | Retry on another node (requests are stateless); drain on health failure |
| Large model unavailable | Interactive quality drops | **Route to the small model** with a header noting degradation |
| Overload | Latency collapse for everyone | Admission control + queue timeouts: reject fast with 429 rather than accept work you can't finish |
| One tenant floods the platform | Everyone suffers | Per-tenant token-rate quotas at the gateway, separate queues per tier |

## 8. Ops & cost

- **SLO:** TTFT p95 < 500 ms, ITL p95 < 30 ms, 99.9% availability, GPU utilisation > 70%.
- **Alert on:** queue depth and wait time, KV cache utilisation, preemption rate, TTFT/ITL by
  tier, tokens/s/GPU, per-tenant token spend anomalies, OOM/eviction counts.
- **Rollout:** model or engine version changes go through an eval suite (quality) plus a load
  test (throughput/latency), then canary by traffic percentage per tenant tier.
- **Cost:** GPU hours dominate; everything else is noise. Track **$/1M tokens served** and
  **tokens/s/GPU**. Levers, biggest first: routing to smaller models, quantisation, batching
  efficiency, prefix caching, spot instances for batch work, and raising utilisation by mixing
  batch traffic into interactive troughs.
- **First thing I'd cut:** max context length per tier, and interactive capacity reserved for
  overnight troughs (fill it with batch).

## Sources & further reading

- [Inside vLLM: anatomy of a high-throughput inference system](https://vllm.ai/blog/2025-09-05-anatomy-of-vllm)
- [vLLM — PagedAttention and continuous batching explained](https://www.runpod.io/articles/guides/vllm-pagedattention-continuous-batching)
- [LLM serving optimization: continuous batching, PagedAttention, chunked prefill on H100 (2026)](https://www.spheron.network/blog/llm-serving-optimization-continuous-batching-paged-attention/)
- [FlowKV: disaggregated inference with low-latency KV cache transfer (arXiv)](https://arxiv.org/pdf/2504.03775)
- Local book: `AI/LLM-Apps/AI Engineering — Chip Huyen (2025).pdf` — inference optimisation chapters
- Local book: `AI/MLOps/LLM Engineer's Handbook.epub`
- Related: [rag-assistant.md](rag-assistant.md), [../02-primitives/cost-engineering.md](../02-primitives/cost-engineering.md)
