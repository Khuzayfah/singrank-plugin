---
name: seo-kb
description: Live client-trend answers over the SingRank dashboard data. Use this WHENEVER the user asks about a client's traffic, impressions, rankings, keywords going up/down, performance trends, or "how is <client> doing". Answers come from the SingRank System MCP's precomputed knowledge docs and live GSC tools — no local script, no offline pipeline.
version: 2.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [SEO, Trends, Analytics, Keywords, Traffic]
    related_skills: [seo-agency]
---

# SEO Trend Brain

There is no local script for this anymore — the client trend/analysis pipeline this skill
used to wrap (`C:\Users\natur\AppData\Local\hermes\seo_kb\seo_kb.py`) no longer exists on
disk. All of its jobs are now done **live, server-side, by the SingRank System MCP** — the
real production pipeline runs on the agency's own NAS (cron-refreshed, first-party, no
Ahrefs/Semrush dependency) and is exposed entirely through MCP tools. Use those.

## CRITICAL: do not guess client metrics — pull the data first

Whenever the user asks about performance, traffic, impressions, rankings, keyword movement,
or trends for a client, run the relevant tool below and reason over the real output. Never
answer client numbers from memory or from a prior conversation's numbers.

## Zero-cost fast path

`mcp__claude_ai_SingRank_System__brain{doc:'content'}` — per-client ranked content ideas,
CTR leaks, high-intent articles, and cluster gaps, regenerated every 3 hours server-side.
`brain{doc:'audit'}` — per-client technical audit + DO-NEXT list, regenerated nightly.
Read these first; they cost zero tool calls and are usually already the answer.

## "How is `<client>` doing?" — standard flow

1. `list_clients` → resolve the exact domain key if unsure.
2. `client_action_briefing {domain}` → one call: traffic delta, keyword bucket counts
   (top3/top10/top20), pillar/content ideas. This is the primary answer for this question.
3. If they ask about a longer trend or a specific date range: `gsc_summary {domain, days}`
   for the rollup, or `gsc_page_trend {domain, page}` / `gsc_query_trend {domain, query}` for
   daily history on one page or query.
4. If they ask *why* something moved: `anomalies {domain}` (auto-flagged) + `top_movers
   {domain, date}` (often empty — if so, diff two `gsc_summary` windows manually) +
   `algo_events {}` to correlate with a known Google update.
5. For content-strategy framing on top of the numbers: `bootstrap_briefing` (whole-account,
   all clients at once) or `brain{doc:'content'}` for this one client.
6. Synthesize a short, decisive read: what moved, by how much, likely driver, next action.
   Cite the actual numbers returned by the tool. State the data's `fetch_log` freshness if
   it's more than ~48h old — don't present stale data as current without saying so.

## Deeper trend/pattern questions

- "What's driving this ranking (or the lack of one)?" → `rank_reasons {url}` — classifies the
  page (🏆/🪫/mid/👻 invisible) and returns why it ranks + the gap checklist vs the client's
  own winner profile.
- "What does content that actually works for this client look like?" → `winning_patterns
  {domain}` — learned feature differences between winners (pos ≤8) and losers (pos ≥15).
- "Which articles are actually producing leads?" → `lead_content_ideas {domain}` (real leads,
  where the tracking widget is installed) or `high_intent_articles {domain}` (heuristic,
  works everywhere).
- Full recipe list and 50-tool map: `brain{doc:'skill'}`.

## Notes

- Monetary values (`traffic_value_sgd`) are already in SGD.
- If a SingRank MCP tool errors or times out, say so rather than inventing numbers — don't
  fall back to a remembered figure from earlier in the conversation.
- To persist a note or finding for future sessions (the old KB's "accumulated reasoning" idea),
  use `mcp__claude_ai_SingRank_Save__put_document` and retrieve it later with
  `search_documents` / `recall` — this is the current first-party equivalent, not a local file.
