---
title: Design an infinite feed (frontend)
type: case
track: frontend
difficulty: core
status: drafted
sources: [web.dev, Front End Interview Handbook]
updated: 2026-09-02
tags: [virtualization, pagination, optimistic-ui, images, cwv]
---

# Design an infinite feed (frontend)

> The client half of [../03-backend-cases/news-feed.md](../03-backend-cases/news-feed.md):
> an infinitely scrolling list of posts with images, video, likes and comments.
> **The hard part:** staying under 200 ms INP and near-zero CLS while the DOM grows without
> bound and images keep arriving.

## 1. Clarify

| Question | Assumed answer |
|---|---|
| Devices? | Mobile-first, mid-range Android on 4G is the target device |
| SEO? | No — it's behind auth. So CSR/SSR shell, no SSG |
| Media? | Images + autoplay video |
| Interactions? | Like, comment, share, follow — all optimistic |
| Offline? | Read cached feed offline; queue likes |
| Accessibility? | WCAG 2.2 AA, screen-reader usable, keyboard navigable |

**Non-goals:** the ranking algorithm, the backend fanout, video encoding.

## 2. Requirements

**Functional**
- Endless scroll with smooth pagination and no duplicates
- Optimistic likes/follows with rollback on failure
- Media loads progressively; video autoplays only when visible
- Restore scroll position when navigating back from a detail page

**Non-functional**

| Target | Value |
|---|---|
| LCP | < 2.5 s on 4G / mid-range Android |
| INP | < 200 ms for every interaction |
| CLS | < 0.1 |
| Initial JS | < 170 KB compressed |
| Memory | Bounded — 10,000 scrolled items must not grow the DOM to 10,000 nodes |

## 3. Estimates

```
Post card ≈ 30–60 DOM nodes. 1,000 scrolled posts un-virtualized = 30–60k nodes
   → layout/style recalculation becomes tens of ms per frame → dropped frames, INP failure
Images: 3–5 per post × 200 KB unoptimized = ~1 MB/post
   → AVIF at the actual displayed size ≈ 40–80 KB. **10x saving, the single biggest lever**
Page size: 20 items × ~2 KB JSON = 40 KB per page request
Prefetch trigger: fetch the next page when ~5 items from the end (≈1.5 screens of runway)
```

> [!info] The scary number
> Un-virtualized DOM growth. Everything else can be tuned; an unbounded DOM cannot.

## 4. API / contract

```http
GET /v1/feed?cursor=<opaque>&limit=20
  → { items: [...], next_cursor }        # cursor, never offset — the list mutates under you

POST /v1/posts/{id}/like        Idempotency-Key: <client uuid>
  → 200 { liked: true, count: 412 }
```

**Component API:**
```tsx
<Feed
  queryKey={['feed', userId]}
  renderItem={(post) => <PostCard post={post} />}
  estimateSize={() => 420}      // virtualizer needs an estimate; measured after mount
  onEndReached={fetchNextPage}
  emptyState={<EmptyFeed />}
  errorState={<FeedError onRetry={refetch} />}
/>
```

## 5. Data model (three kinds of state — see [frontend-playbook.md](frontend-playbook.md))

| State | Where | Notes |
|---|---|---|
| Feed pages | Server-state cache (React Query infinite query) | Normalized by post ID so one post updates everywhere it appears |
| Like counts | Same cache, mutated optimistically | Rollback on error |
| Scroll position, open composer | Client state | Scroll position also written to `history.state` for back-restore |
| Filters / active tab | **URL** | Shareable, survives refresh |

Normalize: `posts: {id → post}` plus `feed: [id, id, ...]`. A post appearing in the feed and
in a profile page must not be two copies that can disagree.

## 6. Architecture

```
App shell (SSR or a cached static shell)  → instant paint, skeletons
   └── Feed route (lazy-loaded chunk)
         ├── useInfiniteQuery (cache, dedupe, retry, background refetch)
         ├── Virtualizer (windowed rendering, dynamic measurement)
         ├── PostCard (memoized, stable props)
         │     ├── Media (IntersectionObserver: lazy load, autoplay when visible)
         │     └── Actions (optimistic mutation + rollback)
         └── Service worker: cache shell + last feed page for offline read
```

### Deep dive A — virtualization

Render only visible items + a small overscan buffer; recycle DOM nodes as you scroll.

- Variable heights (posts differ) need **dynamic measurement**: estimate first, measure on
  mount, correct the offsets. Purely fixed-height virtualizers won't work for a feed.
- **Scroll anchoring**: when an image finishes loading and changes height, the browser must
  not shift what the user is reading. Reserve space with explicit aspect ratios so height is
  known *before* the image loads — that's also how you get CLS to zero.
- Keep the scroll container's total height accurate or the scrollbar jitters.
- Restore-on-back: save the cursor + item index + offset, restore by scrolling to the item,
  not to a pixel value (pixel offsets are wrong once measurements differ).

### Deep dive B — images and video (the LCP and bandwidth fight)

- Serve AVIF/WebP at the **displayed** size via `srcset`/`sizes`. Never ship a 2000 px image
  into a 400 px slot.
- `width`/`height` or `aspect-ratio` on every image → zero layout shift.
- `loading="lazy"` below the fold; `fetchpriority="high"` + preload for the first visible
  image (it's your LCP element).
- Blur-up placeholder (a tiny base64 LQIP) so there is never an empty grey box.
- Video: `IntersectionObserver` to play only while visible, `preload="none"`, pause on
  scroll-away, and respect `prefers-reduced-motion` (which should disable autoplay entirely).

### Deep dive C — optimistic updates done correctly

```
onMutate:   cancel in-flight refetches for this key, snapshot the cache,
            apply the optimistic change
onError:    restore the snapshot, show a non-blocking toast with retry
onSettled:  invalidate so the truth eventually wins
```
The step everyone forgets is **cancelling in-flight refetches** — otherwise a response that
was already in the air overwrites your optimistic update and the heart un-fills a second
after the user tapped it. Also: send an idempotency key so a retry doesn't double-like.

### Deep dive D — INP

- Keep event handlers trivial; defer the real work with `scheduler.yield()` or by scheduling
  after paint.
- Memoize `PostCard` and keep props referentially stable — inline objects/arrays/closures in
  props are the most common cause of whole-list re-renders.
- Never do JSON parsing or heavy transforms in the scroll handler; do them in a worker or at
  fetch time.
- Chunk long lists' work; hydration should be incremental, not one 900 ms task.

## 7. Scale & failure

| Breaks first at 10x | Fix |
|---|---|
| DOM nodes / memory | Virtualization (already), smaller cards, unmount off-screen media |
| Image bandwidth | Better formats, tighter `sizes`, lower quality on `save-data`/slow connections |
| Cache memory in the client | Cap cached pages, drop far-behind pages, keep only IDs |
| Re-render cost as the feed grows | Normalization + memoization + stable keys |

| Failure | User sees | Handling |
|---|---|---|
| Page fetch fails mid-scroll | Spinner forever (bad) | Inline error row with retry; keep the loaded items |
| Offline | Broken app (bad) | Serve last cached page from the service worker + an offline banner; queue likes |
| Slow API | Blank screen | Skeletons matching final layout (also prevents CLS), then a timeout error state |
| Image 404 | Broken icon | Fallback placeholder with the same dimensions |
| Duplicate items across pages | Repeated posts | Cursor pagination + dedupe by ID at merge time |

## 8. Ops & cost

- **SLO / budgets in CI:** Lighthouse CI gate on LCP < 2.5 s, INP < 200 ms, CLS < 0.1,
  bundle < 170 KB. **Failing the build is what keeps it fast** — a budget that only warns is
  a budget that is already exceeded.
- **Monitor:** field data (RUM) for CWV segmented by device class and country, JS error rate,
  API error rate by endpoint, image bytes per session.
- **Rollout:** feature flags per cohort, watch CWV field metrics per release; regression in
  INP is a rollback trigger, same as an error-rate spike.
- **Cost:** image/CDN bandwidth dominates the frontend's contribution — see
  [../02-primitives/cost-engineering.md](../02-primitives/cost-engineering.md).
- **First thing I'd cut:** autoplay video on cellular connections (`navigator.connection`),
  and image quality on `save-data`.

**Accessibility, said explicitly:** the feed is a `<ul>` of `<li>`s (a virtualized list must
still be semantically a list, with `aria-setsize`/`aria-posinset` where the DOM is
incomplete); infinite scroll needs a keyboard-reachable "Load more" alternative; new items
announced via `aria-live="polite"`; focus must never be stolen by loading content.

## Referenced by

- [Frontend cases index](README.md)
- [Question bank](../07-drills/question-bank.md)
- [Repo index](../../INDEX.md)

## Sources & further reading

- [web.dev — optimize INP](https://web.dev/articles/optimize-inp), [optimize LCP](https://web.dev/articles/optimize-lcp), [optimize CLS](https://web.dev/articles/optimize-cls)
- [TanStack Virtual](https://tanstack.com/virtual) · [TanStack Query — optimistic updates](https://tanstack.com/query/latest/docs/framework/react/guides/optimistic-updates)
- Vendor: `10-resources/vendor/front-end-interview-handbook/`
- Backend counterpart: [../03-backend-cases/news-feed.md](../03-backend-cases/news-feed.md)
