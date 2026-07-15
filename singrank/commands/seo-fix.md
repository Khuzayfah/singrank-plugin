---
description: Execute an approved fix on a Wix/Shopify client site (draft-first, never delete)
argument-hint: [client domain + what to change, e.g. "saffrons.com.sg update meta on /catering"]
---

Launch the **platform-executor** agent for: **$ARGUMENTS**

The agent must load the `singrank-playbook` client roster (constraints are
LAW: ablink draft theme 183046078779 + key check, RCS >30KB snippet rule,
saffrons `global.title_tag` metafields, pullupstand meta-only, Wix
`CallWixSiteAPI` + UPDATE_PUBLISH, rajawangi = Squarespace no-API, schema at
theme level), do a READ before every WRITE, verify after, keep everything as
draft unless approval is explicit, NEVER delete anything, return a full
before/after execution log, and close with
`log_experiment {url, changes}` (SingRank System) so `experiment_results`
can verify the fix actually worked.

If the change to make is ambiguous, list what it plans to do and get
confirmation BEFORE the first mutation.
