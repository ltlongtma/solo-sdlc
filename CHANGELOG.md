# Changelog

## 0.3.0

- Artifact-first, harness-agnostic: contract (files + check scripts), instruction (router skill + per-phase references), adapter (agent frontmatter, commands, hooks).
- Machine gate: `check-spec`, `check-plan`, `check-gate` installed by `scaffold.sh`; CI `gate` job (make it a required check); `.githooks/pre-push`. Plan approval and PR sign-off removed.
- B/T/R decision policy: only B items (money-class) stop the AI; others are decided and logged with `reverse with:`.
- Model tiers (`strong` / `standard` / `fast`) with per-task `Tier:` and risk flags; per-harness mapping in `integrations.md`.
- Agents: `qa-breaker` split into `qa-logic` and `qa-ui`; six agents total; reviewer output contract.
- New `evidence` skill: captioned MP4, storyboard PNG, state trace, PR section.
- `sdlc` skill cut to a router; phase detail moved to `references/`; resume via `docs/status.md`; no "one phase = one session".
- Optional SessionStart and Stop hooks driven by `docs/status.md`.
- Upgrading: see README, "Upgrading from 0.2".
