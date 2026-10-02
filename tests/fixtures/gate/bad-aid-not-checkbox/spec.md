# Spec — Todo list

- **Design source:** `docs/design/todo.png`
- **UI:** yes

## Requirements

| ID | Requirement |
|----|-------------|
| R1 | Users can add a todo |
| R2 | Titles are validated |

## Acceptance

- [ ] **A1** (R1) — Adding a todo shows it at the top of the list — Verify by: e2e
- [ ] **A2** (R2) — Empty titles are rejected — Verify by: unit
* [ ] **A3** (R1) — POST /todos persists the todo — Verify by: integration
- [ ] **A4** (R1) — Free plan allows at most 50 todos — Verify by: human-B

## UI states

| Screen | State | Viewport | Mockup ref |
|--------|-------|----------|------------|
| Todo list | empty | 390x844 | docs/design/todo.png#empty |
