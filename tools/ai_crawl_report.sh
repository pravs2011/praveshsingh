#!/bin/bash
# FIX-8: AI-crawler hit report (GEO attribution).
# Usage: tools/ai_crawl_report.sh [access.log [access.log.1 ...]]
#        (no args = tries the common Apache paths, first that exists wins)
# Output: hits per crawler + top 20 AI-crawled URLs. Wire into cron/launchd weekly.
set -u

AGENTS=(GPTBot OAI-SearchBot ChatGPT-User ClaudeBot Claude-User Claude-SearchBot
        anthropic-ai PerplexityBot Perplexity-User Google-Extended
        Applebot-Extended Applebot Amazonbot cohere-ai YouBot Bytespider
        meta-externalagent CCBot diffbot)
REGEX=$(IFS='|'; echo "${AGENTS[*]}")

LOGS=("$@")
if [ ${#LOGS[@]} -eq 0 ]; then
  for cand in /var/log/apache2/access.log /var/log/httpd/access_log \
              /var/log/nginx/access.log "$HOME/ai_crawl_access.log"; do
    if [ -f "$cand" ]; then LOGS=("$cand"); break; fi
  done
fi
if [ ${#LOGS[@]} -eq 0 ]; then
  echo "No access log found. Pass one: tools/ai_crawl_report.sh /path/access.log" >&2
  exit 2
fi

ALL=$(cat "${LOGS[@]}")
echo "== AI crawler hits — generated $(date '+%Y-%m-%d %H:%M') — sources: ${LOGS[*]} =="
total=0
for a in "${AGENTS[@]}"; do
  c=$(grep -c "$a" <<<"$ALL" || true)
  total=$((total + c))
  [ "$c" -gt 0 ] && printf '%8d  %s\n' "$c" "$a"
done
printf '%8d  TOTAL\n' "$total"

echo
echo "== Top 20 AI-crawled URLs =="
grep -E "$REGEX" <<<"$ALL" | awk '{print $7}' | sort | uniq -c | sort -rn | head -20

echo
echo "Baseline this output into the next audit for trend attribution."
