---
title: Cost engineering
type: primitive
track: universal
difficulty: core
status: drafted
sources: [AWS Well-Architected cost pillar]
updated: 2026-09-02
tags: [cost, finops, egress, gpu]
---

# Cost engineering

New in the 2026 senior rubric, and the section almost nobody prepares. One dollar figure and
one lever in every design puts you ahead of most candidates.

## Where the money actually goes

In roughly this order for most consumer systems:

1. **Egress / bandwidth** — the silent killer for anything with media
2. **Compute at low utilisation** — fleets sized for peak, idle at night
3. **Storage that never expires** — nobody deletes anything, ever
4. **Managed service premiums** — convenient, 2–5x the raw resource
5. **Cross-AZ/region chatter** — a microservice tax you pay per hop
6. **Observability** — logs and high-cardinality metrics can rival the app's own bill
7. **GPU idle time** — for ML systems this jumps to #1 instantly

## The unit that matters: cost per request / per user / per token

Absolute cloud spend tells you nothing. **Cost per unit of business value** tells you
everything, and it's the number that lets you say "this feature costs $0.004 per view and
earns $0.01."

```
cost_per_request = (compute + storage + egress + managed services) / requests
```

Graph it. A regression in cost per request is a bug, exactly like a latency regression.

## Levers, roughly by payoff

| Lever | Typical saving | Cost |
|---|---|---|
| **CDN / edge caching** for anything served repeatedly | 50–90% of egress | Invalidation complexity |
| **Storage tiering + lifecycle policy** (hot → warm → archive) | 5–20x on cold data | Restore latency |
| **Compression** (zstd, columnar formats, Parquet) | 3–10x storage + transfer | CPU |
| **Right-sizing + autoscaling** to actual demand | 30–60% of compute | Scaling lag, cold starts |
| **Spot/preemptible** for interruptible work (batch, training, CI) | 60–90% of compute | Must be interruption-tolerant |
| **Reserved / savings plans** for steady baseline | 30–70% | 1–3 year commitment |
| **Sampling** logs and traces | 50–90% of observability | Less forensic depth |
| **Retention policies** everywhere | Compounding | Someone must decide what matters |
| **Colocating chatty services** in one AZ | Cross-AZ transfer | Reduced AZ redundancy — trade carefully |
| Batching (requests, writes, GPU inference) | Large | Latency |

## ML/GenAI-specific costs

| Lever | Effect |
|---|---|
| **Batching inference** (continuous batching for LLMs) | 3–5x throughput on the same GPU |
| **Quantisation** (fp16 → int8/int4) | 2–4x memory, more concurrent requests, small quality cost |
| **Distillation / model routing** — small model for the easy 80%, big model for the hard 20% | Often 5–10x |
| **Prompt/KV cache reuse** for repeated prefixes | Cuts prefill cost, which dominates in RAG |
| **Cache the whole answer** for repeated questions | The cheapest token is the one not generated |
| Spot GPUs + checkpointing for training | 60–90% |
| Right-sized embedding dimension / int8 vectors | 4x on vector store |

> [!tip] Interview line
> "Serving is $180k/month of GPU at 60% utilisation. Continuous batching plus routing the
> easy 80% of queries to a distilled model takes that under $60k with a measured quality
> delta we'd gate on eval. That's a bigger lever than any infrastructure change here."

## The FinOps loop (say it as a process, not a one-off)

1. **Attribute** — tags/labels per team, service, feature. Unattributed spend never shrinks.
2. **Show back** — each team sees its own bill weekly.
3. **Budget + anomaly alert** — catch the runaway job in hours, not at month end.
4. **Optimise** — the levers above, biggest first.
5. **Design reviews include a cost estimate** — the cheapest time to fix cost is before build.

## Traps

| Trap | Reality |
|---|---|
| "Serverless is cheaper" | True at low/spiky volume. At sustained high rps it's often 3–10x a reserved fleet |
| "Managed is expensive" | Compare against the engineer-months of running it yourself, honestly |
| "We'll optimise later" | Egress and retention compound; later is 10x the bill and the same fix |
| "Multi-region for reliability" | Doubles compute *and* adds replication egress. Justify with an actual RTO/RPO requirement |
| "Logs are cheap" | At 10 KB/request × 50k rps that's 43 TB/day of ingest |

## Interview lines

> [!tip] Say this
> "Rough monthly cost: ~$40k egress, ~$25k compute, ~$12k storage. Egress dominates, so a
> CDN is the first thing I'd build, not the last."

> [!tip] Say this
> "If I had to cut this bill by half tomorrow: lifecycle everything older than 30 days to
> archive, sample traces to 1%, and move batch transcoding to spot. None of those change the
> architecture."

## Numbers

See the cost anchors table in [../01-numbers.md](../01-numbers.md#6-cost-anchors).

## Referenced by

- [Design an infinite feed (frontend)](../04-frontend-cases/infinite-feed.md)
- [Design an LLM serving platform](../06-ml-cases/llm-serving-platform.md)
- [Design file sync / object storage (Dropbox, S3-like)](../03-backend-cases/object-storage-sync.md)
- [Design video streaming (YouTube / Netflix)](../03-backend-cases/video-streaming.md)
- [ML system design playbook](../06-ml-cases/ml-playbook.md)
- [Networking and the edge](networking-and-edge.md)
- [Primitives index](README.md)

## Sources & further reading

- [AWS Well-Architected — Cost Optimization Pillar](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html)
- [FinOps Foundation — framework](https://www.finops.org/framework/)
- Local book: `DevOps/Cloud-Certs/` (AWS/Azure cost and architecture material)
