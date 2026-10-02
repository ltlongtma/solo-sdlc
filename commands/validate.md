---
description: Phase 1 only - adversarially validate a product idea before committing any build effort.
---

Run **only phase 1 (Validate)** of the `sdlc` skill on the idea below. Do not write a spec, create a repo, or touch code.

1. State the idea in one paragraph (problem, who has it, rough solution). Fill gaps with stated assumptions; if it cannot be stated at all, state your assumptions anyway, record them, and continue.
2. Spawn the `product-critic` agent with that paragraph plus any constraints given (budget, timeline, audience).
3. Relay the verdict and its conditions **verbatim** - never soften a NO-GO.
4. Write the report to `docs/business/<idea>-validation.md` if a repo exists; otherwise keep it in a scratch directory and report the path. A NO-GO should not leave a repo behind.
5. GO / NO-GO is a **B item**: add it to `docs/gates.md` (before a repo exists: `<scratch>/gates.md`, copied to `docs/gates.md` by scaffold after GO; format: `docs/templates/gates.md`) with options, a default, and what it blocks, and stop the build work it blocks. Do not continue to the spec phase until its Answer is filled.

Idea: $ARGUMENTS
