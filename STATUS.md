# STATUS

Written when work stopped. Kills the re-entry cost; does not summarise the repo.

| You want | Read |
|---|---|
| **To start working right now** | [docs/NEXT-SESSION.md](docs/NEXT-SESSION.md) — commands and the verify loop |
| **To finish publishing the work** | `bash scripts/merge-pr-stack.sh` — PRs #2–#9 |
| The stop point and the traps | This file |
| Why things are the way they are | [docs/WORKLOG.md](docs/WORKLOG.md) |
| Unscheduled ideas worth keeping | [docs/BACKLOG.md](docs/BACKLOG.md) |
| What happened last session, mistakes included | [docs/sessions/2026-09-02-fundamentals-batches-1-5.md](docs/sessions/2026-09-02-fundamentals-batches-1-5.md) |
| Why the structure changed | [docs/adr/0001-split-primitives-into-atomic-fundamentals.md](docs/adr/0001-split-primitives-into-atomic-fundamentals.md) |
| The repo map | [INDEX.md](INDEX.md) |

**Last updated:** 2026-09-23
**Branch:** `build/vendor-doc-scripts` — the tip of a 14-branch linear stack
**PRs:** #1 **merged** 2026-09-23 · #2–#9 open and now *conflicting* — see the next action

The stack, oldest first, is exactly the `STACK` list in
[`scripts/merge-pr-stack.sh`](scripts/merge-pr-stack.sh). Four of its branches have no PR yet and
two — `docs/resources-audit`, `docs/applied-sections` — had never been pushed at all. The script
pushes and opens them as it goes.

---

## Where things stopped

The restructure is decided, recorded, and **executing**. Batches 1–8 wrote the mechanism layer;
batches 9–12 raised the existing corpus instead of adding topics. **The 26 case files still have
not been rewritten to the staff contract** — that is the open work, and it is the largest single
gap in the repo.

| Layer | State |
|---|---|
| D1–D4 decisions | Answered — all approved, scope = **all 123 topics**. [ADR-0001](docs/adr/0001-split-primitives-into-atomic-fundamentals.md) |
| `interview-prep/fundamentals/` | **25 pages** (consistency · replication · storage+caching · messaging · reliability) + README |
| `interview-prep/comparisons/` | **5 pages** (SQL vs NoSQL · OLTP engines · messaging · consistency defaults · batch vs streaming) + README. **Folder created in batch 8** |
| `interview-prep/patterns/` | **10 pages** — atomicity (outbox · saga · 2PC · derived data · expand–contract) and blast radius (fanout · cells · degradation · breakers · backfill) + README |
| `interview-prep/11-behavioural/` | **3 pages** + README — question bank, rubric, and an empty story inventory only the reader can fill. **Folder created 2026-09-21, still absent from the manifest** |
| Applied sections | `## On AWS and Azure` + `## In an LLM deployment` now on **67 files**. Contract in [`_templates/applied-sections.md`](interview-prep/_templates/applied-sections.md); **not yet added to the section-contract table in CLAUDE.md** |
| Case diagrams | All 26 cases carry a `flowchart` **and** a `sequenceDiagram`, ASCII sketches removed. One exception: `06-ml-cases/feed-ranking.md` has a `stateDiagram` where the sequence should be |
| Case **content** | **0 of 26 rewritten.** Every case still runs the old `## 1. Clarify … ## 8. Ops & cost` skeleton and carries none of the ten contract headings. They also end `## Sources & further reading`, not `## Sources` |
| `02-primitives/` split so far | **7 of 12 files**, all kept and banner-marked, each still holding at least one topic with no successor: `consistency-and-consensus` (clocks, CRDTs) · `replication-and-partitioning` (rebalancing) · `caching` (Redis internals) · `storage-and-databases` (store selection, object storage, schema evolution) · `messaging-and-streams` (backpressure) · `transactions-and-idempotency` (2PC, outbox, sagas, ledgers) · `reliability-patterns` (**down to bulkheads and DR**). `transactions-and-idempotency` is down to **ledgers only** and is retired when `ledgers-and-double-entry.md` lands |
| `02-primitives/` **not started** | The other **5 of 12** have no successor page at all and no banner: `networking-and-edge` · `load-balancing-and-gateways` · `observability-and-delivery` · `security-and-multitenancy` · `cost-engineering`. That is 20 unwritten topics and five whole domains with nothing in `fundamentals/` |
| Manifest | §7 records the decisions, §8 tracks progress: **40 / 123** topic pages. Batches 9–12 added no topic pages, so the count is unchanged and correct |
| `08-reference/tech-selection.md` | **Not retired** — it still uniquely covers 13 decisions with no comparison page yet. Banner added; becomes a stub when they land |
| Links / backlinks | **2023 links checked, 0 broken** with `--exclude vendor "markdown files"`; without the exclusions, the four `path/to/…` placeholders in `markdown files/md_blacklinks.md` make it exit 1. Backlink pass idempotent |

## The next action

Four things, in this order:

1. **Finish merging the stack: `bash scripts/merge-pr-stack.sh`.** PR #1 is squash-merged. That
   rewrote history, so #2–#9 now report `CONFLICTING` even though their content is unchanged —
   their merge-base went stale. The script drops each already-merged prefix with
   `git rebase --onto` and re-pushes, which replays cleanly because `origin/main` is tree-identical
   to the commit each batch sits on. It cannot be run from a Claude session: `git rebase` and
   `git push --force-with-lease` are both blocked by the auto-mode classifier.
2. ~~**Publish the front door.**~~ Done — the root `README.md` now leads with the layer table and
   links `fundamentals/`, `patterns/`, `comparisons/` and `11-behavioural/`. It reaches readers
   only once step 1 lands.
3. ~~**Vendor the doc scripts.**~~ Done — `check_links.py`, `gen_backlinks.py` and `lint_docs.py`
   are in [`scripts/`](scripts/README.md). The Definition of Done now runs from a bare clone.
4. **Batch 13 — the first case rewrites.** A genuinely different kind of work: five existing case
   files rewritten **in place** to the staff contract, keeping the design skeleton (Clarify ·
   Requirements · Estimates · API · Data model · Architecture · Scale & failure · Ops & cost)
   *inside* `Mechanics & internals` and `Numbers that matter`:
   `news-feed` · `chat-messaging` · `ride-hailing` · `payments-ledger` · `ticket-booking` (new).

The case rewrites are where the 40 pages already written start paying off: a case should **link to
the mechanism pages rather than re-explaining them**, and spend its length on the design decisions,
the estimates and the failure analysis that are specific to *this* problem. A case that re-teaches
fan-out or idempotency is a case that has not used the set.

## Traps — things that will bite on re-entry

| Trap | What to do |
|---|---|
| **Squash-merging a stacked PR breaks every PR above it** | The branches are strictly linear ancestors of each other. Squashing #1 gave `main` a commit that is not in any branch's history, so #2's merge-base went stale and GitHub called it `CONFLICTING` — the content had not changed at all. Never `gh pr merge` a stack in a loop. Use `scripts/merge-pr-stack.sh`, which rebases each branch onto the new `main` first |
| **`git rebase` and `git push --force` are blocked in Claude sessions** | The auto-mode classifier denies both. Anything needing them goes in a `scripts/*.sh` the human runs |
| **Python `write_text` turns a whole LF file CRLF on Windows** | A read-modify-write of a doc silently rewrites every line ending. Harmless here — `core.autocrlf=true`, so the committed blob is unaffected and `git diff` stays empty — but a byte-level diff of the working tree will look like the whole file changed. Write bytes, or pass `newline="
"`, when that matters |
| **`gen_backlinks.py` edits inside code fences** | It matches `## Referenced by` / `## Sources` textually. A fenced example containing those headings gets a generated backlink list injected into it. This happened to `CLAUDE.md` and `CONVENTIONS.md`; both contracts are tables now. **Never put those headings in a fence** |
| **Run doc scripts from the repo root** | `gen_backlinks.py` scoped to a subfolder cannot see inbound links from outside it and strips them as though gone |
| **`lint_docs.py --contract` false positive** | Reports "missing: Follow-up questions" on every staff page. The skill's generic name is `Follow-up questions`; this repo's contract says `Staff-level follow-ups`. Repo wins — ignore that line, do not rename the section |
| **Never rename legacy files to tidy them up** | Inbound links are relative and break silently. Percent-encode the link target instead. `main.md` was fixed this way, not by renaming |
| Legacy filenames contain spaces and parentheses | Escape as `%20` `%28` `%29`; an unescaped `(` breaks on GitHub while looking fine locally |
| Wikilinks are disabled in this vault | Markdown links only. Legacy `[[...]]` stay; add no more |
| **Don't delete a primitive file early** | Delete only when *every* topic it carries has a successor page. `consistency-and-consensus.md` waits for `clocks-and-ordering.md` + `crdts-and-conflict-resolution.md`; `replication-and-partitioning.md` waits for `rebalancing-and-resharding.md` |
| `interview-prep/10-resources/vendor/` | ~100 MB of upstream clones. Gitignored, read-only. Refresh with `fetch-references.sh` |
| `markdown files/md_blacklinks.md` | Reports 4 "broken links" forever — `{rel_path}` placeholders in a script's own docs. Expected noise |
| Windows console + skill-creator viewer | `generate_review.py` server mode crashes on cp1252. Prefix `PYTHONIOENCODING=utf-8 PYTHONUTF8=1`, or use `--static` |
| Quoted heredocs in the Bash tool | `<<'EOF'` leaks apostrophes into the shell parser. Use the Write tool for file content |

## Verify before claiming anything is done

```bash
python scripts/gen_backlinks.py .   # run twice: second must say "0 changed"
python scripts/gen_backlinks.py .
python scripts/check_links.py . --exclude vendor "markdown files"
python scripts/lint_docs.py interview-prep/fundamentals --contract
```

Expected today:

```
233 files scanned, 933 inbound links mapped, 0 changed
checked 2023 relative links; broken: 0
```

Anything else is new breakage. Quote the output — "links verified" is an assertion, the count is
evidence. Backlinks run **first**: generated links are links too.

The exclusions are what make the check exit 0. Without them it exits 1 on the four `path/to/…`
placeholders in `markdown files/md_blacklinks.md`, which are that file's own documentation.

Full notes on the scripts, their known noise and the fenced-code bug: [scripts/README.md](scripts/README.md).

## Related work outside this repo

`~/.claude/skills/staff-technical-docs/` — the method as a reusable skill. Three open items:
`evals/evals.json` v2 has never been run; eval-3's fixture (`fixtures/existing-set/`) is specified
but not built; and `gen_backlinks.py` should skip fenced code blocks — this repo hit that bug today
and worked around it in the docs rather than in the script.

## Referenced by

- [Backlog — ideas not scheduled](docs/BACKLOG.md)
- [CLAUDE.md — system-design-prep](CLAUDE.md)
- [Docs index](docs/README.md)
- [Next session — start here](docs/NEXT-SESSION.md)
- [Repo index](INDEX.md)
- [Session record — fundamentals batches 1–5](docs/sessions/2026-09-02-fundamentals-batches-1-5.md)
- [System design prep](README.md)
- [Worklog](docs/WORKLOG.md)
