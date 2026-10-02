# Plan: Notes

- **Spec:** `tests/fixtures/plan/bad-no-task0/spec.md`
- **Branch:** `feat/notes`

## Tasks

### Task 1 — Add note

- **Covers:** A1
- **Files:** `src/notes.ts`, `src/notes.test.ts`
- **Test (red → green):** `[A1]` test in notes.test.ts
- **Verify:** `npm test -- notes`
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

- [ ] Task 1 — Add note — `<commit>`
- [ ] Task 2 — Delete note — `<commit>`
