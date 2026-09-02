---
title: GitHub repositories
type: resource
track: universal
status: drafted
updated: 2026-09-02
tags: [github, repos]
---

# GitHub repositories

Cloned into `vendor/` (gitignored) by [fetch-references.sh](fetch-references.sh). Verdicts are
what matter — most of these overlap heavily, and reading all of them is a waste of a month.

## Vendored here

| Repo | Verdict | Use it for |
|---|---|---|
| [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) | **The canonical free curriculum.** Start here if you start anywhere | Concepts, latency numbers, worked exercises with solutions under `solutions/system_design/` |
| [ByteByteGoHq/system-design-101](https://github.com/ByteByteGoHq/system-design-101) | Excellent diagrams, shallow text | Visual first-pass on a concept; good for revision, bad for depth |
| [ashishps1/awesome-system-design-resources](https://github.com/ashishps1/awesome-system-design-resources) | Best-maintained curated index in 2026 | Finding the one good article on a specific topic |
| [karanpratapsingh/system-design](https://github.com/karanpratapsingh/system-design) | Clean, linear written course | A structured read-through if the primer feels scattered |
| [alirezadir/Machine-Learning-Interviews](https://github.com/alirezadir/Machine-Learning-Interviews) | **The best free ML system design material** | `src/MLSD/ml-system-design.md` — framework + worked ML cases |
| [chiphuyen/machine-learning-systems-design](https://github.com/chiphuyen/machine-learning-systems-design) | Question set + short book | ML design questions to drill |
| [eugeneyan/applied-ml](https://github.com/eugeneyan/applied-ml) | **Curated real company ML case studies by topic** | Finding how a real company solved the case you just drilled |
| [binhnguyennus/awesome-scalability](https://github.com/binhnguyennus/awesome-scalability) | Enormous link list, organised by scaling problem | Deep dives after you know what you're looking for |
| [yangshun/front-end-interview-handbook](https://github.com/yangshun/front-end-interview-handbook) | The frontend standard | Front-end system design section; RADIO framework |
| [checkcheckzz/system-design-interview](https://github.com/checkcheckzz/system-design-interview) | Older, still dense | Company-specific architecture links |

## Worth knowing about, not vendored

| Repo | Use it for |
|---|---|
| [ashishps1/awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design) | The *other* design round — OOD/LLD, which many loops also include |
| [kilimchoi/engineering-blogs](https://github.com/kilimchoi/engineering-blogs) | The definitive list of company engineering blogs |
| [donnemartin/awesome-aws](https://github.com/donnemartin/awesome-aws) | AWS-specific depth |
| [ByteByteGoHq/ml-bytebytego](https://github.com/ByteByteGoHq/ml-bytebytego) | ML system design diagrams |
| [ramitsurana/awesome-kubernetes](https://github.com/ramitsurana/awesome-kubernetes) | If the role is platform/infra |
| [mlabonne/llm-course](https://github.com/mlabonne/llm-course) | LLM fundamentals if the GenAI round is new to you |
| [Hannibal046/Awesome-LLM](https://github.com/Hannibal046/Awesome-LLM) | LLM papers and tooling index |

## How to actually use them

1. **Pick one primary** (`system-design-primer`) and finish its concept section. Don't graze.
2. **Use `applied-ml` and `awesome-scalability` as answer keys** — after you drill a case here,
   find the real company write-up and diff.
3. **Use `awesome-system-design-resources` as a search index**, not a reading list.
4. **Ignore the rest until a specific gap sends you there.**

> [!warning] Trap
> Repo collecting feels like progress and isn't. Ten starred repos and zero timed drills is the
> most common failed preparation pattern there is.

## Refreshing the local clones

```bash
bash interview-prep/10-resources/fetch-references.sh          # clone or update all
bash interview-prep/10-resources/fetch-references.sh --clean  # delete and re-clone
```

`vendor/` is gitignored and must never be edited — treat it as read-only upstream, per the
`vendor/` rule in [../../CLAUDE.md](../../CLAUDE.md).

## Referenced by

- [Resources index](README.md)
