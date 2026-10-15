# ABDM Integration: A Pragmatic Engineering Guide for HealthTech Developers — Pravesh Singh

Published: 2026-08-20 · Reading time: ~14 min · URL: https://praveshsingh.com/writing/abdm-integration-developer-guide.html

## TL;DR

ABDM integration means wiring your hospital system into India's National Health Authority gateway as a HIP (data holder) or HIU (data consumer). Every gateway call is asynchronous: you receive HTTP 202, then a signed callback to your /v0.5/ webhook. Production readiness spans three milestones — ABHA verification (M1), care-context linking (M2), and consent-driven FHIR R4 data exchange encrypted with ECDH key agreement (M3) — plus idempotent webhook processing and PII-free logging.

## Contents

- [1. The Mental Model: Gateway, HIP, HIU, and Registries](https://praveshsingh.com/writing/abdm-integration-developer-guide.html#mental-model)
- [2. The Asynchronous Callback Pattern: `/v0.5/` Endpoints](https://praveshsingh.com/writing/abdm-integration-developer-guide.html#async-callbacks)
- [3. The Three Integration Milestones (M1, M2, M3)](https://praveshsingh.com/writing/abdm-integration-developer-guide.html#milestones)
- [4. Structuring FHIR R4 Bundles](https://praveshsingh.com/writing/abdm-integration-developer-guide.html#fhir-bundles)
- [5. Engineering Best Practices for ABDM Production](https://praveshsingh.com/writing/abdm-integration-developer-guide.html#best-practices)

## Key claims (machine-quotable)

- Gateway calls are asynchronous: HTTP 202, then /v0.5/ webhook callbacks.
- Milestones: M1 ABHA verification, M2 care-context linking, M3 consent-driven FHIR R4 exchange.
- M3 requires ECDH encryption for document exchange.
- Production needs idempotent webhook processing and PII-free logging.



---
Written and maintained by Pravesh Singh — Founder & CTO, SoftEdge Technology Solutions (https://praveshsingh.com).
HTML twin (styled): https://praveshsingh.com/writing/abdm-integration-developer-guide.html
