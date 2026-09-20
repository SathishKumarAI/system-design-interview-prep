---
title: Design <X>
type: case
track: backend        # backend | frontend | data | ml
difficulty: core      # intro | core | advanced
status: seed
sources: []
updated: 2026-01-01
tags: []
---

# Design <X>

> One sentence: what the system does and who for.
> **The hard part:** <the one thing this problem is really testing>.

## 1. Clarify

| Question | Assumed answer if waved on |
|---|---|
| Scale — users, read:write ratio? | |
| Latency target, at which percentile? | |
| Consistency / freshness tolerance? | |
| One region or global? | |
| Cost of failure — annoyance, money, safety? | |

**Non-goals:** <written on the board so scope can't creep>

## 2. Requirements

**Functional**
- [ ]
- [ ]

**Non-functional** (numbers, not adjectives)
| Target | Value |
|---|---|
| Availability | |
| p99 latency | |
| Durability | |
| Consistency | |

## 3. Estimates

```
peak_rps   =
storage/yr =
bandwidth  =
cost/month =
```

> [!info] The scary number
> <which of the above is the actual design constraint>

## 4. API / contract

```http
POST /v1/... 
```

## 5. Data model

| Entity | Key | Partition by | Serves |
|---|---|---|---|

**Why this partition key:** <the sentence that wins the interview>

## 6. Architecture

```
client → ... → store
```

**Deep dive:** <the one or two parts worth 15 minutes>

## 7. Scale & failure

| Breaks first at 10x | Fix |
|---|---|

| Component dies / is slow | Blast radius | Degraded behaviour |
|---|---|---|

## 8. Ops & cost

- **SLO:**
- **Alert on:**
- **Rollout:**
- **$/month, dominant term:**
- **First thing I'd cut:**

## Sources & further reading

-
