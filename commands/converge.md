---
description: Reconcile the real codebase against the spec and plan before resuming work in flight.
---

Run the **converge** step of the `sdlc` skill. Do not trust the plan's checkboxes — trust the code and `git log`.

1. Read the open spec (`docs/specs/`) and plan (`docs/plans/`), including the plan's "Task status" section.
2. Read what actually exists: the relevant source, plus `git log --oneline` for the branch.
3. Produce three lists:
   - **(a) Claimed but absent** — tasks the plan marks done where the code is missing or implements something different. Cite file paths.
   - **(b) Built but unplanned** — code that exists but no task covered (scope drift → needs an ADR or a spec amendment).
   - **(c) Unbuilt requirements** — spec requirements with no task at all.
4. Also flag any ticked task whose line has no commit hash — by the skill's rules that counts as not done until git proves otherwise.
5. Present all three lists to the user and ask what to do. Only after they decide: update the plan's Task status section, write any needed ADR, and resume at the correct phase.

Scope (optional — a plan file, branch, or feature name): $ARGUMENTS
