---
name: singrank-prospecting
description: >
  SingRank qualified B2B lead generation — find Singapore/Indonesia businesses that
  demonstrably need SEO, prove it with a live audit, and reach them via their own
  published business contact. Trigger phrases: "cari klien", "cari prospek", "lead
  generation", "prospek SEO", "cari perusahaan yang butuh SEO", "find prospects",
  "who needs SEO". Produces a ranked, CRM-ready lead pack where every lead carries a
  real audit hook to open the pitch. Business-contact only, PDPA-safe — no personal
  data harvesting, no bypassing logins/anti-bot.
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  singrank:
    tags: [Prospecting, LeadGen, Sales, Audit, B2B]
    related_skills: [singrank-playbook, singrank-deep-research]
---

# SingRank Prospecting v1.0 — Qualified Leads, Not Cold Spray

The agency's growth engine. The winning move is NOT mass email scraping (low
conversion, PDPA-violating, gets you blocked). It is: **find businesses whose SEO is
measurably weak → prove it with a real audit → reach them through their own published
business contact → open with a concrete finding.** "Your site ranks nowhere for your
main service and has 12 broken links — we fix exactly this" converts. A cold blast
does not.

## SCOPE & ETHICS (non-negotiable — this is what keeps the system running smooth)
- **Public BUSINESS contact only** — the email/phone/form a company publishes on its
  own Contact/About/footer for exactly this purpose. Business data, not personal.
- **PDPA-safe (Singapore) / UU PDP (Indonesia):** no personal-individual harvesting,
  no event attendee lists behind logins, no scraping of private directories.
- Respect the target's robots.txt; rate-limited; the scraper identifies itself.
- Never bypass authentication, anti-bot, or paywalls. `prospect_hunter.py` enforces
  these in code — don't work around them.
- Downstream outreach must honour opt-out and identify the sender. Cold outreach law
  is the operator's responsibility; this skill only QUALIFIES leads.

## THE FLOW

### 1. Define the target segment
Pick a niche + area with real SEO spend potential (dental clinics, aircon servicing,
law firms, F&B chains, renovation, clinics, tuition centres — SG or ID). The best
segments: fragmented markets, high customer LTV, visible competitors already ranking.

### 2. Discover candidates (Claude's WebSearch — keyless engines are blocked here)
`WebSearch "<niche> singapore"`, `"<niche> <district>"`, `"best <niche> singapore"`
→ collect the business homepage URLs from the results (their OWN sites, not
directories). Also mine `competitor_gap`/SERP: whoever ranks pages 2–5 for the niche's
money keywords is a business that's trying at SEO and failing = a warm prospect.

### 3. Qualify (the tool does the heavy lifting)
```
python C:\Users\natur\singrank-plugin\singrank\tools\prospect_hunter.py qualify \
    --niche "<niche> singapore" --urls <homepage1> <homepage2> ... --out-dir leads_<niche>
```
For each candidate it: runs the live SEO audit (reusing `seo_audit.py`), extracts the
public business contact (mailto/contact page/footer, tech-noise filtered), and scores
the LEAD. **Scoring logic = opportunity × reachability:** SEO 40–70 (clearly needs
help AND salvageable) + reachable = 🔥 HOT; already-strong sites score low (low need);
no public contact = dropped. Output: `LEADS.md` (ranked table) + `leads.jsonl` (CRM).

### 4. Scale the research (optional, GPU — many candidates)
For a big candidate list, `smart_scrape.py` can pre-read each site's about/services to
enrich the segment understanding, and `llm_local.py` can classify fit in bulk — all
token-free on the RTX 5080. End with `llm_local.py --down`.

### 5. Arm the pitch (per HOT lead)
```
python tools\seo_audit.py <lead-url> --out <lead>-audit.md
```
The full audit is the attachment/leave-behind. Open the outreach with the lead's
`pitch_hooks` (real findings from THEIR site) — never a generic intro. The pitch is a
free, specific diagnosis, not a sales blast. Route interested leads into onboarding
(SingRank System `list_clients` once signed).

## OUTPUT FORMAT (Claude-friendly, RAG-ready)
- `LEADS.md` — ranked human-readable pack (tier · business · SEO score · contact ·
  pitch hook). This is what you read/act on.
- `leads.jsonl` — one JSON object per lead (CRM import / dedupe / follow-up tracking).
- Per-lead `<lead>-audit.md` — the full technical audit, generated on demand for HOTs.
Store a segment's pack under `D:\database\leads\<niche>\` so it persists and dedupes
across runs. Every metric is audit-derived from the live site — zero fabricated data.

## HONEST LIMITS
- Keyless search is blocked on this network → candidate discovery uses Claude's
  WebSearch, not an in-tool crawler.
- The tool finds PUBLISHED contacts; some businesses only expose a form → the lead
  still qualifies on `contact_page`, outreach goes through the form.
- Lead score is an OPPORTUNITY heuristic (SEO weakness + reachability), not a promise
  of conversion — it ranks where to spend outreach effort first.
