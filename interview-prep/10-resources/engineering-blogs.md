---
title: Engineering blogs and case studies
type: resource
track: universal
status: drafted
updated: 2026-09-20
tags: [blogs, case-studies]
---

# Engineering blogs and case studies

**Read the blog of the company you're interviewing at.** Interviewers ask about problems their
company actually has, and their public writing is the answer key.

## The ones worth a standing subscription

| Blog | Best for |
|---|---|
| [Uber](https://www.uber.com/blog/engineering/) | **The most detailed of the big blogs.** Marketplace/matching, H3 geo-indexing, Pinot, Hudi, Michelangelo (ML platform) |
| [Netflix](https://netflixtechblog.com/) | Streaming, CDN economics (Open Connect), recommendations, chaos engineering, data platform |
| [Discord](https://discord.com/blog) | Message storage at trillions of rows (MongoDB → Cassandra → ScyllaDB), presence, realtime at scale |
| [Cloudflare](https://blog.cloudflare.com/) | Edge, networking, DDoS, rate limiting — unusually deep and readable |
| [Stripe](https://stripe.dev/blog/topic/engineering) | Idempotency, API design, online migrations, correctness |
| [Meta](https://engineering.fb.com/) | Feed, storage, networking at extreme scale |
| [Dropbox](https://dropbox.tech/) | Magic Pocket (exabyte storage), sync, chunking/dedup |
| [Figma](https://www.figma.com/blog/engineering/) | Multiplayer/CRDT, browser performance, sharding Postgres |
| [Slack](https://slack.engineering/) | Realtime messaging, scaling a monolith, search |
| [Airbnb](https://medium.com/airbnb-engineering) | Search/ranking, data platform, service migration |
| [Canva](https://www.canva.dev/blog/engineering/) | Frontend at scale, media pipelines |
| [Datadog](https://www.datadoghq.com/blog/engineering/) | Time-series at enormous cardinality |
| [Shopify](https://shopify.engineering/) | Flash-sale scale, Rails at the limit, sharding |
| [LinkedIn](https://www.linkedin.com/blog/engineering) | Kafka's birthplace; graph and feed systems |
| [Spotify](https://engineering.atspotify.com/) | 1,500+ microservices, data platform, recommendations |

## Curated aggregators

| Source | Use |
|---|---|
| [ByteByteGo real-world case studies](https://bytebytego.com/guides/real-world-case-studies/) | Pre-digested versions of the above |
| [eugeneyan/applied-ml](https://github.com/eugeneyan/applied-ml) | ML case studies by topic (also in `vendor/`) |
| [awesome-scalability](https://github.com/binhnguyennus/awesome-scalability) | Architecture posts organised by scaling problem (also in `vendor/`) |
| [kilimchoi/engineering-blogs](https://github.com/kilimchoi/engineering-blogs) | The full list of company blogs |
| [InfoQ case studies](https://www.infoq.com/) | Conference-grade architecture write-ups |
| [High Scalability](https://highscalability.com/) | **Dormant — last post May 2024.** The "architecture of X" archive is still worth searching; nothing new is coming |

## Where the failures are written down

A post-mortem is the only genre that reports what the authors got wrong. Worth more per minute
than any architecture post, and it is what a staff interviewer is probing for.

| Source | Use |
|---|---|
| [postmortem.io](https://postmortem.io/) | **645 public incident reports and shutdown write-ups**, tagged by failure class, newest August 2026. Search your target company before the loop |
| [AWS post-event summaries](https://aws.amazon.com/premiumsupport/technology/pes/) | AWS's own write-ups, retained five years — including the October 2025 DynamoDB / us-east-1 event. Read one before claiming multi-AZ solves anything |
| [danluu/post-mortems](https://github.com/danluu/post-mortems) | The classic annotated collection, grouped by failure class. Also in `vendor/` |
| [Cloudflare `post-mortem`](https://blog.cloudflare.com/tag/post-mortem/) · [GitHub](https://github.blog/news-insights/company-news/) · [GitLab](https://about.gitlab.com/blog/) | The three companies that publish honest, technical, same-week incident reports |

## Posts worth reading before specific cases

| Case here | Read |
|---|---|
| [chat-messaging](../03-backend-cases/chat-messaging.md) | Discord — "How Discord stores trillions of messages" |
| [object-storage-sync](../03-backend-cases/object-storage-sync.md) | Dropbox — "Inside the Magic Pocket" |
| [video-streaming](../03-backend-cases/video-streaming.md) | Netflix — per-title encode optimisation; Open Connect |
| [ride-hailing](../03-backend-cases/ride-hailing.md) | Uber — H3 hexagonal spatial index; marketplace matching |
| [collaborative-editor](../04-frontend-cases/collaborative-editor.md) | Figma — "How Figma's multiplayer technology works" |
| [payments-ledger](../03-backend-cases/payments-ledger.md) | Stripe — idempotency; online migrations |
| [metrics-monitoring](../03-backend-cases/metrics-monitoring.md) | Facebook Gorilla paper; Prometheus TSDB docs |
| [rate-limiter](../03-backend-cases/rate-limiter.md) | Cloudflare — counting things at scale; Stripe — rate limiters |
| [llm-serving-platform](../06-ml-cases/llm-serving-platform.md) | vLLM blog — "Anatomy of a high-throughput inference system" |
| [feature-store](../06-ml-cases/feature-store.md) | Uber — Michelangelo |

## Papers, specs and individual blogs

Moved to [primary-sources.md](primary-sources.md) — with working links, and with the count of how
many times each is cited by `fundamentals/`, `patterns/` and `comparisons/`. A paper listed by
name and no link is a paper nobody reads.

## How to read a blog post like an interview candidate

1. **Read only the problem statement.** Stop.
2. Design it yourself for 20 minutes.
3. Read the rest and diff — what constraint did you miss? What did they choose that surprised you?
4. Write one line in your drill log.

Ten posts read this way are worth a hundred read passively.

## Referenced by

- [Courses and mock interviews](courses-and-mocks.md)
- [GitHub repositories](github-repos.md)
- [Newsletters and Substacks](newsletters-substack.md)
- [Primary sources](primary-sources.md)
- [Question bank](../07-drills/question-bank.md)
- [Resources index](README.md)
