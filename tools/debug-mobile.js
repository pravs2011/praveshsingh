#!/usr/bin/env node
/** Focused mobile diagnostic for one page at 390px. Usage: node tools/debug-mobile.js build/index.html */
'use strict';
const { spawn } = require('child_process');
const fs = require('fs'), os = require('os'), path = require('path');

const target = path.resolve(process.argv[2] || 'build/index.html');
const CHROME = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ps-dbg-'));
const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=0',
  '--user-data-dir=' + tmpDir, '--no-first-run', '--disable-gpu', 'about:blank'], { stdio: 'ignore' });
process.on('exit', () => { try { chrome.kill('SIGKILL'); } catch (_) {} });

function waitPort(file, tries) {
  for (let i = 0; i < tries; i++) {
    try { const [p] = fs.readFileSync(file, 'utf8').split('\n'); if (p) return +p; } catch (_) {}
    Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 100);
  }
  return null;
}
const port = waitPort(path.join(tmpDir, 'DevToolsActivePort'), 60);

(async () => {
  setTimeout(() => process.exit(3), 60000).unref();
  const tabs = await fetch(`http://127.0.0.1:${port}/json/list`).then(r => r.json());
  const page = tabs.find(t => t.type === 'page');
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
  let id = 0; const pending = new Map();
  ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } };
  const send = (method, params = {}) => new Promise((res) => { const mid = ++id; pending.set(mid, res); ws.send(JSON.stringify({ id: mid, method, params })); });
  const cdp = async (m, p) => { const r = await send(m, p); if (r.error) throw new Error(m + ': ' + r.error.message); return r.result; };

  await cdp('Page.enable');
  await cdp('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
  await cdp('Page.navigate', { url: 'file://' + target });
  await new Promise(r => setTimeout(r, 800));

  const expr = `(() => {
    const vw = document.documentElement.clientWidth;
    const out = { vw, media980: matchMedia('(max-width: 980px)').matches, media720: matchMedia('(max-width: 720px)').matches };
    const label = (el) => el.tagName + (typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\\s+/).join('.') : '');
    out.widest = [];
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
      if (cs.display === 'none' || !r.width) continue;
      out.widest.push({ el: label(el), w: Math.round(r.width), right: Math.round(r.right),
        disp: cs.display, minW: cs.minWidth, gridCols: cs.gridTemplateColumns !== 'none' ? cs.gridTemplateColumns : undefined });
    }
    out.widest.sort((a, b) => b.right - a.right);
    out.widest = out.widest.slice(0, 8);
    const bad = document.querySelector('body *');
    out.escaperDetail = [];
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
      if (cs.display === 'none' || !r.width || r.right <= vw + 2) continue;
      out.escaperDetail.push({
        el: label(el), w: Math.round(r.width), right: Math.round(r.right),
        parent: label(el.parentElement), parentGrid: getComputedStyle(el.parentElement).gridTemplateColumns,
        parentW: Math.round(el.parentElement.getBoundingClientRect().width)
      });
      if (out.escaperDetail.length >= 6) break;
    }
    return out;
  })()`;
  const res = await cdp('Runtime.evaluate', { expression: expr, returnByValue: true });
  console.log(JSON.stringify(res.result.value, null, 1));
  ws.close(); chrome.kill('SIGKILL'); process.exit(0);
})().catch(e => { console.error('FATAL ' + e.message); process.exit(2); });
