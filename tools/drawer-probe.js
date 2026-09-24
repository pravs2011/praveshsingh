#!/usr/bin/env node
/** Drawer stacking probe at 390px. Usage: node tools/drawer-probe.js build/index.html [build/about.html ...] */
'use strict';
const { spawn } = require('child_process');
const fs = require('fs'), os = require('os'), path = require('path');

const targets = process.argv.slice(2);
if (!targets.length) { console.error('usage: node tools/drawer-probe.js <page.html> [more.html]'); process.exit(1); }
const CHROME = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ps-drawer-'));
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
  setTimeout(() => process.exit(3), 120000).unref();
  const tabs = await fetch(`http://127.0.0.1:${port}/json/list`).then(r => r.json());
  const page = tabs.find(t => t.type === 'page');
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
  let id = 0; const pending = new Map();
  ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } };
  const send = (method, params = {}) => new Promise((res) => { const mid = ++id; pending.set(mid, res); ws.send(JSON.stringify({ id: mid, method, params })); });
  const cdp = async (m, p) => { const r = await send(m, p); if (r.error) throw new Error(m + ': ' + r.error.message); return r.result; };

  await cdp('Page.enable');
  const FIND_JS = `(() => {
    const ham = document.querySelector('#hamburgerBtn, .hamburger, #navBurger, .nav-burger');
    const drawer = document.querySelector('#mobileMenu, .mobile-drawer, #navDrawer, .nav-drawer');
    if (!ham || !drawer) return { error: 'missing ' + (!ham ? 'hamburger' : 'drawer') };
    ham.click();
    return { inHeader: !!drawer.closest('header') };
  })()`;
  const JS = `(() => {
    const label = (el) => !el ? 'null' : el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\\s+/).join('.') : '') + (el.id ? '#' + el.id : '');
    const drawer = document.querySelector('#mobileMenu, .mobile-drawer, #navDrawer, .nav-drawer');
    const dr = drawer.getBoundingClientRect();
    const cs = getComputedStyle(drawer);
    const samples = [0.25, 0.5, 0.75].map(f => {
      const x = Math.round(innerWidth / 2), y = Math.round(dr.top + dr.height * f);
      const stack = document.elementsFromPoint(x, y).slice(0, 4).map(label);
      return { y, top: stack[0], stack, drawerTopHit: stack.includes(label(drawer)) || stack.some(s => document.querySelector(s) && drawer.contains(document.querySelector(s))) };
    });
    return {
      openNow: drawer.classList.contains('open') || drawer.classList.contains('active'),
      drawerRect: { top: Math.round(dr.top), h: Math.round(dr.height), w: Math.round(dr.width) },
      drawerDisplay: cs.display, drawerVisibility: cs.visibility, drawerPos: cs.position, drawerZ: cs.zIndex,
      onTop: samples.every(s => s.drawerTopHit),
      samples: samples.map(s => ({ y: s.y, top: s.top }))
    };
  })()`;

  for (const file of targets) {
    const name = path.basename(path.dirname(file)) + '/' + path.basename(file);
    try {
      await cdp('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
      await cdp('Page.navigate', { url: 'file://' + path.resolve(file) });
      await new Promise(r => setTimeout(r, 700));
      const find = await cdp('Runtime.evaluate', { expression: FIND_JS, returnByValue: true });
      await new Promise(r => setTimeout(r, 350)); // let open transition (opacity/visibility) settle
      const res = await cdp('Runtime.evaluate', { expression: JS, returnByValue: true });
      const merged = Object.assign({ page: name }, find.result.value || {}, res.result.value || {});
      process.stdout.write(JSON.stringify(merged) + '\n');
    } catch (e) {
      process.stdout.write(JSON.stringify({ page: name, error: e.message }) + '\n');
    }
  }
  ws.close(); chrome.kill('SIGKILL'); process.exit(0);
})().catch(e => { console.error('FATAL ' + e.message); process.exit(2); });
