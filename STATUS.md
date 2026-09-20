# STATUS

Written when work stopped. Kills the re-entry cost; does not summarise the repo.

| You want | Read |
|---|---|
| **To start working right now** | [docs/NEXT-SESSION.md](docs/NEXT-SESSION.md) — commands, batch 2 |
| The stop point and the traps | This file |
| Why things are the way they are | [docs/WORKLOG.md](docs/WORKLOG.md) |
| Why the structure changed | [docs/adr/0001-split-primitives-into-atomic-fundamentals.md](docs/adr/0001-split-primitives-into-atomic-fundamentals.md) |
| The repo map | [INDEX.md](INDEX.md) |

**Last updated:** 2026-09-02
**Branch:** `docs/fundamentals-batch-1` · **PR #1** (the plan branch) is open and **unmerged**

---

## Where things stopped

The restructure is decided, recorded, and **executing**. Batch 1 is written and verified.

| Layer | State |
|---|---|
| D1–D4 decisions | Answered — all approved, scope = **all 123 topics**. [ADR-0001](docs/adr/0001-split-primitives-into-atomic-fundamentals.md) |
| `interview-prep/fundamentals/` | **5 pages written** (consistency cluster) + README |
| `02-primitives/consistency-and-consensus.md` | Kept, banner added — still uniquely holds clocks + CRDTs |
| Manifest | §7 records the decisions, §8 tracks progress: **5 / 123** |
| `patterns/`, `comparisons/` | Not created yet — they arrive with batches 6–8, deliberately |
| Links / backlinks | 1089 links checked, 4 broken (known placeholders), backlink pass idempotent |

## The next action

Two things, in this order:

1. **Merge PR #1** (`docs/staff-level-restructure` → `main`, squash). It carries only the plan and
   conventions. The merge could not be done from the session — the tool call was blocked by the
   permission classifier — so it needs a click, or `gh pr merge 1 --squash --delete-branch` run by
   you. Then rebase the batch-1 branch on top.
2. **Batch 2 — the replication cluster.** Five files, all `split ←`
   `02-primitives/replication-and-partitioning.md`:
   `partitioning-strategies` · `replication-topologies` ·
   `replication-lag-and-session-guarantees` · `hot-shard-mitigation` · `consistent-hashing`.
   Batch order is in [manifest §6](interview-prep/topics/manifest.md).

Follow the shape of batch 1: research 2–3 sources first, one cited production incident per page,
≥ 2 Mermaid diagram *types*, real arithmetic in "Numbers that matter", then the three scripts.

## Traps — things that will bite on re-entry

| Trap | What to do |
|---|---|
| **`gen_backlinks.py` edits inside code fences** | It matches `## Referenced by` / `## Sources` textually. A fenced example containing those headings gets a generated backlink list injected into it. This happened to `CLAUDE.md` and `CONVENTIONS.md`; both contracts are tables now. **Never put those headings in a fence** |
| **Run doc scripts from the repo root** | `gen_backlinks.py` scoped to a subfolder cannot see inbound links from outside it and strips them as though gone |
| **`lint_docs.py --contract` false positive** | Reports "missing: Follow-up questions" on every staff page. The skill's generic name is `Follow-up questions`; this repo's contract says `Staff-level follow-ups`. Repo wins — ignore that line, do not rename the section |
| **Never rename legacy files to tidy them up** | Inbound links are relative and break silently. Percent-encode the link target instead. `main.md` was fixed this way, not by renaming |
| Legacy filenames contain spaces and parentheses | Escape as `%20` `%28` `%29`; an unescaped `(` breaks on GitHub while looking fine locally |
| Wikilinks are disabled in this vault | Markdown links only. Legacy `[[...]]` stay; add no more |
| **Don't delete a primitive file early** | Delete only when *every* topic it carries has a successor page. `consistency-and-consensus.md` waits for `clocks-and-ordering.md` and `crdts-and-conflict-resolution.md` |
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

Expected today: **1089 links checked, 4 broken** (the placeholders above). Anything else is new
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
