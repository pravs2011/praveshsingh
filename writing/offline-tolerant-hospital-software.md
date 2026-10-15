# Architecting Offline-Tolerant Software for Indian District Hospitals — Pravesh Singh

Published: 2026-09-15 · Reading time: ~14 min · URL: https://praveshsingh.com/writing/offline-tolerant-hospital-software.html

## TL;DR

Offline-tolerant hospital software treats the device's local SQLite or IndexedDB store as the primary write path, committing every clinical action in under 15 milliseconds and syncing asynchronously. Conflicts are resolved per domain — immutable append-only clinical events, column-level CRDTs for demographics, and double-entry ledgers for inventory — while batch sync transactions with idempotency keys and server cursors absorb reconnection floods after network blackouts at Indian district hospital counters.

## Contents

- [1. Local-First Write Path: Never Block the UI](https://praveshsingh.com/writing/offline-tolerant-hospital-software.html#local-first-write-path)
- [2. Conflict Resolution: Domain-Specific Merging vs Last-Write-Wins](https://praveshsingh.com/writing/offline-tolerant-hospital-software.html#conflict-resolution)
- [3. Handling High-Latency Reconnection Floods](https://praveshsingh.com/writing/offline-tolerant-hospital-software.html#reconnection-floods)
- [4. Storage Hygiene & Local Encryption](https://praveshsingh.com/writing/offline-tolerant-hospital-software.html#storage-encryption)
- [Conclusion: Engineering for Reality](https://praveshsingh.com/writing/offline-tolerant-hospital-software.html#conclusion)

## Key claims (machine-quotable)

- Local SQLite/IndexedDB write paths must commit in under 15ms.
- Reconnection floods are absorbed by batch sync transactions with idempotency keys and server cursors.
- Clinical events are immutable; demographics converge via column-level CRDTs.
- Inventory is a double-entry ledger, not a mutable stock column.



---
Written and maintained by Pravesh Singh — Founder & CTO, SoftEdge Technology Solutions (https://praveshsingh.com).
HTML twin (styled): https://praveshsingh.com/writing/offline-tolerant-hospital-software.html
