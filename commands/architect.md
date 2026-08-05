---
description: Phase 3 only — get 2-3 architecture/stack options with trade-offs and draft ADRs.
---

Run **only phase 3 (Architecture)** of the `sdlc` skill. Do not write product code.

1. Read the inputs the architect needs: the spec (`docs/specs/`), the validation report (`docs/business/`) if present, and the current repo structure if there is code. If there is no spec at all, say so — architecture without an agreed WHAT is guesswork; offer to run phase 2 first.
2. Spawn the `solution-architect` agent. It must return 2–3 options with upsides, downsides, monthly cost (with arithmetic), one-person operability, lock-in, plus a recommendation and draft ADRs.
3. Present the options to the user and discuss. **Do not pick for them.**
4. Once they decide: commit the ADR to `docs/decisions/NNNN-<slug>.md` and update the spec's architecture section.
5. Then prompt the user to run `/html-diagram` themselves to produce `docs/design/architecture.html` from the high-level design (that skill blocks model invocation). If it isn't installed, offer to write the diagram by hand to the standard in the skill.

Remember: the architect proposes and is never the reviewer — whatever plan comes out of this still goes through `tech-lead-reviewer` at phase 4.

Context: $ARGUMENTS
