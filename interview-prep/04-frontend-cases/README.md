---
title: Frontend cases index
type: index
track: frontend
status: drafted
updated: 2026-09-02
tags: [index, frontend]
---

# Frontend system design

A different round with a different rubric. Backend design asks "how does this scale to 100M
users"; frontend design asks "how does this stay fast, accessible and maintainable on a
mid-range Android phone on 4G".

## Where to look

| Question | File |
|---|---|
| How do I run the round? RADIO, what's scored | [frontend-playbook.md](frontend-playbook.md) |
| Real-time collaborative editing, CRDT vs OT | [collaborative-editor.md](collaborative-editor.md) |
| Infinite feed, virtualization, image loading, optimistic UI | [infinite-feed.md](infinite-feed.md) |
| Live dashboard: streaming data, charts, backpressure in the browser | [realtime-dashboard.md](realtime-dashboard.md) |
| Reusable component/design system API design | [component-design-system.md](component-design-system.md) |

## What's actually scored

| Axis | What they want to hear |
|---|---|
| **Rendering strategy** | CSR vs SSR vs SSG vs streaming SSR/RSC — chosen from the requirement, not from fashion |
| **Data fetching** | Cache, revalidation, pagination, optimistic updates, race handling |
| **State** | Server state vs client state vs URL state, and why they're different |
| **Performance** | Core Web Vitals with numbers, bundle budget, virtualization, image strategy |
| **Accessibility** | Keyboard, focus management, ARIA, contrast — not an afterthought |
| **Resilience** | Offline, slow network, failed request, empty and error states |
| **Component API** | Props, composition, controlled vs uncontrolled, escape hatches |

## Core Web Vitals — memorise the thresholds

| Metric | Good | Measures | Main lever |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | < 2.5 s | Load speed of the main content | Server response, image priority/preload, no render-blocking resources |
| **INP** (Interaction to Next Paint) — replaced FID in March 2024 | < 200 ms | Responsiveness to *all* interactions | Break up long tasks, yield to the main thread, less JS |
| **CLS** (Cumulative Layout Shift) | < 0.1 | Visual stability | Explicit width/height, reserve space for ads/embeds, no injected content above the fold |

Supporting: TTFB < 800 ms, FCP < 1.8 s, TBT < 200 ms (lab proxy for INP).

**INP is the one that matters in 2026 interviews** because it's newest and it's the metric a
JavaScript-heavy app fails. The fix is architectural — less main-thread work, chunked
rendering, `scheduler.yield()`, web workers for heavy computation — not a config flag.

## Budgets worth quoting

| Budget | Value |
|---|---|
| JS on initial route (compressed) | < 150–200 KB |
| Total initial payload | < 500 KB |
| Time to interactive on mid-range Android / 4G | < 3.5 s |
| Long task threshold | 50 ms — anything longer blocks input |
| Image: use AVIF/WebP, responsive `srcset`, lazy below the fold, `fetchpriority=high` on the LCP image |
