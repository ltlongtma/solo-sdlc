---
description: "Phase 6 only — run the QA/review gate: check-gate, then fresh-context reviewers in parallel, fixes by a fresh implementer."
---

Run **only phase 6 (QA / Review)** of the `sdlc` skill on the current branch or PR. The gate is a script, not a statement: only `check-gate` exit 0 passes it.

1. **Contract check first.** Run the full test suite with JSON reporters, then:
   ```
   python3 scripts/sdlc/check-gate.py --spec docs/specs/<slug>.md --reports reports/*.json \
     --ledger docs/qa/ledger.tsv --gates docs/gates.md --reviews docs/reviews --sha "$(git rev-parse HEAD)"
   ```
   If it fails, it lists what is missing (tests, ledger rows, gate answers). Send that list to a **fresh implementer** before any review — never fix it in the main session.

2. **Spawn reviewers in parallel, each in a fresh context:**
   - `tech-lead-reviewer` — the diff, plus requirement→diff coverage against the spec.
   - `qa-logic` — acceptance tests, business rules, money math, multi-screen flows.
   - `qa-ui` — UI specs only: real browser, mockup, axe, console, ledger rows.
   - `security-reviewer` — when the diff touches auth, schema, money, uploads, user input, or a public endpoint. If skipped, say why.

   Each writes `docs/reviews/<date>-<agent>-<slug>.md` in the `review.md` buckets — **Act on**, **Consider**, **Noted**, **Dismissed** (each with a reason) — and returns ≤15 lines. Act on: every `BLOCKING:` line, none dropped or moved for the cap; then up to 5 other items, highest value first; the rest go to Consider. No multi-vendor panel. No subagent support in the harness → run each reviewer as a separate headless process, which gives it a fresh context.

3. **Fix loop.** Send the Act on findings to a **fresh implementer** — never the main session, never the reviewer. The implementer never edits `docs/reviews/`: only the reviewer who raised a finding re-reviews the fix diff and appends `[resolved]` in its review file. After any fix that changes files outside `docs/`, rerun `qa-ui` on a UI spec — ledger rows at the old SHA no longer count. Max 2 rounds. Still unresolved: if it needs the human, add a B item to `docs/gates.md`; otherwise re-plan.

4. **Rerun `check-gate`** with the step 1 command plus `--require-review tech-lead-reviewer --require-review qa-logic`, and `--require-review qa-ui` for a UI spec, `--require-review security-reviewer` when it ran. Never declare a pass without exit 0 — quote its output line. A green gate merges with no sign-off; only B items (prod deploy, money, destructive data ops — see `docs/gates.md`) stop for the human.

Scope: $ARGUMENTS
