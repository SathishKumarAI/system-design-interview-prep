# scripts/

| Change | File |
|---|---|
| Are any relative links dead? | `check_links.py` |
| Regenerate every `## Referenced by` list | `gen_backlinks.py` |
| Does a folder meet the section contract / does a topic already exist? | `lint_docs.py` |
| Publish the stacked docs PRs to `main` | `merge-pr-stack.sh` |
| Render the vault, and check every diagram parses | `preview.py` |
| Fence and inline-code masking the others depend on | `_md.py` |
| Check that masking still works | `test_doc_scripts.py` |

Python 3, standard library only — no install step, no requirements file.
**Always run the Python three from the repo root.** `gen_backlinks.py` scoped to a subfolder
cannot see inbound links from outside it and strips them as though they were gone.

## The verify loop

This is the Definition of Done in [CLAUDE.md](../CLAUDE.md). Run it before any commit claims to be
finished, and quote the output — "links verified" is an assertion, the count is the evidence.

```bash
python scripts/gen_backlinks.py .          # run twice; the second must say "0 changed"
python scripts/gen_backlinks.py .
python scripts/check_links.py .
python scripts/lint_docs.py interview-prep/fundamentals --contract
```

Expected today:

```
233 files scanned, 934 inbound links mapped, 0 changed
checked 2023 relative links; broken: 0
all relative links resolve
```

Backlinks first, then the link check — **generated links are links too**, and a backlink pass that
writes a bad path is the failure this ordering catches.

The check exits 0 with no exclusions needed. It used to exit 1 forever on four `path/to/…`
placeholders inside `markdown files/md_blacklinks.md` — those live in a fenced example and inside
backticks, and the scripts mask code before matching now.

## Known noise, do not "fix"

| Output | Why |
|---|---|
| `missing: Follow-up questions` on every staff page | The script ships the generic heading name; this repo's contract says `Staff-level follow-ups`. The repo wins — do not rename the section |
| `not checked: semantic duplicates` | `lint_docs.py` compares filenames. `rate-limiting.md` vs `throttling.md` is invisible to it — that is exactly what the aliases column in [topics/manifest.md](../interview-prep/topics/manifest.md) is for |

## Code masking — the fix that removed both

`_md.py` owns one job: telling the other scripts which byte offsets are inside a fenced block or
an inline backtick span. `mask_code()` returns a **same-length** copy with those regions blanked,
so a heading or link regex matches on the mask and slices the original. That killed two defects at
once, because they were the same defect pointed in opposite directions:

| Was | Now |
|---|---|
| `gen_backlinks.py` injected a backlink list into any fenced *example* containing `## Referenced by` or `## Sources`. It damaged `CLAUDE.md` and `CONVENTIONS.md` | An example of the format is documentation, not an instance. Headings in fences are left alone |
| `check_links.py` reported `path/to/file.md` in a usage example as broken, forever. Everyone learned to read "4 broken, as expected" — and a real fifth break rode in on that habit | Exits 0 with no exclusions. A number that means something |

Run `python scripts/test_doc_scripts.py` after touching any of this: 13 assertions, no framework,
each named after damage that actually happened.

**One sharp edge, with its own test.** A line like ` ```text``` ` is **not** a fence — CommonMark
says a backtick fence's info string may not contain a backtick, so that is an inline span. Reading
it as an opener masks every line to end of file. `basic/prep/CAP theorem.md:8` is exactly that
shape, and it hid the real `## Referenced by` 19 lines below, making `gen_backlinks.py` append a
second copy on every run. Guarded by `test_same_line_triple_backticks_are_not_a_fence`.

## Where these came from

`check_links.py`, `gen_backlinks.py` and `lint_docs.py` were vendored from
`~/.claude/skills/staff-technical-docs/scripts/` on 2026-09-23 so that a clone on any machine can
run the Definition of Done. `check_links.py` and `gen_backlinks.py` have since **diverged** from
upstream by the code-masking fix above; `_md.py` and `test_doc_scripts.py` are new here and
`lint_docs.py` is still verbatim. The fix should go upstream — the skill still ships the broken
version to every other vault.

## Referenced by

- [STATUS](../STATUS.md)
