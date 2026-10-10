# Changelog

## 0.3.1

- Models are the human's choice: new `## Models` table in `docs/preferences.md` (scaffolded with suggested defaults); every spawn passes the model from it, so nothing inherits the session's model by accident; the AI suggests changes, never edits the table. Until the table carries `Confirmed:`, the AI asks once per session without blocking work (not a B gate). Fix-diff re-review defaults to `standard` unless the fix touches a risk flag.
- `integrations.md`: optional `env` for pinning aliases to full IDs and a `CLAUDE_CODE_SUBAGENT_MODEL` fallback. README: that variable sits below frontmatter (Claude Code ≥ 2.1.251), not above it.
- `evidence`: the PR section references the storyboard and MP4 by relative path and is posted with `gh pr edit --attach`, so the recording plays inline in the PR. Repo-blob `.mp4` links only offered a download.

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
