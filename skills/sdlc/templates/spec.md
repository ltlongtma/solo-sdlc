# Spec: <feature name>

- **Track:** trivial | feature | subsystem/high-risk | new product
- **UI:** yes | no
- **Design source:** <path or url | none>
- **Status:** draft | clarifying | agreed | superseded by <link>
- **Plan:** `docs/plans/<YYYY-MM-DD-slug>.md` (once phase 4 starts)

## Problem

<What hurts today, for whom, and what it costs them. Not the solution.>

## Requirements

Every requirement gets an ID — `tech-lead-reviewer` builds its requirement→task matrix from these,
so an unnumbered requirement is a requirement that silently gets no task.

| ID | Requirement | Priority |
|---|---|---|
| R1 | <observable behavior, not implementation> | must |
| R2 | <…> | must |
| R3 | <…> | should |

## Out of scope

<What this round deliberately does NOT do. Prevents scope drift being mistaken for a missing requirement.>

- <…>

## Acceptance checklist — REQUIRED, do not delete

Unit tests for prose: every line must be checkable by someone who did not write the code.
"Works well" is not checkable. "Returns 400 with `{error: "…"}` for an empty title" is.
`qa-logic` (and `qa-ui` for UI specs) score the feature against exactly this list, so a vague line here becomes an unverifiable gate at phase 6.

Each line has a unique A-id, the requirement it proves, and exactly one `Verify by:` word:

- `e2e` — a browser/end-to-end test drives the real UI or API.
- `integration` — a test across real components (DB, HTTP handler), no browser.
- `unit` — a pure-logic test.
- `human-B` — only the human can judge it (taste, money, brand); needs a gate block in `docs/gates.md` listing this A-id under `Blocks:`.

Test titles must contain `[A<n>]` (e.g. `test('[A3] rejects empty title', …)`) so a test is traceable to its acceptance line.

- [ ] **A1** (R1) — <exact input and exact expected output> — Verify by: e2e
- [ ] **A2** (R2) — <…> — Verify by: integration
- [ ] **A3** (R3) — <…> — Verify by: unit

## UI states

Required when **UI: yes**. One row per screen × state; states: loading, empty, error, success.
Viewports: 360 (mobile) and 1440 (desktop). Mockup ref points into the design source.

| Screen | State | Viewport | Mockup ref |
|---|---|---|---|
| <screen> | loading | 360 | <frame / path> |
| <screen> | empty | 1440 | <frame / path> |
| <screen> | error | 360 | <frame / path> |
| <screen> | success | 1440 | <frame / path> |

## Clarifications — REQUIRED, do not delete

Phase 2.5 lands here. One question, one answer, per line. An answer that stays in chat does not exist:
the next session cannot read this conversation.

| # | Question | Answer | Affects |
|---|---|---|---|
| Q1 | <…> | <…> | R2 |

## Architecture

Filled at phase 3 (or left as "n/a — no architectural impact" for a feature that touches none).

- **Decision:** <chosen approach> — see ADR `docs/decisions/<NNNN-slug>.md`
- **Components touched:** <…>
- **Deliberate YAGNI:** <what is knowingly not solved now, and why that is safe at this stage>

## Open questions

<Anything still unresolved. Empty is the goal before the phase 2 gate; anything left here must be
harmless to the plan, otherwise it belongs in Clarifications.>

- <…>
