---
name: seo-platforms
description: >
  Platform-specific SEO implementation skill for Wix and Shopify. Use when
  executing technical fixes, meta updates, schema injection, content edits, or
  internal link changes on Wix or Shopify client sites. Contains exact MCP tool
  calls, API patterns, and platform gotchas. Trigger phrases: "fix di Wix",
  "update Shopify", "inject schema Wix", "meta title Shopify", "technical fix Wix",
  "CWV Shopify", "internal link Wix", "orphan Shopify", "schema Shopify theme".
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Wix, Shopify, Technical, Implementation, Schema, Meta, CWV, Platform]
    related_skills: [seo-agency, seo-audit, seo-geo, singrank-article-writer, shopify-theme-liquid]
---

# SingRank Platform SEO — Wix + Shopify v1.0

Execution-layer skill. Assumes audit findings already identified (via `seo-audit` or
`seo-agency` playbooks). This skill implements the fixes on the actual CMS platforms.

**Scope note:** this skill covers content and metafield-level fixes (meta
tags, schema via metafields/theme snippets, body content, internal links).
For anything that edits actual theme CODE — Liquid files, section schema,
JSON templates, theme file pushes/publishing — use the deeper
`shopify-theme-liquid` skill and the `shopify-theme-engineer` agent instead.

**Golden rules (apply to all platforms):**
- NEVER delete articles, pages, products, or collections
- Fix via: rewrite → redirect → canonical → strengthen → interlink
- Body payloads > 30KB → use the PUSH PLAYBOOK below (never one giant call)
- Always verify the fix landed by reading back the saved content

---

## ARTICLE PUSH & EDIT — KNOWN MCP LIMITATIONS + THE HANDLING PLAYBOOK

Every limitation below has bitten us at least once. The prep tool for both flows:
`python C:\Users\natur\singrank-plugin\singrank\tools\publish_prep.py`

### SHOPIFY limitations → handling

| # | Limitation | Handling |
|---|---|---|
| S1 | **Body >~30KB** rejects/truncates through Admin API, and MCP tool calls have their own payload ceiling | `publish_prep.py shopify article.html --max-kb 25` → ordered block-boundary chunks + manifest. **RCS:** `create_article` (draft) with chunk-01 → `append_to_article` for the rest (X_RCS MCP has a purpose-built append). **Other stores:** read-modify-write append via graphql grows the payload each call and is UNSAFE past ~30KB → use the THEME-SNIPPET route: body = intro chunk only; full content in `snippets/article-<handle>.liquid` via `themeFilesUpsert` (>20–30KB theme files: gist→URL push, see shopify-theme-liquid) |
| S2 | `<script>` stripped from article/page body | All JSON-LD at THEME level, keyed to handle (Article+Breadcrumb+Speakable only) |
| S3 | **X_RCS `list_articles` caps at newest-160** — pre-Dec-2025 RCS articles unreachable by listing | Get the ID without the list: (a) find the handle via SingRank System RAG (`search_articles` → URL → handle); (b) `graphql_query`: `{ blogs(first:5){nodes{ articles(first:1, query:"handle:<handle>"){nodes{id title}} }} }`; (c) paginate a blog's articles with cursors only as last resort |
| S4 | Ablink dual keys: read key can't mutate | Confirm the ADMIN key is active before any `graphql_mutation`; a "success-looking" response from the read key is a lie — verify with a read-back |
| S5 | Timeouts / partial writes on big mutations | One logical change per mutation; ALWAYS read back and compare word count vs source file before calling it done |
| S6 | Editor strips some tags in body (`<style>`, some attrs) | Keep body semantic HTML (h2/p/ul/table/details); presentation via theme CSS |

### WIX limitations → handling

| # | Limitation | Handling |
|---|---|---|
| W1 | **Draft Posts body = RICOS JSON, not HTML** — you cannot push HTML | `publish_prep.py ricos article.html --batch-nodes 40` → converts h1-h6/p/bold/italic/links/ul/ol/blockquote/**tables**/details into RICOS nodes, batched |
| W2 | **One-call payload too big** for a 2,500w article | Batched flow: CREATE draft with batch-01 → for each batch: GET draft, append nodes to `richContent.nodes`, UPDATE (fieldMask `draftPost.richContent`) → VERIFY node count == manifest → ONE `UPDATE_PUBLISH` at the end |
| W3 | `ExecuteWixAPI` silently no-ops on writes | ALL writes via `CallWixSiteAPI` — no exceptions |
| W4 | `UPDATE` on a published post only saves a draft | Published posts: action `UPDATE_PUBLISH` |
| W5 | Echoing `memberId` back breaks the update | Strip `memberId` from every GET response before re-sending |
| W6 | `<script>` stripped from body | Schema via `seoData.tags` script entry (head route persists) — Article+Breadcrumb+Speakable only |
| W7 | `relatedPostIds` max 3, must be published post IDs | Cap at 3; verify targets are published |
| W8 | Images must exist in the media manager | `UploadImageToWixSite` first, then reference the media ID in RICOS |
| W9 | RICOS node shapes (esp. TABLE) vary by Wix version | First article per site: push ONE small throwaway draft with a table+list, GET it back, confirm Wix accepted the shapes — then push the real thing |

### Universal rules for every push
1. **Draft first, always.** `published:false` (Shopify) / draft until UPDATE_PUBLISH (Wix).
2. **Verify after every write**: read back; word/node count must match the manifest.
3. **Chunk, don't cram**: many small calls beat one giant call that times out halfway.
4. Publish only with explicit approval → then `log_experiment {url, changes}`.
5. rajawangi.co.id = Squarespace: NO API path at all — manual editor or `claude-in-chrome`.

**Client → platform map (verified by live probe 2026-07-08 — Save doc id 79):**

| Platform | Clients |
|---|---|
| Shopify | pullupstand.com, renovationcontractorsingapore.com, ablink.sg, saffrons.com.sg, yescpap.com, matchdayaffairs.com, www.edureachsg.com, kgteknik.co.id |
| Wix | www.dehallsg.com, www.ifgshipping.com, www.livinmalaysia.com |
| **Squarespace** | www.rajawangi.co.id |
| Next.js (own code) | singrank.com, id.singrank.com, my.singrank.com — edit at D:\singrank-web, deploy via Cloudflare Pages (confirm before deploy) |

**Squarespace (rajawangi.co.id) — no MCP write access:** there is no Squarespace
MCP connected. Content/SEO edits go through the Squarespace editor manually, or
via the `claude-in-chrome` browser tools driving the editor UI with the user's
session. Sitewide code (GEO pixel, schema JSON-LD) → Settings → Advanced →
Code Injection (Business plan+). Taxonomy: 1 EXISTING category + 3–5 tags,
never a new category. Never present a Wix/Shopify API call as applicable to
rajawangi.

---

## WIX — PLATFORM REFERENCE

### MCP Tool Hierarchy for Wix

```
READ operations:  mcp__claude_ai_Wix__ExecuteWixAPI  (read-only)
WRITE operations: mcp__claude_ai_Wix__CallWixSiteAPI  (required for all writes)
```

**Never use ExecuteWixAPI for writes** — it will appear to succeed but changes won't save.

### Key Wix APIs

**Blog posts (content + SEO):**
```
API: Draft Posts v3
Service: wix-blog-backend.v3.draft-posts

Read published post:
  method: GET
  query: { "filter": { "id": "<postId>" }, "fieldsets": ["SEO", "CONTENT"] }

Update published post (non-destructive — preserves unpassed fields):
  method: POST
  action: UPDATE_PUBLISH
  body: { "draftPost": { "id": "<postId>", "title": "…", "seoData": {…} },
          "fieldMask": "draftPost.title,draftPost.seoData" }

CRITICAL: Use UPDATE_PUBLISH (not UPDATE) for published posts — UPDATE only saves a draft.
CRITICAL: Do NOT include "memberId" in the body — strip it from any GET response before re-sending.
```

**SEO metadata on blog posts:**
```json
{
  "seoData": {
    "tags": [
      { "type": "title", "children": "SEO Title — 50-60 chars" },
      { "type": "meta", "props": { "name": "description", "content": "Meta desc 150-160 chars" } },
      { "type": "script",
        "props": { "type": "application/ld+json" },
        "children": "{\"@context\":\"https://schema.org\",\"@graph\":[{\"@type\":\"Article\",…},{\"@type\":\"BreadcrumbList\",…}]}"
      }
    ],
    "slug": "url-slug-here"
  }
}
```
The `script` entry in `seoData.tags` is how schema is injected on Wix — it persists in
the `<head>` and survives content edits. Use this for ALL schema (Article,
BreadcrumbList, Speakable, LocalBusiness) on blog posts and pages.
**NEVER inject FAQPage/HowTo** (deprecated — QC P0); when editing a post that carries a
legacy FAQPage block, strip it in the same write and keep the Q&A as visible content.

**relatedPostIds:** maximum 3 IDs; must be valid published post IDs.

**Wix Pages (non-blog):**
```
Use: Pages v2 API via CallWixSiteAPI
For SEO fields: seo.title, seo.description, seo.hidden (noindex)
For schema on pages: inject via seoData.tags script entry (same pattern as blog posts)
```

**Wix CWV Optimization:**
```
1. Wix Performance Booster: Site Settings → Performance → enable all options
2. Images: use Wix Media Manager → all images auto-served as WebP by Wix CDN
3. Fonts: use Wix-native fonts (pre-loaded); avoid Google Fonts imports in custom CSS
4. Apps: every installed Wix App adds JS. Audit active apps; remove unused ones.
5. Custom HTML widgets: check for render-blocking JS; move to bottom of page
6. Avoid embedded iFrames above the fold (CLS contributor)
```

**Wix Schema Injection (correct approach):**
```
For any Wix page/post, schema goes in seoData.tags as a script entry.
Do NOT put <script> tags inside the rich-text body (Ricos) — they are stripped.
Do NOT use Wix's built-in schema fields for complex types — they are limited.
Use the seoData.tags script injection for full control over all schema types.

Validate: Google Rich Results Test → paste the page URL after saving.
```

**Wix Ricos (Rich Content format for body):**
When updating article body content via the API, use Ricos JSON format.
Key Ricos node types:
```
PARAGRAPH       → { type: "PARAGRAPH", nodes: [{ type: "TEXT", textData: { text: "…" } }] }
HEADING         → { type: "HEADING", headingData: { level: 2 }, nodes: [{ type: "TEXT", … }] }
BLOCKQUOTE      → { type: "BLOCKQUOTE", nodes: [{ type: "PARAGRAPH", … }] }
  (IFG/Wix theme styles blockquote as Key Takeaway box)
IMAGE           → { type: "IMAGE", imageData: { image: { src: { url: "…" } }, altText: "…" } }
BULLETED_LIST   → { type: "BULLETED_LIST", nodes: [{ type: "LIST_ITEM", … }] }
DIVIDER         → { type: "DIVIDER" }
```

**Wix internal links (add to article body):**
```json
{ "type": "TEXT",
  "textData": { "text": "anchor text" },
  "nodes": [],
  "style": {},
  "inlineStyleSheet": {},
  "textStyle": { "textAlignment": "AUTO" },
  "decoration": [{ "type": "LINK", "linkData": { "link": { "url": "https://domain.com/target" } } }]
}
```

**Wix Workflow — Safe Content Update Process:**
1. GET the post with full CONTENT + SEO fieldsets → save the full response
2. Modify ONLY the specific fields needed (use fieldMask to protect others)
3. POST with UPDATE_PUBLISH action + fieldMask
4. GET again to verify the change persisted
5. Check in browser (incognito) to confirm live

**Common Wix Mistakes to Avoid:**
- Don't use UPDATE action on published posts (creates a draft, doesn't publish)
- Don't send body without fieldMask (may overwrite fields you didn't intend to change)
- Don't put schema inside Ricos body (stripped on save)
- relatedPostIds > 3 entries → API rejects the whole request
- Slug changes → always check if the old URL needs a redirect (Wix Redirects section)

---

## WIX — COMMON FIX PLAYBOOKS

### Fix 1: Update SEO meta title + description
```python
# Via CallWixSiteAPI
body = {
    "draftPost": {
        "id": "<postId>",
        "seoData": {
            "tags": [
                {"type": "title", "children": "New Title Tag Here — 55 chars"},
                {"type": "meta", "props": {"name": "description", "content": "New meta description — 155 chars"}}
            ]
        }
    },
    "fieldMask": "draftPost.seoData"
}
```

### Fix 2: Inject Article + BreadcrumbList + Speakable schema (NEVER FAQPage — deprecated, QC P0)
```python
page_schema = json.dumps({
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "Article", "headline": "<title>",
         "author": {"@type": "Organization", "name": "<client byline>"},
         "datePublished": "<ISO>", "dateModified": "<ISO>"},
        {"@type": "BreadcrumbList", "itemListElement": []},
        {"@type": "WebPage", "speakable": {"@type": "SpeakableSpecification",
         "cssSelector": [".key-takeaway", "article > p:first-of-type"]}}
    ]
}, ensure_ascii=False)

body = {
    "draftPost": {
        "id": "<postId>",
        "seoData": {
            "tags": [
                # Keep existing title/meta tags, add schema:
                {"type": "script", "props": {"type": "application/ld+json"}, "children": page_schema}
            ]
        }
    },
    "fieldMask": "draftPost.seoData"
}
```
**Note:** If you only send the schema entry, the title/meta tags may be removed.
Always GET the current seoData.tags first, then append the schema entry to the existing list.

### Fix 3: Add internal links (de-orphan)
1. GET post content as Ricos JSON
2. Find the paragraph where the link fits contextually (by searching text content)
3. Add LINK decoration to the text node at that position
4. POST with fieldMask: "draftPost.content"

### Fix 4: Fix cannibalization — change meta title focus
Change H1 and title/meta to shift keyword focus away from cannibalizing keyword:
```python
body = {
    "draftPost": {
        "id": "<weakPostId>",
        "title": "New Title Focused on Different Keyword",
        "seoData": {
            "tags": [
                {"type": "title", "children": "Differentiated Title Tag"},
                {"type": "meta", "props": {"name": "description", "content": "Updated meta description"}}
            ]
        }
    },
    "fieldMask": "draftPost.title,draftPost.seoData"
}
```
Never delete or redirect (per agency rules) — change focus only.

---

## SHOPIFY — PLATFORM REFERENCE

### MCP Tool for Shopify
Primary tool: `mcp__claude_ai_Shopify__graphql_mutation` and `graphql_query`

The SingRank clients with Shopify:
- **RCS** (`renovationcontractorsingapore.com`) — full admin via Shopify MCP
- **Saffrons** (`saffrons.com.sg`) — blog (News) 281 articles, SEO meta in metafields
- **Pullupstand** (`pullupstand.com`) — products + blog, meta in metafields
- **Ablink** (`ablink.sg`) — draft theme ID 183046078779; use `mcp__claude_ai_Shopify__switch-shop` to confirm active store; read key separate from admin key

### Ablink-Specific Rules
```
Theme: ALWAYS edit draft theme ID 183046078779 — NEVER the live published theme
Schema: inject via theme Liquid snippets in draft theme (never body content)
API keys: read key for queries, admin key for mutations — verify which key is active
Theme file push: gist → themeFilesUpsert URL approach for large file updates
T8 pricelist API: at E:\Backend Pricelist — for product data; separate from Shopify SEO
```

### Schema on Shopify
**CRITICAL:** Shopify's article/page/product body editor strips `<script>` tags.
ALL schema must be injected at THEME level, not in body content.

```liquid
<!-- In theme/snippets/seo-schema.liquid or article.liquid template -->
{% if article %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{ article.title | json }}",
  "author": { "@type": "Organization", "name": "{{ shop.name | json }}" },
  "datePublished": "{{ article.published_at | date: '%Y-%m-%d' }}",
  "dateModified": "{{ article.updated_at | date: '%Y-%m-%d' }}"
}
</script>
{% endif %}
```

For per-article Speakable (keyed to article handle — NEVER FAQPage/HowTo, deprecated QC P0):
```liquid
{% if article.handle == 'target-article-handle' %}
<script type="application/ld+json">
{ "@context": "https://schema.org", "@type": "WebPage",
  "speakable": { "@type": "SpeakableSpecification",
  "cssSelector": [".key-takeaway", "article p:first-of-type"] } }
</script>
{% endif %}
```
**Legacy cleanup rule:** RCS/IFG and other client themes may still carry FAQPage blocks
from before the policy change (pre-Jul-2026). Whenever you touch a theme snippet or
seoData that contains one, strip the FAQPage/HowTo block in the same edit — the visible
Q&A content stays.

### SEO Meta on Shopify — metafields

Articles use metafields for custom SEO title/description:
```graphql
# Set SEO title + description via metafield
mutation SetArticleSEO($id: ID!, $title: String!, $description: String!) {
  articleUpdate(id: $id, article: {
    metafields: [
      { namespace: "global", key: "title_tag", value: $title, type: "single_line_text_field" },
      { namespace: "global", key: "description_tag", value: $description, type: "single_line_text_field" }
    ]
  }) {
    article { id title }
    userErrors { field message }
  }
}
```

Products use the same metafield pattern:
```graphql
mutation SetProductSEO($id: ID!, $title: String!, $description: String!) {
  productUpdate(input: {
    id: $id,
    metafields: [
      { namespace: "global", key: "title_tag", value: $title, type: "single_line_text_field" },
      { namespace: "global", key: "description_tag", value: $description, type: "single_line_text_field" }
    ]
  }) {
    product { id title }
    userErrors { field message }
  }
}
```

### Article Content Update
```graphql
mutation UpdateArticle($id: ID!, $body: String!) {
  articleUpdate(id: $id, article: { bodyHtml: $body }) {
    article { id title handle }
    userErrors { field message }
  }
}
```
**Body size warning:** if bodyHtml > ~30KB, the API may reject or truncate.
For large articles: send content in separate mutations for distinct sections if possible,
or use a theme snippet to inject additional content blocks.

### Image Alt Text Update
```graphql
mutation UpdateArticleImage($articleId: ID!, $imageId: ID!, $altText: String!) {
  articleImageUpdate(articleId: $articleId, imageId: $imageId, image: { altText: $altText }) {
    image { id altText }
    userErrors { field message }
  }
}
```

### Add Internal Links (in article body)
1. graphql_query to get current article bodyHtml
2. Edit HTML to add `<a href="/blogs/news/target-slug">anchor text</a>` in right context
3. graphql_mutation to save updated bodyHtml
4. Verify: graphql_query to read back the article

### PULLUPSTAND RULE (from agency standard)
For pullupstand.com: fix cannibalization via article meta title/description ONLY.
NEVER touch collections, products, or visible body content.
Use `global.title_tag` and `global.description_tag` metafields for all fixes.

### Shopify Blog SEO Workflow
1. `graphql_query` → list all articles in a blog + their handles + metafields
2. For each article needing a fix: `graphql_mutation` → update metafields for SEO title/desc
3. For schema: update theme snippets via Admin API or manually via theme editor
4. For image alts: `articleImageUpdate` mutation per image

### Shopify CWV Optimization
```
1. Theme: use a performance-optimized theme (Dawn is fastest by default)
   Heavy apps = CWV killers. Run: Shopify → Apps → check which apps load scripts
2. Images: all product/blog images → convert to WebP, compress before upload
   Shopify CDN serves WebP automatically when original is uploaded as JPG/PNG
3. JS deferral: defer non-critical app JS (most apps don't do this by default)
   Custom apps: add defer/async to <script> tags in theme
4. Fonts: use system fonts or load with font-display: swap in theme CSS
5. LCP: ensure the hero image (usually the main product image or header image)
   has <link rel="preload"> in theme <head>
6. CLS: all images in theme must have explicit width + height attributes
   Fix via: theme code → find img tags → add width="{{ image.width }}" height="{{ image.height }}"
```

### Shopify robots.txt for AI Crawlers
Shopify auto-generates robots.txt. To allow AI crawlers:
1. Shopify Admin → Online Store → Preferences → Robots.txt → Edit
   OR create `robots.txt.liquid` in theme
2. Add allow rules for AI crawlers (same list as Wix section above)

---

## CROSS-PLATFORM — COMMON SEO FIXES

### Fix: Canonical Issues
- **Wix:** canonical is auto-generated from the slug; change slug via API if needed
- **Shopify:** canonical is auto-generated; override via `canonical_url` liquid variable in theme

### Fix: Redirect Chain (A→B→C)
Both platforms: create a direct redirect A→C, delete A→B.
- Wix: Site → Redirects section in dashboard
- Shopify: Online Store → Navigation → URL Redirects

### Fix: Noindex Pages (deliberate)
- Wix: seoData.tags → add `{"type": "meta", "props": {"name": "robots", "content": "noindex, nofollow"}}`
- Shopify: theme snippet or per-page noindex via Online Store → Preferences

### Fix: hreflang (SG + ID clients)
For clients with both English (SG) and Bahasa Indonesia (ID) content:
```html
<link rel="alternate" hreflang="en-sg" href="https://domain.com/sg/page" />
<link rel="alternate" hreflang="id-id" href="https://domain.com/id/page" />
<link rel="alternate" hreflang="x-default" href="https://domain.com/page" />
```
- Wix: inject via seoData.tags with type: "link"
- Shopify: inject via theme head snippet

### Fix: Add AI Crawler Allowlist to robots.txt
For any platform with editable robots.txt:
```
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: OAI-SearchBot
Allow: /
```

### Fix: Create llms.txt
Both platforms: create a plain-text page at the root path `/llms.txt`
- Wix: create a blank page with URL slug "llms" → content via text element (or custom HTML)
  Note: Wix may not serve as plain text; use a custom HTML widget with pre-formatted text
  Better approach: use Wix's static file hosting or embed via Velo/custom domain
- Shopify: create a new page with handle "llms" → NOT a blog post, a standalone page
  Add `content_type: text/plain` via theme override if needed

---

## BACKLINK ASSESSMENT (Pre-Fix Context)

Before large-scale on-page fixes, check link health via Ahrefs MCP:
```
mcp__claude_ai_Ahrefs__site-explorer-domain-rating     → DR benchmark (SG SME avg: DR 15-35)
mcp__claude_ai_Ahrefs__site-explorer-referring-domains → total RDs + trend (growing/shrinking)
mcp__claude_ai_Ahrefs__site-explorer-anchors           → anchor text distribution (over-optimized = risk)
mcp__claude_ai_Ahrefs__site-explorer-broken-backlinks  → broken backlinks to reclaim
mcp__claude_ai_Ahrefs__site-explorer-backlinks-stats   → new/lost link velocity
```

**Anchor text health — HHI formula (from seo-agency MASTER SCORING SYSTEM Formula 6):**
```
HHI = Σᵢ(sᵢ²) × 10,000  [s₁=branded, s₂=exact, s₃=partial, s₄=naked, s₅=generic]

< 2,000: healthy  |  2,000-3,500: moderate  |  3,500-6,000: concentrated  |  >6,000: critical

HARD OVERRIDE RULES (apply regardless of HHI total):
  s₂ (exact-match) > 0.20: HIGH RISK — diversify immediately
  s₂ (exact-match) > 0.35: CRITICAL RISK — disavow review + diversification campaign

Target distribution: Branded≥40%, Naked≥20%, Partial≥15%, Generic≥10%, Exact≤5%
```
Source: Ahrefs site-explorer-anchors. Compute before any link-building campaign.

**Toxic link flags:**
- RD from spam TLDs (.xyz, .click, .info in bulk) → flag for disavow review
- DR 0-5 sites with 100+ outbound links → flag
- Link velocity z-score >+3.0 (see seo-agency Formula 8) → investigate for PBN/link farm

**Semrush backlink cross-check (for high-stakes audits):**
```
mcp__claude_ai_Semrush__backlink_research  → referring domain overlap with Ahrefs data
```

---

## VERIFICATION CHECKLIST AFTER ANY FIX

```
[ ] Read back the saved content via the same API (GET/graphql_query)
[ ] Confirm the specific fields changed correctly
[ ] Open the page in an incognito browser window
[ ] Check: title tag in browser tab matches intended tag
[ ] Check: meta description via right-click > View Page Source
[ ] Check: schema via Google Rich Results Test (Rich Results Test URL)
[ ] Check: no broken internal links introduced
[ ] Cross-check: Ahrefs site-explorer-crawled-pages in 24-48h for indexed status
```
