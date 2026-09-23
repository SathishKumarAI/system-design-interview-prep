---
title: Applied sections — the contract
type: template
track: universal
status: drafted
updated: 2026-09-20
tags: [template, contract, aws, azure, llm]
---

# Applied sections — the contract

Two sections are added to every `type: topic` and `type: comparison` page, between
`Real-world examples` and `Staff-level follow-ups`:

```
## On AWS and Azure
## In an LLM deployment
```

They exist because the corpus explains mechanisms correctly and then stops one step short of the
two places the reader actually has to use them: a cloud console, and a model being put into
production. A page that teaches quorums but never names DynamoDB's `ConsistentRead` has taught the
idea and withheld the handle.

## Why these two and not more

| Section | The question it answers | Why it cannot be inferred from the rest of the page |
|---|---|---|
| `On AWS and Azure` | *Which managed thing IS this, and what do I actually set?* | Every cloud renames the mechanism and picks a default. The default is usually the interview answer's opposite |
| `In an LLM deployment` | *Where does this bite when the thing being served is a model?* | The economics invert. A cache miss costs GPU-seconds, not a disk seek; a retry storm costs real money per token |

## `## On AWS and Azure`

A table, then at most three lines of prose for anything the table cannot hold.

```markdown
## On AWS and Azure

| | AWS | Azure |
|---|---|---|
| **The service** | ElastiCache (Valkey/Redis) | Azure Cache for Redis |
| **What you configure** | `maxmemory-policy`, reserved memory %, cluster mode | Eviction policy, tier, zone redundancy |
| **The default that bites** | No stampede protection of any kind — a mass expiry is your problem | Same; Redis semantics are identical |
| **Where it is solved instead** | CloudFront Origin Shield collapses concurrent origin requests | Front Door caching, rules engine |
```

Rules:

| Rule | Why |
|---|---|
| **Name the service exactly**, as the console spells it | "Azure Redis" is not a thing you can search for |
| **Name the KNOB**, not the capability | "supports TTL" is not a design input; `maxmemory-policy allkeys-lru` is |
| **The default that bites is the most valuable row** — always fill it | Defaults are where production and the interview answer disagree |
| **If a cloud genuinely has no equivalent, say so** | A fabricated service name is worse than a gap, and it is the failure mode of writing this section quickly |
| Every service claim carries a link in `Sources` | This is the section most likely to be quietly wrong, and it ages fastest |
| No pricing figures unless dated | They move, and a stale price read as current is worse than none |

## `## In an LLM deployment`

Prose, 4–10 lines, with at least one number. Not a table — the point is the causal chain, and a
grid hides it.

It must answer: **where does this mechanism appear when the workload is a model, and what changes
about it there?** "It also applies" is not an answer. If the honest answer is that it genuinely
does not apply, write one line saying so and move on — that is useful and takes ten seconds.

The three things worth reaching for, in order of how often they are the real answer:

1. **The economics invert.** A miss, a retry or a duplicate costs GPU-seconds. Quantify it.
2. **The unit of work is enormous and variable.** A 4-second request with a 200:1 spread between
   short and long generations breaks every assumption built on uniform, millisecond requests.
3. **The state is huge and warm.** KV cache, prefix cache, model weights, an embedding index —
   anything that must be resident changes what a restart, a scale-out or an eviction costs.

## Verification — this is the part that goes wrong

This section carries more falsifiable claims than any other, and an LLM writing it will produce
plausible service names that do not exist.

- Every service name, knob and default must be **fetched from vendor documentation**, not recalled.
- Add the doc URL to `Sources`.
- A claim you cannot verify does not get softened — it gets **cut**.
- Say "no direct equivalent" freely. A page with one honest cloud column beats a page with two
  columns where one is invented.

## Referenced by

- [Books already on this machine](../10-resources/books-on-this-machine.md)
- [File conventions](../CONVENTIONS.md)
- [Topic manifest](../topics/manifest.md)
