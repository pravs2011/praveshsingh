# SEO · AEO · AIO/GEO Keyword & Visibility Playbook — praveshsingh.com

**Goal:** appear when buyers search for a **senior developer / CTO / senior AI development expert / good software company** in the **US, Europe and India** — in Google, Bing, ChatGPT Search, Perplexity, Gemini and Google AI Overviews.
**Date:** 2026-09-24 · **Companion doc:** `IMPROVEMENTS_SEO_AIO_GEO.md` (technical audit, Sprints 1–4 implemented)

---

## 0. Strategy Reality Check (read this first)

You will NOT win head terms like "software development company" or "AI development company" — those SERPs are owned by Clutch, Toptal, Accenture and $50M content budgets. Don't chase them directly.

You CAN own three tiers where a founder-led site beats companies:

| Tier | Query shape | Example | Why you win |
|---|---|---|---|
| **T1 — Brand/entity** | "pravesh singh", "softedge technology solutions", "pravesh singh CTO" | — | Zero competition; must be flawless |
| **T2 — Niche authority** | "ABDM integration consultant", "multi-tenant PostgreSQL RLS architecture", "cold chain pharma inventory software", "hospital software offline tolerant" | — | Few credible sources; you have shipped systems + essays |
| **T3 — Role + qualifier** | "fractional CTO healthcare SaaS", "senior AI developer for healthcare startup", "HIPAA-aware EHR development India" | — | Qualifier ("healthcare", "for startups", "India/EU") removes the giants |

**For AI engines (AEO/GEO), T3 is where deals happen:** Perplexity/ChatGPT answers *"who can build my healthcare SaaS?"* by citing **entities with extractable, corroborated claims** — not homepage keyword density. Every fix below feeds that.

**Honest framing rule:** say **"HIPAA-aware / GDPR-conscious architecture"**, never "HIPAA certified" or "GDPR certified" (you don't hold certifications; LLMs penalize unverifiable claims and it's a legal risk).

---

## 1. Keyword Universe by Region & Intent

Legend: 🎯 target page · ✅ already on site · 🆕 needs adding

### 1.1 UNITED STATES (highest commercial value, thinnest coverage today)

| Keyword / query | Intent | Target | Status |
|---|---|---|---|
| fractional CTO for healthcare startup | Role | expertise.html | 🆕 |
| interim CTO SaaS company | Role | expertise.html | 🆕 |
| healthcare software architect / consultant | Role | expertise.html, icare.html | 🆕 |
| HIPAA-aware application development | Service | industries.html | 🆕 (phrase exists once; needs a dedicated passage + FAQ) |
| HIPAA compliant patient registry software (aware) | Service | icare.html | 🆕 |
| FHIR / HL7 FHIR integration developer | Service | expertise.html, glossary | ✅ partial (glossary) → 🆕 service passage |
| EHR / EMR integration engineer | Service | icare.html | 🆕 |
| AI development services for healthcare | Service | automation.html | 🆕 |
| document intelligence / document processing AI | Service | automation.html | ✅ |
| multi-tenant SaaS architecture consultant | Problem | writing/multi-tenant essay + expertise | ✅ strong |
| PostgreSQL row level security expert | Problem | multi-tenant essay | ✅ strong |
| LLM document extraction company | Service | automation.html | 🆕 |
| startup CTO as a service USA | Role | expertise.html | 🆕 |
| cold chain monitoring software pharma | Problem | icare.html | ✅ partial |
| "software company in India for US clients" | Company | company.html | 🆕 |

### 1.2 EUROPE / UK (almost zero coverage today — biggest new gap)

| Keyword / query | Intent | Target | Status |
|---|---|---|---|
| GDPR-compliant software development | Service | privacy.html is wrong surface → 🆕 section on expertise/company | 🆕 |
| EU AI Act compliance for health AI | Problem | 🆕 essay (see §4) | 🆕 |
| DPDP + GDPR dual compliance India EU | Problem | writing/dpdp essay | 🆕 (link them together) |
| digital health software developer Europe | Service | expertise.html | 🆕 |
| healthtech development company UK / DACH | Company | company.html | 🆕 |
| medical data platform developer | Service | icare.html | 🆕 |
| AI document automation for clinics GDPR | Service | automation.html | 🆕 |
| SaaS development partner Europe timezone overlap | Company | company.html | 🆕 |
| NIS2 / medical software regulatory readiness | Problem | 🆕 essay or glossary | 🆕 |

### 1.3 INDIA (already strongest — protect + sharpen)

| Keyword / query | Intent | Target | Status |
|---|---|---|---|
| ABDM integration developer / M1 M2 M3 sandbox | Problem | writing/abdm essay | ✅ strong |
| ABDM compatible application partner | Service | abdm essay + icare | 🆕 phrase on icare |
| hospital management software Punjab / Chandigarh / Mohali | Local-Company | icare/company | 🆕 city mentions thin (0 on about/expertise) |
| pharma cold chain / medicine inventory software India | Problem | icare.html | ✅ |
| hemophilia / thalassemia patient registry software | Niche | icare.html | ✅ unique — you may be the only source |
| fractional CTO India / CTO for hire startup India | Role | expertise.html | 🆕 |
| AI automation company Mohali / Chandigarh | Local-Company | automation.html | 🆕 |
| government health tech vendor NHM / state pipelines | Company | about/speaking | ✅ partial |
| DPDP Act compliance checklist app | Problem | dpdp essay | ✅ strong |

### 1.4 ROLE KEYWORDS (region-neutral — your "senior developer / CTO" ask)

Senior AI developer · senior software engineer consultant · experienced software architect · CTO-level technical advisor · technical due diligence expert (investor DD — new angle, high value) · AI strategist for enterprises · healthtech CTO · SaaS technical co-founder (for hire) · enterprise AI consultant · applied AI engineer.
→ Home: `jobTitle` ✅ has 4 roles. **Missing entirely:** "Fractional CTO", "Technical Advisor", "AI Consultant" — add to `jobTitle` array + about/expertise prose (§3.2).

---

## 2. Page-by-Page On-Page Mapping (exact edits)

| Page | Title (suggested) | Add to H1/H2s/first 100 words |
|---|---|---|
| index.html | keep brand title; description append "…for clients in India, the US and Europe" | one line in hero: "Partnering with funded startups and enterprises across India, the US, UK and EU" |
| expertise.html | "Fractional CTO & Technical Advisory — Healthcare, SaaS & AI \| Pravesh Singh" | H2 "Fractional CTO & advisory engagements"; engagement models section gets "CTO-as-a-service", "interim CTO", "technical due diligence" |
| about.html | "About Pravesh Singh — Fractional CTO & Healthcare Software Architect in Mohali, India" | city/region sentence (currently **0** mentions of Mohali/Chandigarh — add 1–2, natural) |
| icare.html | append "\| HIPAA-aware, ABDM-ready" | compliance-awareness passage + one FAQ: "Is iCare ABDM-compatible and suitable for HIPAA-style deployments?" |
| automation.html | "AI Document Automation & LLM Extraction Services" | "AI development services", "LLM-powered document processing for healthcare, pharma and fintech" |
| industries.html | add "for Healthcare, Pharma & FinTech" | per-industry blocks gain 1 line each: US (HIPAA-aware), EU (GDPR-conscious), IN (ABDM/DPDP) compliance posture |
| company.html | strongest company-intent page — add "software development company for healthcare & SaaS" phrase to H1 area + "clients in India, US, UK/EU" | 🆕 |
| writing/ hub | — | hub H1 add "practical guides on ABDM, multi-tenant SaaS, DPDP/GDPR and applied AI" |

**Global title-pattern rule:** `Primary Keyword — Entity | Pravesh Singh`. Never exceed ~60 chars.

---

## 3. Structured Data & Entity Fixes (gates for AI visibility)

1. **`areaServed` 🆕 on Person + Organization** (index.html `@graph`): `[{"@type":"Country","name":"India"},{"@type":"Country","name":"United States"},{"@type":"Country","name":"United Kingdom"},{"@type":"Country","name":"Germany"},{"@type":"Country","name":"European Union"}]` — this is *the* signal telling AI engines you serve US/EU buyers.
2. **`jobTitle` array:** add `"Fractional CTO"`, `"Technical Advisor"`, `"AI Consultant"`.
3. **`knowsAbout`:** add `"HIPAA-compliant software architecture"`, `"HL7 FHIR interoperability"`, `"GDPR and DPDP data protection engineering"`, `"EU AI Act readiness"`, `"LLM document extraction"`, `"Cold chain pharmaceutical logistics"`.
4. **`Service` nodes with `serviceType` strings** matching §1 keywords on expertise/automation/company (expertise already has OfferCatalog — rename `serviceType` values to the keyword phrases above).
5. **`sameAs` expansion 🆕 (highest-leverage entity fix):** GitHub (create + pin iCare/TaskEdge case-study repos or code samples), Google Developer profile / StackExchange, Crunchbase (SoftEdge), conference/event pages that list you, LinkedIn **company page** for SoftEdge. Every resolvable edge = stronger Knowledge Panel + LLM entity merge.
6. **Third-party corroboration 🆕 (the #1 gap overall):** all 4 talks and both products are **self-attested only**. LLMs cross-check. Get: 1 news mention (Punjab/TechCircle-type), Clutch/GoodFirms vendor profile for SoftEdge, 1 podcast/guest-post byline. Even 3 external sources mentioning "Pravesh Singh, CTO of SoftEdge" measurably changes AI answers.
7. Add `alumniOf`/`hasCredential` if any exist; keep email ✅.

---

## 4. Content Gaps — new assets that capture commercial queries

Ordered by ROI:

1. **Essay: "Shipping HIPAA-aware, GDPR-conscious and DPDP-ready health software: one architecture, three regimes"** — captures US+EU+IN compliance queries simultaneously; you already have the DPDP essay to interlink. (🆕, biggest single content win)
2. **Expertise.html: "Fractional CTO for healthcare & SaaS startups"** section — 300 words + 3 FAQ pairs ("What does a fractional CTO cost in India?", "Fractional vs interim CTO: which do I need?", "When should a funded startup hire a CTO-as-a-service?").
3. **Essay: "EU AI Act readiness for health-AI products"** (risk-class checklist format like your DPDP piece).
4. **Comparison table at top of multi-tenant essay** ("Schema-per-tenant vs RLS: decision table") — comparison queries dominate AI Overview citations.
5. **Glossary additions (definitional = #1 AEO citation format):** "What is FEFO in pharma logistics?", "ABDM M1 vs M2 vs M3", "What is a patient registry?", "RLS vs schema-per-tenant", "HIPAA vs GDPR in one table".
6. **Pricing anchor** on expertise (even "fixed-scope sprints from ₹X / $X" in FAQ + `Offer.priceSpecification`) — engines cannot cite you for "how much does…?" without a public number.
7. **One verified stats block per product page** (patients served, vials/month, uptime) — unique numbers = you become the only citable source.

---

## 5. AEO — Query-Shaped FAQ Bank (add as visible HTML + FAQPage JSON-LD)

Highest-probability buyer prompts (map: 2–3 per page, exact phrasing in `<h3>`):

- "Who is a trusted fractional CTO for healthcare startups in India?"
- "How much does it cost to hire a CTO for a funded startup?"
- "Can I hire a software development company in India that understands HIPAA?"
- "How do I make my hospital app ABDM compliant?" ✅ (covered by essay)
- "Which is better: schema-per-tenant or row-level security?" (add table)
- "How do I extract structured data from insurance documents with AI?" (automation)
- "What is the best way to build a multi-tenant SaaS on PostgreSQL?" ✅
- "Is Pravesh Singh available for US/European clients?" ← add literally, answer with timezones (IST + 4–6h overlap with CET/US-East mornings)
- "What happened at [event]? / Who spoke at NHM Punjab workshop?" (speaking page)
- "iCare vs a generic EMR — what's different?" (icare FAQ)

---

## 6. GEO / AIO — extractability rules (apply to every new/edited page)

- TL;DR callout ≤80 words under every H1 ✅ (pattern established — replicate on new pages)
- Stats with units in **plain sentences** ("99.4% field precision across 12 district hospitals"), never only in graphics
- One-sentence definitional answers to every FAQ question before elaboration
- H2/H3 anchors + "On this page" TOC ✅
- 3–6 outbound primary-source links per essay (HIPAA: HHS.gov; EU AI Act: EUR-Lex; FHIR: hl7.org) 🆕
- Mirror every new section into `llms.txt`/`llms-full.txt` — keep FAQ wording **byte-identical** across HTML, JSON-LD and llms files
- Add `/build`-style markdown twins for the 2 flagship essays when time permits (§5.5 of audit — still open)

---

## 7. Technical & Regional Config

- ✅ Done: llms.txt suite, AI-crawler allowlist, Atom feed, IndexNow key, 404 fix, OG images, hreflang correctly skipped (single-lang).
- 🆕 GSC: filter Performance by **Country = US / DE / GB / IN** after 60 days — this is your measurement for "did US/EU visibility move?"
- 🆕 Add AI-referral regex to analytics: `chatgpt\.com|perplexity\.ai|gemini\.google|copilot\.microsoft|claude\.ai` as a channel group.
- 🆕 `X-Robots-Tag`/`hreflang`: if you ever add a US/EU service page, keep `en` canonical global (no hreflang needed; don't fragment a small site).
- Keep `og:locale` = en_IN — fine; add `og:image:alt` with entity string.

---

## 8. Off-Page (without this, §1 keywords stay dormant)

Be honest: no referring domains = no T3 rankings. Minimum viable link profile:

1. Clutch/GoodFirms/DesignRush profile for SoftEdge (category: healthcare software development, India) — also puts you in "best companies" lists AI engines read.
2. GitHub org + 2 public repos (ABDM sandbox snippets, RLS boilerplate) — developers and LLMs both mine GitHub.
3. 2 guest posts/quarter: HealthTech blogs, PostgreSQL weekly, Indian startup publications (YourStory/Inc42 style) — each with one contextual link.
4. Claim/backlink event pages (BFUHS, NHM Punjab, PSACS) — email organizers to list speaker + link.
5. LinkedIn: publish the TL;DR of every essay (LinkedIn is heavily mined by AI answers for professional entities).

---

## 9. 30 / 60 / 90-Day Sequence

**Day 0–7 (schema + entity, ~half day):** §3.1–3.5 edits → rebuild → IndexNow ping → validate with Rich Results Test.
**Day 8–30:** §2 title/H1 edits · §4.2 fractional CTO section · §5 FAQs on icare/automation · glossary additions (§4.5) · §8.1–8.2 accounts.
**Day 31–60:** §4.1 compliance essay (US/EU/IN) · §4.4 decision table · §8.3 first guest post · stats blocks (§4.7).
**Day 61–90:** §4.3 EU AI Act essay · pricing anchor · 2nd guest post + podcast · GSC country-filter review + AI-referral channel report.

**Success metrics:** brand SERP 100% owned · ≥3 T2 keywords in top 10 (IN) · first AI-engine citation (check Perplexity: "ABDM integration developer", "multi-tenant PostgreSQL consultant") · GSC impressions >0 from US+DE+GB · ≥5 referring domains.

---

*Generated 2026-09-24 from repository source audit. Keyword volumes are intent-shaped, not tool-extracted — validate with GSC after 30 days of data.*
