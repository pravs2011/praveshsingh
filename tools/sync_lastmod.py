#!/usr/bin/env python3
"""FIX-6: rewrite sitemap <lastmod> from each file's last relevant git commit date.

Run from repo root: python3 tools/sync_lastmod.py [sitemap.xml]
Falls back to today's date for files with no git history (never committed).
Exit codes: 0 ok, 1 on any failure — suitable for make_build.sh gating.
"""
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

SITE = Path(sys.argv[1] if len(sys.argv) > 1 else "sitemap.xml")
BASE = "https://praveshsingh.com/"

def last_commit_date(rel: str) -> str:
    p = Path(rel)
    if rel == "" or rel == ".":
        p = Path("index.html")
    if not p.exists() and not rel.endswith("/"):
        p = Path(rel).with_suffix(".html")
    if rel.endswith("/"):  # directory-ish URLs (the /writing/ hub)
        p = Path(rel.rstrip("/")) / "index.html"
    if not p.exists():
        return None
    out = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", str(p)],
        capture_output=True, text=True,
    )
    return out.stdout.strip() or None

xml = SITE.read_text()
today = date.today().isoformat()
changed, missing = 0, []

def repl(m):
    global changed
    loc, old = m.group(1), m.group(2)
    rel = loc.replace(BASE, "", 1)
    got = last_commit_date(rel)
    if got is None:
        missing.append(loc)
        got = old if old else today
    got = got or today
    if got != old:
        changed += 1
    return f"<loc>{loc}</loc>\n    <lastmod>{got}</lastmod>"

new = re.sub(r"<loc>(.+?)</loc>\s*<lastmod>([^<]+)</lastmod>", repl, xml)
if new != xml:
    SITE.write_text(new)

if missing and BASE:  # only flag real misses, empty <loc> never happens in this sitemap
    print(f"  warning: no git history for: {missing}", file=sys.stderr)
print(f"sync_lastmod: {changed} lastmod values updated "
      f"({len(set(re.findall(chr(60) + 'lastmod>([^<]+)<', new)))} distinct dates)")
sys.exit(0)
