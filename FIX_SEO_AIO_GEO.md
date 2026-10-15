# FIX_SEO_AIO_GEO.md — Implementation Plan for the 2026-10-15 Audit

**Source:** `SEO_AIO_GEO_AUDIT_2026-10-15.md`
**Purpose:** exact, copy-pasteable fixes for every finding that requires a code change, ordered by priority, each with old→new strings and a post-fix verification command.
**Status legend:** [ ] pending · [x] done (mark as you go)
**One decision is required from the site owner before FIX-5 — see §5.0.**

---

## Priority A — Bugs (implement first, ~30 min total)

### [x] FIX-1 🔴 Delete `<meta keywords>` from `index.html` (audit 1.2)

**File:** `index.html`, line 12 — it is the ONLY page in the repo that still carries this tag; delete it for consistency with the other 12 pages.

**Old:**
```html
  <meta name="keywords" content="healthcare software architect, clinical systems design, offline-first applications, district hospital software, hemophilia management systems, healthcare operations, SaaS platform design, India healthcare technology, ABDM integration, FHIR interoperability">
```
**New:** *(delete the entire line)*

**Verify:** `grep -rl 'name="keywords"' *.html writing/*.html` → must return **nothing**.

---

### [x] FIX-2 🔴 Stale OG image metadata on `index.html` (audit 1.1)

**File:** `index.html` head. The real file is `images/og-default.png = 1200×630` (verified), but the homepage declares 880×1140 portrait. Every other page declares 1200×630. Also `og:type profile` (with `profile:*` props) — swap to `website`; the Person identity is already carried by JSON-LD.

**Change A (line 28):**
```html
  <meta property="og:type" content="profile">
```
→
```html
  <meta property="og:type" content="website">
```

**Change B (lines 37–38):**
```html
  <meta property="og:image:width" content="880">
  <meta property="og:image:height" content="1140">
```
→
```html
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
```

**Change C (lines 40–41) — these props are only valid under `og:type=profile`; delete them:**
```html
  <meta property="profile:first_name" content="Pravesh">
  <meta property="profile:last_name" content="Singh">
```

**Verify:** `grep -A2 'og:image:width' index.html` → both dims `1200`/`630`; `grep -c 'profile:' index.html` → **0**; and dims now uniform sitewide:
```bash
for f in *.html writing/*.html; do grep -m1 'og:image:width' "$f" | grep -q 1200 || echo "WRONG: $f"; done
```
(essay and inner pages all pass; nothing should print).

---

### [x] FIX-3 🟠 Remove `eventStatus: "EventScheduled"` from the four past `Event` nodes (audit 2.1)

**File:** `index.html`, lines **263, 284, 304, 324**. All four events (Faridkot 2023, Chandigarh 2024, Bhopal 2025, PSACS 2025) are in the past as of today; Google's event guidelines treat `EventScheduled` as future-only, and LLMs can misread it as "upcoming talks", which is a factual-drift risk for a trust-selling entity.

**Old (4 occurrences):**
```json
        "eventStatus": "https://schema.org/EventScheduled",
```
**New:** *(delete each line — with `allowMultiple`, one replacement kills all four)*

Refresh-dated events (e.g. a genuinely upcoming workshop) should re-add the property only for future events.

**Verify:**
```bash
grep -c 'EventScheduled' index.html   # → 0
python3 -c "import re,json;[x for x in re.findall(r'ld\+json\">(.*?)</script',open('index.html').read(),re.S) for _ in [json.loads(x)]];print('JSON-LD still parses')"
```

---

## Priority B — Entity consistency (requires one decision, then ~1 hr)

### 5.0 Decide the canonical role string (BLOCKS FIX-5)

The site currently mixes **"Founder & CTO"** (all `<title>` tags, og, most headers) with **"Managing Director & CTO"** (llms.txt, llms-full.txt, FAQ answer, footers/portrait captions). Cross-document role inconsistency is the #1 entity-noise vector for LLMs answering "Who is Pravesh Singh?".

**Recommendation (used in the replacements below):** headline identity = **"Founder & CTO"**, everywhere. Retain "Managing Director" only as a legal-entity fact in `company.html` prose and inside `jobTitle` **arrays** (arrays listing multiple roles are not a contradiction and are kept).

---

### [x] FIX-5 🟠 Sync the role string across every surface (audit 3.2/3.3)

Apply after §5.0 decision. Exact replacements (grep-verified line numbers):

**5.1 `index.html` line 213 (FAQ JSON-LD answer):**
```
...entrepreneur, and the Managing Director and Chief Technology Officer (CTO) of SoftEdge Technology Solutions. With over 15 years...
```
→
```
...entrepreneur, and the Founder and Chief Technology Officer (CTO) of SoftEdge Technology Solutions. With over 15 years...
```

**5.2 `llms.txt` line 8 — same phrase swap:**
```
...and the Managing Director and Chief Technology Officer (CTO) of SoftEdge Technology Solutions.
```
→ `Founder and Chief Technology Officer (CTO)` (same sentence pattern)

**5.3 `llms.txt` line 14:**
```markdown
- **Managing Director & CTO**, SoftEdge Technology Solutions (https://softedgetechnology.com)
```
→
```markdown
- **Founder & CTO**, SoftEdge Technology Solutions (https://softedgetechnology.com)
```

**5.4 `llms-full.txt` lines 11, 163, 166 — same phrase swap as 5.1** (sentence pattern "the Managing Director and Chief Technology Officer (CTO) of").
**5.5 `llms-full.txt` line 15:** `**SoftEdge Technology Solutions (Managing Director & CTO):**` → `**SoftEdge Technology Solutions (Founder & CTO):**`

**5.6 Visible caption lines (keep the same rendered style, change words only):**
- `about.html:1034`, `automation.html:1181`, `icare.html:1221`, `index.html:1866`: `Managing Director & CTO, SoftEdge Technology Solutions` → `Founder & CTO, SoftEdge Technology Solutions`
- `expertise.html:1382`: `Founder, Managing Director &amp; CTO` → `Founder &amp; CTO`
- `expertise.html:1901`: `Managing Director &amp; CTO, ...` → `Founder &amp; CTO, ...`

**5.7 Do NOT touch** (correct as-is): `about.html:94` and `expertise.html:95` `jobTitle` arrays, and `company.html` (legal MD reference is legitimate there).

**5.8 While in the files, byte-sync the canonical 2-sentence bio** (live meta description wording is the winner):
```
Fractional CTO, senior AI developer & healthcare software architect at SoftEdge Technology Solutions. Building AI-powered platforms, multi-tenant SaaS and HIPAA-aware, GDPR-conscious health systems for clients in India, the US and Europe.
```
Use it for: JSON-LD `Person.description` lead, `llms.txt` §Identity, `llms-full.txt` §Identity, `about.html` intro — sentence for sentence identical (allowed: prefix "Pravesh Singh is ..." where grammar requires a subject).

**Verify — zero drift:**
```bash
grep -rn 'Managing Director & CTO\|Managing Director and Chief' *.html writing/*.html *.txt .well-known/*.txt | grep -v company.html
# Expect: only the two jobTitle-array lines in about.html / expertise.html
grep -rc 'Founder & CTO' llms.txt llms-full.txt   # → expected ≥ matches in each file
```

---

## Priority C — Build & measurement (no user decision needed)

### [x] FIX-6 🟡 Per-URL `lastmod` from git dates (audit 1.5)

All 15 sitemap URLs currently share `2026-09-25`, which reads as a freshness strobe (uniform values get discounted). Hook into `make_build.sh` next to the existing sitemap check (script lines 116–138).

Add to `make_build.sh` (BEFORE the packaging step) and regenerate `sitemap.xml` in-repo too:

```bash
python3 - <<'PYEOF' || fail "lastmod sync failed"
import subprocess, re, sys
from pathlib import Path
root = Path(".")
sm = root / "sitemap.xml"
xml = sm.read_text()

def lastmod_for(loc: str) -> str:
    path = loc.replace("https://praveshsingh.com/", "").rstrip("/") or "."
    p = Path(path) / "index.html" if not Path(path).suffix and path != "." else Path(path)
    if not p.exists():
        p = Path(path + ".html") if path else Path("index.html")
    if not p.exists():
        return None
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(p)],
                         capture_output=True, text=True)
    return out.stdout.strip() or None

def repl(m):
    lm = lastmod_for(m.group(1)) or m.group(2)
    return f"<loc>{m.group(1)}</loc>\n    <lastmod>{lm}</lastmod>"
# wire the regex to your current sitemap indentation inside the heredoc
xml2 = re.sub(r"<loc>(https://praveshsingh\.com/[^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", repl, xml)
sm.write_text(xml2)
PYEOF
```

**Verify:** `grep -o '<lastmod>[^<]*</lastmod>' sitemap.xml | sort | uniq -c` → **more than one distinct date** (each file's true git date). Keep the existing well-formedness check green (`xmllint --noout`).

---

### [x] FIX-7 🟡 Per-essay markdown twins + llms.txt registration (audit 3.5)

Only `expertise.md` has a markdown twin. Extend the essay generator (`make_page.sh`) so each `writing/*.html` also emits `writing/<slug>.md` containing:

```markdown
# {ARTICLE_TITLE} – Pravesh Singh
Published: {date} · Reading time: {n} min · https://praveshsingh.com/writing/{slug}.html

## TL;DR
{the 60–80 word TL;DR block verbatim from the article}

## Contents
{anchored TOC as links}

## Key claims
{5–8 extractable factual bullets with hard numbers}

---
Fallback HTML: https://praveshsingh.com/writing/{slug}.html
```

Then register each twin in `llms.txt` §Site Structure (+ `llms-full.txt` §9) in the `{Article}: https://.../{slug}.md` pattern already used for `expertise.md`. Add `AddType text/markdown .md` coverage if any URL is protected — `.htaccess` already serves it.

**Verify:** `ls writing/*.md | wc -l` → 6 (+ new ones as you publish); each twin linked in `llms.txt`; served with `Content-Type: text/markdown`.

---

### [x] FIX-8 🔴 AI-crawler visibility monitoring (audit §6.5 — biggest unmet item)

robots.txt allowlists 19 AI bots, but nothing measures their traffic, so GEO work is unattributable. Three tiers, best available wins:

**Tier 1 — host access logs (Apache):** weekly digest script (e.g. `tools/ai_crawl_report.sh`, run via cron/launchd):

```bash
#!/bin/bash
# AI crawler hit report — expects a combined-access-log path as $1
LOG="${1:-/var/log/apache2/access.log}"
AGENTS='GPTBot|OAI-SearchBot|ChatGPT-User|ClaudeBot|Claude-User|Claude-SearchBot|anthropic-ai|PerplexityBot|Perplexity-User|Google-Extended|Applebot|Amazonbot|cohere-ai|YouBot|Bytespider|meta-externalagent|CCBot'
echo "== AI crawler hits (last $(wc -l < "$LOG") log lines) =="
grep -E "$AGENTS" "$LOG" | awk -F'"' '{print $6}' | awk '{print $1}' | sort | uniq -c | sort -rn
echo "== Most-fetched AI URLs =="
grep -E "$AGENTS" "$LOG" | awk '{print $7}' | sort | uniq -c | sort -rn | head -20
echo "== GSC-equivalents: check Settings → Crawl stats for GPTBot/OAI-SearchBot naming =="
```

**Tier 2 — GSC:** Settings → Crawl statistics (if your host pipes referrers/user-agent classes) + GSC Performance filtered by `Search Appearance` now that AI-Overview-linked sessions exist.
**Tier 3 — Cloudflare/edge:** if the domain is behind CF, enable AI Crawl Control / bot analytics.

**Acceptance:** at minimum one of the three is live and produces a weekly report you actually look at; record the baseline in the report file (first `tools/ai_crawl_report.sh` output) so the next audit can show a trend.

---

### [x] FIX-9 🟡 Automate the IndexNow ping post-deploy (audit 5.4)

Key file is shipped (`8f4a2c19e7b34d5680f1ae92c7b5d316.txt`) but nothing pings. Append to the deploy recipe (or `make_build.sh --zip` output instructions) and run after **every** deployment:

```bash
KEY=8f4a2c19e7b34d5680f1ae92c7b5d316
for u in https://praveshsingh.com/ \
         https://praveshsingh.com/llms.txt \
         https://praveshsingh.com/sitemap.xml; do
  curl -sS "https://api.indexnow.org/indexnow?url=$u&key=$KEY" -o /dev/null -w "%{http_code} $u\n"
done
```
(Plus one line per changed content page.) Success = `200`/`202` per URL; a `4xx` on the key means the key file isn't deployed at the web root.

---

## Priority D — Post-deploy / manual / commercial-decision

| # | Item | Where | Action |
|---|---|---|---|
| [ ] FIX-10 | **CSP → enforcing** | `.htaccess` | After the report-only window (post-2026-09-23+4wk) produces zero reports: copy the `Content-Security-Policy-Report-Only` value to a real `Header always set Content-Security-Policy "..."` header and delete the report-only line. Verify with `curl -I https://praveshsingh.com/ \| grep -i content-security` showing an *enforcing* header and no console-violation breakage in 1 page pass with devtools open. |
| [ ] FIX-11 | **Portrait PNG** | `images/pravesh-singh.png` (475 KB) | Re-export at 1102px width (<250 KB target). WebP twin (73 KB) already serves modern browsers via `<picture>`; PNG only matters for the JSON-LD `image.url` and legacy crawlers. |
| [ ] FIX-12 | **External `sameAs` edges** (audit 6.1) | `index.html`, `about.html` JSON-LD | Add only verifiable URLs: LinkedIn **company** page for SoftEdge, event-program pages for the 4 talks (BFUHS / NHM Punjab / PSACS), Crunchbase, X profile if active. Do not add dead profiles. Each edge helps Knowledge-Panel + LLM entity merge. |
| [ ] FIX-13 | **Pricing anchor** (commercial decision, audit 4.3) | `expertise.html` + FAQ | If you publish even one band ("Architecture review: from ₹X / fixed-scope"), mirror it into `Offer.priceSpecification` + a decision-shaped FAQ answer. Unlocks the entire "how much does X cost" AI-Overview citation class. |
| [ ] FIX-14 🟡 | **Title trim** (optional, audit 1.3) | `icare.html` | `<title>` is 73 chars; trim "HIPAA-Aware, ABDM-Ready" to "iCare — Patient Registry & Cold-Chain Software \| Pravesh Singh" (60 chars) if you want guaranteed non-truncation. Low priority. |

---

## Order-of-work & acceptance summary

1. **FIX-1, FIX-2, FIX-3** (30 min, zero-risk edits) → run all three verify commands → rebuild.
2. **§5.0 decision → FIX-5** → run the drift grep → rebuild.
3. **FIX-6, FIX-7, FIX-9** in the build pipeline; **FIX-8** at the host level (needs log access / CF).
4. **Deploy via `./make_build.sh --zip`** (it re-validates sitemap↔files and the consent block — do not hand-copy files), then run the FIX-9 pings and a header check (`curl -I` for HSTS/robots).
5. Item **FIX-8** is the acceptance gate for "GEO is now measurable" — no other priority-D item blocks the next audit cycle.

**Verified-not-broken (from the audit, do not "re-fix"):** FAQ visible parity on `icare.html`, `taskedge.html`, `automation.html` — sampled questions/answers match their `FAQPage` JSON-LD (the audit's finding 2.2 was a false positive caused by the accordion-class grep; the corrected status is recorded in the audit file).

*Prepared 2026-10-15. Line numbers are from the audited commit state; re-run the grep next to each fix if you've committed since.*

---

## Implementation Log — 2026-10-15 (committed fixes)

| Fix | Status | Notes |
|---|---|---|
| FIX-1, FIX-2, FIX-3 | ✅ shipped | Verified: 0 keywords tags, og 1200×630 + og:type website sitewide, 0 EventScheduled (index + speaking.html) |
| §5.0 decision | ✅ adopted | Canonical headline = **Founder & CTO** (report's recommendation), MD retained only in company.html + jobTitle arrays |
| FIX-5 | ✅ shipped incl. writing/*, _template, speaking.html, .well-known twins | Drift grep = clean repo-wide; visible FAQ answers re-synced to JSON-LD |
| FIX-6 | ✅ shipped | `tools/sync_lastmod.py` + hook in make_build.sh; sitemap now truthful per-file git dates |
| FIX-7 | ✅ shipped | `tools/fix7_essay_twins.py` → 6 twins in writing/, registered in llms.txt + llms-full.txt (+ .well-known) |
| FIX-8 | ✅ script | `tools/ai_crawl_report.sh` (needs host access-log path at first run) |
| FIX-9 | ✅ script | `tools/ping_indexnow.sh` — run post-deploy, not before |
| FIX-11 | ⚠️ closed as-is | PNG already 880px/475KB & well-compressed; sips/magick re-encode gave ≥0 gain; WebP twin (73KB) serves browsers. Further shrink requires quality-losing quantization |
| FIX-10/12/13/14 | ⏸ deferred | CSP enforcement (post report window), sameAs edges + pricing (owner data/decision), title trim (optional) |
| Build | ✅ `./make_build.sh` green (78 files, 5.2 MB); JSON-LD parses 0 failures repo-wide |
