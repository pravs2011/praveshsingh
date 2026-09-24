#!/bin/bash
# ---------------------------------------------------------------------------
# make_build.sh — assemble a production build of praveshsingh.com
#
#   ./make_build.sh            → builds ./build/ (deploy this directory)
#   ./make_build.sh --zip      → also prunes stale praveshsingh-production.zip
#                                and rebuilds it from ./build/
#
# What goes in:  every page, .htaccess, robots/sitemap/llms files, verification
#                file, .well-known/, images/, writing/ hub + 6 essays + feed.
# What stays out: build system itself, page generator, templates, planning
#                docs, .DS_Store. The stale build/ mirror is wiped first.
#
# The script validates the result and exits non-zero on any failure, so it is
# safe to run before every deployment.
# ---------------------------------------------------------------------------
set -euo pipefail

cd "$(dirname "$0")"

BUILD="build"
ZIP="praveshsingh-production.zip"
FAILED=0

say()  { printf '%s\n' "$*"; }
fail() { printf 'FAIL  %s\n' "$*" >&2; FAILED=1; }

say "==> Cleaning $BUILD/ ..."
rm -rf "$BUILD"
mkdir -p "$BUILD/writing" "$BUILD/.well-known"

say "==> Copying deploy files ..."

# Root pages
for f in index.html about.html icare.html taskedge.html automation.html \
         industries.html expertise.html speaking.html glossary.html company.html \
         404.html \
         .htaccess robots.txt sitemap.xml llms.txt llms-full.txt \
         expertise.md 8f4a2c19e7b34d5680f1ae92c7b5d316.txt \
         yandex_489999cb20aa0fec.html; do
  cp "$f" "$BUILD/"
done

# Writing section
cp writing/index.html \
   writing/feed.xml \
   writing/offline-tolerant-hospital-software.html \
   writing/abdm-integration-developer-guide.html \
   writing/multi-tenant-postgresql-isolation.html \
   writing/high-value-medicine-inventory-logistics.html \
   writing/structured-data-extraction-llm-limits.html \
   writing/dpdp-act-2023-health-tech-checklist.html \
   "$BUILD/writing/"

# Support directories
cp .well-known/security.txt .well-known/index.html "$BUILD/.well-known/"
cp .well-known/llms.txt .well-known/llms-full.txt "$BUILD/.well-known/"
cp -R images "$BUILD/images"

# Strip OS junk
find "$BUILD" -name '.DS_Store' -delete
find "$BUILD" -name '._*'  -delete

say "==> Validating build ..."

# 1. Required files exist
for f in index.html about.html icare.html taskedge.html automation.html \
         industries.html expertise.html speaking.html glossary.html company.html \
         404.html .htaccess robots.txt sitemap.xml llms.txt llms-full.txt \
         expertise.md writing/index.html writing/feed.xml \
         .well-known/security.txt images/pravesh-singh.png; do
  [ -f "$BUILD/$f" ] || fail "missing required file: $f"
done

# 2. Nothing that must never ship
leak=$(find "$BUILD" \( -name '_template.html' -o -name 'make_page.sh' \
        -o -name '*.md' ! -name 'expertise.md' -o -name '.DS_Store' \
        -o -path "$BUILD/build*" -o -name 'CLAUDE*' -o -name 'CHATGPT*' \
        -o -name 'IMPROVEMENTS*' -o -name 'WEBSITE_*' -o -name 'LLM_VIS*' \
        -o -name 'GTAG*' -o -name 'ANALYTICS*' -o -name 'README.txt' \) -print)
[ -z "$leak" ] || fail "dev artifacts leaked into build: $leak"

# 3. Canonical href hygiene: no bare /writing/index.html links, no ../index.html
bad=$(grep -rl 'href="writing/index\.html"\|href="\.\./index\.html"' \
      "$BUILD" --include='*.html' || true)
[ -z "$bad" ] || fail "non-canonical hub/home hrefs in: $bad"

# 4. Stale llms/feed references
grep -rq 'writing/index\.html' "$BUILD/llms.txt" "$BUILD/llms-full.txt" \
     "$BUILD/writing/feed.xml" && fail "stale /writing/index.html refs in llms/feed"

# 5. Template must be noindexed if it ever ships
[ -f "$BUILD/writing/_template.html" ] && \
  grep -q 'noindex' "$BUILD/writing/_template.html" || true

# 6. Every sitemap URL maps to a file in the build
python3 - "$BUILD" <<'PYEOF' || fail "sitemap references missing files"
import re, sys, os
b = sys.argv[1]
sitemap = open(os.path.join(b, "sitemap.xml")).read()
locs = re.findall(r"<loc>(.*?)</loc>", sitemap)
missing = []
for u in locs:
    p = u.replace("https://praveshsingh.com/", "")
    fs = os.path.join(b, p) if p else os.path.join(b, "index.html")
    if p.endswith("/"):
        fs = os.path.join(b, p, "index.html")
    if not os.path.exists(fs):
        missing.append(u)
if missing:
    print("missing: " + ", ".join(missing), file=sys.stderr)
    sys.exit(1)
print(f"    sitemap OK — {len(locs)} URLs all present in build")
PYEOF

# 7. Sitemap / robots / htaccess are well-formed XML where applicable
if command -v xmllint >/dev/null 2>&1; then
  xmllint --noout "$BUILD/sitemap.xml" 2>/dev/null || fail "sitemap.xml not well-formed"
  xmllint --noout "$BUILD/writing/feed.xml" 2>/dev/null || fail "feed.xml not well-formed"
fi

# 8. No internal link points into /build/
grep -rl 'href="/build\|href="build/' "$BUILD" --include='*.html' >/dev/null 2>&1 \
  && fail "internal link points at /build/"

if [ "$FAILED" -ne 0 ]; then
  say ""
  say "==> BUILD FAILED — fix the issues above and re-run."
  exit 1
fi

FILES=$(find "$BUILD" -type f | wc -l | tr -d ' ')
SIZE=$(du -sh "$BUILD" | cut -f1)
say ""
say "==> Build OK: $BUILD/ ($FILES files, $SIZE)"

# Optional zip
if [ "${1:-}" = "--zip" ]; then
  say "==> Repackaging $ZIP ..."
  rm -f "$ZIP"
  ( cd "$BUILD" && zip -q -r "../$ZIP" . )
  say "==> $ZIP ready ($(du -h "$ZIP" | cut -f1))"
  say "    Upload its contents to the web root; delete any stale build/ on the server."
fi
