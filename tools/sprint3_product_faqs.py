#!/usr/bin/env python3
"""Sprint 3: visible FAQ sections + FAQPage JSON-LD on product pages.

AEO value: FAQ blocks are the highest extractable-passage format for
Perplexity/ChatGPT/Copilot citations (audit §3.4, §7.2). Each page gets a
visible accordion-free FAQ list (always in DOM) + mirrored FAQPage schema
referencing the page's existing @graph via @id.

Run from repo root:  python3 tools/sprint3_product_faqs.py
"""
import json
import re
import sys

FAQ_CSS = """
    /* FAQ (AEO extractable answers) */
    .faq-section { padding: 72px 0; border-top: 1px solid var(--border); }
    .faq-head { max-width: 760px; margin-bottom: 36px; }
    .faq-eyebrow {
      font-size: 0.78rem; font-weight: 700; text-transform: uppercase;
      letter-spacing: 0.12em; color: #818cf8; margin-bottom: 10px;
    }
    .faq-title {
      font-size: clamp(1.7rem, 3vw, 2.3rem); font-weight: 800;
      color: #ffffff; letter-spacing: -0.02em; margin-bottom: 12px; line-height: 1.25;
    }
    .faq-list { max-width: 820px; display: flex; flex-direction: column; gap: 14px; }
    .faq-item {
      background: var(--bg-surface, #10141d);
      border: 1px solid var(--border, rgba(255,255,255,0.08));
      border-radius: 12px; padding: 22px 26px;
    }
    .faq-q { font-size: 1.02rem; font-weight: 700; color: #ffffff; margin-bottom: 8px; }
    .faq-a { font-size: 0.94rem; color: var(--text-muted, #9aa3b5); line-height: 1.7; margin: 0; }
"""

FAQS = {
    "icare.html": {
        "page_name": "iCare Healthcare Platform",
        "faqs": [
            (
                "What is iCare and who built it?",
                "iCare is a mission-critical digital healthcare platform designed and built by Pravesh Singh, Founder & CTO of SoftEdge Technology Solutions. It manages electronic patient registries and cold-chain medicine inventory for hemophilia and thalassemia care across state hospital networks in Punjab and Madhya Pradesh.",
            ),
            (
                "Which hospitals use iCare?",
                "iCare is deployed across state hospital networks and day-care centres in Punjab (with NHM Punjab and PSACS) and Madhya Pradesh. Patients registered at one district hospital can receive verified care and factor concentrate at any connected centre statewide.",
            ),
            (
                "How does iCare prevent medicine stock-outs?",
                "The platform tracks every vial by batch number and expiry date in a double-entry inventory ledger, computes real-time cold-chain stock levels, and coordinates inter-hospital stock transfers using nearest-expiry (FEFO) allocation before local stock-outs occur.",
            ),
            (
                "Is iCare ABDM and FHIR compatible?",
                "Yes. iCare's architecture is aligned with Ayushman Bharat Digital Mission (ABDM) guidelines, supports HL7 FHIR R4 document bundles, and includes role-based access control, encrypted storage, and immutable audit logs.",
            ),
            (
                "Can iCare be deployed in a new state or hospital network?",
                "Yes. Deployments are executed by SoftEdge Technology Solutions with a phased rollout: registry migration, staff training, offline-tolerant terminal setup, and state health commissioner analytics dashboards. Inquiries: hello@praveshsingh.com.",
            ),
        ],
    },
    "taskedge.html": {
        "page_name": "TaskEdge",
        "faqs": [
            (
                "What is TaskEdge?",
                "TaskEdge is an AI-powered business operating system and multi-tenant operations SaaS built by Pravesh Singh. It coordinates daily execution, recurring workflows, proposals, invoicing, and expenses for growing teams and enterprises.",
            ),
            (
                "Who is TaskEdge built for?",
                "TaskEdge targets deskless and shift-based teams — operations supervisors, field crews, and growing businesses that need structured shift handovers and task accountability without heavyweight enterprise overhead or lengthy training.",
            ),
            (
                "How does TaskEdge isolate each tenant's data?",
                "TaskEdge uses true multi-tenant isolation at both the application and database layers, following the shared-schema Row-Level Security (RLS) patterns described in Pravesh's PostgreSQL multi-tenancy essay, with granular audit trails and role-based permissions.",
            ),
            (
                "How fast is TaskEdge?",
                "TaskEdge delivers sub-50ms task updates with predictable database queries, keeping the interface responsive for shift workers under real operational load.",
            ),
            (
                "How can we try or buy TaskEdge?",
                "Request a demo via hello@praveshsingh.com or through the contact section. Platform builds and SLA-backed support are contracted through SoftEdge Technology Solutions.",
            ),
        ],
    },
    "automation.html": {
        "page_name": "Applied AI & Automation",
        "faqs": [
            (
                "What kinds of AI systems do you build?",
                "Production-grade applied AI: multimodal document extraction from scanned clinical and administrative records, domain-grounded Retrieval-Augmented Generation (RAG) assistants over verified manuals, automated regulatory report generation, and AI agents with deterministic validation.",
            ),
            (
                "How accurate is your document extraction?",
                "Pipelines use schema-constrained LLM decoding, Pydantic invariant validation, mathematical checks on extracted line items, and targeted delta-retry loops — achieving over 99.4% field-level precision on invoices and clinical documents.",
            ),
            (
                "How do you prevent LLM hallucinations in production?",
                "Free-form prompting is replaced with schema-constrained generation and deterministic validation: every extracted record must satisfy JSON Schema types, arithmetic invariants, and bounding-box citation anchoring before it reaches downstream systems. Human-in-the-loop queues handle the residual exceptions.",
            ),
            (
                "Can AI models run on-premise for data privacy?",
                "Yes. Local and hybrid model deployments keep sensitive clinical and financial documents inside your infrastructure, with the same deterministic validation pipeline applied regardless of where inference runs.",
            ),
            (
                "What does an AI integration sprint involve?",
                "A fixed-scope sprint typically covers document inventory and schema design, pipeline construction, validation harnesses, and a human-review exception queue — delivered production-ready with handover documentation. Scope via hello@praveshsingh.com.",
            ),
        ],
    },
}


def faq_html(faqs):
    items = "\n".join(
        f'          <div class="faq-item">\n'
        f'            <h3 class="faq-q">{q}</h3>\n'
        f"            <p class=\"faq-a\">{a}</p>\n"
        f"          </div>"
        for q, a in faqs
    )
    return (
        '    <!-- =========================================================\n'
        '         FAQ (AEO: extractable answers for search & AI engines)\n'
        '         ========================================================= -->\n'
        '    <section class="faq-section" id="faq" aria-labelledby="faq-title">\n'
        '      <div class="container">\n'
        '        <div class="faq-head">\n'
        '          <div class="faq-eyebrow">Direct Answers</div>\n'
        '          <h2 class="faq-title" id="faq-title">Frequently asked questions</h2>\n'
        '        </div>\n'
        '        <div class="faq-list">\n'
        + items + "\n"
        '        </div>\n'
        '      </div>\n'
        '    </section>\n'
    )


def faq_ld(faqs, page_url, page_name):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": page_url + "#faq",
        "name": f"{page_name} — Frequently Asked Questions",
        "inLanguage": "en-IN",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }


def process(path, cfg):
    src = open(path, encoding="utf-8").read()
    orig = src
    notes = []

    # CSS once
    if ".faq-item {" not in src:
        src = src.replace("</style>", FAQ_CSS + "  </style>", 1)
        notes.append("FAQ CSS added")

    # Visible FAQ section before </main>
    if 'id="faq"' not in src:
        block = faq_html(cfg["faqs"])
        src = src.replace("  </main>", block + "  </main>", 1)
        notes.append("visible FAQ section added")

    # FAQPage JSON-LD as separate script (mirrors visible HTML)
    if '"@type": "FAQPage"' not in src:
        url = "https://praveshsingh.com/" + path
        ld = faq_ld(cfg["faqs"], url, cfg["page_name"])
        script = (
            '\n  <script type="application/ld+json">\n'
            + json.dumps(ld, indent=2, ensure_ascii=False)
            + "\n  </script>\n"
        )
        src = src.replace("</head>", script + "</head>", 1)
        notes.append("FAQPage JSON-LD added")

    if src != orig:
        open(path, "w", encoding="utf-8").write(src)
    return notes


def main():
    for path, cfg in FAQS.items():
        notes = process(path, cfg)
        print(f"✓ {path}")
        for n in notes:
            print(f"    - {n}")


if __name__ == "__main__":
    sys.exit(main())
