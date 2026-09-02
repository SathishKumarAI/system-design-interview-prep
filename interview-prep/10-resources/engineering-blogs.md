---
title: Engineering blogs and case studies
type: resource
track: universal
status: drafted
updated: 2026-09-02
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
| [Discord](https://discord.com/blog/tag/engineering) | Message storage at trillions of rows (MongoDB → Cassandra → ScyllaDB), presence, realtime at scale |
| [Cloudflare](https://blog.cloudflare.com/) | Edge, networking, DDoS, rate limiting — unusually deep and readable |
| [Stripe](https://stripe.com/blog/engineering) | Idempotency, API design, online migrations, correctness |
| [Meta](https://engineering.fb.com/) | Feed, storage, networking at extreme scale |
| [Dropbox](https://dropbox.tech/) | Magic Pocket (exabyte storage), sync, chunking/dedup |
| [Figma](https://www.figma.com/blog/section/engineering/) | Multiplayer/CRDT, browser performance, sharding Postgres |
| [Slack](https://slack.engineering/) | Realtime messaging, scaling a monolith, search |
| [Airbnb](https://medium.com/airbnb-engineering) | Search/ranking, data platform, service migration |
| [Canva](https://www.canva.dev/blog/engineering/) | Frontend at scale, media pipelines |
| [Datadog](https://www.datadoghq.com/blog/engineering/) | Time-series at enormous cardinality |
| [Shopify](https://shopify.engineering/) | Flash-sale scale, Rails at the limit, sharding |
| [LinkedIn](https://engineering.linkedin.com/blog) | Kafka's birthplace; graph and feed systems |
| [Spotify](https://engineering.atspotify.com/) | 1,500+ microservices, data platform, recommendations |

## Curated aggregators

| Source | Use |
|---|---|
| [ByteByteGo real-world case studies](https://bytebytego.com/guides/real-world-case-studies/) | Pre-digested versions of the above |
| [eugeneyan/applied-ml](https://github.com/eugeneyan/applied-ml) | ML case studies by topic (also in `vendor/`) |
| [awesome-scalability](https://github.com/binhnguyennus/awesome-scalability) | Architecture posts organised by scaling problem (also in `vendor/`) |
| [kilimchoi/engineering-blogs](https://github.com/kilimchoi/engineering-blogs) | The full list of company blogs |
| [InfoQ case studies](https://www.infoq.com/) | Conference-grade architecture write-ups |
| [High Scalability](http://highscalability.com/) | Older, still a great archive of "the architecture of X" posts |

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

## Papers worth knowing by name (you don't have to read them all)

| Paper | Why it matters |
|---|---|
| **Dynamo** (Amazon, 2007) | Consistent hashing, quorums, eventual consistency — the KV-store blueprint |
| **Bigtable** (Google, 2006) | Wide-column model, LSM storage |
| **MapReduce** (Google, 2004) | Batch processing's origin |
| **Spanner** (Google, 2012) | TrueTime; global external consistency and its latency cost |
| **Raft** (2014) | Understandable consensus; read this one properly |
| **Kafka** (LinkedIn, 2011) | The log as a primitive |
| **Gorilla** (Facebook, 2015) | Time-series compression (delta-of-delta + XOR) |
| **Zanzibar** (Google, 2019) | Relationship-based authorization at scale |
| **PagedAttention / vLLM** (2023) | Why modern LLM serving works |

## How to read a blog post like an interview candidate

1. **Read only the problem statement.** Stop.
2. Design it yourself for 20 minutes.
3. Read the rest and diff — what constraint did you miss? What did they choose that surprised you?
4. Write one line in your drill log.

Ten posts read this way are worth a hundred read passively.
