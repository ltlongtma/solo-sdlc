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

Tasks list commands + interfaces, not full code.

Every task must satisfy all four granularity rules, and the slots below exist to prove it:
filling **Test** proves there is one red→green check; filling **Files** proves a fresh-context
subagent can do it; **Depends on** proves nothing unfinished is needed. Cannot fill a slot → the task
is not ready, split it.

### Task 0 — Verification harness

Required when the spec says **UI: yes**; otherwise delete it.

- **Covers:** harness
- **Files:** <playwright config, seed script, auth-state setup — 1–3 paths>
- **Test (red → green):** <smoke test that opens the app, runs axe, and fails now>
- **Verify:** <exact command, e.g. the e2e smoke run>
- **Tier:** standard
- **Risk flags:** none
- **Setup:** Playwright + axe, seed data, test users (one per role), stored auth state.

### Task 1 — <short name>

- **Covers:** A1
- **Files:** <1–3 paths this touches>
- **Depends on:** nothing | Task N
- **Test (red → green):** <the `[A1]` test that fails now and passes after>
- **Verify:** <exact command>
- **Tier:** strong | standard | fast
- **Risk flags:** none | money, auth, migration, concurrency, public-interface (any flag ⇒ Tier: strong)
- **Steps:**
  1. <command or interface, not code>
- **Done when:** the test above is green, the full suite is still green, and it is committed.

### Task 2 — <short name>

- **Covers:** A2, A3
- **Files:** <…>
- **Depends on:** Task 1
- **Test (red → green):** <…>
- **Verify:** <…>
- **Tier:** <…>
- **Risk flags:** none
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
