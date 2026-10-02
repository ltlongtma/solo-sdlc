---
description: Phase 3 only - get 2-3 architecture/stack options with trade-offs and record the decision as an ADR.
---

Run **only phase 3 (Architecture)** of the `sdlc` skill. Do not write product code.

1. Read the spec (`docs/specs/`), the validation report (`docs/business/`) if present, and the repo structure if there is code. No spec at all: run phase 2 first.
2. Spawn the `solution-architect` agent. It returns 2-3 options with upsides, downsides, monthly cost (with arithmetic), one-person operability, lock-in, a recommendation, and draft ADRs.
3. Choose the option that fits the spec and budget, and record it in `docs/decisions/NNNN-<slug>.md` ending with `reverse with: <word>`. Update the spec's architecture section.
4. Exception: if the choice commits spend over the budget envelope, it is a **B item** - raise it in `docs/gates.md` with a default and stop only what it blocks.
5. Invoke the `archify` skill to produce `docs/design/architecture.html`; if it is not installed, write the diagram by hand.

The architect proposes and is never the reviewer - the resulting plan still goes through `tech-lead-reviewer` at phase 4.

Context: $ARGUMENTS
