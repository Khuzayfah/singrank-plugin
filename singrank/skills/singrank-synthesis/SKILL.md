---
name: singrank-synthesis
description: >
  SingRank synthesis discipline — turn scraped/researched source material into ORIGINAL,
  trustworthy, fact-only writing that reads as if written from understanding and
  experience, never copy-paste. Cite official sources, play on data not assumptions,
  avoid plagiarism, avoid opinion, protect the client's reputation. Trigger phrases:
  "olah hasil scraping", "tulis dari pemahaman", "jangan copy paste", "sintesis",
  "rewrite from sources", "buat original dari data", "akademis dan natural". Read
  alongside singrank-article-writer + singrank-writing-craft whenever an article draws
  on external sources. The originality guard (tools/originality_check.py) enforces it.
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  singrank:
    tags: [Synthesis, Originality, EEAT, Anti-Plagiarism, Facts, Trust]
    related_skills: [singrank-article-writer, singrank-writing-craft, singrank-deep-research, singrank-qc]
---

# SingRank Synthesis v1.0 — Write From Understanding, Not From Copy-Paste

The principle in one line: **facts are borrowed, WORDS are ours, sources are named.**
We gather trusted material (official primary sources, first-party client data, verified
research), understand it, and write original prose that a domain expert would sign —
grounded entirely in data, free of opinion, free of plagiarism, safe for the client's
reputation. We play on data, not assumptions.

---

## 1. THE SYNTHESIS LOOP (per fact, before it becomes a sentence)

1. **Read the source, close it, then write.** Never draft with the source sentence on
   screen to "reword" — that produces echo. Absorb the fact, look away, state it in the
   article's own voice and framing.
2. **One insight from many sources.** The original contribution is the SYNTHESIS: combine
   2–3 sources into a single sentence the reader can't get from any one of them.
   ("HDB caps noisy work at three consecutive days [rule], and fines reach S$5,000 on
   conviction [penalty] — so the real cost of ignoring the window isn't inconvenience,
   it's a five-figure risk [our synthesis].")
3. **Attribute the FACT to its origin, not the reteller.** "According to HDB (2026)…"
   — the official source, verified via `web_research.py verify` / `source-check`.
   Never cite the listicle that retold it.
4. **Fact, then meaning.** State the verified fact, then what it MEANS for this reader.
   The meaning is analysis (allowed, valuable); it must follow from the data, not from
   opinion.

## 2. WHAT COUNTS AS ORIGINAL (the wording test)

- No run of 8+ consecutive words matching any source (that's LIFTED — `originality_check.py`
  flags it as P0).
- No sentence that's a source sentence with synonyms swapped (that's ECHO — reword from
  the idea, not the sentence).
- Structure, order, and emphasis are ours: we choose which facts matter for THIS client's
  reader and arrange them for THIS article's angle. A rearranged copy is still a copy;
  a re-understood explanation is original.
- Numbers, names, dates, quotes are reproduced EXACTLY (facts don't get "reworded") — but
  the sentence carrying them is ours.

## 3. FACT-ONLY, OPINION-OUT (reputation safety)

- **State facts; label judgement.** Anything that isn't verifiable is either cut or
  clearly marked as assessment ("Based on our experience on HDB projects…", `[assessment]`).
  Never present opinion as fact.
- **No disparagement.** Never write anything negative about a named competitor,
  authority, or third party as fact unless it is documented and sourced — reputation and
  defamation risk. Compare on neutral, sourced criteria only.
- **No unsupported absolutes** ("the best", "guaranteed", "always") unless the client's
  own verified credential supports it. YMYL (yescpap): zero health claims without a
  peer-reviewed/gov source.
- **Client compliance is law** — the playbook roster rules (De Hall no pricing, Ablink no
  vehicle price, RCS no CaseTrust, lane locks) apply to synthesized content too.

## 4. ACADEMIC-NATURAL VOICE (trusted, not stiff)

The reader should trust it like a well-sourced guide AND enjoy it like a person wrote it:
- Evidence density of a good explainer: a source or a number in most sections, inline
  attribution, no vague "studies show".
- Human rhythm of the hook engine: answer-first, burstiness, one plain-spoken expert
  view per section, the deliberately-imperfect texture (writing-craft) — NEVER imperfect
  in facts.
- Explain the mechanism, not just the claim. "Why" and "which means" turn a fact list
  into understanding — that's what reads as expertise.
- Define terms in plain language the first time; then use them precisely. Academic =
  rigorous and clear, not jargon-heavy.

## 5. SOURCES WE TRUST (the material, ranked)

1. **Official primary** — gov/authority (HDB, LTA, BCA, MUIS, BPS, Kemenkes, official
   event pages). `web_research.py source-check` must grade PRIMARY.
2. **First-party / client-owned** — the client's verified credentials, real project
   data, SingRank System RAG (`search_articles`/`get_article`), GSC query language.
   This is the "trusted material not widely public" edge: use it, it's ours to use.
3. **Original research** — a named study with its own methodology (source-check =
   ORIGINAL-RESEARCH). Cite the paper, not a blog about it.
4. Reputable secondary only to corroborate, never as the sole source, never quoted.

Anything unverifiable → cut or `[verify before publishing]` (and the publish gate
blocks leftover markers). We don't fill gaps with assumptions.

---

## 6. THE GATE (mechanized — runs before publish)

```
python C:\Users\natur\singrank-plugin\singrank\tools\originality_check.py \
    <draft.html> --sources <facts.jsonl from smart_scrape/deep_research> [--sources PACK.md]
```
- Exit 1 (any LIFTED passage) = BLOCKED. Rewrite the flagged sentences from understanding.
- ECHO passages = reword in our voice before publish.
- Then the normal chain: `qc_check.py` (structure/links/[verify] markers) →
  `score_draft` ≥80 → approval → publish → `log_experiment`.

Originality guard checks WORDING; `web_research.py verify` checks FACTS; both must pass.
An article can be 100% original words and still need a citation for every fact — do both.

## WORKFLOW POSITION
deep-research/smart_scrape (gather + verbatim facts) → **synthesis (this skill): write
original prose from the facts** → originality_check + qc_check + verify → publish.
