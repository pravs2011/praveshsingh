# Analytics inclusion — praveshsingh.com

> **DEPRECATED (2026-09-24):** the raw `gtag.js` loader below was removed from
> every page. Loading GA4 without consent violates the EU/UK GDPR + ePrivacy
> rules and risks the site being blocked or fined for EU/US visitors.
>
> **Use the consent-mode pattern instead (this is the ONLY sanctioned setup):**

```html
<!-- Cookie consent & consent-gated analytics — see /privacy.html -->
<script src="/js/consent.js" defer></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('consent', 'default', {
    'anonymize_ip': true,
    'analytics_storage': 'denied',
    'ad_storage': 'denied',
    'ad_user_data': 'denied',
    'ad_personalization': 'denied',
    'functionality_storage': 'denied',
    'personalization_storage': 'denied',
    'security_storage': 'granted'
  });
</script>
```

- `js/consent.js` shows the cookie banner, stores the choice in
  `localStorage["ps_consent_v1"]`, and injects the GA4 tag **only** after an
  explicit opt-in. `js/consent.js` is the single source of truth for the
  measurement ID (`G-2XHZ5NJZLK`).
- `make_build.sh` fails the build if any shipped page is missing this block.

## Do NOT add

- Google Tag Manager (`GTM-M335RXDF`) — container not in use; adding it would
  bypass the consent gate. Delete this section if GTM is ever properly wired
  into consent mode.
- Any ad, remarketing, or cross-site tracking tag. The privacy policy
  (`privacy.html`) promises none, and `ad_*` consent signals stay denied.
