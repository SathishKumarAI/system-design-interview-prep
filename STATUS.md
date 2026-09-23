# STATUS

Written when work stopped. Kills the re-entry cost; does not summarise the repo.

| You want | Read |
|---|---|
| **To start working right now** | [docs/NEXT-SESSION.md](docs/NEXT-SESSION.md) — decision, commands, batch 1 |
| The stop point and the traps | This file |
| Why things are the way they are | [docs/WORKLOG.md](docs/WORKLOG.md) |
| What happened last session, dead ends included | [docs/sessions/](docs/sessions/) |
| The repo map | [INDEX.md](INDEX.md) |

**Last updated:** 2026-09-02
**Branch:** `docs/staff-level-restructure` — committed, **not merged, no PR opened**

---

## Where things stopped

The prep set exists and is internally consistent. The *plan* to take it from prep-grade to
staff-grade exists and is reviewed. **Execution of that plan has not started** — it is blocked on
one decision, below.

| Layer | State |
|---|---|
| `interview-prep/` 75 files | Written, verified, committed |
| `interview-prep/topics/manifest.md` | 123 topics planned, tiered, alias-protected |
| `interview-prep/diagrams/components.md` | Shared Mermaid vocabulary, 11 snippets |
| `CLAUDE.md`, `INDEX.md`, `CONVENTIONS.md`, `_templates/` | Written |
| The 63 P0 rewrites the manifest calls for | **Not started** |
| `~/.claude/skills/staff-technical-docs/` | Built, benchmarked, iterated once |

## The next action

Answer **D1–D4** in [`interview-prep/topics/manifest.md`](interview-prep/topics/manifest.md) §7.
Each has a recommendation already written; "go with the recommendations" is a valid answer.

| | Decision | Recommendation |
|---|---|---|
| D1 | Rename `02-primitives/` → `fundamentals/` and split 12 files into ~47 | Yes — this is what makes the set staff-level rather than a glossary |
| D2 | Add `patterns/` and `comparisons/`, retire `08-reference/tech-selection.md` into the latter | Yes |
| D3 | Write all 123 topics, or P0 only (63) | P0 only |
| D4 | Rewrite case files in place, or move under `case-studies/` | In place — moving breaks every inbound link |

Then: Batch 1 is the consistency cluster (`consistency-models`, `transaction-isolation-levels`,
`consensus-raft-paxos`, `leases-locks-and-fencing`, `quorums-and-anti-entropy`). Batch order is in
manifest §6. Five files per batch, review between batches.

## Traps — things that will bite on re-entry

| Trap | What to do |
|---|---|
| **Never rename legacy files to tidy them up** | Inbound links are relative and break silently. This is how the 5 broken links found this session were created. Percent-encode the link, don't rename the file |
| Legacy filenames contain spaces and parentheses | Escape as `%20` `%28` `%29`. An unescaped `(` truncates the target and breaks on GitHub while looking fine locally |
| Wikilinks are disabled in this vault | Markdown links only. Legacy `[[...]]` stay; add no more |
| `interview-prep/10-resources/vendor/` | ~100 MB of upstream clones. Gitignored, read-only. Refresh with `fetch-references.sh` |
| **Run doc scripts from the repo root** | `gen_backlinks.py` scoped to a subfolder cannot see inbound links from outside it and will strip them as though they no longer exist |
| `markdown files/md_blacklinks.md` | Reports 4 "broken links" forever — they are `{rel_path}` template placeholders in a script's own docs, not real links. Expected noise |
| Windows console + skill-creator viewer | `generate_review.py` server mode crashes on cp1252. Prefix with `PYTHONIOENCODING=utf-8 PYTHONUTF8=1`, or use `--static` |
| Quoted heredocs in the Bash tool | `<<'EOF'` leaks apostrophes into the shell parser. Use the Write tool for file content instead |

## Verify before claiming anything is done

```bash
python ~/.claude/skills/staff-technical-docs/scripts/check_links.py .
python ~/.claude/skills/staff-technical-docs/scripts/lint_docs.py interview-prep --contract
python ~/.claude/skills/staff-technical-docs/scripts/gen_backlinks.py .   # then re-run check_links
```

Expected today: 478 links checked, 4 broken (the placeholder noise above). Anything else is new
breakage. Quote the output — "links verified" is an assertion, the count is evidence.

## Related work outside this repo

`~/.claude/skills/staff-technical-docs/` — the method extracted as a reusable skill, with an eval
set and benchmark. Its `evals/evals.json` v2 has an unbuilt fixture (`fixtures/existing-set/`) for
eval-3; that is the next thing to do there if the skill is picked back up.
