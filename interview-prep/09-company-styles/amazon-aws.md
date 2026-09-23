---
title: Amazon / AWS interview style
type: reference
track: universal
status: drafted
sources: [Exponent 2026, interviewing.io, PracHub 2026]
updated: 2026-09-02
tags: [amazon, aws, leadership-principles, bar-raiser]
---

# Amazon / AWS

## What makes Amazon different

Three things, and all three are structural:

1. **Leadership Principles are scored inside the technical rounds**, not in one separate
   behavioural block. Each interviewer is assigned specific LPs to probe, and they will ask for
   *concrete* examples. Hypothetical or vague answers are an explicit red flag.
2. **A Bar Raiser sits in the loop** — a trained interviewer from a different organisation, with
   **veto power** over the hire. Their job is to check you raise the bar, not merely meet it.
3. **Operational excellence and cost are first-class**, because AWS-native teams live and die by
   them. This is the company most likely to score you on the ops and cost sections.

## The loop

| Round | Focus |
|---|---|
| Phone screen | Coding + LPs |
| Onsite ×4–5 | Coding, system design, LPs woven throughout, one **Bar Raiser** round |

Design rounds run 45–60 minutes. For senior/principal and Solutions Architect roles, expect more
design and more depth on operations and cost.

## What they want in the design round

| Emphasis | What to do |
|---|---|
| **Customer obsession** | Start from the customer's problem and success criteria, not the tech |
| **Operational excellence** | SLOs, alarms, runbooks, dashboards, deployment safety, rollback. Say these unprompted |
| **Cost** | An explicit $/month with the dominant term and the biggest lever. AWS interviewers notice |
| **Scale gradually** | Show the v1 and the path to 100x — "design it enormous immediately" reads as poor judgement |
| **Ownership** | "I'd own the on-call for this; here's the runbook for the top alert" |
| **Dive deep** | Be ready to go two levels below your first answer on any component |
| **Bias for action** | Say what you'd build first and what you'd defer |

## The Well-Architected framework — use it as your checklist

AWS's own six pillars map almost perfectly onto a strong design answer. Walking them at the end
of a round is a very effective closing move at Amazon:

| Pillar | In your answer |
|---|---|
| **Operational excellence** | Monitoring, deployment, runbooks, game days |
| **Security** | AuthN/Z, encryption, least privilege, secrets, audit trail |
| **Reliability** | Multi-AZ, failure modes, retries with backoff, RTO/RPO |
| **Performance efficiency** | Right-sized components, caching, the latency budget |
| **Cost optimisation** | Tiering, right-sizing, spot, egress, lifecycle policies |
| **Sustainability** | Utilisation, region choice, data retention |

Reliability and operational excellence are the two pillars most worth internalising.

## Speaking AWS

You don't have to name AWS services — but for AWS roles, mapping generics to services shows
fluency. Always give the generic reason first, then the service:

| Generic | AWS |
|---|---|
| Object storage | S3 (+ lifecycle to Glacier tiers) |
| CDN | CloudFront |
| Managed relational | RDS / Aurora |
| Managed KV | DynamoDB (+ DAX for caching) |
| Cache | ElastiCache (Redis) |
| Queue / pub-sub | SQS / SNS / EventBridge |
| Streaming log | Kinesis / MSK (managed Kafka) |
| Stream processing | Kinesis Data Analytics / Flink on KDA / EMR |
| Batch + lakehouse | EMR, Glue, Athena, Iceberg on S3, Redshift |
| Orchestration | Step Functions / MWAA (Airflow) |
| Serverless compute | Lambda / Fargate |
| Containers | ECS / EKS |
| Search | OpenSearch |
| ML platform | SageMaker |
| Managed LLMs | Bedrock (and Anthropic's own API for Claude) |
| Secrets / keys | Secrets Manager / KMS |
| Observability | CloudWatch, X-Ray |

> [!warning] Trap
> Listing services instead of designing. "I'd use S3, Lambda, DynamoDB and SQS" is not a design.
> Say what each one is *for* and what it costs you.

## LP evidence to have ready (STAR, with numbers)

Prepare 8–10 stories, each usable for several LPs, each with a measured outcome:

- **Customer obsession** — you changed a design because of what users actually did
- **Ownership** — you fixed something outside your remit / carried a system through its incident
- **Invent and simplify** — you removed complexity, not just added a feature
- **Dive deep** — you found a root cause everyone else had guessed at
- **Deliver results** — you shipped under a hard constraint, with the number
- **Are right, a lot** — you changed your mind on evidence
- **Have backbone; disagree and commit** — you pushed back, lost, and executed well anyway
- **Frugality** — you cut cost materially; name the before and after

Each story: Situation, Task, **Action (mostly "I", not "we")**, Result **with a number**. The
Bar Raiser will push for specifics — "what exactly did *you* do?" — and vague answers fail there.

## Common Amazon design prompts

Design: Amazon.com product page · shopping cart + checkout · order fulfilment tracking ·
inventory reservation · Prime Video streaming · a recommendation system · S3 · DynamoDB ·
a rate limiter for an API gateway · a notification service · warehouse robot coordination ·
a deployment/CI system.

## Sources

- [Exponent — Amazon system design interview (2026)](https://www.tryexponent.com/blog/amazon-system-design-interview)
- [interviewing.io — Amazon hiring process](https://interviewing.io/guides/hiring-process/amazon)
- [PracHub — Amazon Bar Raiser guide 2026](https://prachub.com/resources/amazon-bar-raiser-interview-guide-2026-leadership-principles-signals-and-questions)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [AWS Builders' Library](https://aws.amazon.com/builders-library/) — **the best free operational-excellence reading anywhere**
- [Amazon Leadership Principles](https://www.amazon.jobs/content/en/our-workplace/leadership-principles)
- Local book: `DevOps/System Design on AWS (O'Reilly, 2025).pdf`
