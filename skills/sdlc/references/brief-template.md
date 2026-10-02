# Subagent brief template

Every subagent gets one brief. It carries pointers, not content; the subagent reads the files itself.

```
GOAL:        <one sentence — the outcome, not the steps>
SCOPE:       <the files it may touch (1–3 for a plan task)>
CONTEXT:     <pointers only — plan task id, spec path, ADR paths. No pasted file contents.>
ACCEPTANCE:  <the A-ids / checks that must hold when done>
VERIFY:      <the exact command(s) that prove it>
FORBIDDEN:   <files, actions and shortcuts that are off limits — e.g. weakening or deleting an [A<n>] test>
REPORT:      ≤15 lines — PASS | ISSUES | BLOCKED, the commands run with their result, the commit hash.
```

Add for implementers:
- the task's `Tier:`;
- both retry ceilings (3 for the same failure, 5 for the task — see `phase-5-execute.md`). It hands control back at a ceiling and never raises its own.

Add for reviewers:
- write the full review to `docs/reviews/<date>-<agent>-<slug>.md` (format: `docs/templates/review.md`), return only the ≤15-line summary.
