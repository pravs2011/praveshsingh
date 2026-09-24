# praveshsingh.com — Executive Founder & CTO Platform Package

## Building for production

Run:

    ./make_build.sh --zip

This assembles a validated production build in build/ and packages it as
praveshsingh-production.zip (3.8 MB, 77 files). The script wipes the old
build/, copies only deployable files, then validates: required files present,
no dev artifacts (templates, generator, planning docs), canonical href
hygiene, sitemap↔file consistency, and XML well-formedness. It exits non-zero
on any failure — do not deploy a failed build.

Deploy: upload the CONTENTS of the zip (or of build/) to the web root.
Delete any stale build/ directory on the server first. Never upload the
dev-repo root as-is: that is how build/ (with planning docs) leaked into
production and triggered the GSC "access forbidden (403)" coverage error.

Files deployed:

- .htaccess (Crucial: Apache canonical 301 redirects, /build/ 404-block, MIME types)
- index.html (Unified Executive Positioning, Proof Strip, Hub-and-Spoke Architecture)
- 404.html (Real 404 handler — served by ErrorDocument)
- about.html (Executive Bio, Engineering Philosophy, Career Timeline, Media Proof)
- icare.html (Clinical Registry & Biological Cold-Chain Logistics Deep-Dive)
- taskedge.html (Multi-Tenant Operations Execution SaaS Deep-Dive)
- automation.html (Deterministic Applied AI, Schema-Constrained Extraction & ETL)
- industries.html (Healthcare, Deskless Ops, FinTech, Public Sector DPI Footprint)
- speaking.html (Invited talks, workshops & live demonstrations)
- glossary.html (Plain-language Indian health-tech glossary)
- company.html (SoftEdge Technology Solutions company profile)
- expertise.html (Commercial Engagement Packaging, 4 Standardized Formats & Inquiry Generator)
- expertise.md (Markdown twin of expertise.html)
- 404.html (Real 404 handler — served by ErrorDocument)
- robots.txt (Full web and AI search crawler directives)
- sitemap.xml (Comprehensive sitemap covering all 14 canonical platform URLs)
- llms.txt (Concise machine-readable site index & executive context)
- llms-full.txt (Comprehensive machine-readable context, architectures & essay abstracts)
- yandex_489999cb20aa0fec.html (Search engine site verification)
- .well-known/
  - security.txt (RFC 9116 security contact)
  - llms.txt
  - llms-full.txt
  - index.html (fallback redirect)
- images/
  - index.html (fallback redirect)
  - pravesh-singh.png (High-resolution executive portrait)
  - pravesh-singh.webp (Web-optimized high-performance portrait)
  - showcase/ (Optimized proof & milestone photos)
- writing/
  - index.html (Thought leadership hub & filterable essay catalog)
  - feed.xml (Atom syndication feed)
  - feed.xml (Atom syndication feed)

Do NOT upload: build/ (local mirror), writing/_template.html (generator
template), make_page.sh, *.md planning docs. The .htaccess 404-blocks /build/;
uploading it would only add dead weight.
  - offline-tolerant-hospital-software.html
  - abdm-integration-developer-guide.html
  - multi-tenant-postgresql-isolation.html
  - high-value-medicine-inventory-logistics.html
  - structured-data-extraction-llm-limits.html
  - dpdp-act-2023-health-tech-checklist.html

The platform features:
- Executive dark-tech aesthetic with responsive, mobile-first layouts and zero external build dependencies
- Multi-entity Schema.org JSON-LD (Person, Organization, ProfilePage, ItemList, Article, BreadcrumbList)
- 4 Standardized commercial engagement packages with an interactive inquiry generator
- 6 Deep architectural thought-leadership essays with production schemas, SQL queries, and Python examples
- Full Apache .htaccess for 301 canonical redirects (HTTPS, non-www, /index.html -> /)
- Complete directory traversal and 403 Forbidden protection

After deployment:
1. Verify https://praveshsingh.com/ loads cleanly on desktop and mobile.
2. Verify all subpages (/about.html, /icare.html, /taskedge.html, /automation.html, /industries.html, /expertise.html).
3. Verify https://praveshsingh.com/writing/ and all 6 technical essays.
4. Verify https://praveshsingh.com/robots.txt and https://praveshsingh.com/sitemap.xml.
5. Verify https://praveshsingh.com/llms.txt and https://praveshsingh.com/llms-full.txt.
