# Phase 5 — Execute

- **Artifact:** code + commits on a `feat/*` branch.
- **Driven by:** `superpowers:subagent-driven-development` (preferred) or `superpowers:executing-plans`. If the superpowers skills are present, the `writing-plans` execution choice is already answered: subagent-driven development. Several subagents in parallel → give each its own worktree (`superpowers:using-git-worktrees`) so they don't collide.
- **One fresh subagent per task**, briefed with `brief-template.md`. Model: the task's `Tier:` (`model-tiers.md`); with subagent-driven-development present, follow its "Model Selection" section.
- **Per task:** the `[A<n>]` test red → green → commit. The same commit ticks the plan's Task status with the hash and updates `docs/status.md` (`session-lifecycle.md`).

## Branches and commits

Branches are `feat/*`, `fix/*`, `docs/*`; never commit straight to main. Commits read `type(scope): description`.

## Divergence

Diverging from the spec is a bug unless there is an ADR in `docs/decisions/NNNN-<slug>.md` (context → decision → consequences).

## Retry ceilings — no infinite loops

The ceiling is a backstop; the real stop signal is **lack of progress**, not hitting a count.

- **Tier 1 — the SAME failure (tight loop): 3 attempts max.** Missing the same failure three times means you don't understand the cause. Another attempt piles code around something you don't understand. After 3, CHANGE approach (re-read the spec / plan, add logging, shrink the repro); do not keep patching blind.
- **Tier 2 — the whole task (different failures in sequence): 5 attempts max**, and each must be a NEW failure (real progress). Out of attempts, or the same failure returns → stop, revert to the last green commit (never leave half-done code), and write a report: which test fails, what was tried, what you suspect.
- Every implementer gets the task plus both ceilings in its brief; at a ceiling it hands control back and NEVER raises its own ceiling.
- Stop earlier if fixing A breaks B, or if the task needs files outside its scope → suspect the plan / spec and go back to the matching gate.

## Escalation after a ceiling

1. One fresh implementer, one tier up (the only mid-task model change — `model-tiers.md`).
2. Still failing → `tech-lead-reviewer` re-plans or splits the task (back to phase 4).
3. The human only if the spec or a B item must change — raise it in `docs/gates.md`.
