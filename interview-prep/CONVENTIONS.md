---
title: File conventions
type: index
track: universal
status: drafted
updated: 2026-09-02
tags: [meta, conventions]
---

# File Conventions — how every note in this repo is written

One format everywhere. You should be able to open any file and know where the
answer is without reading the whole thing. Templates live in
[_templates/](_templates/). Copy, don't improvise.

## 1. Every file starts with frontmatter

```yaml
---
title: Design a news feed          # human title, no "the"
type: case                         # index | topic | case | comparison | playbook | drill | reference | resource | adr | primitive (legacy)
track: backend                     # universal | backend | frontend | data | ml
difficulty: core                   # intro | core | advanced
status: seed                       # seed | drafted | drilled | mastered
sources: [DDIA ch.11, Alex Xu v1 ch.11]
updated: 2026-09-02
tags: [feed, fanout, cache]
---
```

`status` is the study tracker. Move it yourself:

| status | Means |
|---|---|
| `seed` | Stub, title only |
| `drafted` | Content written, never practised |
| `drilled` | Designed it on paper at least once under a timer |
| `mastered` | Two clean 45-minute runs, including failure + cost sections |

Query the board in Obsidian search with `status: drilled` — that's your revision list.

## 2. Heading order is fixed per type

**`case`** (backend / frontend / data / ml design problem) — always these eight, in
this order, even if a section is one line:

`1. Clarify` · `2. Requirements` · `3. Estimates` · `4. API / contract` · `5. Data model` ·
`6. Architecture` · `7. Scale & failure` · `8. Ops & cost` · `Sources & further reading`

Case files being rewritten to the staff contract keep this skeleton **inside**
`Mechanics & internals` and `Numbers that matter` — see the `topic` contract below.

**`topic`** (one mechanism, staff-level — everything new in `fundamentals/`, `patterns/`,
`comparisons/`). This is the current contract; the full description of what each section must
carry is in [../CLAUDE.md](../CLAUDE.md) → *Section contract*:

| # | Heading | Carries |
|---|---|---|
| 1 | `Core concept` | 3–6 lines, no 101 |
| 2 | `Mechanics & internals` | The actual protocol / algorithm / data structure |
| 3 | `Numbers that matter` | Real arithmetic, sourced or marked order-of-magnitude |
| 4 | `Failure modes` | What breaks at scale, with cited incidents |
| 5 | `Trade-offs vs alternatives` | X vs Y vs Z, and where staff engineers get it wrong |
| 6 | `Real-world examples` | Cited, specific systems and versions |
| 7 | `Staff-level follow-ups` | 3–5 multi-part probes, never definitional |
| 8 | `See also` | Hand-written |
| 9 | `Referenced by` | **Generated** by `gen_backlinks.py`. Never hand-edited |
| 10 | `Sources` | |

> [!warning] Trap
> Do not put a literal `## Referenced by` line inside a code fence anywhere in this repo.
> `gen_backlinks.py` matches the heading textually and will inject a backlink list **into your
> example block**. That is why the contract above is a table, not a fenced snippet.

Frontmatter for `topic`/`case` uses `tier: P0|P1|P2` and `status: seed|drafted|reviewed|mastered`
(no `difficulty`). Diagrams: ≥ 2 types per page, reusing
[diagrams/components.md](diagrams/components.md).

**`primitive`** (legacy — the 12 files in `02-primitives/`, being split into `fundamentals/`
per [ADR-0001](../docs/adr/0001-split-primitives-into-atomic-fundamentals.md)). Do not create new
files in this format:

`What it is (3 lines)` · `When to reach for it` · `Options & trade-offs` (table, always) ·
`Failure modes` · `Interview lines` (sentences to say out loud) · `Numbers` ·
`Sources & further reading`

**`index`** (any folder README): first section after the title is a **change → file**
table, so a reader picks the file without opening any other.

## 3. Rules that keep files readable

| Rule | Why |
|---|---|
| Lead with the answer, then the reasoning | You re-read these at 1am before an interview |
| **Tables over prose** for anything comparative | Trade-offs are a grid; prose hides the axis |
| ~300 lines target, 500 hard ceiling | Past that, split by concern and link |
| One concern per file, named after the concern | Search finds it; the index stays short |
| Every claim with a number gets the number | "fast" is not a design input |
| Code fences get a language tag | Obsidian + GitHub both highlight |
| Links are **markdown**, not wikilinks | This vault has `Use Wikilinks` disabled (see root README) |
| Relative links only (`../02-primitives/cache.md`) | Survives the repo being cloned or moved |
| Spaces in filenames get `%20` in links | Otherwise the link breaks on GitHub |
| A file that goes stale gets `status: seed` again | Lying notes cost more than missing ones |

## 4. Naming

- Files: `kebab-case.md`. No spaces in new files, ever. (Old notes keep their names —
  renaming breaks their inbound links.)
- Folders: `NN-topic/` numbered so sort order = study order.
- One folder per track; a case never lives in two places — cross-link instead.

## 5. Callouts

Obsidian callout syntax, used sparingly and only for these four:

```markdown
> [!tip] Interview line
> "I'd fan out on write for normal users and read for celebrities."

> [!warning] Trap
> Fanout on write dies on the celebrity account. Always say it before they ask.

> [!info] Number
> 100M DAU × 10 reads/day ≈ 12k rps average, ~50k peak.

> [!question] Drill
> Redesign this for 100x writes and a 50ms p99. What breaks first?
```

## 6. Sources

Every file ends with `## Sources & further reading`, listing:

1. **Local books** — path relative to the library root, with chapter.
   See [10-resources/books-on-this-machine.md](10-resources/books-on-this-machine.md).
2. **Upstream repos** — path inside `10-resources/vendor/`.
3. **Web** — full markdown links.

No source, no claim. If it's your own reasoning, say `(own analysis)`.

## 7. When you add a new file

1. Copy the matching template from [_templates/](_templates/).
2. Fill frontmatter first — `status: seed` is fine.
3. Add one line to the folder's `README.md` change → file table.
4. If it's a case, add it to [07-drills/question-bank.md](07-drills/question-bank.md).

That's the whole ritual. Three steps, or the index rots and the repo becomes a pile.

## Referenced by

- [ADR-0001: Split bundled primitives into atomic fundamentals pages](../docs/adr/0001-split-primitives-into-atomic-fundamentals.md)
- [CLAUDE.md — system-design-prep](../CLAUDE.md)
- [Diagram component library](diagrams/components.md)
- [Fundamentals index](fundamentals/README.md)
- [Interview prep index](README.md)
- [Repo index](../INDEX.md)
- [System Design Interview Preparation](../README.md)
- [Topic manifest](topics/manifest.md)
