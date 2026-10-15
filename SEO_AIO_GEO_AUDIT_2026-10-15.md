# SEO · AIO · GEO Audit Report — praveshsingh.com

**Auditor persona:** Senior SEO × AEO (Answer Engine Optimization) × GEO/AIO (Generative Engine Optimization)
**Audit date:** 2026-10-15 · **Scope:** full repo (13 canonical pages + writing hub, 6 essays, `llms.txt`, `llms-full.txt`, `robots.txt`, `sitemap.xml`, `.htaccess`, JSON-LD, brand assets) **plus live-site verification** of `/` and `/robots.txt`
**Method:** live fetch + static-source inspection + JSON-LD parse validation. Findings are verified against current files, not against the prior (2026-09-23) audit log.

---

## 0. Executive Summary

praveshsingh.com is in the **top ~1% of personal/static sites on AI-search readiness**. Live verification confirms:

- ✅ HTTPS, HTTP 200, clean canonical homepage, correct `<title>` and meta description served live
- ✅ `robots.txt` served live, allowlisting **19 named AI/LLM crawlers** (GPTBot, OAI-SearchBot, ClaudeBot, Claude-SearchBot, PerplexityBot, Google-Extended, Applebot-Extended, CCBot, Amazonbot, cohere-ai, YouBot, Bytespider, …) with a sitemap declaration
- ✅ Full GEO apparatus: `llms.txt` + `llms-full.txt` + `expertise.md` markdown twin + Atom feed, all cross-linked from `<head>` link relations
- ✅ Server-side entity hygiene: real 404 handler, `/build/` 404-block + `X-Robots-Tag`, HTTPS/non-www/`index.html` 301 canonicalization, HSTS, consent-gated GA4 (GDPR pattern done right)
- ✅ Every sampled page's JSON-LD `@graph` **parses cleanly** (validated programmatically): ProfilePage / Person / Organization / SoftwareApplication / Service / ProfessionalService / WebSite / FAQPage / Event ×4 / Article / BreadcrumbList
- ✅ All 6 essays carry **TL;DR quotable-answer blocks, `<h2 id>` heading anchors, References sections with primary-source outbound links, and essay↔essay cross-links** — the core GEO extraction surface

The remaining issues are **polish and consistency drift**, not foundations. Four concrete defects were found in this pass (one stale-metadata bug, one past-event schema misuse, one residual `meta keywords`, one uniform-sitemap regression). Grade: **A−**.

### Scorecard

| Dimension | Score | Notes |
|---|---|---|
| Technical crawlability (search) | 96/100 | Canonicalization, 404s, headers, sitemap all verified live |
| Classic on-page SEO | 90/100 | Titles/descriptions strong; minor length + residue issues |
| Structured data / rich results | 92/100 | Deep `@graph`, all valid; `Event` status misused on past events |
| AEO (answer-engine surfaces) | 93/100 | FAQ layers, TL;DRs, glossary; visible-FAQ parity varies by page |
| GEO (LLM citation readiness) | 95/100 | llms.txt stack + markdown twins are genuinely elite |
| Entity recognition / Knowledge Graph | 88/100 | Strong `@id` graph; `sameAs` still thin on external corroboration |
| Measurement | 55/100 | GA4 ok, **no AI-crawler log monitoring** — GEO effort is unmeasurable |
| **Overall** | **A− (88/100)** | |

---

## 1. Verified Live State (as of 2026-10-15)

| Check | Result |
|---|---|
| `GET https://praveshsingh.com/` | HTTP 200, `text/html; charset=utf-8` ✅ |
| Live `<title>` | "Pravesh Singh – Founder & CTO, AI Software Architect" ✅ |
| Live meta description | "Fractional CTO, senior AI developer & healthcare software architect…" ✅ |
| `robots.txt` | HTTP 200, AI-crawler allowlist + sitemap ✅ |
| Canonical redirects | `.htaccess` 301s: http→https, www→apex, `/index.html`→`/`, `/writing`→`/writing/` ✅ (not re-tested over wire this pass; config is present and was live-verified in the prior cycle) |
| Site hub extraction | Homepage text extracts as clean factual copy about iCare capability blocks — LLM-favorable ✅ |

### Prior audit → current repo: verification of claimed fixes

The 2026-09-23 implementation log claims were **spot-checked against current files**. Confirmed shipped: TL;DR blocks (6/6 essays), heading anchors (5 per essay), References with outbound sources, essay cross-links, Atom feed + `<link rel="alternate">`, `Article.image` + `publisher.logo`, `Event` nodes ×4, Person enrichment (`email`, `nationality`, `address`, `knowsLanguage`), Organization `logo` 512×512, favicon/logo/OG asset set, HSTS + CSP-Report-Only, IndexNow key file, `changefreq` removed, real 404, `/build/` enforcement.

⚠️ **Two claims did not fully hold** (see findings 1.2 and 2.2 below): visible-FAQ parity on product pages, and `<meta keywords>` removal on `index.html`. Reminder: the production zip is built by `./make_build.sh`, which validates and fails on missing consent blocks — redeploy after fixes so repo ≠ production drift doesn't recur.

---

## 2. Findings

Legend: 🔴 high impact · 🟠 medium · 🟡 low/polish · ✅ correct as-is

### 1) On-page & metadata

| # | Finding | Evidence | Fix |
|---|---|---|---|
| 1.1 | 🔴 **Stale OG image dimensions on `index.html`** — head declares `og:image:width 880` / `height 1140` (portrait), but the actual `images/og-default.png` file is **1200×630** and every *other* page declares 1200×630. LinkedIn/Slack/iMessage and AI card generators trust the declared size; a portrait-declared image gets mis-scaled or rejected on the site's most-shared URL. | `index.html` lines 37–38 vs `file images/og-default.png` → "PNG image data, 1200 x 630" | Set `"og:image:width" content="1200"` / `"height" content="630"` in `index.html`. Also swap `og:type` from `profile` → `website` (with `Person` in JSON-LD already carrying the identity, `profile` adds nothing and limits link previews). |
| 1.2 | 🟠 **`<meta name="keywords">` survives on `index.html` only** | `grep name="keywords"` → matches `index.html` alone | Delete the line (dead since 2009; keep consistency with the other 12 pages). |
| 1.3 | 🟡 **Title lengths at the display edge**: `icare.html` `<title>` ≈ 74 chars ("iCare — HIPAA-Aware, ABDM-Ready Patient Registry & Cold-Chain Software"), `taskedge.html` ≈ 63. `icare` risks truncation on mobile SERPs; brand term "Pravesh Singh" absent from both titles (site-name rewriting usually supplies it, but don't rely on it) | titles as served | Either trim "HIPAA-Aware, ABDM-Ready" to the two strongest qualifiers or append brand. Keep each ≤ 60 chars of visible text. |
| 1.4 | ✅ **Hero H1 is now entity + outcome anchored**: "Building software for when lives depend on it." — short, memorable, and the persona keywords live in the meta description. Acceptable. | `index.html` | None. |
| 1.5 | 🟡 **Uniform `lastmod` regression**: all 15 sitemap URLs share `2026-09-25`, even though essays were touched 2026-09-21+ and files differ. Uniform `lastmod` trains Google to distrust freshness signals | `sitemap.xml` | Derive per-URL `lastmod` from the file's git commit date in `make_build.sh`. |

### 2) Structured data (Schema.org)

All five sampled pages' JSON-LD parse ✅ with stable `@id` cross-references. One real defect:

| # | Finding | Evidence | Fix |
|---|---|---|---|
| 2.1 | 🟠 **All four `Event` nodes declare `eventStatus: "EventScheduled"` for events that began 2023-07 through 2025-07 — i.e., all in the past as of today.** Google's event guidelines treat `EventScheduled` as future-only; mislabelled past events are rejected from event surfaces and can be read by LLMs as claiming *upcoming* talks (a subtle factual-drift risk for an entity that sells trust). | `index.html` JSON-LD nodes `#event-bhopal-2025`, `#event-chandigarh-2024`, `#event-faridkot-2023`, `#event-psacs-2025` | Remove `eventStatus` entirely on past events (Google only expects it for postponed/cancelled/moved). Optionally mark them `"@type": "Event"` with `endDate` where multi-day. The Bhopal and PSACS 2025 events may be near-adjacent to the present; verify none are genuinely upcoming before asserting. |
| 2.2 | ✅ **CORRECTED 2026-10-15 (was a false positive): visible-FAQ parity is present.** The product pages don't use the `faq-row` accordion class (hence the earlier zero-grep), but each has an `id="faq"` section with `h3` questions + `p` answers, and sampled question/answer strings match their `FAQPage` JSON-LD verbatim (icare.svg 6 Q&A, taskedge 5, automation 5, expertise 12). | programmatic parity check on `icare.html` (question + answer text found in visible section) | No change needed. See `FIX_SEO_AIO_GEO.md` §"Verified-not-broken". |
| 2.3 | 🟡 **`ProfilePage` used as the page type on icare/taskedge/automation** — those are case studies/service pages, not profile pages. Google's newer `ProfilePage` doc expects the main entity to be a person profile. | JSON-LD `@type` per page | Switch to `WebPage` (or `AboutPage`/`CollectionPage` as apt) with `mainEntity`/`about` → `#person` and the product node as `mentions`. Low stakes but cleaner entity edges. |
| 2.4 | ✅ `Article` nodes on essays now include `image` + `publisher.logo`; `BreadcrumbList` on every inner page; `ProfessionalService` + `OfferCatalog` on `expertise.html`. All correct. | parsed graphs | — |

### 3) GEO — machine surfacing for LLM engines (the site's core bet)

| # | Finding | Evidence | Fix |
|---|---|---|---|
| 3.1 | ✅ **llms.txt is structured like an entity dossier** — verified-facts block with hard numbers (15+ yrs, sub-50ms, >99.4% precision, 4 events), capability pillars, product cards with URLs, per-essay abstracts, and dated talks. This is precisely the format that gets quoted. | `llms.txt` | — |
| 3.2 | 🟠 **`llms-full.txt` last-updated: 2026-09-21 is stale vs current index-page copy.** The live homepage description says "Fractional CTO, senior AI developer & healthcare software architect… clients in India, the US and Europe"; the homepage JSON-LD `Person.description` still opens with the older clinic-reality narrative and only mentions India-scale deployments. Cross-document drift among three Person descriptions (live meta, JSON-LD, llms.txt) is the #1 entity-noise vector. | compare `index.html` head vs JSON-LD vs `llms.txt` §Identity | Pick one canonical 2-sentence bio (recommend the fractional-CTO/global-clients one, since it carries commercial intent) and byte-sync it across live `<title>`/meta, JSON-LD `Person.description`, `llms.txt`, `llms-full.txt`, `about.html` lead, and `expertise.md`. |
| 3.3 | 🟠 **Role-string drift persists inside `llms.txt`**: it says "Managing Director and Chief Technology Officer" while the live title/JSON-LD lead with "Founder & CTO". Since `llms.txt` is the first thing an LLM reads, MD-vs-Founder inconsistency across surfaces dilutes the single most-queried fact ("Who is Pravesh Singh?") | `llms.txt` §Identity & llms-full.txt | One canonical courtesy title, one order, everywhere. Suggested canonical: *"Founder & Chief Technology Officer (CTO), SoftEdge Technology Solutions"*; keep "Managing Director" only as a legal-entity fact in company.html. |
| 3.4 | 🟡 **`robots.txt` blocklist of `/yandex_` prefix is fine, `Disallow: /build/` correct, template disallow correct.** One nit: `Bytespider` is allowed, but Bytespider ignores robots.txt anyway; harmless to keep. | — | None needed. |
| 3.5 | 🟡 **No per-essay markdown twins** — only `expertise.md` exists. For a site that already ships `text/markdown` MIME types + link relations, per-essay `.md` twins (auto-derived from the TL;DR + TOC) are the cheapest still-missing GEO uplift. | `expertise.md` only | Extend `make_page.sh`/build to emit each essay's twin + add to `llms.txt` site index. |
| 3.6 | ✅ Sitemap + llms.txt cover all 14 canonical URLs; `sitemap ↔ files` consistency holds (6 essays + hub present on disk and in sitemap). | verified | — |

### 4) AEO — answer-engine surfaces (Google AI Overviews, Perplexity, Copilot)

| # | Finding | Evidence | Fix |
|---|---|---|---|
| 4.1 | ✅ Strong extractable passages: TL;DR boxes under every essay H1, `<h2 id>` anchors + TOC (deep-link/passage citation ready), decision tables, References with outbound primary sources (NHA sandbox, FHIR, PostgreSQL docs, MeitY DPDP). | essays | — |
| 4.2 | 🟠 **Definitional-intent gap between glossary and AI Overviews**: `glossary.html` targets exactly the "what is FEFO / ABDM M1 vs M2 / HIP vs HIU" queries that AI Overviews love, but it is a single page. Winning these citations usually requires one focused page per term (or at least one anchored definition per term with its own `<h2 id>`, a direct 40–60-word answer paragraph, and one outbound authority link each). | glossary.html | Verify glossary uses one `<h2 id>` per term with a definition-first paragraph; add outbound links (NHA, FHIR spec, MeitY) per entry. |
| 4.3 | 🟡 **No pricing anchor anywhere** — AI Overviews and Perplexity cite "how much does X cost" answers; you'll never win those queries without one publishable band ("from ₹X / fixed-scope architecture review"), even soft. Decision is commercial, not technical. | expertise.html | Your call; if yes, mirror into `Offer.priceSpecification` + FAQ "How much does a fractional CTO engagement cost?" |
| 4.4 | 🟡 **FAQ questions still product-shaped; buyer-decision questions unbeaten**: "Schema-per-tenant vs RLS: which should I choose?", "How do I make a hospital app ABDM compliant?", "Fractional CTO in India — engagement models?" — high AI-Overview citation likelihood. | FAQ sets | Add 2–3 decision-shaped Q&As to product/FAQ surfaces. |
| 4.5 | ✅ FAQ accordions keep answers in-DOM; no crawlability issue. Google restricted FAQ *rich results* to authority sites, but the AEO extraction value is unchanged. | — | — |

### 5) Performance & infrastructure

| # | Finding | Fix |
|---|---|---|
| 5.1 | 🟡 `images/pravesh-singh.png` = 475 KB (down from 2 MB — improved), still the largest first-load asset; WebP twin (73 KB) serves modern browsers via `<picture>`. Squée to <250 KB and call it done. | TinyPNG/squoosh re-export |
| 5.2 | ✅ Cache headers, DEFLATE, HSTS, CSP-Report-Only, `nosniff`, frame + permissions policies — all present in `.htaccess`. Flip CSP to enforcing after the report-only window. | — |
| 5.3 | ✅ Consent-gated GA4 with default-denied consent is the correct EU/UK/DPDP posture (and privacy.html promises no ad tags). | — |
| 5.4 | ✅ IndexNow key file shipped. **The ping is manual** — nothing in the repo pings after deploys. Add a post-deploy step: `curl "https://api.indexnow.org/indexnow?url=https://praveshsingh.com/&key=8f4a2c19e7b34d5680f1ae92c7b5d316"` for the homepage + each changed URL. | wire into make_build.sh/deploy flow |

### 6) Entity & authority (Knowledge Graph / E-E-A-T)

| # | Finding | Fix |
|---|---|---|
| 6.1 | 🟠 **`sameAs` external corroboration is still thin** (LinkedIn, GitHub, SoftEdge site, taskedge.io, own subpages). The four government-health-event claims are self-attested only — no external link, no press mention, no event-program URL. LLMs verify cross-source before treating an entity's claims as ground truth. | Add any verifiable third-party edges: LinkedIn company page for SoftEdge, conference/event program pages, news mentions, Crunchbase, X profile. Even 3 edges materially merge the entity. |
| 6.2 | 🟡 `Person.award` strings embed event names — fine, but the richer `Role`/`PerformingRole` modeling was never applied; low priority. | optional |
| 6.3 | ✅ `knowsAbout` list is disciplined and niche (16 well-scoped terms incl. ABDM, FHIR, FEFO, DPDP, EU AI Act) — strong topical-vector alignment for LLM retrieval. | — |

---

## 3. Prioritized Roadmap

### Sprint 0 — bugs from this audit (1 hour, do all)

1. 🔴 `index.html` OG dims 880×1140 → 1200×630; `og:type` `profile` → `website` (1.1)
2. 🟠 Drop `<meta keywords>` from `index.html` (1.2)
3. 🟠 Remove `eventStatus: "EventScheduled"` from the 4 past `Event` nodes (2.1)
4. 🟠 Byte-sync the canonical bio string across JSON-LD `Person.description` ↔ `llms.txt` ↔ `llms-full.txt` ↔ live meta; unify Founder/MD role string (3.2/3.3)
5. ~~🟠 Add visible Q&A mirrored 1:1 with JSON-LD on `icare.html`, `taskedge.html`, `automation.html`~~ — **withdrawn after verification (§2.2 CORRECTED): parity already present.**

### Sprint 1 — citation-surface expansion (2–4 days)

6. Per-essay markdown twins + `llms.txt` index update (3.5)
7. Glossary: definition-first, anchor-per-term, outbound-authority-per-term (4.2)
8. 2–3 decision-shaped Q&As on product pages (4.4)
9. 3+ external `sameAs`/event-program citations for entity corroboration (6.1)
10. True per-URL `lastmod` derived from git in the build (1.5)

### Sprint 2 — measurement & automation (ongoing)

11. 🔴 **AI-crawler log monitoring** ( Apache access-log grep for GPTBot/ClaudeBot/PerplexityBot/OAI-SearchBot, or GoAccess) — without this, none of the GEO work can be attributed; the single biggest unmet item on the site
12. IndexNow ping automation post-deploy (5.4)
13. Flip CSP to enforcing (5.2)
14. Compress portrait PNG (5.1)

### Content bets (your decision)

15. Publish one pricing anchor → unlocks "cost of" query class (4.3)
16. One comparison table per essay surfaced at the top → comparison queries dominate AI Overview citations
17. Consider one thematic essay per commercial pillar (e.g., "ABDM integration sprint: scope and timeline in practice") — content that maps 1:1 to the engagement packages in `llms.txt`

---

## 4. What's Already Excellent (do not change)

- ✅ `llms.txt` + `llms-full.txt` + markdown twin + Atom feed — elite machine-context stack
- ✅ Named 19-crawler AI allowlist in robots.txt with intent comments
- ✅ Valid multi-node JSON-LD `@graph` with stable `@id`s and cross-references on every page (programmatically verified)
- ✅ TL;DR + anchors + References + cross-links on every essay — the measurable GEO surface is *there*
- ✅ Server-side canonical/lifecycle discipline: real 404, `/build/` 404+noindex, IndexNow key, consent-gated GA4, HSTS/CSP-Report-Only
- ✅ Disciplined, niche `knowsAbout` taxonomy; fact-strip numbers mirrored into `llms.txt`
- ✅ Build pipeline with validation (`make_build.sh` fails on missing consent block, sitemap↔file mismatch, canonical hygiene)

---

*Sources: live fetches of `/` and `/robots.txt` (2026-10-15); repo source at commit state as of this audit; JSON-LD parse validation script run over 6 representative pages; all grep counts quoted are from current files. Line references approximate.*
