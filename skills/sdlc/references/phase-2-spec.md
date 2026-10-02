# Phase 2 — Spec, and 2.5 — Clarify

## Phase 2 — Spec

- **Artifact:** `docs/specs/<feature>.md` from `docs/templates/spec.md`, with an **Acceptance checklist** — every requirement measurable and checkable ("unit tests for prose"). Format: `artifact-format.md`.
  - Requirements carry `R<n>`; acceptance lines carry `**A<n>**` and `Verify by: e2e|integration|unit|human-B`.
  - A UI spec (`UI: yes` or `Design source:` set) fills the **UI states** table.
- **Driven by:** a solution-level brainstorm (product: WHAT — requirements, not HOW) via `superpowers:brainstorming` if available.
- **Gate:** problem and approach are clear, trade-offs are written down, and `python3 scripts/sdlc/check-spec.py docs/specs/<feature>.md` exits 0.

## Phase 2.5 — Clarify

- **Artifact:** the spec's **Clarifications** section (question → answer, one per row).
- Sweep the spec for coverage gaps and ambiguity.
  - **T** ambiguity → the AI picks the answer and records it as a Clarifications row ending `reverse with: <word>`.
  - **B** ambiguity (money, scope cut, legal, brand… — see `decision-policy.md`) → a gate in `docs/gates.md`; only the work it blocks waits.
- **Gate:** nothing ambiguous still blocks the plan; **answers are committed into the spec, not left in chat.**

If the architecture later proves the spec infeasible or too expensive → back here to fix the spec, with an ADR.
