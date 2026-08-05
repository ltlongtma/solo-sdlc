# Process for this project

<!-- scaffolded from solo-sdlc v__SOLO_SDLC_VERSION__ on __DATE__ -->

This file is the process **this repo** follows, and it wins over any skill or plugin when they disagree.
It is written to be followed by any agent or human, with or without solo-sdlc installed.

If you are an agent and solo-sdlc *is* installed: diff this file against the skill. Missing a phase,
gate, or agent → report the drift and propose a sync, but keep following this file until the human decides.

- **Track this project usually runs:** <feature | subsystem | new-product>
- **Current state:** see `AGENTS.md`

## The 9 phases

| # | Phase | Artifact (committed) | Exit gate | Who decides |
|---|---|---|---|---|
| 0 | Triage / Idea | a line in `docs/backlog.md` | Worth doing? which track? | Human |
| 1 | Validate (new product only) | `docs/business/<idea>-validation.md` | **GO / NO-GO** — every fatal assumption has a cheap test | **Human ⛔** |
| 2 | Spec | `docs/specs/<feature>.md` + acceptance checklist | Problem and approach clear; checklist is checkable | AI proposes → human decides |
| 2.5 | Clarify | Clarifications section in the spec | Nothing ambiguous still blocks the plan; answers are IN the spec, not in chat | AI asks → human answers |
| 3 | Architecture | ADR in `docs/decisions/` + spec architecture section + `docs/design/architecture.html` | Stack chosen, trade-offs recorded | **Human ⛔** |
| 4 | Plan | `docs/plans/YYYY-MM-DD-<feature>.md` + verified research + task status | Every task passes the granularity rules; ≥1 adversarial review round with a requirement→task matrix | **Human approves ⛔** |
| 5 | Execute | commits on `feat/*` | Per task: test red → green → commit → tick task status with the commit hash | AI |
| 6 | QA / Review | PR + review notes + ADR for any divergence | CI green + reviews confirmed + acceptance checklist passes + no CRITICAL/HIGH open | AI runs → **human signs off** |
| 7 | Release | merge + tag + `docs/releases/*` + `docs/runbook.md` | Smoke test + rollback plan + runbook + diagram matches reality | **Human ships ⛔** |
| 8 | Retro | `docs/retro/*` + backlog + this file | Lessons written down | Human + AI |

**The pipeline loops.** A failed gate goes backward, not forward: architecture breaks the spec → back to
phase 2 (+ADR); QA finds BLOCKING → back to phase 5; plan review BLOCKING → back to phase 4; execution
hits the retry ceiling → back to phase 4 (bad plan) or 2 (bad spec). Any backward step that changes a
settled artifact gets an ADR.

## Rigor tracks

| Track | When | Path |
|---|---|---|
| **Trivial** | typo, one line, config | skip 1–4. Branch → PR → CI → merge |
| **Feature** | one screen or endpoint in a product that exists | 0 → 2 → 2.5 → 4…8. Skip 1; phase 3 only if architecture is touched. One plan, one review round |
| **Subsystem / high-risk** | schema, money, auth, migrations, deleting data | Feature + phase 3 REQUIRED + two adversarial review rounds + security review REQUIRED + canary deploy |
| **New product / big bet** | new project, pivot, >~2 weeks | full 0→8; phases 1 and 3 REQUIRED. NO-GO at 1 → stop, record the reason, no regrets |

## Reviews — the author never grades their own work

Every review is a **separate agent with fresh context**. The session that wrote the plan cannot be the
one that approves it, and no agent may review its own output while wearing a different hat.

| Review | Runs at | Mandate |
|---|---|---|
| Technical review of the plan | 4, before asking for approval | Dependency order, interface drift across tasks, placeholders, task granularity, requirement→task matrix, YAGNI |
| Technical review of the code | 6 | Same lens on the diff; every in-scope requirement must appear in it |
| Break-it QA | 6 | Attack it: empty/huge/unicode input, boundaries, replay, concurrency, cross-account access, error paths. Scored against the acceptance checklist. A bug without a repro does not count |
| Security review | 6, and always on subsystem/new-product | Secrets, auth coverage, IDOR/multi-tenancy, injection, SSRF, webhook replay, abuse cost, dependency CVEs. CRITICAL/HIGH block the merge |

Reviewers report; they never edit. Fixing belongs to the main session.

## Hard rules

- A gate that needs a human → **stop and ask**. Never walk through a gate alone.
- **No product code before the plan is approved.** Until then: artifacts, reading code, and spikes only.
  A spike lives in scratch, is never committed, and its conclusion is written into the plan's verified
  research before it is deleted. The trivial track is exempt.
- Git is the source of truth, not the chat. Every phase produces a committable artifact.
- Tests and CI are the real status; checkboxes are a summary. **A ticked box with no commit hash counts as not done.**
- Branches `feat/*` `fix/*` `docs/*`; never commit straight to main. Commits read `type(scope): description`.
- Diverging from the spec is a bug unless an ADR in `docs/decisions/NNNN-<slug>.md` says otherwise.
- Technical claims about APIs, versions, or spec behavior get verified against docs and cited. Never recall.
- Clarifications and mid-flight decisions land in an artifact. The next session cannot read this chat.
- Work only a human can do (accounts, billing, pricing, legal, going live) goes in the backlog **early**.
- **Execution has a ceiling.** Same failure: 3 attempts, then change approach — a fourth attempt piles
  code around something not understood. Whole task: 5 attempts, each one a *new* failure. Out of
  attempts or the same failure returns → revert to the last green commit and report which test fails,
  what was tried, what is suspected. No agent raises its own ceiling.
- "Brainstorm" means three different conversations, in this order: **idea** (what and for whom, phase 0),
  **solution** (what it does, phase 2), **technical** (how it is built, phase 3). Discussing libraries
  while defining requirements means the wrong phase — pull it back.

## Local deviations

Where this project deliberately differs from the standard process. Add the reason — an undocumented
deviation is indistinguishable from drift.

| Rule | This project instead | Why |
|---|---|---|
| <…> | <…> | <…> |
