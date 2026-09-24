#!/usr/bin/env python3
"""Mobile fixes round 2: drawer containing-block bug, burger cascade, tap targets."""
import re

# --- 1. Essays: move #mobileDrawer out of <header> (backdrop-filter on header
#        traps position:fixed descendants -> drawer clamped to 65px). ---
ESSAYS = ['writing/multi-tenant-postgresql-isolation.html',
          'writing/abdm-integration-developer-guide.html',
          'writing/high-value-medicine-inventory-logistics.html',
          'writing/structured-data-extraction-llm-limits.html',
          'writing/dpdp-act-2023-health-tech-checklist.html',
          'writing/offline-tolerant-hospital-software.html']
PAT = re.compile(r'\n\n    <!-- Mobile Drawer -->[\s\S]*?\n    </div>\n  </header>')
for f in ESSAYS:
    src = open(f, encoding='utf-8').read()
    m = PAT.search(src)
    if not m:
        print(f'FAIL {f}: drawer block not found'); continue
    drawer = m.group(0)[: -len('\n  </header>')]  # keep drawer markup, drop header close
    src = src.replace(m.group(0), '\n  </header>', 1)
    src = src.replace('  </header>', '  </header>\n' + drawer.lstrip('\n'), 1)
    open(f, 'w', encoding='utf-8').write(src)
    print(f'ok {f}: drawer moved outside header')

# --- 2. Four new pages: burger visibility must win the cascade.
#        Base .nav-burger{display:none} is later in the sheet than the early
#        media rule, so re-assert visibility in a media rule AFTER the base. ---
for f in ['privacy.html', 'glossary.html', 'speaking.html', 'company.html']:
    src = open(f, encoding='utf-8').read()
    if '@media (max-width: 820px) { .nav-burger { display: flex; } }' in src:
        print(f'skip {f}'); continue
    if src.count('  </style>') != 1:
        print(f'FAIL {f}: style anchor'); continue
    src = src.replace(
        '  </style>',
        '\n    @media (max-width: 820px) { .nav-burger { display: flex; } }\n  </style>')
    open(f, 'w', encoding='utf-8').write(src)
    print(f'ok {f}: burger cascade fixed')

# --- 3. Footer links: comfortable tap targets on phones (all real pages). ---
PAGES = ['index.html', 'about.html', 'icare.html', 'taskedge.html', 'automation.html',
         'industries.html', 'expertise.html', 'privacy.html', 'glossary.html',
         'speaking.html', 'company.html'] + ESSAYS + \
        ['writing/index.html', 'writing/_template.html']
PAD = ('\n    @media (max-width: 720px) {\n'
       '      .footer-links a { display: inline-block; padding: 10px 0; }\n'
       '    }\n')
for f in PAGES:
    src = open(f, encoding='utf-8').read()
    if '.footer-links a { display: inline-block; padding: 10px 0; }' in src:
        print(f'skip {f}'); continue
    if src.count('  </style>') != 1:
        print(f'FAIL {f}: style anchor'); continue
    src = src.replace('  </style>', PAD + '  </style>')
    open(f, 'w', encoding='utf-8').write(src)
    print(f'ok {f}: footer tap targets')
