---
description: Full technical SEO audit of a SingRank client site (20 categories, weighted scoring)
argument-hint: [client domain]
---

Launch the **seo-auditor** agent for: **$ARGUMENTS**

The agent must read `singrank-playbook` + `seo-audit` skills, start from
`brain{doc:'audit'}` (precomputed nightly audit + DO-NEXT), then live MCP data
(`list_clients` → `site_health` → `index_coverage` → `broken_links` →
`cwv_report` → `gsc_summary` → `anomalies` → `fetch_log`), verify findings on
the live pages with `python tools/seo_audit.py <url>`, run the 20-category
audit, and return findings in the standard block sorted by F1 Priority with
calculations shown.

If no client was given, ask which client first.
