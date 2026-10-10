# solo-sdlc

A gated 9-phase SDLC for **one founder shipping with AI**.

Most AI coding workflows optimize the wrong bottleneck. When you're solo, the expensive failure isn't slow typing — it's spending three weeks building something nobody wanted, or letting an agent grind on a broken plan until it has wrecked your codebase. This plugin puts gates where those failures happen.

It is **artifact-first and harness-agnostic**. Three layers, each usable without the one above it:

- **Contract** — plain files in your repo: specs with `A<n>` acceptance IDs, a plan with per-task `Tier:` and risk flags, `docs/status.md`, `docs/gates.md`, a QA ledger. Three stdlib-only scripts (`check-spec`, `check-plan`, `check-gate`) read them.
- **Instruction** — the `sdlc` skill, a router into one reference per phase. Any agent that can read markdown can follow it.
- **Adapter** — the thin Claude Code layer: agent frontmatter (`model`, `effort`), slash commands, and optional hooks. Other harnesses map tiers to models via [`integrations.md`](skills/sdlc/references/integrations.md).

Four ideas do most of the work:

- **Validate the business case before the repo exists.** A repo is the artifact of deciding to *build*, not of deciding *whether* to build. Phases 0–1 run in a scratch directory; `git init` happens only after you say GO.
- **The author never grades their own work, and a gate is a script, not a statement.** Every review is a separate agent with fresh context. A phase passes when its check exits 0; `check-gate` runs in CI, so make the `gate` job a **required status check** in branch protection or it is advice. There is no plan-approval or PR sign-off step to rubber-stamp.
- **Only money-class decisions stop the AI.** Decisions are sorted B / T / R: **B** (money, pricing, GO/NO-GO, prod deploy, destructive data ops, legal or customer-facing content, cutting scope) is the only kind that waits for you, recorded in `docs/gates.md` with options and a default; **T** is decided by the AI and logged with a `reverse with:` word; **R** rubber-stamp approvals are removed.
- **Execution has a ceiling.** An agent gets 3 attempts at the same failure and 5 at a task. Then it reverts to the last green commit and reports, instead of looping until your budget and your architecture are both gone.

## Install

**Claude Code**

```
/plugin marketplace add ltlongtma/solo-sdlc
/plugin install solo-sdlc@solo-sdlc
```

**Any other agent, via [APM](https://github.com/microsoft/apm)** — Copilot, Cursor, Codex, Gemini, OpenCode, Windsurf, Kiro:

```
apm install ltlongtma/solo-sdlc
```

APM writes each primitive to the directory your harness actually reads: skills to `.agents/skills/` (the location Copilot, Cursor, Codex, Gemini, OpenCode and Windsurf share) or to `.claude/skills/` and `.kiro/skills/` for the two that differ, and agents to the harness-specific agents directory. `apm.lock.yaml` pins the version.

**VS Code / GitHub Copilot, without APM** — the plugin format is shared, and VS Code looks for `.claude-plugin/plugin.json`, so this repo installs as-is. Run **Chat: Install Plugin From Source** from the Command Palette and paste the repo URL (requires `chat.plugins.enabled`).

**By hand** — Cursor and VS Code both read `~/.claude/`, so symlinking works too:

```
git clone https://github.com/ltlongtma/solo-sdlc
ln -s "$PWD/solo-sdlc/skills/sdlc" ~/.claude/skills/sdlc
ln -s "$PWD"/solo-sdlc/agents/*.md ~/.claude/agents/
```

Verified with `apm install <local checkout> --target cursor`: all 14 primitives land — the three skills at `.agents/skills/` (`sdlc`, `find-idea`, `evidence`), the six agents at `.cursor/agents/`, the five commands at `.cursor/commands/` — plus the two optional hooks at `.cursor/hooks.json`. What I have *not* verified is whether each harness then surfaces those commands in its own `/` menu, or whether the agents' `model: opus` / `effort: high` is honored outside Claude Code — worst case they run on your session model, which is harmless. The skill auto-triggers either way.

## Use it

```
/solo-sdlc:find-idea  <nothing, or a vague idea>        # phase 0 — mine the web, shortlist 2-3 ideas
/solo-sdlc:start      I want to build a tool that ...   # full pipeline, from anywhere
/solo-sdlc:validate   <a rough idea>                    # phase 1 only — is this worth building?
/solo-sdlc:architect                                    # phase 3 only — stack options + trade-offs
/solo-sdlc:gate                                          # phase 6 only — the QA/review gate
/solo-sdlc:converge                                      # reconcile real code against spec + plan
```

The `evidence` skill (browser proof for a PR: captioned MP4, storyboard PNG, state trace, ready-to-paste PR section) triggers on requests like *"record the flow"* or *"video evidence"*; `qa-ui` and phase 6 use it. It needs Node, `playwright-core` and `ffmpeg`.

The `sdlc` skill also auto-triggers on things like *"take this idea to production"* or *"resume this project properly"*. A vague idea is a fine starting point — phase 0 exists to sharpen it. **No idea at all is also a fine starting point**: `find-idea` mines complaints, reviews, job ads and market shifts for a pain somebody already pays to escape, and hands you a shortlist instead of a guess.

## The pipeline

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/pipeline-dark.svg">
  <img alt="The nine phases: Triage, Validate, Spec, Clarify, Architecture, Plan, Execute, QA/Review, Release, Retro. Phases 0-1 run in scratch with no repo; four phases are human gates; three loop-backs return to an earlier phase when a gate fails." src="docs/pipeline-light.svg" width="100%">
</picture>

<sub>Phase 6 spawns up to four agents in parallel: `tech-lead-reviewer`, `qa-logic`, `qa-ui` (UI specs), and `security-reviewer` (only when the diff touches sensitive ground). Regenerate the diagram with `python3 docs/generate-pipeline-svg.py`.</sub>

| # | Phase | Artifact | Gate |
|---|---|---|---|
| 0 | Triage / Idea | `docs/backlog.md` (+ an idea scan, if you started with nothing) | Worth doing? which track? |
| 1 | Validate | `docs/business/<idea>-validation.md` | **GO / NO-GO ⛔** |
| 2 | Spec | `docs/specs/<feature>.md` + acceptance checklist | Spec agreed |
| 2.5 | Clarify | Clarifications section in the spec | Nothing ambiguous blocks the plan |
| 3 | Architecture | ADRs + `docs/design/architecture.html` | **Stack chosen ⛔** |
| 4 | Plan | `docs/plans/YYYY-MM-DD-*.md` + verified research + task status | **Plan approved ⛔** |
| 5 | Execute | code on `feat/*`, one commit per task | Every task green |
| 6 | QA / Review | PR + `docs/reviews/*` + `docs/qa/ledger.tsv` | `check-gate` exits 0 in CI — no sign-off |
| 7 | Release | tag + `docs/releases/*` + `docs/runbook.md` | **Human ships ⛔** |
| 8 | Retro | `docs/retro/*` | Lessons written down |

Phases scale to the work through four rigor tracks: **trivial** (skip 1–4), **feature** (skip validate), **subsystem** (architecture + security required, two review rounds), **new product** (all nine). Specs, plans and the gate are checked by `scripts/sdlc/check-spec.py`, `check-plan.py` and `check-gate.py`, which `scaffold.sh` installs into your repo.

There's an interactive version of this diagram in [`docs/workflow-diagram.html`](docs/workflow-diagram.html) — open it locally to click through each phase and highlight the path a given track takes.

## The agents

| Agent | Runs at | Mandate |
|---|---|---|
| `product-critic` | phase 1 | Kill bad ideas cheaply. Market, competitors, unit economics, distribution, risk. Every claim cited; every fatal assumption gets the cheapest possible test. |
| `solution-architect` | phase 3 | Propose 2–3 stacks with real monthly costs and escape routes. Optimizes for *"can one person fix this at 2am?"* Proposes — never approves. |
| `tech-lead-reviewer` | phases 4 & 6 | Assume the document is broken and find out how. Dependency order, interface drift, oversized tasks, requirement→task coverage matrix. |
| `qa-logic` | phases 4–5 & 6 | Writes the acceptance tests first (`test.fixme('[A<n>] …')`), then breaks the logic: business rules, money math, multi-screen flows, edge cases, replay, cross-account access, error paths. A bug without a repro doesn't count. |
| `qa-ui` | phase 6, UI specs | Real browser at 360 and 1440 px against the mockup, axe, any console error = FAIL, loading/empty/error states. Appends `live-ui-verified` or `fail` rows to `docs/qa/ledger.tsv`. |
| `security-reviewer` | phase 6, conditional | Attacker's lens: secrets, IDOR, injection, SSRF, webhook replay, dependency CVEs. CRITICAL/HIGH block the merge. |

None of them fixes product code — fixes go to a fresh implementer. Each writes only its report (`docs/reviews/`, or `docs/business/` for `product-critic`, plus draft ADRs under `docs/decisions/` for `solution-architect`), `qa-logic`'s acceptance tests, and `qa-ui`'s evidence and ledger rows under `docs/qa/`. That write-path restriction is instruction-level, not enforced: the agents have Write, and nothing in the harness stops a stray file — review the diff.

## Tuning models and effort

Skills and references speak in three **tiers**, never model names: `strong` (judgment, hard-to-reverse decisions, review), `standard` (coding to a clear plan), `fast` (wide reads, summaries, commit messages). Every plan task carries `Tier:` and `Risk flags:`; money/pricing, auth/RLS, migrations, concurrency, or touching 2+ modules or a public interface force `Tier: strong` (`check-plan` fails otherwise). The model changes only at spawn or on escalation after a failure, never mid-session. Tier-to-model mapping per harness is in [`integrations.md`](skills/sdlc/references/integrations.md); on Claude Code it is `strong` = `claude-opus-5-5`/high, `standard` = `claude-sonnet-5-5`, `fast` = `claude-haiku-5-5`.

**Agents.** All six ship as `model: claude-opus-5-5` with `effort: high` as a suggested default — your `## Models` table overrides it: each is a judgment call whose miss is expensive (a bad GO, a wrong stack, a missed BLOCKING finding), and the gate trusts the QA agents. Only aliases are used, never a full model ID, so the plugin doesn't rot when a new model lands. `effort: high` is [already the default](https://docs.claude.com/en/docs/claude-code/model-config#adjust-effort-level), so it mainly pins reviewers against a lower session level; frontmatter effort *overrides your session level*, which is why nothing here pins `xhigh`.

| What you want | How |
| --- | --- |
| Choose models for a project | Edit `## Models` in `docs/preferences.md` (scaffolded with the suggested defaults); the AI passes them at every spawn |
| A different model for one agent | Edit `model:` in `agents/<name>.md` — alias (`opus`, `sonnet`, `haiku`, `fable`), a full model ID, or `inherit` |
| A model for subagents that name none | `CLAUDE_CODE_SUBAGENT_MODEL` — below the spawn parameter and agent frontmatter (Claude Code ≥ 2.1.251) |
| The single biggest saving | Let plan tasks carry `Tier: standard`. Execution subagents are spawned per task from the plan, not by an agent file, and once tasks satisfy the granularity rules the extra capability buys little |
| Deeper reasoning on the merge-blocking reviewers | Add `effort: xhigh` to `agents/tech-lead-reviewer.md` and `agents/security-reviewer.md` |
| Cheaper QA passes | `model: haiku` on `qa-logic` / `qa-ui`, or add `effort: medium` |
| Cap it globally | `CLAUDE_CODE_EFFORT_LEVEL` — takes precedence over frontmatter and the session |

Phases that reward depth: **1, 3 and 4** (validation, architecture, plan review) and **6** (review gate). **5** (execute) is mostly mechanical once the plan is good — that's the point of the task-granularity rules.

## Design decisions worth knowing about

**Required sections are slots, not reminders.** `scaffold.sh` writes a template set into `docs/templates/`, and every artifact starts as a copy of one. The sections gates read — acceptance checklist, clarifications, verified research, task status, rollback — are pre-cut slots marked REQUIRED. A prose instruction to "remember the acceptance checklist" gets skipped under pressure; an empty slot in the file you're already editing does not. Numbered requirement IDs (`R1`, `R2`) exist for the same reason: they make `tech-lead-reviewer`'s requirement→task matrix mechanical instead of a judgement call.

**The repo stays self-describing.** Scaffolding also writes `docs/WORKFLOW.md` (a short pointer to the process, stamped with the plugin version), `AGENTS.md` (track, build commands) and `docs/status.md` (`next:` and `waiting-on-human:`). All are for the agent that shows up without this plugin installed — including one that isn't Claude. Scaffolding also installs `scripts/sdlc/check-*.py`, a CI workflow whose `gate` job runs `check-gate`, and a `.githooks/pre-push` that runs the spec and plan checks.

**Task granularity is a gate, not a suggestion.** Oversized tasks are the number-one reason subagents fail. A task ships only if it has one red→green test, is committable on its own with the repo still green, can be done by a fresh-context agent from the plan plus 1–3 named files, and depends on nothing unfinished.

**Task status lives in git.** Agent scratch ledgers are git-ignored and vanish. So the plan file carries `- [x] Task 3 — <name> — <commit hash>`, ticked the moment the task goes green, in the same commit as the code and the `docs/status.md` update. A ticked box with no resolvable hash counts as not done. There is no "one phase, one session" rule: start a new session at a task boundary around 60% context, or after ship.

**The pipeline loops.** Architecture that breaks the spec goes back to the spec. A retry ceiling means the plan was wrong, not that the agent needs more attempts. Every backward step that changes a settled artifact gets an ADR.

**"Brainstorm" is disambiguated.** Idea-level (phase 0), solution-level (phase 2), and technical (phase 3) are different conversations. Discussing libraries while defining requirements means you're in the wrong phase.

## Optional hooks

`hooks/` ships two opt-in Claude Code hooks (need `jq`; silent no-ops without it or without `docs/status.md`): **SessionStart** injects the head of `docs/status.md` as context, and **Stop** keeps the agent working while `status.md` has a real `next:` action and no B gate is open. It never traps a stop on a loose match, a missing marker, or a repeated stop. The pipeline works the same without them.

## Optional integrations

Everything works standalone. When these are installed, the skill and agents use them as a baseline layer and keep going:

- [`superpowers`](https://github.com/obra/superpowers) — `brainstorming`, `writing-plans`, `subagent-driven-development`, `test-driven-development`, `using-git-worktrees`. The strongest pairing; solo-sdlc supplies the business gates and review agents that sit around it.
- [`tt-a1i/archify`](https://github.com/tt-a1i/archify) — `archify` for the living architecture diagram.
- `minimalist-entrepreneur` — pricing, first customers, and marketing frameworks at phases 1 and 7.
- gstack — `/qa`, `/browse`, `/review`, `/ship`, `/cso`, `/retro`.
- Trail of Bits `skills` — security plugins used by `security-reviewer` on large PRs.
- MCP servers for code graphs and library docs (e.g. context7) — used to verify claims instead of trusting recall.

## How this relates to Spec Kit

[GitHub Spec Kit](https://github.com/github/spec-kit) solves an adjacent problem: it standardizes spec-driven artifacts across any agent, through a CLI and command set (`specify`, `plan`, `tasks`, `clarify`, `analyze`, `checklist`, `converge`). solo-sdlc borrows several of its ideas — acceptance checklists as "unit tests for prose", clarifications committed into the spec rather than left in chat, an explicit requirement→task matrix, and reconciling real code against the spec when resuming.

It deliberately does **not** wrap the Spec Kit CLI. This plugin keeps its artifacts in plain `docs/` and adds what a solo founder needs and a spec toolkit doesn't cover: business validation before the repo, adversarial review agents, an execution retry ceiling, an incident runbook, and human gates on value decisions. If you already run Spec Kit, take the agents from here and ignore the pipeline.

## Upgrading from 0.2

1. Re-run `skills/sdlc/scaffold.sh` in your project. It is idempotent: it adds `scripts/sdlc/`, `.githooks/pre-push`, the new templates and the CI `gate` job, and leaves existing files alone.
2. Make `gate` a required status check in branch protection.
3. If you kept a handoff file, migrate it to `docs/status.md`.
4. In open specs, add `A<n>` acceptance IDs and a `Verify by` line to each; in open plans, add `Tier:` and `Risk flags:` to each task. `check-spec` and `check-plan` list what is missing.
5. The single QA agent is now `qa-logic` plus `qa-ui`; update any local references.

See [CHANGELOG.md](CHANGELOG.md).

## Contributing

Issues and PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). The most useful contribution is a real session where the process failed you: which phase, what the agent did, what you expected. Process rules are behavior-shaping prompts, so changes need evidence from actual use, not just a tidier wording.

## License

MIT — see [LICENSE](LICENSE).
