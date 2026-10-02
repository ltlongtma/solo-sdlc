# Phase 7 — Release

- **Artifact:** merge to main + tag + `docs/releases/*` + an incident runbook `docs/runbook.md` (created / updated from the validation's risk section plus what deploying actually taught you).
- **Driven by:** `/ship`, `/land-and-deploy` (if installed); otherwise by hand to the same artifacts.
- **Gate:**
  - post-deploy smoke test;
  - rollback plan;
  - runbook exists;
  - architecture diagram updated if this round changed the structure (`phase-3-arch.md`; the diagram check script in CI, if the project has one).
- **Production deploy is a B gate** (`decision-policy.md`): the human pushes the button. Merging a green PR is not.

## Go-to-market

Not a phase the AI drives. On the new-product track, phase 7 surfaces the human-only items already in the backlog — final pricing, the channel for the first customers, landing page and marketing — as B items (drive with `minimalist-entrepreneur:pricing` / `first-customers` / `marketing-plan` if installed).
