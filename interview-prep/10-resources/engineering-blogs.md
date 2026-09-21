---
title: Engineering blogs and case studies
type: resource
track: universal
status: drafted
sources: [every URL on this page fetched 2026-09-21, own analysis]
updated: 2026-09-21
tags: [blogs, case-studies]
---

# Engineering blogs and case studies

**Read the blog of the company you're interviewing at.** Interviewers ask about problems their
company actually has, and their public writing is the answer key.

**Every URL below was fetched on 2026-09-21.** `Latest` is a date that was visible on the page or
its feed that day — not a recollection. `Cadence` is inferred from the dates on the listing, and
it is the column that decides whether something is worth a subscription: a blog that posts twice a
year costs you the same attention as one that posts weekly and repays a fraction of it.

| Question | Section |
|---|---|
| I deploy models and I want numbers | [§1 LLM and ML infrastructure](#1-llm-and-ml-infrastructure) |
| I'm designing a distributed system | [§2 Distributed systems, storage, streaming](#2-distributed-systems-storage-and-streaming) |
| Is this one still alive? | [§3 Thin or stalled](#3-thin-or-stalled--search-the-archive-dont-subscribe) |
| Where do people admit what broke? | [§5 Where the failures are written down](#5-where-the-failures-are-written-down) |

---

## 1. LLM and ML infrastructure

The half of the corpus with the fewest textbooks and the most movement. Four of these publish
throughput and latency deltas with the change that caused them, which is exactly what
[../06-ml-cases/llm-serving-platform.md](../06-ml-cases/llm-serving-platform.md) is made of.

| Blog | Latest | Cadence | Actually good at |
|---|---|---|---|
| [vLLM](https://vllm.ai/blog) | 2026-09-21 | **~2–3/week** | **The single best subscription for LLM serving.** KV-cache and prefill/decode disaggregation, INT4 MoE, per-GPU tok/s before and after. `blog.vllm.ai` 301s here — update any old bookmark |
| [Modal](https://modal.com/blog) | 2026-09-14 | ~2–4/month | Serverless GPU internals nobody else publishes: container cold-boot, scheduler design, a million concurrent sandboxes. No RSS feed, and the index is JS-rendered — dates are only visible in a browser or on the post itself |
| [Baseten](https://www.baseten.co/blog/) | 2026-09-02 | ~weekly | Inference optimisation with the speedup attached (9.6× on diarization; prefill efficiency; RL weight sync). The index renders no dates — freshness is only visible inside a post |
| [Together AI](https://www.together.ai/blog) | 2026-09-18 | ~3–5/month | Kernel and cluster work (ThunderKittens, preemptible compute). Interleaved with sales-led case studies; filter |
| [Pinterest](https://medium.com/pinterest-engineering) ([feed](https://medium.com/feed/pinterest-engineering)) | 2026-09-17 | ~2–4/month | **The closest public writing to an ML-system-design interview**: retrieval towers, embedding platforms, VLM serving. Medium 403s automated fetchers — use the feed URL from a script |
| [Instacart](https://tech.instacart.com/) ([feed](https://tech.instacart.com/feed)) | 2026-09-03 | ~1–2/month, uneven (7-week gap Jul–Sep) | Applied ML with real experimental rigour: variance reduction below the randomization grain, ads-retrieval rebuilds, on-call tooling. Medium-hosted, so the HTML 403s fetchers — use the feed |
| [Databricks — Engineering](https://www.databricks.com/blog/category/engineering) | 2026-09-14 | ~1–2/month | Data-plane scale (10T samples/day monitoring; object storage plus a WAL Postgres). Use the *category* URL — the main blog is marketing |
| [Anthropic — Engineering](https://www.anthropic.com/engineering) | 2026-04-23 | **Bursty, ~1–2/month when active; nothing seen since April** | Agent and harness design, context engineering, eval methodology. Read it for how agents are built, not for serving numbers — it publishes almost none |
| [Google Research](https://research.google/blog/) | 2026-09-18 | ~2–3/week | Mostly science; the occasional inference-bottleneck post. Skim, don't subscribe |
| [Hugging Face](https://huggingface.co/blog) | ~2026-09-20 (relative dates only) | Several per day, community-posted | A reference to search, not a feed to follow. Real KV-cache work sits beside model self-promotion |

## 2. Distributed systems, storage and streaming

| Blog | Latest | Cadence | Actually good at |
|---|---|---|---|
| [Cloudflare](https://blog.cloudflare.com/) | 2026-09-21 | **~3–4/week** | Edge, networking, DDoS and protocol work with real numbers — post-quantum DNSSEC, Pingora, Rust memory wins. Unusually deep *and* readable, which is rare |
| [PlanetScale](https://planetscale.com/blog) | 2026-09-18 | **~2–3/week** | **Top three on this page for interview substance.** Postgres and sharding internals with hard numbers: MVCC and VACUUM pathology, connection-pool failure modes, "768 servers look like one" |
| [ScyllaDB](https://www.scylladb.com/blog/) | 2026-09-14 | ~1–2/week (10 posts Jul 22 – Sep 14) | The deepest pure distributed-database content here: QUIC inside Seastar, an asymmetric io_uring backend, a Rust DynamoDB-API driver at +58% throughput, migration write-ups. Also serialising **DDIA 2nd-edition excerpts** |
| [Uber](https://www.uber.com/blog/engineering/) | 2026-09-17 | ~1/week | **Still the most detailed of the big-company blogs.** Retry storms, M3DB sharding, OpenSearch zone failure, H3 geo-indexing, Michelangelo |
| [Netflix](https://netflixtechblog.com/) ([feed](https://medium.com/feed/netflix-techblog)) | 2026-09-18 | ~2–3/month | Streaming-scale data and ML platform internals — Flink autoscaling, real-time distributed graph, LLM-native recsys. Medium 403s fetchers; the feed works |
| [Meta](https://engineering.fb.com/) | 2026-09-03 | ~4/month | Hyperscale infra and AI hardware: ZippyDB proxying, RDMA transport, MTIA silicon, ads-ranking architecture |
| [Shopify](https://shopify.engineering/) | 2026-09-10 | ~weekly | Commerce-scale Rails and Vitess sharding, and currently the best public writing on production LLM agent harnesses. Listing interleaves evergreen posts |
| [Datadog](https://www.datadoghq.com/blog/engineering/) ([feed](https://www.datadoghq.com/blog/engineering/index.xml)) | 2026-09-01 | ~1.5–2/month | Low-level systems performance: Go/Rust/JVM profiling, eBPF, Postgres pathology, trillion-event query engines. Cards on the index carry **no dates** — use the feed |
| [Notion](https://www.notion.com/blog/topic/tech) | 2026-09-18 | ~1–2/month | Concrete scaling war stories: CRDTs, multi-region, vector search at 10× scale for a tenth the cost, Spark on Kubernetes. Index hides dates |
| [Stripe](https://stripe.dev/blog/topic/engineering) | 2026-09-14 | ~1–2/month | Money correctness and monorepo engineering: ledgers, zero-downtime migrations, CI over 50M lines of Ruby |
| [Grab](https://engineering.grab.com/) | 2026-08-28 | ~3–4/month | Data mesh, Iceberg migration, agent platforms — full-stack data infra with the trade-offs left in |
| [Lyft](https://eng.lyft.com/) ([feed](https://eng.lyft.com/feed)) | 2026-09-10 | ~1–2/month, uneven | Marketplace and streaming: Flink operator migration, semantic metric layer |
| [Airbnb](https://medium.com/airbnb-engineering) ([feed](https://medium.com/feed/airbnb-engineering)) | 2026-09-17 | ~2–3/month | Applied ML in production: sequence recommenders and Chronon, search personalisation, GenAI eval at scale |
| [Spotify](https://engineering.atspotify.com/) | 2026-09-16 | ~2/month | Experimentation and causal inference (A/B testing, LLM evals) plus Backstage developer-experience work |
| [Dropbox](https://dropbox.tech/) | 2026-08-31 | ~1–2/month | Content processing and storage platform; Magic Pocket is the archive post everyone cites |
| [Figma](https://www.figma.com/blog/engineering/) | 2026-09-02 | ~1–2/month | Client-side rendering and performance (WebGPU, Rust memory, incremental loading) plus the Postgres sharding work. Listing is not chronological |
| [Fly.io](https://fly.io/blog/) | 2026-09-03 | ~1/month, with a 4-month gap this year | Opinionated deep infra writing; currently all-in on agent sandboxes. Thin cadence, high quality |
| [LinkedIn](https://www.linkedin.com/blog/engineering) | 2026-09-02 | ~2–4/month (weak signal — featured items are undated) | Kafka's birthplace; recommender, search and LLM ranking at member scale |

## 3. Thin or stalled — search the archive, don't subscribe

These are not dead links. They are live pages that are not worth a feed slot, and knowing which is
which is the whole point of this file.

| Blog | Latest confirmed | Verdict |
|---|---|---|
| [Slack](https://slack.engineering/) | 2026-07-14 | Quiet for two months. Good platform-migration war stories in the back catalogue (EC2 rebuild, notifications rewrite) |
| [Canva](https://www.canva.dev/blog/engineering/) | 2026-09-17 | **Two posts in all of 2026.** The queue-backpressure and session-revocation pieces are genuinely good; that is two afternoons, not a subscription |
| [Discord](https://discord.com/blog) | patch notes dated 2026-09-08 in their titles | The landing page is product and patch notes with **no post dates at all**. The trillions-of-messages storage posts are archive material — search for them, don't watch the feed |
| [High Scalability](https://highscalability.com/) | 2024-05-09 | **Dormant.** Four posts in 2024, nothing since. The "architecture of X" archive is still worth searching; nothing new is coming |

## 4. Curated aggregators

| Source | Latest | Use |
|---|---|---|
| [eugeneyan/applied-ml](https://github.com/eugeneyan/applied-ml) | — | ML case studies by topic (also in `vendor/`) |
| [awesome-scalability](https://github.com/binhnguyennus/awesome-scalability) | — | Architecture posts organised by scaling problem (also in `vendor/`) |
| [kilimchoi/engineering-blogs](https://github.com/kilimchoi/engineering-blogs) | — | The full list of company blogs, when the one you need is not above |
| [ByteByteGo case studies](https://bytebytego.com/guides/real-world-case-studies/) | "Updated 3/14/2024" | Diagram-first summaries of other people's architectures. **Two years stale, and a secondary source** — fine for a first pass, never as the citation |
| [InfoQ](https://www.infoq.com/) | — | Conference-grade architecture write-ups |

## 5. Where the failures are written down

A post-mortem is the only genre that reports what the authors got wrong. Worth more per minute
than any architecture post, and it is what a staff interviewer is probing for.

| Source | Latest | Use |
|---|---|---|
| [AWS post-event summaries](https://aws.amazon.com/premiumsupport/technology/pes/) | 2025-10-19 (DynamoDB / us-east-1) | **~1 per year, event-driven.** AWS's own root-cause detail — the canonical primary source. Read one before claiming multi-AZ solves anything |
| [Cloudflare `post-mortem`](https://blog.cloudflare.com/tag/post-mortem/) | 2026-05-01 | ~4 in 2026, ~6 in 2025. The best vendor postmortems in the industry: same-week, timeline-level, names the bad config or code path |
| [postmortem.io](https://postmortem.io/) | 2026-08-04 | An **index** of other people's public incident reports, each linked to source — a single search surface, not original analysis. ~2–3/week while active; quiet for seven weeks |
| [danluu/post-mortems](https://github.com/danluu/post-mortems) | — | The classic annotated collection, grouped by failure class. Also in `vendor/` |
| [Anthropic — "A postmortem of three recent issues"](https://www.anthropic.com/engineering) | 2025-09-17 | Rare: an **inference-stack** postmortem. Three overlapping infrastructure bugs degrading model output, and why they were hard to detect. The closest thing to an incident report for an LLM serving platform |
| [GitHub](https://github.blog/news-insights/company-news/) · [GitLab](https://about.gitlab.com/blog/) | — | The other two companies that publish honest, technical, same-week incident reports |

## 6. Posts worth reading before specific cases

Every link in this table was opened on 2026-09-21. The dates are the posts' own — most of these
are old, and that is the point: a 2017 post that named the mechanism is still the reference.

| Case here | Read | Published |
|---|---|---|
| [chat-messaging](../03-backend-cases/chat-messaging.md) | [How Discord Stores Trillions of Messages](https://discord.com/blog/how-discord-stores-trillions-of-messages) — Cassandra → ScyllaDB, and why | 2023-03-06 |
| [object-storage-sync](../03-backend-cases/object-storage-sync.md) | [Scaling to exabytes and beyond](https://dropbox.tech/infrastructure/magic-pocket-infrastructure) — the canonical Magic Pocket post. **There is no Dropbox post titled "Magic Pocket"**; that is the QCon SF 2022 talk | 2016-03-14 |
| [video-streaming](../03-backend-cases/video-streaming.md) | [Per-Title Encode Optimization](https://netflixtechblog.com/per-title-encode-optimization-7e99442b62a2) · [Serving 100 Gbps from an Open Connect Appliance](https://netflixtechblog.com/serving-100-gbps-from-an-open-connect-appliance-cdb51dda3b99) · [openconnect.netflix.com](https://openconnect.netflix.com/en/) for current OCA specs | 2015-12-14 · 2017-09-29 |
| [ride-hailing](../03-backend-cases/ride-hailing.md) | [H3: Uber's Hexagonal Hierarchical Spatial Index](https://www.uber.com/blog/h3/) | 2018-06-27 |
| [collaborative-editor](../04-frontend-cases/collaborative-editor.md) | [How Figma's multiplayer technology works](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/) — Evan Wallace on why they did **not** use OT or a general CRDT | 2019-10-16 |
| [payments-ledger](../03-backend-cases/payments-ledger.md) | [Designing robust and predictable APIs with idempotency](https://stripe.com/blog/idempotency) · [Online migrations at scale](https://stripe.com/blog/online-migrations) — the four-phase dual-write | 2017-02-22 · 2017-02-02 |
| [rate-limiter](../03-backend-cases/rate-limiter.md) | [How we built rate limiting capable of scaling to millions of domains](https://blog.cloudflare.com/counting-things-a-lot-of-different-things/) | 2017-06-07 |
| [metrics-monitoring](../03-backend-cases/metrics-monitoring.md) | [Prometheus storage docs](https://prometheus.io/docs/prometheus/latest/storage/) (operator view; the on-disk format spec is linked from it) + the Gorilla paper in [primary-sources.md](primary-sources.md) | undated docs |
| [llm-serving-platform](../06-ml-cases/llm-serving-platform.md) | [Inside vLLM: Anatomy of a High-Throughput LLM Inference System](https://vllm.ai/blog/2025-09-05-anatomy-of-vllm) — then the newest disaggregation post on the [index](https://vllm.ai/blog), then the PagedAttention paper | 2025-09-05 |
| [feature-store](../06-ml-cases/feature-store.md) | [Meet Michelangelo: Uber's Machine Learning Platform](https://www.uber.com/blog/michelangelo-machine-learning-platform/) | 2017-09-05 |
| [recommender](../06-ml-cases/recommender.md), [feed-ranking](../06-ml-cases/feed-ranking.md) | [Pinterest](https://medium.com/pinterest-engineering) on retrieval towers and embedding platforms; [Airbnb](https://medium.com/airbnb-engineering) on sequence recommenders and Chronon | current, see §1 |

> [!warning] Trap
> `netflixtechblog.com` returns **403 to every scripted fetcher** — curl and Googlebot UA
> included — while serving 200 to a real browser. That is a bot challenge, not a dead link. The
> same is true of `medium.com/airbnb-engineering`, `medium.com/pinterest-engineering`,
> `eng.lyft.com` and `tech.instacart.com`. If a future link audit flags any of them as broken,
> check the feed URL before deleting the row.

## 7. Checked on 2026-09-21 and deliberately cut

Recording the negative result, so nobody re-adds them next quarter:

| Candidate | Why it is not on this page |
|---|---|
| [Character.AI](https://blog.character.ai/) | Posts weekly, but it is fandom, product and safety content now. The famous serving-efficiency engineering posts are historical |
| [Meta AI](https://ai.meta.com/blog/) | Launch announcements with a research veneer. `engineering.fb.com` above is the one with the numbers |
| [Microsoft Research](https://www.microsoft.com/en-us/research/blog/) | Real research, but essentially nothing on serving, latency or cost |
| Segment engineering | `segment.com/blog/engineering` 302s to `twilio.com/en-us/blog/developers/`. The engineering blog no longer exists as such, and the destination publishes no dates |
| [Vercel](https://vercel.com/blog) · [Sentry](https://blog.sentry.io/) | Both post often and both have real engineering in them (Vercel's CDN-metadata latency work; Sentry's tracing posts), but the majority is product release notes. Search them, don't subscribe |
| OpenAI | `openai.com/news/engineering/` is the right index and it returns **403 to every automated fetcher**, so no date could be seen. Its infra posts (Postgres at millions of QPS; Rust storage rewrites) are reportedly the most valuable on this list — **open it in a browser and add it yourself once you can see a date.** Unverified claims do not go in an index whose job is to be trustworthy |

## How to read a blog post like an interview candidate

1. **Read only the problem statement.** Stop.
2. Design it yourself for 20 minutes.
3. Read the rest and diff — what constraint did you miss? What did they choose that surprised you?
4. Write one line in your drill log.

Ten posts read this way are worth a hundred read passively.

## Papers, specs and individual blogs

Moved to [primary-sources.md](primary-sources.md) — with working links, and with the count of how
many times each is cited by `fundamentals/`, `patterns/` and `comparisons/`. A paper listed by
name and no link is a paper nobody reads.

## Referenced by

- [Courses and mock interviews](courses-and-mocks.md)
- [GitHub repositories](github-repos.md)
- [Newsletters and Substacks](newsletters-substack.md)
- [Primary sources](primary-sources.md)
- [Question bank](../07-drills/question-bank.md)
- [Resources index](README.md)
