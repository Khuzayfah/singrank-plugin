---
name: seo-kb
description: Local SEO knowledge base + trend brain over the SingRank dashboard data. Use this WHENEVER the user asks about a client's traffic, impressions, rankings, keywords going up/down, performance trends, or "how is <client> doing". It gives grounded, data-backed answers from a local SQLite store that auto-refreshes daily and accumulates a learning history of trends.
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [SEO, Trends, RAG, Analytics, Keywords, Traffic, Self-learning]
    related_skills: [seo-agency]
---

# SEO Knowledge Base + Trend Brain

A local pipeline mirrors the **SingRank dashboard** (13 clients) into a SQLite KB and
analyzes it. It runs fully offline (data pulled from the `singrank` MCP, embeddings via
local Ollama `nomic-embed-text`). It **auto-refreshes daily at 06:00** via cron and
**accumulates a dated trend-insight history** — so the longer it runs, the more pattern
context you have. That accumulating history is the "learning": always lean on it.

Script: `C:\Users\natur\AppData\Local\hermes\seo_kb\seo_kb.py` (run with `python`).

## CRITICAL: do not guess client metrics — query the KB first

Whenever the user asks about performance, traffic, impressions, rankings, keyword
movement, or trends for a client, **run the relevant command below and reason over the
real output.** Never answer client numbers from memory.

## Commands

```bash
# List tracked clients (get the exact domain key)
python C:\Users\natur\AppData\Local\hermes\seo_kb\seo_kb.py clients

# TREND ANALYSIS — traffic/impression WoW %, 28-day change, avg-position delta,
# and rising/falling keywords. THIS is the trend brain — use it for "how is X doing".
python C:\Users\natur\AppData\Local\hermes\seo_kb\seo_kb.py trends --domain ablink.sg
python ...\seo_kb.py trends --json            # all clients, machine-readable

# RAG retrieval — semantic search over snapshots, keywords, articles, and the
# accumulated daily insight notes. Use for "what content covers X", "what changed".
python ...\seo_kb.py query "electric van rental pricing" --domain ablink.sg -k 6
python ...\seo_kb.py query "biggest traffic changes this week" --domain ablink.sg --json

# What's in the KB + when it last refreshed
python ...\seo_kb.py stats

# Force a fresh pull + re-embed now (normally automatic at 06:00 daily)
python ...\seo_kb.py refresh                  # all clients
python ...\seo_kb.py refresh --domain ablink.sg
```

## Strategy, analysis & research commands (the "SEO weapon")

```bash
# AI daily read — gemma explains WHY metrics moved + logs wins/issues/actions to
# reports/<domain>/<date>.md and the rolling knowledge/<domain>.md. Runs in the daily cron.
python ...\seo_kb.py analyze --domain ablink.sg

# FULL per-client strategy — target keywords, content PILLARS, topic clusters, and an
# internal-link plan. Written to strategy/<domain>.md. This is the planning weapon.
python ...\seo_kb.py strategy ablink.sg

# Internal-link suggestions only (no model) — which existing articles should interlink,
# computed from content-embedding similarity. Use when planning interlinking.
python ...\seo_kb.py links ablink.sg

# Web search for source material AFTER you know what to write (finds references).
# If it reports "unreachable", use the duckduckgo-search / scrapling skills instead.
python ...\seo_kb.py search "electric van rental singapore 2026"
```

Persisted outputs (read these — they accumulate the agency's SEO brain):
- `seo_kb/reports/<domain>/latest.md` + dated — daily AI analysis (why, wins, issues, actions).
- `seo_kb/knowledge/<domain>.md` — rolling change-log: what moved each day, what's good/bad.
- `seo_kb/strategy/<domain>.md` — current keyword/pillar/topic/internal-link plan.

## Self-learning RAG (gets smarter daily)

Every daily run embeds the new trend insight, the AI "why" analysis, and the strategy into
the vector store, and **ingests the skills + knowledge logs + notes** as RAG too. So the
`query` command retrieves not just raw data but the agency's *accumulated reasoning* — past
analyses, strategies, and operating knowledge — "stored exact, usable anywhere". The longer
it runs, the more pattern context every answer has. A client query also pulls `_global`
knowledge (skills/memory/notes) automatically.

```bash
# Ingest MD knowledge (skills, knowledge logs, notes) into the RAG. Runs in the daily cron.
# Add your own SEO playbooks/SOPs as .md under seo_kb/notes/ and they become retrievable too.
python ...\seo_kb.py ingest
python ...\seo_kb.py ingest path\to\a-playbook.md   # ingest a specific file/dir
```

Before answering a hard SEO/GEO question for a client, `query` it first — you will get the
relevant past conclusions back, then build on them instead of starting from scratch.

## Recommended "SEO weapon" workflow for a client

1. `trends --domain X` → see what moved.
2. `analyze --domain X` → AI read of why + actions (or read `reports/X/latest.md`).
3. `strategy X` → keyword targets, pillars, topics, internal-link plan.
4. `links X` → exact interlinking pairs to implement.
5. For a new article: `brief <domain> "<topic>"` to get a KB-grounded research brief, then
   `write <domain> "<topic>"` for a full ≥2500-word SingRank-standard draft (auto: outline →
   sections → FAQ → schema), then refine with the `singrank-article-writer` skill — verify any
   `[verify before publishing]` stats live via `duckduckgo-search`/`scrapling`, humanize, ship.

```bash
python ...\seo_kb.py brief ablink.sg "monthly electric van rental"
python ...\seo_kb.py write ablink.sg "monthly electric van rental" --type guide   # -> articles/<domain>/<slug>.html
```

## How to answer a "how is <client> doing?" request

1. Resolve the domain via `clients` if unsure.
2. Run `trends --domain <domain>` → read clicks/impressions WoW %, 28-day change,
   position delta, rising/falling keywords.
3. If they ask *why* or about content/topics, run `query "<topic>" --domain <domain>`.
4. Synthesize a short, decisive read: what moved, by how much, likely driver, and the
   next action. Cite the numbers. Mark the source date.

## What the trend brain tracks

- **Traffic & impressions:** week-over-week and 28-day % change from 90 days of GSC daily history.
- **Average position:** 7-day vs prior 7-day delta (negative = improved).
- **Keyword movement:** rising/falling queries by position + click delta. This needs **2+
  daily snapshots** to populate — it activates automatically after the KB has run on two
  separate days. Until then it says it's "building history" (expected on day one).
- **Daily insight notes:** every refresh writes a dated trend digest per client into the KB
  and embeds it, so you can retrieve "what was happening on/around <date>" over time.

## Training corpus (LoRA/QLoRA)

Every daily refresh also regenerates `seo_kb/dataset/seo_train.jsonl` — an instruction
corpus (ShareGPT `messages`) built from the accumulated trend insights, for eventually
fine-tuning a local model. Build on demand:

```bash
python ...\seo_kb.py dataset --out C:\Users\natur\AppData\Local\hermes\seo_kb\dataset\seo_train.jsonl
```

The full QLoRA → GGUF → Ollama recipe is in `seo_kb/TRAINING.md`. Keep RAG for live numbers;
the fine-tune is only for analysis *style/reasoning*.

## Notes

- Monetary values (`traffic_value_sgd`) are already in SGD.
- If a command errors with a connection problem, the `singrank` MCP or Ollama may be down;
  say so rather than inventing numbers.
- The reasoning quality is bounded by the local model. For deep written analysis the owner
  can enable a stronger model; the *data* here is always exact.
