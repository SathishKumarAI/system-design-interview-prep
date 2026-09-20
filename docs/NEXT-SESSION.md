---
title: Next session — start here
type: handoff
status: current
updated: 2026-09-02
tags: [handoff, resume]
---

# Next session — start here

Written to make the first ten minutes productive instead of archaeological. If you read one file,
read this one.

**Branch:** `docs/fundamentals-batch-1` · **PR #1** open on `main`, not merged.

---

## 1. The state in one paragraph

The restructure decision is made and recorded
([ADR-0001](adr/0001-split-primitives-into-atomic-fundamentals.md)): `02-primitives/` is being
split into `fundamentals/`, one mechanism per page, scope **all 123 manifest topics**, P0 first,
five per branch. **Batch 1 is written and verified** — the five consistency-cluster pages exist
under `interview-prep/fundamentals/` with cited incidents, real arithmetic and two diagram types
each. 5 of 123 done. Nothing is half-applied: the primitive file they split from is still present,
banner-marked, and stays until its last two topics land.

## 2. Two housekeeping items before writing

1. **Merge PR #1** — `docs/staff-level-restructure` → `main`, squash. It carries only the plan and
   conventions. The session could not merge it (permission classifier blocked `gh pr merge`), so:
   `gh pr merge 1 --squash --delete-branch`. Then rebase `docs/fundamentals-batch-1` on `main` and
   open its own PR.
2. **Baseline the repo** before touching anything:
   ```bash
   cd ~/Documents/coding/learn/system-design-prep
   python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .
   # expect: checked 1089 relative links; broken: 4   (the {rel_path} placeholders)
   ```

## 3. Batch 2 — the replication cluster

Five files, all `split ←` `02-primitives/replication-and-partitioning.md`. Chosen next because
every case study leans on them and they pair directly with batch 1.

| File | Must carry |
|---|---|
| `partitioning-strategies.md` | Range/hash/directory/geo; the three tests a partition key must pass; cross-partition query cost |
| `replication-topologies.md` | Single/multi-leader/leaderless; sync vs semi-sync vs async; RPO arithmetic; failover mechanics |
| `replication-lag-and-session-guarantees.md` | The three anomalies, LSN-aware routing, why "just read from a replica" quietly breaks products |
| `hot-shard-mitigation.md` | Salting, splitting, dedicated shards, read-path caching; detection *before* it pages you |
| `consistent-hashing.md` | Ring mechanics, virtual nodes, bounded loads, rendezvous hashing as the alternative |

Do **not** delete `replication-and-partitioning.md` at the end of batch 2 — it also carries
`rebalancing-and-resharding` (P1, later batch).

## 4. What "done" means for one page

Copy the shape of `fundamentals/consistency-models.md`. The bar, in order of what actually
separates a good page from a passable one:

1. **A cited production incident** in Failure modes — a public postmortem beats any tutorial.
   Batch 1 used GitHub 2018, Jepsen PostgreSQL 12.3, Roblox 2021, the Raft membership bug.
2. **Real arithmetic** in Numbers that matter, each figure sourced or explicitly labelled
   "order of magnitude".
3. **≥ 2 Mermaid diagram *types*** (flowchart + sequence/state), reusing the palette and node
   naming in [../interview-prep/diagrams/components.md](../interview-prep/diagrams/components.md).
4. **A "where staff engineers get this wrong" list** inside Trade-offs — the section that makes
   the page worth reading for someone who already knows the topic.
5. Section order per [CLAUDE.md](../CLAUDE.md) → *Section contract*. Frontmatter complete,
   `updated` bumped, manifest row marked ✅ and §8 progress count raised.

Then, from the **repository root**:

```bash
python ~/.claude/skills/staff-technical-docs/scripts/gen_backlinks.py .   # twice — second run must print "0 changed"
python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .     # backlinks are links too
python ~/.claude/skills/staff-technical-docs/scripts/lint_docs.py interview-prep/fundamentals --contract
```

Quote the counts in the commit or PR body. "Links verified" is an assertion; the count is evidence.

## 5. Traps that will cost you an hour

Full list in [../STATUS.md](../STATUS.md). The three that are new since last session:

| Trap | Rule |
|---|---|
| **`gen_backlinks.py` writes inside code fences** | It matches `## Referenced by` / `## Sources` textually. It injected backlink lists into the contract examples in `CLAUDE.md` and `CONVENTIONS.md`; both are tables now. Never put those headings inside a fence |
| **`lint_docs.py --contract` always reports "missing: Follow-up questions"** | Skill-generic name vs this repo's `Staff-level follow-ups`. Expected noise; do not rename the section |
| **A primitive file is deleted only when empty of unique topics** | Not when "most of it" has moved |

Unchanged and still true: never rename a legacy file to fix a link (percent-encode instead), run
scripts from the repo root, wikilinks stay disabled, `vendor/` is read-only.

## 6. Also open, lower priority

**This repo**
- `patterns/` and `comparisons/` do not exist yet — created with batches 6–8, by design.
- 26 case files still carry the old eight-heading skeleton; they are rewritten in place, batch 9+.

**In `~/.claude/skills/staff-technical-docs/`**
- `evals/evals.json` v2 written but never run; eval-3's fixture not built.
- `gen_backlinks.py` should skip fenced code blocks. This repo hit that bug and worked around it in
  the docs; the script itself is still wrong.
- No human ever reviewed the iteration-1 outputs — still the weakest evidence in the effort.

## Referenced by

- [Docs index](README.md)
- [Repo index](../INDEX.md)
- [STATUS](../STATUS.md)
- [Worklog](WORKLOG.md)
