---
title: Security and multi-tenancy
type: primitive
track: universal
difficulty: core
status: drafted
sources: [OWASP, AWS Well-Architected security pillar]
updated: 2026-09-02
tags: [auth, tenancy, privacy, abuse]
---

# Security and multi-tenancy

You will not be asked to design a security system, but a design that ignores auth, tenancy
isolation and abuse reads as junior. Two minutes, every time.

## AuthN vs AuthZ

- **Authentication**: who are you. **Authorization**: what may you do.
- Where they live: token validation at the gateway (cheap, uniform); **ownership checks in
  the service** (only it knows that row 42 belongs to tenant 7). Never trust a tenant ID sent
  by the client — derive it from the token.

| Mechanism | Use | Watch out |
|---|---|---|
| Session cookie + server store | Classic web; instant revocation | Needs a session store lookup; CSRF protection required |
| **JWT (short-lived access + refresh)** | Stateless APIs, microservices | **Revocation is the hard part** — keep access tokens 5–15 min, keep a refresh-token denylist |
| OAuth2 / OIDC | Third-party login, delegated access | Get the grant type right: auth code + PKCE for apps, client credentials for services |
| API keys | Server-to-server, partners | Rotate; scope; never in the URL (they end up in logs) |
| mTLS | Service-to-service inside the mesh | Cert lifecycle is the operational cost |

**Authorization models:** RBAC (roles — simple, coarse) → ABAC (attributes — flexible,
harder to reason about) → ReBAC (relationship graph, Zanzibar-style: "user is editor of
document via folder"). Say Zanzibar/relationship-based when the product has sharing
semantics — that's exactly what it was built for.

## Multi-tenancy isolation

| Model | Isolation | Cost | Use |
|---|---|---|---|
| Shared everything, `tenant_id` column | Weakest — one bad query leaks | Cheapest | SMB SaaS at scale |
| Shared DB, schema per tenant | Better; noisy-neighbour still shared | Medium | Mid-market |
| DB per tenant | Strong; easy per-tenant restore | Higher ops | Enterprise, regulated |
| **Cell / stack per tenant group** | Strong blast-radius isolation | Highest | Large enterprise, compliance |

Enforcement that survives a mistake: **row-level security in the database**, or a
repository layer where the tenant filter is impossible to omit. A `WHERE tenant_id = ?` a
developer must remember to type will eventually not be typed.

**Noisy neighbours** need per-tenant quotas and rate limits, and often a dedicated shard for
the whale.

## Data protection

- **In transit**: TLS everywhere, including inside the VPC (mTLS in the mesh).
- **At rest**: disk encryption is table stakes and protects against a stolen disk, nothing
  else. **Field-level encryption** for PII/secrets is what protects against an application
  bug or an over-broad query.
- **Key management**: KMS/HSM, rotation, envelope encryption. Never a key in the repo.
- **Secrets**: a secrets manager with short-lived dynamic credentials, not env vars baked
  into an image.
- **PII**: know where it lives (data map), how it's deleted (GDPR erasure — including from
  backups, derived stores, and your log archive: this is where designs quietly fail),
  and residency constraints (EU data staying in EU changes your replication topology).
- **Tokenisation** for card data so PCI scope stays inside one small service.

## Abuse and the internet being the internet

| Threat | Design response |
|---|---|
| Credential stuffing | Rate limit per account *and* per IP, breached-password check, MFA, exponential lockout |
| Scraping | Per-key quotas, anomaly detection on access patterns, bot detection |
| DDoS | Anycast + edge absorption, SYN cookies, upstream scrubbing; you cannot solve this in the app tier |
| Spam / fraud content | Async classification + human review queue; never synchronous in the write path |
| Enumeration (`GET /user/1,2,3…`) | Opaque/random IDs, authorization checks per object |
| Replay | Nonces, short-lived signed requests, idempotency keys |

## The list you can recite (OWASP-flavoured)

Broken access control · injection (parameterised queries, always) · SSRF (allowlist outbound,
block link-local metadata endpoints) · insecure deserialization · dependency vulnerabilities
(SBOM + scanning in CI) · secrets in code (pre-commit scanning) · missing audit logging.

**Audit log**: append-only, tamper-evident, retained. Who did what to which record, when.
Every enterprise design needs it and almost no candidate mentions it.

## Interview lines

> [!tip] Say this
> "Tenant isolation is enforced by row-level security in Postgres, not by application code —
> so a forgotten `WHERE` clause is a failed query, not a data breach."

> [!tip] Say this
> "Access tokens live 10 minutes so revocation lag is bounded without a lookup on every
> request; refresh tokens are stateful and revocable. That's the trade between stateless
> scale and being able to log someone out."

## Numbers

| Quantity | Typical |
|---|---|
| Access token lifetime | 5–15 min |
| Refresh token lifetime | Days–weeks, rotating |
| bcrypt/argon2 hash | ~100 ms deliberately (that's the point) |
| Per-IP login limit | ~5/min, exponential backoff |
| Audit log retention | 1–7 years (regulated) |

## Sources & further reading

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [AWS Well-Architected — Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- [Google Zanzibar paper (authorization at scale)](https://research.google/pubs/pub48190/)
- Repo notes: `data engineering/AWS/Security/`
