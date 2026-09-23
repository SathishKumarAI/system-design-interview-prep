---
title: Repo index
type: index
status: drafted
updated: 2026-09-02
tags: [index, moc]
---

# INDEX — the whole repo in one map

Start here. Everything in this vault is reachable from this page.

> **Note on old notes:** files under `basic/` and `data engineering/` predate the current
> conventions — names contain spaces, some links are wikilinks. They are **not** being renamed
> (that breaks inbound links). New material goes in `interview-prep/`.

---

## 1. Interview curriculum — [interview-prep/](interview-prep/README.md)

The current, structured material. Everything below has frontmatter, fixed section order, and
sources.

| Layer | Where | What |
|---|---|---|
| **Framework** | [00-interview-playbook.md](interview-prep/00-interview-playbook.md) | How to run the 45 minutes; what's scored |
| **Numbers** | [01-numbers.md](interview-prep/01-numbers.md) | Latency, capacity, availability, cost |
| **Primitives** | [02-primitives/](interview-prep/02-primitives/README.md) | 12 building blocks with trade-offs and failure modes |
| **Backend cases** | [03-backend-cases/](interview-prep/03-backend-cases/README.md) | 11 worked designs |
| **Frontend cases** | [04-frontend-cases/](interview-prep/04-frontend-cases/README.md) | RADIO + 4 worked designs |
| **Data cases** | [05-data-cases/](interview-prep/05-data-cases/README.md) | Playbook + 4 worked designs |
| **ML / GenAI cases** | [06-ml-cases/](interview-prep/06-ml-cases/README.md) | Playbook + 7 worked designs |
| **Drills** | [07-drills/](interview-prep/07-drills/README.md) | 8-week plan, rubric, question bank, flashcards |
| **Reference** | [08-reference/](interview-prep/08-reference/README.md) | Glossary, technology selection |
| **Company styles** | [09-company-styles/](interview-prep/09-company-styles/README.md) | Amazon/AWS, Meta, Google, others, startups |
| **Resources** | [10-resources/](interview-prep/10-resources/README.md) | Books you own, repos, newsletters, blogs, mocks |
| **Conventions** | [CONVENTIONS.md](interview-prep/CONVENTIONS.md) | How every file here is written |
| **Templates** | [_templates/](interview-prep/_templates/) | Case, primitive, drill log, ADR |

### Every case, alphabetically

**Backend** — [chat](interview-prep/03-backend-cases/chat-messaging.md) ·
[metrics + alerting](interview-prep/03-backend-cases/metrics-monitoring.md) ·
[news feed](interview-prep/03-backend-cases/news-feed.md) ·
[notifications](interview-prep/03-backend-cases/notification-system.md) ·
[file sync / object store](interview-prep/03-backend-cases/object-storage-sync.md) ·
[payments + ledger](interview-prep/03-backend-cases/payments-ledger.md) ·
[rate limiter](interview-prep/03-backend-cases/rate-limiter.md) ·
[ride hailing](interview-prep/03-backend-cases/ride-hailing.md) ·
[search + typeahead](interview-prep/03-backend-cases/search-typeahead.md) ·
[URL shortener](interview-prep/03-backend-cases/url-shortener.md) ·
[video streaming](interview-prep/03-backend-cases/video-streaming.md)

**Frontend** — [collaborative editor](interview-prep/04-frontend-cases/collaborative-editor.md) ·
[design system](interview-prep/04-frontend-cases/component-design-system.md) ·
[infinite feed](interview-prep/04-frontend-cases/infinite-feed.md) ·
[realtime dashboard](interview-prep/04-frontend-cases/realtime-dashboard.md)

**Data** — [CDC pipeline](interview-prep/05-data-cases/cdc-pipeline.md) ·
[clickstream → lakehouse](interview-prep/05-data-cases/clickstream-lakehouse.md) ·
[data quality + contracts](interview-prep/05-data-cases/data-quality-and-contracts.md) ·
[realtime analytics](interview-prep/05-data-cases/realtime-analytics.md)

**ML / GenAI** — [feature store](interview-prep/06-ml-cases/feature-store.md) ·
[feed ranking](interview-prep/06-ml-cases/feed-ranking.md) ·
[fraud detection](interview-prep/06-ml-cases/fraud-detection.md) ·
[LLM serving](interview-prep/06-ml-cases/llm-serving-platform.md) ·
[ML monitoring + eval](interview-prep/06-ml-cases/ml-monitoring-and-eval.md) ·
[RAG assistant](interview-prep/06-ml-cases/rag-assistant.md) ·
[recommender](interview-prep/06-ml-cases/recommender.md)

---

## 2. Concept notes — `basic/`

Longer-form background, largely sourced from
[system-design-primer](https://github.com/donnemartin/system-design-primer). Use these when a
primitive file assumes something you don't know.

| Topic | Notes |
|---|---|
| Fundamentals | [Common Principles](basic/prep/Common%20Principles.md) · [Availability](basic/prep/Availability.md) · [Consistency](basic/prep/Consistency.md) · [CAP theorem](basic/prep/CAP%20theorem.md) |
| Scaling | [Horizontal scaling](basic/prep/Horizontal%20scaling.md) · [Vertical scaling](basic/prep/Vertical%20scaling.md) · [Load balancing](basic/prep/Load%20balancing.md) · [Load Balancer](basic/prep/Load%20Balancer.md) · [Reverse proxy](basic/prep/Reverse%20proxy%20%28web%20server%29.md) |
| Network | [DNS](basic/prep/DNS.md) · [CDN](basic/prep/CDN.md) · [TCP/UDP](basic/prep/TCP%20UDP.md) · [RPC](basic/prep/RPC.md) · [Communication](basic/prep/Communication.md) · [Application Layer](basic/prep/Application%20Layer.md) |
| Data | [SQL or NoSQL](basic/prep/SQL%20or%20NoSQL.md) · [Sharding](basic/prep/Sharding.md) · [Database partitioning](basic/prep/Database%20partitioning.md) · [Database replication](basic/prep/Database%20replication.md) · [Federation](basic/prep/Federation.md) · [Denormalization](basic/prep/Denormalization.md) · [SQL tuning](basic/prep/SQL%20tuning.md) · [Document store](basic/prep/Document%20store.md) · [Wide column store](basic/prep/Wide%20column%20store.md) · [Graph Database](basic/prep/Graph%20Database.md) |
| Performance | [Cache](basic/prep/Cache.md) · [Caching](basic/prep/Caching.md) · [Asynchronism](basic/prep/Asynchronism.md) |
| Architecture | [Microservices](basic/prep/Microservices.md) |
| Advanced | [CI-CD](basic/advanced/CI-CD/CI-CD.md) · [DevOps](basic/advanced/DevOps/DevOps.md) · [CD](basic/advanced/DevOps/CD.md) |
| Old design notes | [Airbnb](basic/advanced/designs%20%28needs%20update%20as%20we%20go%29/Airbnb.md) · [YouTube stream](basic/advanced/designs%20%28needs%20update%20as%20we%20go%29/Video%20Stream/Design%20a%20YouTube%20Video%20Stream.md) · [Design YouTube](basic/advanced/designs%20%28needs%20update%20as%20we%20go%29/Video%20Stream/Design%20Youtube%20-%20System%20Design%20Interview.md) · [Scaling Dropbox](basic/advanced/designs%20%28needs%20update%20as%20we%20go%29/Video%20Stream/how%20we've%20scaled%20Dropbox.md) |
| Setup guides | [MySQL on WSL2](basic/installations_doc/Installation%20of%20MySQL%20in%20WSL2.0.md) · [Spark on WSL](basic/installations_doc/Spark%20Installation%20Guide%20Using%20WSL%20%28Windows%20Subsystem%20for%20Linu.md) |
| SQL practice | [SQL questions](basic/question%20and%20answers/SQL%20questions.md) · [SQL questions updated](basic/question%20and%20answers/SQL%20questions_updated.md) |

---

## 3. Data engineering notes — `data engineering/`

Tool- and platform-specific notes. Pair these with
[interview-prep/05-data-cases/](interview-prep/05-data-cases/README.md), which is the
interview-shaped layer on top.

| Area | Notes |
|---|---|
| Overview | [data engineering](data%20engineering/data%20engineering.md) · [AWS](data%20engineering/AWS/AWS.md) · [AWS intro](data%20engineering/AWS/AWS_intro.md) |
| Ingestion / streaming | [Clickstream data ingestion](data%20engineering/AWS/Clickstream%20data%20ingestion/Clickstream%20data%20ingestion.md) · [AWS Kinesis](data%20engineering/AWS/Integrated/AWS%20Kinesis/AWS%20Kinesis.md) · [Integrated real-time streaming](data%20engineering/AWS/Integrated/Integrated%20real-time%20data%20streaming%20technologies.md) · [Event Hub](data%20engineering/AWS/Event%20Hub/Event%20Hub.md) |
| Processing | [PySpark](data%20engineering/AWS/PySpark/PySpark.md) · [MapReduce](data%20engineering/AWS/MapReduce/MapReduce.md) · [Hive](data%20engineering/AWS/Hive/Hive.md) · [processing](data%20engineering/AWS/processing/processing.md) · [Spark SQL](data%20engineering/database/Spark%20SQL.md) |
| Storage / warehouse | [Delta Lake](data%20engineering/AWS/Delta%20Lake/Delta%20Lake.md) · [AWS Redshift](data%20engineering/AWS/AWS%20Redshift/AWS%20Redshift.md) · [Snowflake](data%20engineering/AWS/SnowFlake/SnowFlake.md) · [Apache Cloudera](data%20engineering/AWS/Apache%20Cloudera/Apache%20Cloudera.md) |
| Orchestration | [Airflow](data%20engineering/AWS/Airflow.md) · [Azure Data Factory](data%20engineering/AWS/Azure%20Data%20Factory/Azure%20Data%20Factory.md) · [streamlined data pipelines](data%20engineering/AWS/streamlined%20data%20pipelines/streamlined%20data%20pipelines.md) |
| Databases | [Databases](data%20engineering/database/Databases.md) · [SQL](data%20engineering/database/SQL/SQL.md) · [SQL Database](data%20engineering/database/SQL/SQL%20Database.md) · [NoSQL](data%20engineering/database/NoSQL/NoSQL.md) · [Cassandra](data%20engineering/database/NoSQL/Apache%20Cassandra.md) · [MongoDB](data%20engineering/database/NoSQL/MongoDb.md) · [Riak](data%20engineering/database/NoSQL/Riak.md) · [Replications](data%20engineering/database/Replications.md) |
| Cloud infra | [EC2](data%20engineering/AWS/EC2/EC2.md) · [AWS Lambda](data%20engineering/AWS/Clickstream%20data%20ingestion/AWS%20Lambda/AWS%20Lambda.md) · [Google Cloud Functions](data%20engineering/AWS/Clickstream%20data%20ingestion/Google%20Cloud%20Functions/Google%20Cloud%20Functions.md) · [CloudFormation](data%20engineering/AWS/AWS%20CloudFormation.md) · [VPC](data%20engineering/AWS/VPC%20.md) · [Regions](data%20engineering/AWS/Regions.md) · [Availability Zone](data%20engineering/AWS/Tags/Availability%20Zone.md) · [resiliency](data%20engineering/AWS/Tags/resiliency.md) · [Security](data%20engineering/AWS/Security/Security.md) |
| Quality / ops | [data testing](data%20engineering/AWS/data%20testing/data%20testing.md) · [Evaluated system performance](data%20engineering/AWS/Evaluated%20system%20performance/Evaluated%20system%20performance.md) · [data migrations](data%20engineering/data%20migrations/data%20migrations.md) |
| CI/CD | [GitHub](data%20engineering/AWS/GitHub/GitHub.md) · [Git Action](data%20engineering/AWS/GitHub/Git%20Action/Git%20Action.md) |
| Privacy | [OpenMined — remote data science](data%20engineering/Openmined_Introduction_to_Remote_DS/Openmined_Introduction_to_Remote_DS.md) · [Use Case](data%20engineering/Openmined_Introduction_to_Remote_DS/Use%20Case.md) |
| Glossary | [dict](data%20engineering/AWS/dict/dict.md) |

---

## 4. Coding practice — `leetcode/`

| Problem | Notes |
|---|---|
| Two Sum | [pro solution](leetcode/twosum/twosum_pro.md) · [student version](leetcode/twosum/twosum_students.md) · [code v2](leetcode/twosum/code_v2.md) · [additional material](leetcode/twosum/additional_material.md) |

Coding-round prep material: `DSA/Coding Interview Patterns (Alex Xu).pdf` in the local library —
see [interview-prep/10-resources/books-on-this-machine.md](interview-prep/10-resources/books-on-this-machine.md).

---

## 5. Repo meta

| File | What |
|---|---|
| [docs/NEXT-SESSION.md](docs/NEXT-SESSION.md) | **Read first on return** — blocking decision, first commands, batch 1 |
| [STATUS.md](STATUS.md) | Where work stopped and the traps that will bite |
| [docs/WORKLOG.md](docs/WORKLOG.md) | Dated entries: what changed, how, why, and the trade-offs found |
| [docs/README.md](docs/README.md) | Index of the reasoning docs, and why the split isn't redundant |
| [docs/sessions/](docs/sessions/) | One immutable record per session, dead ends included |
| [README.md](README.md) | Repo front page |
| [CLAUDE.md](CLAUDE.md) | Rules for agents working here, incl. ADR conventions |
| [main.md](main.md) | Original hand-made map of content (legacy; this INDEX supersedes it) |
| [Resources.md](Resources.md) | Original short resource list (superseded by [10-resources/](interview-prep/10-resources/README.md)) |
| [Track your learning.md](Track%20your%20learning.md) | Daily learning log — **write in this after every drill** |
| `markdown files/` | Link-maintenance scripts |
| `assets/images/` | Diagrams referenced by the old notes |

---

## Where to start, by situation

| Situation | Start at |
|---|---|
| Interview next week | [7-day cut-down plan](interview-prep/07-drills/8-week-plan.md#cut-down-one-week-before-an-interview) |
| Starting from scratch | [interview-prep/README.md](interview-prep/README.md) → [00-interview-playbook.md](interview-prep/00-interview-playbook.md) |
| Want to practise now | [question-bank.md](interview-prep/07-drills/question-bank.md) |
| Forgot a number | [01-numbers.md](interview-prep/01-numbers.md) |
| Forgot a term | [glossary.md](interview-prep/08-reference/glossary.md) |
| Choosing a technology | [tech-selection.md](interview-prep/08-reference/tech-selection.md) |
| Company-specific prep | [09-company-styles/](interview-prep/09-company-styles/README.md) |
