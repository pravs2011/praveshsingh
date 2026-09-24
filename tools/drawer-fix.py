#!/usr/bin/env python3
"""Move .mobile-drawer out of <header> on pages where it's trapped by the
header's backdrop-filter containing block (drawer painted as 390x73 sliver
behind hero content). Same fix already applied to the 6 writing/ essays."""
import re, sys

PAGES = [
    "index.html", "about.html", "icare.html", "taskedge.html",
    "automation.html", "industries.html", "expertise.html",
    "writing/index.html", "writing/_template.html",
]

OPEN_RE = re.compile(r'[ \t]*<div class="mobile-drawer" id="mobileMenu" aria-hidden="true">')
MAIN_RE = re.compile(r'^([ \t]*<main[ >])', re.M)
HEADER_CLOSE_RE = re.compile(r'^([ \t]*</header>)', re.M)


def indent_of(line: str) -> str:
    return line[: len(line) - len(line.lstrip())]


def fix(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        src = f.read()

    m_open = OPEN_RE.search(src)
    if not m_open:
        return "SKIP no drawer"
    # Extract drawer block: from its opening line to the line before </header>
    # (drawer is the last child; </header> closes it). Find </header> AFTER drawer start.
    hdr = HEADER_CLOSE_RE.search(src, m_open.end())
    if not hdr:
        return "SKIP no </header> after drawer"
    drawer_block = src[m_open.start(): hdr.start()].rstrip("\n")
    rest = src[: m_open.start()] + src[hdr.start():]  # header block sans drawer

    m_main = MAIN_RE.search(rest)
    if not m_main:
        return "SKIP no <main>"

    ind = indent_of(m_main.group(1))
    moved = "<!-- Mobile Drawer -->\n" + indent(drawer_block, ind) + "\n\n"
    out = rest[: m_main.start(1)] + moved + rest[m_main.start(1):]
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    return "OK moved after </header>, before <main>"


def indent(block: str, ind: str) -> str:
    if block.startswith("    <"):
        # strip one level of 4-space indent then re-indent
        lines = []
        for ln in block.split("\n"):
            lines.append(ln[4:] if ln.startswith("    ") else ln.lstrip() if ln.strip() else ln)
        block = "\n".join(lines)
    return "\n".join((ind + ln) if ln.strip() else ln for ln in block.split("\n"))


if __name__ == "__main__":
    for p in PAGES:
        print(f"{p}: {fix(p)}")
