# Model tiers

Three abstract tiers. This file uses tier names only; the mapping from tier to a concrete model for each harness lives in `references/integrations.md` (added later).

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

## Phase 5

When superpowers `subagent-driven-development` is present, follow its "Model Selection" section together with the task's `Tier:` field. Do not restate its rules here.
