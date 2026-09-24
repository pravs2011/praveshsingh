#!/usr/bin/env node
/**
 * Headless behaviour tests for js/consent.js (GDPR consent gate).
 * Plain Node, no dependencies:  node tools/consent-behaviour.test.js
 *
 * Simulates a browser with a minimal DOM + localStorage mock and runs the
 * real consent.js source in a VM sandbox, asserting the legally relevant
 * behaviour: nothing loads before consent, opt-in loads GA, choices persist,
 * and the settings panel can be reopened at any time.
 */
'use strict';

const fs = require('fs');
const vm = require('vm');
const path = require('path');

const CODE = fs.readFileSync(path.join(__dirname, '..', 'js', 'consent.js'), 'utf8');

let passed = 0;
let failed = 0;
function assert(cond, msg) {
  if (cond) { passed++; console.log('  ok    ' + msg); }
  else { failed++; console.log('  FAIL  ' + msg); }
}

/* ------------------------------------------------------------------ */
/* Minimal DOM mock                                                    */
/* ------------------------------------------------------------------ */

const VOID_TAGS = new Set(['input', 'br', 'img', 'meta', 'link', 'hr', 'source']);

class FakeElement {
  constructor(tag) {
    this.tagName = String(tag).toLowerCase();
    this.children = [];
    this.parentNode = null;
    this._handlers = {};
    this._attrs = {};
    this.hidden = false;
    this.checked = false;
    this.id = '';
    this.className = '';
    this.style = {};
    this.textContent = '';
    this.src = '';
    this.focus = () => {};
  }
  setAttribute(k, v) {
    this._attrs[k] = String(v);
    if (k === 'id') this.id = String(v);
    if (k === 'class') this.className = String(v);
  }
  getAttribute(k) {
    return Object.prototype.hasOwnProperty.call(this._attrs, k) ? this._attrs[k] : null;
  }
  appendChild(child) { child.parentNode = this; this.children.push(child); return child; }
  addEventListener(type, fn) { (this._handlers[type] = this._handlers[type] || []).push(fn); }
  /* Dispatch with DOM-style bubbling to ancestor handlers. */
  dispatch(type, evt) {
    let el = this;
    while (el) {
      (el._handlers[type] || []).slice().forEach((fn) => fn.call(el, evt));
      el = el.parentNode;
    }
  }

  matches(sel) {
    if (sel.startsWith('#')) return this.id === sel.slice(1);
    if (sel.startsWith('.')) return (' ' + this.className + ' ').includes(' ' + sel.slice(1) + ' ');
    const m = sel.match(/^\[([^\]=~^$*]+)(?:="([^"]*)")?\]$/);
    if (m) {
      if (!Object.prototype.hasOwnProperty.call(this._attrs, m[1])) return false;
      return m[2] === undefined || this._attrs[m[1]] === m[2];
    }
    return this.tagName === sel.toLowerCase();
  }
  closest(sel) {
    let el = this;
    while (el) { if (el.matches && el.matches(sel)) return el; el = el.parentNode; }
    return null;
  }
  querySelectorAll(sel) {
    const out = [];
    const walk = (el) => {
      el.children.forEach((c) => { if (c.matches(sel)) out.push(c); walk(c); });
    };
    walk(this);
    return out;
  }
  querySelector(sel) { return this.querySelectorAll(sel)[0] || null; }
  set innerHTML(html) { this.children = []; parseHTML(this, html); }
  get innerHTML() { return ''; }
}

function parseHTML(parent, html) {
  const tokens = html.match(/<\/?[a-zA-Z][^>]*>|[^<]+/g) || [];
  const stack = [parent];
  for (const tok of tokens) {
    if (!tok.startsWith('<')) continue;
    if (tok.startsWith('</')) { if (stack.length > 1) stack.pop(); continue; }
    const m = tok.match(/^<([a-zA-Z][a-zA-Z0-9]*)((?:\s+[^<>]*?)?)(\/?)>$/);
    if (!m) continue;
    const el = new FakeElement(m[1].toLowerCase());
    const re = /([a-zA-Z_:][-a-zA-Z0-9_:.]*)(?:\s*=\s*"([^"]*)"|\s*=\s*'([^']*)')?/g;
    let am;
    while ((am = re.exec(m[2] || ''))) {
      el.setAttribute(am[1], am[2] !== undefined ? am[2] : (am[3] !== undefined ? am[3] : ''));
    }
    stack[stack.length - 1].appendChild(el);
    if (!VOID_TAGS.has(el.tagName) && m[3] !== '/') stack.push(el);
  }
}

function freshEnv(stored) {
  const store = new Map();
  if (stored) store.set('ps_consent_v1', JSON.stringify(stored));

  const document = new FakeElement('#document');
  const head = document.appendChild(new FakeElement('head'));
  const body = document.appendChild(new FakeElement('body'));
  document.head = head;
  document.body = body;
  document.createElement = (tag) => new FakeElement(tag);

  const docHandlers = {};
  document.addEventListener = (type, fn) => { (docHandlers[type] = docHandlers[type] || []).push(fn); };
  document.dispatchDoc = (type, evt) => (docHandlers[type] || []).slice().forEach((fn) => fn(evt));

  const window = {
    localStorage: {
      getItem: (k) => (store.has(k) ? store.get(k) : null),
      setItem: (k, v) => store.set(k, String(v)),
      removeItem: (k) => store.delete(k),
    },
  };
  vm.runInContext(CODE, vm.createContext({ window, document, Element: FakeElement, Date, console }));

  return {
    window, document, head, body, store,
    banner: () => body.children.find((c) => c.id === 'ps-consent') || null,
    gaScripts: () => head.children.filter((c) => c.tagName === 'script' && c.src),
    lastConsent: () => {
      const es = (window.dataLayer || [])
        .map((a) => Array.from(a))
        .filter((x) => x[0] === 'consent');
      return es.length ? es[es.length - 1][2] : null;
    },
    hasEvent: () => (window.dataLayer || []).some((a) => Array.from(a)[0] === 'event'),
  };
}

/* ------------------------------------------------------------------ */
/* Scenarios                                                           */
/* ------------------------------------------------------------------ */

console.log('\n[1] First visit — nothing loads before consent');
let env = freshEnv();
let b = env.banner();
assert(!!b && !b.hidden, 'banner is shown on first visit');
assert(env.lastConsent() && env.lastConsent().analytics_storage === 'denied', 'consent default: analytics_storage denied');
assert(env.gaScripts().length === 0, 'no GA script injected before any choice');
assert(!env.hasEvent(), 'no events in the dataLayer');

console.log('\n[2] Cached page stub fires gtag after consent.js — gate must hold');
env.window.gtag('consent', 'default', { analytics_storage: 'denied' });
assert(env.lastConsent().analytics_storage === 'denied', 'page-level consent default still passes through');
env.window.gtag('event', 'cta_click', { section: 'hero' });
assert(!env.hasEvent(), 'pre-consent custom events are dropped');

console.log('\n[3] Accept — GA loads, choice persists, events flow');
env = freshEnv();
b = env.banner();
const accept = b.querySelector('[data-pscc="accept"]');
accept.dispatch('click', { target: accept });
assert(env.lastConsent() && env.lastConsent().analytics_storage === 'granted', 'consent update granted');
assert(env.gaScripts().length === 1 && env.gaScripts()[0].src.includes('googletagmanager.com/gtag/js'), 'GA script injected after opt-in');
const saved = JSON.parse(env.store.get('ps_consent_v1'));
assert(saved.analytics === true && saved.v === 1 && typeof saved.ts === 'string', 'choice persisted with version + timestamp');
assert(b.hidden === true, 'banner hidden after choice');
env.window.gtag('event', 'page_view');
assert(env.hasEvent(), 'custom events flow after opt-in');

console.log('\n[4] Reject — GA never loads');
env = freshEnv();
b = env.banner();
const reject = b.querySelector('[data-pscc="reject"]');
reject.dispatch('click', { target: reject });
assert(env.lastConsent() && env.lastConsent().analytics_storage === 'denied', 'consent stays denied after reject');
assert(env.gaScripts().length === 0, 'GA never injected after reject');
assert(b.hidden === true, 'banner hidden after reject');

console.log('\n[5] Customize — save with analytics unchecked stays denied');
env = freshEnv();
b = env.banner();
b.querySelector('[data-pscc="customize"]').dispatch('click', { target: b.querySelector('[data-pscc="customize"]') });
const viewMain = b.querySelector('[data-pscc-view="main"]');
const viewPrefs = b.querySelector('[data-pscc-view="prefs"]');
assert(!viewPrefs.hidden && viewMain.hidden, 'customize opens the preferences panel');
b.querySelector('[data-pscc="save"]').dispatch('click', { target: b.querySelector('[data-pscc="save"]') });
assert(env.lastConsent().analytics_storage === 'denied', 'unchecked analytics saved as denied');

console.log('\n[6] Returning visitor (opted in) — GA loads, no banner');
env = freshEnv({ v: 1, ts: '2026-09-24T00:00:00.000Z', analytics: true });
assert(!env.banner(), 'no banner shown');
assert(env.gaScripts().length === 1, 'GA loads for returning opted-in visitor');
assert(env.lastConsent().analytics_storage === 'granted', 'granted state re-applied on load');

console.log('\n[7] Returning visitor (opted out) — nothing loads, no nagging');
env = freshEnv({ v: 1, ts: '2026-09-24T00:00:00.000Z', analytics: false });
assert(!env.banner(), 'no banner shown');
assert(env.gaScripts().length === 0, 'GA does not load');
env.window.gtag('event', 'cta_click', {});
assert(!env.hasEvent(), 'events still dropped while opted out');

console.log('\n[8] Footer "Cookie settings" + Escape key');
env = freshEnv({ v: 1, ts: '2026-09-24T00:00:00.000Z', analytics: false });
const link = new FakeElement('a');
link.setAttribute('data-consent-settings', '');
link.setAttribute('href', 'privacy.html');
env.document.dispatchDoc('click', { target: link, preventDefault: () => {} });
b = env.banner();
assert(!!b && !b.hidden, 'footer link re-opens the consent panel');
assert(!b.querySelector('[data-pscc-view="prefs"]').hidden, 'preferences view is shown');
env.document.dispatchDoc('keydown', { key: 'Escape' });
assert(b.hidden, 'Escape hides the panel');

console.log('\n[9] Corrupt / missing storage — falls back to asking, stays denied');
env = freshEnv();
env.store.set('ps_consent_v1', '{not json');
env = freshEnv();
assert(env.banner() && !env.banner().hidden, 'banner shown when stored state is unreadable');

/* ------------------------------------------------------------------ */

console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
