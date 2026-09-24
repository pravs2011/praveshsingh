#!/usr/bin/env python3
"""Mobile-optimization sweep for praveshsingh.com (from tools/mobile-audit.js findings)."""
import sys

def edit(path, pairs, strict=True):
    src = open(path, encoding='utf-8').read()
    ok = True
    for old, new, cnt in pairs:
        n = src.count(old)
        if n == cnt:
            src = src.replace(old, new)
        elif not strict and n == 0:
            print(f'  skip {path}: pattern not found: {old[:44]!r}')
            continue
        else:
            print(f'FAIL {path}: expected {cnt}x found {n}x: {old[:44]!r}'); ok = False
    if ok:
        open(path, 'w', encoding='utf-8').write(src)
        print(f'ok {path}')

# --- 1. footer-links: allow wrapping (fixes ~970px overflow on phones) ---
FL_BLOCK = """.footer-links {
      display: flex;
      gap: 20px;
    }"""
FL_NEW = """.footer-links {
      display: flex;
      flex-wrap: wrap;
      gap: 14px 20px;
    }"""
for f in ['index.html', 'about.html', 'icare.html', 'taskedge.html',
          'automation.html', 'industries.html', 'expertise.html']:
    edit(f, [(FL_BLOCK, FL_NEW, 1)])

FL_ONE = '.footer-links { display: flex; gap: 20px; }'
FL_ONE_NEW = '.footer-links { display: flex; flex-wrap: wrap; gap: 14px 20px; }'
ESSAYS = ['writing/multi-tenant-postgresql-isolation.html',
          'writing/abdm-integration-developer-guide.html',
          'writing/high-value-medicine-inventory-logistics.html',
          'writing/structured-data-extraction-llm-limits.html',
          'writing/dpdp-act-2023-health-tech-checklist.html',
          'writing/offline-tolerant-hospital-software.html',
          'writing/index.html', 'writing/_template.html']
for f in ESSAYS:
    pairs = [(FL_ONE, FL_ONE_NEW, 1)]
    if 'writing/index' not in f and '_template' not in f:
        # 2. long inline <code> must wrap, not force page-wide overflow
        pairs.append(('padding: 2px 6px;\n      border-radius: 4px;',
                      'padding: 2px 6px;\n      border-radius: 4px;\n      overflow-wrap: anywhere;', 1))
        # 3. <pre> must never exceed the viewport width
        pairs.append(('overflow-x: auto;\n      margin: 28px 0;',
                      'overflow-x: auto;\n      max-width: 100%;\n      margin: 28px 0;', 1))
        # 4. breadcrumb links: bigger tap targets (were ~16px tall)
        pairs.append(('.crumb a { color: var(--text-muted); }',
                      '.crumb a { color: var(--text-muted); display: inline-block; padding: 10px 2px; }', 1))
    edit(f, pairs, strict=False)

# --- 5. high-value essay: comparison table gets a scroll wrapper ---
T = '          <table style="width:100%; border-collapse:collapse; margin:24px 0; font-size:0.95rem; border:1px solid var(--border);">'
T_NEW = ('          <div style="overflow-x:auto; -webkit-overflow-scrolling:touch;">\n'
         '          <table style="min-width:640px; width:100%; border-collapse:collapse; margin:24px 0; font-size:0.95rem; border:1px solid var(--border);">')
edit('writing/high-value-medicine-inventory-logistics.html',
     [(T, T_NEW, 1), ('        </table>', '        </table>\n          </div>', 1)], strict=False)

print('sweep done')
