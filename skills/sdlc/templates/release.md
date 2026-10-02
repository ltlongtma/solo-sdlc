# Release <version> — <YYYY-MM-DD>

- **Tag:** <…>
- **Spec / plan:** <links>
- **Track:** <…>

## What shipped

- <…>

## Gate evidence

The phase 7 gate is not "it looks fine" — these lines are the proof.

| Check | Result |
|---|---|
| CI green on the merge commit | <link / commit> |
| Acceptance checklist passing | <link to spec + who verified> |
| `tech-lead-reviewer` | <clean / findings fixed> |
| `qa-logic` | <bugs found + fixed> |
| `qa-ui` (UI specs) | <ledger rows live-ui-verified at the release sha> |
| `security-reviewer` (if the diff needed it) | <no CRITICAL/HIGH open, or why it was skipped> |
| Architecture diagram matches reality | <updated / no structural change> |
| Runbook exists and covers this change | <…> |

## Migrations

- <what ran, in which order, and whether it is reversible — or "none">

## Post-deploy smoke test

- [ ] <the main user flow, run against production, with the result>
- [ ] <…>

## Rollback plan

- <the exact command, and the tag to roll back to>

## Known issues shipped knowingly

- <…> — <why it was acceptable to ship, and the backlog item that fixes it>
