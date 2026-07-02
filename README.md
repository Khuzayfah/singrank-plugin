# SingRank SEO Plugin

A Claude Code plugin bundling the SingRank SEO/GEO agency toolkit for Singapore & Indonesia clients: technical audits, ranking recovery, keyword & content-gap analysis, cannibalization checks, GEO/AI-search visibility, Wix/Shopify platform fixes, and long-form article writing.

## Install

In Claude Code:

```
/plugin marketplace add Khuzayfah/singrank-plugin
/plugin install singrank@singrank-plugin
```

Then restart Claude Code (or reload) so the skills and command register.

## What's included

### Slash command
- `/seo [task]` — routes an SEO/GEO task to the right skill and starts with live MCP data.

### Skills (auto-invoked by trigger phrases)
| Skill | Use for | Trigger examples |
|---|---|---|
| `seo-agency` | Master agency workflow — audits, recovery, keyword/content-gap, cannibalization, orphans, reports, strategy | "audit", "ranking turun", "cari keyword", "content gap", "laporan bulanan" |
| `seo-audit` | Full 20-category technical audit with weighted scoring, CWV, schema, E-E-A-T | "full audit", "technical SEO", "core web vitals", "schema audit" |
| `seo-geo` | GEO/AEO — AI search visibility, llms.txt, citability, AI Share of Voice | "AI search", "GEO", "llms.txt", "Perplexity citation" |
| `seo-platforms` | Wix & Shopify implementation — meta, schema, internal links, gotchas | "fix di Wix", "update Shopify", "inject schema" |
| `seo-kb` | Local trend brain over SingRank dashboard data | "how is X doing", "trend klien", "traffic naik/turun" |
| `singrank-article-writer` | 2500+ word humanized, zero-fabrication SEO/AEO/GEO articles from a brief | "tulis artikel", "write article", "draft article for [client]" |

## Notes

- The skills expect the SingRank / Ahrefs / Semrush MCP servers to be connected for live data.
- No client content is ever deleted — fixes are done via rewrite, redirect, canonical, strengthen, or interlink.

## License

MIT
