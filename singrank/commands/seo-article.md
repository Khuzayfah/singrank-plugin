---
description: Write a SingRank-standard article (≥2500w, zero-fabrication, GEO-ready) from a brief
argument-hint: [client domain + topic, or "from brief" if one exists in context]
---

Launch the **article-writer** agent for: **$ARGUMENTS**

The agent requires a verified research brief. If none exists in context,
first generate one via the singrank-pipeline Stages 2–5 (discovery →
prioritize → SERP recon → `content_brief`), THEN write.

Standards enforced: ≥2500 words, Key Takeaway box, citation magnets, 6
keyword floors, FAQ + FAQPage schema, meta title ≤60 / description 140–155
chars, per-client constraints from the playbook roster (YMYL, MUIS,
no-pricing, bylines), zero fabricated facts.

Deliver as draft — do not publish without approval (use platform-executor
for publishing after approval).
