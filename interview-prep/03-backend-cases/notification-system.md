---
title: Design a notification system
type: case
track: backend
difficulty: core
status: drafted
sources: [Alex Xu v1 ch.10]
updated: 2026-09-02
tags: [fanout, queues, dedup, providers, preferences]
---

# Design a notification system

> One service that sends push, email, SMS and in-app notifications for the whole company,
> respecting user preferences, without ever double-sending.
> **The hard part:** third-party providers you don't control, and idempotency across retries
> when the side effect is irreversible (you cannot un-send an email).

## 1. Clarify

| Question | Assumed answer |
|---|---|
| Channels? | Push (APNs/FCM), email, SMS, in-app inbox |
| Who triggers? | Other internal services, via an event or an API call |
| Transactional vs marketing? | Both, with different priority, throttling and opt-out rules |
| Templating/localisation? | Yes — templates versioned, per-locale |
| Scheduling / digests? | Yes — "send at 9am local", daily digest batching |
| Scale? | 10M notifications/day baseline, 100M on a campaign day |
| Delivery guarantee? | At-least-once with dedup; **never** double-send |

**Non-goals:** the content/marketing tooling, consent capture UI, per-channel provider
contracts.

## 2. Requirements

**Functional**
- Accept a notification request, resolve recipients, render per channel, deliver
- Respect preferences, quiet hours, per-user frequency caps and global opt-out
- Retry transient failures; dead-letter permanent ones; expose delivery status
- Priority tiers: transactional (OTP, password reset) never queues behind marketing

**Non-functional**

| Target | Value |
|---|---|
| Transactional latency | p99 < 10 s end to end (OTP is useless at 60 s) |
| Marketing latency | Minutes acceptable |
| Availability | 99.9% ingest; delivery is best-effort per provider |
| Duplicate rate | ~0 — the user-visible failure everyone notices |

## 3. Estimates

```
Baseline 10M/day ≈ 116/s;  campaign 100M in 2h ≈ 14k/s      ← 100x burst is the design
Channel mix: 60% push, 30% email, 10% SMS
Provider limits: FCM ~ millions/min (fine); email provider ~1k/s contracted;
                 SMS ~ 100/s per number pool                 ← the real ceiling
Storage: 100M events × 500 B × 90 days retention = 4.5 TB
Cost: SMS ≈ $0.005–0.05 each → a 10M SMS campaign is $50k–500k. Say this out loud.
```

> [!info] The scary number
> Provider rate limits, not your own capacity. Your system's job is largely to **absorb a
> 14k/s burst and drip it into a 1k/s pipe** without losing anything or double-sending.

## 4. API / contract

```http
POST /v1/notifications
{
  "template_id": "order_shipped_v3",
  "recipients": [{"user_id": "u1"}],        // or a segment_id for campaigns
  "data": {"order_id": "A123", "eta": "..."},
  "channels": ["push", "email"],            // or "auto" → preference-driven
  "priority": "transactional",
  "dedup_key": "order_shipped:A123:u1",     // required
  "send_at": null                            // or a timestamp / "user_local_09:00"
}
→ 202 { "notification_id": "..." }

GET /v1/notifications/{id}     → per-channel status timeline
GET /v1/users/{id}/inbox       → in-app notifications, paginated
PUT /v1/users/{id}/preferences
```

**`dedup_key` is mandatory and caller-supplied.** It's the only thing that makes an
irreversible side effect safe under retries — and it must be *semantic* ("this order, this
event, this user"), not a random UUID per attempt.

## 5. Data model

| Entity | Key | Partition by | Serves |
|---|---|---|---|
| `notifications` | `notification_id` | `hash(id)` | Status API, audit |
| `deliveries` | `(notification_id, channel)` | `hash(notification_id)` | Per-channel state machine |
| `dedup` | `dedup_key` UNIQUE, TTL 7d | `hash(key)` | The double-send guard |
| `preferences` | `user_id` | `user_id` | Channel opt-in, quiet hours, caps |
| `devices` | `(user_id, device_token)` | `user_id` | Push targets; tokens expire constantly |
| `inbox` | `(user_id, created_at DESC)` | `user_id` | In-app list + unread count |
| `templates` | `(template_id, version, locale)` | — | Rendering |

Delivery state machine: `queued → rendered → sent → delivered → opened | failed | bounced |
suppressed`. Only legal transitions; every transition timestamped. This table is what the
support team lives in.

## 6. Architecture

```
callers → ingest API ──(dedup check, validate, persist)──→ Kafka: notif.requested
                                                                  │
                                     ┌────────────────────────────┴───────────────┐
                            preference/eligibility service               scheduler (send_at,
                            (opt-out, quiet hours, caps, locale)          user-local time, digests)
                                                │
                   Kafka topics per channel × priority (push.txn, push.mkt, email.txn, sms.txn…)
                                                │
                      channel workers (rate-limited per provider, token bucket)
                                                │
                        provider adapters → APNs / FCM / SES / Twilio
                                                │
                              webhooks in ← delivery/bounce/open events → deliveries table
```

### Deep dive A — never double-send

Layered, because one layer is not enough:

1. **Ingest dedup**: `INSERT dedup_key` with a unique constraint, inside the same transaction
   that persists the notification. Duplicate → return the original `notification_id`, 202,
   no new work.
2. **Per-delivery idempotency**: pass a provider-side idempotency key where supported
   (SES/Twilio/Stripe-style), so a retry after an ambiguous timeout doesn't resend.
3. **The ambiguous case** — you sent the request and never got a response. You genuinely
   cannot know. Policy per channel: for SMS/email, **do not retry** an ambiguous send for
   transactional messages (a missing OTP is recoverable by the user; a duplicate charge
   notification is not); for push, retry (cheap, and clients dedupe on `dedup_key`).
4. **Client-side dedup** on `dedup_key` for push and in-app, as the last net.

> [!tip] Say this
> "Retries are safe for push and unsafe for SMS, so the retry policy is per channel, not
> global. That's the kind of thing that has to be a config knob because the right answer is
> a business decision."

### Deep dive B — absorbing bursts, respecting provider limits

- Separate topic per (channel × priority). A marketing campaign fills `email.mkt`; `email.txn`
  stays empty and fast. **This is a bulkhead** and it's why an OTP still arrives during a
  campaign.
- Channel workers hold a **token bucket sized to the provider contract**, shared across
  workers via the pattern in [rate-limiter.md](rate-limiter.md). Exceeding a provider's rate
  gets you throttled or blocklisted — worse than being slow.
- Campaigns get admission control: a 100M-recipient campaign is chunked and drip-fed with an
  explicit completion deadline, and it's visible on a dashboard while it drains.
- Backpressure: if `email.mkt` lag exceeds the campaign deadline, alert and stop accepting new
  campaigns — do not silently fall further behind.

### Deep dive C — preferences, caps and quiet hours

- Evaluated **at send time, not at enqueue time**: a user who opts out while a campaign is
  draining must stop receiving it.
- **Frequency caps** ("max 3 marketing pushes/week") need a per-user counter with a sliding
  window — same primitive as the rate limiter, different purpose.
- **Quiet hours** need the user's timezone and shift the send, not drop it — unless the
  notification has expired (a "your ride is here" push at +8 h is worse than nothing, so
  notifications carry a TTL and are dropped, with a metric, when stale).
- Global suppression list (hard bounces, complaints, unsubscribes, regulatory) is checked
  last and always wins. Sending to a hard-bounced address damages domain reputation for
  *every* email you send.

## 7. Scale & failure

| Breaks first at 10x | Fix |
|---|---|
| Provider throughput | More provider accounts/pools, multi-provider routing, longer drip windows |
| Preference lookups per send | Cache preferences with a short TTL + invalidate on change |
| Campaign recipient resolution (segment of 100M) | Resolve in batches into the queue, don't materialise 100M rows first |
| Webhook ingest volume (delivery/open events) | Sample opens; aggregate before writing |

| Component fails | Blast radius | Degraded behaviour |
|---|---|---|
| One provider down | That channel stalls | Failover to a secondary provider (per-channel routing table); queue retains everything |
| Preference service down | Can't evaluate eligibility | **Fail closed for marketing, fail open for transactional** — say this trade explicitly |
| Dedup store down | Double-send risk | Fail closed: reject new sends rather than risk duplicates |
| Kafka lag | Delayed notifications | TTL drops stale ones; transactional topics prioritised |
| Template service down | Can't render | Cached compiled templates; last-known-good |

## 8. Ops & cost

- **SLO:** 99% of transactional notifications delivered to the provider within 10 s;
  duplicate rate < 0.01%; bounce rate < 2% (above that, your email reputation degrades).
- **Alert on:** per-channel queue lag, provider error/throttle rate, bounce and complaint
  rates, dedup-conflict rate (a spike means a caller is buggy), TTL-drop count.
- **Rollout:** template changes are content changes — preview + send-to-self + 1% canary
  cohort. A bad template reaching 10M inboxes cannot be rolled back.
- **Cost:** SMS dominates and is not close ($0.005–0.05 each). Email ≈ $0.0001. Push ≈ free.
  The design lever is **channel selection**: pushing users toward push/in-app instead of SMS
  saves more than any infrastructure change.
- **First thing I'd cut:** open/click event retention, and SMS as a default channel.

## Referenced by

- [Backend cases index](README.md)
- [Question bank](../07-drills/question-bank.md)
- [Repo index](../../INDEX.md)

## Sources & further reading

- Local book: Alex Xu vol. 1 ch.10 (notification system)
- [AWS Builders' Library — Avoiding fallback in distributed systems](https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/)
- Primitives: [messaging-and-streams](../02-primitives/messaging-and-streams.md), [transactions-and-idempotency](../02-primitives/transactions-and-idempotency.md), [reliability-patterns](../02-primitives/reliability-patterns.md)
