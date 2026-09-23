---
title: Primary sources
type: resource
track: universal
status: drafted
sources: [citation audit of fundamentals/ patterns/ comparisons/ 2026-09-20, own analysis]
updated: 2026-09-20
tags: [papers, specs, docs, primary]
---

# Primary sources

**This file was reverse-engineered from the corpus.** Every external link in
`fundamentals/`, `patterns/` and `comparisons/` was counted on 2026-09-20; anything cited
repeatedly and not already indexed here is listed below, with its citation count. A source you
lean on forty times and never wrote down is the most expensive gap in a resource index — it is
the one you re-find by search, every time.

**Cited** = occurrences of that domain across the 40 mechanism pages, 2026-09-20.

| Question | Section |
|---|---|
| Which paper do I actually have to read? | [§1 Papers](#1-papers-with-links-that-work) |
| Where does the real behaviour of a system get documented? | [§2 Official docs](#2-official-docs-the-corpus-leans-on) |
| Who writes the good stuff, by name? | [§3 People](#3-people-not-companies) |
| Where do I go deep for free? | [§4 Courses](#4-free-courses-that-beat-the-paid-ones) |

---

## 1. Papers, with links that work

Nine papers were listed by name in [engineering-blogs.md](engineering-blogs.md) with no links.
These are the links, verified 2026-09-20, plus the four the corpus actually leans on hardest.

| Paper | Read it for | Link |
|---|---|---|
| **Dynamo** (Amazon, SOSP 2007) | Consistent hashing, sloppy quorums, hinted handoff, vector clocks. The KV blueprint, and the source of the "eventual consistency" vocabulary everyone misuses | [PDF](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf) |
| **Scaling Memcache at Facebook** (NSDI 2013) | **Cited 4× in this corpus — more than any other paper.** Lease-based stampede control, the cold-cluster warm-up, why they chose to serve stale. The caching pages are built on it | [PDF](https://www.usenix.org/system/files/conference/nsdi13/nsdi13-final170_update.pdf) |
| **Metastable Failures in Distributed Systems** (HotOS 2021) | The formal shape of "the retry storm that will not drain even after the trigger is gone". The single best framing for the load-shedding and admission-control pages | [PDF](https://sigops.org/s/conferences/hotos/2021/papers/hotos21-s11-bronson.pdf) |
| **Raft** (Ongaro & Ousterhout, 2014) | Read this one properly, including §6 membership changes — that is where the follow-up questions live | [PDF](https://raft.github.io/raft.pdf) · [site](https://raft.github.io/) |
| **Spanner** (Google, OSDI 2012) | TrueTime, and the commit-wait latency you pay for external consistency. The honest version of "just use a globally consistent database" | [Google Research](https://research.google/pubs/spanner-googles-globally-distributed-database/) |
| **Bigtable** (Google, OSDI 2006) | Wide-column model and the LSM lineage that became HBase, Cassandra and RocksDB | [Google Research](https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/) |
| **Amazon Aurora** (SIGMOD 2017) | "The log is the database" — storage/compute separation, quorum writes over 6 copies in 3 AZs, and why they stopped shipping pages | [Amazon Science](https://www.amazon.science/publications/amazon-aurora-design-considerations-for-high-throughput-cloud-native-relational-databases) |
| **Gorilla** (Facebook, VLDB 2015) | Delta-of-delta + XOR compression. The numbers behind every time-series answer | [PDF](https://www.vldb.org/pvldb/vol8/p1816-teller.pdf) |
| **Zanzibar** (Google, ATC 2019) | Relationship-based authorization at scale, and the "zookie" consistency token — the cleanest worked example of bounded staleness as a product decision | [USENIX](https://www.usenix.org/conference/atc19/presentation/pang) |
| **MapReduce** (Google, OSDI 2004) | Historical, but the shuffle and the straggler discussion still set the vocabulary for every batch answer | [Google Research](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/) |
| **PagedAttention / vLLM** (2023) | Why modern LLM serving works: KV-cache paging, continuous batching | [arXiv 2309.06180](https://arxiv.org/abs/2309.06180) |

Where to find the rest:

| Source | Cited | Use it for |
|---|---|---|
| [research.google/pubs](https://research.google/pubs/) | 14 | Google's own papers, free, with abstracts. The origin of half the vocabulary in this repo |
| [USENIX proceedings](https://www.usenix.org/publications/proceedings) | 6 | NSDI / OSDI / ATC — **all open access**. Where the operational papers are: Memcache, Zanzibar, Kafka-at-LinkedIn-scale, TAO |
| [ACM Queue](https://queue.acm.org/) | 9 | Practitioner-written, and **open access since January 2026**. The best single-article explanations of tail latency, timeouts and queueing exist here |
| [arXiv](https://arxiv.org/) | 5 | Anything ML/LLM-serving, before it reaches a venue |
| [Jepsen analyses](https://jepsen.io/analyses) · [consistency map](https://jepsen.io/consistency) | 8 | **What a database actually does under partition**, versus what its marketing claims. The consistency map is the reference for which model implies which |

## 2. Official docs the corpus leans on

Cited constantly, indexed nowhere until now. These are the sources that make a claim a claim
rather than a recollection.

| Docs | Cited | Read specifically |
|---|---|---|
| [AWS Builders' Library](https://builder.aws.com/learn/topics/builders-library) | 9 | **Moved from `aws.amazon.com/builders-library`.** *Timeouts, retries and backoff with jitter*; *Using load shedding to avoid overload*; *Workload isolation using shuffle-sharding*; *Avoiding fallback in distributed systems*. Four articles that answer four whole pages of this corpus |
| [AWS service docs](https://docs.aws.amazon.com/) | 24 | The most-cited domain in the repo. Quotas and consistency guarantees per service — DynamoDB, SQS, Kinesis, S3 |
| [PostgreSQL docs](https://www.postgresql.org/docs/current/mvcc.html) | 12 | MVCC, isolation levels and what each one *actually* prevents; `pg_stat` for the numbers |
| [MySQL / InnoDB manual](https://dev.mysql.com/doc/refman/8.4/en/innodb-storage-engine.html) | 6 | Gap locks, next-key locking, online DDL — where "MySQL and Postgres behave the same" stops being true |
| [Kafka docs](https://kafka.apache.org/documentation/) + [KIP index](https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Improvement+Proposals) | 3 + 10 | **The KIP wiki is cited 10× and was not in this index.** A KIP states the problem, the rejected alternatives and the compatibility plan — it is the highest-density design-doc reading available for free |
| [Envoy docs](https://www.envoyproxy.io/docs/envoy/latest/) | 5 | Outlier detection, circuit breaking, retry budgets — the blast-radius patterns with real config knobs |
| [Cassandra](https://cassandra.apache.org/doc/latest/) · [Redis](https://redis.io/docs/latest/) · [etcd](https://etcd.io/docs/latest/) · [Vitess](https://vitess.io/docs/) | 6 / 4 / 4 / 2 | Replication, eviction, lease and resharding mechanics from the implementers |
| [Flink](https://nightlies.apache.org/flink/flink-docs-stable/) · [Iceberg](https://iceberg.apache.org/docs/latest/) | 3 / 2 | Exactly-once semantics and table-format compaction, for the streaming comparisons |
| [Google SRE books](https://sre.google/books/) | 8 | Free. *SRE* ch. 21–22 (overload, cascading failure) and *The SRE Workbook* on SLOs and error budgets. The most-cited book in the corpus's frontmatter |
| [use-the-index-luke.com](https://use-the-index-luke.com/) | 3 | Markus Winand on index internals and query plans. Short, correct, and the only free source that explains *why* your index is not used |
| [microservices.io](https://microservices.io/patterns/index.html) | 3 | Chris Richardson's pattern catalogue — the canonical statements of saga, outbox and CQRS that `patterns/` cites |

## 3. People, not companies

Individual blogs cited by this corpus. Higher signal than any company blog, because a person can
say "we got this wrong".

| Who | Cited | Verdict |
|---|---|---|
| [Marc Brooker](https://brooker.co.za/blog/) | 3 | AWS principal engineer. Timeouts, retries, leases, simulation, the maths of queueing. **If you read one blog on this list, read this one** — it is the closest thing to a staff-level distributed-systems curriculum written by one person |
| [Werner Vogels — All Things Distributed](https://www.allthingsdistributed.com/) | 2 | The Dynamo paper's home, plus the annual architecture retrospectives. Sparse now; the archive is the value |
| [Jack Vanlightly](https://jack-vanlightly.com/) | 2 | Replication protocols taken apart formally — Kafka, RabbitMQ, Raft, Iceberg. *"How to lose messages on a Kafka cluster"* is cited in `messaging/` and is the best failure walkthrough of its kind |
| [Martin Kleppmann](https://martin.kleppmann.com/) | 13 (as DDIA) | DDIA's author. The post-book writing on CRDTs and local-first, and the Redlock critique the corpus cites |
| [Dan Luu](https://danluu.com/) | — | Latency, hardware reality, and the postmortem collection in [github-repos.md](github-repos.md) §2. Measured, not argued |

## 4. Free courses that beat the paid ones

| Course | Verdict |
|---|---|
| [MIT 6.5840 — Distributed Systems](https://pdos.csail.mit.edu/6.824/schedule.html) | **The best free distributed-systems course there is.** Lectures, the paper list with reading questions, and the Go labs (MapReduce → Raft → fault-tolerant KV → sharded KV). Doing the Raft lab once is worth more than every system-design course on the market combined |
| [CMU 15-445 — Database Systems](https://15445.courses.cs.cmu.edu/) | Andy Pavlo. Storage, buffer pool, indexes, concurrency control, recovery. Full lecture video + assignments ([BusTub](https://github.com/cmu-db/bustub)) |
| [CMU 15-721 — Advanced Database Systems](https://15721.courses.cs.cmu.edu/) | In-memory, columnar, vectorised execution, query compilation. Take it after 15-445 or after DDIA ch. 3 |
| [Kleppmann — Concurrent & Distributed Systems](https://www.cl.cam.ac.uk/teaching/2122/ConcDisSys/dist-sys-notes.pdf) | Cambridge lecture notes, ~80 pages, free PDF. The formal spine DDIA deliberately leaves out — proofs for the impossibility results you otherwise quote on faith |

## How to use this file

1. **When a mechanism page makes a claim you cannot defend, come here, not to a blog.** The
   citation counts say which source that page was written from.
2. **Papers in §1 get read once, properly, and then only re-skimmed.** Dynamo and Memcache
   between them cover most of what a caching or replication follow-up will ask.
3. **§4 is a commitment, not a resource.** One lab, finished, beats four courses started.

## See also

- [GitHub repositories](github-repos.md) — including the runnable ones (Maelstrom, Hermitage)
- [Engineering blogs and case studies](engineering-blogs.md)
- [Books already on this machine](books-on-this-machine.md)

## Referenced by

- [Books already on this machine](books-on-this-machine.md)
- [Courses and mock interviews](courses-and-mocks.md)
- [Engineering blogs and case studies](engineering-blogs.md)
- [GitHub repositories](github-repos.md)
- [Newsletters and Substacks](newsletters-substack.md)
- [Resources index](README.md)

## Sources

- Citation counts: `grep -rhoE 'https?://[^) >"]+' interview-prep/{fundamentals,patterns,comparisons}`,
  by domain, 2026-09-20 (own analysis)
- Every link above fetched and confirmed 200 on 2026-09-20. `dev.mysql.com` and `queue.acm.org`
  return 403 to `curl` and were confirmed live in a browser-equivalent fetch instead
