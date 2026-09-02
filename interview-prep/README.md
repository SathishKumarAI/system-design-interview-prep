---
title: Interview prep index
type: index
track: universal
status: drafted
updated: 2026-09-02
tags: [index]
---

# Interview Prep — System Design (full curriculum)

One place for the whole design round: backend, frontend, data, ML/GenAI. Built to be
**drilled**, not read once. Every case file has the same skeleton so you build one
muscle instead of forty facts.

Notes in `../basic/prep/` are the raw concept notes (mostly from system-design-primer).
This folder is the **interview layer** on top: framework, numbers, worked cases, drills.

## Where to look

| Question | File |
|---|---|
| How do I run the 45 minutes? What is scored? | [00-interview-playbook.md](00-interview-playbook.md) |
| How many servers / how much storage / what does it cost? | [01-numbers.md](01-numbers.md) |
| How does this mechanism actually work, what does it cost, how does it break? | [fundamentals/](fundamentals/README.md) |
| What is the building block and when do I reach for it? (fast revision layer) | [02-primitives/](02-primitives/README.md) |
| Worked backend designs (feed, chat, payments, …) | [03-backend-cases/](03-backend-cases/README.md) |
| Worked frontend designs (editor, feed, dashboard) | [04-frontend-cases/](04-frontend-cases/README.md) |
| Worked data-platform designs (lakehouse, CDC, realtime) | [05-data-cases/](05-data-cases/README.md) |
| Worked ML / GenAI designs (recsys, RAG, LLM serving) | [06-ml-cases/](06-ml-cases/README.md) |
| What do I practise this week? How do I score myself? | [07-drills/](07-drills/README.md) |
| Term I forgot / which tech do I pick | [08-reference/](08-reference/README.md) |
| What does Amazon / Meta / Google weight differently? | [09-company-styles/](09-company-styles/README.md) |
| Books I own, repos, newsletters, blogs, mocks | [10-resources/](10-resources/README.md) |
| How is every file here written? | [CONVENTIONS.md](CONVENTIONS.md) |
| Templates to copy when adding a note | [_templates/](_templates/) |

## The one rule

**A design round is not a knowledge test. It is a decision-making test under ambiguity.**
Interviewers score whether you drove the conversation, named trade-offs out loud, and
knew what breaks. Naming Kafka gets you nothing; saying *why Kafka over SQS here, and
what that costs you* gets you everything.

2026 rubrics add two lines that used to be bonus points and are now scored explicitly:
**operational maturity** (monitoring, failure modes, rollout) and **cost**. Both are
covered as first-class sections in every case file here.

## How each case file is structured

Same eight headings everywhere. Learn the shape once; it becomes your speaking order.

1. **Clarify** — questions to ask, and the answers you assume if the interviewer waves you on
2. **Requirements** — functional, non-functional, explicit non-goals
3. **Estimates** — traffic, storage, bandwidth, cost. Numbers, not adjectives
4. **API / contract** — the interface before the boxes
5. **Data model** — tables/keys/partitioning; this is where most designs are won or lost
6. **Architecture** — high level, then the one or two deep dives that matter
7. **Scale & failure** — bottleneck, hotspot, what breaks at 10x, what happens when X dies
8. **Ops & cost** — SLOs, metrics, rollout, dollar figure, and what you'd cut first

## How to use this repo

- **Whole-repo map (including the older notes):** [../INDEX.md](../INDEX.md)
- **Week-by-week plan:** [07-drills/8-week-plan.md](07-drills/8-week-plan.md)
- **Never read a case file passively.** Cover everything below "Requirements", design it
  yourself on paper for 30 minutes, *then* diff against the file. The diff is the learning.
- Log the diff in [../Track your learning.md](../Track%20your%20learning.md) — what you missed
  is your actual study list.
- Score yourself with [07-drills/self-scoring-rubric.md](07-drills/self-scoring-rubric.md).

## Status of the numbers here

Latency and hardware numbers are 2026 figures (see sources in `01-numbers.md`). Cloud
prices are **order-of-magnitude anchors for interview arithmetic**, not quotes — check
the vendor calculator before putting any of them in a real design doc.

## Referenced by

- [CLAUDE.md — system-design-prep](../CLAUDE.md)
- [Next session — start here](../docs/NEXT-SESSION.md)
- [Repo index](../INDEX.md)
- [System Design Interview Preparation](../README.md)
