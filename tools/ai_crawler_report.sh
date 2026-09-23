#!/usr/bin/env bash
# tools/ai_crawler_report.sh — AI crawler visibility report
#
# Run ON THE SERVER (has access to web-server logs):
#   bash tools/ai_crawler_report.sh /var/log/apache2/access.log
#   bash tools/ai_crawler_report.sh /var/log/nginx/access.log.1
#   zcat /var/log/apache2/access.log-20260922.gz | bash tools/ai_crawler_report.sh
#
# Prints a per-bot tally of AI/LLM crawler hits so GEO/AIO progress is
# measurable (LLM_VISIBILITY_UPDATES.md §1.3e / §11.3). Pipe to cron weekly.

set -euo pipefail

LOG="${1:-/var/log/apache2/access.log}"

if [[ ! -r "$LOG" ]]; then
  echo "Cannot read log file: $LOG" >&2
  echo "Usage: bash tools/ai_crawler_report.sh <access.log path>" >&2
  exit 1
fi

# Bot name -> user-agent fragment
declare -A BOTS=(
  [GPTBot]="GPTBot"
  [OAI-SearchBot]="OAI-SearchBot"
  [ChatGPT-User]="ChatGPT-User"
  [ClaudeBot]="ClaudeBot"
  [Claude-SearchBot]="Claude-SearchBot"
  [Claude-User]="Claude-User"
  [PerplexityBot]="PerplexityBot"
  [Perplexity-User]="Perplexity-User"
  [Google-Extended]="Google-Extended"
  [Applebot-Extended]="Applebot-Extended"
  [CCBot]="CCBot"
  [meta-externalagent]="meta-externalagent"
  [Amazonbot]="Amazonbot"
  [cohere-ai]="cohere-ai"
  [YouBot]="YouBot"
  [Bytespider]="Bytespider"
  # classic search (reference lines)
  [Googlebot]="Googlebot"
  [bingbot]="bingbot"
)

echo "AI Crawler Report — $LOG"
echo "Generated: $(date -u '+%Y-%m-%d %H:%M UTC')"
echo

total=0
printf "%-22s %10s\n" "BOT" "HITS"
printf "%-22s %10s\n" "--------------------" "----------"
for bot in GPTBot OAI-SearchBot ChatGPT-User ClaudeBot Claude-SearchBot Claude-User PerplexityBot Perplexity-User Google-Extended Applebot-Extended CCBot meta-externalagent Amazonbot cohere-ai YouBot Bytespider Googlebot bingbot; do
  frag="${BOTS[$bot]}"
  # match UA fragment, then count; logs vary, match anywhere in line
  hits=$(grep -c -- "$frag" "$LOG" 2>/dev/null || true)
  printf "%-22s %10s\n" "$bot" "$hits"
  total=$((total + hits))
done
printf "%-22s %10s\n" "--------------------" "----------"
printf "%-22s %10s\n\n" "TOTAL" "$total"

echo "Top 10 requested paths by AI crawlers:"
for bot in GPTBot ClaudeBot PerplexityBot OAI-SearchBot; do
  grep -- "$bot" "$LOG" 2>/dev/null | awk '{print $7}'
done | sort | uniq -c | sort -rn | head -10 || true
