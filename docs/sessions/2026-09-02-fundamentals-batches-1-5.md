---
title: Session record — fundamentals batches 1–5
type: session
date: 2026-09-02
branch: docs/fundamentals-batch-1 … batch-5
status: complete
updated: 2026-09-02
tags: [session, fundamentals, execution]
---

# Session record — 2026-09-02 (second session)

What happened, in order, with the decisions and the evidence — including the parts that went
wrong. The worklog carries the durable trade-offs per batch; this file carries the narrative and
the mistakes.

The [previous session](2026-09-02-staff-restructure-and-skill.md) produced the plan and stopped.
This one executed it: **0 → 25 pages**, five branches, six pull requests, none merged.

---

## Arc

| Phase | Outcome |
|---|---|
| 1. Unblock | D1–D4 answered, recorded as [ADR-0001](../adr/0001-split-primitives-into-atomic-fundamentals.md) |
| 2. Batch 1 — consistency | 5 pages; the section contract survived first contact |
| 3. Batch 2 — replication | 5 pages; the split mechanic proved repeatable |
| 4. Batch 3 — storage + caching | 5 pages; first batch splitting **two** source files |
| 5. Batch 4 — messaging | 5 pages; first time a page was pulled forward out of batch order |
| 6. Batch 5 — reliability | 5 pages; first batch that was mostly **new**, not split |

25 of 123 topics written. Fundamentals 25 of 47. Patterns and comparisons: not started, by design.

## Phase 1 — the decision that was blocking everything

The previous session ended with four open questions and written recommendations. All four were
approved, with **one deviation**: scope went to **all 123 topics**, not the recommended 63 P0. The
recommendation still stands in the manifest, and the batch order still runs P0 first, so stopping
early remains available at any batch boundary — that is why the deviation was cheap to accept.

Recorded as ADR-0001 rather than a worklog line, because it is a decision with rejected
alternatives and accepted costs, and someone will ask "why 47 files instead of 12" in a year.

## Phases 2–6 — the batches

Each batch: research 2–3 independent sources → write 5 pages → wire the indexes → run the three
scripts → commit → PR. Roughly the same shape every time, which is the point — the process became
boring by batch 3, which is when it started producing pages faster than it produced decisions.

**What each batch contributed beyond its pages:**

- **Batch 1** proved the contract. Five pages exercised every section, so a bad contract would have
  shown up on batch 1 rather than batch 9. It didn't.
- **Batch 2** proved the split mechanic — banner the source, keep it until its last unique topic
  lands, update the manifest row to ✅.
- **Batch 3** was the first to split two source files at once, which turned out to be no harder.
- **Batch 4** broke batch order deliberately: `idempotency` belongs to the transactions primitive
  but was written with the messaging pages, because `delivery-semantics` is incoherent without it.
  Splitting them across branches would have shipped a dangling argument.
- **Batch 5** was the first mostly-new batch — three pages with no source text — and was written as
  **one interlocking argument** rather than five essays: the knee, the fan-out that drags you into
  it, the retries that multiply past it, the shedding that prevents it, the metastability that
  follows without it.

**The rule that held all five batches:** every page carries a *cited production incident*, and no
incident is reused across batches. That constraint did more for quality than any style rule — it
forced real research per page and produced the failure-mode sections that make the set worth
reading.

## What went wrong

Five things, all recorded because the next session will otherwise rediscover them.

**1. `gen_backlinks.py` writes inside code fences.** It matches `## Referenced by` and `## Sources`
textually, so the section-contract *examples* in `CLAUDE.md` and `CONVENTIONS.md` — fenced blocks
showing the required headings — received generated backlink lists injected into them. Caught by
reading the diff, not by any check.

Fixed **in this repo** by converting both contract examples from fenced snippets to tables, and
documenting the trap. The script itself is still wrong; that is filed against the skill in
STATUS.md. Worth noting the shape of the mistake: a tool that edits documentation broke the
documentation *about* the tool.

**2. The recorded link count was stale by four.** The batch-5 commit quoted 1485 links, measured
before a final handoff edit added four more. Corrected in a follow-up commit to 1489. Minor, but
the count is the "expected baseline" the next session diffs against, so a stale one is worse than
none — it makes a real regression look like drift.

**3. A scripted manifest edit replaced only the first occurrence.** The batch-4 update used a
`replace(..., 1)` for the action column and silently left three of four rows saying `split ←`
instead of `written ←`. Caught by grepping the file afterwards. **Lesson: verify scripted edits by
re-reading the result, not by trusting the replacement count.**

**4. Windows console encoding.** Printing a ✅ from a Python one-liner raises `UnicodeEncodeError`
under cp1252 — the *file write* succeeded and only the console print failed, which is confusing for
about thirty seconds. Prefix with `PYTHONIOENCODING=utf-8`, or don't print the emoji.

**5. Six pull requests, none merged.** `gh pr merge` is blocked by the permission classifier in
this environment, so every branch is stacked on the one before it and all six PRs are open. This is
the largest open risk in the repo right now: the stack must be merged **oldest first** or GitHub's
automatic retargeting produces a confusing diff.

## Evidence

Final state, measured from the repository root:

```
$ python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .
checked 1511 relative links; broken: 4
  BROKEN markdown files\md_blacklinks.md:30 -> {rel_path}
  BROKEN markdown files\md_blacklinks.md:93 -> path/to/file.md
  BROKEN markdown files\md_blacklinks.md:121 -> path/to/Common-Principles.md
  BROKEN markdown files\md_blacklinks.md:121 -> path/to/Another-Note.md

$ python ~/.claude/skills/staff-technical-docs/scripts/gen_backlinks.py .   # second run
208 files scanned, 709 inbound links mapped, 0 changed
```

Baseline at the start of the session was 501 links; the final figure includes this session record and the docs pass that added it. The 4 breaks are `{rel_path}` template
placeholders inside a script's own documentation — pre-existing, unchanged, and expected forever.

Also fixed along the way: four links in `main.md` using raw spaces and backslashes
(`basic\prep\SQL or NoSQL.md`) that resolved locally and broke on GitHub. Percent-encoded — the
files were **not** renamed, per the standing rule that renaming is what broke the links originally.

All 25 fundamentals pages carry two Mermaid diagram types, verified by count rather than by
assertion.

## Branches and PRs

| PR | Branch | Contents |
|---|---|---|
| #1 | `docs/staff-level-restructure` | The plan: manifest, diagram library, conventions |
| #2 | `docs/fundamentals-batch-1` | Consistency cluster |
| #3 | `docs/fundamentals-batch-2` | Replication cluster |
| #4 | `docs/fundamentals-batch-3` | Storage engines and caching |
| #5 | `docs/fundamentals-batch-4` | Messaging and delivery |
| #6 | `docs/fundamentals-batch-5` | Reliability under overload |

Merge oldest first: `gh pr merge 1 --squash --delete-branch`, then 2–6.

## What the next session inherits

- A working, boring process — five pages per branch, one incident per page, three scripts, one PR.
- Batch 6, which is the first to **create a folder** (`patterns/`) and therefore needs a folder
  README plus rows in `INDEX.md` and `interview-prep/README.md`.
- Seven of twelve primitive files partly split, all banner-marked, none deleted. The deletion rule
  has held: a source file dies only when empty of unique topics.
- One unreviewed assumption, unchanged since the last session: **no human has read these pages for
  depth calibration.** 25 pages now carry the same style bet.

## See also

- [../WORKLOG.md](../WORKLOG.md) — per-batch reasoning and trade-offs
- [../NEXT-SESSION.md](../NEXT-SESSION.md) — what to do first
- [../../STATUS.md](../../STATUS.md) — stop point and traps
- [../adr/0001-split-primitives-into-atomic-fundamentals.md](../adr/0001-split-primitives-into-atomic-fundamentals.md) — the decision this session executed
- [2026-09-02-staff-restructure-and-skill.md](2026-09-02-staff-restructure-and-skill.md) — the session that produced the plan

## Referenced by

- [Docs index](../README.md)
- [STATUS](../../STATUS.md)
