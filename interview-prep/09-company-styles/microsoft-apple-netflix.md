---
title: Microsoft, Apple, Netflix and other big tech
type: reference
track: universal
status: drafted
updated: 2026-09-02
tags: [microsoft, apple, netflix, uber, stripe]
---

# Microsoft, Apple, Netflix and others

## Microsoft

| | |
|---|---|
| **Format** | 4–5 onsite rounds; usually one design round, more for senior. Often includes an "as-appropriate" round with a senior leader |
| **Style** | Collaborative and conversational — closer to a design discussion with a colleague than an exam |
| **Weights** | Practicality, extensibility, testing, and how you'd work with other teams |
| **Azure-flavoured** | For Azure roles, map generics to Azure services (Cosmos DB, Event Hubs, Service Bus, Data Factory, Synapse, AKS, Blob Storage) |
| **Watch for** | Questions about maintainability, backwards compatibility and versioning — Microsoft ships software people run for a decade |
| **Prompts** | Teams chat · OneDrive sync · a telemetry pipeline · an authentication service · a code-search service · a multi-tenant SaaS control plane |

Say more than usual about **APIs and versioning**, **testing strategy**, and **enterprise
multi-tenancy** — those land well here.

## Apple

| | |
|---|---|
| **Format** | Highly team-dependent; loops vary a lot between orgs |
| **Style** | Deep in the team's specific domain. Less standardised than Meta/Google |
| **Weights** | Domain depth, quality, privacy, on-device constraints |
| **Distinctive** | **Privacy is a first-class design constraint** — on-device processing, differential privacy, minimal data collection. Bring it up unprompted |
| **Watch for** | Resource constraints: battery, memory, offline behaviour, sync across devices |
| **Prompts** | iCloud sync · Photos search on device · Find My · App Store search · a push notification service |

If you're interviewing at Apple, research the specific team. A generic FAANG-shaped preparation
underperforms here more than anywhere else.

## Netflix

| | |
|---|---|
| **Format** | Senior-only hiring; conversational, high-context |
| **Style** | Assumes you have operated systems at scale. Fewer toy problems, more "what did you actually do" |
| **Weights** | Judgement, autonomy, freedom-and-responsibility, real production stories |
| **Distinctive** | Chaos engineering, resilience, streaming/CDN economics are native vocabulary |
| **Watch for** | You'll be asked what you'd do without a process telling you — they hire for judgement |
| **Prompts** | Video streaming and delivery · recommendations · A/B experimentation platform · a resilience/chaos framework · a data pipeline for playback telemetry |

Read [Netflix Open Connect](https://openconnect.netflix.com/) and the
[Netflix Tech Blog](https://netflixtechblog.com/) — their public architecture *is* their
interview vocabulary.

## Uber / Lyft / DoorDash (marketplaces)

Geospatial, matching, pricing and real-time systems.
[../03-backend-cases/ride-hailing.md](../03-backend-cases/ride-hailing.md) is the core case. Know
H3/S2, supply–demand balancing, surge, and the ledger/payout side. Uber's engineering blog is
unusually detailed and worth reading directly.

## Stripe / payments companies

Correctness over scale. Idempotency, ledgers, reconciliation, API design, developer experience.
[../03-backend-cases/payments-ledger.md](../03-backend-cases/payments-ledger.md) plus
[../02-primitives/transactions-and-idempotency.md](../02-primitives/transactions-and-idempotency.md).
Expect deep API-design questions — Stripe cares about the interface as much as the internals.

## Databricks / Snowflake / Confluent (data infrastructure)

Deep data-systems knowledge: query execution, storage formats, distributed joins, streaming
semantics. The [../05-data-cases/](../05-data-cases/README.md) folder plus DDIA chapters 10–11.
Expect questions about the internals of the thing they sell.

## OpenAI / Anthropic / AI labs

Inference serving, evaluation, data pipelines for training, safety and abuse systems. See
[../06-ml-cases/llm-serving-platform.md](../06-ml-cases/llm-serving-platform.md) and
[../06-ml-cases/rag-assistant.md](../06-ml-cases/rag-assistant.md). Expect strong emphasis on
**evaluation methodology** and on cost per token — and on reasoning carefully about failure modes
that aren't crashes.

## A note on "MAANG" preparation generally

The company-specific differences are real but smaller than the internet suggests. In practice:

- 80% of preparation is identical across all of them: the framework, the numbers, the primitives,
  and timed practice.
- 15% is level calibration — knowing what "senior" means where you're applying.
- 5% is company-specific flavour, which is what this folder covers.

Spend your time in that proportion. Candidates who read ten company guides and never run a timed
drill do worse than candidates who ran twenty drills and read none.
