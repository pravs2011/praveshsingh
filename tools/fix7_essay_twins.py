#!/usr/bin/env python3
"""FIX-7: generate a markdown twin (writing/<slug>.md) for every essay HTML.

Idempotent: safe to re-run; overwrites twins from current HTML every time.
Run from repo root: python3 tools/fix7_essay_twins.py
"""
import html as html_mod
import re
from pathlib import Path

SLUGS = [
    "offline-tolerant-hospital-software",
    "abdm-integration-developer-guide",
    "multi-tenant-postgresql-isolation",
    "high-value-medicine-inventory-logistics",
    "structured-data-extraction-llm-limits",
    "dpdp-act-2023-health-tech-checklist",
]

# Key claims mirrored in order from llms-full.txt §8b (kept in one place so twins stay stable)
KEY_CLAIMS = {
    "offline-tolerant-hospital-software": [
        "Local SQLite/IndexedDB write paths must commit in under 15ms.",
        "Reconnection floods are absorbed by batch sync transactions with idempotency keys and server cursors.",
        "Clinical events are immutable; demographics converge via column-level CRDTs.",
        "Inventory is a double-entry ledger, not a mutable stock column.",
    ],
    "abdm-integration-developer-guide": [
        "Gateway calls are asynchronous: HTTP 202, then /v0.5/ webhook callbacks.",
        "Milestones: M1 ABHA verification, M2 care-context linking, M3 consent-driven FHIR R4 exchange.",
        "M3 requires ECDH encryption for document exchange.",
        "Production needs idempotent webhook processing and PII-free logging.",
    ],
    "multi-tenant-postgresql-isolation": [
        "Shared-schema Row-Level Security beats schema-per-tenant at scale (single migrations, PgBouncer transaction-pool friendly).",
        "Schema-per-tenant fits fewer than ~100 high-compliance enterprise tenants.",
        "Composite indexes leading with tenant_id keep RLS fast.",
        "Connection pooling strategy differs fundamentally between the two models.",
    ],
    "high-value-medicine-inventory-logistics": [
        "Every movement is a balanced debit/credit journal entry.",
        "On-hand stock is a derived SUM \u2014 zero phantom stock by construction.",
        "FEFO allocation uses SELECT ... FOR UPDATE SKIP LOCKED.",
        "The pattern applies double-entry financial accounting to biological pharmaceuticals.",
    ],
    "structured-data-extraction-llm-limits": [
        "Four failure modes of naive prompting: schema drift, hallucinated fields, silent arithmetic errors, unverifiable provenance.",
        "Production stack: schema-constrained decoding + Pydantic invariants + delta-retry + bounding-box anchoring.",
        "Measured result: >99.4% field-level precision.",
    ],
    "dpdp-act-2023-health-tech-checklist": [
        "Right to Erasure vs statutory medical retention is resolved architecturally, not contractually.",
        "Components: consent-manager state machines, purpose-limitation schemas.",
        "Cryptographic scrubbing of identifiers while retaining clinical fact.",
        "Immutable audit logs close the compliance loop.",
    ],
}

TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")

def strip(s: str) -> str:
    return WS.sub(" ", html_mod.unescape(TAG.sub(" ", s))).strip()

def twin_for(slug: str) -> Path:
    src = Path("writing") / f"{slug}.html"
    s = src.read_text()
    title_full = re.search(r"<title>(.*?)</title>", s, re.S).group(1)
    title = re.sub(r"\s*[–-]\s*Pravesh Singh$", "", title_full).strip()
    date = (re.search(r'published_time" content="([^"]+)"', s) or [None, ""])[1][:10]
    body_only = re.sub(r"<(!DOCTYPE.*?)|<script.*?</script>", "", s, flags=re.S)
    n = len(re.sub(r"<style.*?</style>", "", body_only, flags=re.S))
    words = len(strip(body_only).split())
    read_min = max(2, round(words / 200))

    # TL;DR: the paragraph inside .tldr
    t = ""
    m = re.search(r'class="tldr".*?<p[^>]*>(.*?)</p>', s, re.S)
    if m:
        t = strip(m.group(1))

    # TOC from anchored H2s
    h2s = re.findall(r'<h2[^>]*id="([^"]+)"[^>]*>(.*?)</h2>', s, re.S)
    toc = "\n".join(f"- [{strip(t_)}](https://praveshsingh.com/writing/{slug}.html#{i})"
                    for i, t_ in h2s)

    # Related essays (from the Related reading block)
    rel_urls = sorted(set(re.findall(r'href="https://praveshsingh\.com/writing/((?!' + slug + r")[a-z-]+)\.html\"", s)))
    related = "\n".join(f"- [{u.replace('-', ' ').title()}](https://praveshsingh.com/writing/{u}.html)"
                        for u in rel_urls) or "_(series start — no siblings yet)_"

    claims = "\n".join(f"- {c}" for c in KEY_CLAIMS.get(slug, []))

    md = f"""# {title} — Pravesh Singh

Published: {date} · Reading time: ~{read_min} min · URL: https://praveshsingh.com/writing/{slug}.html

## TL;DR

{t}

## Contents

{toc}

## Key claims (machine-quotable)

{claims}

{("## Related reading\n\n" + related) if rel_urls else ""}

---
Written and maintained by Pravesh Singh — Founder & CTO, SoftEdge Technology Solutions (https://praveshsingh.com).
HTML twin (styled): https://praveshsingh.com/writing/{slug}.html
"""
    out = Path("writing") / f"{slug}.md"
    out.write_text(md)
    return out

written = [str(twin_for(s)) for s in SLUGS]
print("generated:", *written, sep="\n  ")
