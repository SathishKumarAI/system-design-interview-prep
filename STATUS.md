# STATUS

Written when work stopped. Kills the re-entry cost; does not summarise the repo.

| You want | Read |
|---|---|
| **To start working right now** | [docs/NEXT-SESSION.md](docs/NEXT-SESSION.md) — commands, batch 4 |
| The stop point and the traps | This file |
| Why things are the way they are | [docs/WORKLOG.md](docs/WORKLOG.md) |
| Why the structure changed | [docs/adr/0001-split-primitives-into-atomic-fundamentals.md](docs/adr/0001-split-primitives-into-atomic-fundamentals.md) |
| The repo map | [INDEX.md](INDEX.md) |

**Last updated:** 2026-09-02
**Branch:** `docs/fundamentals-batch-3` · **PRs #1–#4** open, none merged

---

## Where things stopped

The restructure is decided, recorded, and **executing**. Batches 1–3 are written and verified.

| Layer | State |
|---|---|
| D1–D4 decisions | Answered — all approved, scope = **all 123 topics**. [ADR-0001](docs/adr/0001-split-primitives-into-atomic-fundamentals.md) |
| `interview-prep/fundamentals/` | **15 pages written** (consistency · replication · storage+caching) + README |
| `02-primitives/` split so far | 4 of 12 files: `consistency-and-consensus` (holds clocks + CRDTs), `replication-and-partitioning` (rebalancing), `caching` (Redis internals), `storage-and-databases` (store selection, object storage, schema evolution). All kept and banner-marked |
| Manifest | §7 records the decisions, §8 tracks progress: **15 / 123** |
| `patterns/`, `comparisons/` | Not created yet — they arrive with batches 6–8, deliberately |
| Links / backlinks | 1286 links checked, 4 broken (known placeholders), backlink pass idempotent |

## The next action

Two things, in this order:

1. **Merge the open PRs, oldest first** — #1 (plan) → #2 (batch 1) → #3 (batch 2) → #4
   (batch 3). They are stacked, so each retargets to `main` as the one below it lands. The
   session could not merge them (`gh pr merge` blocked by the permission classifier):
   `gh pr merge 1 --squash --delete-branch`, then 2, 3, 4.
2. **Batch 4 — messaging and delivery.** Five files, all `split ←`
   `02-primitives/messaging-and-streams.md` except the last:
   `log-vs-queue` · `kafka-internals` · `delivery-semantics` · `stream-processing-semantics` ·
   `idempotency` (this one `split ←` `transactions-and-idempotency.md`).
   Batch order is in [manifest §6](interview-prep/topics/manifest.md).

Follow the shape of batches 1–3: research 2–3 sources first, one cited production incident per
page, ≥ 2 Mermaid diagram *types*, real arithmetic in "Numbers that matter", then the three
scripts. Batch 4 again splits two source files, and neither gets deleted —
`messaging-and-streams.md` still owns backpressure/consumer-lag, `transactions-and-idempotency.md`
still owns 2PC, sagas, outbox and ledgers.

## Traps — things that will bite on re-entry

| Trap | What to do |
|---|---|
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
python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .
python ~/.claude/skills/staff-technical-docs/scripts/gen_backlinks.py .   # run twice: second must say "0 changed"
python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .     # backlinks are links too
python ~/.claude/skills/staff-technical-docs/scripts/lint_docs.py interview-prep/fundamentals --contract
```

Expected today: **1286 links checked, 4 broken** (the placeholders above). Anything else is new
breakage. Quote the output — "links verified" is an assertion, the count is evidence.

## Related work outside this repo

`~/.claude/skills/staff-technical-docs/` — the method as a reusable skill. Three open items:
`evals/evals.json` v2 has never been run; eval-3's fixture (`fixtures/existing-set/`) is specified
but not built; and `gen_backlinks.py` should skip fenced code blocks — this repo hit that bug today
and worked around it in the docs rather than in the script.

## Referenced by

- [CLAUDE.md — system-design-prep](CLAUDE.md)
- [Docs index](docs/README.md)
- [Next session — start here](docs/NEXT-SESSION.md)
- [Repo index](INDEX.md)
- [Worklog](docs/WORKLOG.md)
