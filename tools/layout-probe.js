#!/usr/bin/env node
/**
 * Headless-Chrome layout probe #3 — root-cause hunt for the escaping <ol>.
 * Dumps offsetParent chain, ancestor computed styles, and every CSS rule
 * matching list/nav/hero/container selectors. No npm deps (Node >= 22).
 * Usage: node tools/layout-probe.js [file.html]
 */
'use strict';

const { spawn } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const target = path.resolve(process.argv[2] || 'build/privacy.html');
const CHROME = process.env.CHROME_PATH ||
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

if (!fs.existsSync(CHROME)) { console.error('Chrome not found'); process.exit(2); }
if (!fs.existsSync(target)) { console.error('File not found: ' + target); process.exit(2); }

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ps-probe3-'));
const chrome = spawn(CHROME, [
  '--headless=new', '--remote-debugging-port=0', '--user-data-dir=' + tmpDir,
  '--no-first-run', '--no-default-browser-check', '--disable-gpu',
  '--window-size=1080,860', 'about:blank',
], { stdio: 'ignore' });

function fail(msg) {
  console.error('PROBE FAILED: ' + msg);
  try { chrome.kill('SIGKILL'); } catch (_) {}
  process.exit(2);
}

function waitForPort(file, tries) {
  for (let i = 0; i < tries; i++) {
    try {
      const [port] = fs.readFileSync(file, 'utf8').split('\n');
      if (port) return Number(port);
    } catch (_) {}
    Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 100);
  }
  return null;
}

const port = waitForPort(path.join(tmpDir, 'DevToolsActivePort'), 50);
if (!port) fail('no debugging port');

fetch(`http://127.0.0.1:${port}/json/list`)
  .then((r) => r.json())
  .then((tabs) => {
    const page = tabs.find((t) => t.type === 'page');
    if (!page) throw new Error('no page target');
    return page.webSocketDebuggerUrl;
  })
  .then((wsUrl) => new Promise((resolve, reject) => {
    const ws = new WebSocket(wsUrl);
    let id = 0;
    const pending = new Map();
    ws.onopen = () => {
      const send = (method, params) => new Promise((res) => {
        const mid = ++id;
        pending.set(mid, res);
        ws.send(JSON.stringify({ id: mid, method, params: params || {} }));
      });
      resolve({ send, close: () => ws.close() });
    };
    ws.onmessage = (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg.result); pending.delete(msg.id); }
    };
    ws.onerror = () => reject(new Error('websocket error'));
  }))
  .then(async (cdp) => {
    await cdp.send('Page.enable');
    await cdp.send('Page.navigate', { url: 'file://' + target });
    await new Promise((r) => setTimeout(r, 1200));

    const expr = `(() => {
      const out = {};
      const toc = document.querySelector('nav.toc');
      const ol = toc.querySelector('ol');
      const tocCS = getComputedStyle(toc);
      out.tocDisplay = { display: tocCS.display, position: tocCS.position, height: tocCS.height,
                         maxHeight: tocCS.maxHeight, overflow: tocCS.overflow, zoom: tocCS.zoom };
      const olR = ol.getBoundingClientRect();
      out.olRect = { x: Math.round(olR.x), y: Math.round(olR.y), w: Math.round(olR.width), h: Math.round(olR.height) };
      out.olOffset = { offsetParent: ol.offsetParent && (ol.offsetParent.tagName + '.' + ol.offsetParent.className),
                       offsetTop: ol.offsetTop, offsetLeft: ol.offsetLeft };
      const olCS = getComputedStyle(ol);
      out.olMore = { width: olCS.width, maxWidth: olCS.maxWidth, alignSelf: olCS.alignSelf,
                     gridColumn: olCS.gridColumn, gridRow: olCS.gridRow, flex: olCS.flex,
                     breakInside: olCS.breakInside, columnSpan: olCS.columnSpan };
      out.ancestors = [];
      let el = ol.parentElement;
      while (el && el !== document.documentElement) {
        const cs = getComputedStyle(el);
        out.ancestors.push({
          el: el.tagName + (el.className ? '.' + String(el.className).split(' ').join('.') : ''),
          display: cs.display, position: cs.position,
          columns: cs.columnCount + '/' + cs.columnWidth, zoom: cs.zoom,
          transform: cs.transform, gridCols: cs.gridTemplateColumns
        });
        el = el.parentElement;
      }
      const htmlCS = getComputedStyle(document.documentElement);
      const bodyCS = getComputedStyle(document.body);
      out.root = { htmlZoom: htmlCS.zoom, htmlFontSize: htmlCS.fontSize, bodyZoom: bodyCS.zoom, bodyTransform: bodyCS.transform };
      out.listRules = [];
      for (const sheet of document.styleSheets) {
        let list; try { list = sheet.cssRules; } catch (_) { continue; }
        for (const rule of list) {
          if (rule.selectorText && /(^|[\\s,>~+])(ol|ul|nav|\\.page-hero|\\.container|main|li)\\b/.test(rule.selectorText)) {
            out.listRules.push(rule.selectorText + ' { ' + rule.style.cssText + ' }');
          }
        }
      }
      return out;
    })()`;

    const res = await cdp.send('Runtime.evaluate', { expression: expr, returnByValue: true });
    console.log(JSON.stringify(res.result.value, null, 2));
    await cdp.close();
    try { chrome.kill('SIGKILL'); } catch (_) {}
    setTimeout(() => { try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {} process.exit(0); }, 300);
  })
  .catch((e) => fail(e.message));
