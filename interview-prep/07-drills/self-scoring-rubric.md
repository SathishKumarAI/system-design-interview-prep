---
title: Self-scoring rubric
type: drill
track: universal
difficulty: core
status: drafted
sources: [2026 interview rubrics]
updated: 2026-09-02
tags: [rubric, scoring]
---

# Self-scoring rubric

Score **before** reading the reference. 1–4 per line. Be harsh — a generous self-score is a
wasted drill.

| Score | Meaning |
|---|---|
| 1 | Didn't do it |
| 2 | Did it badly or only when prompted |
| 3 | Did it competently, unprompted — **the hire bar** |
| 4 | Did it excellently; taught the interviewer something |

## The scorecard

| # | Competency | 3 = hire looks like | Score |
|---|---|---|---|
| 1 | **Requirements & scope** | Asked 4–6 questions that changed the design; wrote functional, non-functional and **non-goals** on the board | |
| 2 | **Estimation** | Produced peak rps, storage/year and one cost number; identified **which number is the constraint** | |
| 3 | **API & data model** | Defined the contract before the boxes; chose a partition key and justified it against access patterns | |
| 4 | **High-level architecture** | Every component traced to a requirement; arrows labelled; described the request path end to end in one sentence | |
| 5 | **Depth** | One or two deep dives with real mechanics — key formats, TTLs, algorithms, numbers | |
| 6 | **Trade-offs** | For each significant choice, said what it buys *and* what it costs, and why that's acceptable here | |
| 7 | **Scale & failure** | Named the first bottleneck at 10x; gave degraded behaviour for each dependency, unprompted | |
| 8 | **Ops** | SLO, alerts, rollout/canary, rollback — unprompted | |
| 9 | **Cost** | One $/month figure, the dominant term, and the biggest lever | |
| 10 | **Communication** | Narrated continuously; structured; no silences > 15 s; diagram legible | |
| 11 | **Drove the conversation** | Proposed the plan and the deep dives; didn't wait to be asked | |
| 12 | **Handled challenge** | Conceded fast when wrong, patched the design on the board, moved on | |

**Total /48.**

| Total | Read as |
|---|---|
| < 24 | Not ready — go back to fundamentals for this problem class |
| 24–31 | Mid-level. Correct but reactive |
| 32–39 | **Senior.** Drove it, covered ops and cost |
| 40+ | Staff-ish. Framed the problem, not just solved it |

The three lines that most often separate 2 from 3 in real interviews: **#7 failure**, **#9 cost**,
and **#11 drove it**. Check those first when your total is stuck.

## After scoring — the only three questions that matter

1. **What did the reference have that I didn't?** (→ study list)
2. **What did I have that was wrong or unjustified?** (→ the more dangerous gap)
3. **What would I do differently in the first five minutes next time?**

Write the answers in your drill log. If a miss appears in three consecutive logs, it isn't a
knowledge gap — it's a habit, and it needs a rule ("always say the SLO before the cost").

## Track variants

**Frontend** — replace #2 with rendering-strategy justification, #3 with component API + state
split, #9 with performance budgets (LCP/INP/CLS + bundle).

**Data** — #2 becomes volume/velocity/freshness; #7 becomes late data, backfill and restatement;
#8 becomes data-quality checks and lineage.

**ML** — add: *framed the ML task and named offline + online metrics + a guardrail*; *addressed
training–serving skew*; *specified the evaluation and rollout plan*; *gave $/prediction*.

## Interviewer questions to ask yourself while reviewing the recording

- Could someone build a v1 from what I said?
- Did I say a single number, or only adjectives?
- Did I mention failure before minute 40?
- Would I have hired me?
