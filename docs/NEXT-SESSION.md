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

**Branch:** `docs/comparisons-batch-8` · **PRs #1–#9** open, none merged.

---

## 1. The state in one paragraph

The restructure decision is made and recorded
([ADR-0001](adr/0001-split-primitives-into-atomic-fundamentals.md)): `02-primitives/` is being
split into `fundamentals/`, one mechanism per page, scope **all 123 manifest topics**, P0 first,
five per branch. **Batches 1–8 are written and verified** — 25 pages in `fundamentals/`, 10 in
`patterns/` and 5 in the new `comparisons/`, each with a cited production incident, real arithmetic
and two diagram types. **40 of 123** done, and every folder the restructure needs now exists. Nothing is
half-applied: every primitive file they split from is still present and banner-marked, and each
stays until its remaining topics land.

## 2. Two housekeeping items before writing

1. **Merge the stacked PRs, oldest first.** #1 (plan) → #2 → … → #9; each retargets to `main`
   as the one below it lands. The session could not merge them (permission classifier blocked
   `gh pr merge`): `gh pr merge 1 --squash --delete-branch`, then 2–9.
2. **Baseline the repo** before touching anything:
   ```bash
   cd ~/Documents/coding/learn/system-design-prep
   python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .
   # expect: checked 1858 relative links; broken: 4   (the {rel_path} placeholders)
   ```

## 3. Batch 9 — the first case rewrites

**A different kind of work.** Batches 1–8 wrote new pages; this rewrites five existing case files
**in place** (no renames, no moves — inbound links live in `INDEX.md` and the legacy notes).

| File | Note |
|---|---|
| `03-backend-cases/news-feed.md` | Already banner-linked to `fanout-write-vs-read`; the case keeps the end-to-end design |
| `03-backend-cases/chat-messaging.md` | Composite partition key, ordering, presence, delivery receipts |
| `03-backend-cases/ride-hailing.md` | Geo indexing moves to `fundamentals/` later; the case keeps matching and dispatch |
| `03-backend-cases/payments-ledger.md` | Idempotency, ledger invariants, the unknown-outcome path |
| `03-backend-cases/ticket-booking.md` | **New file** — the case that punishes eventual consistency |

The case contract (from [CLAUDE.md](../CLAUDE.md)): the staff sections apply, with the design
skeleton — Clarify · Requirements · Estimates · API · Data model · Architecture · Scale & failure ·
Ops & cost — kept **inside** `Mechanics & internals` and `Numbers that matter`.

**This is where the 40 pages already written pay off.** A case should **link to the mechanism pages
rather than re-explain them**, and spend its length on what is specific to this problem: the
estimates, the key design, the failure analysis, the cost. A case that re-teaches fan-out,
idempotency or quorums has not used the set — link and move on.

Cases are expected to run long (the manifest says so), and each still needs its own cited incident,
its own arithmetic, and ≥ 2 diagram types.

## 4. What "done" means for one page

Copy the shape of `fundamentals/consistency-models.md`. The bar, in order of what actually
separates a good page from a passable one:

1. **A cited production incident** in Failure modes — a public postmortem beats any tutorial.
   Batch 1 used GitHub 2018, Jepsen PostgreSQL 12.3, Roblox 2021 and the Raft membership bug;
   batch 2 used GitLab 2017, Discord's Cassandra hot partitions, DynamoDB's per-partition
   ceilings and Facebook's remote markers; batch 3 used RocksDB write stalls, Uber's 2016
   Postgres→MySQL write amplification, Facebook's 2010 four-hour cache-stampede outage and Meta's
   Polaris consistency work; batch 4 used Vanlightly's Kafka message-loss analysis, Jepsen
   Redpanda 21.10.1, Pinterest's watermark starvation and the Stripe/Brandur idempotency design;
   batch 5 used AWS Kinesis 2020, Dean & Barroso's hedging measurements, Facebook's Fail at Scale
   and the HotOS 2021 metastability paper; batch 6 used Jepsen MongoDB 4.2.6, Stripe's online
   migrations and the Noria paper; batch 7 used AWS S3 2017, Route 53's shuffle-sharding numbers,
   Twitter's timeline design and Kreps on reprocessing; batch 8 used Notion's Postgres sharding,
   Figma's database scaling and Slack's job-queue wedge. Do not reuse one across batches — find a
   new one.
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
- `patterns/` exists (10 of 20 pages). `comparisons/` does not — batch 8 creates it and retires
  `08-reference/tech-selection.md` into it.
- 26 case files still carry the old eight-heading skeleton; they are rewritten in place, batch 9+.

**In `~/.claude/skills/staff-technical-docs/`**
- `evals/evals.json` v2 written but never run; eval-3's fixture not built.
- `gen_backlinks.py` should skip fenced code blocks. This repo hit that bug and worked around it in
  the docs; the script itself is still wrong.
- No human ever reviewed the iteration-1 outputs — still the weakest evidence in the effort.

## Referenced by

- [Backlog — ideas not scheduled](BACKLOG.md)
- [Docs index](README.md)
- [Repo index](../INDEX.md)
- [Session record — fundamentals batches 1–5](sessions/2026-09-02-fundamentals-batches-1-5.md)
- [STATUS](../STATUS.md)
- [Worklog](WORKLOG.md)
