---
name: singrank-pipeline
description: >
  The SingRank WINNING PIPELINE — end-to-end flow from idea discovery to
  published, interlinked, GEO-ready, tracked content. Use when running a full
  content campaign, launching new topics, or when asked "dari idea sampai
  publish", "full pipeline", "cara menang", "win this keyword", "campaign
  lengkap", or any request that spans discovery → brief → writing → publishing
  → tracking. Orchestrates seo-agency, seo-geo, seo-platforms, and
  singrank-article-writer in the correct order with gates between stages.
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  singrank:
    tags: [SEO, GEO, Pipeline, Content, Campaign]
    related_skills: [singrank-playbook, seo-agency, seo-geo, seo-platforms, singrank-article-writer]
---

# SingRank Winning Pipeline: Idea → Published → Tracked

Ten stages, each with a GATE. Do not skip a gate — a failed gate sends the
work back, not forward. Read `singrank-playbook` first for formulas (F1–F10),
client constraints, and output format.

---

## STAGE 0 — Baseline (always)

Pull the core data set: `list_clients` → `bootstrap_briefing` → `site_health`
→ `gsc_summary` → `anomalies` → `ai_visibility` → `fetch_log`.

**GATE 0:** Data fresh (per `fetch_log`)? Client constraints loaded from the
playbook roster? If data is stale → tell the user, do not proceed on guesses.

## STAGE 1 — Structural clearance

**Structural first: never build new content on a broken foundation.**
- `find_cannibalization` → any pair with SERP_overlap ≥0.40 (F6) touching the
  target topic must be resolved (consolidate/canonical/de-optimize) first.
- `site_health` + `broken_links` → Critical crawl issues fixed first.
- `suggest_interlinks` → note orphans to fix alongside the new content (F7).

**GATE 1:** No CRITICAL cannibalization on the target topic; no Critical
crawl blockers. Otherwise fix those first (they usually out-Priority new
content under F1 anyway).

## STAGE 2 — Opportunity discovery (the "idea")

Run in parallel:
- `keyword_gap` — keywords competitors rank for, we don't
- `content_gap` — topics competitors cover, we don't
- `content_targets` — existing pages most worth improving
- `high_intent_articles` — pages closest to converting
- GSC positions 4–20 → score with **ROS (F2)**
- Ahrefs `keywords-explorer-overview` → volume + difficulty for candidates
- Semrush `organic_research` on top 2–3 competitors → cross-check

**GATE 2:** Every candidate has: search volume (verified, not guessed),
ROS or gap evidence, and intent_fit ≥0.7 for the client's money pages.

## STAGE 3 — Prioritize

Score every candidate with **F1 Priority** (improve-existing counts
AffectedPages ≥1 and usually beats net-new on Effort). Sort DESC. Present the
top list to the user with calculations shown. Improve-existing vs net-new is
decided here: if `content_targets` shows a page with V(t) <0.60 (F5) on the
same topic → refresh THAT page, don't create a duplicate (avoids future
cannibalization).

**GATE 3:** User (or the brief) confirms the target list. One primary
keyword + intent per URL — never two URLs chasing one keyword.

## STAGE 4 — SERP + AI-SERP recon

For each confirmed target:
- Ahrefs `serp-overview` → who ranks, DR range, content type that wins,
  SERP features (apply the F2 SERP modifier honestly).
- `geo_briefing` + `geo_answerability_score` → what the AI engines need.
- Ahrefs `brand-radar-cited-pages` → which pages AI engines already cite for
  this topic — that structure is the citability benchmark.

**GATE 4:** We can realistically beat the weakest top-5 result (content
angle, depth, or freshness edge identified in writing). If DR gap is
hopeless, re-route to a longer-tail variant instead of burning effort.

## STAGE 5 — Brief

`content_brief` (SingRank MCP) for the GEO-optimized brief, then enrich:
target keyword + 5 secondary floors, search intent, required entities, FAQ
questions (from PAA/serp-overview), internal link targets (from
`suggest_interlinks`), citation magnets to include, word-count floor,
client-specific constraints from the roster (YMYL rules for yescpap, MUIS for
saffrons, no-pricing for dehall, etc.).

**GATE 5:** Brief contains ZERO unverified statistics. Every data point in
the brief has a live source. No source = not in the brief.

## STAGE 6 — Write

Hand the brief to **singrank-article-writer**. Standards (hard floor):
- ≥2500 words, humanized, expert-level, zero fabrication
- Key Takeaway box near the top
- Citation magnets (quotable stats/definitions AI engines lift)
- 6 keyword floors respected
- FAQ section + FAQPage schema (JSON-LD)
- Language per market: British EN (SG) / Bahasa Indonesia EYD V (ID)
- Byline per client rules (e.g., Iman Yusoff for IFG/Livin)

**GATE 6:** Word count ≥2500; every claim traceable to brief sources;
keyword floors met; no health/pricing/transit-time fabrications per client
constraints.

## STAGE 7 — Publish (platform-correct, draft-first)

Via **seo-platforms**:
- Shopify: `graphql_mutation` (articleCreate/articleUpdate as draft);
  meta per client (saffrons → `global.title_tag` metafield); schema at THEME
  level; body >30KB → snippet approach; ablink → draft theme 183046078779
  only, confirm admin key first.
- Wix: `CallWixSiteAPI` Draft Posts (create draft; publish via
  UPDATE_PUBLISH when approved); FAQ schema via seoData script tag;
  relatedPostIds max 3.

**GATE 7:** Published as DRAFT first. Meta title ≤60 chars, meta description
140–155 chars, CTR-optimized. User approves before going live unless standing
approval exists for that client.

## STAGE 8 — Interlink + GEO layer

- `suggest_interlinks` → add 3–5 contextual inbound links from relevant
  existing pages TO the new page (kills orphan status day one), and outbound
  links from the new page to money pages.
- GEO: verify answerability (`geo_answerability_score`), llms.txt updated if
  the client has one, schema valid, citation magnets present.
- Anchor discipline: check F8 — no exact-match anchor stuffing.

**GATE 8:** New page has ≥3 inbound internal links and passes answerability;
anchors diversified.

## STAGE 9 — Track + learn

- Log the play: target keyword, publish date, baseline position/impressions.
- Check `algo_events` before attributing any movement to the content.
- Day 14 & 28: `gsc_page_trend` / `gsc_query_trend` → score movement with
  **SDS (F3)** — act only ≥2.0; ignore noise <1.65.
- If decayed later: **F5** decides refresh vs rewrite; if dropped: **F4 RPS**
  decides fix-in-place vs deep rewrite vs consolidate.
- Feed the outcome back: what angle won/lost goes into the next Stage 2.

**GATE 9 (loop):** Every published piece has a scheduled 14/28-day check.
The pipeline is a loop, not a line.

---

## Compressed cheat-sheet

```
0 Baseline    → fresh data or stop
1 Structure   → no cannibal/crawl blockers on topic
2 Discover    → keyword_gap + content_gap + ROS(F2)
3 Prioritize  → F1 sort; refresh-vs-new via F5
4 Recon       → serp-overview + geo benchmark; beatable or re-route
5 Brief       → content_brief + zero unverified stats
6 Write       → article-writer standard (≥2500w, takeaway, magnets, FAQ)
7 Publish     → draft-first, platform-correct, meta optimized
8 Interlink   → ≥3 inbound links + GEO layer + anchor check(F8)
9 Track       → SDS(F3) @ d14/d28; decay F5; recovery F4; learn → loop
```
