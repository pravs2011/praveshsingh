#!/bin/bash
TITLE="$1"
DESC="$2"
KEYWORDS="$3"
PAGE="$4"
OUT="$5"

cat << 'HEADER' > "$OUT"
<!DOCTYPE html>
<html lang="en-IN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- =========================================================
       SEO, AIO & GEO FOUNDATION
       ========================================================= -->
  <title>__TITLE__</title>
  <meta name="description" content="__DESC__">
  <meta name="author" content="Pravesh Singh">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="googlebot" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="keywords" content="__KEYWORDS__">
  <meta name="theme-color" content="#090b10">
  <meta name="color-scheme" content="dark">
  <link rel="canonical" href="https://praveshsingh.com/__PAGE__">

  <!-- Machine-readable discovery (llms.txt spec link relations) -->
  <link rel="describedby" type="text/plain" href="https://praveshsingh.com/llms.txt" title="Site index for language models">
  <link rel="describedby" type="text/plain" href="https://praveshsingh.com/llms-full.txt" title="Full site context for language models">
  <link rel="security-policy" href="https://praveshsingh.com/.well-known/security.txt">

  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="__TITLE__">
  <meta property="og:description" content="__DESC__">
  <meta property="og:url" content="https://praveshsingh.com/__PAGE__">
  <meta property="og:site_name" content="Pravesh Singh">
  <meta property="og:locale" content="en_IN">
  <meta property="og:image" content="https://praveshsingh.com/images/pravesh-singh.png">
  <meta property="og:image:secure_url" content="https://praveshsingh.com/images/pravesh-singh.png">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1102">
  <meta property="og:image:height" content="1427">
  <meta property="og:image:alt" content="Portrait of Pravesh Singh">
  <meta property="profile:first_name" content="Pravesh">
  <meta property="profile:last_name" content="Singh">

  <!-- Twitter / X Cards -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="__TITLE__">
  <meta name="twitter:description" content="__DESC__">
  <meta name="twitter:image" content="https://praveshsingh.com/images/pravesh-singh.png">
  <meta name="twitter:image:alt" content="Portrait of Pravesh Singh">

  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='22' fill='%23090b10'/%3E%3Ctext x='50' y='66' text-anchor='middle' font-family='-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif' font-size='50' font-weight='700' fill='%236366f1'%3EPS%3C/text%3E%3C/svg%3E">

  <!-- =========================================================
       STRUCTURED DATA (JSON-LD for Schema.org, Search & LLM Engines)
       ========================================================= -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "ProfilePage",
        "@id": "https://praveshsingh.com/__PAGE__#profile",
        "url": "https://praveshsingh.com/__PAGE__",
        "name": "__TITLE__",
        "description": "__DESC__",
        "inLanguage": "en-IN",
        "dateModified": "2026-09-21",
        "isPartOf": {"@id": "https://praveshsingh.com/#website"},
        "mainEntity": {"@id": "https://praveshsingh.com/#person"},
        "breadcrumb": {"@id": "https://praveshsingh.com/__PAGE__#breadcrumb"}
      },
      {
        "@type": "BreadcrumbList",
        "@id": "https://praveshsingh.com/__PAGE__#breadcrumb",
        "itemListElement": [
          {
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "https://praveshsingh.com/"
          },
          {
            "@type": "ListItem",
            "position": 2,
            "name": "__PAGE_NAME__",
            "item": "https://praveshsingh.com/__PAGE__"
          }
        ]
      },
      {
        "@type": "Person",
        "@id": "https://praveshsingh.com/#person",
        "name": "Pravesh Singh",
        "givenName": "Pravesh",
        "familyName": "Singh",
        "url": "https://praveshsingh.com/",
        "jobTitle": ["Founder", "Chief Technology Officer", "Managing Director", "Software Architect"],
        "description": "Pravesh Singh is an Indian software architect, technology entrepreneur, and the Founder & CTO of SoftEdge Technology Solutions.",
        "image": {
          "@type": "ImageObject",
          "url": "https://praveshsingh.com/images/pravesh-singh.png",
          "caption": "Pravesh Singh"
        },
        "worksFor": {
          "@type": "Organization",
          "@id": "https://softedgetechnology.com/#organization",
          "name": "SoftEdge Technology Solutions",
          "url": "https://softedgetechnology.com/"
        },
        "sameAs": [
          "https://www.linkedin.com/in/praveshsingh/",
          "https://softedgetechnology.com/"
        ]
      }
    ]
  }
  </script>

  <style>
    /* =========================================================
       BASE & RESET
       ========================================================= */
    :root {
      --bg: #090b10;
      --bg-surface: #10141d;
      --bg-surface-elevated: #151a26;
      --border: rgba(255, 255, 255, 0.08);
      --border-hover: rgba(255, 255, 255, 0.16);
      --text: #f0f3f8;
      --text-muted: #9aa3b5;
      --text-sub: #6f788b;
      --primary: #6366f1;
      --primary-soft: rgba(99, 102, 241, 0.12);
      --primary-border: rgba(99, 102, 241, 0.32);
      --teal: #0ea5e9;
      --green: #10b981;
      --green-soft: rgba(16, 185, 129, 0.12);
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 22px;
      --transition: 0.2s ease;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; font-size: 16px; }
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      line-height: 1.65;
      -webkit-font-smoothing: antialiased;
      position: relative;
    }

    .container {
      width: min(1140px, 92%);
      margin: 0 auto;
    }

    a { color: inherit; text-decoration: none; transition: var(--transition); }
    img { display: block; max-width: 100%; height: auto; }

    /* =========================================================
       NAVIGATION
       ========================================================= */
    header {
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(9, 11, 16, 0.88);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border);
    }
    header nav {
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 72px;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-avatar {
      width: 38px;
      height: 38px;
      border-radius: 50%;
      object-fit: cover;
      border: 1px solid var(--border-hover);
    }
    .brand-text { display: flex; flex-direction: column; line-height: 1.2; }
    .brand-name { font-size: 1rem; font-weight: 700; color: #ffffff; }
    .brand-role { font-size: 0.74rem; color: var(--text-muted); }

    .nav-links {
      display: flex;
      gap: 26px;
      align-items: center;
    }
    .nav-link {
      color: var(--text-muted);
      font-size: 0.92rem;
      font-weight: 500;
      transition: var(--transition);
    }
    .nav-link:hover, .nav-link.active { color: #ffffff; }

    .nav-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 9px 18px;
      border-radius: 8px;
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      border: 1px solid var(--border);
      background: var(--bg-surface);
      color: var(--text);
      transition: var(--transition);
      white-space: nowrap;
    }
    .btn:hover {
      background: var(--bg-surface-elevated);
      border-color: var(--border-hover);
      color: #ffffff;
    }
    .btn-primary {
      background: var(--primary);
      border-color: var(--primary);
      color: #ffffff;
    }
    .btn-primary:hover {
      background: #5457e5;
      border-color: #5457e5;
    }

    .hamburger {
      display: none;
      background: none;
      border: none;
      cursor: pointer;
      padding: 6px;
      color: var(--text);
    }
    .mobile-menu {
      display: none;
      flex-direction: column;
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border);
      padding: 16px 24px 22px;
      gap: 14px;
    }
    .mobile-menu.open { display: flex; }

    /* =========================================================
       HERO SECTION
       ========================================================= */
    .hero {
      padding: 72px 0 84px;
    }
    .hero-grid {
      display: grid;
      grid-template-columns: 1.2fr 0.8fr;
      gap: 56px;
      align-items: center;
      margin-top: 20px;
    }
    .crumb {
      font-size: 0.85rem;
      font-weight: 500;
      color: var(--text-muted);
      margin-bottom: 24px;
    }
    .crumb a { color: var(--primary); }
    .crumb a:hover { color: #818cf8; }
    .crumb span { color: #ffffff; }

    .hero-title {
      font-size: clamp(2.3rem, 4.4vw, 3.6rem);
      line-height: 1.15;
      letter-spacing: -0.035em;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 20px;
    }
    .hero-title span {
      color: #a5b4fc;
    }
    .hero-lead {
      font-size: 1.1rem;
      color: var(--text-muted);
      line-height: 1.75;
      margin-bottom: 30px;
      max-width: 640px;
    }
    .hero-actions {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 44px;
    }

    /* =========================================================
       INNER CONTENT & SECTIONS
       ========================================================= */
    section {
      padding: 84px 0;
      border-top: 1px solid var(--border);
    }
    .section-head {
      margin-bottom: 44px;
      max-width: 760px;
    }
    .section-eyebrow {
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--teal);
      margin-bottom: 10px;
    }
    .section-title {
      font-size: clamp(1.85rem, 3.2vw, 2.5rem);
      letter-spacing: -0.03em;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.22;
      margin-bottom: 14px;
    }
    .section-desc {
      font-size: 1.05rem;
      color: var(--text-muted);
      line-height: 1.7;
    }

    /* Sub-pages standard grid layout */
    .content-layout {
      display: grid;
      grid-template-columns: 1.8fr 1fr;
      gap: 56px;
      align-items: start;
    }
    .content-prose {
      font-size: 1.02rem;
      color: #cbd5e1;
      line-height: 1.75;
    }
    .content-prose p { margin-bottom: 20px; }
    .content-prose p:last-child { margin-bottom: 0; }
    .content-prose h3 {
      font-size: 1.35rem;
      font-weight: 700;
      color: #ffffff;
      margin: 36px 0 16px;
      letter-spacing: -0.01em;
    }
    .content-prose h3:first-child { margin-top: 0; }
    
    .content-list {
      list-style: none;
      margin-bottom: 24px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .content-list li {
      padding-left: 20px;
      position: relative;
    }
    .content-list li::before {
      content: "→";
      position: absolute;
      left: 0;
      color: var(--teal);
      font-weight: bold;
    }

    .sidebar-card {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 24px;
      position: sticky;
      top: 96px;
    }
    .sidebar-title {
      font-size: 1.05rem;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 16px;
    }
    .sidebar-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .sidebar-list li {
      font-size: 0.9rem;
      color: var(--text-muted);
      display: flex;
      flex-direction: column;
    }
    .sidebar-label {
      font-size: 0.76rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-sub);
      margin-bottom: 2px;
      font-weight: 600;
    }
    
    /* Code / Diagram block */
    pre.diagram {
      background: #05070a;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 20px;
      overflow-x: auto;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.85rem;
      line-height: 1.5;
      color: #94a3b8;
      margin: 24px 0;
    }

    /* =========================================================
       FOOTER
       ========================================================= */
    footer {
      border-top: 1px solid var(--border);
      padding: 36px 0;
      color: var(--text-muted);
      font-size: 0.86rem;
    }
    .footer-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }
    .footer-links {
      display: flex;
      gap: 20px;
    }
    .footer-links a:hover { color: #ffffff; }

    /* =========================================================
       RESPONSIVE BREAKPOINTS
       ========================================================= */
    @media (max-width: 980px) {
      .hero-grid { grid-template-columns: 1fr; gap: 44px; }
      .content-layout { grid-template-columns: 1fr; }
      .sidebar-card { position: static; }
    }

    @media (max-width: 720px) {
      .nav-links, .nav-actions .btn { display: none; }
      .hamburger { display: block; }
      .hero-title { font-size: 2.3rem; }
      .footer-row { flex-direction: column; align-items: flex-start; }
    }
  </style>

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

  <!-- GA4 custom events: CTA clicks, contact clicks, form leads -->
  <script>
    (function () {
      function track(name, params) {
        if (typeof gtag === 'function') gtag('event', name, params || {});
      }
      window.trackEvent = track;

      document.addEventListener('click', function (e) {
        var el = e.target instanceof Element ? e.target : null;
        if (!el) return;

        var link = el.closest('a[href]');
        if (link) {
          var href = link.getAttribute('href') || '';
          var text = (link.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 80);
          var host = link.closest('section[id], header, footer');
          var section = host ? (host.id || host.tagName.toLowerCase()) : 'page';

          if (/^mailto:|^tel:/i.test(href)) {
            track('generate_lead', {
              method: /^mailto:/i.test(href) ? 'email' : 'phone',
              link_text: text,
              section: section
            });
            return;
          }
          if (link.closest('.btn')) {
            track('cta_click', {
              cta_text: text,
              link_url: href,
              link_type: /^https?:\/\//i.test(href) ? 'external' : 'internal',
              section: section
            });
          }
          // Plain text links: outbound handled by GA4 enhanced measurement
          return;
        }

        var btn = el.closest('button, [role="button"]');
        if (btn) {
          var bHost = btn.closest('section[id], header, footer');
          track('cta_click', {
            cta_text: (btn.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 80),
            link_type: 'button',
            section: bHost ? (bHost.id || bHost.tagName.toLowerCase()) : 'page'
          });
        }
      }, { passive: true });
    })();
  </script>
</head>

<body>

  <!-- =========================================================
       HEADER & NAVIGATION
       ========================================================= -->
  <header>
    <div class="container">
      <nav aria-label="Main Navigation">
        <a href="/" class="brand" aria-label="Pravesh Singh homepage">
          <picture>
            <source srcset="images/pravesh-singh.webp" type="image/webp">
            <img class="brand-avatar" src="images/pravesh-singh.png" alt="Pravesh Singh" width="38" height="38" loading="eager">
          </picture>
          <div class="brand-text">
            <span class="brand-name">Pravesh Singh</span>
            <span class="brand-role">SoftEdge Technology Solutions</span>
          </div>
        </a>

        <div class="nav-links">
          <a href="/" class="nav-link">Home</a>
          <a href="about.html" class="nav-link__ABOUT_CLASS__">About</a>
          <a href="icare.html" class="nav-link__ICARE_CLASS__">iCare</a>
          <a href="taskedge.html" class="nav-link__TASKEDGE_CLASS__">TaskEdge</a>
          <a href="automation.html" class="nav-link__AUTOMATION_CLASS__">AI Solutions</a>
          <a href="industries.html" class="nav-link__INDUSTRIES_CLASS__">Industries</a>
          <a href="expertise.html" class="nav-link">Expertise</a>
          <a href="writing/" class="nav-link">Writing</a>
        </div>

        <div class="nav-actions">
          <a href="/#contact" class="btn btn-primary">Get in touch</a>
          <button class="hamburger" id="hamburgerBtn" aria-label="Toggle navigation menu" aria-expanded="false">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 6h16M4 12h16M4 18h16"/>
            </svg>
          </button>
        </div>
      </nav>
    </div>

  </header>

  <!-- Mobile Drawer: must stay OUTSIDE <header> — the header's backdrop-filter
       creates a containing block that clamps position:fixed descendants to the
       72px header box, hiding the drawer behind page content. -->
  <div class="mobile-menu" id="mobileMenu" aria-hidden="true">
    <a href="/" class="nav-link" onclick="closeMobileMenu()">Home</a>
    <a href="about.html" class="nav-link__ABOUT_CLASS__" onclick="closeMobileMenu()">About Pravesh</a>
    <a href="/#software" class="nav-link" onclick="closeMobileMenu()">Products & Systems</a>
    <a href="icare.html" class="nav-link__ICARE_CLASS__" onclick="closeMobileMenu()" style="padding-left:24px; font-size:0.85rem; color:var(--text-sub);">↳ iCare Case Study</a>
    <a href="taskedge.html" class="nav-link__TASKEDGE_CLASS__" onclick="closeMobileMenu()" style="padding-left:24px; font-size:0.85rem; color:var(--text-sub);">↳ TaskEdge SaaS</a>
    <a href="automation.html" class="nav-link__AUTOMATION_CLASS__" onclick="closeMobileMenu()">AI Solutions</a>
    <a href="industries.html" class="nav-link__INDUSTRIES_CLASS__" onclick="closeMobileMenu()">Industries</a>
    <a href="/#events" class="nav-link" onclick="closeMobileMenu()">Talks & Workshops</a>
    <a href="expertise.html" class="nav-link" onclick="closeMobileMenu()">Technical Expertise</a>
    <a href="writing/" class="nav-link" onclick="closeMobileMenu()">Writing & Insights</a>
    <a href="/#contact" class="btn btn-primary" style="margin-top:10px;" onclick="closeMobileMenu()">Get in touch</a>
  </div>

__BODY__

  <!-- =========================================================
       FOOTER
       ========================================================= -->
  <footer>
    <div class="container">
      <div class="footer-row">
        <div>
          <div style="font-weight:600; color:#ffffff;">Pravesh Singh</div>
          <div style="font-size:0.8rem; color:var(--text-sub); margin-top:2px;">
            Managing Director & CTO, SoftEdge Technology Solutions · praveshsingh.com
          </div>
        </div>

        <div class="footer-links">
          <a href="about.html">About</a>
          <a href="icare.html">iCare</a>
          <a href="taskedge.html">TaskEdge</a>
          <a href="automation.html">AI Solutions</a>
          <a href="industries.html">Industries</a>
          <a href="expertise.html">Expertise</a>
          <a href="writing/">Writing</a>
          <a href="speaking.html">Speaking</a>
          <a href="glossary.html">Glossary</a>
          <a href="company.html">Company</a>
          <a href="/llms.txt" target="_blank" rel="noopener">llms.txt</a>
          <a href="privacy.html">Privacy</a>
          <a href="privacy.html" data-consent-settings style="color:#93c5fd;">Cookie settings</a>
          <a href="#hero" style="color:var(--teal);">Back to top ↑</a>
        </div>
      </div>
    </div>
  </footer>

  <script>
    // Navigation drawer
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const mobileMenu = document.getElementById('mobileMenu');

    hamburgerBtn.addEventListener('click', () => {
      const isExpanded = hamburgerBtn.getAttribute('aria-expanded') === 'true';
      hamburgerBtn.setAttribute('aria-expanded', !isExpanded);
      mobileMenu.classList.toggle('open');
      mobileMenu.setAttribute('aria-hidden', isExpanded);
    });

    function closeMobileMenu() {
      hamburgerBtn.setAttribute('aria-expanded', 'false');
      mobileMenu.classList.remove('open');
      mobileMenu.setAttribute('aria-hidden', 'true');
    }
  </script>
</body>
</html>
HEADER

sed -i '' "s|__TITLE__|$TITLE|g" "$OUT"
sed -i '' "s|__DESC__|$DESC|g" "$OUT"
sed -i '' "s|__KEYWORDS__|$KEYWORDS|g" "$OUT"
sed -i '' "s|__PAGE__|$PAGE|g" "$OUT"
case "$PAGE" in
  icare.html) PAGE_NAME="iCare Case Study"; sed -i '' 's/__ICARE_CLASS__/ active/g' "$OUT" ;;
  taskedge.html) PAGE_NAME="TaskEdge"; sed -i '' 's/__TASKEDGE_CLASS__/ active/g' "$OUT" ;;
  automation.html) PAGE_NAME="Applied AI Solutions"; sed -i '' 's/__AUTOMATION_CLASS__/ active/g' "$OUT" ;;
  about.html) PAGE_NAME="About"; sed -i '' 's/__ABOUT_CLASS__/ active/g' "$OUT" ;;
  industries.html) PAGE_NAME="Industries"; sed -i '' 's/__INDUSTRIES_CLASS__/ active/g' "$OUT" ;;
esac
sed -i '' "s/__.*_CLASS__//g" "$OUT"
sed -i '' "s|__PAGE_NAME__|$PAGE_NAME|g" "$OUT"

