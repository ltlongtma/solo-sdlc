# Phase 4 — Plan

- **Artifact:** `docs/plans/YYYY-MM-DD-<feature>.md` from `docs/templates/plan.md`, with:
  - a **Verified research** section — facts about versions / APIs / library behavior, each with a cited source;
  - a **Task status** section (see `session-lifecycle.md`);
  - per task: `Covers`, `Files`, `Test`, `Verify`, `Tier`, `Risk flags` (format: `artifact-format.md`; tiers: `model-tiers.md`). Tasks list commands + interfaces, not full code.
  - a UI spec needs `Task 0 — Verification harness`.
- **Driven by:** `superpowers:writing-plans`. If the superpowers skills are present, pre-answer their prompts: the execution-choice question is answered "subagent-driven development".
- **Gate (no human approval — `decision-policy.md`, class R):**
  - `python3 scripts/sdlc/check-plan.py docs/plans/<plan>.md` exits 0 (every A-id covered, risk flags ⇒ `Tier: strong`);
  - tasks are small enough (*Task granularity* below);
  - ≥1 review round by agent `tech-lead-reviewer`, including a requirement → task coverage matrix. Fix every BLOCKING finding; only the reviewer who raised it appends `[resolved]` to its line. Still BLOCKING → stay in phase 4.

## Task granularity — decides whether phase 5 survives

Oversized tasks are the number-one reason subagents fail and burn the whole retry budget. Split until **every task satisfies all four**:

1. **One test** — one concrete test / check goes red → green. If you can't name the test, the task isn't clear yet (a different problem from being too big).
2. **One commit** — when done, you can commit and the repo is still green. A task that needs three commits to go green is three tasks.
3. **A fresh-context subagent can do it** — the plan plus 1–3 files is enough; it does not need the whole repo. You must be able to name the files it will touch.
4. **No dependency on unfinished work** — every interface / type it uses was created by an earlier task (`tech-lead-reviewer` audits exactly this).

Any violation → split further. One task = one function / one endpoint / one migration is normal, not over-fragmented.

## Verify technical claims

API / spec / library behavior is verified against docs or web search and cited — never trusted from recall. Write the result into **Verified research** instead of leaving it in chat.

## No vibe-coding

No product code before the plan passes its gate. Until then you may only write artifacts (spec / plan / ADR), read code, and **spike** — an experiment that answers one technical question, lives in scratch, is NEVER committed to source, and is deleted once its conclusion is recorded under Verified research. The trivial track is exempt.

## Acceptance tests first

At the end of phase 4 / start of phase 5, spawn agent `qa-logic` to write the acceptance tests from the spec **before implementation** — one `test.fixme('[A<n>] …')` per A-id. Implementers flip them to `test` as features land; nobody weakens or deletes one to make it pass.
