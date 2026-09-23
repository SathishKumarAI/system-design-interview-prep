---
title: Observability and delivery
type: primitive
track: universal
difficulty: core
status: drafted
sources: [Google SRE book, OpenTelemetry]
updated: 2026-09-02
tags: [slo, metrics, tracing, canary, deploy]
---

# Observability and delivery

Scored explicitly at senior+ since 2026. Two minutes on this in every design, unprompted.

## SLI / SLO / error budget

- **SLI** — the measurement: "proportion of `GET /feed` requests served < 300 ms".
- **SLO** — the target: "99.9% over 28 days".
- **Error budget** — 100% − SLO. At 99.9% that's 43 minutes/month of failure you are
  *allowed* to spend. Budget left → ship fast. Budget burned → freeze features and fix
  reliability. It converts "how reliable should we be" from an argument into a number.

> [!tip] Interview line
> "The SLO is 99.9% of feed reads under 300 ms at p99, measured at the edge. That gives us
> 43 minutes of budget a month, which is what justifies async fanout instead of a
> synchronous multi-region write."

Measure at the **client or edge**, not inside your service — the user's experience includes
the network and the queueing you don't see from inside.

## What to instrument

**RED** for request-driven services: **R**ate, **E**rrors, **D**uration.
**USE** for resources: **U**tilisation, **S**aturation, **E**rrors.

Plus the ones people forget and interviewers love:

| Metric | Why it matters |
|---|---|
| Queue depth and age | The leading indicator of everything |
| Consumer lag | Tells you how stale every derived store is |
| Cache hit ratio and eviction rate | Hit rate collapse precedes DB collapse |
| Connection pool saturation | The most common invisible bottleneck |
| Replication lag (seconds *and* bytes) | Data loss exposure on failover |
| Cost per request | Nobody graphs it; it's how bills triple quietly |

## Three signals

| Signal | Good for | Cost |
|---|---|---|
| **Metrics** | Aggregates, alerting, dashboards, long retention | Cheap; cardinality is the trap (never put user ID in a label) |
| **Logs** | Detail on one event, forensic | Expensive at volume; sample aggressively, structure them (JSON) |
| **Traces** | Where the latency went across services | Sample (head or tail); tail sampling keeps the slow ones, which is what you want |

Standardise on **OpenTelemetry**; propagate a trace ID from the edge through every hop and
put it in every log line and error response. "What's your trace ID?" turns a two-day support
investigation into a two-minute one.

## Alerting

- **Alert on symptoms, not causes.** "p99 latency above SLO" pages someone; "CPU 80%" does not.
- Every page needs a runbook link and a plausible human action. If there is no action,
  it's a dashboard, not a page.
- **Burn-rate alerting**: page when the error budget is burning fast enough to exhaust the
  window (e.g. 14.4x for 1 hour), not on every blip.
- Alert fatigue is a reliability risk in itself — say it.

## Deployment

| Strategy | Buys | Costs |
|---|---|---|
| Rolling | Simple, no extra capacity | Both versions live at once — needs compatible schemas/APIs |
| **Blue/green** | Instant rollback | 2x capacity during the switch |
| **Canary** (1% → 10% → 50% → 100%) | Catches bad releases at 1% of blast radius | Needs per-cohort metrics and automated abort |
| **Feature flags** | Decouple deploy from release; kill switch without a deploy | Flag debt; flags must be cleaned up or they become permanent branches |

Say **"deploy ≠ release"**: ship the code dark, enable by flag for 1% of users, watch the
metric that would move, ramp. That is how you make a risky change boring.

**Migrations**: expand → migrate → contract. Both versions must work at every step, and
every step must be revertible on its own. Never ship a schema change and the code that
requires it in the same release.

## Incident basics worth naming

- Blast radius: **cell-based architecture** (shard the whole stack per cell/tenant group) so
  one bad deploy or poison tenant hits 1/N of users, not everyone.
- Rollback must be faster than fix-forward, and rehearsed.
- Blameless postmortems, action items with owners, and the follow-up actually done —
  otherwise you buy the same outage twice.

## Interview lines

> [!tip] Say this
> "I'd instrument fanout lag as a first-class SLI, because it's the metric that tells us the
> product is broken while every server metric looks green."

> [!tip] Say this
> "Rollout is 1% canary for an hour with automatic abort on error-rate delta, behind a flag
> so we can kill it without a deploy. That's the difference between a bad release being a
> nuisance and being an incident."

## Numbers

| Quantity | Typical |
|---|---|
| Metric scrape interval | 10–60 s |
| Metric retention | 15 mo aggregated, high-res days |
| Trace sampling | 0.1–1% head, plus tail sampling of slow/errored |
| Log volume | 1–10 KB/request — price it, it surprises people |
| Canary bake time | 15 min – 1 h per step |

## Sources & further reading

- [Google SRE Book — SLOs, monitoring, releases](https://sre.google/sre-book/table-of-contents/)
- [OpenTelemetry docs](https://opentelemetry.io/docs/)
- Local book: `DevOps/Observability/Observability with Grafana ...pdf`
- Local book: `DevOps/CICD/CI_CD Design Patterns ...epub`
- Repo notes: [../../basic/advanced/CI-CD/CI-CD.md](../../basic/advanced/CI-CD/CI-CD.md), [../../basic/advanced/DevOps/DevOps.md](../../basic/advanced/DevOps/DevOps.md)
