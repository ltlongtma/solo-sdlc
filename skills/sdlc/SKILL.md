---
name: sdlc
description: Use when a solo founder working with AI has a new product or feature idea, wants to brainstorm or validate a startup idea, starts a new project, says "run the SDLC" / "take this from idea to ship" / "validate my idea" / "critique this idea", or wants to resume an existing project by the process.
---

# SDLC — one founder + AI

A 9-phase pipeline. The AI does the work and decides most things; the human answers only B items. Gates are scripts, not statements. This file is a router — read the reference for the phase you are in, not all of them.

## When invoked

1. **Resuming a repo** → follow the resume order in [session-lifecycle.md](references/session-lifecycle.md): `AGENTS.md` → `docs/status.md` (`next:`) → `python3 scripts/sdlc/check-plan.py <plan> --list` (plan path from `docs/status.md`). Converge when it reports problems. The repo's `docs/WORKFLOW.md` wins over this skill where they disagree.
2. **Fresh idea, no repo** → phases 0–1 in scratch; no `git init` until GO. See [phase-0-1.md](references/phase-0-1.md).
3. **Repo without the process** → run `scaffold.sh` (idempotent), then enter at the real phase. See [phase-0-1.md](references/phase-0-1.md#scaffold).
4. **Any repo** → if `docs/preferences.md` has no confirmed `## Models` table, ask the human once to pick models; keep working on the suggested defaults ([model-tiers.md](references/model-tiers.md#every-spawn-names-its-model--the-human-picks-it)).

## Decision policy

Full rules: [decision-policy.md](references/decision-policy.md).

- **B — synchronous stop:** money, pricing, spend over budget, GO/NO-GO, prod deploy, destructive data ops, legal or customer-facing content, cutting committed scope, brand. Write it to `docs/gates.md` with options, a default and `blocks:`; only blocked work waits.
- **T — the AI decides** and records it in an ADR or the spec's Clarifications with `reverse with: <word>`.
- **R — rubber-stamp approvals are removed.** No plan approval, no PR sign-off.

Stop and ask the human only at a B gate. (The one-time model question is asked without stopping.)

## Phases

| # | Phase | Read | Gate |
|---|---|---|---|
| 0 | Triage, choose track | [phase-0-1.md](references/phase-0-1.md) | backlog entry, track recorded |
| 1 | Validate (new product) | [phase-0-1.md](references/phase-0-1.md) | `product-critic` report → **B: GO/NO-GO** |
| 2 / 2.5 | Spec, Clarify | [phase-2-spec.md](references/phase-2-spec.md) | `check-spec` exit 0 |
| 3 | Architecture | [phase-3-arch.md](references/phase-3-arch.md) | ADR + `docs/design/architecture.html` |
| 4 | Plan | [phase-4-plan.md](references/phase-4-plan.md) | `check-plan` exit 0 + `tech-lead-reviewer`, no unresolved BLOCKING |
| 5 | Execute | [phase-5-execute.md](references/phase-5-execute.md) | per task: `[A<n>]` red → green, commit, plan ticked with hash |
| 6 | QA / Review | [phase-6-verify.md](references/phase-6-verify.md) → `commands/gate.md` | `check-gate` exit 0 |
| 7 | Release | [phase-7-release.md](references/phase-7-release.md) | smoke + rollback + runbook; **B: prod deploy** |
| 8 | Retro | [phase-8-retro.md](references/phase-8-retro.md) | lessons written |

Tracks (trivial / feature / subsystem / new product) decide which phases run — see [phase-0-1.md](references/phase-0-1.md#four-rigor-tracks).

## Gate = script

A gate passes when its script exits 0, never because a session says so:
- `scripts/sdlc/check-spec.py` — spec IDs, `Verify by`, UI states.
- `scripts/sdlc/check-plan.py` — task fields, coverage of every A-id, risk flags ⇒ `Tier: strong`, ticked hashes resolve.
- `scripts/sdlc/check-gate.py` — passing `[A<n>]` tests, ledger, B answers, no unresolved BLOCKING. Required in CI.

Artifact formats the scripts parse: [artifact-format.md](references/artifact-format.md).

## How work runs

- **Superpowers prompts are pre-answered:** `brainstorming` design/spec approvals are approved by policy unless the work contains a B item (phases 0 and 2).
- **Thin orchestrator, one fresh subagent per task**, briefed with [brief-template.md](references/brief-template.md). Reports ≤15 lines.
- **State in the same commit as the code:** plan tick with hash + `docs/status.md` (`next:`, `waiting-on-human:`). No "one phase = one session" — new session only at ~60% context at a task boundary, or after ship. See [session-lifecycle.md](references/session-lifecycle.md).
- **Model tiers** `strong` / `standard` / `fast`; risk flags force `strong`; the model changes only at spawn or escalation. See [model-tiers.md](references/model-tiers.md). Optional skills and per-harness model mapping: [integrations.md](references/integrations.md).
- **The author does not grade their own work** — reviewers run in a fresh context. No subagent support → run each agent as a separate headless process.
- No superpowers / gstack installed → do it by hand, with the same artifacts and gates.

## Core rules

- No product code before the plan passes its gate (spikes in scratch only).
- Git is the source of truth; a ticked box without a commit hash is not done.
- Diverging from the spec needs an ADR.
- Technical claims are verified and cited in the plan's Verified research.
- Retry ceilings: 3 for the same failure, 5 per task, then escalate ([phase-5-execute.md](references/phase-5-execute.md)).
- A failed gate sends you back, not forward ([session-lifecycle.md](references/session-lifecycle.md#the-pipeline-loops)).
