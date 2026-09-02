---
title: Backend cases index
type: index
track: backend
status: drafted
updated: 2026-09-02
tags: [index, cases]
---

# Backend cases

Ten designs that between them cover every pattern the classic distributed-systems round
tests. Do them in order — each introduces something the next one assumes.

## Where to look

| Case | Teaches | Difficulty |
|---|---|---|
| [url-shortener.md](url-shortener.md) | ID generation, KV at scale, cache, read-heavy | intro |
| [rate-limiter.md](rate-limiter.md) | Algorithms, distributed counters, hot keys, edge enforcement | intro |
| [news-feed.md](news-feed.md) | Fanout write vs read, celebrity problem, ranking, precompute | core |
| [chat-messaging.md](chat-messaging.md) | WebSockets, connection state, ordering, delivery + read receipts, offline sync | core |
| [notification-system.md](notification-system.md) | Multi-channel fanout, dedup, retries, provider failure, preferences | core |
| [search-typeahead.md](search-typeahead.md) | Inverted index, tries, index build path, ranking, tiering | core |
| [object-storage-sync.md](object-storage-sync.md) | Chunking, dedup, delta sync, conflict resolution, metadata vs blob | core |
| [video-streaming.md](video-streaming.md) | Upload/transcode pipeline, ABR, CDN economics, live vs VOD | core |
| [ride-hailing.md](ride-hailing.md) | Geospatial indexing, matching, high-frequency location writes, state machines | advanced |
| [payments-ledger.md](payments-ledger.md) | Idempotency, double-entry ledger, sagas, exactly-once effects, reconciliation | advanced |
| [metrics-monitoring.md](metrics-monitoring.md) | Time-series ingest, cardinality, downsampling, alert evaluation | advanced |

## How to drill a case

1. Read only **§1 Clarify** and **§2 Requirements**.
2. Timer 40 minutes. Whiteboard/paper. Talk out loud — record yourself if solo.
3. Then read the file and fill in
   [../_templates/drill-log-template.md](../_templates/drill-log-template.md).
4. The diff is your study list. Re-drill the case a week later; you should beat it.

## The patterns underneath

Most cases are a recombination of six moves. Learn the moves and new problems stop being new:

| Move | Appears in |
|---|---|
| Precompute on write vs compute on read | feed, typeahead, leaderboards, analytics |
| Partition by the entity that queries colocate on | chat, feed, metrics, payments |
| Absorb writes into a log, derive everything else | notifications, search, analytics, feed |
| Put the big bytes in an object store, the small facts in a database | video, file sync, chat attachments |
| Make the mutating operation idempotent and retryable | payments, notifications, uploads |
| Degrade instead of failing | every single one |

## Referenced by

- [Books already on this machine](../10-resources/books-on-this-machine.md)
- [Fundamentals index](../fundamentals/README.md)
- [Interview prep index](../README.md)
- [Primitives index](../02-primitives/README.md)
- [Repo index](../../INDEX.md)
