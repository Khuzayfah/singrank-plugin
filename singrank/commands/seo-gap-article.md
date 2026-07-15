---
description: Gap → keyword → top-10 teardown → verified deep research → high-conversion article (end-to-end)
argument-hint: [client domain, optional seed topic]
---

Run the **singrank-deep-research** skill end-to-end for: **$ARGUMENTS**, then write.

1. **Phase 1 — Gap hunt (SingRank System first):** `brain{doc:'content'/'ideas'}` →
   `keyword_gap` + `competitor_gap` + `content_targets` + `lead_content_ideas` →
   `keyword_research` for keywords OUTSIDE our footprint.
   **Phase 1b — Sibling expansion (our own high-impression assets):** high-impression
   weak-position clusters, winner-page overflow queries (impressions on the wrong
   intent), high-impression queries with no dedicated page, 9-angle spins of proven
   winners. Siblings with proven impressions usually beat external gaps with estimated
   volume. Gate for ALL candidates: demand evidence + money page + intent_fit ≥0.7 +
   3-part cannibalization test + lane locks.
   Present top 3–5 candidates with ROS/CPS math; confirm the pick.
2. **Phase 2 — SERP teardown:** WebSearch top-10 →
   `python tools/deep_research.py --keyword "<kw>" --urls ...` → beat-plan
   (must-cover + 2–3 ⭐ gap sections + tables to build + depth/freshness edge)
   cross-checked against `winning_patterns {domain}`.
3. **Phase 3 — Deep facts:** primary sources first; every borrowed stat re-verified
   via `python tools/web_research.py verify` (EXACT/PARAPHRASE only); real GSC query
   language as longtails.
4. **Phase 4 — Brief:** merge with `content_brief {domain, keyword}` → emit the
   `=== SINGRANK RESEARCH BRIEF ===` block (keyword, longtails, internal links,
   MONEY PAGE + CTA, SALES ANGLE, provenance table) → save to SingRank Save.
5. **Write:** singrank-article-writer + singrank-writing-craft. High-conversion,
   naturally human, unique — never generic.
6. **Gate:** qc_check.py exit 0 → `score_draft` ≥80 → deliver as DRAFT (publish only
   with approval) → `log_experiment` after publish.

If no client was given, ask which client first.
