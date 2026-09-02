---
title: Worklog
type: worklog
status: current
updated: 2026-09-02
tags: [history, decisions]
---

# Worklog

Dated entries. Newest first. Each entry records **what changed, how, why, and the trade-off** —
the reasoning is the part that isn't recoverable from the diff.

---

## 2026-09-02 — Staff-level restructure groundwork + `staff-technical-docs` skill

Branch: `docs/staff-level-restructure` (not merged)

### What

Two threads, one feeding the other.

**1. Built the interview-prep curriculum, then rebuilt its plan for a staff audience.**
75 files under `interview-prep/` (~10,400 lines): playbook, numbers, 12 primitives, 26 worked
cases across backend/frontend/data/ML, drills, reference, company styles, resources. Then —
after feedback that it read as prep material rather than staff-level content — produced
`interview-prep/topics/manifest.md`: 123 canonical topics with aliases, tiers and split
provenance, plus `diagrams/components.md` (shared Mermaid vocabulary) and a rewritten `CLAUDE.md`
carrying the staff section contract and the ADR anti-patterns.

**2. Extracted the method into a reusable skill.** `~/.claude/skills/staff-technical-docs/` —
SKILL.md, three references, two asset packs, three verification scripts, an eval set. Benchmarked
against a no-skill baseline across 3 cases, 6 parallel runs.

### How

- Cloned 10 upstream reference repos into a gitignored `vendor/` (~100 MB) rather than committing
  other people's git history; a `fetch-references.sh` refreshes them.
- Mapped 243 local books to specific chapters per topic, so "read DDIA" became "read ch. 5–9".
- Wrote link-verification, backlink-generation and lint scripts, then bundled them into the skill
  because the same link checker had been written inline three times in one session.
- Ran the skill against a no-skill baseline: 3 evals × 2 configurations, 25 assertions, graded
  mechanically where possible and by evidence where not.

### Results

| | with skill | baseline |
|---|---|---|
| Assertion pass rate | 100% (25/25) | 76% (19/25) |
| Tokens | 2.1× baseline | — |
| Wall-clock | 2.3× baseline | — |

### Trade-offs found — the part worth keeping

**Bundled topic pages vs atomic pages.** The existing `02-primitives/` had 12 files each carrying
3–6 staff-depth topics; `consistency-and-consensus.md` alone covered CAP, isolation, Raft, leases,
clocks and CRDTs. A page covering six topics cannot go deep on any — they compete for the same
space. Depth is a *structural* fix (split into ~47 pages), not a "write more words" fix. This was
the single most valuable insight of the session and it generalises to any doc set that feels thin.

**Renaming vs percent-encoding a broken link.** The largest measured behavioural difference. The
baseline fixed links whose targets contained spaces and parens by *renaming the files* — for a
user whose stated problem was "I moved files around and links broke". Both configurations reached
zero broken links; only one avoided recreating the original problem. Encoding is local and
reversible; renaming is a migration wearing a tidy-up's clothes.

**Manifest-first vs write-first.** A manifest costs a review cycle before any prose exists. It
buys permanent duplicate prevention via an aliases column. Worth it above ~10 pages; overhead
below that.

**Completeness bar vs word count.** Word caps produce either padding or truncation. "Every section
carries something a principal engineer didn't already know" is unbounded but checkable, and it
lets case studies run long without licensing filler.

**Skill overhead is real.** 2.1× tokens. Justified on a multi-file set; on a single-page rewrite
the measured gains were mostly stylistic. The skill now says so and tells the reader to skip the
machinery for one-page jobs — a skill that doesn't know when to stand down gets switched off.

**Semantic duplicates cannot be scripted.** `lint_docs.py` catches `caching.md` vs
`cache-strategies.md` and is structurally blind to `rate-limiting.md` vs `throttling.md`. It was
printing "no duplicate topics" over a vault containing exactly that. A clean report that
overstates its scope is worse than no report; the script now states what it did not check.

**Verify the verifier.** `gen_backlinks.py` had a Windows path-separator bug: it printed
"262 links mapped, 0 changed" and exited 0 while writing nothing — indistinguishable from success.
I ran it on this repo and read that as working. An eval agent caught it. Scripts that report
success by default are worse than scripts that crash.

**You cannot credibly grade your own skill.** I wrote both the skill and the assertions that
scored it; assertions derived from the skill's own section contract structurally favour it. The
100% is a ceiling artefact, not a triumph. 11 of 25 assertions passed in *both* configurations and
measured nothing. v2 of the eval set drops them and adds harder ones.

**Eval prompts leak instructions.** Eval-0's prompt said "figure out the topic list before you
start writing" — handing the baseline the skill's central mechanism. The baseline still lost, but
the comparison was unfair in my favour. Fixed in v2.

### Verification

```
relative links across repo:  478 checked, 4 broken (all template placeholders in
                             markdown files/md_blacklinks.md — pre-existing, not real links)
frontmatter:                 all 77 interview-prep files complete
longest file:                244 lines (ceiling 500)
scripts:                     compile clean; gen_backlinks regression-tested across
                             forward-slash, backslash and relative roots
```

Also fixed two pre-existing bugs found in passing: 5 links broken by unescaped parentheses in
`INDEX.md` and 3 case files, and 2 image links in `how we've scaled Dropbox.md` pointing at moved
assets.

### Skill iteration, after the benchmark

Every change below traces to something the runs surfaced, not to a hunch:

| Change | Triggered by |
|---|---|
| `gen_backlinks.py` path canonicalisation | Silent no-op on Windows; regression-tested across forward-slash, backslash and relative roots |
| `lint_docs.py` now prints what it did **not** check | It was reporting "no duplicate topics" over a vault that had one |
| New **"Fix the link, not the filename"** section, promoted out of a bullet | The largest measured behavioural difference between configurations |
| New **"When not to use this"** | 2.1× token cost; on a single page the gains were mostly stylistic. A skill that can't stand down gets switched off |
| Manifest section: semantic duplicates can't be scripted | The eval-2 trap didn't trap — both configs caught it by reading, neither by tooling |
| Eval set v2 | Removed the prompt leak, dropped 11 non-discriminating assertions, added harder ones plus a set-level eval |

Iteration-1 caveats are recorded inside `evals/evals.json` rather than in a message, including
that the skill's author also wrote its assertions.

### Open

`D1–D4` in `interview-prep/topics/manifest.md` §7 — the structural decisions (rename
`02-primitives/` → `fundamentals/` and split; add `patterns/` and `comparisons/`; P0-only scope;
rewrite cases in place). Recommendations are recorded; none executed. Writing the 63 P0 pages is
the next substantial block of work and needs a scope decision first.

Also open: no PR; eval v2 written but never run; eval-3's fixture unbuilt; and **no human has
reviewed the iteration-1 outputs** — the skill was graded by its author against that author's
assertions, which is the weakest evidence produced this session.

### See also

- [NEXT-SESSION.md](NEXT-SESSION.md) — the handoff: blocking decision, first commands, batch 1
- [sessions/2026-09-02-staff-restructure-and-skill.md](sessions/2026-09-02-staff-restructure-and-skill.md) — the full narrative, including what went wrong
- [../STATUS.md](../STATUS.md) — stop point and traps
