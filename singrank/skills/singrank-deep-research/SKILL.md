---
name: singrank-deep-research
description: >
  SingRank gap-to-article deep research engine. The full hunt: audit the client's
  weaknesses/gaps → find keywords OUTSIDE the SingRank System footprint (competitor +
  keyword expansion) → tear down the Google top-10 for the chosen keyword → deep-research
  valid, relevant facts with provenance → hand a verified RESEARCH BRIEF to the
  article-writer for a high-conversion, naturally-human article. Trigger phrases: "cari
  gap", "artikel selanjutnya apa", "next article", "keyword dari competitor", "bedah top
  10", "deep research [topic]", "riset mendalam", "compare top 10 google". Every fact in
  the output brief is live-verified or marked [VERIFY] — never guessed.
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  singrank:
    tags: [Research, Gap, SERP, Competitor, Keywords, Brief, Provenance]
    related_skills: [singrank-article-writer, singrank-writing-craft, singrank-pipeline, singrank-qc, singrank-playbook]
---

# SingRank Deep Research v1.0 — Gap → Keyword → SERP Teardown → Verified Brief

One mission: find what to write NEXT that the client can win, prove it with the SERP,
research it deeper than every competitor, and hand the writer a brief where every fact
carries a live source. The article's job is SALES — so the brief must arrive with the
conversion path already decided.

Tools: `C:\Users\natur\singrank-plugin\singrank\tools\` (Python) + SingRank System MCP +
Claude's WebSearch.

---

## PHASE 1 — GAP HUNT (where is the opportunity?)

Start from SingRank System — the weapon:
1. `brain{doc:'audit'}` + `brain{doc:'content'}` + `brain{doc:'ideas'}` — precomputed
   weaknesses, CTR leaks, and NEW-keyword ideas outside our footprint (zero calls).
2. `keyword_gap {domain}` — clusters where demand exists but coverage is weak;
   `losingClicksToSerp` = cheapest wins (title/meta, not new content — route those out).
3. `competitor_gap {domain, competitor}` — topics competitors cover that we don't,
   ranked by impressions we ALREADY get on matching queries. No crawled competitor →
   call without `competitor` to list candidates worth crawling.
4. `content_targets {domain}` → `writeNew` bucket; `lead_content_ideas {domain}` →
   `newArticleIdeas` (keywords proven to convert on similar pages).
5. **Outside the footprint:** `keyword_research {seed, market, depth:'full'}` — expand
   head terms via Autocomplete + kwvol + Trends. Rows with source `gsc` = real volume;
   `trends` = estimate; `autocomplete` = idea. State the confidence.

## PHASE 1b — SIBLING EXPANSION (mine our OWN high-impression assets)

The cheapest new winner is a SIBLING of an existing winner: Google already shows us
demand it half-trusts us for. Mine SingRank System for it:

1. **High-impression, weak-position clusters:** `keyword_gap.topicClusters` where
   impressions are large but avgPosition >15 (e.g. a cluster pulling 20k impressions at
   pos 30 = massive proven demand we're failing). Decide per cluster: strengthen the
   existing page (interlinks + rewrite via `rank_reasons`) OR spin a SIBLING article at
   a DIFFERENT angle the cluster's queries reveal.
2. **Winner-page overflow queries:** `gsc_top_pages` → for each high-impression winner,
   `gsc_top_queries` / the page's query list → queries it gets impressions for but
   whose INTENT it doesn't actually serve (a size-guide page pulling "renovation cost"
   impressions serves the wrong intent) → each mismatched high-impression query is a
   sibling candidate.
3. **High-impression queries with no dedicated page:** `gsc_top_queries {sort_by:
   'impressions'}` at position >10 → cross-check `search_articles` — no page whose
   primary intent matches → sibling candidate.
4. **Angle spin via the 9-angle matrix** (pipeline Stage 2): one winning topic legally
   becomes up to 9 articles — cost guide / comparison / area page / problem→solution /
   timeline / mistakes / rules / package / case story — each a DIFFERENT primary
   intent. A winner on "X rules" with big impressions almost always supports a sibling
   on "X cost" and "X timeline". Copy the winner's exact structure
   (`winning_patterns.exemplarWinners`) with the new angle's content.

Sibling candidates enter the same GATE 1 below — the 3-part cannibalization test is
what keeps "similar" from becoming "competing": a sibling passes ONLY with a distinct
primary intent, materially different SERP, and distinct funnel stage or entity. Fails →
it's a strengthen-the-original job, not a new article.

**GATE 1:** candidate keyword list (external gaps from Phase 1 + siblings from Phase
1b) where each has: demand evidence (volume or real impressions), a client money page
it can feed, intent_fit ≥0.7, a PASSED 3-part cannibalization test (distinct intent /
distinct SERP / distinct funnel-or-entity vs every live article —
`find_cannibalization` + `search_articles`), and lane-lock clearance (KG Teknik ↔
Rajawangi). Score with ROS/CPS (playbook F2/F9) — a sibling with high proven
impressions usually outranks an external gap with estimated volume, because the demand
is already OURS to lose. Present the top 3–5, pick one (ask the user if the choice
isn't obvious).

## PHASE 2 — SERP TEARDOWN (what does winning look like?)

1. `WebSearch "<target keyword>"` → collect the top ~10 organic URLs. Note SERP
   features honestly (AI Overview / snippet / local pack → F2 modifiers).
2. Tear them all down in one command:
```
python tools/deep_research.py --keyword "<kw>" --urls <url1> <url2> ... \
    --out serp-teardown.md --json serp.json
```
   Returns: benchmark (median words, H2 count, table usage, number density,
   freshness, schema in use), coverage matrix (subtopics you MUST cover),
   **⭐ GAP candidates** (subtopics ≤2 pages cover — your information-gain sections),
   question bank (their headings — answer them better), fact bank (stat sentences +
   source URL — provenance candidates).
3. `winning_patterns {domain}` — OUR winner profile for this client; where it
   conflicts with the SERP benchmark, satisfy both (e.g. SERP median 1,800w but our
   winners run 2,900w → write 2,900w).

**GATE 2:** a beat-plan exists: which mandatory subtopics we'll match, which 2–3 GAP
sections we'll own that nobody covers, the table(s) we'll build (AI engines lift tables
verbatim), and the freshness/depth edge. If the SERP is unbeatable (all DR-90 giants,
no angle), go back to Phase 1 and pick a longer-tail sibling.

## PHASE 3 — DEEP FACT RESEARCH (valid + relevant, with provenance)

For every planned section, gather facts in this priority order:
1. **Primary sources first:** WebSearch restricted to authorities (HDB/BCA/LTA/MUIS/
   gov.sg, BPS/Kemenkes/go.id, official event pages) → `python tools/web_research.py
   fetch <url>` to read; the tool flags `primary_source: true`.
2. **SOURCE AUTHENTICITY TEST — is this the origin or a reteller?**
   `python tools/web_research.py source-check <url>` grades every candidate source:
   - **PRIMARY** (authority domain) / **ORIGINAL-RESEARCH** (own methodology/survey/
     data) → citable directly.
   - **SECONDARY / AGGREGATOR** → the page retells someone else; the tool lists the
     origins it names. **TRACE THE CHAIN:** fetch the named origin, source-check IT,
     and cite the origin — never the reteller. A stat that survives two retellings is
     often distorted; the origin has the exact figure, date, and context.
   - **UNCLEAR** → treat as opinion; find a stronger source or mark `[VERIFY]`.
3. **Fact bank from Phase 2:** every borrowed stat gets re-verified at ITS origin —
   `python tools/web_research.py verify <origin-url> "<claim>"` → only EXACT or
   PARAPHRASE enters the brief. NOT-FOUND/UNREACHABLE → drop it or mark `[VERIFY]`.
4. **TRIANGULATION rule for critical numbers** (prices, regulations, dates that carry
   the sales angle): 1 PRIMARY source is enough; anything less needs **2+ independent
   sources** (independent = neither cites the other — check with source-check). Two
   sources that disagree → publish the honest RANGE with both attributions, never pick
   the convenient number.
5. **Bulk mode (many sources, zero Claude tokens on raw pages):**
   `python tools/smart_scrape.py --topic "<topic>" --urls <seeds...> [--depth 1]`
   — parallel fetch → GPU embedding relevance filter → local-LLM extraction →
   `facts.jsonl` with claim + verbatim sentence + source URL per fact. Read only
   the distilled PACK.md; then verify the facts you'll actually use (step 3).
   Ends with `python tools/llm_local.py --down` to free the GPU.
6. **First-party data:** `search_articles`/`get_article` for client facts already
   published; `gsc_top_queries` for the real query language (use THEIR words as
   longtails and H2s).
6. Relevance filter: a fact enters the brief only if it changes the reader's decision
   or serves the sales angle — the test is "so what, for THIS reader, deciding THIS?"
   Interesting-but-useless gets cut.

**GATE 3:** provenance table complete — every stat has: claim · ORIGIN source URL ·
source grade (PRIMARY/ORIGINAL-RESEARCH/triangulated) · date · confidence
(EXACT/PARAPHRASE) · freshness (<24mo or flagged). ZERO unverified numbers, ZERO
citations of retellers.

## PHASE 4 — THE BRIEF (hand-off artifact)

Merge `content_brief {domain, keyword}` (internal links, PAA, productCTA,
cannibalization warning) with the research above and emit:

```
=== SINGRANK RESEARCH BRIEF ===
CLIENT: [domain]   MODE: [per writing-craft §7]   DATE: [today]
PRIMARY KEYWORD: [one keyword, one intent]
LONGTAILS (5-10, from real GSC queries + keyword_research): [each with volume/confidence]
SEARCH INTENT + FUNNEL STAGE: [...]
SERP BENCHMARK: [median words / tables / freshness / schema — from deep_research.py]
MUST-COVER SUBTOPICS: [coverage matrix items]
⭐ INFORMATION-GAIN SECTIONS (2-3): [gap candidates nobody covers + our unique data]
QUESTION BANK: [questions to answer better than competitors]
TABLES TO BUILD: [comparison/cost/spec tables — AI engines lift these]
PROVENANCE TABLE: [claim | source URL | date | EXACT/PARAPHRASE]
INTERNAL LINKS (from content_brief, all live-confirmed): [fromAnchor → toURL]
LINKS TO BUILD TO THIS PAGE: [existing articles that should link in]
MONEY PAGE + CTA: [the ONE conversion target + client-calibrated CTA]
SALES ANGLE: [one sentence: why the reader buys after this article]
UNIQUE POV: [one thing ONLY this client can say — real project data, credential,
             first-party number, lane expertise. If every competitor could write the
             same sentence, it's not a POV. This is what makes the article un-copyable.]
EMOTIONAL DRIVER: [one — status/security/relief/pride/FOMO/hope]
COMPLIANCE FLAGS: [roster rules for this client]
GAPS STILL OPEN: [anything unresolved, marked [VERIFY]]
=== END BRIEF ===
```

Persist it: `mcp__claude_ai_SingRank_Save__put_document` (tag `research-brief`).

**GATE 4:** brief passes → hand to **singrank-article-writer** (+ writing-craft).
After the draft: **singrank-qc** gate → publish → `log_experiment`.

---

## RULES

- SingRank System data first, always. External research fills what it can't know.
- WebSearch for search; Python tools for fetch/verify/teardown (deterministic).
- A keyword without a money page and sales angle is a blog post, not an asset — reject.
- Never two URLs chasing one keyword. Never a fact without a source. Never guess.
