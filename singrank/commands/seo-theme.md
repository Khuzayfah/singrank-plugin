---
description: Edit or push Shopify theme/Liquid code — sections, schema, JSON templates, theme files
argument-hint: [client domain + what to change, e.g. "RCS add FAQ section to article template"]
---

Launch the **shopify-theme-engineer** agent for: **$ARGUMENTS**

The agent must load `singrank-playbook` (client roster) and the
`shopify-theme-liquid` skill, confirm current theme roles via a live
`themes` query (never trust a remembered theme ID's role), verify any
mutation beyond `themeFilesUpsert`/`themeFilesDelete` via
`graphql_schema` → `validate_graphql_codeblocks` before executing, use the
gist→URL path for files >~20-30KB, never touch a MAIN/published theme
experimentally, and never publish without explicit approval.

If the change is ambiguous or touches a live theme, confirm the plan with
the user BEFORE the first write.
