#!/usr/bin/env python3
"""Sprint 2: GEO surfaces for all 6 essays.

Per essay (audit §4.1–4.4):
  1. TL;DR callout (60–80 self-contained, quotable words) under the meta line
  2. "On this page" TOC — adds id= anchors to every H2
  3. "References" section with primary-source outbound citations
  4. "Related reading" cross-links to sibling essays
  5. Shared CSS for all four blocks
  6. article:modified_time meta

Run from repo root:  python3 tools/sprint2_geo_essays.py
"""
import re
import sys

TLDR_CSS = """
    /* GEO blocks: TL;DR, TOC, References, Related reading */
    .tldr {
      background: rgba(99, 102, 241, 0.08);
      border: 1px solid rgba(99, 102, 241, 0.3);
      border-left: 4px solid var(--primary);
      border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
      padding: 20px 24px;
      margin: 0 0 36px;
    }
    .tldr-title {
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: #818cf8;
      margin-bottom: 8px;
    }
    .tldr p { margin-bottom: 0; color: #e2e8f0; }
    .toc {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 18px 24px;
      margin: 0 0 44px;
      font-size: 0.92rem;
    }
    .toc-title {
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--text-sub);
      margin-bottom: 10px;
    }
    .toc ol { margin: 0 0 0 18px; display: flex; flex-direction: column; gap: 6px; }
    .toc a { color: var(--text-muted); }
    .toc a:hover { color: #ffffff; }
    .refs {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 22px 26px;
      margin: 48px 0 0;
      font-size: 0.9rem;
    }
    .refs-title {
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--text-sub);
      margin-bottom: 12px;
    }
    .refs ol { margin: 0 0 0 18px; display: flex; flex-direction: column; gap: 8px; }
    .refs li { color: var(--text-muted); }
    .refs a { color: #93c5fd; text-decoration: underline; text-decoration-color: rgba(147, 197, 253, 0.35); }
    .refs a:hover { color: #bfdbfe; }
    .related {
      margin: 56px 0 0;
      padding-top: 28px;
      border-top: 1px solid var(--border);
    }
    .related-title {
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--teal);
      margin-bottom: 14px;
    }
    .related-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .related-grid a {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 14px 18px;
      font-size: 0.9rem;
      color: var(--text-muted);
      line-height: 1.45;
    }
    .related-grid a:hover { border-color: var(--border-hover); color: #ffffff; }
    .related-grid a span { display: block; font-size: 0.75rem; color: var(--text-sub); margin-top: 4px; }
    @media (max-width: 720px) { .related-grid { grid-template-columns: 1fr; } }
"""

ESSAYS = {
    "writing/offline-tolerant-hospital-software.html": {
        "anchor_map": [
            ("1. Local-First Write Path: Never Block the UI", "local-first-write-path"),
            ("2. Conflict Resolution: Domain-Specific Merging vs Last-Write-Wins", "conflict-resolution"),
            ("3. Handling High-Latency Reconnection Floods", "reconnection-floods"),
            ("4. Storage Hygiene &amp; Local Encryption", "storage-encryption"),
            ("Conclusion: Engineering for Reality", "conclusion"),
        ],
        "tldr": (
            "Offline-tolerant hospital software treats the device's local SQLite or IndexedDB store "
            "as the primary write path, committing every clinical action in under 15 milliseconds and "
            "syncing asynchronously. Conflicts are resolved per domain — immutable append-only clinical "
            "events, column-level CRDTs for demographics, and double-entry ledgers for inventory — while "
            "batch sync transactions with idempotency keys and server cursors absorb reconnection floods "
            "after network blackouts at Indian district hospital counters."
        ),
        "refs": [
            ("PostgreSQL Docs — Logical Replication & bulk loading patterns", "https://www.postgresql.org/docs/current/populate.html"),
            ("SQLite — Application as platform-of-record (local persistence)", "https://www.sqlite.org/appfileformat.html"),
            ("MDN — IndexedDB API (browser-side durable storage)", "https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API"),
            ("W3C — CRDT conflict resolution for offline-first web apps (research overview)", "https://www.w3.org/TR/webdatabase/"),
        ],
        "related": [
            ("writing/multi-tenant-postgresql-isolation.html", "Multi-Tenant Database Isolation in PostgreSQL", "Schemas vs RLS — pooling, migrations, isolation"),
            ("writing/high-value-medicine-inventory-logistics.html", "Double-Entry Ledgers for Cold-Chain Medicines", "Immutable inventory accounting with FEFO locking"),
            ("writing/abdm-integration-developer-guide.html", "ABDM Integration: A Developer's Field Guide", "ABHA, HIP/HIU callbacks, FHIR R4 bundles"),
        ],
    },
    "writing/abdm-integration-developer-guide.html": {
        "anchor_map": [
            ("1. The Mental Model: Gateway, HIP, HIU, and Registries", "mental-model"),
            ("2. The Asynchronous Callback Pattern: `/v0.5/` Endpoints", "async-callbacks"),
            ("3. The Three Integration Milestones (M1, M2, M3)", "milestones"),
            ("4. Structuring FHIR R4 Bundles", "fhir-bundles"),
            ("5. Engineering Best Practices for ABDM Production", "best-practices"),
        ],
        "tldr": (
            "ABDM integration means wiring your hospital system into India's National Health Authority "
            "gateway as a HIP (data holder) or HIU (data consumer). Every gateway call is asynchronous: "
            "you receive HTTP 202, then a signed callback to your /v0.5/ webhook. Production readiness "
            "spans three milestones — ABHA verification (M1), care-context linking (M2), and consent-driven "
            "FHIR R4 data exchange encrypted with ECDH key agreement (M3) — plus idempotent webhook "
            "processing and PII-free logging."
        ),
        "refs": [
            ("ABDM Sandbox — official integrator documentation", "https://sandbox.abdm.gov.in/abdm-docs/getting-started"),
            ("NHA — HIP/HIU Guidelines for Health Information Exchange (PDF)", "https://abdm.gov.in/strapicms/uploads/HIP_HIU_Guidelines_f85df336ec.pdf"),
            ("NRCeS — FHIR Implementation Guide for ABDM (NDHM R4 profiles)", "https://nrces.in/ndhm/fhir/r4/5.0.0/index.html"),
            ("HL7 FHIR R4 — Composition & DiagnosticReport resource specs", "https://hl7.org/fhir/R4/composition.html"),
        ],
        "related": [
            ("writing/offline-tolerant-hospital-software.html", "Architecting Offline-Tolerant Hospital Software", "Local-first write paths for unreliable hospital networks"),
            ("writing/dpdp-act-2023-health-tech-checklist.html", "DPDP Act 2023: Engineering Checklist", "Consent state machines, erasure, audit logging"),
            ("writing/structured-data-extraction-llm-limits.html", "Structured Data Extraction with LLMs", "Schema-constrained decoding & validation loops"),
        ],
    },
    "writing/multi-tenant-postgresql-isolation.html": {
        "anchor_map": [
            ("1. The Fundamental Architectural Spectrum", "architectural-spectrum"),
            ("2. The Hidden Trap of Schema-per-Tenant", "schema-per-tenant-trap"),
            ("3. The Modern Solution: Shared-Schema with Row-Level Security (RLS)", "shared-schema-rls"),
            ("4. Indexing &amp; Query Optimization for RLS", "indexing-optimization"),
            ("5. Decision Matrix: When to Pick Which", "decision-matrix"),
        ],
        "tldr": (
            "For B2B SaaS on PostgreSQL, shared-schema Row-Level Security (RLS) scales better than "
            "schema-per-tenant: one migration instead of hundreds, normal connection-pooling behaviour "
            "under PgBouncer transaction mode, and per-row tenant isolation via a session-scoped "
            "tenant_id policy. Schema-per-tenant suits fewer than ~100 high-compliance enterprise "
            "customers. Composite indexes leading with tenant_id keep RLS range scans fast under "
            "noisy-neighbor load."
        ),
        "refs": [
            ("PostgreSQL Docs — Row Security Policies (CREATE POLICY)", "https://www.postgresql.org/docs/current/sql-createpolicy.html"),
            ("PgBouncer — official features & pooling modes", "https://www.pgbouncer.org/features.html"),
            ("PostgreSQL Docs — current_setting & custom GUC options", "https://www.postgresql.org/docs/current/sql-set.html"),
            ("PostgreSQL Docs — Indexes & composite index behavior", "https://www.postgresql.org/docs/current/indexes.html"),
        ],
        "related": [
            ("writing/high-value-medicine-inventory-logistics.html", "Double-Entry Ledgers for Cold-Chain Medicines", "FOR UPDATE SKIP LOCKED allocation inside one tenant"),
            ("writing/offline-tolerant-hospital-software.html", "Architecting Offline-Tolerant Hospital Software", "Sync targets that respect tenant boundaries"),
            ("writing/structured-data-extraction-llm-limits.html", "Structured Data Extraction with LLMs", "Deterministic pipelines feeding validated rows"),
        ],
    },
    "writing/high-value-medicine-inventory-logistics.html": {
        "anchor_map": [
            ("1. The Core Invariant: Matter Cannot Be Created or Destroyed", "core-invariant"),
            ("2. The Relational Schema in PostgreSQL", "relational-schema"),
            ("3. Calculating Current On-Hand Stock", "on-hand-stock"),
            ("4. FEFO Allocation with PostgreSQL Row Locks", "fefo-allocation"),
            ("5. Zero-Discrepancy Regulatory Audits", "regulatory-audits"),
        ],
        "tldr": (
            "High-value biological medicines (Factor VIII/IX) demand double-entry inventory ledgers: "
            "every stock movement is a balanced debit/credit journal entry, so on-hand quantity is a "
            "derived SUM — never a mutable counter that can drift. PostgreSQL row locks (FOR UPDATE "
            "SKIP LOCKED) enforce FEFO (First-Expired, First-Out) allocation under concurrency, and the "
            "resulting ledger survives CAG-style regulatory audits with zero phantom stock."
        ),
        "refs": [
            ("PostgreSQL Docs — SELECT FOR UPDATE & SKIP LOCKED", "https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE"),
            ("PostgreSQL Docs — Transaction Isolation & serializable snapshot", "https://www.postgresql.org/docs/current/transaction-iso.html"),
            ("WHO — Good storage and distribution practices for medical products", "https://www.who.int/publications/i/item/9789240016755"),
            ("Double-entry bookkeeping — materiality of balanced journals (reference)", "https://en.wikipedia.org/wiki/Double-entry_bookkeeping"),
        ],
        "related": [
            ("writing/offline-tolerant-hospital-software.html", "Architecting Offline-Tolerant Hospital Software", "Where the dispensing events come from at the counter"),
            ("writing/multi-tenant-postgresql-isolation.html", "Multi-Tenant Database Isolation in PostgreSQL", "Isolation patterns when multiple hospitals share the platform"),
            ("writing/abdm-integration-developer-guide.html", "ABDM Integration: A Developer's Field Guide", "Linking care contexts to ABHA records"),
        ],
    },
    "writing/structured-data-extraction-llm-limits.html": {
        "anchor_map": [
            ("1. The Four Flaws of Naive Prompt Engineering", "four-flaws"),
            ("2. The Architecture: Constrained Decoding & Multi-Pass Validation", "constrained-architecture"),
            ("3. Enforcing Strict Types with Pydantic & Instructor", "pydantic-instructor"),
            ("4. The Targeted Delta Correction Loop", "delta-correction"),
            ("5. Human-in-the-Loop with Spatial Grounding", "spatial-grounding"),
        ],
        "tldr": (
            "Naive prompt engineering fails enterprise document extraction on four axes: schema drift, "
            "hallucinated fields, silent arithmetic errors, and unverifiable provenance. The production "
            "architecture replaces free prompting with schema-constrained decoding, Pydantic invariant "
            "validation, a targeted delta-retry loop that resends only failing fields, and bounding-box "
            "citation anchoring so every extracted token is spatially verifiable — achieving >99.4% "
            "field-level precision on invoices and clinical records."
        ),
        "refs": [
            ("Pydantic — data validation using Python type annotations", "https://docs.pydantic.dev/latest/"),
            ("Instructor — structured LLM outputs with retries", "https://python.useinstructor.com/"),
            ("OpenAI — Structured Outputs (JSON Schema constrained decoding)", "https://platform.openai.com/docs/guides/structured-outputs"),
            ("JSON Schema — official specification", "https://json-schema.org/specification"),
        ],
        "related": [
            ("writing/high-value-medicine-inventory-logistics.html", "Double-Entry Ledgers for Cold-Chain Medicines", "Where extracted invoice line items must balance"),
            ("writing/abdm-integration-developer-guide.html", "ABDM Integration: A Developer's Field Guide", "FHIR JSON as another schema-constrained target"),
            ("writing/multi-tenant-postgresql-isolation.html", "Multi-Tenant Database Isolation in PostgreSQL", "Storing validated records per tenant safely"),
        ],
    },
    "writing/dpdp-act-2023-health-tech-checklist.html": {
        "anchor_map": [
            ("1. The Fundamental Paradox: Right to Erasure vs Statutory Medical Retention", "erasure-paradox"),
            ("2. The Actionable 10-Point Technical Architecture Checklist", "checklist"),
            ("3. Sample Consent Ledger Schema (PostgreSQL)", "consent-ledger"),
            ("4. Conclusion: Compliance as a Competitive Advantage", "conclusion"),
        ],
        "tldr": (
            "The DPDP Act 2023 grants Indian patients a Right to Erasure while medical statutes mandate "
            "record retention — a paradox health platforms must resolve architecturally. The 10-point "
            "checklist covers consent-manager state machines, purpose-limitation schemas, cryptographic "
            "scrubbing of identifiers while retaining clinical fact, data-fiduciary access controls, and "
            "immutable audit logs, treating compliance as an engineering property rather than legal "
            "afterthought."
        ),
        "refs": [
            ("MeitY — The Digital Personal Data Protection Act, 2023 (official PDF)", "https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf"),
            ("MeitY — DPDP Act 2023 landing page & rules", "https://www.meity.gov.in/content/digital-personal-data-protection-act-2023"),
            ("Digital Personal Data Protection Rules, 2025 (notified)", "https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa"),
            ("PostgreSQL Docs — GRANT / REVERT & row security for fiduciary access", "https://www.postgresql.org/docs/current/sql-grant.html"),
        ],
        "related": [
            ("writing/abdm-integration-developer-guide.html", "ABDM Integration: A Developer's Field Guide", "Consent artifacts and ABHA-linked data flows"),
            ("writing/multi-tenant-postgresql-isolation.html", "Multi-Tenant Database Isolation in PostgreSQL", "RLS policies as data-fiduciary boundaries"),
            ("writing/offline-tolerant-hospital-software.html", "Architecting Offline-Tolerant Hospital Software", "Local device caching under erasure obligations"),
        ],
    },
}

# JSON-LD publisher logo + Article image per essay
ORG_LOGO = '''"publisher": {
          "@type": "Organization",
          "name": "SoftEdge Technology Solutions",
          "url": "https://softedgetechology.com/",
          "logo": {
            "@type": "ImageObject",
            "url": "https://praveshsingh.com/images/logo.png",
            "width": 512,
            "height": 512
          }
        }'''

def add_anchors(body, anchor_map):
    for title, slug in anchor_map:
        escaped = re.escape(title)
        # match <h2>title</h2> exactly once
        pattern = re.compile(r"<h2>(" + escaped + r")</h2>")
        body = pattern.sub(r'<h2 id="' + slug + r'">\1</h2>', body)
    return body

def build_toc(anchor_map):
    items = "\n".join(
        f'            <li><a href="#{slug}">{title}</a></li>'
        for title, slug in anchor_map
    )
    return (
        '          <nav class="toc" aria-label="On this page">\n'
        '            <div class="toc-title">On this page</div>\n'
        "            <ol>\n" + items + "\n            </ol>\n"
        "          </nav>"
    )

def build_refs(refs):
    items = "\n".join(
        f'            <li><a href="{url}" target="_blank" rel="noopener">{name}</a></li>'
        for name, url in refs
    )
    return (
        '          <div class="refs">\n'
        '            <div class="refs-title">References — primary sources</div>\n'
        "            <ol>\n" + items + "\n            </ol>\n"
        "          </div>"
    )

def build_related(related):
    items = "\n".join(
        f'            <a href="{href}">{title}<span>{desc}</span></a>'
        for href, title, desc in related
    )
    return (
        '          <div class="related">\n'
        '            <div class="related-title">Related reading</div>\n'
        '            <div class="related-grid">\n' + items + "\n            </div>\n"
        "          </div>"
    )

def process(path, cfg):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    orig = src
    notes = []

    # 1. CSS injection (once)
    if ".tldr {" not in src:
        src = src.replace("    .author-card {", TLDR_CSS + "\n    .author-card {", 1)
        notes.append("CSS added")

    # 2. TL;DR + TOC right after article-content opening div
    content_marker = '<div class="article-content">'
    if content_marker in src and 'class="tldr"' not in src:
        block = content_marker + "\n" + \
            '          <div class="tldr">\n' \
            '            <div class="tldr-title">TL;DR</div>\n' \
            f"            <p>{cfg['tldr']}</p>\n" \
            "          </div>\n\n" + \
            build_toc(cfg["anchor_map"])
        src = src.replace(content_marker, block, 1)
        notes.append("TL;DR + TOC injected")

    # 3. Heading anchors
    before = src
    src = add_anchors(src, cfg["anchor_map"])
    if src != before:
        notes.append("H2 anchors added")

    # 4. References + Related reading before author-card
    author_marker = '        <div class="author-card">'
    if author_marker in src and 'class="refs"' not in src:
        block = build_refs(cfg["refs"]) + "\n\n" + build_related(cfg["related"]) + "\n\n" + author_marker
        src = src.replace(author_marker, block, 1)
        notes.append("References + Related reading injected")

    # 5. article:modified_time meta after article:published_time
    if "article:modified_time" not in src:
        m = re.search(r'(<meta property="article:published_time" content="[^"]*">)', src)
        if m:
            src = src.replace(m.group(1), m.group(1) + '\n  <meta property="article:modified_time" content="2026-09-23">', 1)
            notes.append("article:modified_time added")

    # 6. Article image + publisher logo in JSON-LD
    if '"image"' not in src.split("application/ld+json", 1)[-1].split("</script>", 1)[0]:
        slug = path.split("/")[-1].replace(".html", "")
        article_img = f'''<meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <script type="application/ld+json"></script>'''
        # insert image into Article node after description
        src = re.sub(
            r'("description": "[^"]*",\s*\n(\s*)"inLanguage": "en-IN",)',
            lambda m: m.group(1).replace('"inLanguage"', f'"image": {{"@type": "ImageObject", "url": "https://praveshsingh.com/images/og-default.png"}},\n{m.group(2)}"inLanguage"'),
            src,
            count=1,
        )
        notes.append("Article.image added")

    # publisher logo
    if '"logo"' not in src.split("application/ld+json", 1)[-1].split("</script>", 1)[0]:
        src = src.replace(
            '''"publisher": {
          "@type": "Organization",
          "name": "SoftEdge Technology Solutions",
          "url": "https://softedgetechnology.com/"
        }''',
            ORG_LOGO,
        )
        notes.append("publisher.logo added")

    if src != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(src)
    return notes

def main():
    for path, cfg in ESSAYS.items():
        notes = process(path, cfg)
        print(f"✓ {path}")
        for n in notes:
            print(f"    - {n}")

if __name__ == "__main__":
    sys.exit(main())
