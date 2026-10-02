# Phase 3 — Architecture

Runs on the new-product and subsystem tracks, and for anything touching architecture.

- **Artifact:** ADRs in `docs/decisions/` + an architecture section in the spec + `docs/design/architecture.html`.
- **Driven by:** agent `solution-architect` (HOW — 2–3 options with trade-offs; inputs are the spec plus business constraints from validation).
- **Decision:** the stack and architecture choice is T — pick the option, record it in an ADR with the trade-offs and `reverse with: <word>`. It becomes B only when it implies spend over the budget envelope or another B class (`decision-policy.md`).
- **Gate:** stack and architecture chosen, trade-offs recorded in an ADR. **If the architecture breaks the spec (infeasible / too expensive) → go back and fix the spec + write an ADR; never drift silently.**
- The architect PROPOSES and is never the reviewer: the plan that comes out of this still goes through `tech-lead-reviewer` at phase 4.

## Living architecture diagram — the onboarding document

- **Artifact:** `docs/design/architecture.html` — one self-contained HTML file (no external dependencies), committed.
- **Created when:** the architecture is first settled (end of phase 3, from `solution-architect`'s high-level design; projects that skip phase 3 create it at the end of phase 2).
- **Updated when:** any round adds, removes or moves a component — checked at the phase 7 gate. Releasing with a diagram that contradicts reality means the gate is not passed.
- **Automate the check (recommended):** a small project script (e.g. `scripts/check-architecture-diagram.*`) that reconciles both directions — (a) every path a diagram node points at still exists; (b) every real top-level directory (main app / package / module) has a node. Run it in CI on every PR; a failure fails the phase 7 gate. The script is a project artifact, not part of this skill.
- **Content standard:** full-screen interactive SVG; every node is a REAL thing in the repo (directory / file / service); clicking one opens a panel with *what it does + why it lives there + related ADRs*; the main flows (data pipeline, user request, document lifecycle, CI) can be highlighted / animated from chips; pan + zoom + dark mode; node labels match real names, so a newcomer maps the diagram onto the directory tree immediately.
- **How to build it:** invoke the `archify` skill ([tt-a1i/archify](https://github.com/tt-a1i/archify)) directly; if it isn't installed, suggest `npx skills add tt-a1i/archify --skill archify`. If it can't be installed, write the file to the standard above.
- **Its role:** the primary onboarding document for whoever (human or AI) shows up next — `AGENTS.md` says where to resume, the diagram explains the system in five minutes.
