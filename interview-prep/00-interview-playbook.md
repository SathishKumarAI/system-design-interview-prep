---
title: Interview playbook
type: playbook
track: universal
difficulty: core
status: drafted
sources: [DesignGurus 2026, Exponent 2026, Prepfully rubric 2026]
updated: 2026-09-02
tags: [framework, rubric, playbook]
---

# The Interview Playbook

Universal across backend / frontend / data / ML rounds. Track-specific variants:
[frontend RADIO](04-frontend-cases/frontend-playbook.md),
[data](05-data-cases/data-playbook.md),
[ML](06-ml-cases/ml-playbook.md).

---

## 1. What is actually being scored

Five competencies. Interviewers fill a scorecard, not a checklist of technologies.

| Competency | Weak signal | Strong signal |
|---|---|---|
| **Problem navigation** | Starts drawing boxes in minute 2 | Extracts requirements, names the *one* hard part, scopes the rest out loud |
| **Solution design** | A stack list | A design where each component exists because a requirement forced it |
| **Technical depth** | "Use Kafka" | Partitioning key, ordering guarantee, consumer lag, rebalance storm |
| **Trade-off reasoning** | "X is better" | "X, because we need Y; we give up Z, and we can live with Z because…" |
| **Operational maturity** | Silence about failure | SLOs, metrics, canary, circuit breaker, backpressure, blast radius |

Plus the seniority axis, which is orthogonal to all five:

| Level | The bar |
|---|---|
| Mid | Correct, complete design with prompting. Knows the components. |
| **Senior** | **Drives the 45 minutes unprompted.** Picks its own deep dive. Discusses cost, failure, rollout without being asked. |
| Staff+ | Frames the problem, questions the requirement, connects across teams/systems, talks migration path and org cost, not just architecture. |

The gap between "hire" and "strong hire" at senior is almost never more knowledge. It is
**driving instead of responding**.

---

## 2. The clock (45–60 min round)

| Minutes | Phase | Output on the board |
|---|---|---|
| 0–5 | **Clarify + scope** | Bullet list of functional requirements, 3–4 non-functional targets, explicit non-goals |
| 5–10 | **Estimate** | QPS (avg + peak), storage/year, bandwidth, one cost number |
| 10–15 | **API + data model** | 3–6 endpoints/events, key tables with the partition key circled |
| 15–25 | **High-level architecture** | 8–12 boxes, arrows labelled with protocol + sync/async |
| 25–40 | **Deep dive (1–2 max)** | The hard part, at whiteboard-code level of detail |
| 40–50 | **Scale, failure, ops, cost** | Bottleneck table, failure table, SLO + metrics, $/month |
| 50–end | **Wrap** | "If I had more time…", known weaknesses, what I'd build first |

**Say the plan out loud at minute 5.** "I'll spend five minutes on estimates, sketch the
high level, then go deep on the ranking path — tell me if you'd rather go elsewhere."
That single sentence is the clearest seniority signal in the whole round, and it lets the
interviewer steer you to what they want to score.

---

## 3. Phase 1 — Clarify (never skip, never exceed 5 min)

Ask questions whose answers **change the design**. If the answer changes nothing, don't
ask it. Six that almost always change something:

| Question | Why it changes the design |
|---|---|
| Read:write ratio, and absolute scale? | Read-heavy → cache/CDN/replicas. Write-heavy → partitioning, LSM store, queues |
| How fresh must reads be? | Strong consistency → single-leader/quorum. Seconds of staleness → cache + async replication, 10x cheaper |
| Latency target, and at which percentile? | p50 vs p99 decides hedging, timeouts, precompute vs on-demand |
| One region or global? | Global → geo-routing, replication topology, data residency, conflict resolution |
| What is the failure cost — annoyance or money/lives? | Decides at-least-once vs exactly-once, audit trail, idempotency, ledger |
| Who are the users and how many? | Drives every estimate; also decides multi-tenancy and abuse handling |

State the answers you assume when the interviewer says "you decide": *"I'll assume 100M
DAU, read-heavy at 100:1, p99 200ms, single region for v1, and staleness of a few seconds
is acceptable for the feed but not for the balance."* Writing assumptions on the board
means you can never be wrong later — you can only be revising.

**Also write down non-goals.** "No moderation, no payments, no analytics in this design."
Scope control is a scored behaviour.

---

## 4. Phase 2 — Estimate

Full method and reference numbers: [01-numbers.md](01-numbers.md). The three-line version:

```
peak_rps   = DAU × actions_per_day / 86_400 × peak_factor(3–5)
storage/yr = writes_per_day × bytes_per_write × 365 × replication(3) × (1 + index/overhead)
bandwidth  = rps × bytes_per_response          (check egress cost — it dominates for media)
```

Round aggressively (86,400 ≈ 1e5) and say you're rounding. Precision is not the point;
**knowing which number is the scary one** is the point. End estimation with one sentence:
*"So this is a 50k-rps read problem with 20 TB/year of cold data — the reads are the
design problem, storage is boring."*

---

## 5. Phase 3 — API and data model before boxes

Draw the contract first. It forces requirements to become concrete and exposes disagreement
with the interviewer early, while it's still cheap.

- 3–6 endpoints max. Show the pagination token, the idempotency key, the auth scope.
- Then the data model: entities, the **partition/shard key**, the access patterns each
  index serves. Circle the partition key and say *why* — this is where the interview is
  actually won.
- Sanity-check every read requirement against the model: "get user's last 20 posts" →
  which index, how many partitions touched, how many round trips?

---

## 6. Phase 4 — High level architecture

Standard spine — start here, delete what the requirements don't justify:

```
client → DNS/anycast → CDN/edge → LB → API gateway (authn, rate limit, routing)
  → stateless services → cache → primary store
                       ↘ queue/log → async workers → derived stores (search, OLAP, blob)
```

Rules for the drawing:

- **Label every arrow** with protocol and sync/async. An unlabelled arrow is a hidden
  assumption, and hidden assumptions are what interviewers probe.
- **Every box needs a reason.** If you can't name the requirement that forced it, delete it.
  Unjustified components read as cargo-culting and cost you more than a missing one.
- Prefer boring: stateless services, one primary store, one cache, one queue. Add exotic
  parts (consensus, CRDTs, custom sharding) only after you've said why boring fails.
- Say the **request path in one sentence** end to end when you finish drawing. If you can't,
  the diagram is wrong.

---

## 7. Phase 5 — Deep dive (this is the round)

Pick **one or two**, and propose them yourself: *"The interesting part here is fanout on
write vs read for celebrity accounts — can I go deep there?"*

Good deep dives, by shape of problem:

| Problem shape | Deep dive that pays |
|---|---|
| Feed / timeline | Fanout write vs read, hybrid for celebrities, ranking cutoff |
| Chat / presence | Connection state, delivery + ordering guarantees, offline sync, read receipts |
| Counters / limits | Rate-limit algorithm, sharded counters, hot key handling |
| Money | Idempotency, double-entry ledger, exactly-once effect on top of at-least-once delivery |
| Search / typeahead | Index build + refresh path, ranking, tiering hot terms |
| Geo | Cell/quadtree indexing, moving-object update rate, matching |
| ML/GenAI | Feature freshness + training-serving skew, candidate generation vs ranking, eval loop |
| Frontend | Rendering strategy, state sync, virtualization, offline/conflict resolution |

Depth means: data structures, key formats, TTLs, concrete algorithms, and one number.
"LRU cache" is shallow. "Redis, key `feed:{uid}`, sorted set capped at 800 entries,
TTL 24h, ~2 KB/user, ~200 GB for 100M users, refreshed by the fanout worker" is deep.

---

## 8. Phase 6 — Scale, failure, ops, cost

The section that separates senior from mid. Cover all four; two minutes each is enough.

**Bottleneck**: name where it breaks *first* at 10x, and the fix. Every design has one — if
you can't name it, you don't understand your own design.

**Failure**: for each dependency — what happens when it's slow (worse than down), and what's
the degraded behaviour? Vocabulary you should use unprompted: timeout budget, retry with
**exponential backoff + jitter**, circuit breaker, bulkhead, backpressure, load shedding,
graceful degradation, idempotency key, dead-letter queue, blast radius.

**Ops**: SLO (not "it should be fast"), the four RED/USE metrics you'd alert on, tracing
across services, canary + feature flag rollout, and the runbook for the top alert.

**Cost**: one dollar figure per month and its dominant term. Then: "the cheapest 30% saving
here is X." Cost reasoning is explicitly in the senior rubric now.

---

## 9. Scripts to steal

- **Opening:** "Let me restate the problem, agree scope, then estimate, then design. Stop me
  whenever you want to go somewhere specific."
- **Trade-off:** "Two options: A gives us X at the cost of Y; B is the reverse. Given our
  requirement of *R*, I'd take A, and revisit if *R* changes."
- **Unknown:** "I don't know that specific number/system. Here's how I'd reason about it, and
  here's the experiment I'd run to find out." (Never bluff — the fastest way to lose the round.)
- **Interviewer challenges you:** "Good point — that breaks when *…*. Two fixes: … I'd take
  the first because …" (Update the design on the board. Defending a broken design is worse
  than having drawn one.)
- **Running out of time:** "I have 5 minutes left; I'll skip search and cover failure modes,
  which I think matters more here. Say if you'd rather I do search."

---

## 10. Anti-patterns that sink otherwise good candidates

| Anti-pattern | Fix |
|---|---|
| Drawing before clarifying | 5 minutes of questions, always |
| Buzzword salad (Kafka + K8s + Cassandra + Spark, no why) | One component, one reason |
| Silent thinking | Narrate. Silence is unscoreable |
| Designing for 1000x the stated scale | Design for the number you estimated. Mention the next 10x |
| Never mentioning failure or cost | Two dedicated minutes each, unprompted |
| Defending a hole the interviewer found | Concede fast, patch on the board, move on |
| One monolith deep dive with no high level | High level first, always; then dive |
| Ignoring the interviewer's hint | Hints are gifts. Follow them immediately |
| Skipping the data model | It's the highest-signal artefact you produce |

---

## 11. Sources

- [DesignGurus — System Design Interview Guide 2026](https://www.designgurus.io/system-design-interview)
- [Exponent — System Design Interview Guide](https://www.tryexponent.com/blog/system-design-interview-guide)
- [Prepfully — Software Engineer Interview Rubric 2026](https://prepfully.com/interview-guides/software-engineer-interview-rubric-2026)
- [Grokking — System Design Interview Framework 2026](https://www.grokkingsystemdesign.com/system-design-interview-guide)
- [AssessAI — Rubric-based evaluation of system design answers](https://getassessai.com/blog/how-to-evaluate-system-design)
