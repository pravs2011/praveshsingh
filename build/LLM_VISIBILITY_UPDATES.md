# LLM_VISIBILITY_UPDATES.md
### praveshsingh.com — AI Visibility & LLM Readiness Audit + Optimization Plan (PRD)

**Audit performed:** 2026-09-23 · **Framework:** per `LLM_VISIBILITY_IMPROVEMENTS.md` (10-section audit)
**Method:** Live-site crawl of `https://praveshsingh.com` (robots, sitemap, llms.txt, pages, headers, redirect chains, 404 behaviour, favicon/feed/OG asset checks) + full repo source analysis.

> ⚠️ **Critical context discovered during this audit:** the local repository already contains a large set of AI-visibility fixes (implemented 2026-09-23, see `IMPROVEMENTS_SEO_AIO_GEO.md` §10) that are **not yet deployed**. The live site is still running the pre-fix build. This document therefore reports findings in three states:
> - **🔴 LIVE-GAP** — true of the live site today (what AI crawlers actually see)
> - **🟡 REPO-FIXED** — already fixed in the repo, resolves on next deploy
> - **⚪ OPEN** — not yet addressed anywhere; needs new work

---

## 1. Website Accessibility & Crawling

### 1.1 Availability, HTTPS, redirects — verified live

| Check | Live result | Verdict |
|---|---|---|
| `https://praveshsingh.com/` | `200 OK`, `text/html; charset=utf-8` | ✅ |
| `http://praveshsingh.com/` | `301` → `https://praveshsingh.com/` | ✅ |
| `https://www.praveshsingh.com/` | `301` → non-www canonical | ✅ |
| `https://praveshsingh.com/index.html` | `301` → `/` | ✅ |
| `/robots.txt` | `200` | ✅ |
| `/sitemap.xml` | `200`, valid XML | ✅ |
| `/llms.txt`, `/llms-full.txt` | `200`, `text/plain; charset=utf-8` | ✅ |
| Garbage URL (`/garbage-test-url-xyz`) | **real `404`** with 13-byte Apache default body | ✅ status / ⚠️ see 1.3 |
| `/build/index.html` | `404` (build mirror not exposed) | ✅ |

### 1.2 AI crawler permissions (live robots.txt)

All requested agents verified **allowed**:

| Crawler | Status |
|---|---|
| GPTBot (OpenAI training) | ✅ Allow: / |
| OAI-SearchBot + ChatGPT-User | ✅ Allow: / |
| ClaudeBot / Claude-User / Claude-SearchBot / anthropic-ai | ✅ Allow: / |
| Google-Extended | ✅ Allow: / |
| PerplexityBot + Perplexity-User | ✅ Allow: / |
| Bingbot / Googlebot (implied by `User-agent: *`) | ✅ Allow: / |
| + Applebot(-Extended), CCBot, meta-externalagent, Amazonbot, cohere-ai, YouBot, Bytespider | ✅ Allow: / |

Sitemap declared in robots.txt ✅. **No problems found.** This is top-1% configuration — 19 AI bots explicitly permitted.

### 1.3 Problems found

| # | Severity | Finding |
|---|---|---|
| 1.3a | 🟡 REPO-FIXED | Live `.htaccess` contains `ErrorDocument 404 /index.html`. Empirically the host currently returns a **real 404** (the ErrorDocument subrequest appears to fail through the rewrite rules), but the directive is a latent soft-404 trap — any hosting change could silently start serving the homepage with HTTP 200 for every bad URL. Repo now ships a proper `404.html` (noindex, branded, recovery links). |
| 1.3b | 🔴 LIVE-GAP | **No HSTS header** live (`Strict-Transport-Security` absent). 🟡 Repo `.htaccess` now sets `max-age=31536000; includeSubDomains`. |
| 1.3c | 🔴 LIVE-GAP | **No CSP** live. 🟡 Repo ships report-only CSP to be tightened after observation. |
| 1.3d | 🔴 LIVE-GAP | New assets 404 live (not deployed): `/images/favicon.ico`, `/images/og-default.png`, `/writing/feed.xml`. 🟡 Present in repo. |
| 1.3e | ⚪ OPEN | No server-side visibility into AI crawler hits (no log monitoring configured) — you cannot currently prove GPTBot/ClaudeBot/PerplexityBot traffic. |
| 1.3f | 🟡 REPO-FIXED | Live pages load **both GTM (GTM-M335RXDF) and standalone gtag.js (G-2XHZ5NJZLK)** — duplicate pageview counting + double script download on every page. Repo keeps gtag.js only (the custom event tracker depends on `gtag()`). |

**Fixes:** deploy the repo (resolves 1.3a–d, 1.3f). For 1.3e see §10 roadmap item M1.

---

## 2. Robots.txt Analysis

**Live file analysed:** clean, no blocking errors, sitemap declared, intent documented.

Minor improvements already applied in repo (🟡):

```txt
# added in repo
Disallow: /build/
Disallow: /build$
Disallow: /404.html
# trailing comments document llms.txt + llms-full.txt endpoints
```

**Recommended additional hardening (⚪ OPEN):** none required for robots semantics. Optional: add explicit `User-agent: Amazonbot` crawl-delay only if log data later shows aggressive fetching. Do **not** add Crawl-delay for GPTBot/ClaudeBot — they ignore it and it signals distrust.

**Verdict: 10/10 — no blocking issues.**

---

## 3. Sitemap Analysis

**Live:** 14 URLs, all canonical https non-www, all resolve 200, correct priority weighting (home 1.0 → product pages 0.9 → essays 0.85).

| Issue | State |
|---|---|
| `changefreq` present on all URLs (Google ignores; signals template output) | 🟡 removed in repo |
| `lastmod` uniform `2026-09-21` on every page (not per-page-true) | 🟡 repo now has true per-page dates |
| Feed not discoverable from sitemap (Atom feeds are excluded from sitemaps by spec — fine) | n/a |
| Image sitemap extension for showcase/event photos | ⚪ OPEN (optional, §10 M4) |

**Verdict: 9/10 — deploy repo version.**

---

## 4. Technical SEO Audit

### 4.1 HTML (live)

| Element | Live state | Verdict |
|---|---|---|
| Title tags | Unique per page, entity-led; 2 pages at 80–81 chars truncate in SERP | 🟡 trimmed in repo (77/63 chars) |
| Meta descriptions | Unique, keyword-rich, 150–165 chars on all 13 pages | ✅ |
| Heading structure | Single H1 per page; logical H2/H3; `aria-labelledby` on sections | ✅ |
| Homepage H1 | "Building intelligent software products…" — no entity/keyword terms | 🟡 repo: "Pravesh Singh — Founder & CTO building AI platforms, healthcare software & multi-tenant SaaS." |
| Semantic HTML | `<header>/<main>/<section>/<article>/<footer>` throughout | ✅ |
| Image alt attributes | 15/15 imgs with alt on index; all checked pages pass | ✅ |
| Internal linking | Hub-and-spoke; but essays had **zero** essay→essay links (star topology, no spoke edges) | 🟡 repo adds "Related reading" (3 links per essay) |
| `<meta name="keywords">` | Present on every page (obsolete; mild negative signal) | 🟡 removed in repo |
| favicon | Inline SVG data-URI only — invisible to Bing + several AI indexers | 🟡 repo adds real `favicon.ico` + `apple-touch-icon.png` |

### 4.2 Performance (live)

| Issue | Detail | State |
|---|---|---|
| Hero PNG 2.05 MB | `images/pravesh-singh.png`; WebP twin (126 KB) is served via `<picture>` ✅ so browsers OK, but non-WebP crawlers + OG consumers pull the PNG | ⚪ OPEN (re-export <300 KB) |
| Double analytics | GTM + gtag.js both loaded live | 🟡 fixed in repo |
| CLS on gallery images | event/thumbnail/screenshot `<img>` lack `width`/`height` | ⚪ OPEN (low impact) |
| JS rendering | Site is fully server-rendered static HTML — **no JS-rendering issues for AI crawlers** (critical advantage: content does not require execution) | ✅ |
| Caching/compression | Apache mod_deflate + 1y immutable images + 1h HTML revalidate | ✅ |

### 4.3 Security (live)

| Header | Live | State |
|---|---|---|
| X-Content-Type-Options | ✅ nosniff | — |
| X-Frame-Options | ✅ SAMEORIGIN | — |
| Referrer-Policy | ✅ strict-origin-when-cross-origin | — |
| Permissions-Policy | ✅ camera/mic/geo disabled | — |
| **HSTS** | ❌ absent | 🟡 in repo |
| **CSP** | ❌ absent | 🟡 report-only in repo |
| HTTPS enforcement | ✅ 301 chain verified | — |

---

## 5. LLM Understanding Audit

*Test: can a model answer these from the live site alone?*

### 5.1 Person Entity — "Who is Pravesh Singh?"

| Expected understanding | Live evidence | Verdict |
|---|---|---|
| Founder & CTO | ⚠️ **Contradictory**: homepage title says "Founder, CTO & AI Software Architect"; footer says "Managing Director & CTO"; llms.txt says "Managing Director and CTO"; essay author boxes say "Founder, Managing Director & CTO". Four role strings across surfaces. | 🔴 LIVE-GAP → 🟡 repo unifies to "Founder & CTO" + synced MD&CTO FAQ answer |
| Software entrepreneur | ✅ stated in llms.txt, about, JSON-LD description | ✅ |
| Founder of SoftEdge Technology Solutions | ✅ `worksFor` + `founder` edges in JSON-LD | ✅ |
| Creator of TaskEdge | ✅ FAQ JSON-LD + `SoftwareApplication.author` @id edge | ✅ |
| Creator of iCare healthcare platform | ✅ FAQ JSON-LD + case-study page + `SoftwareApplication.author` | ✅ |
| 15+ years experience | ✅ facts strip + llms.txt + FAQ | ✅ |

**Gap:** live site has no extractable TL;DR blocks, no heading anchors, and **zero outbound citations** — models can *understand* the person but are given no verifiable third-party anchors (§5.4). 🟡 all fixed in repo essays.

### 5.2 Company Entity — "What does SoftEdge Technology Solutions do?"

| Check | Live evidence | Verdict |
|---|---|---|
| Description | ✅ JSON-LD Organization node + about/expertise pages | ✅ |
| Services | ✅ expertise.html (4 engagement formats with deliverables) | ✅ |
| Industries served | ✅ industries.html (Healthcare, Deskless Ops, FinTech, DPI) | ✅ |
| Technology expertise | ✅ skill blocks: Node.js/TypeScript, PostgreSQL RLS, AWS/Docker/K8s, FHIR | ✅ |
| Authority signals | ⚠️ Organization node has **no logo, no address, no sameAs**; company site linked but its own entity signals are out of scope of this repo | 🔴 logo gap → 🟡 repo adds `logo.png` 512² to JSON-LD; ⚪ company-site entity work OPEN |

### 5.3 Product Entities

**TaskEdge — "What is TaskEdge?"**

| Question | Answerable live? | Verdict |
|---|---|---|
| What is it? | ✅ "AI-powered business OS / operations SaaS" (title, FAQ, llms.txt) | ✅ |
| Who created it? | ✅ Pravesh Singh (FAQ + JSON-LD author edge) | ✅ |
| Target users | ✅ "deskless and shift-based teams… growing teams and enterprises" | ✅ |
| Features | ✅ tenant isolation, sub-50ms updates, shift handovers, invoicing, audit trails | ✅ |
| Technology | ✅ case study page (multi-tenant, RLS patterns) | ✅ |
| Business value | ✅ "without bloated enterprise management overhead" | ✅ |
| **Pricing?** | ❌ No public number anywhere → never cited for cost queries | ⚪ OPEN |

**iCare — "What healthcare software has Pravesh Singh built?"**

| Question | Answerable live? | Verdict |
|---|---|---|
| Healthcare use case | ✅ case study: registries + cold-chain factor logistics | ✅ |
| Hemophilia/thalassemia management | ✅ explicit throughout | ✅ |
| Government deployment | ✅ Punjab & MP state networks, NHM Punjab, PSACS, named events | ✅ |
| ABDM relevance | ✅ ABDM-aligned, FHIR R4 exportable bundles | ✅ |
| Security approach | ✅ RBAC, encryption, immutable audit logs | ✅ |
| **Quantified impact?** | ⚠️ "state-scale" but no patient/hospital/vial counts in extractable form | ⚪ OPEN |

### 5.4 The single biggest live LLM-understanding gap

The site's knowledge is **locked in prose**. Generative engines lift self-contained passages:
- no TL;DR / key-takeaways blocks (→ 🟡 added to all 6 essays in repo)
- no `id=` anchors on headings (→ 🟡 added; Perplexity cites passage anchors)
- no primary-source citations (→ 🟡 added: ABDM sandbox, NHA PDFs, NRCeS FHIR, PostgreSQL docs, MeitY DPDP, WHO)
- no RSS/Atom feed for discovery (→ 🟡 `writing/feed.xml` added)

---

## 6. Schema.org Structured Data Audit

### What exists live (verified valid JSON-LD on every page)

| Schema | Where | Missing (live) |
|---|---|---|
| `Person` | index, about, icare, taskedge, automation, expertise, essays | `knowsLanguage`, `address`, `nationality`, `email`, richer `sameAs` → 🟡 added in repo |
| `ProfilePage` | all main pages (+ misused as page type on case studies → 🟡 minor, left) | — |
| `Organization` (SoftEdge) | index, about, essays | **logo** → 🟡 repo adds `ImageObject logo.png` |
| `SoftwareApplication` | index, icare, taskedge | `offers`, `featureList` structured stats → ⚪ OPEN |
| `FAQPage` | index, expertise only | product pages → 🟡 repo adds 5 Q&As each on icare/taskedge/automation (visible HTML + JSON-LD) |
| `Article` | all 6 essays | `image`, `publisher.logo`, `article:modified_time` meta → 🟡 all added in repo |
| `BreadcrumbList` | every page | — ✅ exemplary |
| `OfferCatalog`/`Offer`/`Service` | expertise | `priceSpecification` → ⚪ OPEN (needs your pricing decision) |
| `Event` | **none live** | → 🟡 repo adds 4 Event nodes (Bhopal 2025, Chandigarh 2024, Faridkot 2023, PSACS 2025) |
| `CollectionPage`+`ItemList` | writing hub | `datePublished` per item → 🟡 added |

### Missing schema code — supplied (status notes)

Everything below is **already implemented in repo** 🟡 unless marked ⚪.

**(a) Organization logo + contact (⚪ partially — logo done, `contactPoint` optional):**
```json
"logo": {
  "@type": "ImageObject",
  "url": "https://praveshsingh.com/images/logo.png",
  "width": 512, "height": 512
}
```

**(b) Person enrichment (🟡 in repo `index.html`):**
```json
"email": "mailto:hello@praveshsingh.com",
"nationality": { "@type": "Country", "name": "India" },
"address": {
  "@type": "PostalAddress",
  "addressLocality": "Mohali", "addressRegion": "Punjab", "addressCountry": "IN"
},
"knowsLanguage": ["en", "hi", "pa"]
```

**(c) Event nodes (🟡 in repo, pattern):**
```json
{
  "@type": "Event",
  "@id": "https://praveshsingh.com/#event-bhopal-2025",
  "name": "National Hemophilia Consensus Meeting — Live iCare Demonstration",
  "startDate": "2025-05-22",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": { "@type": "Place", "name": "Bhopal, Madhya Pradesh",
    "address": { "@type": "PostalAddress", "addressLocality": "Bhopal",
                 "addressRegion": "MP", "addressCountry": "IN" } },
  "performer": { "@id": "https://praveshsingh.com/#person" }
}
```

**(d) Article image + modified time (🟡 in repo):** `"image": {"@type":"ImageObject","url":"https://praveshsingh.com/images/og-default.png"}` inside every Article node + `<meta property="article:modified_time">`.

**(e) SoftwareApplication offers (⚪ OPEN — needs pricing decision):**
```json
"offers": {
  "@type": "Offer",
  "price": "0", "priceCurrency": "INR",
  "availability": "https://schema.org/InStock",
  "url": "https://praveshsingh.com/expertise.html#packages",
  "description": "Demo available on request; engagement via fixed-scope sprints or SoftEdge contracts."
}
```
(Use a real price/tier only when you decide to publish one — a placeholder damages trust more than absence.)

---

## 7. Content Quality Audit — "Can an LLM answer this from the page?"

| Question | Live site | After repo deploy | Remaining gap |
|---|---|---|---|
| "Who is Pravesh Singh?" | ✅ (with role-string noise) | ✅ clean + consistent | — |
| "Which products has Pravesh Singh created?" | ✅ iCare, TaskEdge, AI engines | ✅ | — |
| "What does SoftEdge Technology Solutions do?" | ✅ | ✅ | external corroboration (⚪) |
| "What is TaskEdge?" | ✅ | ✅ + FAQ passage | pricing (⚪) |
| "What healthcare software has Pravesh Singh built?" | ✅ | ✅ + per-product FAQs | quantified stats (⚪) |
| "Is Pravesh Singh a credible ABDM expert?" | ⚠️ self-attested only | ✅ better: essays now cite official NHA/NRCeS sources; Event nodes add verifiable talks | third-party mentions (⚪) |
| "How does iCare prevent medicine stock-outs?" | ⚠️ buried in prose | ✅ now an extractable FAQ answer | — |
| "How much does a fractional CTO cost in India?" | ❌ | ❌ | pricing page (⚪ §9) |
| "Schema-per-tenant vs RLS — which should I choose?" | ⚠️ prose only | ✅ TL;DR + decision-matrix anchors | — |

**Exact content improvements already applied (🟡):** 5-question FAQ blocks on icare/taskedge/automation with quotable 40–70-word answers; TL;DR + Key-takeaway structures on essays; statistics mirrored into `llms.txt` ("sub-50ms task updates", ">99.4% field-level precision", "15+ years", "4 state/national health events").

---

## 8. AI Search Optimization Recommendations (by engine)

| Engine | Lever | State |
|---|---|---|
| **ChatGPT Search** | Bing index dependence → favicon + IndexNow + clean titles matter; OAI-SearchBot allowed ✅ | 🟡 assets in repo; ⚪ ping after deploy |
| **Perplexity** | Cites passage anchors + fresh feeds; PerplexityBot allowed ✅ | 🟡 anchors + feed in repo |
| **Google AI Overviews** | Rides Googlebot index + structured data + E-E-A-T | 🟡 Event/FAQ/Article-image schema in repo; ⚪ GSC rich-result validation after deploy |
| **Gemini** | Grounds on Google index + `Google-Extended` (allowed ✅) | 🟡 same as above |
| **Copilot** | Bing-grounded | 🟡 IndexNow key ready in repo |

**New-page & knowledge-graph recommendations** → consolidated into §9 plan. The two highest-leverage signals still missing everywhere: **third-party corroboration** (event programs, news mentions, GitHub, Wikidata) and **public pricing anchors**.

---

## 9. Missing Content Plan (prioritized)

| # | Page | Purpose | Title / H1 | Outline | Keywords | Schema |
|---|---|---|---|---|---|---|
| 9.1 | `/speaking.html` | Third-party-verifiable proof page for all talks — the #1 entity-authority gap | **Title:** Speaking & Workshops — HealthTech Keynotes by Pravesh Singh · **H1:** Talks, workshops & state health reviews | One entry per event: date, venue, audience, organiser, *external* link (event program/news), 2 photos, 40-word summary | "Pravesh Singh speaker", "ABDM workshop Punjab", "hemophilia summit Faridkot" | `Event` ×N + `Person.performer` |
| 9.2 | `/case-studies/icare-outcomes.html` | Quantified outcomes → becomes the only citable source for these claims | **H1:** iCare at state scale: registry & cold-chain outcomes | Deployment scope, vial-tracking volume, stock-out reduction, audit results; each stat dated + sourced | "hemophilia registry India outcomes", "cold-chain stock-out prevention software" | `Article` + `Dataset`/stats in `SoftwareApplication` |
| 9.3 | `/pricing.html` (or FAQ block on expertise) | Pricing anchor for commercial-intent AI queries | **H1:** Engagement pricing: audits, fractional CTO, ABDM sprints | 4 packages with from-pricing or ranges; what changes price; procurement notes (state/enterprise) | "fractional CTO cost India", "ABDM integration sprint cost", "healthcare software audit price" | `Offer` + `priceSpecification` |
| 9.4 | `/glossary.html` | Definitional queries are the #1 AEO citation format | **H1:** Health-tech engineering glossary | 10–15 terms: FEFO, ABDM M1/M2/M3, ABHA, HIP/HIU, care context, consent artifact, RLS, cold chain, DPDP fiduciary | "what is FEFO in pharma", "ABDM M1 M2 M3 meaning", "what is a HIP in ABDM" | `DefinedTermSet`/`DefinedTerm` |
| 9.5 | `/company.html` | SoftEdge entity deep-page (currently the company has no page on this domain) | **H1:** SoftEdge Technology Solutions — engineering partner | Services, team model, industries, engagement process, link to softedgetechnology.com | "SoftEdge Technology Solutions", "Mohali software company" | `Organization` (full: address, contactPoint, founder→Person) |
| 9.6 | `/writing/feed.xml` ✅ + 1 essay/month cadence | Freshness signal for all discovery layers | — | Maintain current essay quality; each new essay ships with TL;DR, anchors, references (template updated 🟡) | — | `Article` |

Items 9.1 and 9.3 need **your input** (event URLs/press links; pricing decision) before implementation.

---

## 10. Final AI Visibility Score

### Scores — LIVE site today

| Dimension | Score | Rationale |
|---|---|---|
| **Technical Crawlability** | **88/100** | Exemplary robots (19 AI bots), valid sitemap, llms.txt+llms-full.txt, perfect redirect chain, real 404s, static HTML (no JS-render risk). Deductions: no HSTS/CSP, no favicon/feed live, duplicate analytics. |
| **Search Engine SEO** | **82/100** | Strong titles/descriptions/headings/alt/semantics. Deductions: meta keywords (mild), 2MB hero PNG, no favicon, truncated titles on 2 pages, generic H1, no Organization logo. |
| **LLM Understanding** | **74/100** | llms.txt suite is excellent and entity facts are present. Deductions: role-string contradictions, knowledge locked in prose (no TL;DR/anchors/references live), no feed, FAQ coverage on only 2 of 13 pages. |
| **Entity Recognition** | **62/100** | Person/Product/Organization nodes exist with @id graph — genuinely good. Deductions: thin `sameAs`, no address/language/email in schema, **zero Event markup**, no logo, no external corroboration (Wikidata/news/GitHub), all 4 talks self-attested. |
| **Content Authority** | **70/100** | Production-grounded essays with real deployment proof; named officials/institutions. Deductions: ~900-word essays without citations live, no outbound references, no speaking page, no quantified outcomes, self-referential only. |
| **Composite** | **75/100** | Strong foundation; entity corroboration is the binding constraint. |

### Projected after repo deploy (no new content)

| Dimension | Score |
|---|---|
| Technical Crawlability | 95/100 |
| Search Engine SEO | 90/100 |
| LLM Understanding | 88/100 |
| Entity Recognition | 76/100 |
| Content Authority | 80/100 |
| **Composite** | **86/100** |

---

## 11. Prioritized Action Plan (PRD: "praveshsingh.com AI Visibility Optimization Plan")

### Current state
Static 13-page site, fully server-rendered, best-practice AI-crawler access, solid JSON-LD @graph, dedicated llms.txt suite. Repo contains an implemented, verified fix-set (GEO blocks, schema enrichment, brand assets, hardened .htaccess, feed) **awaiting deployment**.

### Critical issues (deploy blockers / trust risks)
1. **Deploy the repo** — every 🟡 item above resolves in one push. Then verify: `curl -I` HSTS present; `/build/*` → 404; garbage URL → 404 with branded page; `/writing/feed.xml` → 200.
2. **Post-deploy IndexNow ping** (key file live in repo root):
   ```bash
   curl "https://api.indexnow.org/indexnow?url=https://praveshsingh.com/&key=8f4a2c19e7b34d5680f1ae92c7b5d316"
   ```
3. **AI-crawler measurement** — without logs you're flying blind. Minimum: weekly
   `grep -cE "GPTBot|ClaudeBot|PerplexityBot|OAI-SearchBot" access.log` (or GoAccess). Target: dashboard by day 30.

### High-impact improvements (this week → 30 days)
4. Rich-result validation on deploy: Google Rich Results Test on `/`, `/icare.html`, one essay; fix anything flagged.
5. Compress `images/pravesh-singh.png` 2.05 MB → <300 KB (photo; re-export).
6. CSP: review report-only output after 2–4 weeks → enforce.
7. Speaking page (§9.1) — needs your event/press URLs.
8. `sameAs` expansion as profiles exist (GitHub/X/Wikidata item for the person entity).

### Quick wins (1–7 days, mostly done in repo)
9. ✅ favicon/apple-touch-icon/logo/OG-card assets — *done in repo*
10. ✅ TL;DR/anchors/references/related-reading on essays — *done*
11. ✅ Product FAQs + Event nodes + Person/Organization enrichment — *done*
12. ⚪ PNG compression (5 min), ⚪ sitemap `lastmod` auto-truth from deploy script (30 min), ⚪ gallery `width/height` attrs (30 min)

### Long-term improvements (30–90 days)
13. Pricing page with `Offer.priceSpecification` (§9.3) — requires pricing decision.
14. Case-study outcomes page with dated, sourced statistics (§9.2) — requires your numbers.
15. Glossary (§9.4) + 1 essay/month cadence; keep TL;DR/refs pattern.
16. External corroboration campaign: get event listings/news pages to link back; create Wikidata item; GitHub profile with pinned repos; SoftEdge company entity work on softedgetechnology.com (logo, address, sameAs cross-links both directions).
17. Image sitemap for showcase photos (optional).
18. Company page (§9.5) if you want the SoftEdge entity fully represented on this domain.

### Required code changes — status
| Change | Status |
|---|---|
| 404.html + .htaccess (HSTS/CSP/404/build block) | ✅ in repo |
| robots.txt build/404 disallow | ✅ in repo |
| GTM/gtag dedupe, keywords removal, favicon links | ✅ all 16 pages |
| Person/Organization/Event/FAQPage/Article schema | ✅ in repo, all JSON-LD validated |
| Brand assets (logo, favicon, OG 1200×630) | ✅ generated (`tools/generate_brand_assets.py`) |
| Atom feed + llms.txt/llms-full.txt updates | ✅ in repo |
| `width/height` on gallery images | ⚪ open (low priority) |
| Pricing/offers schema, case-study stats, glossary, speaking page | ⚪ open — need your input (content decisions, not code) |

### Required content changes — status
| Change | Status |
|---|---|
| Role-string unification + FAQ sync | ✅ |
| TL;DRs, TOCs, references, related reading | ✅ |
| Key-claims sections in llms-full.txt | ✅ |
| Speaking page content (event URLs/press) | ⚪ needs your input |
| Public pricing | ⚪ needs your decision |
| Quantified iCare/TaskEdge stats | ⚪ needs your numbers |

### Implementation priority
```
P0  Deploy repo + verify headers/404s/feed + IndexNow ping        (1 day)
P1  AI-crawler log monitoring + Rich Results validation            (week 1)
P1  PNG compression + gallery dimensions                           (week 1)
P2  Speaking page (§9.1) + sameAs expansion                        (weeks 2–4)
P2  CSP enforcement after report-only period                       (weeks 3–6)
P3  Pricing page + case-study outcomes + glossary                  (30–90 days)
P3  External corroboration campaign (Wikidata, press, GitHub)      (ongoing)
```

---

*Live-site evidence gathered 2026-09-23 (robots, sitemap, llms.txt, pages, headers, redirect chains, 404s, asset availability). Repo state verified via source analysis + JSON-LD/XML validation. Companion document: `IMPROVEMENTS_SEO_AIO_GEO.md` (implementation log §10).*
