---
description: QC a finished article before publish — blocking gate (score ≥90, zero P0), factcheck, compliance, hook-gate
argument-hint: [article file or paste the article] [client domain]
---

Run the **singrank-qc** skill on: **$ARGUMENTS**

Steps:
1. Machine pass first: `python C:\Users\natur\singrank-plugin\singrank\tools\qc_check.py
   <article.html> --base-url https://<client-domain> --lang <en|id>` — fix or flag every
   P0/P1 it reports.
2. Factcheck every claim against its source with
   `python ...\tools\web_research.py verify <url> "<claim>"` — NOT-FOUND = P0 FABRICATED.
3. Compliance vs the `singrank-playbook` roster row; hook-gate; GEO extraction sample.
4. Close with the `=== SINGRANK QC REPORT ===` block. PASS = score ≥90 AND zero P0;
   FAIL routes back to singrank-article-writer (max 3 iterations, then escalate).

If the article content or client wasn't given, ask for them first.
