# SEO / AEO / GEO-AIO Audit — praveshsingh.com

**Auditor role:** Senior SEO · AEO (Answer Engine Optimization) · GEO/AIO (Generative Engine / AI Optimization)
**Audit date:** 2026-09-23 · **Scope:** Full repo (13 canonical pages, writing hub, `llms.txt`, `llms-full.txt`, `robots.txt`, `sitemap.xml`, `.htaccess`, structured data)
**Scoring legend:** 🔴 High impact · 🟠 Medium · 🟡 Low/polish

---

## 0. Executive Summary

The site is **already far ahead of typical personal sites**: dedicated `llms.txt` + `llms-full.txt`, explicit AI-crawler allowlists in `robots.txt`, JSON-LD `@graph` on every page, FAQPage schema, canonical hygiene via `.htaccess`, `security.txt`, and a well-built writing hub. That foundation is genuinely strong.

The gaps that remain cluster into **five themes**:

1. **Entity consistency drift** — Founder vs Managing Director, iCare "HealthApplication" vs case-study framing, FAQ answers that differ between `index.html`, `llms.txt` and `llms-full.txt`. LLMs and Google's Knowledge Graph reconcile entities by cross-document consensus; contradictions dilute them.
2. **Missing rich-result eligibility** — No `Organization` logo, no `Article` images, incomplete `Person` identifiers (`knowsLanguage`, `address`, `alumniOf`, `hasCredential`), no `favicon`/apple-touch icons beyond an inline SVG.
3. **Thin citation surfaces for GEO** — Articles are ~850–940 words with no TL;DR blocks, no in-page anchor IDs (no jump links), no Article-to-Article cross-linking, no outbound citations to primary sources (ABDM sandbox docs, FHIR spec, DPDP Act text). Generative engines favor *extractable, self-contained, well-cited* passages.
4. **Measurement blind spots** — No server log analytics on AI-crawler hits, GTM + gtag double-loading, no RSS/Atom feed for the writing hub.
5. **Fragile infrastructure** — `ErrorDocument 404 /index.html` soft-404s every missing URL as HTTP 200, `/writing/` directory requests 301 to home, `build/` directory shipped as a deploy sibling risk, 2 MB PNG hero image.

**Overall grade: B+ → target A.** Highest-ROI sequence: §1 entity consistency → §4 GEO content surfaces → §3 schema enrichment → §6 infra fixes.

---

## 1. Entity Consistency & Knowledge-Graph Signals 🟠

*LLMs build one internal entity per person. Every contradiction between pages is noise in that entity's embedding.*

| # | Finding | Evidence | Fix |
|---|---------|----------|-----|
| 1.1 | **Title/role drift: "Founder" vs "Managing Director"** | `index.html` title: *"Founder, CTO & AI Software Architect"*; hero says "Founder & CTO"; footer, `llms.txt` and most subpages say **"Managing Director & CTO"**; about/case-study pages say "Founder & CTO". Pick **one canonical role string** (recommend *"Founder & CTO, SoftEdge Technology Solutions"*) and use it everywhere: `<title>`, meta author, JSON-LD `jobTitle`, `llms.txt`, footer, author boxes. | 🟠 |
| 1.2 | **FAQ answer mismatch across surfaces** | `index.html` FAQ JSON-LD says Founder; `llms-full.txt` §8 says "Managing Director and CTO". Also `llms-full.txt` describes TaskEdge as "operations task management SaaS" while index FAQ calls it "AI-powered business operating system". Reconcile to a single phrasing set; keep `llms-full.txt` §8 byte-identical to the on-page FAQ HTML. | 🟠 |
| 1.3 | **`SoftwareApplication` nodes on index duplicate per-page nodes with different descriptions** | `index.html` `#software` graph describes iCare as *"HealthApplication… deployed across state hospital networks"*, but `icare.html` has its own richer node. Cross-reference instead of duplicating: point index nodes at the canonical page node via `@id` (`https://praveshsingh.com/icare.html#software`) — the index already does this for `@id`s but the descriptions differ, which parsers treat as conflicting claims. | 🟡 |
| 1.4 | **`sameAs` too thin** | Only LinkedIn + SoftEdge site. Add any verifiable profiles: GitHub, X/Twitter, Google Scholar/ResearchGate (if any), Crunchbase, conference speaker pages (BFUHS/NHM Punjab event pages), LinkedIn company page for SoftEdge. Every additional `sameAs` edge strengthens the Knowledge Panel and LLM entity merge. | 🟠 |
| 1.5 | **Person node missing identity facts** | Add: `knowsLanguage: ["en", "hi", "pa"]`, `address` (PostalAddress: Mohali, Punjab, IN), `nationality: IN`, `email: hello@praveshsingh.com`, `alumniOf`, `hasCredential`/`hasOccupation`. LLMs answer "where is Pravesh Singh based?" from these; today the answer only exists in prose. | 🟠 |
| 1.6 | **No `Organization` logo anywhere** | `grep logo` → 0 matches. Add an `ImageObject` logo (min 112×112px, square, on white/dark-safe background) to the SoftEdge `Organization` node on every page, plus a favicon file (`/favicon.ico` + `apple-touch-icon.png`) — currently only an inline SVG data-URI favicon, which Bing and several AI indexers don't process. | 🟠 |

---

## 2. On-Page SEO (Classic) 🟡

| # | Finding | Evidence | Fix |
|---|---------|----------|-----|
| 2.1 | **`<meta name="keywords">` still present on every page** | Dead weight since 2009; some spam-scoring models still weight it slightly negative. Remove globally. | 🟡 |
| 2.2 | **Title tag length at the edge** | `icare.html` = 80 chars, `taskedge.html` = 81 chars — will truncate (~580px) and push the brand off SERP display. Move the brand to the front or trim: *"iCare – Patient Registry & Cold-Chain Inventory Case Study \| Pravesh Singh"* is still long; consider dropping the pipe-brand and relying on site name in Google's title rewriting. | 🟡 |
| 2.3 | **H1 on `index.html` is generic-brandable, not keyword-anchored** | *"Building intelligent software products that solve real business problems."* — zero entity terms. The `<title>` carries "Pravesh Singh" but the H1 doesn't. Recommend: *"Pravesh Singh — Founder & CTO building AI platforms, healthcare software & multi-tenant SaaS."* Keep visual styling; change the words. | 🟠 |
| 2.4 | **Section H2s are good; event H3s lack date strings in heading text** — fine, they're in `.event-location-date`. No action. | — | ✅ |
| 2.5 | **No breadcrumbs visible on main pages' HTML** (JSON-LD BreadcrumbList exists on all pages ✅, but no visible breadcrumb UI outside writing pages). Visible breadcrumbs reinforce the JSON-LD. Low priority. | 🟡 |
| 2.6 | **Image assets unoptimized** | `images/pravesh-singh.png` is **2.05 MB** (webp twin exists at 126 KB and is served via `<picture>` ✅). Strip/scale the PNG (it's still downloaded by non-WebP crawlers + used as OG image). Regenerate a dedicated 1200×630 OG image instead of the 1102×1427 portrait — portrait crops badly in link previews and AI image cards. | 🟠 |
| 2.7 | **Event/gallery images lack `width`/`height` attributes** → CLS. `event-media img`, `thumb-btn img`, `screenshot-frame img` have no intrinsic dimensions. Add them. | 🟡 |

---

## 3. Structured Data (Schema.org) — Rich-Result Eligibility 🟠

| # | Finding | Evidence | Fix |
|---|---------|----------|-----|
| 3.1 | **`Article` nodes missing `image` and `publisher.logo`** | Every writing article's `Article` node has no `image` and the `publisher` Organization has no `logo`. Google requires `image` for Top Stories/article rich results; LLM crawlers use it for card rendering. Add `image` (1200×630 per-article OG image) + `logo`. | 🔴 |
| 3.2 | **`article:modified_time` missing on article pages** | Only `article:published_time` is present (template `writing/_template.html` line ~46) yet `dateModified` exists in JSON-LD. Add `article:modified_time` to the template. | 🟡 |
| 3.3 | **`writing/index.html` ItemList lacks dates and authors** | CollectionPage + ItemList with 8 ListItems but no `datePublished`/`url` enrichment per item — add `datePublished` so freshness is machine-readable at hub level. | 🟡 |
| 3.4 | **FAQPage only on 2 of 13 pages** | Present on `index.html` and `expertise.html` ✅ — but no visible FAQ sections on `icare.html`, `taskedge.html`, `automation.html`, `about.html`. Per Google's current guidance, FAQ rich results are limited to well-known authoritative government/health sites, so the *SERP* value is low now — but the **AEO value is not**: FAQ blocks are the #1 extractable passage format for Perplexity/Copilot/Gemini citations. Add 4–6 question/answer pairs per product page (visible HTML + mirrored JSON-LD). | 🔴 |
| 3.5 | **No `Service`+`Offer` on expertise pricing in visible HTML parity** — expertise.html has `OfferCatalog`/`Offer`/`Service` ✅ (good). Keep prices-with-currency in `Offer.priceSpecification` if you add public pricing. | ✅ |
| 3.6 | **`industries.html` is schema-thin** | Only a bare `WebPage`. Add `Service` nodes per industry vertical or at least `WebPage` + `about`/`mentions` edges to the Person. | 🟡 |
| 3.7 | **No `Event` markup for the 4 talks** | These are verifiable, dated, located public events — perfect E-E-A-T anchors. Add `Event` nodes (type `Event`/`EducationalEvent`, `startDate`, `location`, `performer` → Person) on `index.html#events`. Strongly boosts "has this person really done this?" verification by LLMs. | 🟠 |
| 3.8 | **Speaking → `roleName` unused**: add `Role`s or `PerformingRole` under Person for "Guest of Honour/Speaker" claims instead of free-text `award` strings. | 🟡 |
| 3.9 | **`ProfilePage` on subpages is redundant** — `icare.html` etc. use `ProfilePage` as the page type; they're case studies, not profiles. Use `WebPage`/`AboutPage` + `mainEntity` referencing the Product/SoftwareApplication. Minor but removes parser confusion. | 🟡 |

---

## 4. GEO / AIO — Generative Engine Optimization (the biggest lever) 🔴

*This is where the site wins or loses citations in ChatGPT Search, Perplexity, Gemini, Copilot and Google AI Overviews.*

| # | Finding | Evidence | Fix |
|---|---------|----------|-----|
| 4.1 | **No extractable "answer blocks" in articles** | Articles are continuous prose (~850–940 words). No TL;DR, no "Key takeaways", no Q&A subsections. Generative engines lift *self-contained 40–80 word passages*. Add a **"TL;DR" callout box (60–80 words, factual, quotable)** directly under every article H1, plus a **"Key takeaways" list** at the end. | 🔴 |
| 4.2 | **No in-page anchors (jump links)** | `grep id=` on essays → only `hamburgerBtn`/`mobileMenu`. H2s have no IDs → no deep-linking, no passage-level citation anchoring. Add `id` slugs to every H2/H3 and a small "On this page" TOC on each article. Perplexity cites passage anchors; without IDs it cites the whole page. | 🔴 |
| 4.3 | **Zero outbound citations to primary sources** | ABDM guide cites no `cebpb.nha.gov.in`/NHA sandbox docs; PostgreSQL article cites no postgresql.org RLS docs; DPDP checklist doesn't link the MeitY Act PDF. GEO systems weight claims backed by primary sources and it's your single strongest E-E-A-T signal for YMYL-adjacent health-tech content. Add 3–6 authoritative outbound links per essay. | 🔴 |
| 4.4 | **No Article→Article cross-links** | `writing/offline-tolerant-hospital-software.html` links only back to `index.html` (4×). Topic-cluster interlinking ("Related reading" footer on every essay) increases crawl depth and topical authority; currently the cluster is a star with no edges between spokes. | 🔴 |
| 4.5 | **No RSS/Atom feed** | No feed anywhere. Feeds are consumed by AI aggregators, newsletter tools, and Perplexity's discovery layer. Add `/writing/feed.xml` (Atom), link it in `<head>` (`<link rel="alternate" type="application/atom+xml">`) and from the writing hub. | 🟠 |
| 4.6 | **`llms-full.txt` lacks per-essay extract blocks** | It has abstracts ✅ but not the *actual key claims*. Consider appending a "Key claims & facts" section per essay (5–8 bullet facts with numbers, e.g. "sub-50ms task updates", ">99.4% field precision", "FEFO allocation with FOR UPDATE SKIP LOCKED") — these exact strings are what LLMs quote. | 🟠 |
| 4.7 | **Freshness signals are static** | All `lastmod` dates in `sitemap.xml` are the same 2026-09-21; `changefreq weekly` on static pages is noise. Make `lastmod` per-page-true (Git commit date per file is fine), or drop `changefreq` entirely (Google ignores it). | 🟡 |
| 4.8 | **"Statistics proof strip" is visual-only** | The `facts-strip` (15+ years, Punjab & MP, sub-50ms, >99.4%) is HTML but not machine-attributed. Numbers in JSON-LD (`SoftwareApplication.featureList`, or a `Dataset`/`claim` in the Person node) are far more quotable. Mirror key stats into `llms.txt` §1 (partially there) and into each product page's FAQ answers. | 🟠 |

---

## 5. AEO — Answer-Engine Readiness (Q&A surfaces) 🟠

| # | Finding | Evidence | Fix |
|---|---------|----------|-----|
| 5.1 | **FAQ accordions render closed with `max-height:0`** — content is in DOM (crawlable ✅) but the *first* FAQ row only is `open` by default. Fine. However `toggleFaq` collapses siblings; if you add FAQ to product pages, keep answers in DOM at all times (they are — good). | ✅ |
| 5.2 | **Question phrasing not query-shaped** | Questions like *"What government workshops and technical keynotes has Pravesh delivered?"* are good; add comparison/decision queries buyers actually ask: *"How much does a fractional CTO cost in India?"*, *"Schema-per-tenant vs RLS: which should I choose?"*, *"How do I make a hospital app ABDM compliant?"* — these map to real Perplexity/AI-Overview prompts and to commercial intent. | 🟠 |
| 5.3 | **No HowTo/step surfaces** — the DPDP checklist and ABDM guide are naturally step-formatted; the checklist is prose. Convert the DPDP 10-point checklist into a real `<ol>` with anchored steps (also earns `HowTo`-style passage extraction even though Google dropped HowTo rich results). | 🟠 |
| 5.4 | **`llms.txt` doesn't link `expertise.md`** | `expertise.md` exists (5.8 KB markdown twin ✅, linked from `index.html`/`expertise.html` heads ✅) but is absent from `llms.txt` §Site Structure and `llms-full.txt` §9. Add it — markdown twins are the single highest-consumption format for LLM agents. | 🟠 |
| 5.5 | **No per-article markdown twins** — same pattern as `expertise.md` would make each essay directly ingestible; even an auto-generated pandoc/markdown export per essay is high-value for a static site. | 🟡 |

---

## 6. Technical Infrastructure 🔴 (silent killers)

| # | Finding | Evidence | Fix |
|---|---------|----------|-----|
| 6.1 | **Soft-404: `ErrorDocument 404 /index.html`** returns HTTP 200 with homepage content for *any* bad URL. This is the highest-risk issue in the repo: it dilutes crawl budget, floods GSC with "Duplicate without canonical"/soft-404 flags, and can serve the homepage as the canonical answer for garbage URLs to LLM crawlers. Replace with a real `404.html` (still branded, links to hub pages, `meta robots noindex`) or serve 410 for removed content. | 🔴 |
| 6.2 | **`/writing/` directory request → 301 to homepage** (`.htaccess` rule 3 matches `/images/` only; but `DirectoryIndex` serves `writing/index.html` fine — verify). More importantly, **directory URL trailing-slash canonicalization**: `/writing` vs `/writing/` — Apache will redirect, confirm it lands on `/writing/` (or better, `/writing.html`-style canonical). Add a rewrite for `/writing` → `/writing/` explicitly. | 🟡 |
| 6.3 | **`build/` directory is deploy-litter** | `build/` mirrors the whole site (with same sitemap) — if it ships to the web root, `https://praveshsingh.com/build/index.html` creates a full duplicate site. Add `Disallow: /build/` to robots.txt **and** exclude it from deployment (or `noindex` header via `.htaccess` `<FilesMatch>`/`RedirectMatch 404 ^/build/`). | 🔴 |
| 6.4 | **GTM + gtag.js double-loading** | Every page loads **both** `GTM-M335RXDF` (in `<head>`) *and* standalone `gtag.js` `G-2XHZ5NJZLK`. If the GA4 tag is inside the GTM container, this double-counts pageviews and inflates bounce-fix metrics. Load GA4 *either* via GTM *or* standalone — remove the duplicate. (Found in `index.html` lines ~1276–1290 and every page/template.) | 🟠 |
| 6.5 | **No AI-crawler hit measurement** | robots.txt allowlists 19 AI bots but you can't see their traffic. Options: (a) pipe Apache access logs into a weekly script grepping GPTBot/ClaudeBot/PerplexityBot user agents; (b) server-side log analytics (GoAccess); (c) at minimum, GSC → Settings → Crawler reports + Cloudflare Workers "AI Crawl Control" style firewall logs if behind CF. Without this, GEO effort is unmeasurable. | 🔴 |
| 6.6 | **Missing `hreflang`** — `lang="en-IN"` is declared but no `hreflang`. Single-language site: *not required*, skip. But then remove the misleading `en-IN` vs `en_IN` inconsistency risk by keeping both HTML `lang` and `og:locale` aligned (they currently are ✅). | ✅ |
| 6.7 | **Missing security/CSP headers** — `.htaccess` has `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy` ✅ but **no CSP** and no `Strict-Transport-Security` (HSTS). Add `Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"` + a conservative `Content-Security-Policy` (report-only first). Also worth adding `X-Robots-Tag` for `/build/` if kept. | 🟡 |
| 6.8 | **`sitemap.xml` missing `xhtml:link` hreflang (N/A) but missing `<image:image>` extensions for showcase images** — optional; images drive Google Images traffic for the event photos (rankable, named entities: "Pravesh Singh NHM Punjab workshop"). Consider an image sitemap extension. | 🟡 |
| 6.9 | **`yandex_*.html` verification file** — fine; keep. Consider adding Bing (IndexNow) — **IndexNow key file is absent**; instant indexing for a static site is one file + a ping. Low effort, real freshness signal. | 🟠 |

---

## 7. Content Strategy Gaps (what AI engines can't currently quote you for)

| # | Gap | Why it matters | Suggested asset |
|---|-----|----------------|-----------------|
| 7.1 | **No pricing anchor** | "How much does an ABDM integration sprint cost?" — you'll never be cited without a public number. Even "from ₹X / fixed-scope" in FAQ + `Offer` schema. | FAQ + Offer schema 🟠 |
| 7.2 | **No case-study numbers in extractable form** | "iCare tracks how many patients?" — no public counts (patients, vials/month, hospitals, uptime). One verified stat line per product page would make it the *only citable source* for that claim. | icare/taskedge FAQ 🟠 |
| 7.3 | **Comparison pages missing** | "iCare vs generic EMR", "schema-per-tenant vs RLS: decision table". Comparison queries dominate AI Overview citations. The PostgreSQL essay *is* this — surface a decision table at its top. | Table in essay 🟠 |
| 7.4 | **Glossary pages** — "What is FEFO in pharma logistics?", "ABDM M1 vs M2 vs M3" — definitional queries are the #1 AEO citation format and you have the authority to own them. | 🟡 |
| 7.5 | **Author page → paper trail**: the Person entity would benefit from a `/speaking` or expanded about page listing each talk with date, venue, audience size, and *external* links (event programs, news mentions). LLMs verify claims cross-source; right now all 4 events are self-attested only. | 🟠 |

---

## 8. Prioritized Roadmap

### Sprint 1 — Stop the bleeding (1–2 days)
1. Fix soft-404 (`404.html`, §6.1) 🔴
2. Block/redirect `/build/` + robots.txt (§6.3) 🔴
3. Remove duplicate GA4/GTM load (§6.4) 🟠
4. Fix entity drift: one role string everywhere; sync FAQ text between HTML, JSON-LD, llms.txt (§1.1–1.2) 🟠
5. Remove `meta keywords` (§2.1) 🟡

### Sprint 2 — GEO content surfaces (3–5 days)
6. TL;DR + Key-takeaways blocks on all 6 essays (§4.1) 🔴
7. Heading anchors + per-article "On this page" TOC (§4.2) 🔴
8. 3–6 outbound primary-source citations per essay (§4.3) 🔴
9. "Related reading" cross-links between essays (§4.4) 🔴
10. Atom feed + `<link rel="alternate">` (§4.5) 🟠
11. Update `llms-full.txt` with per-essay key claims; add `expertise.md` to llms.txt (§4.6, §5.4) 🟠

### Sprint 3 — Schema & rich results (2–3 days)
12. `Article.image` + `publisher.logo` on all essays (§3.1) 🔴
13. Per-product visible FAQ sections + FAQPage JSON-LD (§3.4) 🔴
14. `Event` nodes for the 4 talks (§3.7) 🟠
15. Person node enrichment: `knowsLanguage`, `address`, `nationality`, extra `sameAs` (§1.4–1.5) 🟠
16. OG image redesign: 1200×630 per page-type; compress hero PNG (§2.6) 🟠

### Sprint 4 — Measurement & freshness (ongoing)
17. AI-crawler log monitoring (§6.5) 🔴
18. IndexNow key + ping on publish (§6.9) 🟠
19. True per-page `lastmod`; drop `changefreq` (§4.7) 🟡
20. HSTS + CSP report-only (§6.7) 🟡

---

## 9. What's Already Excellent (don't touch)

- ✅ `llms.txt` + `llms-full.txt` with clean structure, endpoints section, and FAQs — top 1% of sites
- ✅ Explicit AI-crawler allowlist in robots.txt with documented intent
- ✅ JSON-LD `@graph` with stable `@id`s and cross-references on every page
- ✅ BreadcrumbList on every page incl. essays
- ✅ FAQPage with visible HTML parity on index & expertise
- ✅ `.htaccess` canonicalization (https, non-www, /index.html strip)
- ✅ `security.txt` (RFC 9116) + yandex verification
- ✅ `expertise.md` markdown twin pattern
- ✅ WebP `<picture>` with PNG fallback, `fetchpriority="high"` on hero, lazy-loading below fold
- ✅ Semantic `aria-labelledby` sections, single H1 per page, alt text on all images
- ✅ GTM noscript fallback, event tracking architecture

---

*Generated by audit of the repository source on 2026-09-23. Line references approximate; verify in current files before editing.*

---

## 10. Implementation Log — 2026-09-23

**Status: Implemented (Sprints 1–4).** All changes verified: every JSON-LD block parses, Atom feed and sitemap are well-formed XML, build mirror resynced.

| Fix | Audit ref | Files touched | Status |
|---|---|---|---|
| Real 404 page (HTTP 404 + noindex, recovery links) | §6.1 | `404.html` (new), `.htaccess` (`ErrorDocument 404 /404.html`) | ✅ |
| `/build/` hard block (404 rewrite + `X-Robots-Tag` + robots Disallow) | §6.3 | `.htaccess`, `robots.txt` | ✅ |
| GA4/GTM dedupe — kept gtag.js (tracker depends on `gtag()`), removed GTM container + noscript from all 16 pages | §6.4 | all `*.html` | ✅ |
| Entity role strings unified ("Founder & CTO") in titles/OG/Twitter | §1.1 | `index.html` | ✅ |
| FAQ entity answer synced to llms-full.txt wording (MD & CTO) | §1.2 | `index.html`, `llms-full.txt` | ✅ |
| Hero H1 rewritten with entity + keywords | §2.3 | `index.html` | ✅ |
| `<meta keywords>` removed | §2.1 | all 16 pages | ✅ |
| TL;DR callouts (quotable 60–80 word answers) | §4.1 | 6 essays | ✅ |
| Heading anchors (`id=`) + "On this page" TOC | §4.2 | 6 essays | ✅ |
| References — primary-source outbound links (ABDM sandbox, NHA PDFs, NRCeS FHIR, PostgreSQL docs, MeitY DPDP, Pydantic, WHO) | §4.3 | 6 essays | ✅ |
| Related reading — essay↔essay cross-links | §4.4 | 6 essays | ✅ |
| Atom feed + `<link rel="alternate">` on all pages | §4.5 | `writing/feed.xml` (new), 14 pages | ✅ |
| llms.txt: feed + expertise.md + sitemap endpoints, verified-facts block | §4.6, §5.4 | `llms.txt`, `llms-full.txt` (§8b key claims) | ✅ |
| `Article.image` + `publisher.logo` in essay JSON-LD | §3.1 | 6 essays | ✅ |
| `article:modified_time` meta | §3.2 | 6 essays | ✅ |
| `ItemList` `datePublished` per essay | §3.3 | `writing/index.html` | ✅ |
| Visible FAQ sections + FAQPage JSON-LD on product pages | §3.4, §7.2 | `icare.html`, `taskedge.html`, `automation.html` (5 Q&As each) | ✅ |
| `Event` nodes ×4 (Bhopal, Chandigarh, Faridkot, PSACS) | §3.7 | `index.html` JSON-LD | ✅ |
| Person enrichment: `email`, `nationality`, `address`, `knowsLanguage`, extra `sameAs` | §1.4–1.5 | `index.html` JSON-LD | ✅ |
| Organization `logo` (512×512) in JSON-LD | §1.6 | `index.html`, 6 essays | ✅ |
| Brand assets: `logo.png`, `favicon.ico` (16/32/48), `apple-touch-icon.png`, `og-default.png` 1200×630 | §1.6, §2.6 | `images/*` (new), favicon links on all pages, `tools/generate_brand_assets.py` | ✅ |
| OG image swapped to 1200×630 card on all pages | §2.6 | all pages | ✅ |
| Title trims (80→77, 81→63 chars) | §2.2 | `icare.html`, `taskedge.html` | ✅ |
| HSTS + CSP report-only headers | §6.7 | `.htaccess` | ✅ |
| IndexNow key file | §6.9 | `8f4a2c19e7b34d5680f1ae92c7b5d316.txt` (new) | ✅ |
| True per-page `lastmod`; `changefreq` removed | §4.7 | `sitemap.xml` | ✅ |
| Build mirror resync (excludes repo-only files) | §6.3 | `tools/sync_build.sh` (new), `build/` | ✅ |

### Post-deploy checklist (requires hosting access)

1. **Deploy the repo root, never `build/`** — the web server now 404s `/build/`, but don't ship the mirror.
2. **Verify headers:** `curl -I https://praveshsingh.com/` → confirm `Strict-Transport-Security`, `X-Robots-Tag` absent on normal pages, 404 on `/build/index.html` and any garbage URL (real 404, not 200).
3. **CSP:** run report-only for 2–4 weeks (`Content-Security-Policy-Report-Only` is set), then flip to enforcing `Content-Security-Policy` once no violations appear.
4. **AI-crawler measurement (§6.5):** add log-based monitoring — e.g. weekly `grep -cE "GPTBot\|ClaudeBot\|PerplexityBot" access.log` or GoAccess; without this GEO progress is invisible.
5. **IndexNow ping after deploy:** `curl "https://api.indexnow.org/indexnow?url=https://praveshsingh.com/&key=8f4a2c19e7b34d5680f1ae92c7b5d316"` (and once per changed URL).
6. **Portrait PNG (§2.6):** `images/pravesh-singh.png` is still 2 MB (it's your photo — left untouched). Recommended: re-export at 1102px width with squoosh/TinyPNG (target <300 KB); WebP twin already serves most browsers.
7. **Validate rich results:** Google Rich Results Test on `/`, `/icare.html`, one essay; Schema.org validator sitewide.
8. **`sameAs` (§1.4):** add GitHub/X/Crunchbase profiles if/when they exist — entity edges only help if they resolve.

### Not implemented (deliberate)

- §7 content strategy assets (pricing anchors, glossary pages, comparison tables beyond the existing decision matrix) — new content, requires your input on public numbers.
- §2.7 CLS `width/height` on every gallery `<img>` — mechanical, low-impact; fold into the next content update.
- §5.5 per-article markdown twins — recommend generating from the TL;DR + TOC structure in a future pass.
