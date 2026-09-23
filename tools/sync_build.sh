#!/usr/bin/env bash
# tools/sync_build.sh — mirror the deployable site into build/
#
# build/ is a staging mirror of the site root. It is NOT meant to be deployed;
# the web server hard-blocks /build/ (see .htaccess rule 5 and robots.txt).
# Run this after editing site files to keep the mirror current.
#
# Usage: bash tools/sync_build.sh

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD="$ROOT/build"

cd "$ROOT"

echo "Syncing site files into build/ ..."

# Files & dirs that must never enter build/
EXCLUDES=(
  build
  tools
  graft
  .git
  .github
  .claude
  node_modules
  .DS_Store
  IMPROVEMENTS_SEO_AIO_GEO.md
  WEBSITE_UPDATE_PLAN.md
  ANALYTICS_CODE.md
  GTAG_CODE.md
  CLAUDE_SUGGESTION.md
  CHATGPT_SUGGESTION.md
  praveshsingh-production.zip
  make_page.sh
  .gitignore
  .ignore
)

ARGS=()
for e in "${EXCLUDES[@]}"; do
  ARGS+=(--exclude "$e")
done

# Ensure build exists and clean stale top-level mirrors (keep dir itself)
mkdir -p "$BUILD"

# Mirror everything (HTML, assets, images/, writing/, .well-known/, etc.)
rsync -a --delete "${ARGS[@]}" \
  --exclude '.git*' \
  ./ "$BUILD/"

# Explicitly guarantee build/ never contains itself or repo-only files
rm -rf "$BUILD/build" "$BUILD/tools" "$BUILD/graft" 2>/dev/null || true

echo "Done. Mirror at: $BUILD"
echo "Remember: do NOT deploy build/ — deploy the repo root (or a clean export of it)."
