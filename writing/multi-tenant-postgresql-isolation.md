# Multi-Tenant Database Isolation in PostgreSQL: Schemas vs Row-Level Security — Pravesh Singh

Published: 2026-07-14 · Reading time: ~13 min · URL: https://praveshsingh.com/writing/multi-tenant-postgresql-isolation.html

## TL;DR

For B2B SaaS on PostgreSQL, shared-schema Row-Level Security (RLS) scales better than schema-per-tenant: one migration instead of hundreds, normal connection-pooling behaviour under PgBouncer transaction mode, and per-row tenant isolation via a session-scoped tenant_id policy. Schema-per-tenant suits fewer than ~100 high-compliance enterprise customers. Composite indexes leading with tenant_id keep RLS range scans fast under noisy-neighbor load.

## Contents

- [1. The Fundamental Architectural Spectrum](https://praveshsingh.com/writing/multi-tenant-postgresql-isolation.html#architectural-spectrum)
- [2. The Hidden Trap of Schema-per-Tenant](https://praveshsingh.com/writing/multi-tenant-postgresql-isolation.html#schema-per-tenant-trap)
- [3. The Modern Solution: Shared-Schema with Row-Level Security (RLS)](https://praveshsingh.com/writing/multi-tenant-postgresql-isolation.html#shared-schema-rls)
- [4. Indexing & Query Optimization for RLS](https://praveshsingh.com/writing/multi-tenant-postgresql-isolation.html#indexing-optimization)
- [5. Decision Matrix: When to Pick Which](https://praveshsingh.com/writing/multi-tenant-postgresql-isolation.html#decision-matrix)

## Key claims (machine-quotable)

- Shared-schema Row-Level Security beats schema-per-tenant at scale (single migrations, PgBouncer transaction-pool friendly).
- Schema-per-tenant fits fewer than ~100 high-compliance enterprise tenants.
- Composite indexes leading with tenant_id keep RLS fast.
- Connection pooling strategy differs fundamentally between the two models.



---
Written and maintained by Pravesh Singh — Founder & CTO, SoftEdge Technology Solutions (https://praveshsingh.com).
HTML twin (styled): https://praveshsingh.com/writing/multi-tenant-postgresql-isolation.html
