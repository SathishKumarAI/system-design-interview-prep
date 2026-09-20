---
title: Resources index
type: index
track: universal
status: drafted
updated: 2026-09-02
tags: [index, resources]
---

# Resources

Everything external, in one place, with a **verdict** on each — a list without verdicts is just
a bookmark folder.

| Question | File |
|---|---|
| What books do I already own, and which chapter do I read? | [books-on-this-machine.md](books-on-this-machine.md) |
| Which GitHub repos, and what are they good for? | [github-repos.md](github-repos.md) |
| What do I subscribe to? | [newsletters-substack.md](newsletters-substack.md) |
| Which subreddits and communities? | [reddit-communities.md](reddit-communities.md) |
| Which engineering blogs, and which posts? | [engineering-blogs.md](engineering-blogs.md) |
| Paid courses and mock interviews — worth it? | [courses-and-mocks.md](courses-and-mocks.md) |

## Upstream repos, cloned locally

`vendor/` holds shallow clones of the best open-source system-design repos. It is **gitignored**
and **never edited** — refresh with:

```bash
bash interview-prep/10-resources/fetch-references.sh
```

Currently vendored:

| Repo | Use it for |
|---|---|
| `system-design-primer` | The canonical free curriculum + worked exercises |
| `system-design-101` | ByteByteGo's visual explanations |
| `awesome-system-design-resources` | Curated index of everything else |
| `system-design` (karanpratapsingh) | Clean written course |
| `Machine-Learning-Interviews` | ML system design framework + questions |
| `machine-learning-systems-design` | Chip Huyen's ML design question set |
| `applied-ml` | Real company ML case studies, by topic |
| `awesome-scalability` | Architecture case studies by scale problem |
| `front-end-interview-handbook` | Frontend system design |
| `system-design-interview` (checkcheckzz) | Older but dense link collection |

## How to use resources without wasting time

| Anti-pattern | Do instead |
|---|---|
| Collecting resources | Pick **one** primary source per topic and finish it |
| Reading passively | Drill first, read to fill the gap the drill exposed |
| Watching videos as study | Videos are for a first pass only; the learning is in the timed drill |
| Buying three courses | One course + this repo + timed practice beats three courses |
| Reading every case study | Read the two that match your target company's product |

**Priority order if you only have limited time:**
1. This repo's [00-interview-playbook.md](../00-interview-playbook.md) + [01-numbers.md](../01-numbers.md)
2. Timed drills from [../07-drills/question-bank.md](../07-drills/question-bank.md)
3. DDIA chapters 5–9 (you own it — see [books-on-this-machine.md](books-on-this-machine.md))
4. Your target company's engineering blog
5. Everything else

## Referenced by

- [Interview prep index](../README.md)
- [Repo index](../../INDEX.md)
- [System Design Interview Preparation](../../README.md)
