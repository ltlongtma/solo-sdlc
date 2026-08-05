# Spec: <feature name>

- **Track:** trivial | feature | subsystem/high-risk | new product
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
`qa-breaker` scores the feature against exactly this list, so a vague line here becomes an unverifiable gate at phase 6.

- [ ] **R1** — <how to check it, with the exact input and the exact expected output>
- [ ] **R2** — <…>
- [ ] **R3** — <…>

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
