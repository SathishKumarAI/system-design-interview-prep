---
title: Design a RAG assistant over company documents
type: case
track: ml
difficulty: advanced
status: drafted
sources: [AI Engineering (Huyen), RAG survey 2026, Harmonia RAG serving]
updated: 2026-09-02
tags: [rag, retrieval, embeddings, eval, guardrails]
---

# Design a RAG assistant

> An internal assistant that answers questions from 10M company documents, with citations, and
> without leaking documents a user shouldn't see.
> **The hard part in 2026 interviews is not the pipeline — it's the *evaluation*, the *cost*, and
> the *permissions*.** Everyone can draw embed → retrieve → generate. Few can say how they'd know
> it works.

## 1. Clarify

| Question | Assumed answer |
|---|---|
| Corpus? | 10M documents (wiki, tickets, code, PDFs, Slack), 500 GB of text, changing daily |
| Users? | 20k employees, 50k queries/day, bursty during the working day |
| Latency? | First token < 2 s; full answer < 10 s (streaming) |
| Accuracy bar? | Must cite sources; "I don't know" is an acceptable and *desirable* answer |
| Permissions? | **Yes — per-document ACLs, strictly enforced** |
| Freshness? | New/edited documents searchable within ~15 minutes |
| Multi-turn? | Yes, conversational with follow-ups |

**Non-goals:** training a foundation model, the document authoring tools, agentic actions
(read-only assistant for v1).

## 2. Requirements

**Functional**
- Answer natural-language questions grounded in retrieved documents, with citations
- Respect per-user document permissions **at retrieval time**
- Handle follow-ups (query rewriting against conversation history)
- Say "I don't know" rather than fabricate
- Collect feedback (thumbs, corrections) for evaluation

**Non-functional**

| Target | Value |
|---|---|
| Time to first token | < 2 s p95 |
| Groundedness | > 95% of claims supported by a cited source |
| **Permission leaks** | **Zero. A single leak ends the project** |
| Freshness | < 15 min |
| Cost | Budget per answer; measured and graphed |

## 3. Estimates

```
Corpus: 10M docs → chunked ~600 tokens with overlap ≈ 40M chunks
Embeddings: 40M × 1024 dims × 4 B = 164 GB (fp32) → 41 GB int8 → 10 GB with PQ
   → fits in a memory-resident vector index on a few nodes
Embedding cost (one-off + ~2% daily churn): 40M × 600 tokens = 24B tokens
   → a batch embedding job, cheap per token but not free; recompute on model change is the
     expensive event to plan for
Queries: 50k/day ≈ 0.6 rps avg, ~5 rps peak                     ← tiny; this is NOT a scale problem
Per answer: ~8 chunks × 600 tokens = ~5k input tokens + ~500 output
   Frontier-model list pricing (e.g. Claude Opus 5: $5/M input, $25/M output) →
     ~$0.025 + ~$0.0125 ≈ $0.04/answer → 50k/day ≈ $2k/day ≈ $60k/month   ← the scary number
   Prompt caching of the stable system prompt + reused context cuts input cost materially
```

> [!info] The scary number
> **Cost per answer × volume.** Retrieval is cheap; generation is not. The design levers that
> matter are context size, model routing, caching, and answer reuse — not vector-database
> throughput.

## 4. API / contract

```http
POST /v1/chat            (SSE stream)
  { conversation_id, message, filters?: {space, doc_type, after} }
  → stream of tokens, then:
    { citations: [{doc_id, chunk_id, title, url, quote, score}],
      retrieval_debug_id, model, tokens: {in, out}, cost_usd }

POST /v1/feedback  { message_id, rating, correction?, reason? }
```

Citations are part of the contract, not decoration: they're how the user verifies, how you
measure groundedness, and how you debug.

## 5. Data model

| Store | Content |
|---|---|
| Document store | Raw docs + metadata + **ACL list** + version + updated_at |
| Chunk store | `chunk_id → text, doc_id, position, heading path, ACL, embedding_version` |
| **Vector index** | Chunk embeddings + filterable metadata (ACL, space, date, doc_type) |
| **Lexical index** | BM25 over the same chunks (hybrid retrieval — see below) |
| Conversation store | Messages, retrieved context refs, feedback |
| Eval store | Golden Q/A set, judgments, run history |

**Chunking** deserves a real answer, not "split by 500 tokens":

| Strategy | Notes |
|---|---|
| Fixed-size + overlap (~600 tokens, 15%) | Simple, robust baseline |
| **Structure-aware** (headings, sections, code blocks, table rows) | Much better — respects the document's own boundaries |
| Small-to-big | Embed small precise chunks, but return the surrounding parent section to the model |
| Contextual prefixing | Prepend document title + heading path to each chunk before embedding — cheap, and one of the largest single retrieval-quality wins available |

## 6. Architecture

```
INGESTION (continuous)
sources → CDC/webhooks → parse (PDF/HTML/code) → clean → chunk (structure-aware)
        → embed (batch) → upsert into vector index + lexical index (ACL carried on every chunk)
        → dead-letter for parse failures

QUERY
user → auth → query understanding (rewrite follow-ups into standalone queries; classify intent)
     → HYBRID retrieval, ACL-filtered:
          dense (ANN over embeddings)  ─┐
          lexical (BM25)               ─┴→ fusion (RRF) → top ~50
     → rerank (cross-encoder) → top ~8
     → assemble prompt (system + citations-required instructions + chunks + history)
     → LLM (streaming) → post-process: verify citations resolve, apply guardrails
     → response + citations + logs
```

### Deep dive A — retrieval quality (where the wins are)

Ranked by payoff per unit of effort:

1. **Hybrid retrieval.** Dense embeddings miss exact identifiers (error codes, ticket numbers,
   function names); BM25 misses paraphrase. Run both, fuse with reciprocal rank fusion. This is
   the single biggest quality jump and it's cheap.
2. **Reranking.** A cross-encoder scores (query, chunk) pairs jointly and reorders the top 50 to
   the top 8. Adds ~50–100 ms and materially improves precision — the second-biggest win.
3. **Query rewriting.** "What about the second one?" is unanswerable standalone. Rewrite against
   history before retrieving. Also decompose multi-part questions into several retrievals.
4. **Metadata filters** as first-class: date ranges, spaces, document types.
5. **Contextual chunk prefixes** (title + heading path) before embedding.

> [!tip] Interview line
> "I'd start with hybrid retrieval plus a reranker before touching the generation model at all.
> In practice most 'the LLM is hallucinating' complaints are retrieval failures — the model never
> got the right chunk."

### Deep dive B — permissions (the one that gets people fired)

**Filter at retrieval, never after generation.** If a forbidden chunk reaches the model, it is
already in the answer — post-filtering the citation list does not remove the leaked content from
the generated text.

- ACLs stored **on the chunk**, and the vector search is a filtered search (pre-filter or
  filtered-HNSW), not "search then filter" (which silently returns fewer than k results, or
  none).
- ACL changes must propagate fast; a revoked user must not retrieve within minutes.
- Multi-tenant deployments: consider a separate index per tenant, so a filter bug can't cross
  the tenant boundary at all — defence in depth beats a correct `WHERE` clause.
- **Test it explicitly**: a red-team eval set of "questions whose answer lives in a document this
  user can't see", asserting the assistant says it doesn't know. Volunteering this test set is
  a very strong signal.

### Deep dive C — evaluation ("the new system design")

Four layers, and interviewers now expect all four:

| Layer | What | Metric |
|---|---|---|
| **Retrieval** | Does the right chunk come back? | recall@k, MRR, nDCG on a labelled query set |
| **Generation** | Is the answer grounded, complete, correct? | Groundedness/faithfulness, answer relevance, citation accuracy |
| **End-to-end** | Would a human accept this? | Human review on a sample + a golden set of ~200 Q/A pairs |
| **Online** | Real usage | Thumbs up/down, follow-up rate, escalation-to-human rate, task completion |

**LLM-as-judge** is the practical tool for scale — but say its failure modes, because that's the
depth question: position bias, verbosity bias, self-preference, and drift when the judge model
changes. Mitigate with a **fixed, pinned judge model and prompt**, randomised option order,
calibration against human labels on a subset, and rubric-style scoring rather than a bare 1–10.

**Regression testing is the deliverable:** a golden set that runs in CI on every prompt, chunking,
embedding or model change. Without it, every change is a guess. The retrieval layer is where
most regressions actually originate, so instrument it separately.

### Deep dive D — cost and latency

| Lever | Effect |
|---|---|
| **Prompt caching** of the stable system prompt + reused context | Large input-token saving on repeated prefixes |
| **Answer caching** (semantic cache on normalised queries) | The cheapest token is one never generated; internal assistants have very repetitive questions |
| **Model routing** — small model for easy/lookup queries, frontier model for hard ones | Often 5–10x on the blended rate |
| Fewer/tighter chunks (8 → 5, with reranking making up the quality) | Direct input-token saving |
| Streaming | Doesn't cut cost, but cuts *perceived* latency, which is what users judge |
| Batch embedding jobs and int8/PQ vectors | Ingestion + memory cost |

**Latency budget:** rewrite ~150 ms + retrieval ~100 ms + rerank ~80 ms + LLM first token
~600 ms ≈ 1 s to first token, streaming after. If it doesn't add up, cut the rerank depth first.

## 7. Scale & failure

| Breaks first at 10x | Fix |
|---|---|
| Generation cost | Routing, caching, shorter contexts |
| Vector index memory | int8/PQ quantisation, sharding, tiering cold documents |
| Re-embedding on model change | Plan for it: versioned embeddings, dual-index and cut over — never in place |
| Ingestion lag on bursty edits | Priority queue by document importance |

| Component fails | Blast radius | Degraded behaviour |
|---|---|---|
| LLM provider degraded/rate-limited | No answers | Fallback to a secondary model/provider; queue and retry; **show retrieved documents with snippets** — search results are a genuinely useful degraded mode |
| Vector index down | No dense retrieval | **BM25-only** retrieval, flagged as degraded — a real benefit of hybrid |
| Reranker down | Lower precision | Skip it; serve fusion order |
| Ingestion stalled | Stale answers | Show "as of" freshness; alert on index age |
| ACL propagation lag | **Potential leak** | Fail closed: if the ACL service is unavailable, retrieve nothing rather than everything |

## 8. Ops & cost

- **SLO:** TTFT p95 < 2 s; groundedness > 95% on the golden set; **zero** permission leaks;
  freshness < 15 min.
- **Alert on:** thumbs-down rate, "I don't know" rate (both a spike *and* a collapse are bad),
  retrieval recall proxy, citation-resolution failures, cost per answer, ingestion lag,
  ACL-filter error rate.
- **Rollout:** every change (prompt, chunking, embedding model, LLM version) runs the golden set
  in CI, then ships to an internal cohort, then to everyone. **Pin model versions** — a silent
  provider-side model change is a real production risk and worth naming.
- **Cost:** generation dominates. Track $/answer and $/user/month, and put both on a dashboard —
  cost per answer is the metric that keeps a GenAI product alive after the pilot.
- **First thing I'd cut:** context size and routing more traffic to a smaller model, gated on
  golden-set quality.

**Guardrails, briefly:** prompt-injection defence (documents are untrusted input — a document can
contain "ignore your instructions"; instruct the model to treat retrieved content as data, not
instructions, and never let retrieved text trigger tool calls in v1), PII redaction, refusal for
out-of-scope questions, and output filtering. Say prompt injection unprompted — retrieved content
is attacker-controllable in any system where users can create documents.

## Referenced by

- [8-week study plan](../07-drills/8-week-plan.md)
- [Books already on this machine](../10-resources/books-on-this-machine.md)
- [Design an LLM serving platform](llm-serving-platform.md)
- [Design search and typeahead](../03-backend-cases/search-typeahead.md)
- [Microsoft, Apple, Netflix and other big tech](../09-company-styles/microsoft-apple-netflix.md)
- [ML and GenAI cases index](README.md)
- [Question bank](../07-drills/question-bank.md)
- [Repo index](../../INDEX.md)
- [Storage and databases](../02-primitives/storage-and-databases.md)

## Sources & further reading

- Local book: `AI/LLM-Apps/AI Engineering — Chip Huyen (2025).pdf` — **the best single reference for this case**
- Local book: `AI/RAG-Knowledge-Graphs/A Simple Guide to Retrieval Augmented Generation.pdf`
- Local book: `AI/RAG-Knowledge-Graphs/Essential GraphRAG.pdf`, `Prompt Engineering for LLMs (O'Reilly).pdf`
- Local: `AI/RAG-Knowledge-Graphs/AI_Evals_The_Ultimate_FAQ_Free_Resources.pdf`
- [Engineering the RAG Stack: architecture and trust frameworks (arXiv 2026)](https://arxiv.org/pdf/2601.05264)
- [Harmonia: End-to-End RAG Serving Optimization (arXiv)](https://arxiv.org/pdf/2505.07833)
- Related: [llm-serving-platform.md](llm-serving-platform.md), [../03-backend-cases/search-typeahead.md](../03-backend-cases/search-typeahead.md)
