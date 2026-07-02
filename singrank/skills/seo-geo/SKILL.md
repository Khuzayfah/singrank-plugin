---
name: seo-geo
description: >
  GEO (Generative Engine Optimization) and AEO (Answer Engine Optimization) skill.
  Use for AI search visibility, AI crawler access audit, llms.txt generation,
  citability scoring, brand authority scanning, multi-platform AI SoV tracking,
  and GEO content structure optimization. Trigger phrases: "AI search", "AI visibility",
  "GEO", "AEO", "llms.txt", "ChatGPT ranking", "Perplexity citation", "AI Overview",
  "kenapa tidak muncul di AI", "GEO audit", "AI search share of voice".
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GEO, AEO, AI-search, llms-txt, Citability, AI-SoV, ChatGPT, Perplexity]
    related_skills: [seo-agency, seo-audit, scrapling, duckduckgo-search, seo-kb]
---

# SingRank GEO / AEO Skill v1.0

Optimizes client content and site configuration for citation by AI engines:
ChatGPT, Perplexity, Google AI Overviews, Gemini, Claude.ai, and AI Mode.

**Context (June 2026):**
- ChatGPT: ~63% of B2B AI search referrals
- Claude: ~18.5% (up from 1.4% eight months ago — fastest growing)
- Gemini: ~10.6% | Perplexity: ~7.3%
- Only 11% of domains appear on BOTH ChatGPT and Google AI Overviews for same queries
- 55% of AI Overview citations come from the first 30% of page content
- Content updated <3 months ago has 3× higher citation likelihood

---

## ALWAYS START: Pull AI Data from SingRank + Ahrefs

**SingRank MCP (GEO-specific tools — use all of these):**
```
list_clients              → domain key
geo_briefing              → pre-built GEO health summary per client
geo_answerability_score   → which pages are most answerable by AI (use to prioritize)
geo_citation_tracker      → track where client is being cited by AI engines
ai_referral_log           → actual referral traffic coming from AI platforms
ai_visibility             → current AI citation signals per client
ai_summary                → AI presence narrative
gsc_summary               → organic baseline (compare vs AI traffic delta)
published_articles        → content inventory for citability audit
```

**Ahrefs MCP (Brand Authority for GEO):**
```
mcp__claude_ai_Ahrefs__brand-radar-sov-overview        → AI Share of Voice by platform
mcp__claude_ai_Ahrefs__brand-radar-ai-responses        → AI response mentions of client
mcp__claude_ai_Ahrefs__brand-radar-cited-pages         → which pages AI engines cite
mcp__claude_ai_Ahrefs__brand-radar-cited-domains       → which competitor domains AI cites
mcp__claude_ai_Ahrefs__brand-radar-mentions-overview   → brand mention signals
```

Use `geo_briefing` as the entry point. If geo_briefing is empty (new client), run the full 5-layer protocol below.

## GEO COMPOSITE SCORE

Score the client's GEO health before and after optimization. Use this EVERY time.

```
GEO Composite Score (0.0–1.0, target ≥ 0.65 = GEO-ready):

Component              Weight  How to Score                               Your Score
─────────────────────────────────────────────────────────────────────────────────────
AI Citability          0.25    Avg citability scorecard across top 5 pages / 100
                               Example: pages scored 70, 40, 85, 60, 45 → avg = 60 → 0.60
                               
Brand Authority        0.20    Count platforms with verified presence (max 8):
                               GBP, Reddit, YouTube, Wikipedia/Wikidata, LinkedIn, 
                               G2/Capterra, Local media mention, Industry directory
                               Score = platforms_present / 8
                               Example: 5/8 = 0.625
                               
Content + E-E-A-T      0.20    Use seo-audit Category 3 score / 100
                               Example: cat3_score=80 → 0.80
                               
Technical Foundation   0.15    AI bots allowed / 14 × (SSR_check: 1.0 if all SSR, 0.5 if JS-heavy)
                               Example: 12/14 bots allowed × 1.0 = 0.857
                               
Schema Quality         0.10    Use seo-audit Category 4 score / 100
                               Example: cat4_score=50 → 0.50
                               
Platform SoV           0.10    mentions_in_sample_queries / total_sample_queries
                               Example: appears in 3 of 20 test queries → 3/20 = 0.15
─────────────────────────────────────────────────────────────────────────────────────

GEO Score = (0.60×0.25) + (0.625×0.20) + (0.80×0.20) + (0.857×0.15) + (0.50×0.10) + (0.15×0.10)
          = 0.150 + 0.125 + 0.160 + 0.129 + 0.050 + 0.015
          = 0.629 → Borderline GEO-ready (above 0.65 threshold? No → identify weakest component)

Fix priority: lowest (weight × score) contribution first = Platform SoV here.
```

---

## GEO AUDIT — 5 LAYER PROTOCOL

Execute layers in order. Layer 1 failures block all other layers — fix first.

### LAYER 1 — AI Crawler Access (Critical Foundation)

If AI crawlers are blocked, zero GEO impact regardless of content quality.

**Check robots.txt** (scrapling: `https://domain.com/robots.txt`):
```
Required: these crawlers must be ALLOWED
User-agent: GPTBot           → ChatGPT crawler
User-agent: OAI-SearchBot    → ChatGPT search
User-agent: ClaudeBot         → Claude.ai crawler
User-agent: PerplexityBot     → Perplexity crawler
User-agent: Google-Extended   → Google AI training data
User-agent: Googlebot-Extended→ Google AI Overview
User-agent: Applebot-Extended → Apple Intelligence
User-agent: CCBot             → Common Crawl (Llama/GPT training)
User-agent: Amazonbot         → Amazon Alexa AI
User-agent: meta-externalagent→ Meta AI crawler
User-agent: Bytespider        → TikTok/ByteDance AI
User-agent: Diffbot           → AI content extraction
User-agent: cohere-ai         → Cohere AI training
User-agent: anthropic-ai      → Anthropic training data

Flag: any of these listed under Disallow: / → CRITICAL
```

**Check WAF/CDN (Cloudflare, Sucuri, AWS WAF):**
- AI crawlers are often blocked by bot management rules that treat them as scrapers
- Check if the User-Agent strings above get 403 or 429 responses
- Wix and Shopify CDNs: usually allow bots by default; verify if custom WAF rules exist

**Check JS rendering:**
- AI crawlers cannot execute JavaScript
- Raw HTML source must contain ALL critical content (title, H1, body, schema)
- If content is JS-rendered → AI crawlers see empty pages → zero citation potential

### LAYER 2 — /llms.txt (AI Context File)

llms.txt is a plain-text file at `domain.com/llms.txt` that tells AI systems what your site
is about, what your key content is, and how to reference you.
Spec: `github.com/AnswerDotAI/llms-txt`

**Audit:** Does `domain.com/llms.txt` exist? (scrapling: raw fetch)
**Generate if missing:**

```markdown
# [Company Name]

[Company name] is [1-sentence description of what the company does, including market/location].

## Main Services / Products
- [Service 1]: [brief description]
- [Service 2]: [brief description]

## Key Pages
- [Page Title](https://domain.com/page-url): [what this page covers]
- [Key Category](https://domain.com/category): [description]

## About
Founded [year]. Based in [city/country]. [Key credential or differentiator].

## Contact
[contact page URL or email]

## Content License
Content available for AI training under [license or "All rights reserved"].
```

**llms-extended.txt** (optional, for richer AI context):
Include full text of top 5-10 pages, properly separated by `---` delimiters.
Helps AI systems that read extended context for better citation accuracy.

### LAYER 3 — Content Citability Scoring

**Optimal citation block: 134–167 words (self-contained)**
Source: Princeton GEO research (Aggarwal et al., KDD 2024) + practitioner consensus.

**Per-page citability score card (0–100 points, consistent across all pages):**

```
CITABILITY SCORECARD — [URL]

Signal                                      Points  Your Score
────────────────────────────────────────────────────────────
Direct answer in first 150 words            25      [ ]
≥3 self-contained H3 blocks of 134-167w    25      [ ]  (each block opens with answer)
≥2 named expert quotes (name + title + org) 20      [ ]  (10pts each, max 20)
≥3 statistics with named source + year      15      [ ]  (5pts each, max 15)
Content updated within last 3 months        15      [ ]
────────────────────────────────────────────────────────────
TOTAL                                       100     [ ]

Interpretation:
  ≥70: HIGH citability — likely to appear in AI responses
  40-69: MEDIUM — fixable; focus on the lowest-scoring signals first
  <40:  LOW — not AI-citation-ready; deep rewrite needed

Action priority: score from LOWEST to HIGHEST → fix cheapest signals first.
  Easiest lift: update date (if ≤1mo away from 3-month threshold)
  Second: add 1 named stat with source (adds +5 points)
  Third: restructure 1 H3 section into 134-167w self-contained block (+8 points)
  Hardest: add expert quote (requires outreach or internal expert interview)
```

**Citability audit per page — step by step:**
1. Fetch raw HTML (scrapling) — confirm content is SSR (not JS-injected)
2. Extract first 150 words → does it answer the page's primary query directly? (Yes/No)
3. For each H3 section: count words → target 134-167w per block
4. For each H3: does the first 2 sentences answer the sub-question directly? (Yes/No)
5. Count named expert quotes (must have: name + title + organization)
6. Count statistics with named source + year (e.g., "According to Singapore Tourism Board (2025)…")
7. Check publish/update date in Article schema vs actual content recency
8. Score → priority fix list

**GEO Citation Probability (relative multiplier — compare pages, not absolute):**
```
P_relative = 1.0 × ∏(1 + boost_i)

Boosts (multiply per signal found):
  Direct answer first 150w:     × 1.55
  Each 134-167w block (cap 5):  × 1.35 per block
  Each expert quote (cap 3):    × 1.41 per quote
  Each stat + named source:     × 1.30 per stat (cap 5)
  Fresh content <3 months:      × 3.00
  Question-formatted headings:  × 1.25

Worked example — Page A (weak):
  No direct answer, 2 blocks, 0 quotes, 1 stat, fresh content
  P = 1.0 × 1.35 × 1.35 × 1.30 × 3.00 = 7.1×

Worked example — Page B (optimized):
  Direct answer, 4 blocks, 2 quotes, 3 stats, fresh content
  P = 1.55 × 1.35⁴ × 1.41² × 1.30³ × 3.00 = 1.55×3.32×1.99×2.20×3.00 = ~67.6×

Page B is ~9.5× more likely to be cited than Page A. Prioritize Page B's pattern.
Use relative ranking to decide WHICH pages to optimize first — not absolute citation chance.

**GEO Citation Efficiency Score (compare pages on a normalized 0-100 scale):**
```
P_max = max possible P_relative when ALL 5 content signals are present:
  P_max = 1.55 × 1.35⁵ × 1.41³ × 1.30⁵ × 3.00
        = 1.55 × 4.484 × 2.803 × 3.713 × 3.00
        ≈ 217

GEO_efficiency = (P_relative / 217) × 100

Targets:
  ≥ 60%: Highly optimized (P ≥ 130) — multiple signals compounding; protect this
  30–59%: Optimized (P = 65–130) — most signals present; add missing ones incrementally
  15–29%: Partially optimized (P = 33–65) — fix 2-3 key missing signals this sprint
  < 15%: Not GEO-ready (P < 33) — structural rewrite required before any AI citation likely

Worked examples:
  Page A (P_rel=7.1):   GEO_efficiency = 7.1/217 × 100 = 3.3%  → Not GEO-ready
  Page B (P_rel=67.6):  GEO_efficiency = 67.6/217 × 100 = 31.1% → Partially optimized

What Page B is missing to reach Optimized (30-59%):
  Current: 4 blocks, 2 quotes, 3 stats, fresh → P=67.6 → 31.1%
  Add 1 more stat: P = 67.6 × 1.30 = 87.9 → 40.5% → into Optimized zone
  Add 1 more block: P = 87.9 × 1.35 = 118.7 → 54.7% → solidly Optimized

Use efficiency to prioritize page-level optimization in the GEO sprint backlog.
```


### LAYER 4 — Entity + Brand Authority

AI engines heavily weight brand mentions across the web, not just links.
**Research (correlation, not causation):** brand mentions across 7+ platforms correlate
3× more strongly with AI visibility than backlinks alone.

**Platform priority by AI engine:**
```
ChatGPT    → Wikipedia presence (47.9% of citations from Wikipedia-linked content)
Perplexity → Reddit presence (46.7% of citations from Reddit-linked content)
Google AIO → E-E-A-T signals (author schema, structured data, Google Business Profile)
Gemini     → Mix of Reddit + E-E-A-T signals
Claude.ai  → High-quality long-form content + cited sources
```

**Brand authority audit:**
Scan these for client brand mentions (duckduckgo-search `site:reddit.com "[brand]"`):
- Reddit: r/singapore, r/asksingapore, r/indonesia, niche subreddits
- YouTube: channel presence + video mentions
- Wikipedia / Wikidata: entity page, sameAs links
- LinkedIn: company page completeness, employee profiles
- Industry directories: Google Business Profile, Yelp SG, Singapore Yellow Pages
- G2 / Capterra / Trustpilot (for B2B SaaS clients)
- Local media: CNA, The Straits Times, Kompas, Detik (for ID clients)

**Action for gaps:**
- No Wikipedia: build through citation-worthy content and external press first
- No Reddit presence: answer questions in relevant subreddits (not promotional)
- GBP incomplete → fill all fields (photos, Q&A, weekly posts, respond to reviews)
- Unlinked brand mentions → outreach to add link (use `domain-intel` + scrapling)

### LAYER 5 — AI Search Share of Voice (Monthly Tracking)

**Setup:**
Define 20–50 priority queries that matter for the client's business.
For each, manually check (or via `page-agent` + Perplexity/ChatGPT interface):
- Does the client appear in the answer?
- Are they cited as a source link?
- Which competitors appear instead?

**SoV Score per platform:**
```
SoV(platform) = mentions_in_sample_queries / total_sample_queries × 100
Compare vs prior month → track delta
```

**Tools:**
- `page-agent` skill → drive browser to ChatGPT/Perplexity, submit queries, read citations
- SingRank `ai_visibility` tool → platform-aggregated signals
- Open-source self-hosted: `github.com/danishashko/geo-aeo-tracker` (free)
- Manual audit for sample of 10 queries: sufficient for monthly check

**Competitor citation gap:**
For queries where competitors appear and client doesn't:
1. What page of theirs is cited? → scrapling to analyze
2. What makes it citation-worthy? (citability score, freshness, brand authority)
3. Can we match or exceed those signals? → plan specific content updates

---

## PLATFORM-SPECIFIC GEO OPTIMIZATION

### ChatGPT (GPT-4o, SearchGPT)
**What it prioritizes:** Wikipedia, high-authority domains, cited factual content
**Optimization:**
- Ensure Organization schema with sameAs links to Wikipedia/Wikidata (if applicable)
- Create content cited by other authoritative sites (link building with GEO intent)
- Named sources in every key claim (Wikipedia cross-reference helps)
- Author schema linked to recognized expert profiles

### Perplexity
**What it prioritizes:** Reddit, real-time web, first-person experience content
**Optimization:**
- Active, genuine presence on r/singapore / r/asksingapore / niche subreddits
- "Experience" language in content ("We tested…", "In our [N] projects…")
- Fresh content (Perplexity indexes recent pages heavily)
- Direct answers in first 100 words (Perplexity extracts answer snippets)

### Google AI Overviews
**What it prioritizes:** E-E-A-T, structured data, existing top-10 ranking pages
**Optimization:**
- Must rank in top 10 organically first (AI Overview draws from ranked content)
- Content in first 30% of page (55% of citations from top third)
- FAQPage schema (even if not eligible for rich results, helps AIO extraction)
- Author schema with verified credentials
- Long-form content (3000+ words) signals depth

### Gemini
**What it prioritizes:** Similar to Google AIO + Reddit signals
**Optimization:**
- Same as Google AIO approach + Reddit presence

### Google AI Mode (formerly SGE — distinct from AI Overviews)
**What it prioritizes:** Real-time web results, structured data, multi-step reasoning queries
**Optimization:**
- AI Mode activates on complex, multi-faceted queries (not simple lookups)
- Content must answer follow-up questions in depth — 1500+ words, multiple subtopics covered
- FAQPage schema + nested Q&A in body helps AI Mode chain answers
- Product schema critical for e-commerce clients in AI Mode shopping results
- Focus on establishing "source of record" for a narrow topic cluster

### Microsoft Copilot (Bing AI)
**What it prioritizes:** Bing index + authoritative cited pages + Microsoft ecosystem
**Optimization:**
- Bing Webmaster Tools verification required (separate from Google)
- Submit sitemap to Bing Webmaster Tools (often neglected for SG clients)
- Add `User-agent: Bingbot` Allow rule in robots.txt (verify not blocked)
- Copilot uses the same sources as Bing search — rank in Bing first
- Organization schema with `sameAs` to Bing-indexed profiles helps
- Bing places more weight on exact-match anchor text than Google

### Claude.ai
**What it prioritizes:** Long-form factual content, cited sources, structured knowledge
**Optimization:**
- Content needs external citations to reputable sources (Claude is trained to prefer cited claims)
- ClaudeBot must be explicitly allowed in robots.txt (check — many CMSs block unknown bots)
- @graph schema with linked entity types helps Claude identify entity relationships
- Technical accuracy > emotional/persuasion language
- First-party research, case studies with data, and expert quotes are highest-value signals

---

## GEO CONTENT CHECKLIST (Pre-Publish)

```
LAYER 1 — Access:
[ ] robots.txt allows all major AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended)
[ ] /llms.txt present and updated
[ ] All critical content in raw HTML source (not JS-injected)

LAYER 2 — Structure:
[ ] Primary answer in first 150 words
[ ] Each H3 section: 134-167 words, self-contained, opens with direct answer
[ ] Headings formatted as natural-language questions where appropriate
[ ] At least 1 named expert quote with attribution per major H2
[ ] At least 1 statistic with source + year per major H2

LAYER 3 — Freshness + Authority:
[ ] Content published or updated within 3 months
[ ] datePublished and dateModified in Article schema match actual dates
[ ] 15+ named entities across article
[ ] sameAs schema links on Organization pointing to all official profiles
[ ] Author schema with credentials + external profile links

LAYER 4 — Platform signals:
[ ] Reddit: active presence on relevant subreddits
[ ] GBP: complete, verified, recent posts (if local business)
[ ] Wikipedia/Wikidata: entity page exists and is accurate (if eligible)
```

---

## MONTHLY GEO REPORT

Include in monthly client report:

```
## AI / GEO Visibility — [Month]

Platform SoV:
  Google AI Overviews:  X% of tracked queries (±Y% vs last month)
  ChatGPT:              X% (±Y%)
  Perplexity:           X% (±Y%)

Top AI-cited pages: [list 3 with citation platform]
Competitor gaps: [where competitors appear, we don't]
Actions taken: [llms.txt updated / fresh content / schema fix]
Next month focus: [specific improvement target]
```

Source: `ai_visibility` MCP tool + manual sample check via `page-agent`.
