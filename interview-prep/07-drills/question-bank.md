---
title: Question bank
type: drill
track: universal
status: drafted
updated: 2026-09-02
tags: [questions, practice]
---

# Question bank

Problems grouped by the pattern they test — because **the pattern is what transfers**, not the
problem. If you can do one problem in a row well, you can do the rest of that row.

Cases with a link have a worked reference here. The rest are drill-only: design them, then find
a real architecture to compare against (see [../10-resources/engineering-blogs.md](../10-resources/engineering-blogs.md)).

## Backend / distributed systems

| Pattern | Problems |
|---|---|
| **Read-heavy KV + cache** | [URL shortener](../03-backend-cases/url-shortener.md) · Pastebin · Image host · DNS-like lookup service |
| **Counters & limits** | [Rate limiter](../03-backend-cases/rate-limiter.md) · Leaderboard · Analytics counter · Voting/likes at scale |
| **Fanout & timelines** | [News feed](../03-backend-cases/news-feed.md) · Twitter · Instagram · Activity/notification inbox |
| **Realtime connections** | [Chat](../03-backend-cases/chat-messaging.md) · Presence · Collaborative cursors · Live sports scores · Multiplayer game state |
| **Multi-channel delivery** | [Notification system](../03-backend-cases/notification-system.md) · Email marketing platform · Webhook delivery service |
| **Search & retrieval** | [Search + typeahead](../03-backend-cases/search-typeahead.md) · Product search · Log search · Code search |
| **Big bytes** | [File sync / object store](../03-backend-cases/object-storage-sync.md) · [Video streaming](../03-backend-cases/video-streaming.md) · Photo storage · Backup service |
| **Geospatial & matching** | [Ride hailing](../03-backend-cases/ride-hailing.md) · Food delivery · Nearby friends · Yelp/proximity · Ad targeting by location |
| **Money & correctness** | [Payments + ledger](../03-backend-cases/payments-ledger.md) · Ticketmaster/seat booking · Hotel reservations · Inventory reservation · Wallet/points |
| **Time series & telemetry** | [Metrics + alerting](../03-backend-cases/metrics-monitoring.md) · Distributed tracing backend · IoT ingestion |
| **Coordination** | Distributed job scheduler · Cron at scale · Distributed lock service · Config/feature-flag service · Service discovery |
| **Crawl & pipeline** | Web crawler · Sitemap indexer · Price scraper (respecting robots.txt) |

## Frontend

| Pattern | Problems |
|---|---|
| Collaborative state | [Collaborative editor](../04-frontend-cases/collaborative-editor.md) · Design canvas · Kanban board |
| Large lists | [Infinite feed](../04-frontend-cases/infinite-feed.md) · Data grid with 1M rows · Email client |
| Streaming data | [Realtime dashboard](../04-frontend-cases/realtime-dashboard.md) · Trading terminal · Live ops console |
| Reusable UI | [Design system](../04-frontend-cases/component-design-system.md) · Autocomplete component · Rich file uploader |
| App shells | Video player page · Checkout flow · Multi-step form with autosave |

## Data engineering

| Pattern | Problems |
|---|---|
| Ingest at scale | [Clickstream → lakehouse](../05-data-cases/clickstream-lakehouse.md) · IoT telemetry · Log ingestion platform |
| Replication | [CDC pipeline](../05-data-cases/cdc-pipeline.md) · Multi-source customer 360 · Reverse ETL |
| Realtime analytics | [Ad click aggregation](../05-data-cases/realtime-analytics.md) · Live business dashboard · A/B experiment metrics platform |
| Trust | [Data quality + contracts](../05-data-cases/data-quality-and-contracts.md) · Lineage/catalog · GDPR deletion across a lake |
| Batch | Nightly ETL for finance · Data warehouse dimensional model · Backfill framework |

## ML / GenAI

| Pattern | Problems |
|---|---|
| Retrieval + ranking | [Recommender](../06-ml-cases/recommender.md) · [Feed ranking](../06-ml-cases/feed-ranking.md) · Search ranking · Ads CTR prediction · People-you-may-know |
| Realtime scoring | [Fraud detection](../06-ml-cases/fraud-detection.md) · Spam/abuse classifier · Credit decisioning · Dynamic pricing |
| Platform | [Feature store](../06-ml-cases/feature-store.md) · [Monitoring + retraining](../06-ml-cases/ml-monitoring-and-eval.md) · Experimentation platform · Model registry + CI |
| GenAI | [RAG assistant](../06-ml-cases/rag-assistant.md) · [LLM serving platform](../06-ml-cases/llm-serving-platform.md) · Support-ticket agent · Code review assistant · Semantic search over a product catalogue |
| Vision/audio | Image moderation at scale · Video content ID · Speech transcription pipeline |

## By company flavour

Interviewers usually pick something adjacent to their product. Prepare the row that matches.

| Company type | Likely problems |
|---|---|
| Social | Feed, chat, notifications, search, moderation |
| E-commerce | Product search, cart/checkout, inventory reservation, recommendations, payments |
| Fintech | Ledger, fraud, real-time balances, reconciliation, audit |
| Infra / dev tools | Metrics, logging, CI at scale, feature flags, rate limiting |
| Media | Video pipeline, CDN economics, recommendations, live streaming |
| Marketplace | Matching, geo, pricing, ratings, payouts |
| AI company | RAG, LLM serving, evaluation platform, data pipelines for training |

## Curveballs worth rehearsing once each

- "Design X for 100 users, then for 100M." (Tests whether you over-engineer the first version.)
- "Your design just lost a region. Walk me through the next 30 minutes."
- "Halve the cost without hurting p99."
- "The product manager wants this feature next week — what would you cut?"
- "What's the worst thing about your design?" (Answer honestly and specifically. Deflecting here
  costs more than the flaw itself.)

## Referenced by

- [Drills index](README.md)
- [File conventions](../CONVENTIONS.md)
- [Repo index](../../INDEX.md)
- [Resources index](../10-resources/README.md)
