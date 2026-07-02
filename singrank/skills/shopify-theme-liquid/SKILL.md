---
name: shopify-theme-liquid
description: >
  Advanced Shopify theme engineering — Liquid code, Online Store 2.0 JSON
  templates, section/block schema, and theme file mutations via the Admin
  GraphQL API. Use whenever the task requires actually EDITING theme code
  (not just SEO metafields): "edit theme", "ganti theme", "update Liquid",
  "buat section baru", "theme file", "publish theme", "theme.liquid",
  "section schema", "app block", "large theme file push", "theme check",
  "duplicate theme". This is the execution layer beneath seo-platforms for
  anything touching actual theme code rather than content/metafields.
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  singrank:
    tags: [Shopify, Liquid, Theme, GraphQL, Online-Store-2.0]
    related_skills: [seo-platforms, singrank-playbook]
---

# Shopify Theme & Liquid Engineering

Execution layer for actual theme-code changes (Liquid files, JSON templates,
section schema) via the Shopify Admin GraphQL API. `seo-platforms` covers
content/metafield SEO fixes; this skill covers the theme itself.

---

## 0. THE ONE HARD RULE — NEVER HARDCODE, ALWAYS VERIFY LIVE

Shopify's Admin API is versioned and evolves. **Never trust a mutation shape
from memory or from this file alone** — the Shopify MCP ships tools
specifically to prevent hallucinated fields:

```
1. mcp__claude_ai_Shopify__graphql_schema('Mutation')       → confirm the mutation exists + exact name
2. mcp__claude_ai_Shopify__graphql_schema('<InputType>')    → confirm exact input fields (returns full nested closure)
3. mcp__claude_ai_Shopify__search_docs_chunks(...)          → pull a live worked example from shopify.dev
4. mcp__claude_ai_Shopify__validate_graphql_codeblocks(...) → validate BEFORE executing
5. mcp__claude_ai_Shopify__graphql_mutation(...) / graphql_query(...) → execute only after validation passes
```

Skip step 1–4 only for the two mutations explicitly confirmed below (their
exact shape is verified against live shopify.dev docs as of this skill's
writing) — even then, re-verify if Shopify's API version has since changed
or the mutation errors unexpectedly.

If `graphql_schema` reports "requires re-authorization" or similar, tell the
user the Shopify MCP session expired — do not fall back to guessing field
names.

---

## 1. THEME OBJECT MODEL

A theme is an `OnlineStoreTheme` with a **role**: `MAIN` (live/published),
`UNPUBLISHED` (draft), or `DEVELOPMENT`. Query current themes and roles
before touching anything:

```graphql
query GetThemes {
  themes(first: 20) {
    nodes { id name role createdAt updatedAt }
  }
}
```

**Golden rule (same as seo-platforms): NEVER edit a MAIN/published theme
directly for anything experimental.** Duplicate it, edit the duplicate,
preview, then publish only on explicit approval. Exception: same-risk small
fixes on a client's already-designated working theme (see the playbook
roster — e.g. RCS's current MAIN state is documented there and changes
regularly; always re-check role via the query above, don't trust stale
memory of "which theme ID is live").

---

## 2. CONFIRMED MUTATIONS (verified live against shopify.dev, 2026-07)

### `themeFilesUpsert` — create or update theme files (bulk)

```graphql
mutation themeFilesUpsert($files: [OnlineStoreThemeFilesUpsertFileInput!]!, $themeId: ID!) {
  themeFilesUpsert(files: $files, themeId: $themeId) {
    upsertedThemeFiles { filename }
    job { id }
    userErrors { field message }
  }
}
```
```json
{
  "themeId": "gid://shopify/OnlineStoreTheme/<id>",
  "files": [
    { "filename": "templates/index.json", "body": { "type": "TEXT", "value": "{ \"sections\": {}, \"order\": [] }" } },
    { "filename": "assets/custom-content.txt", "body": { "type": "BASE64", "value": "<base64>" } },
    { "filename": "assets/large-image.jpg", "body": { "type": "URL", "value": "<https-url>" } }
  ]
}
```

Three body types:
- `TEXT` — inline raw text/Liquid/JSON. Fine for small-to-medium files.
- `BASE64` — inline binary or text as base64.
- `URL` — Shopify fetches the file content from a public HTTPS URL. **This
  is the only reliable path for large Liquid/JSON files** (proven pattern:
  gist → raw URL → `themeFilesUpsert` with `type: URL`). Use this whenever
  the file is too large to inline without blowing the MCP token budget
  (rule of thumb: if the raw file is >~20-30KB, use URL, not TEXT).

**themeFilesUpsert is a WHOLE-FILE REPLACE — there is no patch/diff API.**
Always fetch the current file first, apply your edit locally (preserve the
original line endings — many theme files use `\r\n`), then push the full
file back. Never reconstruct a large file from memory/summary.

**Big-file workflow (proven on ABLINK + RCS, both 50–250KB theme files):**
1. `graphql_query` → read the current file content (if >30KB, expect the
   read itself to be large — process to disk, don't hold it all in context)
2. Edit the local copy, preserving exact whitespace/line-ending style
3. `gh gist create <local-file>` → get the raw content URL
4. `themeFilesUpsert(themeId, files: [{ filename, body: { type: URL, value: rawUrl } }])`
5. Verify via the returned `upsertedThemeFiles` + a follow-up read;
   compare content or checksum to confirm the intended change landed
6. Delete the gist (it was only a transport mechanism, not a record)
7. Render-verify: view the storefront with `?preview_theme_id=<themeId>`
   (works for unpublished themes on the live domain)

### `themeFilesDelete` — remove theme files

```graphql
mutation themeFilesDelete($themeId: ID!, $files: [String!]!) {
  themeFilesDelete(themeId: $themeId, files: $files) {
    deletedThemeFiles { filename }
    userErrors { field message }
  }
}
```
Requires `write_themes` scope. **Only delete files you created/that are
demonstrably unused** (e.g. a scratch snippet) — never delete a section,
template, or asset that might be referenced elsewhere without first grepping
the theme for references to that filename. This does NOT touch site content
(articles/products/pages) — the no-delete-content rule from the playbook is
about client content, not dead code cleanup, but when in doubt, ask first.

### Other theme mutations (verify via `graphql_schema('Mutation')` before use)

These exist in the Admin API but were not re-verified in this skill's most
recent research pass — confirm exact input shape live before calling:
`themeCreate` (upload a new theme from a zip/URL), `themeDuplicate`
(duplicate an existing theme — the standard "safe draft" workflow),
`themePublish` (promote a theme to MAIN — publishing is often blocked via
API on some plans/store configs; if it errors, the user may need to publish
manually from Shopify Admin), `themeFilesCopy` (copy files within/between
themes), `themeDelete`. Always run the verify-first workflow (§0) for these.

---

## 3. LIQUID LANGUAGE REFERENCE

### Core objects
```liquid
{{ shop.name }}  {{ shop.description }}  {{ shop.domain }}
{{ product.title }}  {{ product.price | money }}  {{ product.featured_image | image_url: width: 800 }}
{{ article.title }}  {{ article.content }}  {{ article.author }}  {{ article.published_at | date: '%B %d, %Y' }}
{{ collection.title }}  {{ collection.products }}
{{ page.title }}  {{ page.content }}
{{ section.settings.<key> }}   {{ block.settings.<key> }}
{{ request.page_type }}  {{ template.name }}  {{ template.suffix }}
```

### Metafield access (any resource)
```liquid
{{ product.metafields.namespace.key }}
{{ article.metafields.custom.faq.value }}   {# type: json → returns parsed data #}
{% if article.metafields.custom.faq.value != blank %} ... {% endif %}
```

### Control flow & iteration
```liquid
{% if condition %} ... {% elsif other %} ... {% else %} ... {% endif %}
{% unless condition %} ... {% endunless %}
{% for item in collection.products limit: 8 %} ... {% endfor %}
{% case variable %} {% when 'a' %} ... {% when 'b' %} ... {% endcase %}
{% assign x = 'value' %}  {% capture y %} ... {% endcapture %}
```

### Includes / modularity
```liquid
{% render 'snippet-name', param: value %}   {# preferred — scoped, no access to parent variables except passed params #}
{% section 'section-name' %}                 {# renders a section file #}
```
`render` is preferred over the deprecated `include` — `include` leaks the
parent scope and is slower; new code should always use `render`.

### Common filters
```liquid
{{ value | money }}  {{ value | money_with_currency }}
{{ string | upcase }} {{ string | downcase }} {{ string | capitalize }}
{{ string | truncate: 100 }}  {{ string | strip_html }}  {{ string | escape }}
{{ array | join: ', ' }}  {{ array | first }}  {{ array | size }}
{{ image | image_url: width: 800 }} {{ image | image_tag: loading: 'lazy' }}
{{ date | date: '%Y-%m-%d' }}
{{ json_object | json }}
```

### Section schema (Online Store 2.0)
Every section file (`sections/*.liquid`) ends with a `{% schema %}` block
defining its settings and (optionally) blocks:

```liquid
{% schema %}
{
  "name": "Custom Hero",
  "settings": [
    { "type": "text", "id": "heading", "label": "Heading", "default": "Welcome" },
    { "type": "image_picker", "id": "image", "label": "Background image" },
    { "type": "url", "id": "cta_link", "label": "Button link" },
    { "type": "richtext", "id": "body", "label": "Body text" }
  ],
  "blocks": [
    {
      "type": "feature",
      "name": "Feature item",
      "settings": [
        { "type": "text", "id": "title", "label": "Title" },
        { "type": "textarea", "id": "description", "label": "Description" }
      ]
    }
  ],
  "presets": [ { "name": "Custom Hero" } ]
}
{% endschema %}
```
Common setting types: `text`, `textarea`, `richtext`, `image_picker`, `url`,
`checkbox`, `range`, `select`, `color`, `font_picker`, `product`,
`collection`, `blog`, `article`, `page`, `video`, `liquid` (raw Liquid
input — powerful but sanitize/scope carefully).

### JSON templates (Online Store 2.0)
`templates/*.json` compose a page from sections, decoupled from the theme's
Liquid — this is what makes drag-and-drop section reordering possible:

```json
{
  "sections": {
    "main": { "type": "main-article", "settings": {} },
    "related": { "type": "related-articles", "settings": { "heading": "You might also like" } }
  },
  "order": ["main", "related"]
}
```
Section keys in `order` must exactly match keys in `sections`. Reference a
non-existent section type → the page silently omits that block, doesn't
error — always render-verify after a template edit.

### App blocks
Theme app extensions expose blocks that merchants add via the theme editor;
`{% schema %}` on an app block section is similar but scoped to the app —
relevant if a client's SEO/tracking widget ships as an app block rather than
a raw section (check before assuming a widget is hand-coded, e.g. compare
against ABLINK's hand-coded `ablink-wa-widget.liquid` which is a raw section,
not an app block).

---

## 4. SCHEMA / SEO INJECTION AT THEME LEVEL

Shopify strips `<script>` tags from article/page/product body HTML — all
structured data MUST be injected via theme Liquid, not content:

```liquid
{% if article %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": {{ article.title | json }},
  "author": { "@type": "Organization", "name": {{ shop.name | json }} },
  "datePublished": "{{ article.published_at | date: '%Y-%m-%d' }}",
  "dateModified": "{{ article.updated_at | date: '%Y-%m-%d' }}"
}
</script>
{% endif %}
```

Per-article dynamic schema from a metafield (proven pattern, RCS FAQ system):
metafield `custom.faq` (type `json`, ownerType `ARTICLE`) holds
`[{question, answer}]`; the section renders BOTH a visible accordion AND a
separate FAQPage `<script>` block from the same data, guarded by a blank
check so empty articles render nothing:

```liquid
{% if article.metafields.custom.faq.value != blank %}
  <div class="faq-accordion">
    {% for qa in article.metafields.custom.faq.value %}
      <details><summary>{{ qa.question }}</summary><p>{{ qa.answer }}</p></details>
    {% endfor %}
  </div>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org", "@type": "FAQPage",
    "mainEntity": [
      {% for qa in article.metafields.custom.faq.value %}
      { "@type": "Question", "name": {{ qa.question | json }},
        "acceptedAnswer": { "@type": "Answer", "text": {{ qa.answer | json }} } }
      {% unless forloop.last %},{% endunless %}
      {% endfor %}
    ]
  }
  </script>
{% endif %}
```
Set the metafield value via `metafieldsSet` (type `json`, value = stringified
array) — separate mutation from theme files, but the two work together.

---

## 5. PERFORMANCE (CWV) IN LIQUID

```liquid
{# Explicit width/height kills CLS #}
<img src="{{ image | image_url: width: 800 }}" width="{{ image.width }}" height="{{ image.height }}"
     loading="lazy" alt="{{ image.alt | escape }}">

{# LCP hero image: preload, no lazy-load #}
<link rel="preload" as="image" href="{{ section.settings.image | image_url: width: 1600 }}">
<img src="{{ section.settings.image | image_url: width: 1600 }}" loading="eager" fetchpriority="high">

{# Defer non-critical JS #}
<script src="{{ 'custom.js' | asset_url }}" defer></script>

{# font-display swap in theme CSS/settings #}
@font-face { font-display: swap; }
```
Audit installed Apps first — most CWV regressions on Shopify come from app
script injections, not theme code. Heavy apps often can't be fixed in
Liquid; the fix is disabling/replacing the app.

---

## 6. SAFE CHANGE WORKFLOW (mandatory sequence)

```
1. Query themes → confirm which ID is MAIN vs UNPUBLISHED right now (§1)
2. If experimenting: themeDuplicate the target (or use an existing
   designated working/draft theme — check the playbook roster for the
   client's current documented state, but ALWAYS re-verify with the query,
   theme roles change over time as work gets published)
3. Read the target file(s) first — never edit blind
4. Make the change locally; preserve line endings; keep the diff minimal
5. Push via themeFilesUpsert (TEXT for small, gist→URL for large — §2)
6. Verify: re-read the file OR check upsertedThemeFiles response, AND
   render-check via ?preview_theme_id=<themeId> on the live domain
7. If schema/JSON template: verify no reference breaks (order[] matches
   sections{} keys; app block types still installed)
8. Only publish (themePublish or manual Admin action) on explicit approval
9. After publish: re-check the live URL (no preview param) to confirm
```

## 7. PER-CLIENT THEME NOTES

Cross-reference `singrank-playbook` for the authoritative, current roster —
theme IDs and roles change as work gets published. Do not hardcode IDs here;
always confirm role via the themes query (§1) before editing. Client-specific
constraints that persist regardless of which theme ID is currently live:
- **ablink.sg** — read/write API key split; confirm the admin key is active
  before any mutation (a read-only key will fail mutations silently-ish —
  check `userErrors`).
- **renovationcontractorsingapore.com (RCS)** — large theme files
  (50–250KB) are normal; always use the gist→URL path, never TEXT inline.
- Both have used the gist→URL big-file pattern successfully — it is the
  proven default for any theme file expected to exceed ~20-30KB.
