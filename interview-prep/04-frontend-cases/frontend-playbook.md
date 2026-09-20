---
title: Frontend system design playbook (RADIO)
type: playbook
track: frontend
difficulty: core
status: drafted
sources: [Front End Interview Handbook, web.dev]
updated: 2026-09-02
tags: [radio, rendering, state, performance, a11y]
---

# Frontend system design playbook — RADIO

The frontend round has its own framework. Use **RADIO**; it maps to the same eight-section
case template used elsewhere in this repo.

| RADIO | Minutes | What you produce |
|---|---|---|
| **R**equirements | 5 | Functional + non-functional, devices, network, scale, non-goals |
| **A**rchitecture | 10 | Component tree, data flow, module boundaries, rendering strategy |
| **D**ata model | 5 | Server state vs client state vs URL state, normalized shape |
| **I**nterface | 10 | Component props/API **and** the network API it consumes |
| **O**ptimizations | 15 | Performance, accessibility, resilience, i18n, security |

## R — Requirements

Ask these; they change the design:

| Question | Changes |
|---|---|
| Devices and network? (low-end Android on 3G?) | Bundle budget, whether you can afford client-side rendering at all |
| SEO required? | SSR/SSG vs CSR — decides the whole architecture |
| Real-time, or is polling fine? | WebSocket/SSE tier vs plain fetch |
| Offline support? | Service worker, local persistence, conflict resolution |
| How much data on screen at once? | Virtualization, pagination strategy |
| Internationalisation, RTL? | Layout, formatting, bundle splitting per locale |
| Accessibility target (WCAG 2.2 AA)? | Focus management, semantics, contrast |

## A — Architecture and rendering strategy

| Strategy | Use when | Cost |
|---|---|---|
| **CSR** (SPA) | App behind a login, SEO irrelevant, rich interaction | Slow first paint, big JS, poor on low-end devices |
| **SSR** | Content matters for SEO/first paint, data is per-request | Server cost, TTFB depends on your backend, hydration cost |
| **SSG** | Content changes rarely | Rebuild on change; stale until rebuilt |
| **ISR / on-demand revalidation** | Mostly static with some freshness | Cache invalidation complexity |
| **Streaming SSR / server components** | Big pages where part of the data is slow | Newer, more complex mental model; needs a supporting framework |
| **Islands / partial hydration** | Mostly-static pages with a few interactive bits | Framework support required |

> [!tip] Say this
> "Product pages are SSG with on-demand revalidation because they're read by crawlers and
> change rarely; the cart and checkout are client-rendered behind auth. Two strategies in one
> app is normal — the question is per-route, not per-app."

Also cover: module boundaries (feature folders, not layer folders), what's shared, how the
BFF shapes payloads so the client doesn't over-fetch, and micro-frontends **only** if the
requirement is independent deploys by separate teams (say the cost: duplicated dependencies,
version skew, harder shared state — don't propose them unprompted).

## D — Data model: three kinds of state

Conflating them is the most common frontend design mistake:

| Kind | Lives in | Tools | Rules |
|---|---|---|---|
| **Server state** | Cache of remote data | React Query / SWR / RTK Query | Has staleness, refetching, retries. **Not** app state |
| **Client state** | Truly local UI (modal open, form draft) | useState/useReducer, a small store | Keep it as local as possible |
| **URL state** | Filters, tabs, pagination, selection | Router params | If it should survive refresh or be shareable, it belongs in the URL |

Normalize entities (`{users: {id: {...}}, posts: {...}}`) so one update doesn't require
hunting through nested arrays, and so two views of the same entity can't disagree.

## I — Interfaces

Two interfaces, and you should draw both:

**Network API** — endpoints, payload shape, pagination (**cursor, not offset**), and what the
client needs that the API doesn't yet give it. Say if you'd add a BFF endpoint to avoid a
waterfall of three dependent requests.

**Component API** —
```tsx
<DataTable
  data={rows}
  columns={columns}          // declarative, not children-parsing magic
  onRowClick={...}
  virtualized                // opt-in behaviour
  emptyState={<Empty/>}      // states are props, not afterthoughts
  loading={isLoading}
  error={error}
/>
```
Cover: controlled vs uncontrolled, composition over configuration (compound components
instead of 30 boolean props), sensible defaults, and an escape hatch (`className`, `render`
props, `asChild`) so the component doesn't have to be forked.

## O — Optimizations (where most of the points are)

**Performance**
- Bundle: code split per route, lazy-load below-the-fold and modal content, tree-shakeable
  imports, analyse and set a budget in CI that **fails the build**.
- Rendering: virtualize long lists (only render what's visible +overscan), memoize expensive
  subtrees, avoid new object/array identities in props (that's the #1 needless re-render).
- Network: preconnect to critical origins, preload the LCP image, prefetch the likely next
  route on hover/idle, HTTP caching with immutable hashed asset URLs.
- **INP specifically**: break long tasks (`scheduler.yield()`, `requestIdleCallback`), move
  heavy work to a web worker, debounce input handlers, keep hydration incremental.
- Images: AVIF/WebP, `srcset`+`sizes`, explicit dimensions (CLS), lazy below the fold,
  `fetchpriority="high"` for the hero.

**Accessibility** — semantic HTML first (a `<button>` beats a `div` with a click handler and
six ARIA attributes), keyboard operability for everything, visible focus, focus trap and
restore for modals, `aria-live` for async updates, 4.5:1 contrast, respect
`prefers-reduced-motion`. WCAG 2.2 AA is the usual target.

**Resilience** — every async surface has four states: loading (skeleton, not a spinner where
you can), empty, error (with a retry), success. Optimistic updates need a rollback path.
Retry with backoff. Offline: service worker for the shell, queued mutations, a clear
"you're offline" affordance.

**Security** — XSS (never `dangerouslySetInnerHTML` with user content; sanitise), CSP,
tokens in httpOnly cookies rather than localStorage, CSRF protection for cookie auth, and
never trust client-side validation as an authorisation boundary.

## The one-sentence closer

> "I'd ship the SSR shell with a 150 KB JS budget, virtualize the list, keep filters in the
> URL, and gate merges on a Lighthouse CI check for LCP and INP — because a design that
> can't be *kept* fast will not stay fast."

## Referenced by

- [8-week study plan](../07-drills/8-week-plan.md)
- [Design an infinite feed (frontend)](infinite-feed.md)
- [Frontend cases index](README.md)
- [Interview playbook](../00-interview-playbook.md)
- [Load balancing and gateways](../02-primitives/load-balancing-and-gateways.md)

## Sources & further reading

- Vendor: `10-resources/vendor/front-end-interview-handbook/` — the front-end system design section
- [Front End Interview Handbook — front end system design](https://www.frontendinterviewhandbook.com/front-end-system-design)
- [web.dev — Core Web Vitals](https://web.dev/articles/vitals), [INP](https://web.dev/articles/inp)
- [WCAG 2.2 quick reference](https://www.w3.org/WAI/WCAG22/quickref/)
