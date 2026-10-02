---
description: "Phase 6 only — run the QA/review gate: check-gate, then fresh-context reviewers in parallel, fixes by a fresh implementer."
---

Run **only phase 6 (QA / Review)** of the `sdlc` skill on the current branch or PR. The gate is a script, not a statement: only `check-gate` exit 0 passes it.

1. **Contract check first.** Run the full test suite with JSON reporters, then:
   ```
   python3 scripts/sdlc/check-gate.py --spec docs/specs/<slug>.md --reports reports/*.json \
     --ledger docs/qa/ledger.tsv --gates docs/gates.md --reviews docs/reviews --sha "$(git rev-parse HEAD)"
   ```
   If it fails, it lists what is missing (tests, ledger rows, gate answers). Fix that before any review.

2. **Spawn reviewers in parallel, each in a fresh context:**
   - `tech-lead-reviewer` — the diff, plus requirement→diff coverage against the spec.
   - `qa-logic` — acceptance tests, business rules, money math, multi-screen flows.
   - `qa-ui` — UI specs only: real browser, mockup, axe, console, ledger rows.
   - `security-reviewer` — when the diff touches auth, schema, money, uploads, user input, or a public endpoint. If skipped, say why.

   Each writes `docs/reviews/<date>-<agent>-<slug>.md` in the `review.md` buckets — **Act on** (≤5, must-fix lines marked `BLOCKING:`), **Consider**, **Noted**, **Dismissed** (each with a reason) — and returns ≤15 lines. No multi-vendor panel. Without subagents, run each reviewer as a separate headless process.

3. **Fix loop.** Send the Act on findings to a **fresh implementer** — never the main session, never the reviewer. The reviewer who raised a finding re-reviews the fix diff and marks it `[resolved]` in its review file. Max 2 rounds. Still unresolved: if it needs the human, add a B item to `docs/gates.md`; otherwise re-plan.

4. **Rerun `check-gate`.** Never declare a pass without exit 0 — quote its output line. A green gate merges with no sign-off; only B items (prod deploy, money, destructive data ops — see `docs/gates.md`) stop for the human.

Scope: $ARGUMENTS
