#!/usr/bin/env node
/**
 * Mobile audit — loads every built page in headless Chrome at 390x844 with
 * mobile emulation and reports measured issues:
 *   - horizontal page overflow & elements escaping the viewport
 *   - hamburger present & visible on mobile
 *   - tap targets < 24px (header/footer/buttons)
 *   - tables/pre wider than the viewport
 * Streams one JSON line per page to stdout. No npm deps (Node >= 22).
 * Usage: node tools/mobile-audit.js [page.html ...]
 */
'use strict';
const { spawn } = require('child_process');
const fs = require('fs'), os = require('os'), path = require('path');

const ROOT = path.resolve(__dirname, '..', 'build');
let pages = process.argv.slice(2);
if (!pages.length) {
  pages = fs.readdirSync(ROOT).filter(f => f.endsWith('.html')).map(f => path.join(ROOT, f));
  const w = path.join(ROOT, 'writing');
  if (fs.existsSync(w)) for (const f of fs.readdirSync(w))
    if (f.endsWith('.html') && !f.startsWith('_')) pages.push(path.join(w, f));
}

// Never hang: hard exit with whatever we have.
setTimeout(() => { console.error('GLOBAL TIMEOUT'); process.exit(3); }, 240000).unref();

const CHROME = process.env.CHROME_PATH ||
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ps-mob-'));
const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=0',
  '--user-data-dir=' + tmpDir, '--no-first-run', '--disable-gpu', 'about:blank'],
  { stdio: 'ignore' });
process.on('exit', () => { try { chrome.kill('SIGKILL'); } catch (_) {} });

function waitPort(file, tries) {
  for (let i = 0; i < tries; i++) {
    try { const [p] = fs.readFileSync(file, 'utf8').split('\n'); if (p) return +p; } catch (_) {}
    Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 100);
  }
  return null;
}
const port = waitPort(path.join(tmpDir, 'DevToolsActivePort'), 60);
if (!port) { console.error('no CDP port'); process.exit(2); }

const withTimeout = (p, ms, tag) => Promise.race([
  p, new Promise((_, rej) => setTimeout(() => rej(new Error('timeout: ' + tag)), ms)),
]);

(async () => {
  const tabs = await withTimeout(
    fetch(`http://127.0.0.1:${port}/json/list`).then(r => r.json()), 10000, 'list');
  const page = tabs.find(t => t.type === 'page');
  if (!page) { console.error('no page target'); process.exit(2); }

  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await withTimeout(new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; }), 10000, 'ws');
  let id = 0; const pending = new Map();
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
  };
  const send = (method, params = {}) => new Promise((res) => {
    const mid = ++id; pending.set(mid, res);
    ws.send(JSON.stringify({ id: mid, method, params }));
  });
  const cdp = (method, params, ms = 15000) =>
    withTimeout(send(method, params).then(r => {
      if (r.error) throw new Error(method + ': ' + r.error.message);
      return r.result;
    }), ms, method);

  await cdp('Page.enable');
  await cdp('Runtime.enable');

  const JS = `(() => {
    const vw = document.documentElement.clientWidth, out = {};
    out.vw = vw;
    out.scrollW = document.scrollingElement.scrollWidth;
    out.overflow = out.scrollW > vw + 1;
    out.escapers = [];
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden' || !r.width) continue;
      if (r.right > vw + 2 || r.left < -2) {
        out.escapers.push(el.tagName + (typeof el.className === 'string' && el.className ? '.' + el.className.split(' ')[0] : '') +
          ' L' + Math.round(r.left) + ' R' + Math.round(r.right));
        if (out.escapers.length >= 5) break;
      }
    }
    const inScroller = (el) => {
      let p = el.parentElement;
      while (p && p !== document.body) {
        const c = getComputedStyle(p);
        if (c.overflowX === 'auto' || c.overflowX === 'scroll') return true;
        p = p.parentElement;
      }
      return false;
    };
    const ham = document.querySelector('.hamburger, #hamburgerBtn, .nav-burger, #navBurger');
    out.hamburger = ham ? { present: true, visible: !!(ham.offsetWidth || ham.offsetHeight) } : { present: false };
    out.drawerOpens = false;
    if (ham) {
      const drawer = document.querySelector('.mobile-drawer, .nav-drawer, #mobileMenu, #navDrawer');
      ham.click();
      if (drawer) {
        const dc = getComputedStyle(drawer);
        out.drawerOpens = drawer.classList.contains('open') || (dc.display !== 'none' && drawer.getBoundingClientRect().height > 100);
      }
      ham.click();
    }
    out.tinyTargets = [];
    for (const el of document.querySelectorAll('header a, header button, footer a, footer button, .btn, button')) {
      const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
      if (cs.display === 'none' || !r.width) continue;
      if (Math.min(r.width, r.height) < 24)
        out.tinyTargets.push((el.textContent || el.tagName).trim().slice(0, 20) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
      if (out.tinyTargets.length >= 5) break;
    }
    out.wideBlocks = [];
    for (const el of document.querySelectorAll('table, pre')) {
      const r = el.getBoundingClientRect();
      if (r.width > vw + 2 && !inScroller(el) && getComputedStyle(el).overflowX !== 'auto')
        out.wideBlocks.push(el.tagName + ' w' + Math.round(r.width));
    }
    // escapers: skip elements contained in a horizontal scroller (they clip correctly)
    out.escapers = [];
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden' || !r.width) continue;
      if ((r.right > vw + 2 || r.left < -2) && !inScroller(el) && cs.overflowX !== 'auto') {
        out.escapers.push(el.tagName + (typeof el.className === 'string' && el.className ? '.' + el.className.split(' ')[0] : '') +
          ' L' + Math.round(r.left) + ' R' + Math.round(r.right));
        if (out.escapers.length >= 5) break;
      }
    }
    out.viewportMeta = !!document.querySelector('meta[name="viewport"][content*="width=device-width"]');
    return out;
  })()`;

  for (const file of pages) {
    const name = path.basename(path.dirname(file)) + '/' + path.basename(file);
    try {
      await cdp('Emulation.setDeviceMetricsOverride',
        { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
      await cdp('Page.navigate', { url: 'file://' + file });
      await new Promise(r => setTimeout(r, 600));
      const res = await cdp('Runtime.evaluate', { expression: JS, returnByValue: true });
      const line = JSON.stringify({ page: name, v: res.result.value });
      process.stdout.write(line + '\n');
      console.error('ok ' + name);
    } catch (e) {
      process.stdout.write(JSON.stringify({ page: name, error: e.message }) + '\n');
      console.error('ERR ' + name + ': ' + e.message);
    }
  }
  ws.close();
  chrome.kill('SIGKILL');
  process.exit(0);
})().catch(e => { console.error('FATAL ' + e.message); process.exit(2); });
