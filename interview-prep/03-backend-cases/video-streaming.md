---
title: Design video streaming (YouTube / Netflix)
type: case
track: backend
difficulty: core
status: drafted
sources: [Alex Xu v1 ch.14, Netflix Open Connect]
updated: 2026-09-02
tags: [transcoding, abr, cdn, egress, pipeline]
---

# Design video streaming

> Upload, process and stream video to millions of concurrent viewers.
> **The hard part:** it's two systems glued together — a batch **transcoding pipeline** and
> a **CDN economics** problem. The application servers are the least interesting part.

## 1. Clarify

| Question | Assumed answer |
|---|---|
| VOD, live, or both? | VOD primary; live as an extension (say how it differs) |
| Upload volume? | 500 hours/minute (YouTube-scale) |
| Viewers? | 100M DAU, 30 min average, peak 10M concurrent streams |
| Devices? | Mobile, web, TV — so multiple codecs and resolutions |
| DRM? | Yes for licensed content |
| Global? | Yes — and this decides everything |

**Non-goals:** recommendations ([../06-ml-cases/recommender.md](../06-ml-cases/recommender.md)),
comments, monetisation, content moderation.

## 2. Requirements

**Functional**
- Resumable upload of large files
- Transcode to an adaptive bitrate ladder + thumbnails + captions
- Stream with adaptive bitrate; seek; resume where you left off
- Publish/unpublish, visibility rules

**Non-functional**

| Target | Value |
|---|---|
| Start-up time (join latency) | < 1 s to first frame |
| Rebuffer ratio | < 0.5% of playback time |
| Upload → playable | < 10 min for a 10-min video |
| Availability | 99.99% playback |

## 3. Estimates

```
Ingest: 500 h/min = 30,000 h/day
   at ~1 GB/h source → 30 TB/day raw upload ≈ 350 MB/s sustained
Transcoding: ~1–2× realtime per rendition on CPU; 6 renditions per video
   30,000 h/day × 6 = 180,000 CPU-hours/day ÷ 24 = ~7,500 cores continuously  ← big
   (hardware encoders / GPU cut this several-fold)
Storage: 30 TB/day source + ~3× for all renditions ≈ 120 TB/day → 44 PB/year

Delivery: 10M concurrent × 3 Mbps avg = 30 Tbps peak                ← THE number
   30 Tbps sustained ≈ 300+ PB/month.
   At retail CDN pricing that is hundreds of millions per month, which is exactly why
   Netflix built Open Connect and put appliances inside ISPs.
```

> [!info] The scary number
> **30 Tbps of egress.** Every serious design decision here is downstream of bandwidth cost.

## 4. API / contract

```http
POST /v1/videos                 { title, visibility }  → { video_id, upload_url }
PUT  <upload_url>               (resumable, chunked, direct to object storage)
POST /v1/videos/{id}/complete   → 202  (kicks off the pipeline)
GET  /v1/videos/{id}            → { status: "processing"|"ready", renditions[], manifest_url }

GET  <manifest_url>             → HLS .m3u8 / DASH .mpd  (player picks a rendition)
GET  <segment_url>              → 2–6 s media segment    (served by CDN; this is 99.9% of traffic)
POST /v1/videos/{id}/progress   { position_s }           (batched, best-effort)
```

## 5. Data model

| Entity | Key | Partition by | Serves |
|---|---|---|---|
| `videos` | `video_id` | `hash(video_id)` | Metadata, status |
| `renditions` | `(video_id, profile)` | `video_id` | Manifest generation |
| `segments` | Object keys in blob storage | — | Content-addressed, CDN-cacheable |
| `watch_progress` | `(user_id, video_id)` | `user_id` | Resume playback |
| `view_events` | Kafka → OLAP | `hash(video_id)` | Counts, analytics, ranking signals |

Source, renditions and segments all live in object storage. The database holds only small
facts — the classic "big bytes in the object store, small facts in the database" split.

## 6. Architecture

```
UPLOAD & PROCESS
client → presigned resumable upload → object store (raw)
                                        ↓ event
                          pipeline orchestrator (DAG, per-video workflow)
        ┌────────────┬──────────────┬──────────────┬──────────────┐
     validate    split into      transcode        thumbnails     captions (ASR)
     + probe     GOP chunks    (fan-out per       + preview       + language ID
                               rendition ×        sprite
                               chunk, parallel)
                                    ↓
                          concatenate + package (HLS/DASH) + encrypt (DRM)
                                    ↓
                          publish manifests → warm CDN → mark ready

PLAYBACK
player → manifest (small, from API/CDN) → segments (CDN edge; origin shield behind it)
       → ABR: measure throughput/buffer, switch rendition per segment
```

### Deep dive A — the transcoding pipeline

- **Split by GOP (group of pictures)** so chunks are independently decodable, then transcode
  chunks in parallel and concatenate. A 1-hour video becomes hundreds of tasks that finish in
  minutes instead of hours. This is the core trick.
- **DAG orchestration** with per-task retries, idempotent tasks (output keyed by
  `(video_id, rendition, chunk, pipeline_version)`), and a dead-letter path. Re-running a
  failed chunk must be free and safe.
- **Priority queues**: a 30-second short from a large creator ahead of a 4-hour archive
  upload. Otherwise one big job blocks the queue.
- **Spot instances** for transcoding — it's interruptible batch work, so 60–90% cheaper.
  Checkpoint at chunk granularity so an interruption loses seconds.
- **Codec ladder**: H.264 for compatibility, plus HEVC/AV1 for bandwidth savings on devices
  that support them. AV1 is ~30% smaller than H.264 at the same quality — at 30 Tbps that's
  an enormous saving, paid for in encoding CPU. **That trade is the interesting cost decision
  in this case**, and it's worth stating explicitly: spend compute once, save bandwidth
  forever.
- **Per-title / per-scene encoding**: an animated cartoon needs far fewer bits than a sports
  broadcast. Optimising the ladder per title saves double-digit percentages of total egress.

### Deep dive B — adaptive bitrate delivery

- Video is cut into 2–6 s segments at each quality level; the manifest lists them.
- The **player** decides: measure recent throughput and buffer occupancy, pick the next
  segment's rendition. Server does nothing clever — the intelligence is at the edge, which is
  why this scales.
- Start-up: request the lowest rendition first for instant playback, then ramp up. That's how
  you hit < 1 s join time.
- Trade-off: shorter segments = faster adaptation and lower live latency, but more requests
  and worse compression efficiency.

### Deep dive C — CDN economics

- **95%+ of bytes must come from cache.** Popularity is extremely long-tailed (Zipf), so a
  small hot set serves most traffic — cache hit rates are naturally high if you don't fragment
  the cache key.
- **Origin shield**: a mid-tier between edge PoPs and origin, so a cold popular video doesn't
  pull from origin once per PoP.
- **Pre-positioning**: for predictable demand (a big premiere), push content to edges *before*
  release. Netflix's model taken to its conclusion is putting appliances inside ISP networks,
  where the marginal delivery cost approaches zero.
- **Multi-CDN** with a steering layer: cost arbitrage plus resilience against one CDN having
  a bad day.

**Live streaming differs on:** ingest via RTMP/SRT, transcode in real time (no batch
parallelism available — latency is the constraint), LL-HLS/WebRTC for low latency, and DVR
windows. Say those four differences and you've covered it.

## 7. Scale & failure

| Breaks first at 10x | Fix |
|---|---|
| Transcoding fleet cost | Hardware/GPU encoders, per-title ladders, transcode-on-demand for the cold tail |
| Egress | More AV1, better ABR ladder, ISP-embedded caches, multi-CDN arbitrage |
| Origin load on a viral video | Origin shield, pre-warm, request coalescing at the edge |
| Storage of unwatched renditions | Generate the long tail lazily on first request |

| Component fails | Blast radius | Degraded behaviour |
|---|---|---|
| One CDN degraded | Rebuffering in a region | Steer to a second CDN (multi-CDN is the mitigation, not a luxury) |
| Transcoding backlog | Uploads take longer to publish | Priority queues; publish the 720p rendition first and add the rest later |
| Metadata service down | Can't browse | Playback of an already-loaded manifest continues — decoupling wins |
| DRM licence server down | Protected content unplayable | Cache licences client-side with a validity window |

## 8. Ops & cost

- **SLO:** join time p95 < 1 s; rebuffer ratio < 0.5%; upload→ready p95 < 10 min.
  Note these are **player-side** metrics — server-side metrics cannot see them.
- **Alert on:** rebuffer ratio by CDN/region/ISP, join time, transcode queue depth and
  failure rate, cache hit ratio, playback error codes by device class.
- **Rollout:** ladder/codec changes are A/B tested on QoE metrics (rebuffer + join time +
  bitrate delivered), never shipped on theory.
- **Cost:** egress ≫ transcoding ≫ storage. A 1% improvement in compression efficiency is
  worth more than the entire application tier.
- **First thing I'd cut:** the highest rendition for content nobody watches at 4K, and
  renditions for the cold tail generated on demand instead of eagerly.

## Sources & further reading

- Local book: Alex Xu vol. 1 ch.14 (YouTube)
- Repo notes: [../../basic/advanced/designs%20%28needs%20update%20as%20we%20go%29/Video%20Stream/](../../basic/advanced/designs%20%28needs%20update%20as%20we%20go%29/Video%20Stream/)
- [Netflix Open Connect](https://openconnect.netflix.com/en/)
- [Netflix — per-title encode optimization](https://netflixtechblog.com/per-title-encode-optimization-7e99442b62a2)
- Primitives: [networking-and-edge](../02-primitives/networking-and-edge.md), [cost-engineering](../02-primitives/cost-engineering.md)
