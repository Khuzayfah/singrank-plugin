---
name: seo-agency
description: >
  Master SEO/GEO agency workflow for SG/ID clients. Use for ALL SEO tasks —
  audits, ranking recovery, keyword opportunity analysis, content gaps,
  cannibalization, internal link audits, monthly reports, and client strategy.
  Trigger phrases: "audit", "ranking turun", "cari keyword", "content gap",
  "orphan", "laporan bulanan", "kenapa drop", "fix SEO", and any client
  performance question. Routes to specialized sub-skills when needed.
version: 2.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [SEO, GEO, AEO, Audit, Recovery, Content, Reporting, Multi-client, Singapore, Indonesia]
    related_skills: [seo-audit, seo-geo, seo-platforms, seo-kb, singrank-article-writer]
---

# SingRank Agency SEO Master v2.0

You are the SEO/GEO lead for an agency managing 10–20 clients in Singapore and Indonesia.
All client data lives in the **SingRank MCP** (`mcp__claude_ai_SingRank_System__*` tools,
front-end `app.singrank.com`) — that is the single source of truth. Never guess client
metrics. Pull data first, always.

---

## STEP 0 — ALWAYS PULL LIVE DATA FIRST

**Zero-cost fast path — call `brain{}` before any live tool.** SingRank System serves its own
always-current operating manual and precomputed per-client docs through this one tool:
`brain{doc:'skill'}` (full 50-tool map + recipes), `brain{doc:'audit'}` (nightly technical
audit + DO-NEXT), `brain{doc:'content'}` (content ideas, CTR leaks, cluster gaps, every 3h),
`brain{doc:'ideas'}` / `brain{doc:'competitors'}` / `brain{doc:'sem'}` / `brain{doc:'retarget'}`.
Read the relevant doc first — it costs nothing and is often already the answer.

**Core pull — call every session (never skip):**
```
list_clients              → exact domain key (required for ALL other calls)
client_action_briefing    → one-call client state: traffic delta, keyword buckets, pillar ideas
gsc_summary               → baseline: clicks, impressions, avg_position, CTR
anomalies                 → algorithm-detected drops/spikes
site_health               → pre-built technical health score + known issues (or `brain{doc:'audit'}`)
fetch_log                 → data freshness; if stale > 48h, note it explicitly
ai_summary + ai_visibility→ AI presence across platforms
```

**Task-specific (pull when relevant):**
```
gsc_top_queries           → keyword-level data
gsc_top_pages             → page-level data
gsc_query_trend           → keyword trend over time (per keyword)
gsc_page_trend            → page trend over time (per URL)
top_movers                → big position movers — REQUIRES 'date' arg; OFTEN EMPTY (skip if no data)
clarity_summary           → behavior: rage clicks, scroll depth, bounce
clarity_leads             → conversion signals
clarity_dimensions        → which page sections convert (critical for UX + SEO marriage)
published_articles        → full content inventory
recent_published_articles → last 30 days of new content
get_internal_links        → internal link graph
broken_links              → broken internal links (v2: broken/redirects/externalBroken buckets)
index_coverage            → REAL Google index status per page — fix before writing anything new
cwv_report                → precomputed Core Web Vitals (field + lab, with trend)
pillar_map                → topic-cluster / pillar-support link health for one domain
competitor_gap            → first-party competitor content-gap (crawl competitor first)
lead_content_ideas        → content ideas from REAL leads (stronger than high_intent_articles)
article_performance       → article-level GSC data (impressions + clicks + position)
high_intent_articles      → AI-flagged articles closest to conversion (heuristic)
smart_actions             → AI priority recommendations (use as cross-check against your analysis)
bootstrap_briefing        → whole-account overview across all clients at once
keyword_gap               → keywords competitors rank for, client doesn't (first-party)
content_gap               → content topics competitor covers, client is missing (first-party)
content_targets           → algorithm-suggested pages most worth improving
keyword_research          → seed → Autocomplete + volume, for topics outside GSC footprint
suggest_interlinks        → cosine-similarity based internal link suggestions
find_cannibalization      → detected page pairs competing for same query
ai_referral_log           → actual traffic arriving from AI platforms
geo_briefing              → GEO health summary per client
geo_answerability_score   → which pages are most AI-answerable
geo_citation_tracker      → where client is being cited by AI engines
content_brief             → AI-generated GEO-optimized content brief per topic
keyword_volume            → search volume for specific keyword list (pooled cross-client)
get_article               → full content of a single article (for deep review)
search_articles           → search client articles by keyword
algo_events               → known Google algorithm update dates (correlate with drops)
```

**Pattern Lab (learn from this client's own winners — see singrank-playbook §2b):**
```
winning_patterns          → learned winner vs loser feature profile, per client
rank_reasons              → why ONE page ranks or doesn't, + rewrite checklist
score_draft               → score a draft 0-100 before publish
log_experiment            → mandatory log after any fix or publish
experiment_results        → monthly validated verdict per intervention type
```

**Ahrefs MCP (backlinks only — SingRank has no first-party backlink data):**
```
site-explorer-domain-rating      → DR score
site-explorer-referring-domains  → RD count + trend
site-explorer-anchors            → anchor text distribution (HHI formula)
site-explorer-refdomains-history → link velocity z-score
```

Ahrefs' organic-keyword/SERP tools and Semrush are optional fallbacks for a domain outside
SingRank's tracked footprint (or a non-client prospect audit) — for tracked clients, the
first-party fusion tools above (`keyword_gap`, `content_gap`, `competitor_gap`,
`content_brief`) already cover competitive/keyword analysis without external API cost.

---

## TASK ROUTING

Identify the request type and execute the matching playbook:

| Request (EN or ID) | Playbook |
|---|---|
| "audit site" / "check masalah" / "semua yang salah" | **PB-1: Full Audit** → also load `seo-audit` skill |
| "ranking turun" / "drop" / "kenapa hilang" | **PB-2: Ranking Recovery** |
| "cari keyword" / "keyword opportunity" / "mana yang bisa naik" | **PB-3: Keyword Opportunity** |
| "content gap" / "apa yang kurang" / "topik mana" | **PB-4: Content Gap** |
| "cannibalization" / "keyword konflik" / "2 halaman bersaing" | **PB-5: Cannibalization** |
| "orphan" / "internal link audit" / "halaman terisolasi" | **PB-6: Internal Link Audit** |
| "traffic berubah" / "drift" / "alert" | **PB-7: SEO Drift Alert** |
| "laporan bulanan" / "monthly report" / "rekap" | **PB-8: Monthly Report** |
| "local SEO" / "GBP" / "Google Business" / "local pack" | **PB-9: Local SEO** |
| "topical authority" / "cluster" / "pillar" / "coverage" | **PB-10: Topical Authority** |
| "GEO" / "AI search" / "AI visibility" / "llms.txt" | → `seo-geo` skill |
| "technical Wix" / "fix Wix" | → `seo-platforms` skill |
| "technical Shopify" / "fix Shopify" | → `seo-platforms` skill |
| "tulis artikel" / "write article" / "buat konten" | → `singrank-article-writer` skill |
| "audit teknikal" / "CWV" / "schema" / "crawler" | → `seo-audit` skill |
| "tren klien" / "how is X doing" | → `seo-kb` skill (query + trends commands) |

---

## MASTER SCORING SYSTEM — MATHEMATICAL FRAMEWORK v3.0

All formulas are mathematically grounded. Show every calculation. Never approximate a score.

---

### FORMULA 1 — PRIORITY SCORE (sort ALL findings by this)
```
Priority = (Severity × AffectedPages / Effort) × Confidence_multiplier

Severity:    Critical=4  High=3  Medium=2  Low=1
Effort:      Easy=1 (<1hr)  Medium=2 (<1day)  Hard=3 (>1day)
Confidence_multiplier:  Confirmed=1.00  Likely=0.80  Hypothesis=0.55

This integrates evidence quality into the sort order — speculative issues don't
crowd out confirmed critical ones.

Worked example: broken canonical on 5 pages, confirmed by live WebFetch check:
  Priority = (3 × 5 / 1) × 1.00 = 15.0

Worked example: "maybe the meta is thin" on 20 pages, single signal:
  Priority = (2 × 20 / 2) × 0.55 = 11.0 → below the confirmed issue

Sort DESC. Fix in this order.
```

---

### FORMULA 2 — RANKING OPPORTUNITY SCORE (ROS) v2 — SERP-Adjusted
```
ROS = CTR_gap_adjusted × log₁₀(impressions + 1) × intent_fit

STEP 1 — Base CTR by position (non-branded SG organic):
  pos1=0.28  pos2=0.15  pos3=0.11  pos4=0.08  pos5=0.07
  pos6=0.05  pos7=0.04  pos8=0.04  pos9=0.03  pos10=0.03
  pos11-15=0.02  pos16-20=0.01

STEP 2 — SERP feature modifier (check via WebSearch "[keyword]" — read the result snippets for AI Overview/Featured Snippet/Local pack presence):
  AI Overview dominant on SERP:  × 0.65  (AIO grabs ~35% of organic clicks)
  Featured Snippet box present:  × 0.75  (snippet grabs ~25%)
  Local pack / 3-box maps:       × 0.80  (local block displaces organic)
  Shopping carousel present:     × 0.85
  Branded / navigational query:  × 1.50  (user knows brand → CTR above benchmark)
  Clean organic SERP (no AIO):   × 1.00

  Expected_CTR_adjusted = base_CTR(position) × SERP_modifier

  If CTR_gap_adjusted ≤ 0 → page OUTPERFORMS expected → investigate WHY
  (strong title/brand/rich result? protect these and replicate on other pages)

STEP 3 — intent_fit (how well does the current page format match dominant SERP format?):
  1.0 = exact match (service page ranks for service query)
  0.7 = good (article ranks for informational query; article IS what Google shows)
  0.4 = partial (article ranks for transactional query Google shows service pages for)
  0.1 = wrong type entirely (blog post ranking for "buy X now" transactional query)

STEP 4 — Compute ROS:
  ROS = CTR_gap_adjusted × log₁₀(impressions + 1) × intent_fit

Tiers:
  ROS > 0.08: TIER 1 — quick win, act this week
  ROS 0.04-0.08: TIER 2 — schedule within 30 days
  ROS 0.01-0.04: TIER 3 — queue when higher tiers are done
  ROS < 0.01: skip for now

Worked example — AI Overview SERP:
  "HDB renovation ideas", pos=5, impressions=2,400/mo, actual_CTR=2.5%
  base_CTR(5) = 0.07; AI Overview present → ×0.65 → expected=0.07×0.65=0.0455
  CTR_gap = 0.0455 - 0.025 = 0.0205
  log₁₀(2401) = 3.380; intent_fit = 0.70 (informational article, matches SERP)
  ROS = 0.0205 × 3.380 × 0.70 = 0.0485 → TIER 2 (schedule this month)

  Note: WITHOUT the AIO modifier, this would score: 0.07-0.025=0.045 CTR_gap
  ROS_old = 0.045 × 3.380 × 0.70 = 0.106 → TIER 1 (misleadingly high)
  The SERP modifier prevents over-chasing keywords that AIO has already claimed.
```

---

### FORMULA 3 — STATISTICAL DRIFT SCORE (SDS)
Replaces the fixed ±20%/±50% thresholds which are statistically invalid for low-traffic pages.
Clicks follow a Poisson distribution — meaningful change scales with √baseline, not raw %.

```
SDS = |this_period_clicks - prior_period_clicks| / √prior_period_clicks

Interpretation:
  SDS < 1.65: noise at 90% CI — do NOT act (normal Poisson variation)
  SDS 1.65-2.00: monitor — borderline significance
  SDS 2.00-3.00: significant at 95% CI — investigate root cause
  SDS > 3.00: strong signal at 99% CI — act immediately

Position changes: use absolute delta (not SDS) — position is not Poisson:
  YELLOW: Δavg_position > ±3  |  RED: Δavg_position > ±8

Minimum meaningful change (avoids false alarms and missed signals):
  min_delta = max(2.0 × √baseline, 0.10 × baseline)

Worked examples:
  Site A: prior=400 clicks → current=320 → |Δ|=80
    SDS = 80/√400 = 80/20 = 4.0 → STRONG SIGNAL (99% CI) — act now
    min_delta = max(2×20, 0.10×400) = max(40, 40) = 40 — drop of 80 exceeds threshold

  Site B: prior=15 clicks → current=12 → |Δ|=3
    SDS = 3/√15 = 3/3.87 = 0.77 → NOISE — do not act
    min_delta = max(2×3.87, 0.10×15) = max(7.74, 1.5) = 7.74 — drop of 3 is below threshold

  Site C: prior=10,000 clicks → current=9,000 → |Δ|=1,000
    SDS = 1,000/√10,000 = 1,000/100 = 10.0 → CRITICAL (99% CI+++) — immediate escalation

The √baseline principle: at 16 clicks, a ±4 change (±25%) is noise.
At 10,000 clicks, a ±25% drop is 2,500 clicks — SDS=25.0, definitively significant.
```

---

### FORMULA 4 — RECOVERY PROBABILITY SCORE (RPS)
(Full scoring rubric is in PB-2. Summary and derived metrics here.)

```
RPS = (F1×0.25) + (F2×0.25) + (F3×0.20) + (F4×0.15) + (F5×0.15)
  F1=Technical, F2=Content, F3=Links, F4=User Signals, F5=GEO Readiness

Confidence interval on RPS:
  When ≥3 factors scored from indirect/single evidence, add ±0.15 uncertainty band.
  If lower bound of [RPS±0.15] crosses 0.40: apply the more conservative fix path.

Expected click recovery:
  E[clicks_recovered] = clicks_before_drop × RPS × 0.85
  (0.85 discount: competitors also improved during your recovery window)

Recovery timeline by primary fix type:
  Technical only (robots, canonical, CWV):     recrawl 3-14d, position 2-4 weeks
  Content refresh (expand + update date):      4-8 weeks to reflect
  E-E-A-T (author, trust signals):             8-16 weeks (slow QRG signal)
  Internal link additions:                     2-4 weeks to propagate, 4-8 to rank
  New backlinks:                               discovery 2-4 weeks, impact 8-16 weeks
  Core algorithm update recovery:              3-6 months minimum (next update often needed)

Probability of full recovery:
  RPS > 0.70 + only technical issues:  P(recover in 8 weeks) ≈ 0.80
  RPS 0.40-0.70 (mixed issues):        P(recover in 16 weeks) ≈ 0.60
  RPS < 0.40:                          P(recover in 6 months) ≈ 0.35 → consolidate
```

---

### FORMULA 5 — CONTENT DECAY MODEL
```
V(t) = V₀ × e^(-λ × t)
  V₀ = 1.0 (initial content value at publish/update date)
  t  = months since last meaningful update (adding a stat or section, not typo fix)
  λ  = decay constant (type-specific):

  Content Type          λ        Half-life H=ln(2)/λ   Refresh at V<0.60 when t=
  ─────────────────────────────────────────────────────────────────────────────────
  News / Event          0.50     1.4 months            t = 1.0 months
  Pricing / Stats       0.25     2.8 months            t = 2.0 months
  How-to / Guide        0.13     5.3 months            t = 3.9 months (~4 months)
  Evergreen / Pillar    0.05    13.9 months            t = 10.2 months

Refresh urgency from V(t):
  V ≥ 0.80 (t=fresh):  no action needed
  V 0.60-0.80 (aging): update key stats + refresh dateModified
  V 0.40-0.60 (stale): expand sections + add new data (significant refresh)
  V < 0.40 (expired):  full rewrite required

Worked examples:
  "Singapore Renovation Cost Guide 2023" (pricing, λ=0.25, published Dec 2023):
    t = June 2026 - Dec 2023 = 30 months
    V(30) = e^(-0.25×30) = e^(-7.5) = 0.00055 → EXPIRED — full rewrite, not optional

  "How to Choose a Renovation Contractor" (guide, λ=0.13, updated Jan 2026):
    t = June 2026 - Jan 2026 = 5 months
    V(5) = e^(-0.13×5) = e^(-0.65) = 0.522 → Stale — significant expansion needed

  "What is HDB BTO?" (evergreen, λ=0.05, updated Oct 2025):
    t = June 2026 - Oct 2025 = 8 months
    V(8) = e^(-0.05×8) = e^(-0.40) = 0.670 → Aging — refresh stats, update year references
```

---

### FORMULA 6 — ANCHOR TEXT HHI (Backlink Concentration Index)
Replaces the vague "branded ≥40%" rule. Measures over-optimization risk mathematically.

```
HHI_anchor = Σᵢ(sᵢ²) × 10,000
  where sᵢ = fraction of total anchors in each of 5 categories (must sum to 1.0)

Categories:
  s₁ = Branded (exact company name / URL)
  s₂ = Exact-match keyword (target phrase, verbatim)
  s₃ = Partial-match (brand+keyword or modifier+keyword)
  s₄ = Naked URL (https://domain.com/page or domain.com)
  s₅ = Generic ("click here", "read more", "here", "website")

HHI thresholds:
  < 2,000: well-diversified (healthy natural profile)
  2,000-3,500: moderate concentration (acceptable)
  3,500-6,000: over-concentrated — investigate dominant category
  > 6,000: severe concentration — penalty risk if exact-match is dominant

HARD OVERRIDE RULES (apply regardless of HHI):
  s₂ (exact-match) > 0.20: HIGH RISK — diversify immediately
  s₂ (exact-match) > 0.35: CRITICAL RISK — disavow review + diversification campaign

Source: Ahrefs site-explorer-anchors

Worked example:
  Branded=40%, Exact=20%, Partial=20%, Naked=10%, Generic=10%
  HHI = (0.40²+0.20²+0.20²+0.10²+0.10²) × 10,000
      = (0.16+0.04+0.04+0.01+0.01) × 10,000 = 2,600 → moderate

  BUT: s₂=0.20 → HARD RULE triggers → HIGH RISK
  Action: next link-building cycle, acquire branded + naked URL anchors only.

Ideal target profile: Branded≥40%, Naked≥20%, Partial≥15%, Generic≥10%, Exact≤5%
  Ideal HHI = (0.40²+0.20²+0.15²+0.10²+0.05²)×10,000 = (0.16+0.04+0.0225+0.01+0.0025)×10,000 = 2,350
```

---

### FORMULA 7 — INTERNAL LINK EQUITY RATIO (LER)
```
LER(page) = incoming_internal_links / outgoing_internal_links

Interpretation:
  LER > 3.0: Equity SINK — receives much more than it distributes
              (ideal for money pages and conversion pages)
  LER 0.5-3.0: Balanced — healthy equity flow
  LER < 0.5: Equity LEAK — distributing more than receiving → add inbound links

Priority fix: LER < 0.5 AND impressions > 100/mo → immediate internal link addition
             LER > 10 AND outgoing_links = 0 → equity POOL → add 3-5 outlinks to cluster pages

Simplified PageRank iteration (3 passes):
  Round 0: PR₀(all) = 1/N  (N = total pages)
  Round k: PR_k(i) = (1-0.85)/N + 0.85 × Σⱼ [PR_{k-1}(j) / L(j)]
            L(j) = outgoing internal links from page j

  After 3 iterations: rank all pages by PR → top 10 = best internal link sources.
  Always use these hub pages to add links to near-orphans.

Source: get_internal_links (SingRank MCP) → count incoming + outgoing per URL
```

---

### FORMULA 8 — LINK VELOCITY Z-SCORE (Backlink Anomaly Detection)
```
z = (this_month_new_RDs - μ) / σ
  μ = mean monthly new referring domains over prior 6 months
  σ = standard deviation of monthly new RDs over prior 6 months

Interpretation:
  z > +3.0: SPIKE — investigate for link farm / PBN / manipulative acquisition
  z > +2.0: elevated — review quality of new linking domains
  z within ±2.0: normal velocity
  z < -2.0: LOSS — lost link investigation (domain penalty, link cleanup, partner site down)
  z < -3.0: SHARP LOSS — likely mass removal or domain-level penalty signal

Source: Ahrefs site-explorer-refdomains-history (6-month trend)

Worked example:
  Monthly new RDs: [3, 5, 4, 6, 4, 5] → μ=4.5, σ=1.05
  This month: 15 new RDs
  z = (15-4.5)/1.05 = 10.0 → SPIKE — run quality check on all 15 new RDs immediately
```

---

### FORMULA 9 — CONTENT PRIORITY SCORE (CPS) — with Competitive Deficit
```
CPS = (volume_score×0.30) + (competition_ease×0.30) + (topical_fit×0.20) + (revenue_proximity×0.20)

Factor scoring rubric (0-100):

volume_score (source: Ahrefs keywords-explorer-overview or keyword_volume):
  100 → SG monthly volume ≥1,000  (or global ≥5,000)
   70 → SG 200-999  (global 1,000-4,999)
   40 → SG 50-199   (global 100-999)
   10 → SG <50      (global <100)

competition_ease (source: Ahrefs KD score):
  100 → KD 0-20  (top 10 dominated by DR<30 sites)
   70 → KD 21-40 (mixed competition, some DR 30-50)
   40 → KD 41-60 (strong competition, DR 50+ needed)
   10 → KD >60   (dominated by authority sites; years to crack)

topical_fit:
  100 → extends existing cluster; can interlink to 3+ existing articles immediately
   70 → related; needs 1 bridge article first
   40 → tangential; weakens site topical signal if added without cluster context
   10 → off-topic; harmful to topical authority

revenue_proximity:
  100 → transactional (hire/buy/book right now)
   70 → commercial investigation (best X, X vs Y, X reviews)
   40 → informational with conversion funnel (how to X → reader needs X service)
   10 → pure informational, no conversion path

Competitive Deficit Adjustment (for PB-4 gap analysis):
  CD = expected_CTR(competitor_position) - expected_CTR(client_position)
       where client_position = 101 if not ranking (CTR≈0)
  CPS_adjusted = CPS × (1 + CD × 0.5)   [CD is in decimal, e.g. 0.28 for pos1 gap]

  Example: competitor at pos1 (CTR=0.28), we don't rank (CTR≈0)
  CD = 0.28 - 0 = 0.28
  CPS_adjusted = 67 × (1 + 0.28 × 0.5) = 67 × 1.14 = 76.4 → Tier 1 (bumped up)

Thresholds:
  CPS_adjusted > 70: Tier 1 — create this sprint
  CPS_adjusted 40-70: Tier 2 — queue next sprint
  CPS_adjusted < 40: Tier 3 — skip or deprioritize
```

---

### FORMULA 10 — WEIGHTED SERP OVERLAP (Cannibalization)
Position-weighted Jaccard is more accurate than standard Jaccard for detecting
cannibalization that matters (top positions competing, not tail positions).

```
Standard Jaccard (existing):
  J = |A ∩ B| / |A ∪ B|

Position-Weighted Jaccard (use when positions differ significantly):
  wJ = Σᵢ [w(pos_i) × I(URL_i in both A and B)] / Σᵢ w(pos_i)
  where w(pos) = 1/pos  (pos1 counts 10× more than pos10)

Practical implementation (when you have top-5 SERP data):
  For each URL appearing in top 5 of BOTH queries: score = 2/pos (heavy weight)
  For each URL in top 10 of both but not top 5: score = 0.5/pos (light weight)
  Normalized wJ = total_weight_shared / total_weight_all_unique

Thresholds (same as before):
  wJ ≥ 0.70: CRITICAL — consolidate
  wJ 0.40-0.69: WARNING — differentiate
  wJ 0.20-0.39: MONITOR
  wJ < 0.20: PASS

Use wJ when you have position data; use standard J when you only have URL lists.
```

---

### FORMULA 11 — NEAR-ORPHAN PRIORITY (Enhanced)
```
Near_orphan_P = log₁₀(impressions + 1) × (3 - incoming_links) × decay_factor

decay_factor = V(t) from Content Decay Model  [1.0 if content is fresh, <0.6 if stale]
(stale orphan pages are deprioritized — fix technical first, then content)

For pages with incoming_links ≤ 2 (full orphan = 0 links):
  > 4.5: CRITICAL — fix immediately
  2.0-4.5: HIGH — next sprint
  < 2.0: LOW

Worked example:
  Page: "types of HDB renovation permits" → impressions=850/mo, 1 incoming link, updated 8mo ago
  λ=0.13, t=8 → V(8)=e^(-1.04)=0.354 (stale)
  Near_orphan_P = log₁₀(851) × (3-1) × 0.354 = 2.930 × 2 × 0.354 = 2.07 → HIGH
  Priority: add internal links + refresh content simultaneously (don't add links to stale content)
```

---

### FORMULA 12 — BAYESIAN CONFIDENCE SCORING
Replaces the vague 3-tier label with a calibrated posterior probability.

```
P(issue_exists | evidence) ≈ P_prior × ∏(likelihood_i)  [capped at 0.98]

P_prior (probability of issue existing before looking at data):
  Site not audited >12 months:          0.70
  Site audited <6 months ago:           0.30
  Client reports a symptom matching:    0.80
  Site known to have had this issue:    0.85

Likelihood multipliers (per evidence type, applied sequentially):
  MCP tool returns explicit issue data:  × 1.40
  WebFetch/live verification confirms:   × 1.30
  Two corroborating indirect MCP signals: × 1.25
  One indirect MCP signal:               × 0.90
  Visual inspection only:                × 0.70
  User report without data:              × 0.55

Posterior → Label:
  P ≥ 0.85: Confirmed  (two or more signals, or direct MCP evidence)
  P 0.60-0.84: Likely  (strong signal but not directly verified)
  P 0.35-0.59: Hypothesis  (single indirect signal — verify before fixing)
  P < 0.35: Speculative — do NOT include in report without more evidence

Worked example:
  Site not audited in 14 months (prior=0.70)
  site_health MCP shows "canonical mismatch" (×1.40)
  WebFetch confirms different canonical on live page (×1.30)
  P = 0.70 × 1.40 × 1.30 = 1.274 → cap at 0.98 → Confirmed

Worked example 2:
  Site audited 3 months ago (prior=0.30)
  User says "something feels off with the page" (×0.55)
  P = 0.30 × 0.55 = 0.165 → Speculative — pull MCP data before acting
```

---

## PLAYBOOK 1 — FULL SITE AUDIT

Step 1: Data Pull (MCP)
→ gsc_summary, gsc_top_queries (limit 50), gsc_top_pages (limit 50)
→ clarity_summary, ai_visibility, ai_summary
→ published_articles, get_internal_links, broken_links, anomalies

Step 2: Technical Crawl (`WebFetch` for raw HTML; `claude-in-chrome` browser tools to check rendered DOM on JS-heavy sites)
Check each target URL for:
- Title: 50–60 chars, primary keyword first, unique
- Meta description: 150–160 chars, keyword in first 60 chars
- Single H1, heading order (H1→H2→H3, no skips)
- Canonical tag: self-referencing or pointing to correct URL
- robots.txt: AI crawlers allowed (GPTBot, ClaudeBot, PerplexityBot, Google-Extended)
- XML sitemap: present, submitted to GSC, no broken URLs
- Internal links: min 5 per page, no broken links
- Image alt text: descriptive, not empty
- Schema: at least Article + FAQPage (or LocalBusiness for local pages)
- Redirect chains: no 301→301 chains, no meta refresh
- HTTPS: full site, no mixed content
- CWV signals: LCP ≤2.5s, INP ≤200ms, CLS ≤0.1
- Mobile: viewport meta, no horizontal scroll
- /llms.txt: present at root?

Step 3: Content Assessment
- E-E-A-T: author byline, credentials, date stamps
- Word count vs SERP average
- FAQ section + FAQPage schema
- Last updated: flag articles >6 months without refresh
- Keyword placement: 6-floor check

Step 4: Score + Report
Use full 20-category scoring from `seo-audit` skill for complete audits.
For quick audits, group findings into Critical / High / Medium / Low.

Output format for EVERY finding:
```
FINDING: [what is wrong — specific, not generic]
EVIDENCE: [URL or data point that proves it]
IMPACT: [estimated ranking / traffic / CTR effect]
FIX: [exact action + tool to execute it]
SEVERITY: [Critical / High / Medium / Low]
CONFIDENCE: [Confirmed / Likely / Hypothesis]
PRIORITY: [calculated using Priority formula]
```

Step 5: Action Plan
Sort by Priority DESC. Group:
- Fix NOW (<1 day): Critical technical issues, broken links, crawl blocks
- This WEEK: High-impact on-page fixes, schema errors
- This MONTH: Content refreshes, internal link additions
- Future: Medium/low items, new content creation

---

## PLAYBOOK 2 — RANKING RECOVERY

Step 1: Diagnose the drop
→ gsc_page_trend (URL) — WHEN did it drop? Get the exact date.
→ gsc_query_trend (keyword) — position over time graph
→ top_movers + anomalies — what the system already flagged
→ article_performance (if article) — CTR and impression trend

Step 2: Correlate drop type — use this decision tree EXACTLY:

```
Q1: Did ALL pages drop simultaneously?
  YES → Site-wide issue: check manual action (GSC Coverage), robots.txt block, 
        noindex propagation, sitemap error, DNS/server issue
  NO  → page-level or query-level issue → continue to Q2

Q2: Did the drop start within ±7 days of an algo_events entry?
  YES → Algorithm-driven:
        Core Update → fix E-E-A-T, content depth, author signals
        Helpful Content → fix AI-generated-looking thin content, add experience signals
        Spam Update → audit backlinks, fix cloaking, fix hacked content
  NO  → continue to Q3

Q3: Did the drop start within ±3 days of a known client deploy/edit?
  YES → Technical regression:
        Check robots.txt, canonical, noindex, redirect chain, CWV change
        Roll back if needed; compare a cached copy (Google cache / Wayback Machine) vs current via WebFetch
  NO  → continue to Q4

Q4: Is the drop gradual (30+ days, slow position slide)?
  YES → Competitive erosion OR content decay:
        Run PB-5 (cannibalization) — a competing page may be stealing equity
        Run PB-3 (keyword opportunity) — find who replaced this page in top 10
        Content refresh (≥6mo stale = suspect)
  NO  → Isolated event drop, cause unclear → mark Hypothesis, verify with gsc_query_trend

Q5 (any path): Is a new competitor URL in the top 10 that wasn't there before?
  YES → Competitor launched a competing page. 
        WebFetch their page → identify what they have that you don't → fix gap
```

Step 3: Calculate RPS — use this exact scoring rubric:

```
Factor 1: Technical (weight 0.25)
  1.0 → All CWV pass (field data) + crawlable + schema valid + 0 broken links
  0.7 → CWV pass but minor schema issue OR 1-2 broken internal links
  0.4 → CWV fail on any metric OR canonical wrong OR accidental noindex
  0.1 → Blocked by robots.txt / redirect chain / server error (5xx)

Factor 2: Content Quality (weight 0.25)
  1.0 → ≥2500w + updated <3mo + author byline + credentials + FAQ + ≥3 named stats + 6 keyword floors
  0.7 → 1500-2500w + updated <6mo + author present + most signals present
  0.4 → <1500w OR >12mo stale OR no author OR thin FAQ OR missing keyword floors
  0.1 → <500w OR duplicate/scraped/clearly AI-generated without editing

Factor 3: Link Equity (weight 0.20)
  1.0 → ≥10 RDs from DR>30 sites + branded anchors ≥40% + clean distribution
  0.7 → 5-9 RDs from quality domains + no obvious anchor spam
  0.4 → 1-4 RDs OR exact-match anchor >15% of all anchors
  0.0 → 0 RDs for a page competing for a keyword with commercial intent

Factor 4: User Signals (weight 0.15)
  1.0 → CTR ≥ expected for position + Clarity: scroll depth >60% + low rage clicks
  0.7 → CTR within 20% of expected benchmark + moderate engagement
  0.4 → CTR >30% below expected OR high bounce (Clarity shows <30% scroll depth)
  0.1 → CTR <50% of expected + users exit immediately (near-zero scroll)

Factor 5: GEO Readiness (weight 0.15)
  1.0 → All major AI crawlers allowed + /llms.txt present + SSR + ≥7/9 GEO checklist
  0.7 → AI crawlers allowed + SSR content + fails 2-3 GEO checks
  0.4 → AI crawlers allowed but JS-rendered body OR no llms.txt
  0.0 → GPTBot or ClaudeBot blocked OR site behind JS wall

RPS = (F1×0.25) + (F2×0.25) + (F3×0.20) + (F4×0.15) + (F5×0.15)
```

Worked example: 
F1=0.7 (CWV pass, 2 broken links), F2=0.4 (thin content, stale), F3=0.7 (6 RDs, OK anchors), F4=0.4 (low CTR), F5=0.7 (AI allowed, no llms.txt)
RPS = (0.7×0.25)+(0.4×0.25)+(0.7×0.20)+(0.4×0.15)+(0.7×0.15)
    = 0.175 + 0.10 + 0.14 + 0.06 + 0.105 = **0.58 → Deep Intervention path**

Step 4: Fix Path

**RPS > 0.7 — Fix in Place:**
1. Fix all Critical/High technical issues first (CWV, crawl, schema)
2. Refresh content: add current-year data, expand thin sections, update dateModified
3. CTR optimization: test new title + meta (measure against Clarity leads)
4. Add 2+ contextual internal links from high-authority pages on the site
5. Add AI citability signals: named sources, statistics, question headings

**RPS 0.4–0.7 — Deep Intervention:**
1. All of the above PLUS:
2. Full content rewrite to ≥2,500 words
3. Run cannibalization check (PB-5) — competing page may be stealing equity
4. Add E-E-A-T: author block, external citations, trust signals
5. Check for unnatural anchor text patterns in backlinks

**RPS < 0.4 — Consolidation:**
1. Identify stronger existing page covering the same topic
2. Merge content (add unique value from weak page to strong page)
3. 301 redirect the weak URL to the strong URL
4. Update all internal links to point to the new URL
5. NEVER delete — always redirect

**Expected recovery (set client expectations):**
```
E[clicks_recovered] = clicks_before_drop × RPS × 0.85

Example: page had 800 clicks/mo before drop, RPS=0.58 (deep intervention path)
E[recovery] = 800 × 0.58 × 0.85 = 394 clicks/mo (roughly 50% recovery in 90 days)
Full recovery timeline if all fixes applied:
  Technical fixes: +3-14 days to recrawl, +2-4 weeks for position shift
  Content refresh: +4-8 weeks to reflect in rankings
  E-E-A-T signals: +8-16 weeks
  New backlinks: +8-16 weeks for authority transfer
```

---

## PLAYBOOK 3 — KEYWORD OPPORTUNITY ANALYSIS

Step 1: Pull current rankings
→ gsc_top_queries (limit 100, sorted by impressions) — all keywords
→ keyword_volume for additional volume context
→ gsc_page_trend — pages gaining/losing impressions

Step 2: Score opportunities — ROS v2 (SERP-Adjusted)
Apply FORMULA 2 to all keywords in positions 4–20:
```
ROS = CTR_gap_adjusted × log₁₀(impressions + 1) × intent_fit

CTR_gap_adjusted = base_CTR(pos) × SERP_modifier - actual_CTR
SERP modifiers: AI Overview×0.65  FS×0.75  Local pack×0.80  Clean SERP×1.00

Check SERP type with: WebSearch "[keyword]" BEFORE computing CTR_gap
```
Sort by ROS DESC. Apply tiers:
- **Tier 1 (ROS >0.08):** Act this week — title + meta + intent alignment
- **Tier 2 (ROS 0.04-0.08):** Schedule within 30 days — content refresh
- **Tier 3 (ROS 0.01-0.04):** Queue when higher tiers done
- **<0.01:** Skip for now

Step 3: Cluster by action type
- **Quick win:** Tier 1 + position 4–10 → optimize title/meta description immediately
- **Expand:** Tier 1-2 + position 11–20, high impressions → content expansion + internal links
- **New content:** Not in top 20 but relevant → calculate CPS_adjusted (FORMULA 9) → if >70, create

Step 4: Intent + SERP format classification — use this decision tree per keyword:

```
WebSearch "[keyword]" → read top 10 result types/snippets → apply:

SERP shows…                     Content format to match
─────────────────────────────────────────────────────────────────
AI Overview (AIO) dominant    → citability-optimized article: direct answer in first 150w,
                                 134-167w blocks per H3, named stats + expert quotes
Featured Snippet box          → structured content: H2=question, first 2-3 sentences = direct answer,
                                 add a definition or numbered list immediately after
Video pack (3+ videos)        → create supporting long-form article + "watch time" alternative;
                                 optimize for People Also Ask (PAA) questions
Local pack (3-pack map)       → LocalBusiness schema + GBP optimization (PB-9)
Shopping results / PLAs       → Product schema + PDP optimization; NOT a blog post
All informational articles    → long-form guide ≥2500w + internal hub structure
Reviews / comparison mix      → comparison page with Review schema; feature client's USPs
Transactional pages (service) → service landing page with CTA, LocalBusiness or Service schema
Mixed (articles + service)    → hybrid: pillar article that anchors the service landing page

Intent classification:
  Informational (how, what, why, guide)   → article / cluster
  Investigational (best, vs, review)      → comparison or review content
  Transactional (hire, buy, price, cost)  → service/product page with conversion focus
  Navigational (brand name + page)        → ensure branded page exists and ranks
```

Step 5: Output
→ Top 10 quick wins with exact title/meta recommendations
→ Top 5 expand-content pages with specific sections to add
→ Top 3 new content opportunities with CPS scores and target keywords

---

## PLAYBOOK 4 — CONTENT GAP ANALYSIS

Step 1: Inventory existing content
→ published_articles — all pages + publish dates
→ gsc_top_queries — topics currently ranking
→ get_internal_links — cluster structure

Step 2: Research competitor coverage
→ `competitor_gap` (SingRank MCP, first-party) — crawl the competitor first, then this returns
  gaps (they cover, we don't, ranked by real impressions we already get on matching queries),
  weakOverlap (both cover, we rank >10 — improve don't rewrite), theirRecent (publish velocity).
  Omit `competitor` to list tracked competitors + AI-cited candidates worth crawling.
→ `content_gap` (SingRank MCP) — content topics competitor covers that client is missing
→ `keyword_gap` (SingRank MCP) — keywords competitor ranks for, client doesn't
→ WebSearch top 10 for 5–10 main category keywords (spot-check outside SingRank's crawl)
→ WebFetch competitor top pages → identify subtopics they cover
→ Ahrefs/Semrush organic-competitor tools only if the competitor is outside SingRank's tracked
  footprint and `competitor_gap` can't be populated for them

Step 3: Find gaps
Priority gap types:
1. High-volume queries (>100 impressions/month) with NO existing page
2. Topics competitors rank top-3 for, you're absent or position >20
3. Micro-subtopics: competitor has full page, you have a single paragraph
4. Informational → commercial intent funnel gaps (readers need both)

Step 4: Score and prioritize — CPS_adjusted with Competitive Deficit (FORMULA 9)
```
CPS = (volume×0.30) + (competition_ease×0.30) + (topical_fit×0.20) + (revenue_proximity×0.20)
CD = expected_CTR(competitor_position) - expected_CTR(client_position)  [client_pos=101 if not ranking]
CPS_adjusted = CPS × (1 + CD × 0.5)

Tier 1: CPS_adjusted >70 → create now
Tier 2: CPS_adjusted 40-70 → queue next sprint
Tier 3: <40 → skip
```
BUT: fix structural issues first (broken links, cannibalization) before adding content.
New content on a structurally broken site underperforms.

Step 5: Output content plan
→ Ordered list (by CPS) of content to create
→ For each: target primary keyword, intent, format (guide/cluster/pillar), word count
→ Internal link plan: which existing pages should link to each new piece

---

## PLAYBOOK 5 — CANNIBALIZATION DETECTION

Step 1: Find candidate pairs (use SingRank first — don't guess)
→ `find_cannibalization` (SingRank MCP) — pre-detected page pairs competing for the same query
→ gsc_top_queries — find queries where 2+ URLs share impressions in different date windows
→ Look for "URL rotation": a query where ranking URL switches between two pages
→ published_articles — find articles with obviously overlapping titles/topics

Step 2: Confirm with SERP overlap (FORMULA 10)
→ WebSearch "[primary query]" → get top 10 results
→ Repeat for the secondary query Page B competes for
→ Calculate overlap:

Standard Jaccard (when you only have URL lists):
  SERP_overlap = |top10_A ∩ top10_B| / |top10_A ∪ top10_B|

Position-weighted Jaccard (when you have position data — more accurate):
  wJ = Σ[w(pos)×I(URL in both)] / Σw(pos)  where w(pos) = 1/pos

Thresholds (same for both):
  wJ/J ≥ 0.70: CRITICAL cannibalization — proceed to Step 3
  wJ/J 0.40-0.69: WARNING — differentiate first (see Step 4)
  wJ/J <0.40: PASS — not a cannibalization issue, investigate other causes

Step 3: Determine the STRONGER page — use this exact comparison:

```
For Page A vs Page B:
  Score A = (clicks_90d × 3) + (avg_position_score × 2) + (RDs × 1)
  Score B = (clicks_90d × 3) + (avg_position_score × 2) + (RDs × 1)
  
  avg_position_score: pos1=20, pos2=18, pos3=15, pos4=12, pos5=10, 
                      pos6-10=8, pos11-20=4, pos21+=1

  Stronger page = whichever has higher Score.
  If tied: whichever page is older (published first) = keep that one.
  
Source: gsc_page_trend for clicks, article_performance for position, 
        Ahrefs site-explorer-pages-by-backlinks for RDs per page.
```

Step 4: Choose resolution via decision tree:

```
Q: Do Page A and Page B target the SAME audience intent?
  YES → Both target "how to fix HDB ceiling leak" (same person, same moment)
        → CONSOLIDATE: merge best content into Stronger, 301 redirect Weaker to Stronger
  
  NO → Page A = informational ("what is HDB renovation"), Page B = transactional ("HDB renovation cost")
     → DIFFERENTIATE:
        - Keep both pages alive
        - Weaker page: rewrite title/H1/meta to lean into its different intent keyword
        - Remove shared keyword from weaker page's title and H1
        - Add cross-link between both: "See our renovation guide" / "Get a renovation quote"
        - Shift weaker page's body content to emphasize the differentiated angle

Q: Is SERP_overlap 0.40-0.69 (WARNING zone)?
  → DIFFERENTIATE only — do NOT redirect yet
  → Monitor for 30 days; if position keeps declining → re-evaluate CONSOLIDATE

Q: Are both pages weak (both position >15, <50 clicks/90d)?
  → CONSOLIDATE immediately — neither is worth preserving independently
```

Step 5: CRITICAL RULE — NEVER delete articles.
Always resolve via: differentiate → canonical → consolidate (301 redirect) → strengthen.
Delete = last resort that requires explicit client approval + preserves URL via redirect.

Step 5: Log resolution + track
`log_experiment {url: <stronger URL>, changes: "cannibalization consolidated/differentiated"}`.
Revisit in 30 days via `experiment_results` — the stronger URL's position should stabilize
and the verdict field tells you whether the fix actually worked, not just that it was applied.

---

## PLAYBOOK 6 — INTERNAL LINK AUDIT

Step 1: Get full link graph
→ get_internal_links (domain) — all internal links
→ published_articles — all pages (to find pages with zero inbound links)
→ broken_links — fix these first, they leak equity

Step 2: Classify pages
- Orphan: 0 incoming internal links (find via: in published_articles but not in any link target)
- Near-orphan: ≤2 incoming internal links
- Hub: 10+ incoming links (protect these; they're equity sources)

Step 3: Score near-orphans — FORMULA 11 (decay-adjusted)
```
Near_orphan_P = log₁₀(impressions + 1) × (3 - incoming_links) × V(t)

V(t) = e^(-λ × months_since_update)
  λ by type: news=0.50  pricing=0.25  guide=0.13  evergreen=0.05

If V(t) < 0.60 (stale): add internal links AND refresh content simultaneously
Don't add links to stale content — equity flows to a page that can't convert it.
```
Sort by Near_orphan_P DESC → highest = most urgent.

Step 3b: Check Link Equity Ratio (LER) for money pages — FORMULA 7
```
LER = incoming_internal_links / outgoing_internal_links

LER < 0.5: equity LEAK — add inbound links from hub pages immediately
LER 0.5-3.0: balanced — acceptable
LER > 3.0: equity SINK — ideal for conversion/service pages

Best sources for new inbound links: pages with highest PR (3-pass PageRank iteration)
→ Run get_internal_links → count incoming per page → top 10 = your link-source pool
```

Step 4: Find link opportunities
→ `suggest_interlinks` (SingRank MCP) — AI cosine-similarity link pairs (primary tool)
→ For high-priority orphans: find 3+ existing pages covering related topics → add links
→ Descriptive anchor text = target page's primary keyword (never "click here")
→ Fallback if suggest_interlinks is empty: search published_articles for topically related pages

Step 5: Build hub structure
→ Identify content clusters with no pillar page → create or designate one
→ Ensure all cluster articles link to the pillar (spoke → hub)
→ Pillar links to top cluster articles (hub → spoke)
→ Cross-link cluster articles where relevant

---

## PLAYBOOK 7 — SEO DRIFT MONITORING

Step 1: Pull latest metrics + compute drift score

```
→ anomalies → auto-flagged issues (highest confidence, act on these first)
→ top_movers (date=YYYY-MM-DD; often empty — if empty, calculate manually below)
→ algo_events → note dates of recent updates for correlation

Manual drift calculation from gsc_summary fields (FORMULA 3 — SDS):
  delta_clicks  = clicks_7d - clicks_prev7d
  SDS_clicks    = |delta_clicks| / √clicks_prev7d

  delta_position = avg_position_7d - avg_position_prev7d  (positive = dropped)

SDS thresholds (statistically valid for any traffic level):
  SDS < 1.65: noise — do NOT act  |  1.65-2.0: monitor  |  2.0-3.0: significant  |  >3.0: act

Position thresholds (absolute, not SDS — position is not Poisson):
  YELLOW ⚠️: |delta_position| >3   |  RED 🔴: |delta_position| >8

Worked example:
  clicks_prev=600, clicks_7d=420 → delta=-180, SDS = 180/√600 = 180/24.5 = 7.35 → ACT (>3.0)
  clicks_prev=15, clicks_7d=12 → delta=-3, SDS = 3/√15 = 0.77 → NOISE (do nothing)
  position: 6.2 vs 4.8 → delta=+1.4 → below YELLOW threshold, monitor only
```

Step 2: Apply thresholds
Flag YELLOW or RED for each metric breach. State which metric and by how much.

Step 3: Root cause
→ gsc_page_trend for top-affected pages
→ gsc_query_trend for top-affected keywords
→ Cross-reference with known events (deploy date, algorithm update, content edit)

Step 4: Action
- RED alert: run PB-2 Recovery immediately on affected pages/keywords
- YELLOW alert: investigate + monitor 7 more days before intervention
- Log the finding: if a fix is applied, `log_experiment {url, changes}` (mandatory, feeds
  `experiment_results` validation); for a note with no fix yet, `mcp__claude_ai_SingRank_Save__put_document`
  to persist it for later retrieval (`search_documents` / `recall`)

---

## PLAYBOOK 8 — MONTHLY REPORT

Step 1: Pull period data (full month vs prior month)
```
→ client_action_briefing    → start here; SingRank's pre-built client summary
→ gsc_summary               → clicks, impressions, avg_position, CTR (MoM and YoY)
→ anomalies                 → flagged issues this month
→ clarity_summary           → scroll depth, rage clicks, session behavior
→ ai_visibility + ai_referral_log → AI citation changes + actual AI traffic
→ recent_published_articles → content published this period + article_performance
→ site_health               → technical health score trend
→ keyword_gap + content_gap → what competitor gained this month that we haven't
```

Step 2: Calculate ROI proxy (include this in EVERY client report)
```
Traffic Value delta:
  traffic_value_sgd (this month) - traffic_value_sgd (last month) = SGD delta
  
  Example: SGD 4,200 this month vs SGD 3,600 last month
  Delta = +SGD 600 MoM
  Annualized: +SGD 7,200/year in search traffic equivalence
  
  Frame for client: "Your organic traffic this month is equivalent to SGD X
  in paid search value — up/down SGD Y vs last month."

Ranking momentum score:
  keywords_in_top3 (this month) vs keywords_in_top3 (last month) → ±%
  keywords_in_top10 (this month) vs last month → ±%
  avg_position (this month) vs last month → direction (improving/declining)
  
Agency KPI gate:
  Green ✅:  traffic_value_sgd +5% MoM  OR  avg_position improved ≥0.5
  Yellow ⚠️: traffic_value_sgd ±5% MoM (stable)
  Red 🔴:    traffic_value_sgd -10% MoM  OR  avg_position worsened >2
```

Step 3: Build narrative structure
```
SECTION 1 — TL;DR (3 bullets max, goes at top of every report):
  ✅ Win:      [specific metric + number that improved]
  ⚠️ Problem:  [specific metric + number that dropped]
  → Priority:  [ONE action this month that will move the needle most]

SECTION 2 — Traffic & Ranking (with numbers, never vague):
  Clicks: [X] this month vs [Y] last month ([+/-Z%])
  Impressions: [X] vs [Y] ([+/-Z%])
  Avg Position: [X] vs [Y] ([improved/declined] by [N])
  Traffic Value (SGD): [X] vs [Y] ([+/-Z])
  Top 3 rankings: [X keywords] vs [Y] last month

SECTION 3 — Content Published:
  [Article title] → published [date] → [clicks] clicks, [impressions] impressions so far
  → early performance: [above/below/on par with] site average

SECTION 4 — Technical Health:
  Health score: [X]/100 → [same/improved/declined] from last month
  Issues fixed: [list with impact]
  Issues open: [list with severity]

SECTION 5 — AI/GEO Visibility:
  AI referral traffic: [X clicks from AI platforms this month]
  Platform citations: [where client appears / where they dropped]
  
SECTION 6 — Next Month Actions (max 3, sorted by Priority score):
  1. [Action] → Expected impact: [metric + estimate]
  2. [Action] → Expected impact: [metric + estimate]
  3. [Action] → Expected impact: [metric + estimate]
```

Step 4: Deliver
→ Deck/presentation: `mcp__claude_ai_Gamma__generate` — use Section 1 TL;DR as the opening card
→ Quick shareable page: `Artifact` tool (HTML report) — good for an internal review pass before
  a client-facing deck
→ Drive/Docs delivery: `mcp__claude_ai_Google_Drive__create_file` (or Google Docs/Sheets MCP tools)
→ File name: `<client>_<market>_SEO_<YYYY-MM>`

---

## PLAYBOOK 9 — LOCAL SEO (SG + ID Local Businesses)

Applies to: saffrons.com.sg (halal catering), dehallsg.com (venue), RCS (renovation),
            rajawangi (ID), kgteknik (ID).

Step 1: GBP (Google Business Profile) audit
- Is GBP claimed and verified?
- Name-Address-Phone (NAP) consistent across site + GBP + all directories?
- Photos: minimum 10 photos (exterior, interior, products/services)
- Q&A section: populated with common questions + answers
- Recent posts (GBP posts): ≥1 per week → Google uses post frequency as engagement signal
- Reviews: volume + recency + response rate

Step 2: LocalBusiness schema audit
Check site for:
```json
{
  "@type": "LocalBusiness",
  "name": "…",
  "address": { "@type": "PostalAddress", "streetAddress": "…", "addressLocality": "Singapore", "postalCode": "…", "addressCountry": "SG" },
  "telephone": "+65XXXXXXXX",
  "geo": { "@type": "GeoCoordinates", "latitude": 1.XXXX, "longitude": 103.XXXX },
  "openingHoursSpecification": [{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "09:00", "closes": "18:00" }],
  "priceRange": "$$",
  "servesCuisine": "Halal"  // for food businesses
}
```
For Saffrons: also add `hasMenuSection` + `servesCuisine: "Halal"` + MUIS cert number in description.

Step 3: Local citation audit (SG)
Verified NAP must exist on:
- Google Business Profile
- Yelp Singapore (yelp.com.sg)
- Singapore Yellow Pages (yellowpages.com.sg)
- HardwareZone (for B2C services with community angle)
- Nextdoor.com (for residential services)
- STB (Singapore Tourism Board) if applicable
- JobStreet / LinkedIn Company Page (trust signal)
- Clutch.co / DesignRush (for agencies)

For Indonesia clients: GooglE Business, Tokopedia/Shopee store, Kaskus, Detik listing.

Step 4: Local keyword targeting
- Primary: `[service] Singapore` / `[service] [district]`
- Secondary: `best [service] Singapore`, `affordable [service] SG`, `[service] near me`
- Neighborhood modifiers: Orchard, Novena, Bukit Timah, Jurong, Tampines, etc.
- Intent: For local, prioritize transactional intent (hire, book, call) over informational

Step 5: Local content strategy
- Area landing pages (if serving multiple districts): unique content per page, not duplicate templates
- "Near me" targeting: include neighborhood names naturally in content
- Local events + news: seasonal content tied to SG calendar (National Day, CNY, Hari Raya, Deepavali)
- Customer-specific case studies with suburb/area mentioned

Step 6: Local pack optimization (3-pack)
Three factors: Relevance × Prominence × Distance
- Relevance: GBP category + website SEO alignment
- Prominence: reviews + citations + backlinks from local sites
- Distance: cannot be changed, but service-area radius in GBP should be set correctly
Target: appear in 3-pack for primary transactional keyword in Singapore

---

## PLAYBOOK 10 — TOPICAL AUTHORITY STRATEGY

Use when: client lacks cluster coverage and content isn't ranking despite technical health.

Step 1: Map topical clusters via SingRank
```
content_gap    → what topics are uncovered
keyword_gap    → what queries competitor ranks for client doesn't
published_articles → current content inventory
```

Step 2: Build cluster map
- 1 Pillar page (2500-4000w) covering the main topic at broad level
- 5-10 Cluster pages (2000-2500w each) covering subtopics in depth
- Cross-link: every cluster → pillar + related clusters

Step 3: Score coverage
```
Topical Authority Score (per cluster):
  Cluster coverage = pages_published / pages_needed × 100
  Link saturation  = pages_crosslinked / pages_published × 100
  
  Overall = (coverage + link_saturation) / 2
  Target ≥ 75% to be considered "authoritative" on the cluster
```

Step 4: Identify highest-value cluster to build out first
Use CPS_adjusted (FORMULA 9) on the pillar keyword of each cluster. Highest CPS_adjusted → build this cluster first.
Also factor in: existing topical coverage (clusters with 30-50% coverage need fewer new pieces).

---



- **Evidence over assertion.** Every claim needs a MCP data point or live-verified source.
- **Confidence labels.** Tag every finding: `Confirmed` (direct evidence) / `Likely` (multiple signals) / `Hypothesis` (single signal, needs verification).
- **Severity labels.** Every issue: `Critical` / `High` / `Medium` / `Low` / `Info`.
- **NEVER delete content.** Fix via rewrite → redirect → canonical → strengthen.
- **Client isolation.** Never mix data, credentials, or reports across clients.
- **Privacy.** Local model — no client PII or sensitive data to external services.
- **Locale.** SG default = en-SG, Indonesia = id-ID. Confirm market before SERP/keyword work.
- **Data freshness.** Always check `fetch_log` first. If data is stale, say so; don't guess.
- **Structural fixes first.** Fix crawl issues, broken links, and cannibalization before creating new content.

---

## TOOL ROUTING QUICK REFERENCE

| Need | Tool / Skill |
|---|---|
| Session bootstrap / always-current tool map | `brain{}` (SingRank MCP — call first, every session) |
| Client GSC / Clarity / AI data | SingRank MCP (`list_clients` → then others) |
| One-call client state | `client_action_briefing` (SingRank MCP) |
| Whole-account overview across clients | `bootstrap_briefing` (SingRank MCP) |
| Technical health score | `site_health` (SingRank MCP), or `brain{doc:'audit'}` for zero-cost precomputed |
| Real Google index status | `index_coverage` (SingRank MCP) |
| Core Web Vitals | `cwv_report` (SingRank MCP) |
| AI suggestions for what to fix | `smart_actions` (SingRank MCP) |
| Cannibalization detection | `find_cannibalization` (SingRank MCP) |
| Internal link suggestions | `suggest_interlinks` (SingRank MCP) |
| Cluster/pillar structure health | `pillar_map` (SingRank MCP) |
| Content gaps vs competitor (first-party) | `content_gap` + `keyword_gap` + `competitor_gap` (SingRank MCP) |
| Content ideas from real leads | `lead_content_ideas` (SingRank MCP) |
| Content brief (GEO-optimized) | `content_brief` (SingRank MCP) |
| Why one page ranks/doesn't | `rank_reasons` (SingRank MCP) |
| Learned winner-vs-loser features | `winning_patterns` (SingRank MCP) |
| Score a draft before publish | `score_draft` (SingRank MCP) |
| Log a fix/publish for validation | `log_experiment` → `experiment_results` (SingRank MCP) |
| Keyword research outside GSC footprint | `keyword_research` (SingRank MCP, first-party) |
| GEO health + AI citation data | `geo_briefing` / `geo_answerability_score` / `geo_citation_tracker` |
| Backlink profile / DR / RDs / anchor HHI | `mcp__claude_ai_Ahrefs__site-explorer-*` tools (Ahrefs — backlinks only, SingRank has none) |
| SERP check / "who ranks for X" | `WebSearch` |
| Fetch a page's raw HTML / competitor content | `WebFetch` |
| JS-rendered site / rendered DOM check | `claude-in-chrome` browser tools |
| Persist a note/finding for later retrieval | `mcp__claude_ai_SingRank_Save__put_document` / `search_documents` / `recall` |
| Report deck / presentation | `mcp__claude_ai_Gamma__generate` |
| Quick shareable report page | `Artifact` tool |
| Google Sheets/Docs/Drive delivery | `mcp__claude_ai_Google_Drive__*` tools |
| Client trend query ("how is X doing") | `brain{doc:'content'}` / `client_action_briefing` — see `seo-kb` skill |
| Full 20-category technical audit | `seo-audit` skill |
| GEO/AEO layer / AI crawler / llms.txt | `seo-geo` skill |
| Wix or Shopify platform-specific fixes | `seo-platforms` skill |
| Write SEO article (≥2500w) | `singrank-article-writer` skill |

Ahrefs' organic-keyword/SERP tools and all Semrush tools are optional fallbacks for domains
outside SingRank's tracked footprint — the first-party fusion tools above are the default.
