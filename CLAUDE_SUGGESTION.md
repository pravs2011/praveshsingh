# Task: Improve the content, structure and SEO of praveshsingh.com

You are working on my personal website (https://praveshsingh.com/), a static site with an index page and an expertise.html page, plus llms.txt, sitemap.xml and robots.txt. I am Pravesh Singh, MD & CTO of SoftEdge Technology Solutions. I build iCare (hemophilia/thalassemia registry and drug inventory platform used in Punjab and Madhya Pradesh), TaskEdge (multi-tenant operations SaaS), and applied-AI data automation tools.

## Step 0: Inputs from me (fill these in before running)

PRIMARY_AUDIENCE: [choose one: "health programmes, hospitals and public-sector bodies" OR "startup founders and product teams" OR "both, with healthcare as the lead"]
REAL_NUMBERS: [e.g. number of treatment centres live, patients registered, stock transfers processed, states covered. Write "unknown" for anything I haven't confirmed.]
NON_HEALTHCARE_PROJECTS: [short anonymised descriptions of 1-3 non-healthcare projects, or "none"]
TESTIMONIALS: [any quotes with name, role, and permission to publish, or "none yet"]
ENGAGEMENT_MODEL: [does the client contract with me personally or with SoftEdge? Any typical engagement types and price bands I am happy to publish]
BOOKING_LINK: [Calendly/Cal.com URL or "none"]
GITHUB_URL / OTHER_PROFILES: [URLs or "none"]

## Ground rules (important)

1. Inspect the existing codebase first. Match its structure, HTML/CSS conventions, dark theme, typography and component patterns. Do not introduce a framework or build step unless one already exists. Do not redesign the visual identity.
2. Never invent facts. Do not fabricate statistics, testimonials, client names, outcomes, certifications, or project details. Wherever real data is missing, insert a clearly visible placeholder in the form `[TODO: ...]` and list every placeholder in a final summary.
3. Be precise with regulated or sensitive claims. Do not write "ABDM certified" or "accepted by state health departments" unless I have confirmed it. Use wording such as "designed in line with ABDM guidelines" instead. Do not imply endorsement by any government body beyond what the existing page already states.
4. Never include patient data or identifiable patient information in any screenshot, copy or alt text. Use placeholders for screenshots that need anonymising.
5. Write for human visitors first. Plain, direct, grounded tone, consistent with the existing copy. No buzzwords, no filler.
6. Work in phases. After each phase, summarise what changed and wait for my go-ahead only if something is ambiguous; otherwise continue.

## Phase 1: Fix credibility and dead ends (highest priority)

- The links "Full architecture →", "Product detail →" and "How this is scoped →" currently jump to anchors on the same page. Repoint them to the new dedicated pages created below, or remove them if no destination exists.
- Replace the hero stats row. Items like "iCare: Patient registry & drug tracking" are descriptions, not numbers. Use REAL_NUMBERS where provided; otherwise use `[TODO: real number]` placeholders. Keep "15+ years" and "Punjab & MP".
- Tighten precision of claims on both pages as per ground rule 3.
- Rewrite the home-page H1 and subhead around an outcome for PRIMARY_AUDIENCE rather than a generic "software engineering for X". Keep it to one clear sentence plus a supporting line. Offer me two alternative hero variants in your summary.
- Rename the vague nav label "Field Work & Talks" to something clearer (e.g. "Talks & Workshops"). Update all references on both pages.
- Remove the phrase "search engines and automated research tools" from FAQ subtitles. Write FAQ intros for humans.

## Phase 2: New dedicated pages (static HTML, same template style)

Create these pages, each with its own title, meta description, canonical URL, Open Graph tags, breadcrumb, and a clear CTA:

1. /icare.html: a proper case study. Structure: The problem (stock-outs, patient portability, fragmented records) / Constraints (spotty networks, busy clinic staff, low-end hardware, public-sector data rules) / What we built / Architecture (include a simple architecture diagram as inline SVG or Mermaid-style static SVG: clients, API, PostgreSQL, tenant isolation, audit log, inter-centre transfer flow) / Key technical decisions and trade-offs / Outcomes (use REAL_NUMBERS or TODOs) / What I would do differently / CTA. Include a `[TODO: testimonial]` block, filled from TESTIMONIALS if provided.
2. /taskedge.html: what it is, who it's for, screenshots (`[TODO: screenshot]` placeholders), feature list, tenant-isolation and audit-log notes, current status (`[TODO: live / beta / private]`), and a CTA ("Request a demo").
3. /automation.html: the applied-AI work. Give 2-3 concrete, scoped examples (structured extraction from scanned clinical records, RAG over technical manuals, government report format conversion). For each: input, output, how correctness is verified, and known limitations. Be honest about limits.
4. /about.html: a short first-person story: why healthcare, what problem I care about, how I approach building software, and how SoftEdge relates to my personal practice (use ENGAGEMENT_MODEL). Mark anything you cannot know as `[TODO]`; do not make up biography.
5. If NON_HEALTHCARE_PROJECTS is not "none", add a "Selected work" section or /work.html showing those projects as short anonymised case snippets (problem, approach, result). If "none", add a `[TODO]` note in the summary that the site will read as healthcare-only until this is added.

Link these pages from the main nav, from the relevant sections on the home page, and from the Expertise page.

## Phase 3: Offer clarity and contact

- On expertise.html, add an "Engagement types" section: e.g. fixed-scope architecture review, prototype sprint, ongoing advisory retainer. Include price bands or "typically starts at" lines only if ENGAGEMENT_MODEL gives them; otherwise add `[TODO]` placeholders.
- Clarify on the home page and expertise page whether the client contracts with me personally or with SoftEdge, per ENGAGEMENT_MODEL.
- Improve the contact section. Keep the email, and add BOOKING_LINK if provided. Add a lightweight inquiry form only if I already have a form handler or backend; otherwise use a mailto link with a prefilled subject and a short "What to include" checklist (problem, timeline, budget band, current stack).
- Add a GitHub link and other profiles from GITHUB_URL / OTHER_PROFILES to the footer and contact section if provided.

## Phase 4: Writing section (content engine)

- Create /writing/index.html as an article index, plus an article template (/writing/_template.html or equivalent) consistent with the site's design. Include title, date, reading time, author byline, table of contents for long posts, related posts, and a CTA.
- Draft the first article outlines as `.md` or HTML stubs with a detailed outline and key points to cover (do not fabricate specifics; use `[TODO: my real example]` where I need to supply the experience). Topics:
  1. Building offline-tolerant software for hospitals with unreliable networks
  2. What ABDM integration involves in practice, from a developer's view
  3. Multi-tenant data isolation in PostgreSQL: approaches and trade-offs
  4. Designing inventory transfer for perishable, high-value medicines
  5. Extracting structured data from scanned clinical records with LLMs, and where it fails
  6. DPDP Act 2023: a practical checklist for health-data products (flag clearly that this is not legal advice)
- Add a "Writing" link to the nav and a "Latest writing" strip on the home page (hidden or placeholder until at least one article is published).

## Phase 5: Technical SEO and discoverability

- Add JSON-LD structured data: `Person` (name, jobTitle, worksFor SoftEdge, url, image, sameAs = LinkedIn, GitHub, SoftEdge site), `Organization` for SoftEdge, `FAQPage` for existing FAQs, `Article` for writing posts, and `BreadcrumbList` on inner pages. Validate the JSON.
- Ensure every page has a unique title, meta description, canonical, and OG/Twitter tags. Fix any duplicates. Add descriptive alt text to all images.
- Update sitemap.xml with all new pages, with correct lastmod dates. Keep robots.txt valid.
- Update llms.txt to describe the new pages and the site's purpose accurately and concisely.
- Add internal links between related pages (home, iCare, expertise, writing, contact).
- Check for performance basics: lazy-load below-the-fold images, provide width/height attributes, compress or flag oversized images (report file sizes; do not silently degrade quality).
- Check accessibility basics: heading hierarchy (one H1 per page), contrast on the dark theme, keyboard navigation for the FAQ accordions and image lightbox, focus states.

## Deliverables

1. All code changes, in logical commits or clearly separated change sets per phase.
2. A final summary containing: (a) what was changed per file, (b) a complete list of every `[TODO]` placeholder with file and line, so I know exactly what facts I still need to supply, (c) any claims you softened for precision and why, (d) two alternative hero variants, (e) anything you noticed but chose not to change.
3. Do not deploy or push to production. Leave everything ready for my review.