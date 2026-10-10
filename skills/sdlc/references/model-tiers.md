# Model tiers

Three abstract tiers. This file uses tier names only; the mapping from tier to a concrete model for each harness lives in [integrations.md](integrations.md).

| Tier | Use for |
|---|---|
| `strong` | judgment, hard-to-reverse decisions, synthesis, verification and review |
| `standard` | coding to a clear plan, multi-file integration, re-reviewing a small fix diff |
| `fast` | wide reads that return pointers, log summaries, release notes, commit messages |

## Picking a tier

- Pick by **difficulty** and by **the cost of being wrong**, not by role name. A role only carries a default tier; the plan can raise it per task.
- Machine checks first: anything a script, test or CI can check costs no model and is the most trustworthy.
- The reviewer is at least as strong as the author on the class of fault it checks.

## Risk flags force `strong`

A task with any of these flags gets `Tier: strong`, however easy it looks:
- money / pricing / quota / scoring;
- auth / session / RLS;
- migrations / data deletion;
- concurrency / idempotency;
- touching 2+ modules, or a public interface.

## `Tier:` per plan task

Every plan task carries `Tier:` and `Risk flags:`. `check-plan` fails a task whose risk flag is not `none` unless `Tier: strong`.

## When the model changes

Only at two moments:
1. **Spawn time** — phase 5 takes the tier from the task's `Tier:`; other phases use the agent's default.
2. **Escalation after a failure** — a fresh implementer one tier up (see `phase-5-execute.md`).

The main session never switches model mid-conversation.

## Every spawn names its model — the human picks it

The plugin suggests; the human decides. The model for each tier (and any per-role override) lives in the `## Models` table of the project's `docs/preferences.md`. Empty or missing → use the suggested defaults in `integrations.md` and say so once.
- Every spawn passes the model from that table explicitly. A subagent never inherits the main session's model by accident — that model is whatever the human last picked for chatting, not a tier decision.
- Re-reviewing a fix diff uses the `standard` row unless the fix touches a risk flag above, then `strong`.
- The AI never edits the `## Models` table on its own. It may suggest a change (with evidence, e.g. findings lost or cost per gate) and waits for the human.

## Phase 5

When superpowers `subagent-driven-development` is present, follow its "Model Selection" section together with the task's `Tier:` field. Do not restate its rules here.
