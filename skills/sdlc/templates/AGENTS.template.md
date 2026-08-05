# <project name>

Entry point for whoever shows up next, human or AI. Read this file first, then open the architecture
diagram. Refresh it at every gate — a stale AGENTS.md is worse than none, because it is trusted.

## Where things are

| | |
|---|---|
| Process this project follows | `docs/WORKFLOW.md` |
| The system, drawn | `docs/design/architecture.html` |
| Backlog (where the next round starts) | `docs/backlog.md` |
| Specs · plans · decisions | `docs/specs/` · `docs/plans/` · `docs/decisions/` |
| Runbook (when production is broken) | `docs/runbook.md` |

## Right now

- **Track:** <trivial | feature | subsystem | new-product>
- **Phase in flight:** <N — name>
- **Open spec:** `docs/specs/<slug>.md`
- **Open plan:** `docs/plans/<file>.md` — task status lives in that file, not in a scratch ledger
- **Branch:** `feat/<slug>`
- **Blocked on:** <a human gate? a decision? nothing?>

**Resuming work in flight → converge before writing any code.** Do not trust the plan's checkboxes:
read the code and `git log`, then reconcile. A ticked box with no commit hash counts as not done.

## Commands

```bash
<install>        # e.g. pnpm install
<test>           # the full suite — this is the real status, not the checkboxes
<typecheck>
<build>
<dev>
```

## Conventions

- Branches: `feat/*` `fix/*` `docs/*`. Never commit straight to main.
- Commits: `type(scope): description`.
- Code that departs from the spec is a bug unless an ADR in `docs/decisions/` explains it.
- Technical claims get verified against docs and cited, never recalled.

## Things a newcomer gets wrong here

<Project-specific traps. Fill this in the first time one bites you — it is the highest-value section
in this file and the one always left empty.>

- <…>
