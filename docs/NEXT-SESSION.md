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

**Branch:** `docs/fundamentals-batch-2` · **PRs #1, #2, #3** open, none merged.

---

## 1. The state in one paragraph

The restructure decision is made and recorded
([ADR-0001](adr/0001-split-primitives-into-atomic-fundamentals.md)): `02-primitives/` is being
split into `fundamentals/`, one mechanism per page, scope **all 123 manifest topics**, P0 first,
five per branch. **Batches 1 and 2 are written and verified** — ten pages under
`interview-prep/fundamentals/`, each with a cited production incident, real arithmetic and two
diagram types. 10 of 123 done. Nothing is half-applied: both primitive files they split from are
still present and banner-marked, and each stays until its remaining topics land.

## 2. Two housekeeping items before writing

1. **Merge the stacked PRs, oldest first.** #1 (plan) → #2 (batch 1) → #3 (batch 2); each
   retargets to `main` as the one below it lands. The session could not merge them (permission
   classifier blocked `gh pr merge`): `gh pr merge 1 --squash --delete-branch`, then 2, then 3.
2. **Baseline the repo** before touching anything:
   ```bash
   cd ~/Documents/coding/learn/system-design-prep
   python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .
   # expect: checked 1186 relative links; broken: 4   (the {rel_path} placeholders)
   ```

## 3. Batch 3 — storage engines and caching

Five files from **two** source primitives. First batch that splits more than one file, so both
need pointer banners and neither is deleted.

| File | Source | Must carry |
|---|---|---|
| `storage-engines.md` | `storage-and-databases.md` | B-tree vs LSM internals; write/read/space amplification; compaction debt and the latency cliff it causes |
| `indexing-and-query-planning.md` | `storage-and-databases.md` | Composite order, covering, partial indexes; cardinality estimation; **why the planner ignores your index** |
| `caching-strategies.md` | `caching.md` | Aside/through/behind/refresh-ahead; layer placement economics; hit-rate arithmetic |
| `cache-invalidation.md` | `caching.md` | TTL vs versioned keys vs CDC-driven; **the delete-on-write race, shown as an interleaving** |
| `cache-failure-modes.md` | `caching.md` | Stampede, hot key, penetration, cold start; single-flight and probabilistic early expiry |

Neither source file is deleted at the end: `caching.md` still owns `redis-internals`,
`storage-and-databases.md` still owns object-storage internals and expand-contract migration.

Incident candidates worth verifying before writing: RocksDB/Cassandra compaction stalls, the
Facebook memcache stampede work (already cited in batch 2), and any public write-up of a cache
cold-start after a flush — the "we restarted the cache tier and took the database down" shape.

## 4. What "done" means for one page

Copy the shape of `fundamentals/consistency-models.md`. The bar, in order of what actually
separates a good page from a passable one:

1. **A cited production incident** in Failure modes — a public postmortem beats any tutorial.
   Batch 1 used GitHub 2018, Jepsen PostgreSQL 12.3, Roblox 2021 and the Raft membership bug;
   batch 2 used GitLab 2017, Discord's Cassandra hot partitions, DynamoDB's per-partition
   ceilings and Facebook's remote markers. Do not reuse one across batches — find a new one.
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
