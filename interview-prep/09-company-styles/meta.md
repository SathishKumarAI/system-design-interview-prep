---
title: Meta interview style
type: reference
track: universal
status: drafted
sources: [Exponent 2026, IGotAnOffer, DesignGurus]
updated: 2026-09-02
tags: [meta, faang]
---

# Meta

## What makes Meta different

- **45 minutes, and it is short.** Time management is itself a scored skill. Design rounds
  typically appear **twice** — once in the technical screen and again onsite.
- **Two tracks.** The recruiter assigns you (sometimes with a choice):
  - **Product architecture** — design a user-facing product's backend end to end: entities, API,
    data model, then scale. Product sense matters.
  - **System design (infrastructure)** — backend distributed systems at massive scale, for
    SWE-Infra candidates.
    Ask your recruiter which one you're getting. Preparing for the wrong track is a common
    self-inflicted failure.
- **Scale is assumed to be enormous.** Billions of users is the default framing; your numbers
  should reflect it without prompting.
- **Behavioural is a separate round**, not woven into design (the opposite of Amazon).

## Scored competencies

Meta's infra design round is evaluated on four:

| Competency | What it looks like |
|---|---|
| **Problem navigation** | Extract requirements, scope aggressively, pick what matters in a 45-minute budget |
| **Solution design** | A coherent end-to-end design where every component is justified |
| **Technical excellence** | Real depth — data model, partitioning, consistency, failure |
| **Communication** | Structured, narrated, legible diagram, responsive to hints |

## Level calibration — the thing that actually decides your offer

The same prompt is given at E4, E5 and E6; the expectation differs completely.

| Level | Expectation |
|---|---|
| **E4** | Clean architecture, sensible trade-offs, a reasonable deep dive |
| **E5** | Drives the round unprompted; owns the trade-offs; goes properly deep on at least one component; covers failure |
| **E6** | Frames the problem, questions requirements, discusses migration paths, org/team implications, and connects the design to systems beyond the immediate scope |

**An E4-quality answer from an E6 candidate is the single most common route to a down-level.**
Correctness is not the bar above E4 — scope and judgement are.

## Running a 45-minute Meta round

| Minutes | Do |
|---|---|
| 0–5 | Requirements + scale numbers. Be fast and decisive; don't over-clarify |
| 5–10 | API + data model |
| 10–20 | High-level architecture, end to end |
| 20–35 | **One deep dive** — propose it yourself |
| 35–45 | Bottlenecks, failure, and what you'd do next |

Cut ruthlessly. A 45-minute round rewards a complete-but-shallower design over a beautiful
half-finished one — but not at the cost of the deep dive, which is where E5+ signal lives.

## What Meta loves

- Concrete scale arithmetic done quickly and out loud
- The **fanout / feed / graph** family of problems (unsurprisingly)
- Clear treatment of caching, sharding and hot keys
- Product-aware trade-offs in the product-architecture track: what does the user actually see
  when this degrades?
- Following the interviewer's hint immediately — Meta interviewers steer deliberately

## Common Meta prompts

News feed · Messenger/WhatsApp chat · Instagram Stories · notification system · live comments on
a video · nearby friends · typeahead search · ad delivery and click aggregation · a photo storage
service · Facebook Live · a privacy/consent system · a metrics pipeline.

## Preparation shortcuts

- Drill [../03-backend-cases/news-feed.md](../03-backend-cases/news-feed.md) and
  [../03-backend-cases/chat-messaging.md](../03-backend-cases/chat-messaging.md) until you can do
  each in 40 minutes cleanly. They cover most of Meta's question space between them.
- Practise the **45-minute** clock specifically — most people's practice runs are 60 and it shows.
- For product architecture, rehearse going from a product requirement to entities to API to data
  model in ten minutes.

## Sources

- [Exponent — Meta system design interview (2026)](https://www.tryexponent.com/blog/meta-system-design-interview)
- [IGotAnOffer — Meta system design interview](https://igotanoffer.com/blogs/tech/meta-system-design-interview)
- [DesignGurus — system design interviews at Google, Meta, Amazon](https://www.designgurus.io/blog/system-design-interviews-at-google-meta-amazon)
- [Meta Engineering blog](https://engineering.fb.com/)
