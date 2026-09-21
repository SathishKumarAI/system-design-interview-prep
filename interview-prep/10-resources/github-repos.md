---
title: GitHub repositories
type: resource
track: universal
status: drafted
sources: [GitHub API repo metadata 2026-09-20, own audit]
updated: 2026-09-20
tags: [github, repos]
---

# GitHub repositories

Grouped by **what you are doing**, not by topic. Every row carries a verdict, the last push date
(GitHub API, 2026-09-20) and — where the repo might get quoted or vendored — its licence.

Cloned into `vendor/` by [fetch-references.sh](fetch-references.sh) where the ✅ column says so.
`vendor/` is gitignored and read-only.

| You are… | Go to |
|---|---|
| Learning how a mechanism actually works | [§1](#1-learning-a-mechanism) |
| Reading how real systems are built, and how they broke | [§2](#2-real-architectures-and-real-failures) |
| Wanting to *run* something, not read about it | [§3](#3-running-something) |
| Drilling interview-shaped cases | [§4](#4-drilling-cases) |
| Wondering why an obvious repo is missing | [§5](#5-deliberately-not-here) |

---

## 1. Learning a mechanism

The corpus in `fundamentals/`, `patterns/` and `comparisons/` cites primary sources far more often
than it cites repos. These are the repos that *are* primary sources, or that index them well.

| Repo | Last push | Licence | Verdict | Vendored |
|---|---|---|---|---|
| [aphyr/distsys-class](https://github.com/aphyr/distsys-class) | 2025-03 | none stated | **Kyle Kingsbury's distributed-systems course notes.** The clearest short treatment of consistency models and the impossibility results in existence. Read it before, not after, DDIA ch. 9 | ✅ |
| [theanalyst/awesome-distributed-systems](https://github.com/theanalyst/awesome-distributed-systems) | 2025-01 | none stated | A *short* list — papers and talks, not blog posts. The brevity is the feature; the long lists are where reading goes to die | ✅ |
| [pingcap/awesome-database-learning](https://github.com/pingcap/awesome-database-learning) | 2024-08 | none stated | **The storage-engine reading path**, ordered by people who shipped one. Query execution, transactions, LSM vs B-tree. Dormant, but a reading *order* does not rot | ✅ |
| [facebook/rocksdb wiki](https://github.com/facebook/rocksdb/wiki) | 2026-09 (code) | Apache-2.0 / GPL-2.0 dual | **The best free LSM-tree documentation that exists.** Compaction styles, write stalls, the actual tuning knobs and what each one costs. Read the wiki; do not clone 250 MB of C++ | — |
| [asatarin/testing-distributed-systems](https://github.com/asatarin/testing-distributed-systems) | 2026-07 | CC-BY-4.0 | How people actually *verify* distributed systems — Jepsen, TLA+, deterministic simulation, lineage-driven fault injection. Narrow and current | ✅ |
| [papers-we-love/papers-we-love](https://github.com/papers-we-love/papers-we-love) | 2026-09 | none stated | Mirrors of the classic papers by field, with talk recordings. A finder, not a curriculum — and 230 MB, so browse it on the web | — |
| [ashishps1/awesome-system-design-resources](https://github.com/ashishps1/awesome-system-design-resources) | 2026-02 | GPL-3.0 | Best-maintained curated index. **Use it as a search index, not a reading list.** GPL-3.0 — do not paste its text into this repo | ✅ |

> [!warning] Trap
> `awesome-*` lists are where preparation goes to die. Open one only with a question already in
> hand. If you cannot name the question, you are collecting, not studying.

## 2. Real architectures and real failures

The highest-value category for a staff loop. A public post-mortem beats ten tutorials, because it
is the only genre that reports what the authors got *wrong*.

| Repo | Last push | Licence | Verdict | Vendored |
|---|---|---|---|---|
| [danluu/post-mortems](https://github.com/danluu/post-mortems) | 2026-08 | none stated | **The classic annotated postmortem collection.** The commentary is the value — it groups by failure class (config push, cascading failure, clock, data loss), which is how these should be read | ✅ |
| [upgundecha/howtheysre](https://github.com/upgundecha/howtheysre) | 2025-11 | CC0-1.0 | Company-by-company SRE practice: SLOs, on-call, incident process, tooling. The one collection of *operational* design rather than architectural design | ✅ |
| [eugeneyan/applied-ml](https://github.com/eugeneyan/applied-ml) | 2024-07 | MIT | **The answer key for ML cases** — real company write-ups by topic. Dormant two years, but the 2018–2024 cases are the ones interviewers were trained on | ✅ |
| [binhnguyennus/awesome-scalability](https://github.com/binhnguyennus/awesome-scalability) | 2026-01 | MIT | Enormous, organised by *scaling problem* rather than by company — the right axis. Deep dives only, once you know what you are looking for | ✅ |
| [kilimchoi/engineering-blogs](https://github.com/kilimchoi/engineering-blogs) | 2024-08 | none stated | The definitive company-blog list, with OPML you can drop into a feed reader. Dormant; the blogs on it have not moved | — |

Not repos, but the same job and more current:

- [postmortem.io](https://postmortem.io/) — 645 indexed public incident reports and shutdown
  write-ups, tagged by failure class, newest from August 2026. Searchable by company before a loop.
- [AWS post-event summaries](https://aws.amazon.com/premiumsupport/technology/pes/) — AWS's own
  incident write-ups, retained five years, including the October 2025 DynamoDB / us-east-1 event.

## 3. Running something

Reading about quorum loss and *watching* a linearizability checker find a violation are different
kinds of knowing. This group is what separates a staff answer from a well-read one.

| Repo | Last push | Licence | Verdict | Vendored |
|---|---|---|---|---|
| [jepsen-io/maelstrom](https://github.com/jepsen-io/maelstrom) | 2026-07 | EPL-1.0 | **The single best exercise in this file.** A workbench where you implement broadcast / a KV store / a transactional store in any language and Jepsen's own checker tears it apart under partition. Do the `lin-kv` challenge once and consistency models stop being vocabulary | ✅ |
| [ept/hermitage](https://github.com/ept/hermitage) | 2026-01 | none stated | Kleppmann's isolation-anomaly suite: the exact SQL that produces write skew, lost update and phantom read, run against Postgres / MySQL / Oracle / SQL Server with the *measured* results. Half an hour here beats any isolation-level table, including the one in `comparisons/` | ✅ |
| [jepsen-io/jepsen](https://github.com/jepsen-io/jepsen) | 2026-09 | EPL-1.0 (see `project.clj`) | The framework behind [jepsen.io/analyses](https://jepsen.io/analyses). Read one test's `checker` and `nemesis` to see what "we tested it under partition" is actually worth | — |
| [Shopify/toxiproxy](https://github.com/Shopify/toxiproxy) | 2026-09 | MIT | A TCP proxy that injects latency, bandwidth limits and partitions on demand. The cheapest way to make a timeout / retry / circuit-breaker design produce evidence instead of an opinion | — |
| [tigerbeetle/tigerbeetle](https://github.com/tigerbeetle/tigerbeetle) | 2026-08 | Apache-2.0 | A production double-entry ledger on VSR with deterministic simulation testing that **documents its own design decisions** ([docs.tigerbeetle.com](https://docs.tigerbeetle.com/)). The reference implementation for the ledger and atomicity pages | — |
| [cmu-db/bustub](https://github.com/cmu-db/bustub) | 2026-09 | MIT | CMU 15-445's teaching DBMS — buffer pool, B+tree, MVCC, query execution as assignments. Worth it only if you want storage internals in your hands; it is a multi-week commitment | — |

## 4. Drilling cases

Interview-shaped material. You need one of these, not five.

| Repo | Last push | Licence | Verdict | Vendored |
|---|---|---|---|---|
| [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) | 2026-09 | CC-BY-4.0 | **The canonical free curriculum**, still maintained at 371k stars. Its value at staff level is `solutions/system_design/` — worked exercises with code, not prose | ✅ |
| [karanpratapsingh/system-design](https://github.com/karanpratapsingh/system-design) | 2026-07 | see repo (NOASSERTION) | Clean, linear, finishable in a weekend. Use it if the primer feels scattered. It is *breadth*, and thin wherever this repo's `fundamentals/` is deep | ✅ |
| [ByteByteGoHq/system-design-101](https://github.com/ByteByteGoHq/system-design-101) | 2025-04 | NOASSERTION | Excellent diagrams, shallow text, no longer updated. Good for revision the night before; useless for the depth follow-up | ✅ |
| [alirezadir/AIMLInterviews](https://github.com/alirezadir/AIMLInterviews) | 2026-09 | MIT | **The best free ML system design material**, and actively maintained. Note the rename from `Machine-Learning-Interviews` — old links redirect. Read `src/MLSD/ml-system-design.md` | ✅ |
| [yangshun/front-end-interview-handbook](https://github.com/yangshun/front-end-interview-handbook) | 2026-08 | MIT | The frontend standard; the RADIO framework is what `04-frontend-cases/` is built on. 28 MB vendored, justified only because the corpus cites it | ✅ |
| [ashishps1/awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design) | 2026-08 | GPL-3.0 | The *other* design round. Many staff loops include an OOD / API-design hour and people walk in having prepared only for this one | — |

## 5. Deliberately not here

Cutting is what the verdict column is for.

| Repo | Why not |
|---|---|
| [checkcheckzz/system-design-interview](https://github.com/checkcheckzz/system-design-interview) | **Removed from `vendor/` 2026-09-20.** Last push 2023-04; a 2017-era link dump whose links have rotted. `awesome-scalability` supersedes it entirely |
| [chiphuyen/machine-learning-systems-design](https://github.com/chiphuyen/machine-learning-systems-design) | **Removed from `vendor/` 2026-09-20.** Last push 2023-04; the author superseded it with *Designing Machine Learning Systems*, which is on this machine — see [books-on-this-machine.md](books-on-this-machine.md) |
| [ByteByteGoHq/ml-bytebytego](https://github.com/ByteByteGoHq/ml-bytebytego) | 28 KB of diagram links, last push 2025-05. Nothing `AIMLInterviews` does not do better |
| [donnemartin/awesome-aws](https://github.com/donnemartin/awesome-aws) | Dormant since 2024-03. AWS's own docs and the [Builders' Library](https://builder.aws.com/learn/topics/builders-library) are the live source, and the corpus already cites them nine times |
| [ramitsurana/awesome-kubernetes](https://github.com/ramitsurana/awesome-kubernetes) | Active, but a platform-role list. Not this reader's loop |
| [mlabonne/llm-course](https://github.com/mlabonne/llm-course), [Hannibal046/Awesome-LLM](https://github.com/Hannibal046/Awesome-LLM) | LLM *fundamentals*. The GenAI design round asks about serving and evaluation: *AI Engineering* (owned) plus the vLLM docs |
| Any "Top N system design questions" repo | The question list is not the scarce thing. The depth follow-up after question three is |

## How to use this file

1. **§3 first.** One weekend on Maelstrom or Hermitage changes how you answer for a year.
2. **§2 as the answer key** — drill a case here, then find the real write-up and diff it.
3. **§1 and §4 on demand**, with a specific question. Never as a reading list.

## Refreshing the local clones

```bash
bash interview-prep/10-resources/fetch-references.sh          # clone or update all
bash interview-prep/10-resources/fetch-references.sh --clean  # delete and re-clone
```

The script prunes any `vendor/` directory not in its `REPOS` list, so dropping a repo here and
from that list is enough. `vendor/` is gitignored and must never be edited — see the `vendor/`
rule in [../../CLAUDE.md](../../CLAUDE.md).

## See also

- [Primary sources](primary-sources.md) — the papers, specs and official docs this corpus cites
- [Engineering blogs and case studies](engineering-blogs.md)
- [Courses and mock interviews](courses-and-mocks.md)

## Referenced by

- [Primary sources](primary-sources.md)
- [Resources index](README.md)

## Sources

- GitHub REST API `/repos/{owner}/{repo}` — push dates, licences, archive status, fetched 2026-09-20
- Link check of every URL in this folder, 2026-09-20 (own analysis)
