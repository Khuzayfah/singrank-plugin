---
name: singrank-qc
description: >
  SingRank quality-control gate (Pipeline Stage 5). Runs on a finished article
  BEFORE publishing: numeric blocking gate (score ≥90 AND zero P0, auto-iterate
  the writer up to 3×), live broken-link check, factcheck confidence scoring
  (EXACT / PARAPHRASE / NOT-FOUND) against the brief's sources, per-client
  compliance from the playbook roster, schema deprecation linting (FAQPage/HowTo
  = P0), hook-gate, and 5-engine GEO extraction audit. Trigger phrases: "QC this
  article", "cek artikel", "quality check", "cek halusinasi", "check broken
  links", "audit before publish", "layak publish nggak". It flags and scores; it
  does NOT rewrite — failures route back to singrank-article-writer.
version: 1.3
platforms: [linux, macos, windows]
metadata:
  singrank:
    tags: [QC, Quality, Factcheck, GEO, Schema, Compliance, Gate]
    related_skills: [singrank-article-writer, singrank-playbook, singrank-pipeline]
---

# SingRank QC v1.3 — Quality Control Gate (Pipeline Stage 5)

Audits a finished article before publishing. It flags problems and scores them; it does
not fix them. On PASS → publish (or hand to the platform executor). On FAIL → route back
to `singrank-article-writer` with the exact fix list — automatically, up to 3 iterations,
then escalate to the user. QC rigour never scales down: a quick cluster article passes
the same full gate as a deep pillar.

**Precedence on conflict:** zero-fabrication wins → stricter rule → engine mechanics →
brand layer → pipeline order.

---

## THE BLOCKING GATE

Score the article 0–100. Severity classes:
- **P0 (CRITICAL):** fabricated/unverified fact, broken link, guessed URL, compliance
  breach (roster), deprecated schema (FAQPage/HowTo), language mix, missing disclaimer,
  curiosity loop that misleads or is never paid off.
- **P1 (major):** weak anchor, buried answer, thin E-E-A-T, missing Speakable, capsule
  size off-target, missing micro-story.
- **P2 (minor):** style, polish.

**PASS = score ≥90 AND zero P0.** Any P0, or score <90 → FAIL → back to the writer with
the exact fix list. Re-QC the returned draft. After **3 failed iterations**, STOP and
escalate with the blocking issues. Never pass a P0 by rounding up.

Weights (100): Factcheck 30 · Compliance 20 · GEO extraction 20 · Links/anchors 10 ·
E-E-A-T 10 · Schema 10.

---

## STEP 1 — MACHINE PASS (run first, one command)

```
python C:\Users\natur\singrank-plugin\singrank\tools\qc_check.py <article.html> \
  --base-url https://<client-domain> --lang <en|id> --min-words 2500
```

Deterministic checks (60 of the 100 points): every link fetched live (4xx = P0, redirect
chains ≥2 hops = P1, weak anchors = P1), word-count floor, H2/H3 capsule sizes (120–180w),
FAQ extractability (≥5 question headings), banned AI-filler phrases, burstiness,
language-mix detection (P0), schema deprecation lint (FAQPage/HowTo/SpecialAnnouncement =
P0). Exit code 1 = P0 present. Fix everything it reports before the manual pass.

---

## STEP 2 — FACTCHECK (30 pts — the part only you can do)

Cross-verify EVERY factual element (number, price, date, named entity, quote, credential)
against the brief's sources. For each claim:

```
python ...\tools\web_research.py verify <source-url> "<the exact claim>"
```

Confidence tiers:
- **EXACT** — appears verbatim on the fetched source ✅
- **PARAPHRASE** — source supports it, wording differs; confirm meaning intact ✅
- **NOT-FOUND / SOURCE-UNREACHABLE** — **P0 FABRICATED** — remove the claim or mark
  `[verify before publishing]` and FAIL the gate.

Also P0: rounded/"cleaned" numbers (must be exact or an honest range); any named entity,
quote, or case study absent from sources; any URL that looks constructed rather than
fetched.

Report each: claim — source — confidence — verdict.

---

## STEP 3 — COMPLIANCE (20 pts — roster-driven)

Read the client's row in `singrank-playbook` §5 (ACTIVE CLIENT ROSTER) and check EVERY
constraint listed there — not a hard-coded subset. Any breach = P0. Highlights:
- RCS: byline "SingRank Singapore"; never CaseTrust. ablink: no vehicle prices in content.
- dehall: zero pricing; facts from site PAGES not blog. yescpap: YMYL — every health claim
  sourced; disclaimer present.
- rajawangi/kgteknik: lane locks respected; no income guarantees; no prices → WhatsApp.
- matchdayaffairs: TA03720; live-confirmed fixtures/prices. livinmalaysia: no visa
  guarantees; official MY gov sources.
- Language lock per roster (en-SG / en-MY / id-ID) — the machine pass detects mixing.
- Topic-appropriate disclaimer near the foot (YMYL → explicit professional disclaimer).

---

## STEP 4 — HOOK-GATE + E-E-A-T (10 pts)

- Answer capsule: 50–60 words, fact-first, resolves the title's promise.
- Curiosity loop present AND paid off honestly at the named location (unpaid/misleading
  loop = P0). ≤3 loops, all closed, none in the FAQ.
- ≥1 true micro-story or real data narrative in the Desire zone; ONE CTA, final block,
  never a summary.
- E-E-A-T: experience signals with numbers, expertise (edge cases covered), trust
  (contact, dated facts, real credentials, transparent "as of").

## STEP 5 — GEO EXTRACTION (20 pts, 5-engine)

The machine pass covers structure; verify semantics by sampling 3 sections:
- Direct self-contained answer in the first 60 words under each H2/H3.
- Key claims survive being quoted out of context (pronoun-free).
- Speakable schema on the answer-first paragraphs.
- Time-sensitive/commercial facts carry inline source + date.
- Optional (SingRank MCP): `geo_answerability_score {domain, url}` after publish;
  `score_draft {domain, title, text}` as the winner-profile cross-check (target ≥80).

---

## OUTPUT — QC REPORT (mandatory closing block)

```
=== SINGRANK QC REPORT ===
CLIENT: [name]   ARTICLE: [title / file]
VERDICT: PASS / FAIL   SCORE: [0-100]   ITERATION: [n/3]
MACHINE PASS (qc_check.py): [score]/60 · P0: [...] · P1: [...]
FACTCHECK: [n claims — EXACT x / PARAPHRASE y / NOT-FOUND z]; FABRICATED: [list or none]
COMPLIANCE (roster): [pass, or breaches + fix]   DISCLAIMER: [present / missing]
HOOK-GATE: [capsule / loop paid / story / one CTA]
GEO (5-engine): [capsule / pronoun-free / Speakable / source-on-claim]
SCHEMA: [types found; deprecated flags]
NEXT: [PASS → publish via seo-platforms] or [FAIL → singrank-article-writer, iter n/3]
=== END QC REPORT ===
```

## WHAT THIS SKILL DOES NOT DO

- It does not write or rewrite — it flags with exact fixes; the writer applies them.
- It never invents a verification: cannot confirm a fact or link → NOT-FOUND / BROKEN.
- It never passes a P0.
