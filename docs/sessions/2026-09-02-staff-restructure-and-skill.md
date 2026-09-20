---
title: Session record — staff restructure groundwork and the docs skill
type: session
date: 2026-09-02
branch: docs/staff-level-restructure
status: complete
updated: 2026-09-02
tags: [session, skill, benchmark]
---

# Session record — 2026-09-02

What happened, in order, with the decisions and the evidence. The worklog carries the durable
trade-offs; this file carries the narrative, including the parts that went wrong.

---

## Arc

Four phases, each triggered by the previous one's shortcoming.

1. **Build the prep curriculum** — 75 files, four tracks, drills, resources.
2. **Reframe for a staff audience** — the set read as prep material, not staff material. Produced
   a manifest and a section contract instead of more prose.
3. **Extract the method as a skill** — the discipline was reusable; the repo was one instance.
4. **Benchmark the skill against no skill** — and find that most of the assumed value wasn't there.

## Phase 1 — the curriculum

Built `interview-prep/`: playbook, numbers, 12 primitives, 26 worked cases (backend, frontend,
data, ML/GenAI), drills, reference, company styles, resources. ~10,400 lines.

Sourcing decisions worth remembering:
- Cloned 10 upstream repos into a **gitignored** `vendor/` rather than committing ~100 MB of other
  people's git history. `fetch-references.sh` refreshes them.
- Inventoried 243 local books and mapped them to specific chapters per topic, so guidance became
  "DDIA ch. 5–9" rather than "read DDIA".
- Web-verified the 2026-specific material: rubric changes, latency numbers, PD disaggregation,
  Iceberg streaming, INP replacing FID.

## Phase 2 — the reframe

Feedback: this is a glossary, not staff-level content; restructure rather than lengthen.

That turned out to be the sharpest observation of the session. Inspection showed `02-primitives/`
had **12 files each carrying 3–6 staff-depth topics** — `consistency-and-consensus.md` alone
covered CAP, isolation levels, Raft, leases, clocks and CRDTs. Six topics competing for one page
cannot each have their own internals, arithmetic and failure modes.

Produced instead of prose:
- `topics/manifest.md` — 123 canonical topics, aliases, tiers, split provenance, batch order, and
  four open decisions with recommendations
- `diagrams/components.md` — 11 reusable Mermaid snippets, fixed palette, dotted-means-async
- Rewritten `CLAUDE.md` — section contract, completeness bar, research rules, ADR anti-patterns

Deliberately **not** done: renaming or moving any existing file. Inbound links are relative.

## Phase 3 — the skill

`~/.claude/skills/staff-technical-docs/` — SKILL.md, 3 references, 2 asset packs, 3 scripts,
an eval set.

The scripts were bundled on direct evidence: the same link checker had been written inline three
times in this one session. A later addition, the **prompt pack**, emits saved thinking prompts
(make the reader reason) and working prompts (drive an assistant over the set later) — because a
prompt that lives only in a transcript is gone by the next session.

## Phase 4 — the benchmark

3 evals × 2 configurations = 6 parallel subagent runs, 25 assertions.

| Eval | with skill | baseline |
|---|---|---|
| new-doc-set-from-scratch | 8/8 | 5/8 |
| deepen-shallow-page | 9/9 | 7/9 |
| vault-hygiene-and-duplicates | 8/8 | 7/8 |
| **overall** | **100%** | **76%** |

Cost: **2.1× tokens, 2.3× wall-clock.**

### What the benchmark actually proved

Less than the headline. Recorded here because the number will look better than it is:

- **11 of 25 assertions passed in both configurations.** Presence checks — found the broken link,
  found the duplicate, saved a report — measure model capability, not skill contribution.
- **Eval-0's prompt leaked the mechanism.** It said "figure out the topic list before you start
  writing", handing the baseline the skill's central move. The baseline still lost 3 points, which
  is the one result that survives the flaw.
- **The author graded his own work.** Assertions derived from the skill's own section contract
  structurally favour it. Not correctable from the inside.
- **100% is a ceiling**, so the set can no longer detect improvement.

### The one finding that held up

The baselines were strong — they planned before writing, marked unverified numbers, wrote their
own link checkers. The durable difference was behavioural:

> The baseline fixed links whose targets contained spaces and parentheses **by renaming the
> files** — for a user whose opening complaint was *"I moved files around and links broke."*
> Both configurations reached zero broken links. Only one avoided recreating the original problem.

That became a promoted section in the skill: *fix the link, not the filename.*

## Bugs found and fixed

| Bug | How it surfaced | Severity |
|---|---|---|
| `gen_backlinks.py` silent no-op on Windows — printed "262 mapped, 0 changed", exit 0, wrote nothing | An eval agent noticed the numbers didn't reconcile | **High** — I had run it on this repo and read the output as success |
| `lint_docs.py` printed "no duplicate topics" over a vault containing a semantic duplicate | An eval agent flagged the false all-clear | Medium — a clean report that overstates scope is worse than none |
| Grader counted `README.md` and prompt files as topic pages | Investigating a failure that appeared in both configs | Low — produced a false negative |
| 5 links broken by unescaped `(` in `INDEX.md` and 3 case files | `check_links.py` on the real repo | Medium — self-inflicted, caught by the tool |
| 2 image links pointing at moved assets | Same | Low — pre-existing |

## Corrections made to my own work

- Wrote `STATUS.md` and `docs/WORKLOG.md` claiming completion while the WORKLOG entry stopped
  before the skill fixes landed and no handoff document existed. Rewritten this session.
- A commit message claimed 480 links checked; the real number was 485 (two later edits added
  links). Amended on the unpushed tip rather than left wrong.

## Decisions taken

| Decision | Choice | Reason |
|---|---|---|
| Parallel `fundamentals/` tree vs modify existing pages | Modify existing | User direction; also avoids a duplicate set |
| Rename legacy files vs add index | Add index | Relative links break silently |
| Commit vendored repos | No — gitignore | ~100 MB of foreign history |
| Word limit on pages | None — completeness bar | Caps produce padding or truncation |
| Grade the skill myself | Yes, with the bias stated | No independent grader available; concealment would be worse |
| Execute D1–D4 unasked | **No** | 63 pages is a scope and cost decision, not a technical one |

## Left open

- D1–D4 unanswered → the 63 P0 pages unwritten
- No PR; branch 2 commits ahead of `main`
- Eval v2 written, never run; eval-3 fixture unbuilt
- **No human reviewed the iteration-1 outputs** — `review.html` still opens standalone

## Files

`interview-prep/**` (75) · `INDEX.md` · `CLAUDE.md` · `STATUS.md` · `docs/WORKLOG.md` ·
`docs/NEXT-SESSION.md` · `docs/sessions/2026-09-02-*.md` ·
`~/.claude/skills/staff-technical-docs/**` (13) ·
`~/.claude/skills/staff-technical-docs-workspace/**` (benchmark, graded runs, review.html)

## Referenced by

- [Worklog](../WORKLOG.md)
