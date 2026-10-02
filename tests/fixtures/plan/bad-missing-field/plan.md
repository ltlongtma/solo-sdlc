# Plan: Notes

- **Spec:** `tests/fixtures/plan/bad-missing-field/spec.md`
- **Branch:** `feat/notes`

## Tasks

### Task 0 — Verification harness

- **Covers:** harness
- **Files:** `e2e/setup.ts`
- **Test (red → green):** `npm run e2e` smoke fails, then passes
- **Verify:** `npm run e2e -- smoke`
- **Tier:** standard
- **Risk flags:** none

### Task 1 — Add note

- **Covers:** A1
- **Files:** `src/notes.ts`, `src/notes.test.ts`
- **Test (red → green):** `[A1]` test in notes.test.ts
- **Tier:** standard
- **Risk flags:** none

### Task 2 — Delete note

- **Covers:** A2
- **Files:** `src/notes.ts`
- **Test (red → green):** `[A2]` test in notes.test.ts
- **Verify:** `npm test -- notes`
- **Tier:** strong
- **Risk flags:** data-loss

## Task status

- [x] Task 0 — Verification harness — `abc1234`
- [ ] Task 1 — Add note — `<commit>`
- [ ] Task 2 — Delete note — `<commit>`
