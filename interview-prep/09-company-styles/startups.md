---
title: Startups and scale-ups
type: reference
track: universal
status: drafted
updated: 2026-09-02
tags: [startups, pragmatism]
---

# Startups and scale-ups

## What's different

The single biggest difference: **big-tech-shaped answers actively hurt you here.** Proposing
Kafka, Kubernetes and a service mesh for a product with 5,000 users signals that you'd burn six
months of a small team's runway on infrastructure.

| | Big tech | Startup |
|---|---|---|
| Scale framing | Billions of users, assume it | Real current numbers; growth is a *maybe* |
| What's scored | Depth, correctness at scale | **Judgement about what not to build** |
| Cost | A line item | Sometimes existential |
| Team | Specialists, platform teams | You are the platform team |
| Success | The system scales | The product ships and can be changed next week |

## What they're actually testing

1. **Can you ship?** What is v1, and how fast?
2. **Do you know what to skip?** Which complexity is premature here?
3. **Can you operate it alone?** Because you will, at 2am, with no SRE.
4. **Do you understand cost?** A $30k/month bill can be a meaningful fraction of burn.
5. **Can you evolve it?** Where are the seams that let v2 differ from v1 without a rewrite?

## The answer shape that wins

> "For 10k users I'd run a monolith on a managed platform with Postgres, Redis and an object
> store — three components, one deploy, one thing to page on. Postgres handles the queue with
> `SKIP LOCKED` until we need more than a few hundred jobs a second. That gets us to roughly
> 100k users. The seams I'd keep clean are the storage layer and the job interface, so when
> writes actually become the bottleneck we can shard or move to Kafka without rewriting the
> product. Here's the metric that would tell us it's time."

That paragraph contains: a v1, a justification, a scaling limit, a stated seam, and a trigger for
the next change. It's a better answer than a correct 20-box diagram.

## Specific "don't" list

| Don't propose | Unless |
|---|---|
| Microservices | Multiple teams genuinely need independent deploys |
| Kubernetes | You already need multi-service orchestration and someone will own it |
| Kafka | You need replay or multiple independent consumers of the same events |
| A service mesh | You have 20+ polyglot services |
| A custom framework | An existing one is measurably wrong for you |
| Multi-region | There's a stated latency or compliance requirement |
| A separate analytics stack | Read replicas plus a warehouse export isn't enough |
| Your own ML platform | You're running more than a handful of models |

Each of these can be right — but you must name the requirement that forces it.

## The Postgres-does-that answer

Worth knowing, because it lands very well at startups: modern Postgres can serve as your queue
(`SKIP LOCKED`), your cache (with care), your full-text search (`tsvector`), your vector index
(`pgvector`), your time-series store (Timescale), your JSON document store (`jsonb`), and your
analytics store at small scale. **One system to operate, back up and monitor** is worth an
enormous amount to a five-person team.

Say it as a deliberate trade, not as ignorance of the alternatives: *"I'd use Postgres for the
queue until we exceed a few hundred jobs a second, then move to SQS — the migration is a day, and
until then we've avoided operating a second system."*

## Interview mechanics at startups

- Rounds are often longer and more conversational, sometimes with a founder or CTO.
- You may be asked to design something they are *actually building* — treat it as a real design
  review and ask real questions.
- Expect trade-off questions about **speed vs quality**: "you have two weeks, what ships?"
- Take-homes and pair-programming are more common than at big tech.
- Culture fit is often decisive, and "can we work with this person at 11pm during an incident"
  is a real, unstated criterion.

## Questions to ask them

Good questions here double as signal that you think about systems in context:

- What breaks most often today?
- What's the on-call load, and who carries it?
- What's the monthly infrastructure bill, and what dominates it?
- What decision from a year ago do you most regret?
- What would you rebuild if you had a free month?

## Referenced by

- [Company interview styles](README.md)
