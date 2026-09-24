#!/usr/bin/env python3
"""Add hamburger + mobile drawer to pages that only hide .nav-links on mobile."""

CSS = """
    /* Mobile navigation drawer */
    .nav-burger {
      display: none;
      width: 44px; height: 44px;
      padding: 11px 10px;
      border-radius: 8px;
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--border);
      cursor: pointer;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      z-index: 1100;
    }
    .nav-burger span { display: block; width: 20px; height: 2px; background: #e2e8f0; border-radius: 2px; transition: all 0.25s cubic-bezier(0.16,1,0.3,1); }
    .nav-burger[aria-expanded="true"] span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
    .nav-burger[aria-expanded="true"] span:nth-child(2) { opacity: 0; transform: scaleX(0); }
    .nav-burger[aria-expanded="true"] span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }
    .nav-drawer {
      display: none;
      position: fixed;
      top: 72px; left: 0; right: 0; bottom: 0;
      background: rgba(9,11,16,0.98);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border-top: 1px solid var(--border);
      padding: 24px 20px 48px;
      overflow-y: auto;
      z-index: 999;
      flex-direction: column;
      gap: 10px;
    }
    .nav-drawer.open { display: flex; }
    .nav-drawer-link {
      display: flex; align-items: center;
      padding: 14px 12px;
      border-radius: 8px;
      color: #e2e8f0; font-size: 1rem; font-weight: 500;
      text-decoration: none;
      background: rgba(255,255,255,0.02);
      border: 1px solid rgba(255,255,255,0.04);
    }
    .nav-drawer-link:hover { background: rgba(255,255,255,0.08); color: #fff; }
"""

MEDIA_ONELINE_OLD = "    @media (max-width: 820px) { .nav-links { display: none; } }"
MEDIA_ONELINE_NEW = ("    @media (max-width: 820px) {\n"
                     "      .nav-links { display: none; }\n"
                     "      .nav-burger { display: flex; }\n"
                     "    }")

LINKS = [
    ("about.html", "About"), ("icare.html", "iCare"), ("expertise.html", "Expertise"),
    ("writing/", "Writing"), ("speaking.html", "Speaking"), ("glossary.html", "Glossary"),
]

def drawer_html(current):
    items = []
    for href, label in LINKS:
        active = " active" if label.lower() in current else ""
        items.append(f'      <a href="{href}" class="nav-drawer-link{active}">{label}</a>')
    return ('  <div class="nav-drawer" id="navDrawer" aria-hidden="true">\n'
            + "\n".join(items) + "\n  </div>")

BURGER = ('      <button class="nav-burger" id="navBurger" aria-label="Open navigation menu"'
          ' aria-expanded="false" aria-controls="navDrawer">\n'
          '        <span></span><span></span><span></span>\n      </button>\n')

JS = """  <script>
    (function () {
      var burger = document.getElementById('navBurger');
      var drawer = document.getElementById('navDrawer');
      if (!burger || !drawer) return;
      function close() {
        burger.setAttribute('aria-expanded', 'false');
        drawer.classList.remove('open');
        drawer.setAttribute('aria-hidden', 'true');
      }
      burger.addEventListener('click', function () {
        var open = burger.getAttribute('aria-expanded') === 'true';
        burger.setAttribute('aria-expanded', String(!open));
        drawer.classList.toggle('open', !open);
        drawer.setAttribute('aria-hidden', String(open));
      });
      drawer.addEventListener('click', function (e) {
        if (e.target instanceof Element && e.target.closest('a')) close();
      });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    })();
  </script>
</body>"""

def main():
    for fname, current in [("privacy.html", "privacy"), ("glossary.html", "glossary"),
                           ("speaking.html", "speaking"), ("company.html", "company")]:
        src = open(fname, encoding="utf-8").read()
        if "navBurger" in src:
            print(f"skip {fname}: already has burger")
            continue
        # 1. CSS before </style>
        if src.count("  </style>") != 1:
            print(f"FAIL {fname}: </style> anchor count = {src.count('  </style>')}"); continue
        src = src.replace("  </style>", CSS + "  </style>")
        # 2. show burger in the 820px media query
        if src.count(MEDIA_ONELINE_OLD) != 1:
            print(f"FAIL {fname}: 820px media anchor count = {src.count(MEDIA_ONELINE_OLD)}"); continue
        src = src.replace(MEDIA_ONELINE_OLD, MEDIA_ONELINE_NEW)
        # 3. burger button before </nav> (only the header nav closes with 6-space indent)
        nav_close = "      </nav>"
        if src.count(nav_close) != 1:
            print(f"FAIL {fname}: </nav> anchor count = {src.count(nav_close)}"); continue
        src = src.replace(nav_close, BURGER + nav_close)
        # 4. drawer right after </header>
        if src.count("  </header>") != 1:
            print(f"FAIL {fname}: </header> anchor count = {src.count('  </header>')}"); continue
        src = src.replace("  </header>", "  </header>\n\n" + drawer_html(current))
        # 5. JS before </body>
        if src.count("</body>") != 1:
            print(f"FAIL {fname}: </body> anchor count = {src.count('</body>')}"); continue
        src = src.replace("</body>", JS)
        open(fname, "w", encoding="utf-8").write(src)
        print(f"ok {fname}")

if __name__ == "__main__":
    main()
