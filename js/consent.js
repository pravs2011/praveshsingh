/*!
 * praveshsingh.com — cookie consent & consent-gated analytics
 * ------------------------------------------------------------
 * - GDPR / ePrivacy (EU-EEA-UK): Google Analytics 4 stays fully denied
 *   until the visitor opts in; nothing is set or transmitted before that.
 * - CCPA/CPRA (California): analytics can be opted out at any time via
 *   "Cookie settings"; the site does not sell or share personal data.
 * - DPDP Act 2023 (India): consent is free, specific, informed and
 *   revocable — the choice is stored locally and can be changed anytime.
 *
 * Storage: one localStorage entry ("ps_consent_v1") holding only the
 * visitor's choice and its timestamp. No personal data is stored.
 *
 * Public API:  window.openConsentSettings()  — re-opens the preferences
 *              panel. Any element with [data-consent-settings] opens it
 *              on click (used by the footer "Cookie settings" link).
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'ps_consent_v1';
  var STATE_VERSION = 1;
  var GA_ID = 'G-2XHZ5NJZLK';

  /* ---------------------------------------------------------------
   * 1. gtag shim — consent defaults BEFORE any Google tag can load.
   * --------------------------------------------------------------- */
  window.dataLayer = window.dataLayer || [];

  function readState() {
    try {
      var raw = window.localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      var s = JSON.parse(raw);
      return (s && s.v === STATE_VERSION) ? s : null;
    } catch (err) {
      return null;
    }
  }

  function analyticsGranted() {
    var s = readState();
    return !!(s && s.analytics);
  }

  /**
   * Consent-aware gtag shim. 'consent' commands always pass through;
   * custom 'event' commands queued before an opt-in are dropped so no
   * pre-consent interaction is ever transmitted or replayed later.
   */
  function gtagGate() {
    if (arguments[0] === 'event' && !analyticsGranted()) return;
    window.dataLayer.push(arguments);
  }
  /* Always install the gate: any inline stub from cached pages is replaced,
   * so custom events fired before an opt-in are never queued for GA. */
  window.gtag = gtagGate;

  window.gtag('consent', 'default', {
    analytics_storage: 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    functionality_storage: 'denied',
    personalization_storage: 'denied',
    security_storage: 'granted',
    wait_for_update: 500
  });
  window.gtag('set', 'ads_data_redaction', true);

  /* ---------------------------------------------------------------
   * 2. Persist the decision (choice + timestamp only).
   * --------------------------------------------------------------- */
  function persist(analytics) {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify({
        v: STATE_VERSION,
        ts: new Date().toISOString(),
        analytics: !!analytics
      }));
    } catch (err) {
      /* Storage blocked: stay denied; the banner re-asks next visit. */
    }
  }

  /* ---------------------------------------------------------------
   * 3. GA4 is injected ONLY after an explicit opt-in.
   * --------------------------------------------------------------- */
  var gaLoaded = false;

  function loadAnalytics() {
    if (gaLoaded) return;
    gaLoaded = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    window.gtag('js', new Date());
    window.gtag('config', GA_ID, { anonymize_ip: true });
  }

  function applyDecision(state) {
    window.gtag('consent', 'update', {
      analytics_storage: state.analytics ? 'granted' : 'denied',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied'
    });
    if (state.analytics) loadAnalytics();
  }

  /* ---------------------------------------------------------------
   * 4. Banner / preferences UI (matches the site's dark theme).
   * --------------------------------------------------------------- */
  var openedFromSettings = false;
  var root = null;
  var viewMain = null;
  var viewPrefs = null;
  var analyticsCheckbox = null;

  var CSS = [
    '.pscc{position:fixed;left:16px;right:16px;bottom:16px;z-index:9500;display:flex;justify-content:center;pointer-events:none;}',
    '.pscc[hidden]{display:none;}',
    '.pscc__card{pointer-events:auto;width:min(560px,100%);background:rgba(13,17,26,0.97);',
    'border:1px solid rgba(255,255,255,0.14);border-radius:14px;box-shadow:0 24px 64px rgba(0,0,0,0.6);',
    'padding:20px 22px;color:#e8ecf4;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;',
    'backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);}',
    '.pscc__title{margin:0 0 6px;font-size:0.95rem;font-weight:700;color:#ffffff;}',
    '.pscc__text{margin:0 0 14px;font-size:0.85rem;color:#aab3c5;line-height:1.55;}',
    '.pscc__text a{color:#93c5fd;text-decoration:underline;}',
    '.pscc__actions{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:4px;}',
    '.pscc__btn{cursor:pointer;border-radius:8px;font-family:inherit;transition:background 0.2s ease,border-color 0.2s ease;}',
    '.pscc__btn--primary{background:linear-gradient(135deg,#4f46e5,#4338ca);color:#ffffff;',
    'border:1px solid rgba(255,255,255,0.15);padding:8px 18px;font-size:0.85rem;font-weight:600;}',
    '.pscc__btn--primary:hover{background:linear-gradient(135deg,#6366f1,#4f46e5);}',
    '.pscc__btn--ghost{background:transparent;color:#e8ecf4;border:1px solid rgba(255,255,255,0.18);',
    'padding:8px 16px;font-size:0.85rem;font-weight:500;}',
    '.pscc__btn--ghost:hover{border-color:rgba(255,255,255,0.35);}',
    '.pscc__btn--link{background:none;border:none;color:#94a3b8;font-size:0.82rem;',
    'text-decoration:underline;padding:8px 4px;}',
    '.pscc__btn--link:hover{color:#ffffff;}',
    '.pscc__opt{display:flex;gap:10px;align-items:flex-start;padding:10px 12px;',
    'border:1px solid rgba(255,255,255,0.1);border-radius:8px;margin-bottom:10px;',
    'font-size:0.85rem;color:#c3cadb;cursor:pointer;line-height:1.5;}',
    '.pscc__opt--locked{opacity:0.7;cursor:default;}',
    '.pscc__opt input{margin-top:3px;accent-color:#6366f1;}',
    '.pscc__opt strong{color:#ffffff;}',
    '.pscc__fine{margin:12px 0 0;font-size:0.75rem;color:#7d8698;}',
    '.pscc__fine a{color:#93c5fd;}',
    '@media (max-width:560px){.pscc{left:10px;right:10px;bottom:10px;}.pscc__card{padding:16px;}}',
    '@media (prefers-reduced-motion: reduce){.pscc *{transition:none!important;}}'
  ].join('');

  function buildUI() {
    if (root) return;

    var style = document.createElement('style');
    style.id = 'ps-consent-style';
    style.textContent = CSS;
    document.head.appendChild(style);

    root = document.createElement('div');
    root.className = 'pscc';
    root.id = 'ps-consent';
    root.hidden = true;
    root.innerHTML =
      '<div class="pscc__card" role="region" aria-label="Cookie consent">' +
        '<div class="pscc__view" data-pscc-view="main">' +
          '<p class="pscc__title">Cookies &amp; privacy</p>' +
          '<p class="pscc__text">We use one analytics cookie (Google Analytics, IP-anonymised) to understand which pages are useful — nothing loads before you choose. No advertising or cross-site tracking, ever. <a href="/privacy.html">Privacy &amp; Cookie Policy</a></p>' +
          '<div class="pscc__actions">' +
            '<button type="button" class="pscc__btn pscc__btn--ghost" data-pscc="reject">Reject</button>' +
            '<button type="button" class="pscc__btn pscc__btn--link" data-pscc="customize">Customize</button>' +
            '<button type="button" class="pscc__btn pscc__btn--primary" data-pscc="accept">Accept</button>' +
          '</div>' +
        '</div>' +
        '<div class="pscc__view" data-pscc-view="prefs" hidden>' +
          '<p class="pscc__title">Cookie preferences</p>' +
          '<label class="pscc__opt pscc__opt--locked">' +
            '<input type="checkbox" checked disabled>' +
            '<span><strong>Strictly necessary</strong> — remembers your cookie choice. Always on.</span>' +
          '</label>' +
          '<label class="pscc__opt">' +
            '<input type="checkbox" data-pscc-analytics>' +
            '<span><strong>Analytics</strong> — Google Analytics 4, IP-anonymised, used only to count page visits and improve content.</span>' +
          '</label>' +
          '<div class="pscc__actions">' +
            '<button type="button" class="pscc__btn pscc__btn--link" data-pscc="back">Back</button>' +
            '<button type="button" class="pscc__btn pscc__btn--primary" data-pscc="save">Save preferences</button>' +
          '</div>' +
          '<p class="pscc__fine">You can change this anytime via “Cookie settings” in the footer. Details: <a href="/privacy.html">Privacy &amp; Cookie Policy</a></p>' +
        '</div>' +
      '</div>';
    document.body.appendChild(root);

    viewMain = root.querySelector('[data-pscc-view="main"]');
    viewPrefs = root.querySelector('[data-pscc-view="prefs"]');
    analyticsCheckbox = root.querySelector('[data-pscc-analytics]');

    root.addEventListener('click', function (e) {
      var btn = e.target instanceof Element ? e.target.closest('[data-pscc]') : null;
      if (!btn) return;
      var action = btn.getAttribute('data-pscc');
      if (action === 'accept') decide(true);
      else if (action === 'reject') decide(false);
      else if (action === 'customize') showView('prefs', false);
      else if (action === 'back') {
        if (openedFromSettings) hide();
        else showView('main', false);
      } else if (action === 'save') {
        decide(analyticsCheckbox && analyticsCheckbox.checked);
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !root.hidden) hide();
    });
  }

  function showView(view, fromSettings) {
    openedFromSettings = !!fromSettings;
    viewMain.hidden = view !== 'main';
    viewPrefs.hidden = view !== 'prefs';
    if (view === 'prefs') {
      analyticsCheckbox.checked = analyticsGranted();
      var saveBtn = root.querySelector('[data-pscc="save"]');
      if (saveBtn) saveBtn.focus();
    } else {
      var acceptBtn = root.querySelector('[data-pscc="accept"]');
      if (acceptBtn) acceptBtn.focus();
    }
    root.hidden = false;
  }

  function hide() {
    if (root) root.hidden = true;
  }

  function decide(analytics) {
    persist(analytics);
    applyDecision({ analytics: !!analytics });
    hide();
  }

  /**
   * Re-opens the preferences panel (footer "Cookie settings", privacy page).
   */
  function openConsentSettings() {
    buildUI();
    showView('prefs', true);
  }
  window.openConsentSettings = openConsentSettings;

  /* Footer / inline [data-consent-settings] links open the panel. */
  document.addEventListener('click', function (e) {
    if (!(e.target instanceof Element)) return;
    var trigger = e.target.closest('[data-consent-settings]');
    if (!trigger) return;
    e.preventDefault();
    openConsentSettings();
  }, { passive: false });

  /* ---------------------------------------------------------------
   * 5. Init: apply a previous decision, otherwise show the banner.
   *    (This file is loaded with `defer`, so the DOM is ready.)
   * --------------------------------------------------------------- */
  var existing = readState();
  if (existing) {
    applyDecision(existing);
  } else {
    buildUI();
    showView('main', false);
  }
})();
