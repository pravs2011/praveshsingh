#!/usr/bin/env python3
"""FIX-5 role-string + bio sync (one-shot). Safe to re-run; exits 0 when no changes remain."""
import re
from pathlib import Path

BIO_LEAD_OLD = re.compile(
    r"Pravesh Singh is an Indian software engineer, entrepreneur, and the "
    r"Managing Director and Chief Technology Officer \(CTO\) of SoftEdge Technology Solutions\.( [^.]+\.?)?"
)

BIO_LEAD_NEW = ("Pravesh Singh is the Founder and Chief Technology Officer (CTO) of "
                "SoftEdge Technology Solutions \u2014 a fractional CTO, senior AI developer & "
                "healthcare software architect. He builds AI-powered platforms, multi-tenant "
                "SaaS and HIPAA-aware, GDPR-conscious health systems for clients in India, "
                "the US and Europe.")

PHRASE_OLD = "the Managing Director and Chief Technology Officer (CTO) of SoftEdge Technology Solutions"
PHRASE_NEW = "the Founder and Chief Technology Officer (CTO) of SoftEdge Technology Solutions"

# (file, old, new)
EDITS = [
    # llms.txt role bullet
    (Path("llms.txt"),
     "- **Managing Director & CTO**, SoftEdge Technology Solutions",
     "- **Founder & CTO**, SoftEdge Technology Solutions"),
    (Path(".well-known/llms.txt"),
     "- **Managing Director & CTO**, SoftEdge Technology Solutions",
     "- **Founder & CTO**, SoftEdge Technology Solutions"),
    # llms-full.txt role bullet
    (Path("llms-full.txt"),
     "**SoftEdge Technology Solutions (Managing Director & CTO):**",
     "**SoftEdge Technology Solutions (Founder & CTO):**"),
    (Path(".well-known/llms-full.txt"),
     "**SoftEdge Technology Solutions (Managing Director & CTO):**",
     "**SoftEdge Technology Solutions (Founder & CTO):**"),
]

# Visible caption lines
CAPTIONS = [
    (Path("about.html"), "Managing Director & CTO, SoftEdge Technology Solutions \u00b7 praveshsingh.com",
     "Founder & CTO, SoftEdge Technology Solutions \u00b7 praveshsingh.com"),
    (Path("automation.html"), "Managing Director & CTO, SoftEdge Technology Solutions \u00b7 praveshsingh.com",
     "Founder & CTO, SoftEdge Technology Solutions \u00b7 praveshsingh.com"),
    (Path("icare.html"), "Managing Director & CTO, SoftEdge Technology Solutions \u00b7 praveshsingh.com",
     "Founder & CTO, SoftEdge Technology Solutions \u00b7 praveshsingh.com"),
    (Path("index.html"), "Managing Director & CTO, SoftEdge Technology Solutions</div>",
     "Founder & CTO, SoftEdge Technology Solutions</div>"),
    (Path("expertise.html"), "Founder, Managing Director &amp; CTO",
     "Founder &amp; CTO"),
    (Path("expertise.html"), "Managing Director &amp; CTO, SoftEdge Technology Solutions",
     "Founder &amp; CTO, SoftEdge Technology Solutions"),
]

TXTS = ["llms.txt", "llms-full.txt", ".well-known/llms.txt", ".well-known/llms-full.txt"]
changed = []

for path in TXTS:
    f = Path(path)
    s = f.read_text()
    orig = s
    n = len(BIO_LEAD_OLD.findall(s))
    if n:
        s = BIO_LEAD_OLD.sub(BIO_LEAD_NEW, s)  # first occurrence per file is the identity lead
    if PHRASE_OLD in s:
        s = s.replace(PHRASE_OLD, PHRASE_NEW)
    if s != orig:
        f.write_text(s)
        changed.append(str(f))

for f, old, new in EDITS + CAPTIONS:
    s = f.read_text()
    if old in s:
        f.write_text(s.replace(old, new))
        changed.append(f"{f} :: {old[:44]!r}")

print("changed:", *changed or ["(nothing \u2014 already clean)"], sep="\n  ")
