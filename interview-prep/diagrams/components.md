---
title: Diagram component library
type: reference
track: universal
status: drafted
updated: 2026-09-02
tags: [diagrams, mermaid, conventions]
---

# Diagram component library

Shared visual vocabulary. **Every diagram in this repo reuses these snippets** — same shapes,
same names, same colours — so a reader who has seen one architecture diagram can read all of
them without re-learning the notation.

Mermaid, because it is plain text: git-diffable, reviewable in a PR, and it renders natively on
GitHub, GitLab, Obsidian and VS Code with no plugin or export step.

---

## 1. Which diagram type, when

| Use | Type | Because |
|---|---|---|
| Component layout — what talks to what | `flowchart LR` | Shows topology and data flow direction |
| Request flow — ordering, round trips, latency | `sequenceDiagram` | Makes round-trip count and blocking explicit; the one that exposes latency budget |
| Lifecycle — order, payment, session, model rollout | `stateDiagram-v2` | Legal transitions and terminal states |
| Data model — entities, keys, cardinality | `erDiagram` | Where the partition key argument lives |
| Timeline — replication lag, watermarks, label delay | `gantt` (sparingly) | Only when time-ordering is the point |

**A case file should carry at least two types** — one architecture, one sequence. A single generic
box diagram per topic is the anti-pattern this library exists to kill.

---

## 2. Style conventions

| Rule | Value |
|---|---|
| Direction | `LR` for request paths, `TB` for layered/tiered systems |
| Node id | short lowercase (`lb`, `api`, `cache`), label carries the readable name |
| Label format | `Name<br/>detail` — put the technology and the one number that matters in the detail line |
| Arrow: synchronous | `-->` with a verb label (`--> |read|`) |
| Arrow: asynchronous | `-.->` (dotted) — **always** dotted, so async is visible at a glance |
| Arrow: bulk/batch | `==>` (thick) |
| Boundary | `subgraph` for trust, region, or tier boundaries |
| Colour | Only via the `classDef` set below. Never inline `style` |

### The palette (copy this block into any flowchart)

```
classDef client   fill:#e8f0fe,stroke:#4285f4,color:#111
classDef edge     fill:#e6f4ea,stroke:#34a853,color:#111
classDef service  fill:#fff,stroke:#5f6368,color:#111
classDef store    fill:#fef7e0,stroke:#f9ab00,color:#111
classDef cache    fill:#fce8e6,stroke:#ea4335,color:#111
classDef queue    fill:#f3e8fd,stroke:#a142f4,color:#111
classDef external fill:#f1f3f4,stroke:#9aa0a6,color:#111,stroke-dasharray:4 3
```

Meaning: **blue** = client, **green** = edge/network, **white** = your stateless compute,
**amber** = durable state, **red** = cache (volatile — losing it is survivable), **purple** =
async boundary, **grey dashed** = something you don't control.

---

## 3. Reusable snippets

### 3.1 The standard request spine

Start here and delete what the requirements don't justify.

```mermaid
flowchart LR
    c[Client]
    dns[DNS / Anycast]
    cdn[CDN edge<br/>95% hit target]
    lb[L7 load balancer<br/>least-outstanding-req]
    gw[API gateway<br/>authn, rate limit]
    svc[Service tier<br/>stateless, N replicas]
    ch[(Redis<br/>TTL 60s)]
    db[(Primary store<br/>partition: hash user_id)]

    c --> dns --> cdn --> lb --> gw --> svc
    svc --> |read| ch
    ch -.-> |miss| db
    svc --> |write| db

    classDef client fill:#e8f0fe,stroke:#4285f4,color:#111
    classDef edge fill:#e6f4ea,stroke:#34a853,color:#111
    classDef service fill:#fff,stroke:#5f6368,color:#111
    classDef store fill:#fef7e0,stroke:#f9ab00,color:#111
    classDef cache fill:#fce8e6,stroke:#ea4335,color:#111
    class c client
    class dns,cdn,lb edge
    class gw,svc service
    class db store
    class ch cache
```

### 3.2 Cache-aside

```mermaid
flowchart LR
    svc[Service]
    ch[(Cache<br/>LRU, TTL 60s)]
    db[(Database)]

    svc --> |1. GET key| ch
    ch --> |2. miss| svc
    svc --> |3. read| db
    svc -.-> |4. SET key, TTL| ch

    classDef service fill:#fff,stroke:#5f6368,color:#111
    classDef store fill:#fef7e0,stroke:#f9ab00,color:#111
    classDef cache fill:#fce8e6,stroke:#ea4335,color:#111
    class svc service
    class db store
    class ch cache
```

### 3.3 Async boundary — log, consumers, derived stores

The shape behind feeds, search indexes, analytics and CDC. Dotted arrows mark where the
response has already been returned to the caller.

```mermaid
flowchart LR
    svc[Write service]
    db[(Source of truth)]
    k[[Kafka<br/>topic, 1024 partitions<br/>key = entity_id]]
    w1[Consumer:<br/>search indexer]
    w2[Consumer:<br/>feed fanout]
    w3[Consumer:<br/>analytics]
    s[(Search index)]
    f[(Feed cache)]
    o[(Lakehouse)]

    svc --> |txn| db
    svc -.-> |outbox relay| k
    k -.-> w1 --> s
    k -.-> w2 --> f
    k -.-> w3 ==> o

    classDef service fill:#fff,stroke:#5f6368,color:#111
    classDef store fill:#fef7e0,stroke:#f9ab00,color:#111
    classDef queue fill:#f3e8fd,stroke:#a142f4,color:#111
    class svc,w1,w2,w3 service
    class db,s,f,o store
    class k queue
```

### 3.4 Sharded + replicated store

```mermaid
flowchart TB
    r[Router / client driver<br/>hash ring, 256 vnodes]
    subgraph s0["Shard 0 — keys 0x00–0x3f"]
        l0[(Leader)]
        f0a[(Follower)]
        f0b[(Follower)]
        l0 -.-> |async repl<br/>lag p99 200ms| f0a
        l0 -.-> f0b
    end
    subgraph s1["Shard 1 — keys 0x40–0x7f"]
        l1[(Leader)]
        f1a[(Follower)]
        l1 -.-> f1a
    end
    r --> |writes| l0
    r --> |writes| l1
    r --> |reads| f0a

    classDef store fill:#fef7e0,stroke:#f9ab00,color:#111
    classDef service fill:#fff,stroke:#5f6368,color:#111
    class r service
    class l0,l1,f0a,f0b,f1a store
```

### 3.5 Two-stage retrieval + ranking (ML)

```mermaid
flowchart LR
    req[Request]
    ann[[ANN index<br/>100M items → 1k<br/>~10ms]]
    cov[Co-visitation]
    pop[Trending]
    mrg[Merge + dedup + ACL filter]
    fs[(Online feature store<br/>batched multi-get, ~10ms)]
    rank[Ranker<br/>1k items, one batch, ~50ms]
    rr[Re-rank:<br/>diversity, freshness, policy]
    out[Top 20]

    req --> ann --> mrg
    req --> cov --> mrg
    req --> pop --> mrg
    mrg --> rank
    fs --> rank
    rank --> rr --> out

    classDef service fill:#fff,stroke:#5f6368,color:#111
    classDef store fill:#fef7e0,stroke:#f9ab00,color:#111
    classDef queue fill:#f3e8fd,stroke:#a142f4,color:#111
    class req,mrg,rank,rr,out service
    class fs store
    class ann,cov,pop queue
```

### 3.6 Trust / region boundary

```mermaid
flowchart LR
    subgraph pub["Untrusted — public internet"]
        c[Client]
    end
    subgraph dmz["Edge — TLS terminates here"]
        cdn[CDN / WAF]
    end
    subgraph vpc["Private VPC — mTLS between services"]
        api[API]
        db[(Store<br/>encrypted at rest)]
    end
    ext[Third-party PSP]

    c --> cdn --> api --> db
    api -.-> |egress allowlist| ext

    classDef client fill:#e8f0fe,stroke:#4285f4,color:#111
    classDef edge fill:#e6f4ea,stroke:#34a853,color:#111
    classDef service fill:#fff,stroke:#5f6368,color:#111
    classDef store fill:#fef7e0,stroke:#f9ab00,color:#111
    classDef external fill:#f1f3f4,stroke:#9aa0a6,color:#111,stroke-dasharray:4 3
    class c client
    class cdn edge
    class api service
    class db store
    class ext external
```

---

## 4. Sequence diagram templates

### 4.1 Latency budget — annotate every hop

The point of a sequence diagram here is the **round-trip count and the budget**, not the boxes.

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant E as Edge (CDN)
    participant A as API
    participant K as Cache
    participant D as Database

    C->>E: GET /feed
    Note over E: hit ratio 95%<br/>miss path below
    E->>A: forward (0.5ms same-region)
    A->>K: MGET feed:{uid} (0.8ms)
    K-->>A: miss
    A->>D: SELECT ... (3ms)
    D-->>A: rows
    A-->>K: SET TTL 60s (fire-and-forget)
    A-->>E: 200 (p99 budget: 200ms total)
    E-->>C: 200 + Cache-Control
```

### 4.2 Idempotent write with an ambiguous outcome

The shape every money/side-effect design needs.

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant A as API
    participant D as DB
    participant P as Payment provider

    C->>A: POST /charge (Idempotency-Key: k1)
    A->>D: INSERT dedup(k1) + attempt(unknown) [same txn]
    alt key already exists
        D-->>A: unique violation
        A-->>C: 200 stored response (no re-charge)
    else new key
        A->>P: charge (provider idempotency key k1)
        alt success
            P-->>A: succeeded
            A->>D: ledger entries + state=captured
            A-->>C: 200
        else timeout — outcome UNKNOWN
            P--xA: (no response)
            A->>D: attempt stays 'unknown'
            A-->>C: 202 processing
            Note over A,P: reconciler queries provider later<br/>settlement file is the arbiter
        end
    end
```

### 4.3 Async fanout — where the response returns early

```mermaid
sequenceDiagram
    autonumber
    participant U as Author
    participant A as API
    participant D as Post store
    participant K as Kafka
    participant W as Fanout worker
    participant R as Feed cache

    U->>A: POST /posts
    A->>D: persist
    A-->>U: 201 (returns here — everything below is async)
    A->>K: post_created (outbox relay)
    K-->>W: consume
    W->>W: load followers, tier by count
    W-->>R: ZADD feed:{follower} (batched)
    Note over W,R: celebrity accounts skip this<br/>merged at read time instead
```

---

## 5. State and data model templates

### 5.1 Lifecycle

```mermaid
stateDiagram-v2
    [*] --> requested
    requested --> matching
    matching --> offered
    matching --> no_drivers: timeout 30s
    offered --> accepted
    offered --> matching: declined / 15s timeout
    accepted --> in_progress
    in_progress --> completed
    accepted --> cancelled
    completed --> [*]
    cancelled --> [*]
    no_drivers --> [*]
```

### 5.2 Data model — circle the partition key in the label

```mermaid
erDiagram
    CONVERSATION ||--o{ MESSAGE : contains
    USER ||--o{ CONVERSATION_MEMBER : joins
    CONVERSATION ||--o{ CONVERSATION_MEMBER : has

    CONVERSATION {
        uuid conversation_id PK "PARTITION KEY"
        bigint last_seq
    }
    MESSAGE {
        uuid conversation_id PK "PARTITION KEY"
        bigint seq CK "sort key — total order per conversation"
        uuid client_msg_id UK "idempotency"
        text body
    }
    CONVERSATION_MEMBER {
        uuid conversation_id PK
        uuid user_id PK
        bigint last_read_seq
    }
```

---

## 6. Rules

1. **Reuse these snippets.** Copy, rename nodes, change the detail lines. Do not invent a new
   shape or colour for a component that already exists here.
2. **Numbers in labels.** A box that says `Redis` is decoration; `Redis — 2.4 TB, TTL 24h`
   is a design.
3. **Dotted = async, always.** A reader must be able to find the async boundary in one glance.
4. **One diagram, one question.** If a diagram answers both "what is the topology" and "what is
   the request order", split it into a flowchart and a sequence diagram.
5. **Add a snippet here** when a shape recurs in three or more files, and link back to it.

## See also

- [../CONVENTIONS.md](../CONVENTIONS.md) — file format contract
- [topics manifest](../topics/manifest.md) — the canonical topic list

## Sources

- [Mermaid documentation](https://mermaid.js.org/intro/)
- [GitHub — including diagrams in Markdown](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)
