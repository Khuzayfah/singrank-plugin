---
description: Find qualified SG/ID businesses that need SEO — audit-proven leads with pitch hooks (PDPA-safe B2B)
argument-hint: [niche + area, e.g. "dental clinics singapore" or "aircon servicing tampines"]
---

Run the **singrank-prospecting** skill for: **$ARGUMENTS**

1. Discover candidate business homepages via `WebSearch "<niche>"`, `"best <niche>
   singapore"`, `"<niche> <district>"` — collect their OWN site URLs (not directories).
   Also flag whoever ranks page 2–5 for the niche's money keywords (trying at SEO,
   failing = warm).
2. Qualify: `python C:\Users\natur\singrank-plugin\singrank\tools\prospect_hunter.py
   qualify --niche "$ARGUMENTS" --urls <homepages...> --out-dir D:\database\leads\<slug>`
   → ranked LEADS.md + leads.jsonl (SEO audit + public business contact + lead score).
3. For each 🔥 HOT lead: `seo_audit.py <url> --out <lead>-audit.md` for the full report,
   and draft a pitch built on its `pitch_hooks` (real findings, never a cold intro).
4. Report the top leads with their hooks and contacts.

SCOPE: public BUSINESS contact only (PDPA/UU-PDP safe) — no personal-data harvesting,
no bypassing logins/anti-bot, respect robots.txt. This skill QUALIFIES leads; outreach
compliance (opt-out, sender ID) is the operator's responsibility.

If no niche/area was given, ask which segment and market first.
