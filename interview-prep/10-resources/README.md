---
title: Resources index
type: index
track: universal
status: drafted
updated: 2026-09-20
tags: [index, resources]
---

# Resources

Everything external, in one place, with a **verdict** on each — a list without verdicts is just
a bookmark folder.

| Question | File |
|---|---|
| What books do I already own, and which chapter do I read? | [books-on-this-machine.md](books-on-this-machine.md) |
| Which GitHub repos, and what are they good for? | [github-repos.md](github-repos.md) |
| Which paper / spec / official doc does this corpus actually cite? | [primary-sources.md](primary-sources.md) |
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

The script **prunes** any directory not in its `REPOS` list, so removing a repo from the list is
enough to remove it from disk on the next run.

Currently vendored (16 repos, 100 MB measured, 2026-09-20):

| Repo | Use it for |
|---|---|
| `maelstrom` | **Implement a replicated KV store and have Jepsen break it.** The one runnable thing here |
| `hermitage` | The SQL that produces each isolation anomaly, with per-database results |
| `distsys-class` | Kingsbury's consistency-model notes |
| `post-mortems` | Annotated public postmortems, grouped by failure class |
| `howtheysre` | Company-by-company SRE practice |
| `testing-distributed-systems` | How distributed systems get verified: Jepsen, TLA+, DST |
| `awesome-distributed-systems` | A short papers-and-talks list |
| `awesome-database-learning` | The storage-engine reading path, in order |
| `system-design-primer` | The canonical free curriculum + worked exercises |
| `system-design-101` | ByteByteGo's visual explanations |
| `awesome-system-design-resources` | Curated index of everything else |
| `system-design` (karanpratapsingh) | Clean written course |
| `AIMLInterviews` | ML system design framework + questions (renamed from `Machine-Learning-Interviews`) |
| `applied-ml` | Real company ML case studies, by topic |
| `awesome-scalability` | Architecture case studies by scale problem |
| `front-end-interview-handbook` | Frontend system design |

Dropped 2026-09-20: `machine-learning-systems-design` (superseded by the author's own book, on
this machine) and `system-design-interview` (checkcheckzz) (2017-era link dump, last push
2023-04). Reasons in [github-repos.md](github-repos.md) §5.

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

**If you have a weekend rather than an hour:** `vendor/maelstrom`. Reading about linearizability
and watching a checker reject your own implementation are different kinds of knowing, and only
one of them survives a follow-up question.

## Referenced by

- [Interview prep index](../README.md)
- [Repo index](../../INDEX.md)
- [System design prep](../../README.md)
