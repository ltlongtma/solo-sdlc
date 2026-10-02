# Session lifecycle

There is no "one phase = one session" rule. One session can run a feature end to end; state lives in git, so a session can die at any moment without losing anything.

## Thin orchestrator

The main session holds only:
- `docs/status.md`, the open spec, and the task list from `check-plan --list`;
- ≤15-line subagent reports and summarized script output.

It never holds large source files, test logs, full reviews or transcripts.

**One fresh subagent per task**, with a brief from `brief-template.md`.

## Subagents

- **Spawn them; don't wait to be asked.** Each phase file says which agent runs when.
- **The author does not grade their own work.** Reviewers are a fresh context (a separate agent), not the same session wearing a different hat.
- No subagent support in the harness → run each agent as a separate headless process, which gives it a fresh context.
- Agent not installed (neither user-level nor in the plugin) → use a general-purpose subagent with an equivalent mandate, spelling the adversarial / break-it mandate out in the brief.

## State is written in the same commit as the code

After every task, the task's own commit also carries:
- the plan's **Task status** line ticked with the commit hash;
- `docs/status.md` updated: `next:` and `waiting-on-human:`.

### Task status belongs in git

`superpowers:subagent-driven-development` keeps a ledger at `.superpowers/sdd/<plan>/progress.md`, but that is **git-ignored scratch**: good for in-session recovery, gone after `git clean -fdx`, unreadable weeks later. The cross-session source of truth is the plan file in git:
- One line per task: `- [x] Task 3 — <task name> — <commit hash>` (not started `- [ ]`; stopped midway records `WIP + why it stopped`).
- Tick it the moment the task goes green and is committed, never in a batch at the end.
- **A ticked box with no commit hash means not done.** Suspect drift → reconcile with `git log --oneline` and trust git over the checkbox.
- Keep using the `.superpowers/` ledger as in-session scratch; the two complement each other.

Git is the source of truth, not the chat: every phase produces a committable artifact (exception: a fresh idea's phases 0–1 live in scratch until GO — see `phase-0-1.md`). Tests and CI are the real status; checkboxes are only a summary.

## When to start a new session

Only when:
- the orchestrator's context passes ~60% **at a task boundary** (never mid-task), or
- the feature has shipped.

Harness compaction is also fine — state is in files, so nothing is lost.

## Resume order

1. `AGENTS.md` (loaded automatically by most harnesses; ≤1500 words).
2. `docs/status.md` → take `next:`.
3. `python3 scripts/sdlc/check-plan.py <plan> --list` (plan path from `docs/status.md`) — prints the task table, then reports ticked tasks whose hash does not resolve and acceptance ids no task covers.
4. Read only the files `next:` needs. Not the backlog, not the full plan.

The repo's `docs/WORKFLOW.md` wins over this skill where they disagree.

**Converge when `check-plan` reports problems** (or the code clearly disagrees with the plan). Do not trust the checkboxes: read the actual code plus `git log`, compare against the open spec and plan, and produce three lists:
- (a) tasks the plan calls done that the code does not have, or implements differently;
- (b) code that exists but the plan never mentioned (scope drift → ADR or spec amendment);
- (c) spec requirements with no task at all.

Resolve each item per `decision-policy.md` (T: fix the plan and record; B — e.g. cutting committed scope: raise a gate), then update the plan and continue. Delegate the wide code read to a `fast` subagent that returns pointers. Skipping converge means redoing finished work, or shipping without work you assumed was done.

## The pipeline loops

When a gate fails, go back instead of pushing forward:
- architecture breaks the spec → back to phase 2 (fix the spec + ADR);
- plan review has BLOCKING → back to phase 4;
- QA / review fails (BLOCKING / CRITICAL) → back to phase 5;
- execution hits the retry ceiling → the escalation ladder in `phase-5-execute.md`; then back to phase 4 (bad plan) or phase 2 (bad spec).

Retro (phase 8) feeds the backlog; the next round starts at phase 0. Any backward step that changes a settled artifact gets an ADR explaining why.
