---
description: Build a client-ready monthly SEO report (statistically honest, SDS-validated)
argument-hint: [client domain, optional month/period]
---

Launch the **report-builder** agent for: **$ARGUMENTS**

The agent must pull `client_action_briefing`, `gsc_summary` (period vs
prior), `top_movers` (with `date` arg; fallback to gsc_summary diff),
`anomalies`, `ai_visibility`, `ai_referral_log`, `algo_events`, and Ahrefs
DR/referring-domains; validate every claimed movement with SDS (report <1.65
as stable, not as change); attribute algorithm-driven movement honestly; and
return a client-ready markdown report plus an internal appendix with the
calculations.

Language: English for SG clients, Bahasa Indonesia for rajawangi/kgteknik.
If no client was given, ask which client first.
