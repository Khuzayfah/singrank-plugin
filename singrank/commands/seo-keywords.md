---
description: Find ROS-scored keyword & content opportunities for a client
argument-hint: [client domain, optional topic focus]
---

Launch the **keyword-strategist** agent for: **$ARGUMENTS**

The agent must start from SingRank System: `brain{doc:'content'}` +
`brain{doc:'ideas'}` (precomputed, often already the shortlist), then live
`keyword_gap`, `content_gap`, `competitor_gap`, `content_targets`,
`lead_content_ideas` (real leads) / `high_intent_articles`, GSC positions
4–20, and `keyword_research {seed}` for volume outside the GSC footprint
(Ahrefs only as fallback). Score with ROS (F2) using honest SERP modifiers,
run the 3-part cannibalization test + lane locks (KG Teknik ↔ Rajawangi),
decide improve-vs-create per topic (F5 decay check), and return a
Priority-sorted opportunity table with calculations plus a cluster map —
ready to feed into /seo-win.

If no client was given, ask which client first.
