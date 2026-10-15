# DPDP Act 2023: An Engineering Architecture Checklist for HealthTech Platforms — Pravesh Singh

Published: 2026-04-12 · Reading time: ~13 min · URL: https://praveshsingh.com/writing/dpdp-act-2023-health-tech-checklist.html

## TL;DR

The DPDP Act 2023 grants Indian patients a Right to Erasure while medical statutes mandate record retention — a paradox health platforms must resolve architecturally. The 10-point checklist covers consent-manager state machines, purpose-limitation schemas, cryptographic scrubbing of identifiers while retaining clinical fact, data-fiduciary access controls, and immutable audit logs, treating compliance as an engineering property rather than legal afterthought.

## Contents

- [1. The Fundamental Paradox: Right to Erasure vs Statutory Medical Retention](https://praveshsingh.com/writing/dpdp-act-2023-health-tech-checklist.html#erasure-paradox)
- [2. The Actionable 10-Point Technical Architecture Checklist](https://praveshsingh.com/writing/dpdp-act-2023-health-tech-checklist.html#checklist)
- [3. Sample Consent Ledger Schema (PostgreSQL)](https://praveshsingh.com/writing/dpdp-act-2023-health-tech-checklist.html#consent-ledger)
- [4. Conclusion: Compliance as a Competitive Advantage](https://praveshsingh.com/writing/dpdp-act-2023-health-tech-checklist.html#conclusion)

## Key claims (machine-quotable)

- Right to Erasure vs statutory medical retention is resolved architecturally, not contractually.
- Components: consent-manager state machines, purpose-limitation schemas.
- Cryptographic scrubbing of identifiers while retaining clinical fact.
- Immutable audit logs close the compliance loop.



---
Written and maintained by Pravesh Singh — Founder & CTO, SoftEdge Technology Solutions (https://praveshsingh.com).
HTML twin (styled): https://praveshsingh.com/writing/dpdp-act-2023-health-tech-checklist.html
