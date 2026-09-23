---
title: Next session — start here
type: handoff
status: current
updated: 2026-09-02
tags: [handoff, resume]
---

# Next session — start here

Written to make the first ten minutes of the next session productive instead of archaeological.
If you read one file, read this one.

**Branch:** `docs/staff-level-restructure` — 2 commits ahead of `main`, clean tree, no PR.

---

## 1. The state in one paragraph

The prep set exists and is verified: 75 files under `interview-prep/`, every link resolving. The
*plan* to raise it from prep-grade to staff-grade also exists and is reviewed:
`interview-prep/topics/manifest.md` lists 123 canonical topics with aliases, tiers and split
provenance. **None of that plan has been executed.** The 63 P0 pages are unwritten. Execution is
blocked on one decision that takes about two minutes to make.

## 2. The blocking decision

Answer **D1–D4** in [`../interview-prep/topics/manifest.md`](../interview-prep/topics/manifest.md) §7.
Recommendations are already written; *"go with the recommendations"* is a complete answer.

| | Decision | Recommendation | If yes, what happens |
|---|---|---|---|
| D1 | Rename `02-primitives/` → `fundamentals/`, split 12 files into ~47 | **Yes** | The structural change that makes the set staff-level rather than a glossary |
| D2 | Add `patterns/` and `comparisons/`; retire `08-reference/tech-selection.md` into the latter | **Yes** | Cross-topic trade-off matrices get a home |
| D3 | Write all 123 topics, or P0 only (63) | **P0 only** | ~13 batches of 5 |
| D4 | Rewrite case files in place, or move to `case-studies/` | **In place** | Moving breaks every inbound link in `INDEX.md` and the legacy notes |

## 3. First commands

```bash
cd ~/Documents/coding/learn/system-design-prep
git checkout docs/staff-level-restructure
cat STATUS.md                                    # traps and stop-point
sed -n '/## 7. Decisions/,$p' interview-prep/topics/manifest.md    # the four decisions

# baseline the repo before touching anything — expect 485 checked, 4 broken (placeholders)
python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .
```

## 4. Batch 1 — the consistency cluster

Five files, all `split ←` from today's `02-primitives/consistency-and-consensus.md`. Chosen first
because they're the highest-value pages in the set and they exercise every part of the section
contract, so problems with the approach surface on batch 1 rather than batch 9.

| File | Carries |
|---|---|
| `consistency-models.md` | The ladder, CAP stated correctly, PACELC, per-database placement |
| `transaction-isolation-levels.md` | MVCC mechanics, write skew shown as an interleaving, SSI aborts |
| `consensus-raft-paxos.md` | Election, log replication, membership change, cost per write |
| `leases-locks-and-fencing.md` | The GC-pause zombie holder, fencing tokens, why a TTL lock isn't mutual exclusion |
| `quorums-and-anti-entropy.md` | R+W>N, sloppy quorums, read repair, Merkle trees, gossip |

**Do not delete `02-primitives/consistency-and-consensus.md` until all five exist** and its
content has a destination. The manifest records the split; the source file is the safety net.

## 5. What "done" means for one page

The `staff-technical-docs` skill is installed and will trigger on this work. Its contract:

```
## Core concept · Mechanics & internals · Numbers that matter · Failure modes
## Trade-offs vs alternatives · Real-world examples · Follow-up questions
## See also · Referenced by · Sources
```

Plus: 2–3 sources cross-checked, numbers sourced or marked order-of-magnitude, ≥2 Mermaid
diagram types reusing `interview-prep/diagrams/components.md`, and the link check quoted.

Then, from the **repository root**:

```bash
python ~/.claude/skills/staff-technical-docs/scripts/lint_docs.py interview-prep --contract
python ~/.claude/skills/staff-technical-docs/scripts/gen_backlinks.py .
python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .    # re-run: backlinks are links
```

## 6. Traps that will cost you an hour

| Trap | Rule |
|---|---|
| **Never rename a legacy file to tidy it up** | Inbound links are relative and break silently. This caused 5 broken links this session. Percent-encode the link target instead |
| Legacy names contain spaces and parens | `%20` `%28` `%29`. An unescaped `(` truncates the target and breaks on GitHub while rendering fine locally |
| Run doc scripts from the **repo root** | `gen_backlinks.py` scoped to a subfolder can't see inbound links from outside it and strips them as though gone |
| `markdown files/md_blacklinks.md` | Reports 4 broken links forever — `{rel_path}` placeholders in a script's own docs. Expected noise, not a regression |
| Wikilinks are disabled in this vault | Markdown links only |
| `interview-prep/10-resources/vendor/` | ~100 MB of upstream clones, gitignored, read-only. Refresh with `fetch-references.sh` |
| Windows + skill-creator viewer | Server mode crashes on cp1252. Prefix `PYTHONIOENCODING=utf-8 PYTHONUTF8=1`, or use `--static` |
| Quoted heredocs in the Bash tool | `<<'EOF'` leaks apostrophes into the parser. Use the Write tool for file content |

## 7. Also open, lower priority

**In this repo**
- No PR opened. Branch is 2 commits ahead of `main`.
- 4 raw-space link targets in `main.md` resolve locally but break on GitHub.

**In `~/.claude/skills/staff-technical-docs/`**
- `evals/evals.json` v2 is written but **never run**. Iteration 2 needs 8 subagent runs.
- eval-3's fixture (`fixtures/existing-set/`) is specified but **not built** — a 5-page set with a
  manifest, a components library, and one topic hidden under a non-obvious alias.
- **No human ever reviewed the iteration-1 outputs.** `review.html` in
  `~/.claude/skills/staff-technical-docs-workspace/iteration-1/` opens standalone, no server.
  This is the weakest evidence in the whole effort — the skill was graded by its own author
  against assertions that author wrote.

## 8. If you'd rather not resume this

Everything is committed and self-describing. The manifest stands alone as a plan, the skill works
independently of this repo, and `STATUS.md` plus `docs/WORKLOG.md` explain the reasoning. Nothing
is half-applied or hidden behind a flag.
