# <project name>

Entry point for whoever shows up next, human or AI.

**Resume order:** this file → `docs/status.md` (current state) → `python3 scripts/sdlc/check-plan.py docs/plans/<plan>.md --list` (plan path from `docs/status.md`; converge if it reports problems).
Do not trust plan checkboxes: a ticked task with no commit hash counts as not done.

## Invariants

- Branches `feat/*` `fix/*` `docs/*`; never commit straight to main. Commits: `type(scope): description`.
- Diverging from the spec is a bug unless an ADR in `docs/decisions/` says otherwise.
- Only B items (`docs/gates.md`) stop for the human; everything else is decided and recorded.
- Technical claims get verified against docs and cited, never recalled.
- Reviews are done by a separate fresh-context agent, never by the author.

## Where things are

| | |
|---|---|
| Current state, in-flight work, waiting-on-human | `docs/status.md` |
| Deviations from the standard process | `docs/WORKFLOW.md` |
| The system, drawn | `docs/design/architecture.html` |
| Backlog · specs · plans · decisions | `docs/backlog.md` · `docs/specs/` · `docs/plans/` · `docs/decisions/` |
| Runbook (when production is broken) | `docs/runbook.md` |

## Commands

```bash
<install>        # e.g. pnpm install
<test>           # the full suite — this is the real status, not the checkboxes
<typecheck>
<build>
<dev>
python3 scripts/sdlc/check-plan.py docs/plans/<plan>.md --list   # task table, then the plan checks (plan path from docs/status.md)
python3 scripts/sdlc/check-spec.py docs/specs/<slug>.md    # spec gate
python3 scripts/sdlc/check-plan.py docs/plans/<file>.md    # plan gate
python3 scripts/sdlc/check-gate.py --spec <spec> --reports <json...> --reviews docs/reviews/   # QA gate (see commands/gate.md)
```

## Things a newcomer gets wrong here

<Project-specific traps. Fill this in the first time one bites you — it is the highest-value section
in this file and the one always left empty.>

- <…>
