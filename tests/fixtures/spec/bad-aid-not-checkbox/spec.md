# Spec: Task board

- **Design source:** designs/board.fig
- **UI:** yes

## Requirements

| ID | Requirement | Priority |
|---|---|---|
| R1 | User can add a task | must |
| R2 | Empty title is rejected | must |

## Acceptance checklist — REQUIRED, do not delete

- [ ] **A1** (R1) — add "x", list shows "x" — Verify by: e2e
* [x] **A2** (R2) — empty title returns 400 — Verify by: unit

## UI states

| Screen | State | Viewport | Mockup ref |
|---|---|---|---|
| Board | empty | 375x812 | designs/board.fig#empty |
