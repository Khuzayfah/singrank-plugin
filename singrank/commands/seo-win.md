---
description: Run the full SingRank winning pipeline — idea → brief → article → publish → track
argument-hint: [client domain, optional topic/keyword]
---

Run the **singrank-pipeline** skill end-to-end for: **$ARGUMENTS**

1. Read the `singrank-playbook` and `singrank-pipeline` skills first.
2. Execute all 10 stages IN ORDER (0 Baseline → 1 Structure → 2 Discover →
   3 Prioritize → 4 Recon → 5 Brief → 6 Write → 7 Publish → 8 Interlink →
   9 Track). Respect every GATE — a failed gate goes back, not forward.
3. Delegate heavy stages to the specialist agents where useful:
   keyword-strategist (Stage 2–3), geo-analyst (Stage 4/8), article-writer
   (Stage 6), platform-executor (Stage 7–8).
4. Stop for user confirmation at GATE 3 (target list) and GATE 7 (publish).

If no client was given, ask which client first ($ARGUMENTS empty → ask).
