---
title: Docs index
type: index
status: current
updated: 2026-09-02
tags: [index]
---

# docs/

Reasoning and history. Code holds the reasons that fit in a comment; this holds the rest.

## Where to look

| Question | File |
|---|---|
| **I'm resuming work — what do I do first?** | [NEXT-SESSION.md](NEXT-SESSION.md) |
| Why was a past change made? What trade-off did we accept? | [WORKLOG.md](WORKLOG.md) |
| What happened in a given session, including the dead ends? | [sessions/](sessions/) |
| Where did work stop, and what will bite me? | [../STATUS.md](../STATUS.md) |
| An idea we are keeping but not scheduling | [BACKLOG.md](BACKLOG.md) |
| What is the plan for the topic set? | [../interview-prep/topics/manifest.md](../interview-prep/topics/manifest.md) |
| Why is the folder structure the way it is? | [adr/0001-split-primitives-into-atomic-fundamentals.md](adr/0001-split-primitives-into-atomic-fundamentals.md) |
| A new architecture decision | `adr/NNNN-…`; template at [../interview-prep/_templates/adr-template.md](../interview-prep/_templates/adr-template.md) |

## Session records

| Date | Session | What it produced |
|---|---|---|
| 2026-09-02 | [staff restructure groundwork and the docs skill](sessions/2026-09-02-staff-restructure-and-skill.md) | The 75-file prep set, the manifest, the diagram library, and the `staff-technical-docs` skill + benchmark |
| 2026-09-02 | [fundamentals batches 1–5](sessions/2026-09-02-fundamentals-batches-1-5.md) | Executed the plan: **25 pages**, five branches, six stacked PRs; found the `gen_backlinks.py` code-fence bug |

## The three-document split, and why it isn't redundant

Each answers a different question, and collapsing them makes all three worse:

| Document | Question | Rewritten |
|---|---|---|
| `STATUS.md` | Where did we stop? | Every time work stops — always current, never historical |
| `NEXT-SESSION.md` | What do I do first? | Every time work stops — actionable, with commands |
| `WORKLOG.md` | Why is it like this? | Appended, never edited — the reasoning a diff can't recover |
| `sessions/*.md` | What actually happened? | One per session, immutable after writing |

A worklog that gets edited stops being a record. A status file that accumulates history stops
being readable at the moment you most need it.

## Conventions

- Session records: `sessions/YYYY-MM-DD-short-slug.md`
- ADRs: `adr/NNNN-short-title.md`, append-only, superseded rather than edited — see the
  anti-patterns table in [../CLAUDE.md](../CLAUDE.md)
- Dates absolute, never "last week"
- Every claim of completion carries the command output that proves it

## Referenced by

- [Repo index](../INDEX.md)
