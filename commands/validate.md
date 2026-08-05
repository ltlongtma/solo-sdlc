---
description: Phase 1 only — adversarially validate a product idea before committing any build effort.
---

Run **only phase 1 (Validate)** of the `sdlc` skill on the idea below. Do not write a spec, do not create a repo, do not touch code.

1. If the idea is too vague for validation, ask questions until you can state it in one paragraph: the problem, who has it, and the rough solution. That is all `product-critic` needs — do not keep refining past that point.
2. Spawn the `product-critic` agent with that paragraph plus any constraints the user gave (budget, timeline, existing audience).
3. Relay the verdict and its conditions **verbatim** — never soften a NO-GO.
4. Write the report to `docs/business/<idea>-validation.md` if a repo exists; otherwise keep it in a scratch directory and tell the user the path. A repo is the artifact of deciding to BUILD — a NO-GO should not leave one behind.
5. End by asking the user for the GO / NO-GO decision. Do not continue to the spec phase on your own.

Idea: $ARGUMENTS
