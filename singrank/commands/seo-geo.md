---
description: GEO/AEO audit — AI-search visibility, citability, llms.txt, AI Share of Voice
argument-hint: [client domain, optional target topic]
---

Launch the **geo-analyst** agent for: **$ARGUMENTS**

The agent must baseline with SingRank System: `geo_briefing` →
`ai_visibility` → `geo_answerability_score` → `geo_citation_tracker`
(Gemini citation probe) → `ai_referral_log` (pixel data; Ahrefs brand-radar
optional cross-check only); audit the full GEO stack per the `seo-geo`
skill (AI crawler access via `tools/seo_audit.py`, citability structure,
entity clarity, schema, brand authority — llms.txt is LOW-priority hygiene,
never a headline finding); score with F9 GEO efficiency showing the boosts;
and return a per-page GEO scorecard with a Priority-ordered fix list per
platform. Be honest about coverage: automated citation probe = Gemini only;
ChatGPT/Perplexity = manual sample.

If no client was given, ask which client first.
