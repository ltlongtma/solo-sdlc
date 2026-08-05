---
description: Phase 6 only — run the QA/review gate: tech-lead review, break-it QA, and security review in parallel.
---

Run **only phase 6 (QA / Review)** of the `sdlc` skill on the current branch or PR.

1. Establish the real status first: full test suite, typecheck, build. Report anything red verbatim.
2. Spawn **in parallel**:
   - `tech-lead-reviewer` — review the code/diff, including a requirement→diff coverage check against the spec.
   - `qa-breaker` — attack the feature and score it against the spec's Acceptance checklist.
   - `security-reviewer` — **only if** the diff touches auth/sessions, schema/RLS/migrations, money/webhooks, user input/uploads, fetching external URLs, or public endpoints. Always spawn it for high-risk or new-product work. If you skip it, say why.
3. Collect the findings, deduplicate, and present them grouped: BLOCKING / CRITICAL first, then the rest.
4. Fix what needs fixing (you are the main session — the agents only report).
5. State plainly whether the gate passes: CI green + reviews confirmed + acceptance checklist passing + no CRITICAL/HIGH open + every spec divergence covered by an ADR. Then ask the user for sign-off — do not merge on your own.

Scope: $ARGUMENTS
