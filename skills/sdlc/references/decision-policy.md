# Decision policy — B / T / R

Every decision in the pipeline falls into exactly one class. Only class B stops the work.

## B — synchronous stop (the human answers)

B covers:
- money and pricing;
- spend over the budget envelope;
- GO / NO-GO;
- production deploy;
- destructive data operations;
- legal or customer-facing content;
- cutting committed scope;
- brand.

How to raise a B item:
1. Add it to `docs/gates.md` (template: `docs/templates/gates.md`) with **Options**, a **Default**, and **Blocks:** (the A-ids / tasks / phases it holds up).
2. Set `waiting-on-human:` in `docs/status.md` to the gate id.
3. Stop only the work listed under **Blocks**. Everything else continues on the **Default**.
4. A B item counts as answered only when **Answer** is filled; an acceptance line marked `human-B` is checked by `check-gate` against it.

This is the only place in the pipeline where the AI stops and asks the human. Never walk through a B gate alone.

Human-only work (accounts, billing, pricing, legal, grading a golden set, going live) → list it in the backlog early, and raise its B item as soon as it is known, so it never blocks you at the last minute.

## T — the AI decides and records

Everything that is not B. The AI picks, then records the decision where the next session will find it:
- an ADR in `docs/decisions/NNNN-<slug>.md` (context → decision → consequences), or
- a row in the spec's **Clarifications** section.

Each record ends with `reverse with: <word>` — the one word the human can type to undo it. A decision that stays in chat does not exist: the next session cannot read this conversation.

Diverging from the spec is a bug unless there is an ADR for it.

## R — rubber-stamp approvals are removed

No "approve the plan", "sign off the PR", "confirm the spec" stops. Where an old gate asked for approval, the gate is now a script (`check-spec`, `check-plan`, `check-gate`) plus fresh-context review. A green gate continues without a human.
