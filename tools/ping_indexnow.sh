#!/bin/bash
# FIX-9: IndexNow ping — run after every deploy (and once per changed URL batch).
# Usage: tools/ping_indexnow.sh [extra-url ...]
KEY=8f4a2c19e7b34d5680f1ae92c7b5d316
HOST=https://praveshsingh.com

# Core URLs always pinged; extra URLs accepted as arguments.
URLS=(
  "$HOST/"
  "$HOST/llms.txt"
  "$HOST/sitemap.xml"
)
for u in "$@"; do URLS+=("$u"); done

rc=0
for u in "${URLS[@]}"; do
  code=$(curl -sS -o /dev/null -w '%{http_code}' "https://api.indexnow.org/indexnow?url=${u}&key=${KEY}")
  printf '%s  %s\n' "$code" "$u"
  case "$code" in 200|202) ;; *) rc=1 ;; esac
done
exit $rc
