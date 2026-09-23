---
title: System design prep
type: index
track: universal
status: drafted
updated: 2026-09-23
tags: [index, entry-point]
---

# System design prep

A staff/principal-level system design corpus, written to be **drilled**. Obsidian vault and git
repo; every page is plain Markdown with Mermaid diagrams that render on GitHub without a plugin.

**Audience: engineers who already have the fundamentals.** The value here is trade-offs under
constraints, failure modes, quantitative reasoning, and where experienced engineers get the choice
wrong. There are no definitions of what a load balancer is.

## Start here

| I want to… | Go to |
|---|---|
| **Run a design round tomorrow** | [interview-prep/00-interview-playbook.md](interview-prep/00-interview-playbook.md) — how to spend the 45 minutes and what is scored |
| **Know the numbers cold** | [interview-prep/01-numbers.md](interview-prep/01-numbers.md) — latency ladder, capacity arithmetic, cost anchors |
| **Study on a schedule** | [interview-prep/07-drills/8-week-plan.md](interview-prep/07-drills/8-week-plan.md) |
| **See the whole curriculum** | [interview-prep/README.md](interview-prep/README.md) |
| **See every file, legacy notes included** | [INDEX.md](INDEX.md) |
| **Know where work stopped** | [STATUS.md](STATUS.md) |

## What is in here

| Layer | Pages | What it answers |
|---|---:|---|
| [fundamentals/](interview-prep/fundamentals/README.md) | 25 | How does this mechanism actually work, what does it cost, how does it break? Consensus, isolation levels, LSM vs B-tree, watermarks, tail latency, metastable failure |
| [patterns/](interview-prep/patterns/README.md) | 10 | Which shape do I assemble, and when does it earn its complexity? Outbox, saga, cells, fan-out, expand–contract, backfill |
| [comparisons/](interview-prep/comparisons/README.md) | 5 | Which technology do I pick, and what do I regret? Each page commits to a recommendation rather than listing features |
| [03–06 cases](interview-prep/03-backend-cases/README.md) | 26 | Worked designs across [backend](interview-prep/03-backend-cases/README.md), [frontend](interview-prep/04-frontend-cases/README.md), [data](interview-prep/05-data-cases/README.md) and [ML/GenAI](interview-prep/06-ml-cases/README.md) |
| [07-drills/](interview-prep/07-drills/README.md) | 4 | Question bank, flashcards, an 8-week plan, and a rubric to score yourself against |
| [08-reference/](interview-prep/08-reference/README.md) | 2 | Glossary and the technology-selection table |
| [09-company-styles/](interview-prep/09-company-styles/README.md) | 5 | What Amazon, Meta, Google, Microsoft/Apple/Netflix and startups weight differently |
| [10-resources/](interview-prep/10-resources/README.md) | 7 | The primary sources this corpus cites, books, repos, blogs, newsletters, mocks |
| [11-behavioural/](interview-prep/11-behavioural/README.md) | 3 | The non-technical round: question bank, rubric, and a story inventory only you can fill |
| [02-primitives/](interview-prep/02-primitives/README.md) | 12 | The older bundled notes, being split into `fundamentals/`. Kept until every topic they carry has a successor page |

Every page carries two extras that most prep material omits: **`## On AWS and Azure`** — the
managed service that already does this and the knob that bites — and **`## In an LLM deployment`**,
because the same mechanism shows up differently in front of a GPU.

Background concept notes from before the restructure live in `basic/prep/` and
`data engineering/`, indexed in [INDEX.md](INDEX.md). They are kept, not maintained.

## How to use it

**Never read a case file straight through.** Cover everything below *Requirements*, design it
yourself on paper for 30 minutes, then diff against the file. The diff is your study list — the
page you agreed with taught you nothing.

- Score the attempt with [07-drills/self-scoring-rubric.md](interview-prep/07-drills/self-scoring-rubric.md).
- Log what you missed in [Track your learning.md](Track%20your%20learning.md).
- Fundamentals, patterns and comparisons are reference, not reading. Reach for one when a case
  makes you hesitate, not before.

## Contributing to it

| Before you… | Read |
|---|---|
| Create any file | [interview-prep/topics/manifest.md](interview-prep/topics/manifest.md) — one topic, one canonical filename. Not listed? Add it there first |
| Write a page | [interview-prep/CONVENTIONS.md](interview-prep/CONVENTIONS.md) and the section contract in [CLAUDE.md](CLAUDE.md) |
| Draw anything | [interview-prep/diagrams/components.md](interview-prep/diagrams/components.md) — the shared Mermaid vocabulary. Do not invent a second visual language |
| Copy a skeleton | [interview-prep/_templates/](interview-prep/_templates/) |

Two rules that are load-bearing rather than stylistic:

- **Wikilinks are disabled in this vault.** Markdown links only, relative, with spaces escaped as
  `%20` and parentheses as `%28` `%29`. Legacy `[[...]]` links stay; add no more. In Obsidian:
  *Settings → Files & Links → Use Wikilinks* **off**.
- **Numbers get a source, or the label "order of magnitude, verify before quoting".** Cloud prices
  here are anchors for interview arithmetic, not quotes.

Design decisions are recorded as ADRs in [docs/adr/](docs/adr/); the reasoning behind each batch is
in [docs/WORKLOG.md](docs/WORKLOG.md).

## Credit

Started from [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer),
which is still the best free starting point and is where the `basic/prep/` notes come from.
Everything under `interview-prep/` is written against the primary sources listed in
[10-resources/primary-sources.md](interview-prep/10-resources/primary-sources.md).

Questions, corrections, or a number you can show is wrong — open an issue.

## Referenced by

- [Repo index](INDEX.md)
