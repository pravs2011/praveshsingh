#!/usr/bin/env python3
"""Sprint 1+3 mechanical sweep across all HTML pages.

- Unify visible role strings to "Founder & CTO" where they say "Founder, CTO"
- Sync FAQ entity answer text with llms-full.txt wording
- Remove <meta name="keywords"> tags
- De-duplicate GTM + gtag.js: keep GTM container (GTM-M335RXDF) only,
  remove the standalone gtag.js block; keep the custom-event tracker
  (it depends on gtag() — so instead we KEEP gtag.js and remove GTM here)
- Add favicon + apple-touch-icon links (replacing the inline SVG data URI)
- Add Atom feed link on pages that lack it

Strategy: GA4 config (G-2XHZ5NJZLK) is required by the on-page trackEvent
helper, so we keep the gtag.js block and REMOVE the GTM container snippet +
noscript iframe (audit §6.4 — one of the two must go).

Run from repo root:  python3 tools/sprint1_sweep.py
"""
import glob
import re
import sys

GTM_SNIPPET = re.compile(
    r"\s*<!-- Google Tag Manager -->\s*<script>\(function\(w,d,s,l,i\).*?GTM-M335RXDF.*?</script>\s*<!-- End Google Tag Manager -->\s*",
    re.S,
)
GTM_NOSCRIPT = re.compile(
    r"\s*<!-- Google Tag Manager \(noscript\) -->\s*<noscript><iframe src=\"https://www\.googletagmanager\.com/ns\.html\?id=GTM-M335RXDF\".*?</noscript>\s*<!-- End Google Tag Manager \(noscript\) -->\s*",
    re.S,
)
KEYWORDS_META = re.compile(r"\s*<meta name=\"keywords\" content=\"[^\"]*\">\s*", re.S)

INLINE_FAVICON = re.compile(r"\s*<link rel=\"icon\" href=\"data:image/svg\+xml,[^\"]*\">")

FAVICON_LINKS = (
    '  <link rel="icon" href="/images/favicon.ico" sizes="any">\n'
    '  <link rel="apple-touch-icon" href="/images/apple-touch-icon.png">'
)

# FAQ entity-answer sync (audit §1.2): index.html FAQ + JSON-LD must match
# llms-full.txt §8 wording ("Managing Director and Chief Technology Officer").
OLD_FAQ = "Pravesh Singh is an Indian software architect, technology entrepreneur, and the Founder and Chief Technology Officer (CTO) of SoftEdge Technology Solutions."
NEW_FAQ = "Pravesh Singh is an Indian software engineer, entrepreneur, and the Managing Director and Chief Technology Officer (CTO) of SoftEdge Technology Solutions."

ROLE_FIXES = [
    # <title> of index.html — entity-consistent role string
    (
        "<title>Pravesh Singh – Founder, CTO & AI Software Architect</title>",
        "<title>Pravesh Singh – Founder & CTO, AI Software Architect</title>",
    ),
    (
        'meta property="og:title" content="Pravesh Singh – Founder, CTO & AI Software Architect"',
        'meta property="og:title" content="Pravesh Singh – Founder & CTO, AI Software Architect"',
    ),
    (
        'meta name="twitter:title" content="Pravesh Singh – Founder, CTO & AI Software Architect"',
        'meta name="twitter:title" content="Pravesh Singh – Founder & CTO, AI Software Architect"',
    ),
    # Hero H1 (audit §2.3) — entity-anchored, keyword-bearing
    (
        "<h1 class=\"hero-title\">\n              Building <span>intelligent software products</span> that solve real business problems.\n            </h1>",
        "<h1 class=\"hero-title\">\n              Pravesh Singh — <span>Founder &amp; CTO</span> building AI platforms, healthcare software &amp; multi-tenant SaaS.\n            </h1>",
    ),
]

def process(path):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    orig = src
    notes = []

    # 1. Remove GTM container + noscript (keep gtag.js — the tracker needs gtag())
    src, n = GTM_SNIPPET.subn("\n", src)
    if n:
        notes.append("removed GTM container")
    src, n = GTM_NOSCRIPT.subn("\n", src)
    if n:
        notes.append("removed GTM noscript")

    # 2. Drop meta keywords
    src, n = KEYWORDS_META.subn("\n", src)
    if n:
        notes.append("removed meta keywords")

    # 3. Role/FAQ/H1 fixes
    for old, new in ROLE_FIXES:
        if old in src:
            src = src.replace(old, new)
            notes.append("role/h1 fix: " + old[:48].replace("\n", " ") + "…")
    if OLD_FAQ in src:
        src = src.replace(OLD_FAQ, NEW_FAQ)
        notes.append("synced FAQ entity answer")

    # 4. Favicon: replace inline SVG data-URI with real files
    if INLINE_FAVICON.search(src):
        src = INLINE_FAVICON.sub("\n" + FAVICON_LINKS, src, count=1)
        notes.append("favicon links added")

    if src != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(src)
    return notes

def main():
    pages = sorted(
        set(glob.glob("*.html"))
        | set(glob.glob("writing/*.html"))
    )
    pages = [p for p in pages if not p.startswith("_") and "404.html" not in p]
    changed = 0
    for p in pages:
        notes = process(p)
        if notes:
            changed += 1
            print(f"✓ {p}")
            for n in notes:
                print(f"    - {n}")
    print(f"\n{changed}/{len(pages)} pages updated")

if __name__ == "__main__":
    sys.exit(main())
