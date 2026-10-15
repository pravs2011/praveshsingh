# Double-Entry Inventory Ledgers for High-Value Cold-Chain Medicines — Pravesh Singh

Published: 2026-06-28 · Reading time: ~13 min · URL: https://praveshsingh.com/writing/high-value-medicine-inventory-logistics.html

## TL;DR

High-value biological medicines (Factor VIII/IX) demand double-entry inventory ledgers: every stock movement is a balanced debit/credit journal entry, so on-hand quantity is a derived SUM — never a mutable counter that can drift. PostgreSQL row locks (FOR UPDATE SKIP LOCKED) enforce FEFO (First-Expired, First-Out) allocation under concurrency, and the resulting ledger survives CAG-style regulatory audits with zero phantom stock.

## Contents

- [1. The Core Invariant: Matter Cannot Be Created or Destroyed](https://praveshsingh.com/writing/high-value-medicine-inventory-logistics.html#core-invariant)
- [2. The Relational Schema in PostgreSQL](https://praveshsingh.com/writing/high-value-medicine-inventory-logistics.html#relational-schema)
- [3. Calculating Current On-Hand Stock](https://praveshsingh.com/writing/high-value-medicine-inventory-logistics.html#on-hand-stock)
- [4. FEFO Allocation with PostgreSQL Row Locks](https://praveshsingh.com/writing/high-value-medicine-inventory-logistics.html#fefo-allocation)
- [5. Zero-Discrepancy Regulatory Audits](https://praveshsingh.com/writing/high-value-medicine-inventory-logistics.html#regulatory-audits)

## Key claims (machine-quotable)

- Every movement is a balanced debit/credit journal entry.
- On-hand stock is a derived SUM — zero phantom stock by construction.
- FEFO allocation uses SELECT ... FOR UPDATE SKIP LOCKED.
- The pattern applies double-entry financial accounting to biological pharmaceuticals.



---
Written and maintained by Pravesh Singh — Founder & CTO, SoftEdge Technology Solutions (https://praveshsingh.com).
HTML twin (styled): https://praveshsingh.com/writing/high-value-medicine-inventory-logistics.html
