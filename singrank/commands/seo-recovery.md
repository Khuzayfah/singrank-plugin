---
description: Diagnose a ranking/traffic drop and build a recovery plan (SDS + RPS scored)
argument-hint: [client domain, optional page/keyword that dropped]
---

Launch the **ranking-recovery** agent for: **$ARGUMENTS**

The agent must first prove the drop is statistically real (SDS ≥ 2.0 — if
<1.65 report "noise, do not act" and stop), correlate with `algo_events`,
classify the cause with ≥2 corroborating signals, compute RPS per dropped
page, and return a Priority-ordered recovery plan with expected recovered
clicks.

If no client was given, ask which client first.
