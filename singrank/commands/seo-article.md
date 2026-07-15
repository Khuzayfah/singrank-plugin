---
description: Write a SingRank-standard article (≥2500w, zero-fabrication, GEO-ready) from a brief
argument-hint: [client domain + topic, or "from brief" if one exists in context]
---

Launch the **article-writer** agent for: **$ARGUMENTS**

The agent requires a verified research brief. If none exists in context,
first generate one live: `content_brief {domain, keyword}` +
`winning_patterns {domain}` (or full singrank-pipeline Stages 2–5), THEN
write, with the `singrank-writing-craft` skill loaded alongside the
article-writer standard.

Standards enforced: ≥2500 words, hook-engine opening (answer capsule 50–60w
+ honest curiosity loop), Key Takeaway box, citation magnets, comparison
table where the topic allows, H2-first flat structure (15–20 blocks of
120–180w; ≥2 question-form H2s; ≥5 PAA question lines; number density
≥4.5/100w), 6 keyword floors, FAQ as on-page content — **NO FAQPage/HowTo
schema** (schema = Article + BreadcrumbList + Speakable, separate block),
meta title ≤60 / description 150–160 chars, per-client constraints from the
playbook roster (YMYL, MUIS, no-pricing, bylines), zero fabricated facts.

Gate before handoff: `python tools/qc_check.py` exits 0 AND `score_draft`
≥80 (or /seo-qc for the full gate). Deliver as draft — do not publish
without approval (platform-executor publishes; then `log_experiment`).
