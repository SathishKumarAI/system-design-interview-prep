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

**Branch:** `docs/fundamentals-batch-3` · **PRs #1–#4** open, none merged.

---

## 1. The state in one paragraph

The restructure decision is made and recorded
([ADR-0001](adr/0001-split-primitives-into-atomic-fundamentals.md)): `02-primitives/` is being
split into `fundamentals/`, one mechanism per page, scope **all 123 manifest topics**, P0 first,
five per branch. **Batches 1–3 are written and verified** — fifteen pages under
`interview-prep/fundamentals/`, each with a cited production incident, real arithmetic and two
diagram types. 15 of 123 done. Nothing is half-applied: all four primitive files they split from
are still present and banner-marked, and each stays until its remaining topics land.

## 2. Two housekeeping items before writing

1. **Merge the stacked PRs, oldest first.** #1 (plan) → #2 (batch 1) → #3 (batch 2) → #4
   (batch 3); each retargets to `main` as the one below it lands. The session could not merge them
   (permission classifier blocked `gh pr merge`): `gh pr merge 1 --squash --delete-branch`, then
   2, 3, 4.
2. **Baseline the repo** before touching anything:
   ```bash
   cd ~/Documents/coding/learn/system-design-prep
   python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .
   # expect: checked 1286 relative links; broken: 4   (the {rel_path} placeholders)
   ```

## 3. Batch 4 — messaging and delivery

Five files from two source primitives; neither is deleted at the end.

| File | Source | Must carry |
|---|---|---|
| `log-vs-queue.md` | `messaging-and-streams.md` | Retention, replay, consumer-group semantics; **when a queue is the correct smaller answer** |
| `kafka-internals.md` | `messaging-and-streams.md` | ISR, `acks` / `min.insync.replicas`, rebalance protocols (eager vs cooperative), log compaction, tiered storage |
| `delivery-semantics.md` | `messaging-and-streams.md` | Why exactly-once *delivery* is impossible and exactly-once *effects* are not; the transactional-producer mechanics |
| `stream-processing-semantics.md` | `messaging-and-streams.md` | Event vs processing time, watermarks, late data, checkpoint/state size, restart cost |
| `idempotency.md` | `transactions-and-idempotency.md` | Key scope, in-flight collisions, storing the response, natural vs synthetic idempotence |

`messaging-and-streams.md` still owns backpressure/consumer-lag; `transactions-and-idempotency.md`
still owns 2PC, sagas, outbox and ledgers. Both keep their banner and stay.

Incident candidates worth verifying before writing: Kafka rebalance storms during rolling deploys,
`min.insync.replicas=1` data loss on ISR shrink, the Slack 2021-01-04 or Cloudflare queue-backlog
write-ups, and any public postmortem where a consumer group's offset reset replayed production
traffic.

## 4. What "done" means for one page

Copy the shape of `fundamentals/consistency-models.md`. The bar, in order of what actually
separates a good page from a passable one:

1. **A cited production incident** in Failure modes — a public postmortem beats any tutorial.
   Batch 1 used GitHub 2018, Jepsen PostgreSQL 12.3, Roblox 2021 and the Raft membership bug;
   batch 2 used GitLab 2017, Discord's Cassandra hot partitions, DynamoDB's per-partition
   ceilings and Facebook's remote markers; batch 3 used RocksDB write stalls, Uber's 2016
   Postgres→MySQL write amplification, Facebook's 2010 four-hour cache-stampede outage and Meta's
   Polaris consistency work. Do not reuse one across batches — find a new one.
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
