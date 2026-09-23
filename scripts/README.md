# scripts/

| Change | File |
|---|---|
| Are any relative links dead? | `check_links.py` |
| Regenerate every `## Referenced by` list | `gen_backlinks.py` |
| Does a folder meet the section contract / does a topic already exist? | `lint_docs.py` |
| Publish the stacked docs PRs to `main` | `merge-pr-stack.sh` |

Python 3, standard library only — no install step, no requirements file.
**Always run the Python three from the repo root.** `gen_backlinks.py` scoped to a subfolder
cannot see inbound links from outside it and strips them as though they were gone.

## The verify loop

This is the Definition of Done in [CLAUDE.md](../CLAUDE.md). Run it before any commit claims to be
finished, and quote the output — "links verified" is an assertion, the count is the evidence.

```bash
python scripts/gen_backlinks.py .          # run twice; the second must say "0 changed"
python scripts/gen_backlinks.py .
python scripts/check_links.py . --exclude vendor "markdown files"
python scripts/lint_docs.py interview-prep/fundamentals --contract
```

Expected today:

```
233 files scanned, 933 inbound links mapped, 0 changed
checked 2022 relative links; broken: 0
all relative links resolve
```

Backlinks first, then the link check — **generated links are links too**, and a backlink pass that
writes a bad path is the failure this ordering catches.

`--exclude vendor "markdown files"` is what makes the check gateable: it exits 0. Without the
exclusions it exits 1 on four `path/to/…` placeholders inside `markdown files/md_blacklinks.md`,
which are that file's own documentation and are never going to resolve.

## Known noise, do not "fix"

| Output | Why |
|---|---|
| `missing: Follow-up questions` on every staff page | The script ships the generic heading name; this repo's contract says `Staff-level follow-ups`. The repo wins — do not rename the section |
| `not checked: semantic duplicates` | `lint_docs.py` compares filenames. `rate-limiting.md` vs `throttling.md` is invisible to it — that is exactly what the aliases column in [topics/manifest.md](../interview-prep/topics/manifest.md) is for |

## Known bug

**`gen_backlinks.py` writes inside fenced code blocks.** It matches `## Referenced by` and
`## Sources` textually, so a fenced example containing either heading gets a generated backlink
list injected into it. It has already damaged `CLAUDE.md` and `CONVENTIONS.md`; both state their
contract as a table now for that reason. Until the script skips fences, **never put those two
headings inside a code fence anywhere in this repo.**

## Where these came from

`check_links.py`, `gen_backlinks.py` and `lint_docs.py` are vendored verbatim from
`~/.claude/skills/staff-technical-docs/scripts/` as of 2026-09-23. They were copied rather than
referenced so that a clone on any machine can run the Definition of Done. Local edits are fine —
the upstream skill is the origin, not the authority.

## Referenced by

- [STATUS](../STATUS.md)
