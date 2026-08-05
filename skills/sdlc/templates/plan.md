# Plan: <feature name>

- **Spec:** `docs/specs/<slug>.md`
- **Branch:** `feat/<slug>`
- **Reviewed by `tech-lead-reviewer`:** <date + outcome, or "not yet — the phase 4 gate is not passable without this">

## Verified research — REQUIRED, do not delete

Facts this plan depends on, each with the source that proves it. Recall does not count.
Anything unverified goes under *Risks*, never into a task as an assumption.

| Claim | Source | Checked |
|---|---|---|
| <library X v2.3 exposes `foo()` returning a Promise> | <link to the docs page> | <date> |

Spike conclusions land here too — the spike itself lives in scratch and is deleted, the conclusion survives.

## Tasks

Every task must satisfy all four granularity rules, and the slots below exist to prove it:
filling **Test** proves there is one red→green check; filling **Files** proves a fresh-context
subagent can do it; **Depends on** proves nothing unfinished is needed. Cannot fill a slot → the task
is not ready, split it.

### Task 1 — <short name>

- **Covers:** R1
- **Files:** <1–3 paths this touches>
- **Depends on:** nothing | Task N
- **Test (red → green):** <the exact test/command that fails now and passes after>
- **Steps:**
  1. <…>
- **Done when:** the test above is green, the full suite is still green, and it is committed.

### Task 2 — <short name>

- **Covers:** R2
- **Files:** <…>
- **Depends on:** Task 1
- **Test (red → green):** <…>
- **Steps:**
  1. <…>
- **Done when:** <…>

## Task status — REQUIRED, do not delete

The cross-session source of truth. Agent scratch ledgers are git-ignored and vanish; this file is in git.
Tick the moment the task goes green **and is committed** — never in a batch at the end.
**A ticked box with no commit hash counts as not done.** Stopped midway → `WIP + why`.

- [ ] Task 1 — <name> — `<commit>`
- [ ] Task 2 — <name> — `<commit>`

## Rollback

- **Code:** <revert which commits / which tag is the last known good>
- **Data:** <migrations are not undone by a code revert — state the actual data path, or "no schema change">
- **Feature flag:** <flag name to flip, or "none">

## Risks

| Risk | If it happens | Mitigation / trigger to stop |
|---|---|---|
| <…> | <…> | <…> |
