---
title: 8-week study plan
type: drill
track: universal
difficulty: core
status: drafted
updated: 2026-09-02
tags: [plan, schedule]
---

# 8-week plan

Assumes ~6–8 hours/week. Compress to 4 weeks by doubling the pace; stretch to 12 by adding a
re-drill week after weeks 4 and 8. **Every week ends with at least two timed drills** — that is
the non-negotiable part; the reading is support.

| Week | Read | Drill (timed, out loud) | Deliverable |
|---|---|---|---|
| **1 — Framework + numbers** | [00-interview-playbook.md](../00-interview-playbook.md), [01-numbers.md](../01-numbers.md) | url-shortener, rate-limiter | Numbers memorised (test yourself blind); one recorded 40-min run |
| **2 — Storage + caching** | primitives: storage, replication-and-partitioning, caching | news-feed, search-typeahead | Can defend a partition key for any entity in 60 seconds |
| **3 — Async + consistency** | primitives: messaging-and-streams, consistency-and-consensus, transactions-and-idempotency | chat-messaging, notification-system | Can explain exactly-once *effects* without notes |
| **4 — Reliability + ops + cost** | primitives: reliability-patterns, observability-and-delivery, cost-engineering | object-storage-sync, video-streaming | Every drill now ends with failure + cost sections, unprompted |
| **5 — Hard backend** | Re-read weak primitives from your drill logs | ride-hailing, payments-ledger, metrics-monitoring | Re-drill week 1–2 problems; scores must be higher |
| **6 — Your track** | [ml-playbook](../06-ml-cases/ml-playbook.md) / [data-playbook](../05-data-cases/data-playbook.md) / [frontend-playbook](../04-frontend-cases/frontend-playbook.md) | 3 cases from your track | One full case in your track scored ≥ 3 on every rubric line |
| **7 — GenAI + company style** | [rag-assistant](../06-ml-cases/rag-assistant.md), [llm-serving-platform](../06-ml-cases/llm-serving-platform.md), [09-company-styles](../09-company-styles/README.md) | rag-assistant, feed-ranking, one repeat | Can talk cost-per-answer and evaluation fluently |
| **8 — Mocks + polish** | Skim everything; re-read your drill logs | 4+ mocks, mixed and unseen | Two clean 45-min runs, recorded, scored ≥ 3 everywhere |

## Daily shape (about an hour)

```
10 min  Flashcards (numbers, trade-off tables) — spaced repetition
30 min  One timed drill segment (a full case takes two sessions)
15 min  Diff against the reference + log it
 5 min  Update your study list
```

## Track-specific week 6 substitutions

| Your track | Cases |
|---|---|
| Backend / infra | ride-hailing, metrics-monitoring, payments-ledger |
| ML / AI (your default given your background) | recommender, feed-ranking, feature-store |
| Data engineering | clickstream-lakehouse, cdc-pipeline, realtime-analytics |
| Frontend | collaborative-editor, infinite-feed, realtime-dashboard |
| Full-stack | one from each of backend, frontend, ML |

## Cut-down: one week before an interview

| Day | Do |
|---|---|
| 1 | [00-interview-playbook.md](../00-interview-playbook.md) + [01-numbers.md](../01-numbers.md); memorise the numbers block |
| 2 | Drill the case closest to the company's product; diff |
| 3 | Skim all 12 primitives; write the trade-off table from memory |
| 4 | Two timed drills, recorded |
| 5 | [09-company-styles](../09-company-styles/README.md) for that company + read their engineering blog |
| 6 | One mock with a human if at all possible |
| 7 | Rest. Re-read your own drill logs, nothing new |

**Do not learn a new primitive the day before.** Re-reading your own diffs beats new material,
every time.

## Progress tracking

Use frontmatter `status` on case files: `seed → drafted → drilled → mastered`. Search
`status: drilled` in Obsidian to get your revision list. Log every session to
[../_templates/drill-log-template.md](../_templates/drill-log-template.md), and log the week's
learning in [../../Track your learning.md](../../Track%20your%20learning.md).
