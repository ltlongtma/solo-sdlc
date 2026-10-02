---
description: Reconcile the real codebase against the spec and plan before resuming work in flight.
---

Run the **converge** step of the `sdlc` skill. Trust the code and `git log`, not the plan's checkboxes.

1. Read `docs/status.md`, the open spec (`docs/specs/`) and plan (`docs/plans/`, run `check-plan.py --list`).
2. Read what actually exists: the relevant source, plus `git log --oneline` for the branch.
3. Produce three lists:
   - **(a) Claimed but absent** - tasks marked done where the code is missing or differs. Cite file paths.
   - **(b) Built but unplanned** - scope drift: record an ADR or a spec amendment.
   - **(c) Unbuilt requirements** - spec requirements with no task.
4. A ticked task with no commit hash counts as not done.
5. Reconcile without waiting: update the plan's Task status, record each decision (ADR or spec Clarifications, ending `reverse with:`), update `docs/status.md`, and continue at the correct phase. Only a B item (`decision-policy.md`) stops work.

Scope (optional - a plan file, branch, or feature name): $ARGUMENTS
