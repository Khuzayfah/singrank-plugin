---
description: Full technical SEO audit of a SingRank client site (20 categories, weighted scoring)
argument-hint: [client domain]
---

Launch the **seo-auditor** agent for: **$ARGUMENTS**

The agent must read `singrank-playbook` + `seo-audit` skills, pull live MCP
data first (`list_clients` → `site_health` → `gsc_summary` → `anomalies` →
`fetch_log`, plus Ahrefs `site-audit-issues` and Semrush
`siteaudit_research`), run the 20-category audit, and return findings in the
standard block sorted by F1 Priority with calculations shown.

If no client was given, ask which client first.
