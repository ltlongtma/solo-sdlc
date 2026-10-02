# Phase 6 — QA / Review

**Follow `commands/gate.md`.** It is the procedure: `check-gate` first, reviewers in parallel, fixes by a fresh implementer, re-review by the reviewer who raised the finding, `check-gate` exit 0 to pass. It is not repeated here.

- **Artifact:** PR + review files in `docs/reviews/` + `docs/qa/ledger.tsv` (UI specs) + an ADR for every place the code diverges from the spec.
- **Reviewers (fresh context each):**
  - `tech-lead-reviewer` — code / PR review against the spec.
  - `qa-logic` — break the logic, scored against the spec's acceptance checklist.
  - `qa-ui` — UI specs: live browser at 360 / 1440 px vs the mockup, axe, console.
  - `security-reviewer` — when the diff touches auth / session · schema / RLS / migrations · money / webhooks · user input / uploads · fetching external URLs · public endpoints. Always on the high-risk and new-product tracks. Unresolved CRITICAL / HIGH means the gate is not passed.
- **Gate:** `check-gate` exits 0 (tests, ledger, required reviews, no unresolved BLOCKING) and every divergence has an ADR. No sign-off — only B items in `docs/gates.md` stop for the human.
- Fails → back to phase 5 (`session-lifecycle.md`, *The pipeline loops*).
