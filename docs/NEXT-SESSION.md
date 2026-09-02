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

**Branch:** `docs/fundamentals-batch-4` · **PRs #1–#5** open, none merged.

---

## 1. The state in one paragraph

The restructure decision is made and recorded
([ADR-0001](adr/0001-split-primitives-into-atomic-fundamentals.md)): `02-primitives/` is being
split into `fundamentals/`, one mechanism per page, scope **all 123 manifest topics**, P0 first,
five per branch. **Batches 1–4 are written and verified** — twenty pages under
`interview-prep/fundamentals/`, each with a cited production incident, real arithmetic and two
diagram types. 20 of 123 done. Nothing is half-applied: all six primitive files they split from
are still present and banner-marked, and each stays until its remaining topics land.

## 2. Two housekeeping items before writing

1. **Merge the stacked PRs, oldest first.** #1 (plan) → #2 → #3 → #4 → #5; each retargets to
   `main` as the one below it lands. The session could not merge them (permission classifier
   blocked `gh pr merge`): `gh pr merge 1 --squash --delete-branch`, then 2, 3, 4, 5.
2. **Baseline the repo** before touching anything:
   ```bash
   cd ~/Documents/coding/learn/system-design-prep
   python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .
   # expect: checked 1386 relative links; broken: 4   (the {rel_path} placeholders)
   ```

## 3. Batch 5 — reliability

Five files: three split from `02-primitives/reliability-patterns.md`, **two written from
scratch**. First batch that is mostly new pages, so there is no source text to lean on — budget
more research time and treat the manifest scope lines as the only brief.

| File | Source | Must carry |
|---|---|---|
| `timeouts-retries-backoff.md` | `reliability-patterns.md` | Deadline propagation, retry budgets, **layered-retry amplification arithmetic** (3 layers × 3 retries = 27× load) |
| `load-shedding-and-admission-control.md` | `reliability-patterns.md` | Shed early and cheap, priority classes, queue-age drop (LIFO under overload), what a 429 actually promises |
| `cascading-and-metastable-failures.md` | **new** | Why load returning to normal does not recover the system; how to break the loop. HotOS 2021 is the primary source |
| `tail-latency.md` | **new** | Fan-out amplification maths, hedged and tied requests, why averages lie. Dean & Barroso *The Tail at Scale* |
| `queueing-theory-basics.md` | **new** | Little's law, the utilisation/latency knee, why ~80% utilisation is the practical ceiling |

`reliability-patterns.md` also owns circuit breakers, bulkheads, graceful degradation and
multi-region DR — those go to `patterns/` in batch 7 — so it keeps its banner and stays.

These five interlock: queueing theory explains the knee, tail latency explains why fan-out hits it,
retries explain how load multiplies past it, shedding is the control, and metastability is what
happens without one. Write them as one argument, not five essays.

Incident candidates worth verifying: AWS's own retry-storm write-ups, the 2021 Salesforce or
Fastly configuration outages, Google's SRE-book overload chapter, and any postmortem where the
service stayed down after the trigger was removed.

## 4. What "done" means for one page

Copy the shape of `fundamentals/consistency-models.md`. The bar, in order of what actually
separates a good page from a passable one:

1. **A cited production incident** in Failure modes — a public postmortem beats any tutorial.
   Batch 1 used GitHub 2018, Jepsen PostgreSQL 12.3, Roblox 2021 and the Raft membership bug;
   batch 2 used GitLab 2017, Discord's Cassandra hot partitions, DynamoDB's per-partition
   ceilings and Facebook's remote markers; batch 3 used RocksDB write stalls, Uber's 2016
   Postgres→MySQL write amplification, Facebook's 2010 four-hour cache-stampede outage and Meta's
   Polaris consistency work; batch 4 used Vanlightly's Kafka message-loss analysis, Jepsen
   Redpanda 21.10.1, Pinterest's watermark starvation and the Stripe/Brandur idempotency design.
   Do not reuse one across batches — find a new one.
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
