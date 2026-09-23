---
title: Books already on this machine
type: resource
track: universal
status: drafted
sources: [full walk of the library 2026-09-21, LIBRARY-ORGANIZATION.md, own analysis]
updated: 2026-09-21
tags: [books, library]
---

# Books already on this machine

Library root: `C:\Users\PRANAS\Documents\rocky_linux_backup_2026\Obsidian Vault\`
(organisation described in that folder's `LIBRARY-ORGANIZATION.md`).

**Measured 2026-09-21: 246 files — 199 PDFs, 47 epubs, 13 GB.** This file indexes **73 of them.**
The other 173 are excluded on purpose and the reasons are in
[§What is deliberately not indexed](#what-is-deliberately-not-indexed) — a flat list of 246 is a
directory listing, not an index.

Paths below are relative to that root, with the Anna's-Archive hash elided as `…`. To open one:

```bash
find "$LIB" -iname "*Fundamentals of Data*"      # $LIB = the root above
```

## The filenames lie — mangled name → real book

Eleven titles cannot be found by searching for the book's actual name. These are the worst, and
one of them is Tier 1 material that was invisible until this walk:

| On disk | Actually |
|---|---|
| `DE/Warehouse-ETL/Fundamentals of Data.pdf` | **Fundamentals of Data Engineering** — Reis & Housley, O'Reilly 2022 |
| `AI/MLOps/“.pdf` | **Google Machine Learning and Generative AI for Solutions Architects** — Kieran Kavanagh, Packt |
| `AI/LLM-Apps/GENERA_2.PDF` | **Generative AI with LangChain, 2nd ed.** — Auffarth & Kuligin, Packt |
| `AI/Agents/a.pdf` | **Building Agentic AI Systems** — Biswas & Talukdar |
| `AI/Agents/ai agents ge.pdf` | **Mastering AI Agents** — Galileo ebook |
| `AI/Agents/agent evals.pdf` | **Survey on Evaluation of LLM-based Agents** — arXiv 2503.16416, IBM / Yale / HUJI, 2025-03-20 |
| `AI/ML-Foundations/inference.pdf` | **Mathematics for Inference and Machine Learning** — Deisenroth & Zafeiriou, Imperial College lecture notes, 2017 |
| `AI/LLM-Theory/Foundations of LLMS.pdf` | **Foundations of Large Language Models** — Xiao & Zhu, arXiv 2501.09223, CC BY-NC |
| `AI/claude/CCOM eCopy 2.pdf` | **The Claude Code Operating Model** — Jia Huang, early review copy |
| `AI/RAG-Knowledge-Graphs/Retrieval-augmented LMs.pdf` | Akari Asai's retrieval-augmented LM lecture deck (UW) — slides, not a book |
| `DevOps/Observability/Acing the System Design Interview …` | Correct title, **wrong folder** — an interview book, not observability |

Misfiling is systematic, not occasional: Alex Xu vol. 2 sits under `AI/ML-Foundations/`,
*Designing ML Systems* under `DE/Warehouse-ETL/`, *Architecting AI Software Systems* under
`Communication/`, and Nielsen & Chuang's quantum computing text at the `DE/` root. Search by
content, not by folder.

## Tier 1 — read these, in this order

| Book | Path | Read |
|---|---|---|
| **Designing Data-Intensive Applications** (Kleppmann) | `DE/System-Design/Designing Data Intensive Applications.pdf` | **Ch. 5 (replication), 6 (partitioning), 7 (transactions), 8 (distributed trouble), 9 (consistency & consensus)** — the best 150 pages in the whole curriculum. Then 1–4, then 10–11 |
| **System Design Interview vol. 2** (Alex Xu, Sahn Lam, 2023) | `AI/ML-Foundations/Alex Xu_ Sahn Lam - System Design Interview … Volume 2-ByteByteGo Inc (2023).epub` | Proximity service, nearby friends, distributed message queue, metrics monitoring, ad click aggregation, hotel reservation, S3-like object storage, real-time gaming leaderboard |
| **Fundamentals of Data Engineering** (Reis & Housley, 2022) | `DE/Warehouse-ETL/Fundamentals of Data.pdf` | **The vocabulary every data-platform round assumes** — the lifecycle model, batch vs streaming, storage abstractions, the undercurrents (security, DataOps, cost). Read it before [../05-data-cases/](../05-data-cases/README.md) |
| **Designing Machine Learning Systems** (Chip Huyen, 2022) | `DE/Warehouse-ETL/Designing machine learning systems … 2022.pdf` | **All of it if you're targeting ML roles.** Especially features, training-serving skew, monitoring, continual learning |
| **AI Engineering** (Chip Huyen, 2025) | `AI/LLM-Apps/AI Engineering_ Building Applications with Foundation Models … O'Reilly.pdf` | RAG, evaluation, inference optimisation, cost. **The GenAI half of the modern ML round** |
| **Acing the System Design Interview** (Zhiyong Tan, 2024) | `DevOps/Observability/Acing the System Design Interview … Manning.pdf` | Interview-shaped walkthroughs; good complement to Alex Xu (misfiled — see above) |
| **System Design on AWS** (Kumar & Singh, O'Reilly 2025) | `DevOps/System Design on AWS (for True Epub) … .pdf` | Read before any AWS/Amazon interview, and before writing another `On AWS and Azure` section |

## Tier 2 — by track

### LLM serving and inference — the thinnest shelf in most libraries, and not thin here

| Book | Path | Good for |
|---|---|---|
| **Hands-On LLM Serving and Optimization** (Chi Wang & Peiheng Hu, O'Reilly, early release dated 2025-08-15) | `AI/ai/Hands-On LLM Serving and Optimization … .epub` | **The most on-topic book in the library for [../06-ml-cases/llm-serving-platform.md](../06-ml-cases/llm-serving-platform.md).** KV-cache paging, vLLM PagedAttention vs SGLang RadixAttention, single- vs multi-model routing, horizontal/vertical scaling, on-device serving. Its own TOC says "Not Yet Final" — trust the mechanisms, verify the numbers |
| **Foundations of Large Language Models** (Xiao & Zhu, 2025) | `AI/LLM-Theory/Foundations of LLMS.pdf` | Pre-training, alignment, prompting, inference at survey depth. CC BY-NC, so **safe to cite publicly** (arXiv 2501.09223) |
| **The Smol Training Playbook** (Hugging Face, 2025) | `AI/LLM-Theory/The Smol Training Playbook.pdf` | What a real training run costs in *decisions*: ablation tables for attention variant, batch size, LR, weight decay, intra-doc masking, tied embeddings. The honest answer to "how would you train this?" |
| **Foundational LLMs & Text Generation** (Google whitepaper, v2) | `AI/LLM-Theory/whitepaper_Foundational Large Language models & text generation_v2.pdf` | Google's own framing of decoding, sampling and serving trade-offs. Short — one sitting |
| **Survey on Evaluation of LLM-based Agents** (2025) | `AI/Agents/agent evals.pdf` | The agent-benchmark landscape, and the gaps the authors admit to: cost-efficiency, safety, robustness. Pairs with [../06-ml-cases/ml-monitoring-and-eval.md](../06-ml-cases/ml-monitoring-and-eval.md) |

### Cloud — where the `On AWS and Azure` sections get their sources

The [applied-sections contract](../_templates/applied-sections.md) wants the managed service, the
knob, and the default that bites. These four supply them without a browser:

| Book | Path and what it carries |
|---|---|
| **The Definitive Guide to MLOps in AWS** (Sendas & Rajale, Apress 2025) | `AI/MLOps/The Definitive Guide to Machine Learning Operations in AWS … .epub` — its chapters *are* the Well-Architected pillars (operational excellence, security, reliability, performance efficiency, cost), which is the shape §7 asks for |
| **Azure OpenAI for Cloud Native Applications** (Sánchez, O'Reilly 2024) | `AI/LLM-Apps/Azure OpenAI for Cloud Native Applications … .pdf` — ch. 2 is *Designing Cloud Native Architectures for Generative AI*. The Azure half, which the corpus is weakest on |
| **Google ML and Generative AI for Solutions Architects** (Kavanagh, Packt) | `AI/MLOps/“.pdf` |
| **Generative AI on AWS** (Fregly, Barth, Eigenbrode, 2024) | `AI/LLM-Apps/Generative AI on AWS … O'Reilly.pdf` |

### Data engineering and storage

| Book | Path |
|---|---|
| Big Book of Data Engineering (Databricks) | `DE/Fundamentals/Big Book of Data Engineering.pdf` |
| Practical Data Quality (Hawker & Askham, 2023) | `DE/Fundamentals/Practical Data Quality … 2023.pdf` — pairs with [../05-data-cases/data-quality-and-contracts.md](../05-data-cases/data-quality-and-contracts.md) |
| Spark: The Definitive Guide | `DE/Spark/Spark-The Definitive Guide.pdf` |
| Scaling Machine Learning with Spark (Adi Polak, 2023) | `DE/Spark/SCALING MACHINE LEARNING WITH SPARK … 2023.pdf` |
| Architecting a Modern Data Warehouse for Large Enterprises (2024) | `DE/Warehouse-ETL/Architecting a Modern Data Warehouse … 2024.pdf` |
| Apache Airflow Best Practices (2024) | `DE/Warehouse-ETL/Apache Airflow Best Practices … 2024.pdf` |
| Database Design and Modeling with PostgreSQL and MySQL (2024) | `DE/SQL-Databases/Database Design and Modeling … 2024.pdf` |
| Learn PostgreSQL, 2nd ed. (2023) | `DE/SQL-Databases/Learn PostgreSQL - Second Edition … 2023.pdf` — the vendor-side view of [../fundamentals/storage-engines.md](../fundamentals/storage-engines.md) |
| Snowflake Recipes (Apress 2025) | `DE/Warehouse-ETL/Snowflake Recipes … 2025.pdf` |

Two Amazon/Snowflake items in `DE/Warehouse-ETL/` are **papers and vendor guides, not books**, and
belong in [primary-sources.md](primary-sources.md) rather than here: *Automated Multidimensional
Data Layouts in Amazon Redshift* (Ding et al., AWS) and *Modernizing to a Data Lakehouse on
Snowflake*.

### ML / MLOps / RAG

| Book | Path |
|---|---|
| Machine Learning Production Systems (Crowe, Hapke et al., O'Reilly 2025) | `AI/MLOps/Machine Learning Production Systems … 2025.epub` |
| **Machine Learning Yearning** (Andrew Ng, 2018) | `AI/ML-Foundations/Machine_Learning_Yearning__1740294641.pdf` — **error analysis and dev/test-set design.** Short, free, and the best answer to "how do you decide what to fix next?" in an ML case |
| The ML Solutions Architect Handbook, 2nd ed. (David Ping, 2024) | `AI/MLOps/The Machine Learning Solutions Architect Handbook … .epub` — **two near-identical copies in that folder**; either |
| Implementing MLOps in the Enterprise (Haviv & Gift, 2024) | `DE/System-Design/Implementing MLOps in the Enterprise … 2024.pdf` |
| Big Book of MLOps, 2nd ed. (Databricks) | `AI/MLOps/2023-10-EB-Big-Book-of-MLOps-2nd-Edition.pdf` |
| LLM Engineer's Handbook (Iusztin, Labonne, Vesa, 2024) | `AI/MLOps/LLM Engineer's Handbook … 2024.epub` |
| MLOps Engineering at Scale (Osipov, 2022) | `AI/MLOps/Mlops engineering at scale … 2022.pdf` |
| A Simple Guide to Retrieval Augmented Generation (Kimothi, 2025) | `AI/RAG-Knowledge-Graphs/A Simple Guide to Retrieval Augmented Generation … 2025.pdf` |
| Essential GraphRAG (Bratanic & Hane, Manning 2025) | `AI/RAG-Knowledge-Graphs/Essential GraphRAG … 2025.pdf` |
| Knowledge Graphs and LLMs in Action (Negro et al., Manning 2025) | `AI/RAG-Knowledge-Graphs/Knowledge Graphs and LLMs in Action … .pdf` |
| Prompt Engineering for LLMs (Berryman & Ziegler, O'Reilly 2024) | `AI/RAG-Knowledge-Graphs/Prompt Engineering for LLMs … 2024.pdf` |
| AI Evals — The Ultimate FAQ | `AI/RAG-Knowledge-Graphs/AI_Evals_The_Ultimate_FAQ_Free_Resources_1752073495.pdf` |
| Build a Large Language Model (From Scratch) — Raschka, 2024 | `AI/LLM-Theory/Build a Large Language Model (From Scratch) … 2024.pdf` |
| LLMs in Enterprise (Menshawy & Fahmy, Packt 2024) | `AI/LLM-Apps/LLMs in Enterprise … 2024.pdf` — deployment strategy rather than modelling |
| Generative AI with LangChain, 2nd ed. | `AI/LLM-Apps/GENERA_2.PDF` |
| Building Agentic AI Systems (Biswas & Talukdar) | `AI/Agents/a.pdf` |
| Architecting AI Software Systems (Avila & Ahmad, 2025) | `Communication/Architecting AI Software Systems … 2025.pdf` (misfiled) |

### DevOps / platform / observability

| Book | Path |
|---|---|
| Observability with Grafana (2024) | `DevOps/Observability/Observability with Grafana … 2024.pdf` |
| CI/CD Design Patterns (2024) | `DevOps/CICD/CI_CD Design Patterns … 2024.epub` |
| GitHub Actions in Action (Kaufmann, Bos, de Vries, Manning 2024) | `DevOps/CICD/GitHub Actions in Action … 2024.pdf` |
| The Ultimate Docker Container Book, 3rd ed. (2023) | `DevOps/Containers-K8s/The Ultimate Docker Container Book … 2023.pdf` |
| Implementing GitOps with Kubernetes (2024) | `DevOps/Containers-K8s/Implementing GitOps with Kubernetes … .pdf` — **two copies, one byte apart**; either |
| Terraform in Depth (Hafner, Manning 2025) | `DevOps/IaC-Terraform/Terraform in Depth … 2025.pdf` |
| Architecting AWS with Terraform (2023) | `DevOps/IaC-Terraform/Architecting AWS with Terraform … 2023.pdf` |
| Building Serverless Microservices in Python (2019) | `DevOps/Cloud-Certs/Building Serverless Microservices in Python … .pdf` — dated, but the only serverless-decomposition text here |

### Coding and fundamentals (the other rounds)

| Book | Path |
|---|---|
| Coding Interview Patterns (Alex Xu & Gunawardane, 2024) | `DSA/Coding Interview Patterns … 2024.pdf` |
| How to Solve Algorithm Problems (Khamies, 2023) | `DSA/How to Solve Algorithm Problems … leanpub.pdf` — method, not a pattern catalogue |
| Concurrency primer | `Programming/concurrency-primer.pdf` |
| Comprehensive Python Cheatsheet | `Programming/Comprehensive Python Cheatsheet.pdf` |
| Mastering Python Design Patterns, 3rd ed. (2024) | `Programming/Mastering Python Design Patterns … 2024.pdf` |
| Mathematics for Inference and Machine Learning (Imperial, 2017) | `AI/ML-Foundations/inference.pdf` — for the ML-theory round, not system design |

### The talking half — behavioural, and defending a design out loud

Staff rounds are lost in the design review, not the design. `Communication/` holds 18 files; these
four change how a system-design session goes, and none of them was indexed before:

| Book | Path | Why it is here and not in a self-help pile |
|---|---|---|
| **The First Minute** (Chris Fenning, 2020) | `Communication/ǂThe ǂfirst minute … 2020.epub` | Framing a technical update in one sentence — the skill the `1. Clarify` step actually tests |
| **Get Heard, Get Results** (Simon Dowling) | `Communication/Get Heard, Get Results … .epub` | Getting buy-in for a design from people who did not propose it. That *is* the staff bar |
| **Difficult Conversations** (Stone, Patton, Heen, 3rd ed. 2023) | `Communication/Difficult Conversations … 2023.pdf` | Disagreement without escalation — for when the interviewer pushes back and is wrong |
| **Meetings That Get Results** (Metz) | `Communication/Meetings That Get Results … .epub` | Running a design review, for the "tell me about a time you led" half |

Plus the two behavioural Q-banks already in use: *High-Impact Interview Questions* (701
behaviour-based, `Interview/High-impact interview questions … 2017.epub`) and *The Ultimate
Handbook: Answering Behavioral Questions* (`Interview/THE ULTIMATE HANDBOOK … 2023.epub`).

## Which chapter maps to which page here

| This repo | Read alongside |
|---|---|
| [../02-primitives/replication-and-partitioning.md](../02-primitives/replication-and-partitioning.md) | DDIA ch. 5–6 |
| [../02-primitives/consistency-and-consensus.md](../02-primitives/consistency-and-consensus.md) | DDIA ch. 7–9 |
| [../fundamentals/kafka-internals.md](../fundamentals/kafka-internals.md), [../comparisons/batch-vs-streaming.md](../comparisons/batch-vs-streaming.md) | DDIA ch. 10–11; Fundamentals of Data Engineering ch. 8 |
| [../03-backend-cases/](../03-backend-cases/README.md) | Alex Xu vol. 2 + Acing the System Design Interview |
| [../05-data-cases/](../05-data-cases/README.md) | **Fundamentals of Data Engineering** first, then Big Book of Data Engineering, Practical Data Quality |
| [../06-ml-cases/ml-playbook.md](../06-ml-cases/ml-playbook.md) | Designing ML Systems (all) + Machine Learning Yearning (error analysis) |
| [../06-ml-cases/rag-assistant.md](../06-ml-cases/rag-assistant.md) | AI Engineering (Huyen); A Simple Guide to RAG; Essential GraphRAG |
| [../06-ml-cases/llm-serving-platform.md](../06-ml-cases/llm-serving-platform.md) | **Hands-On LLM Serving and Optimization** ch. 1–2, then AI Engineering |
| [../06-ml-cases/ml-monitoring-and-eval.md](../06-ml-cases/ml-monitoring-and-eval.md) | Survey on Evaluation of LLM-based Agents; AI Evals FAQ |
| [../09-company-styles/amazon-aws.md](../09-company-styles/amazon-aws.md) | System Design on AWS; The Definitive Guide to MLOps in AWS |
| [../09-company-styles/microsoft-apple-netflix.md](../09-company-styles/microsoft-apple-netflix.md) | Azure OpenAI for Cloud Native Applications |
| The behavioural round and the design review | The First Minute; Get Heard, Get Results; High-Impact Interview Questions |

## What is deliberately not indexed

173 of the 246 files. Counted, not guessed:

| Excluded | Files | Why |
|---|---:|---|
| `Finance/`, `Mindset/`, `Personal/`, `games/`, `linkedin marketing/` | **37** | Nothing to do with this repo. `Personal/` is tax and visa paperwork and should not be in a library folder at all |
| Unattributed Q-bank and cheat-sheet PDFs — `TOP 50 DSA.pdf`, `llm interview.pdf`, `FullMLCheatSheet_…`, `126+sql questions.pdf`, `Data_Engineering_Interview_Question_…` and ~25 more | **~30** | No author, no date, no source, frequently wrong. Fine as a warm-up shuffle, never the place you learn a topic. [../07-drills/question-bank.md](../07-drills/question-bank.md) is the tracked version |
| Résumés and personal documents filed as books — `AI/LLM-Apps/Jillani Resume.pdf`, `DE/Warehouse-ETL/RESUMES.pdf`, `Interview/file_DB26A620-….pdf` | 3 | Not library material |
| Certification exam guides — AWS ML Specialty ×3, Azure Fundamentals, Azure AI-900, Terraform Associate 003, Docker DCA | ~8 | Certification tests recall; this repo tests design. Worth opening only if you are actually sitting the exam |
| Domain-applied ML — banking ×2, marketing, radiology, life sciences, healthcare, finance | ~10 | Real books, wrong domain. Nothing transfers to the design round |
| Adjacent but not this — LLVM ×2, Mastering Vim, Stable Diffusion, computer vision, graph ML, Kaggle ×2, quantum computing | ~12 | Good books; none is a system-design or ML-infra source |
| Narrow LLM-theory papers and decks — *LLMs can hide text in other text*, *Geometric Algebra Transformer*, *Diffusion vs. Autoregressive*, the medical-agent papers | ~15 | Research interest, not interview or deployment material |
| `pdf/` | 0 books | Five downloaded video courses (mp4 + srt, no PDFs): two transformer explainers, a transformer-from-scratch walkthrough, an 8-hour RAG course, a Docker DCA crash course. The `.srt` transcripts are grep-able; the videos are a first pass only |
| The rest of `Communication/` | 14 | English-language practice, networking, small talk. Real books, not this repo's problem |

**Duplicate titles the de-dup pass missed.** `LIBRARY-ORGANIZATION.md` reports 0 duplicates
outside `_ARCHIVE/`, which is true *byte-for-byte* and misleading by title: *ML Solutions
Architect Handbook* (2 copies in `AI/MLOps/`), *Implementing GitOps with Kubernetes* (2, one byte
apart), *Databricks ML in Action* (2 — epub and pdf in different folders), *Learning LangChain*
(2 — pdf and epub), *AWS Certified ML Specialty* (3 across two folders). A content hash cannot
see a re-encoded copy.

## Overlaps with what this repo already writes

Read these **against** the corpus page, not instead of it. Where one contradicts a page here, the
page wins until proved otherwise — the book was not written for this job:

| Book / chapter | Already covered by | Verdict |
|---|---|---|
| Alex Xu vol. 2 — distributed message queue | [../fundamentals/kafka-internals.md](../fundamentals/kafka-internals.md), [../fundamentals/log-vs-queue.md](../fundamentals/log-vs-queue.md), [../comparisons/messaging-matrix.md](../comparisons/messaging-matrix.md) | Corpus is deeper. Use the book for the interview *narration*, not the mechanism |
| Alex Xu vol. 2 — metrics monitoring | [../03-backend-cases/metrics-monitoring.md](../03-backend-cases/metrics-monitoring.md) | Same ground; the corpus cites Gorilla, the book does not |
| Acing the System Design Interview — consistency chapters | [../fundamentals/consistency-models.md](../fundamentals/consistency-models.md), [../comparisons/consistency-model-matrix.md](../comparisons/consistency-model-matrix.md) | Skip; the book is one level shallower than the pages |
| DDIA ch. 7 — isolation levels | [../fundamentals/transaction-isolation-levels.md](../fundamentals/transaction-isolation-levels.md) | **Not a duplicate.** The page is DDIA plus `vendor/hermitage`'s per-database results. Read both |
| System Design on AWS | every `On AWS and Azure` section | The book is the source those sections should be citing; the sections are the index into it |
| AI Engineering — inference optimisation | [../06-ml-cases/llm-serving-platform.md](../06-ml-cases/llm-serving-platform.md) | Overlaps, and Hands-On LLM Serving is more specific than either |
| Designing ML Systems — monitoring | [../06-ml-cases/ml-monitoring-and-eval.md](../06-ml-cases/ml-monitoring-and-eval.md) | The corpus page already drew from it. Re-reading will not add a number |

## Provenance — what is safe to cite publicly

Stated as fact, not as judgement. This repo is public, and a citation is a public claim.

| Class | Count | Citing it publicly |
|---|---:|---|
| Filenames carrying `Anna's Archive`, `Z-Library` or `libgen.li` | **123 of 246** | Shadow-library copies of commercially sold books. **Cite the book — title, author, publisher, chapter — never the local path and never the file.** Buy or borrow the ones you lean on hardest |
| Free or open by the author's own licence | 6 | **Safe, with the link.** Foundations of LLMs (arXiv 2501.09223, CC BY-NC) · Survey on Evaluation of LLM-based Agents (arXiv 2503.16416) · Machine Learning Yearning (Ng / deeplearning.ai, free) · Mathematics for Inference and ML (Imperial lecture notes) · Automated Multidimensional Data Layouts in Amazon Redshift (AWS-authored) · Retrieval-augmented LMs (Asai, UW lecture deck) |
| Vendor ebooks, free with registration | 6 | **Safe.** Big Book of MLOps and Big Book of Data Engineering (Databricks) · Modernizing to a Data Lakehouse (Snowflake) · Understanding ETL (dlt / O'Reilly) · Agentic Architectures (Weaviate) · Foundational LLMs whitepaper (Google) · The Smol Training Playbook (Hugging Face) |
| Unattributed scraped PDFs — the ~30 Q-banks above | ~30 | Unknown provenance **and** unknown accuracy. Do not cite, and do not learn from |
| Marked "Early Review Copy" or "Not Yet Final" | 2 | *Hands-On LLM Serving and Optimization* and *The Claude Code Operating Model* are pre-publication drafts. Quote nothing; the numbers may not survive editing |

The corpus already follows the safe path: [primary-sources.md](primary-sources.md) cites papers
and vendor docs by link, and the sources convention ([../CONVENTIONS.md](../CONVENTIONS.md) §6)
asks for *book, chapter* — not a file path.

## Gaps worth filling (not currently in the library)

| Gap | Fill it with |
|---|---|
| *System Design Interview* vol. 1 (Alex Xu) | Vol. 2 is here, vol. 1 is not. Its chapters (URL shortener, feed, chat, typeahead, YouTube, Drive) are all covered free by [system-design-primer](https://github.com/donnemartin/system-design-primer) `solutions/system_design/`. **Buy nothing** |
| **DDIA 2nd edition** — the copy here is the 1st | Not out yet. Excerpts are being published as they are written (one, *On Scalability*, dated 2026-08-04 on the [ScyllaDB blog](https://www.scylladb.com/blog/)). Keep reading the 1st edition; watch for the excerpts rather than waiting |
| *Database Internals* (Petrov) — deeper on storage engines than DDIA | Free substitute available and arguably better: the [RocksDB wiki](https://github.com/facebook/rocksdb/wiki) plus [CMU 15-445](https://15445.courses.cs.cmu.edu/). Buy the book only if you want it linear |
| *Site Reliability Engineering* + *The SRE Workbook* (Google) | Already free — [sre.google/books](https://sre.google/books/). The most-cited source in this corpus's frontmatter (8 pages). There is no gap here, only an unread book |
| *Understanding Distributed Systems* (Vitillo) | Overlaps DDIA ch. 5–9 almost entirely. If the gap is formal grounding rather than breadth, [Kleppmann's Cambridge notes](https://www.cl.cam.ac.uk/teaching/2122/ConcDisSys/dist-sys-notes.pdf) are free and stricter |
| A **finished** LLM-serving book | *Hands-On LLM Serving* is the only one here and it is a draft. Until it ships, the [vLLM blog](https://vllm.ai/blog) (posting 2–3×/week as of 2026-09-21) and the PagedAttention paper are the primary sources — see [engineering-blogs.md](engineering-blogs.md) |

More free replacements, with the corpus's own citation counts: [primary-sources.md](primary-sources.md).

## Referenced by

- [File conventions](../CONVENTIONS.md)
- [GitHub repositories](github-repos.md)
- [Primary sources](primary-sources.md)
- [Resources index](README.md)
