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

## 2026-09-02 — Batch 2: the replication cluster

Branch: `docs/fundamentals-batch-2` · PRs open: #1 (plan), #2 (batch 1), #3 (this)

### What

Five pages split from `02-primitives/replication-and-partitioning.md`:
`partitioning-strategies`, `replication-topologies`, `replication-lag-and-session-guarantees`,
`hot-shard-mitigation`, `consistent-hashing`. Fundamentals is now 10 of 47; the manifest total is
10 of 123.

### Incidents and primary sources used

| Page | Anchor |
|---|---|
| replication-topologies | GitLab 2017-01-31 — lag treated as a nuisance, `rm -rf` on the primary, **five backup mechanisms all failed for five different reasons**; ~18 h down, permanent loss of 6 h of writes |
| partitioning-strategies · hot-shard-mitigation | Discord 2023 — hot partitions cascading latency on Cassandra; `(channel_id, bucket)` composite key; request coalescing in a Rust data-services tier; migration stalled at 99.9999% on tombstone-dense token ranges |
| hot-shard-mitigation | DynamoDB hard per-partition ceilings (3 000 RCU / 1 000 WCU), split-for-heat, and the fact that an **LSI blocks splitting** |
| replication-lag-and-session-guarantees | Facebook memcache (NSDI 2013) remote markers — mark the known-stale keys and redirect only those reads to the master region |
| consistent-hashing | Consistent Hashing with Bounded Loads (Google/Thorup); Vimeo runs it in HAProxy at `c = 1.25`; Cassandra's vnode default dropped 256 → 16 |

### Why this framing

Three arguments in these pages are the ones that change behaviour, and none of them are the
textbook version of the topic:

- **RPO is not a setting, it is `lag × write rate`.** At 5 000 writes/s and 800 ms p99 lag, an
  async failover loses ~4 000 committed writes. Teams can quote replica counts and cannot quote
  this.
- **Sharding fixes volume; it does nothing for skew.** A hot *key* hashes to one partition no
  matter how many partitions exist. Separating "hot key" from "hot partition" is the whole of
  `hot-shard-mitigation`, because the standard reflex (salting) is correct for write-hot keys and
  actively harmful for read-hot ones.
- **Consistent hashing bounds movement, not load.** Balance comes from vnodes; *load* balance
  needs bounded loads. The page also argues the unpopular position that a fixed logical-partition
  map beats a ring wherever membership changes under human control — which is what Redis, Kafka
  and Elasticsearch all chose.

### Trade-offs

- `replication-and-partitioning.md` kept and banner-marked: it still uniquely holds
  `rebalancing-and-resharding` (P1, later batch). Same staging rule as batch 1.
- Semi-sync's silent 10 s fallback to async and MySQL's `Seconds_Behind_Master` reporting 0 on a
  stalled IO thread are both documented as failure modes rather than footnotes — they are the
  reason "we have replication" and "we have durability" are different claims.
- `consistent-hashing` is P1 but was written in this batch because the other four pages reference
  it constantly; deferring it would have left four dangling explanations.

### Verification

```
$ python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .
checked 1186 relative links; broken: 4          # the {rel_path} placeholders, unchanged
$ python ~/.claude/skills/staff-technical-docs/scripts/gen_backlinks.py .   # run twice
192 files scanned, 563 inbound links mapped, 0 changed
```

All five pages carry two Mermaid diagram types. The `lint_docs.py --contract` "missing: Follow-up
questions" line is the known naming mismatch recorded in STATUS.md, not a gap.

---

## 2026-09-02 — Batch 1: the consistency cluster, and the decisions that unblocked it

Branch: `docs/fundamentals-batch-1` · PR for the plan branch: #1

### What

D1–D4 answered (all four recommendations approved; scope set to **all 123 topics**, not the
recommended 63 P0), recorded as
[ADR-0001](adr/0001-split-primitives-into-atomic-fundamentals.md). Then batch 1 written:
`interview-prep/fundamentals/` with five pages, ~250–280 lines each —
`consistency-models`, `transaction-isolation-levels`, `consensus-raft-paxos`,
`leases-locks-and-fencing`, `quorums-and-anti-entropy` — plus a folder README, manifest progress
section, and pointer banners on the primitive file being split.

### How

Each page was researched against 2–3 independent sources before assertion, and each carries a
**documented production incident** rather than a generic failure list:

| Page | Incident / primary finding |
|---|---|
| consistency-models | GitHub 2018-10-21 — 43 s partition, 24 h 11 m degradation; Orchestrator held quorum, async MySQL replication did not |
| transaction-isolation-levels | Jepsen PostgreSQL 12.3 — real G2-item under `SERIALIZABLE`; XID misattribution in conflict detection; present since SSI shipped in 2011, fixed Aug 2020 |
| consensus-raft-paxos | Raft single-server membership-change safety bug (2015); Roblox 2021 — 73 h outage from Consul streaming + BoltDB freelist pathology |
| leases-locks-and-fencing | Kleppmann vs antirez on Redlock; Chubby sequencers and `lock-delay`; GFS chunk leases + version numbers |
| quorums-and-anti-entropy | Tombstone resurrection when repair misses `gc_grace_seconds`; Cassandra Merkle depth 2^15 causing overstreaming; DynamoDB's move *away* from leaderless |

### Why these five first

They are the highest-value pages in the set and they exercise every part of the section contract —
so if the contract were wrong, it would show on batch 1 rather than batch 9. They also all split
from one source file, which meant the split mechanics got tested end to end immediately.

### Trade-offs and things worth knowing

- **`02-primitives/consistency-and-consensus.md` was kept, not deleted.** It still uniquely holds
  clocks and CRDTs (both P1, batches later). It now carries a banner naming its successor pages.
  The cost is a transitional period where two files discuss the same subject at different depths —
  accepted knowingly and recorded in ADR-0001.
- **Scope decision went against the written recommendation.** The manifest recommends stopping at
  63 P0 files; all 123 were chosen. Batch order still runs P0 first, so stopping early stays
  available at any batch boundary.
- **Found and fixed a real tooling trap.** `gen_backlinks.py` matches `## Referenced by` and
  `## Sources` **textually, including inside code fences** — it injected generated backlink lists
  into the section-contract examples in `CLAUDE.md` and `CONVENTIONS.md`. Both were converted from
  fenced snippets to tables, and the trap is now documented in each file. Second and third runs of
  the script report `0 changed`, so the pass is idempotent again.
- **Fixed 4 pre-existing links** in `main.md` that used raw spaces and backslashes
  (`basic\prep\SQL or NoSQL.md`). Percent-encoded with forward slashes — the files were **not**
  renamed, per the standing rule.
- **Known lint false positive:** `lint_docs.py --contract` reports "missing: Follow-up questions"
  for all five pages. The skill's generic contract names that section `Follow-up questions`; this
  repo's contract (CLAUDE.md) names it `Staff-level follow-ups`. Repo convention wins; expect this
  line on every future page.

### Verification

```
$ python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .
checked 1089 relative links; broken: 4          # the 4 {rel_path} placeholders, unchanged
$ python ~/.claude/skills/staff-technical-docs/scripts/gen_backlinks.py .   # run twice
187 files scanned, 519 inbound links mapped, 0 changed
```

Before this session the same check reported 501 links; the growth is the new pages plus the
regenerated backlink sections. No raw-space GitHub warnings remain.

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

## Referenced by

- [ADR-0001: Split bundled primitives into atomic fundamentals pages](adr/0001-split-primitives-into-atomic-fundamentals.md)
- [CLAUDE.md — system-design-prep](../CLAUDE.md)
- [Docs index](README.md)
- [Repo index](../INDEX.md)
- [STATUS](../STATUS.md)
