---
name: seo-audit
description: >
  Full technical SEO audit skill — 20 categories, weighted scoring, CWV phase
  diagnosis, schema audit (including retired types), JS rendering check,
  E-E-A-T assessment, crawlability, and structured output. Use when doing a
  comprehensive technical or on-page audit for any client site. Trigger phrases:
  "audit teknikal", "full audit", "technical SEO", "CWV", "schema audit",
  "crawl issues", "core web vitals", "semua yang rusak secara teknis".
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [SEO, Technical, Audit, CWV, Schema, E-E-A-T, Crawl, Performance]
    related_skills: [seo-agency, seo-geo, seo-platforms]
---

# SingRank Technical SEO Audit v1.0

Complete technical audit in 5 phases. Always pull SingRank MCP data first (Step 0).
For Wix or Shopify-specific fix implementation, hand off to `seo-platforms` skill.

---

## STEP 0 — Data Pull (Required Before Audit)

**Fast path — zero tool calls:** `brain{doc:'audit'}` returns the per-client FULL technical
audit (site health v2 + index coverage + links + CWV), already fused with a ranked DO-NEXT
list, regenerated nightly at 03:45 WIB. Read this first. Use the live tools below only to go
deeper than the precomputed doc, or if it's stale for this client.

**SingRank MCP (primary, live):**
```
list_clients            → exact domain key
site_health             → v2: on-page (missingTitles, duplicateTitles, thinContent,
                           orphanPages, deadEndPages) + head/technical (noindexPages CRITICAL,
                           missingMetaDesc, canonicalMismatch, missingOgImage, h1Issues,
                           imagesMissingAlt, schemaIssues) + healthScore 0-100. Head-data fills
                           in gradually as the crawler re-fetches (full refresh Sunday) — check
                           `seoCoverage.pct`; don't claim "no issues" while coverage is still low.
index_coverage           → REAL Google index status (GSC URL Inspection, precomputed weekly).
                           notIndexed pages = highest-priority fix, before writing anything new.
                           ⚠️ Returns empty until the service account has FULL permission on the
                           GSC property — if empty, say so, don't report "no issues."
cwv_report               → Core Web Vitals (field CrUX p75 + lab Lighthouse, precomputed weekly,
                           with trend). ⚠️ May be empty/rate-limited without a PSI_KEY set
                           server-side — if empty, fall back to a live PageSpeed Insights check.
broken_links             → v2, 3 buckets: broken (internal 4xx), redirects (3xx chains — fix
                           hops≥2 first), externalBroken (outbound 404/410/DNS). Weekly Monday refresh.
gsc_summary              → baseline traffic + position
anomalies                → algorithm-flagged issues
top_movers               → big winners/losers (date arg required; often empty — skip if no data)
get_internal_links       → link graph for internal link audit
published_articles       → content inventory + freshness
fetch_log                → data freshness check (skip if <24h since last pull)
smart_actions            → AI-suggested priority actions (use as cross-check)
```

⚠️ **pullupstand.com canonicalMismatch ±25 is INTENTIONAL** — it's the June-2026
cannibalization fix via `seo.canonical` metafield, not a bug. Don't flag it as an issue.

**Ahrefs MCP (backlinks only — SingRank has no first-party backlink data):**
```
mcp__claude_ai_Ahrefs__site-explorer-domain-rating     → DR score
mcp__claude_ai_Ahrefs__site-explorer-anchors           → anchor text distribution (HHI formula)
mcp__claude_ai_Ahrefs__site-explorer-refdomains-history→ referring domain trend (link velocity)
```

Semrush and Ahrefs' organic-keyword/technical-audit tools are optional fallbacks for a domain
outside SingRank's tracked footprint — for tracked clients, `site_health`/`index_coverage`/
`cwv_report` are the source of truth (first-party, no external API dependency, no quota cost).

---

## 20-CATEGORY AUDIT (Weighted Scoring)

Health Score = Σ(category_score × category_weight), target ≥ 70/100 (PASS).
**Weights MUST sum to 100%.** Verified: 15+12+10+8+6+6+6+6+6+5+5+4+3+2+2+2+1+1+0+0 = 100%.

| # | Category | Weight | Key Checks |
|---|---|---|---|
| 1 | Core On-Page | 15% | title, meta, canonical, H1, viewport, heading order |
| 2 | Performance / CWV | 12% | LCP ≤2.5s, INP ≤200ms, CLS ≤0.1, TTFB |
| 3 | Content Depth + E-E-A-T | 10% | word count, freshness, FAQ, author, trust signals |
| 4 | Structured Data | 8% | schema presence, validity, retired types, @graph |
| 5 | Links (Internal + External) | 6% | internal count ≥5, broken links, anchor quality |
| 6 | Technical Foundations | 6% | robots.txt, sitemap, redirect chains, 404s |
| 7 | AI / GEO Readiness | 6% | AI crawlers allowed, llms.txt, SSR citability |
| 8 | Crawlability | 6% | Googlebot access, crawl budget, pagination, indexation |
| 9 | Images | 6% | alt text, WebP/AVIF, lazy load, CLS contribution |
| 10 | Security | 5% | HTTPS, HSTS, security headers, SSL expiry |
| 11 | JS Rendering | 5% | raw HTML vs rendered DOM, AI crawler blind spots |
| 12 | Backlink Health | 4% | referring domain quality, anchor distribution, toxic links |
| 13 | Accessibility | 3% | ARIA labels, color contrast ≥4.5:1, keyboard navigation |
| 14 | Social Meta | 2% | OG title/desc/image, Twitter card, correct dimensions |
| 15 | URL Structure | 2% | length ≤75 chars, keywords in slug, no parameters |
| 16 | Mobile | 2% | viewport meta, touch targets ≥48px, no horizontal scroll |
| 17 | Internationalization | 1% | hreflang (en-sg + id-id for dual-market clients) |
| 18 | Page Experience | 1% | no intrusive interstitials, no deceptive layouts |
| 19 | Local SEO | 0%* | GBP completeness, NAP consistency, local schema |
| 20 | Legal / Compliance | 0%* | PDPA (SG), UU PDP (ID), privacy policy, AI-content disclosure |

*Categories 19–20 scored Pass/Fail separately — not in main 100-point score but must be flagged.

### Category Scoring Rubric (apply consistently — do not guess)

**Cat 1 — Core On-Page (15%)**
```
100: title 50-60c + keyword first 3w + unique + meta 150-160c + single H1 + canonical self-ref + correct heading order
 80: title/meta length OK but keyword placement weak OR minor heading order skip
 50: title >65c OR meta <120c OR missing canonical OR H1 not present
  0: no title tag OR duplicate title sitewide OR noindex on an indexable page
```

**Cat 2 — CWV Performance (12%)**
```
100: LCP ≤2.5s + INP ≤200ms + CLS ≤0.10 (all in field data)
 80: 2 of 3 pass field data; failing metric is in "Needs Work" range (not Poor)
 50: any metric in "Poor" range (LCP >4s OR INP >500ms OR CLS >0.25)
  0: 2+ metrics in Poor range OR site not measurable (JS-rendered, no CrUX data)
Source: PageSpeed Insights field data tab (NOT lab data). Lab data only used for diagnosis.
```

**Cat 3 — Content Depth + E-E-A-T (10%)**
```
100: ≥2500w + <3mo fresh + named author + credentials + FAQ ≥5 Q&A + ≥3 named stats + all 6 keyword floors
 80: 1500-2500w + <6mo + author present + most signals present
 50: <1500w OR >12mo stale OR no author byline OR thin FAQ (1-2 Q)
  0: <500w OR no visible text (JS-blocked) OR duplicate of another page
```

**Cat 4 — Structured Data (8%)**
```
100: @graph present + Organization + WebSite + Article/Product/LocalBusiness + no retired types + 0 GRT errors
 80: schema present, valid, but no @graph linking entities
 50: schema present but has deprecated type (HowTo for rich results, old FAQPage) OR 1 GRT error
  0: no schema at all OR retired type still in use causing GRT failure
```

**Cat 5 — Links Internal + External (6%)**
```
100: ≥5 contextual internal links per page + 0 broken links + keyword-rich anchors + ≥1 outbound citation
 80: 3-4 internal links + 0-1 broken links
 50: 1-2 internal links OR 2+ broken links
  0: 0 internal links (orphan) OR broken canonical/redirect chain leaking equity
```

**Cat 6 — Technical Foundations (6%)**
```
100: robots.txt OK + XML sitemap submitted to GSC + 0 redirect chains + 0 404 pages in GSC
 80: sitemap present but not submitted OR 1-2 redirect chains (A→B only, no daisy chains)
 50: sitemap not updated >6mo OR 3+ redirect chains OR URLs not in sitemap
  0: crawl-blocking robots.txt OR no sitemap OR site returning 5xx on key pages
```

**Cat 7 — AI / GEO Readiness (6%)**
```
100: all 14 AI bots allowed + /llms.txt present + SSR all critical content + ≥7/9 GEO checklist
 80: major AI bots allowed (GPTBot, ClaudeBot, PerplexityBot, Google-Extended) + SSR
 50: some AI bots blocked OR /llms.txt missing OR JS-injected H1/body
  0: GPTBot or ClaudeBot in Disallow OR entire site JS-rendered (AI sees blank)
```

**Cat 8 — Crawlability (6%)**
```
100: all key pages indexed in GSC + no excluded pages that should be indexed + correct noindex on utility pages
 80: 1-5% of important pages excluded unexpectedly
 50: coverage errors in GSC (Discovered - not indexed >30 days OR Crawl anomaly)
  0: GSC manual action OR site:domain.com shows near-zero results
```

**Cat 12 — Backlink Health (4%)**
```
100: DR ≥30 + HHI <2,000 (healthy anchor profile) + growing RD trend + 0 toxic links flagged
 80: DR 15-29 + anchor distribution acceptable (HHI <3,500) + no obvious spam
 50: DR <15 OR exact-match (s₂) >0.20 OR HHI >3,500 OR RD count declining >10% MoM
  0: manual action for unnatural links OR DR 0-5 with 80%+ exact-match anchors OR link velocity z-score >+3.0

HHI and link velocity z-score formulas: seo-agency MASTER SCORING SYSTEM Formula 6 + Formula 8
Source: Ahrefs site-explorer-anchors, site-explorer-domain-rating, site-explorer-refdomains-history
```

**Score each category → multiply by weight → sum = Health Score /100.**
Example: Cat1=80×0.15=12, Cat2=50×0.12=6, Cat3=100×0.10=10... → sum all 18 scored categories.

---

## PHASE 1 — CORE ON-PAGE (12%)

For each page (start with top 20 by GSC impressions):

**Title Tag:**
- Length: 50–60 characters (under 50 = wasted space; over 60 = truncation)
- Primary keyword: in the first 3–5 words
- Unique: no duplicate titles across the site (check published_articles list)
- Click-worthy: not a copy of H1; reads as a human-written SERP snippet

**Meta Description:**
- Length: 150–160 characters
- Primary keyword: within first 60 characters
- CTA or value signal present
- Unique per page (duplicate metas = wasted opportunity)

**H1:**
- Exactly ONE per page
- Primary keyword within first 5 words
- ≤60 characters
- Different from the title tag (complementary, not identical)

**Heading order:**
- Must follow H1 → H2 → H3 hierarchy (no skipping)
- No H2 or H3 used for decoration/styling (semantic use only)

**Canonical:**
- Self-referencing canonical on all non-paginated pages
- Paginated pages: canonical to page 1 OR rel=next/prev if series
- No canonical pointing to a 404 or redirect

**Viewport:**
- `<meta name="viewport" content="width=device-width, initial-scale=1">` present

---

## PHASE 2 — CORE WEB VITALS (12%)

### 2026 Thresholds (Updated — INP replaced FID Sept 2024)
```
Metric    Good         Needs Work    Poor
LCP       ≤ 2.5s       2.5–4.0s      > 4.0s
INP       ≤ 200ms      200–500ms     > 500ms
CLS       ≤ 0.10       0.10–0.25     > 0.25
```

**CRITICAL:** Use field data (CrUX / PageSpeed Insights field tab) as truth.
52% of mobile sites fail CWV in field data while passing Lighthouse lab tests.
Lab data identifies causes; field data identifies the verdict.

**Source order:** `cwv_report {domain}` first (precomputed weekly, has trend/history, zero
live-API cost). Only fall back to a live PageSpeed Insights check if it's empty for this client.

### LCP Diagnosis (phase breakdown)
```
LCP total = TTFB + Load Delay + Load Time + Render Delay
Fix the phase consuming the LARGEST SHARE of total LCP time.

TTFB >600ms:  → server response time, CDN, hosting tier
Load Delay:   → render-blocking resources, preload hints missing
Load Time:    → image size (compress + WebP/AVIF), font loading
Render Delay: → client-side rendering delay, JavaScript blocking
```

### INP Diagnosis (phase breakdown)
```
INP total = Input Delay + Processing Time + Presentation Delay
Fix the phase consuming the largest share.

Input Delay >50ms:      → main thread blocked by JS; yield to main thread
Processing Time >150ms: → event handler complexity; break up long tasks
Presentation Delay:     → forced layout/reflow; batch DOM writes
```

### CLS Fixes
- Reserve explicit width + height on ALL images and embeds
- No content injected above the fold after page load (ads, banners, cookie bars)
- Avoid FOUT (Flash of Unstyled Text) — use font-display: optional or swap + size-adjust

### CWV Quick Fixes by Platform
```
Wix:    Enable Wix Performance Booster (Site → Settings → Performance)
        Compress images via Wix Image Manager; use webp format
        Reduce Wix apps that inject JS above the fold

Shopify:Lazy load all images below the fold
        Defer non-critical JS with defer/async
        Use Shopify CDN for all media
        Remove unused apps (each adds JS weight)
```

---

## PHASE 3 — STRUCTURED DATA / SCHEMA (8%)

### Valid Schema Types (Active as of 2026 — 31 types support rich results)
```
Article, BlogPosting, NewsArticle, Book, BreadcrumbList, Carousel,
ClaimReview, Course, CourseInstance, Dataset, DiscussionForumPosting,
Education Occupational Program, EmployerAggregateRating, Event,
FactCheck, FAQ (restricted — see below), HowTo (restricted — see below),
Image Object, JobPosting, LearningResource, LocalBusiness, Movie,
Organization, Person, Product, ProductGroup, Q&A, Recipe, Review,
SiteLinks SearchBox, Software Application, Video, WebPage, WebSite
```

### RETIRED SCHEMA TYPES — Check for and Remove
```
HowTo          → Retired for rich results Sept 2023 (still valid as schema, but no rich result)
SpecialAnnouncement → Retired July 2025 (COVID-era schema)
MedicalBusiness → Merged into LocalBusiness
MedicalCondition → No longer produces rich results
FAQPage        → NOW RESTRICTED to government and healthcare authority sites (Aug 2023)
                  For all other sites: FAQPage schema ignored for rich results
                  Still helps GEO/AI extraction — keep it for that purpose only
```

### @graph Architecture (Best Practice — link types together)
```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", "@id": "https://domain.com/#org", "name": "…", "url": "…", "sameAs": ["…"] },
    { "@type": "WebSite", "@id": "https://domain.com/#website", "publisher": { "@id": "https://domain.com/#org" } },
    { "@type": "WebPage", "@id": "https://domain.com/page/#webpage",
      "isPartOf": { "@id": "https://domain.com/#website" },
      "primaryImageOfPage": { "@id": "https://domain.com/page/#image" }
    },
    { "@type": "Article", "isPartOf": { "@id": "https://domain.com/page/#webpage" },
      "author": { "@id": "https://domain.com/#org" }
    }
  ]
}
```
Linked @graph = entities reinforce each other for E-E-A-T and Knowledge Panel eligibility.

### Minimum Schema Stack per Page Type
```
All pages:    Organization + WebSite (sitewide, once)
Blog article: Article + BreadcrumbList (+ FAQPage for GEO purposes only)
Local page:   LocalBusiness (with address, phone, hours, geo)
Product page: Product + BreadcrumbList (+ Review if applicable)
Event page:   Event
```

### Schema Validation
→ Google Rich Results Test: zero errors before deploy
→ Schema.org validator: for types not covered by GRT
→ Flag any deprecated type found on the site as Critical issue

---

## PHASE 4 — E-E-A-T ASSESSMENT (6%)

**Experience signals (check presence):**
- First-hand evidence: case studies, "I tested this" language, original photos
- Specific results with numbers (not vague "years of experience")
- Client-specific credentials only (HDB Licence, MUIS cert, BCA) — never inflated

**Expertise signals:**
- Author byline + credentials on every article (name, title, organisation)
- Author bio links to external profiles (LinkedIn, professional directory)
- Topical depth: all key subtopics of target keyword addressed
- Industry-accurate terminology

**Authoritativeness signals:**
- External backlinks from authority domains in the niche
- Brand mentions on authoritative external sites
- Social proof with specific outcomes (not generic testimonials)
- Industry certifications/associations named and verifiable

**Trustworthiness signals (2025 QRG heavily weights "T"):**
- HTTPS (required — not optional)
- Contact page with real address and phone
- Privacy policy (PDPA-compliant for SG, UU PDP for ID)
- Transparent content update policy; visible dateModified on articles
- No deceptive page layouts or intrusive interstitials
- Clear disclosure when content is AI-assisted

Score E-E-A-T: 0.0–1.0 per signal cluster, average for overall E-E-A-T score.

---

## PHASE 5 — JS RENDERING CHECK (5%)

**Why this matters:** AI crawlers (GPTBot, ClaudeBot, PerplexityBot) cannot execute
JavaScript. If your critical content (title, H1, meta, canonical, body text, schema)
is injected by JS, these crawlers see a blank shell. So does Googlebot on first crawl.

**How to check:**
1. Raw source: `WebFetch {url}` — this is what a non-JS crawler (GPTBot, ClaudeBot, PerplexityBot, first Googlebot pass) actually sees.
2. Rendered DOM: open the page with the `claude-in-chrome` browser tools and read the live DOM (or `read_page`) — what's visible after JS executes.
3. Compare: if raw ≠ rendered, JS-dependent content won't reach AI crawlers.

**Flags:**
- Title/H1 loaded by JS → CRITICAL (AI crawlers blind to it)
- Body text loaded by JS → CRITICAL
- Schema loaded by JS → HIGH (lost rich results + AI context)
- Navigation/internal links loaded by JS → MEDIUM
- Images loaded by JS → LOW (lazy loading is fine; full-content images in JS = issue)

**Fix:**
- Server-side render (SSR) critical content
- Pre-render for known bots (dynamic rendering as interim solution)
- On Wix: content is typically SSR by default; check for heavy custom HTML widgets
- On Shopify: Liquid templates SSR by default; watch for Section JSON lazy loads

---

## GEO/AI READINESS (5% — Score within audit, full depth in seo-geo skill)

Quick AI-readiness check (full audit → use `seo-geo` skill):

```
✓ / ✗  robots.txt: GPTBot, ClaudeBot, PerplexityBot, Google-Extended all Allowed
✓ / ✗  /llms.txt present at root
✓ / ✗  Key content is server-side rendered (not JS-injected)
✓ / ✗  Self-contained answer blocks of ~134-167 words per H3
✓ / ✗  Primary answer appears in first 150 words of page
✓ / ✗  FAQPage schema present (GEO extraction, not rich results)
✓ / ✗  dateModified updated within 6 months
✓ / ✗  Named expert quotes with attribution present
✓ / ✗  Statistics with named source + year present (not vague "studies show")
```

Pass ≥7/9 for GEO Readiness. Fail any of first 3 → flag as Critical.

---

## AUDIT OUTPUT FORMAT

Produce two deliverables:

### FULL-AUDIT-REPORT.md
```
# [Client] Technical SEO Audit — [Date]

## Health Score: [X]/100 — [PASS/FAIL]
[Category scores table]

## Critical Issues ([count])
[Each finding in standard format below]

## High Priority ([count])
[Each finding]

## Medium Priority ([count])
[Each finding]

## Low Priority / Info ([count])
[Each finding]
```

**Standard Finding Format:**
```
### [FINDING TITLE] — [SEVERITY] — Priority: [score]
FINDING:    [specific issue with URL or selector]
EVIDENCE:   [data point, screenshot path, or MCP tool result]
IMPACT:     [ranking / CTR / AI visibility / traffic effect]
FIX:        [exact implementation steps + tool/platform]
CONFIDENCE: [Confirmed / Likely / Hypothesis]
```

### ACTION-PLAN.md
```
# Action Plan — [Client] — [Date]

## Fix NOW (Critical — complete within 24h)
1. [Priority score] [Fix description] [Time estimate]

## This Week (High)
1-5. [List]

## This Month (Medium)
1-5. [List]

## Future (Low / Nice-to-have)
1-5. [List]
```

For Wix or Shopify implementation of fixes → hand off to `seo-platforms` skill.
