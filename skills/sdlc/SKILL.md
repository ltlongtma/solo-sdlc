---
name: sdlc
description: Use when a solo founder working with AI has a new product or feature idea, wants to brainstorm or validate a startup idea, starts a new project, says "run the SDLC" / "take this from idea to ship" / "validate my idea" / "critique this idea", or wants to resume an existing project by the process.
---

# SDLC — one founder + AI

A 9-phase pipeline with gates. AI does most of the work; the human is the **value gate** — AI **STOPS** at every gate and never walks through one on its own.

## When invoked — do this first

1. **Is there a repo already?**
   - Repo has its own `docs/WORKFLOW.md` → read it plus `docs/backlog.md`, find the phase in flight, resume there. **The repo's WORKFLOW.md WINS over this skill when they disagree.** Still diff them: if WORKFLOW.md is missing a phase/gate/agent this skill has → REPORT the drift and propose syncing; until the human decides, keep following the repo's WORKFLOW.md.
   - Repo has code but no WORKFLOW.md (existing project adopting this process) → scaffold (step 3), then enter the pipeline at the right phase.
   - **Resuming work in flight → CONVERGE before continuing.** Do not trust the plan or its checkboxes: read the actual code plus `git log`, compare against the open spec and plan, and produce three lists — (a) tasks the plan calls done that the code does not have or implements differently, (b) code that exists but the plan never mentioned (scope drift → needs an ADR or a spec amendment), (c) spec requirements with no task at all. Show the human all three, get a decision, then update the plan and continue. Skipping this means redoing finished work or shipping without work you assumed was done.
2. **No repo yet (fresh idea) — do NOT `git init` yet.** A repo is the artifact of the decision to BUILD, not the artifact of deciding *whether* to build. Sequence:
   - **Run phases 0–1 in a scratch directory** (backlog + validation live in scratch). The idea can still come back NO-GO — don't spawn an orphan repo.
   - **Only scaffold the repo once phase 1's gate returns GO** (new-product track). On GO → ask the human where to put it and what to call it → `git init` → scaffold → **move the validation out of scratch into `docs/business/`** (first commit) → continue to phase 2.
   - Tracks other than new-product (adding a feature to a product that exists) already have a repo — this deferral does not apply.
3. **Scaffold (first time creating the repo) — run this skill's `scaffold.sh` from the repo root.** It is idempotent (never overwrites, reports what it skipped), so it is also the right tool for an existing repo adopting the process. It creates `docs/{business,specs,plans,decisions,design,releases,retro,templates}/`, `docs/backlog.md`, `docs/WORKFLOW.md`, `AGENTS.md`, `.gitignore`, `.env.example`, and a CI workflow. Then fill in what it lists as unfilled — **CI commands and `AGENTS.md` before the next gate**, because the phase 6 gate reads "CI green" and *Living architecture diagram* sends the next session to `AGENTS.md` first. If a `.gitignore` already existed it was kept: check it ignores `.env*`, since `security-reviewer` audits `git log --all -- '*.env*'` at phase 6 and a secret committed once lives in history forever.
   - **Every artifact starts from `docs/templates/`** — `cp docs/templates/spec.md docs/specs/<slug>.md`, and the same for plans, ADRs, validation, releases, retros, and the runbook. The required sections (acceptance checklist, clarifications, verified research, task status) are slots in those templates, not things to remember. **Do not delete a section marked REQUIRED** — a gate reads it.
   - Existing repo with no CI → adding it is task 1 of the first plan, not a later nice-to-have.
4. **Run the pipeline** — a fresh idea starts at phase 0; an existing project resumes at its real phase.

## The 9 phases

| # | Phase | Artifact (committed to the repo) | Driven by | EXIT GATE | Owner |
|---|---|---|---|---|---|
| 0 | Triage / Idea | an entry in `docs/backlog.md` | **idea-level brainstorm** (business: what, for whom) — no idea, or an idea still vague → run skill `find-idea` first (evidence-first internet sweep → a 2–3 candidate shortlist, in scratch, no repo); a clear idea in hand → triage it directly. `superpowers:brainstorming` when you want open-ended exploration rather than market evidence | Worth doing? which track? | Human |
| 1 | Validate (**new-product** track only) | `docs/business/<idea>-validation.md` (verdict + competitors + unit economics + risks/incidents) | agent `product-critic` (attacks market, pricing, ROI, distribution) | **GO / NO-GO — every fatal assumption has a cheap test** | **Human decides (⛔)** |
| 2 | Spec | `docs/specs/<feature>.md` **with an "Acceptance checklist"** (every requirement measurable/checkable — "unit tests for prose") | **solution-level brainstorm** (product: WHAT — requirements, not HOW) via `superpowers:brainstorming` if available | Problem + approach are clear; trade-offs written down; the checklist passes against the spec | AI proposes → Human decides |
| 2.5 | Clarify | a **"Clarifications"** section in the spec (Q→A, line by line) | structured Q&A: sweep the spec for coverage gaps and ambiguity, ask the human **one question at a time** | Nothing ambiguous is still blocking the plan; **answers are COMMITTED into the spec, not left in chat** | AI asks → Human answers |
| 3 | Architecture (new-product / anything touching architecture) | ADRs in `docs/decisions/` + an architecture section in the spec + `docs/design/architecture.html` | agent `solution-architect` (HOW — 2–3 options with trade-offs; inputs are the spec + business constraints from validation) → discuss with the human | Stack and architecture chosen, trade-offs recorded in an ADR. **If the architecture breaks the spec (infeasible / too expensive) → go back and fix the spec + write an ADR, never drift silently** | **Human decides (⛔)** |
| 4 | Plan | `docs/plans/YYYY-MM-DD-<feature>.md` **with a "Verified research" section** (facts about versions/APIs/library behavior + cited sources) **and a "Task status" section** (see *Task status belongs in git*) | `superpowers:writing-plans` | Plan carries code + commands + a verification step per task; **tasks are small enough** (see *Task granularity*); **≥1 review round by agent `tech-lead-reviewer`, which must include a requirement→task coverage matrix** | **Human approves (⛔)** |
| 5 | Execute | code + commits on a `feat/*` branch (several subagents in parallel → give each its own worktree via `superpowers:using-git-worktrees` so they don't collide) | `superpowers:subagent-driven-development` (preferred) or `executing-plans` | Per task: test red → green → commit **→ tick "Task status" in the plan with the commit hash** | AI |
| 6 | QA / Review | PR + review notes + an ADR if the code diverges from the spec | agent `tech-lead-reviewer` (code) + agent `qa-logic` (break the logic — scored against the spec's **Acceptance checklist**) + agent `qa-ui` (live browser at 360/1440 px vs the mockup, axe, console; UI specs) + agent `security-reviewer` (when the diff touches sensitive ground) | CI green + reviews confirmed + acceptance checklist passes + no security CRITICAL/HIGH left + every divergence has an ADR | AI runs → **Human signs off** |
| 7 | Release | merge to main + tag + `docs/releases/*` + an **incident runbook `docs/runbook.md`** (created/updated from the risk section of validation plus what deploying actually taught you) | `/ship`, `/land-and-deploy` (if installed) | Post-deploy smoke test + rollback plan + runbook exists + **architecture diagram updated if this round changed the structure** | **Human pushes the button** |
| 8 | Retro | `docs/retro/*` + backlog updates + WORKFLOW.md updates if the process itself needs to change | `/retro` (if installed) | Lessons written down | Human + AI |

**Go-to-market is not a phase the AI drives** — but on the new-product track, phase 7 must surface the human-only items already sitting in the backlog: final pricing, the channel for the first customers, landing page and marketing (drive with `minimalist-entrepreneur:pricing` / `first-customers` / `marketing-plan` if installed).

No superpowers/gstack installed → do it by hand, honoring the same artifacts and gates. Nothing essential changes.

## 4 rigor tracks (chosen at phase 0)

- **Trivial** (typo, one line, config): skip phases 1–4. Branch → PR → CI → merge.
- **Feature** (one screen/endpoint inside a product that exists): 0 → 2 → 2.5 → 4→8. Skip phase 1; phase 3 only if it touches architecture. One plan file, one review round.
- **Subsystem / high-risk** (schema, money, auth, migrations, deleting data): like Feature plus phase 3 REQUIRED + two adversarial review rounds + `security-reviewer` REQUIRED + canary on deploy.
- **New product / big bet** (new project, pivot, more than ~2 weeks of work): full 0→8; phase 1 (Validate) and phase 3 (Architecture) are REQUIRED. NO-GO at phase 1 → stop, write the reason into the backlog, no regrets.

## Task granularity (settled at phase 4, decides whether phase 5 survives)

Oversized tasks are the number-one reason subagents fail and burn the whole retry budget. Split until **every task satisfies all four**:

1. **One test** — there is one concrete test/check that goes red → green. If you can't name the test, the task isn't clear yet (a different problem from being too big).
2. **One commit** — when it's done you can commit and the repo is still green. A task that needs three commits to go green is three tasks.
3. **A fresh-context subagent can do it** — the plan plus 1–3 files is enough; it does not need to understand the whole repo. This is the real measure (replacing "2–5 minutes" of human estimation): you must be able to name the files it will touch.
4. **No dependency on unfinished work** — every interface/type this task uses was created by an earlier task (`tech-lead-reviewer` audits exactly this).

Any violation → split further. Landing at one task = one function / one endpoint / one migration is normal, not over-fragmented.

## Task status belongs in git

`superpowers:subagent-driven-development` keeps a ledger at `.superpowers/sdd/<plan>/progress.md`, but that is **git-ignored scratch** — great for resuming inside or right after a session, gone after `git clean -fdx`, and unreadable when you open the repo weeks later. So the **cross-session source of truth is the plan file in git**:

- The plan carries a **"Task status"** section — one line per task: `- [x] Task 3 — <task name> — <commit hash>` (not started is `- [ ]`; stopped midway records `WIP + why it stopped`).
- **Tick it the moment the task goes green and is committed**, never in a batch at the end. Fold it into the code commit or make a separate `docs:` commit.
- **A ticked box with no commit hash means not done** (per the rule that checkboxes are only a summary). Suspect drift → reconcile with `git log --oneline` and trust git over the checkbox.
- Keep using the `.superpowers/` ledger as in-session recovery scratch; the two are complements, not substitutes.

## Agent roles — SPAWN THEM, don't wait to be asked

- **Phase 1 (new-product track):** spawn agent `product-critic` to attack the idea. Relay the verdict and conditions verbatim — never soften a NO-GO.
- **Phase 3 (new-product / touching architecture):** spawn agent `solution-architect` for 2–3 options with trade-offs. The main session discusses with the human and only commits the ADR once it's decided. The architect PROPOSES and is not the reviewer: the plan that comes out of this architecture still goes through `tech-lead-reviewer` at phase 4. **Once the architecture is settled → draw/update `docs/design/architecture.html`:** the architect's high-level design is the input; invoke the `archify` skill directly to build it (if it isn't installed, the AI writes the diagram to the standard in *Living architecture diagram*).
- **Phase 4 (required before asking for approval):** spawn agent `tech-lead-reviewer` on the plan. Fix every BLOCKING finding before presenting it.
- **Phase 4/5 start:** spawn agent `qa-logic` to write the acceptance tests from the spec **before implementation** — one `test.fixme('[A<n>] …')` per A-id. Implementers flip them to `test` as features land; nobody weakens or deletes one to make it pass.
- **Phase 6:** spawn `tech-lead-reviewer` (code/PR review), `qa-logic` (break the logic) and, for a UI spec, `qa-ui` (live browser, writes `docs/qa/ledger.tsv`) **in parallel**. Collect, fix, and only then ask for sign-off.
- **Phase 6, add `security-reviewer` when the diff touches:** auth/session · schema/RLS/migrations · money/webhooks · user input/uploads · fetching external URLs · public endpoints. Always spawn it on the high-risk and new-product tracks. Unresolved CRITICAL/HIGH means the gate is not passed.
- Core principle: **the author does not grade their own work** — reviewers must be fresh context (a separate agent), not the same session wearing a different hat.
- Agent not installed (`~/.claude/agents/` or the plugin) → fall back to a general-purpose subagent with an equivalent mandate (spell the adversarial/break-it mandate out in the prompt).

## Living architecture diagram — the onboarding document

- **Artifact:** `docs/design/architecture.html` — one self-contained HTML file (no external dependencies), committed to the repo.
- **Created when:** the architecture is first settled (end of phase 3, from `solution-architect`'s high-level design; projects that skip phase 3 create it at the end of phase 2). **Updated when:** any round adds, removes, or moves a component — checked at the phase 7 gate (releasing with a diagram that contradicts reality means the gate is not passed).
- **Automate the check (recommended — don't rely on memory):** write a small script (the project names it, e.g. `scripts/check-architecture-diagram.*`) that reconciles both directions — (a) does every path a diagram node points at still exist, and (b) does every real top-level directory (main app/package/module) have a node representing it. Run it in CI on every PR; a failure means the phase 7 gate is not passed. This script is a PROJECT artifact, not part of this skill, but the principle applies to every project using this process.
- **Content standard:** full-screen interactive SVG; every node is a REAL thing in the repo (directory/file/service); clicking one opens a panel explaining *what it does + why it lives there + related ADRs*; the main flows (data pipeline, user request, document lifecycle, CI) can be highlighted/animated from chips; pan + zoom + dark mode; node labels match real names — a newcomer should be able to map the diagram onto the directory tree immediately.
- **How to build it:** use the `archify` skill from [tt-a1i/archify](https://github.com/tt-a1i/archify) — if it isn't installed, suggest `npx skills add tt-a1i/archify --skill archify`. Unlike the old `html-diagram` pairing, `archify` does not block model invocation, so the AI can invoke it directly. If it can't be installed, the AI writes the file to the standard above.
- **Its role:** this is the primary onboarding document for whoever (human or AI) shows up next — read AGENTS.md to learn where to resume, open the diagram to understand the system in five minutes.

## Hard rules

- A gate that needs a human → STOP and ask. Never walk through a gate alone.
- **No vibe-coding — do NOT write product code before the human approves the plan.** Before the phase 4 gate you may only: write artifacts (spec/plan/ADR), read code, and **spike** (an experiment that answers one technical question — it lives in scratch, is NEVER committed to source, and once it's answered you record the conclusion under "Verified research" and delete it). The trivial track is exempt.
- **"Brainstorm" is an ambiguous word — pin down which kind before starting.** Three kinds, done in this order, no jumping ahead: (a) **idea / business** — what to build and for whom (phase 0; no idea or a vague one → `find-idea`); (b) **solution / WHAT** — how the feature behaves, what the requirements are (phase 2); (c) **technical / HOW** — architecture and stack (phase 3). If the human just says "brainstorm", ask one question to pin the kind down instead of guessing. Discussing stacks or libraries while in (a) or (b) means you're in the wrong phase — pull it back.
- Git is the source of truth, not the chat — every phase produces a committable artifact. **The one exception:** for a fresh idea, phases 0–1 live in scratch until GO (see *When invoked*); the first thing after GO is creating the repo and committing the validation. On NO-GO there is no repo — the idea survives as one line in a personal backlog.
- Tests/CI are the real status; checkboxes are only a summary — a ticked box with no commit hash counts as not done (see *Task status belongs in git*).
- Branches are `feat/*` `fix/*` `docs/*`; never commit straight to main. Commits read `type(scope): description`.
- Diverging from the spec is a bug unless there's an ADR in `docs/decisions/NNNN-<slug>.md` (context → decision → consequences).
- Technical claims (API/spec behavior) must be verified against docs or web search and cited — never trust recall. Write the verified result into the plan's "Verified research" section instead of leaving it to die in the chat.
- Clarification answers and mid-flight decisions must land in an artifact (spec Clarifications, ADR) — the next session cannot read this chat.
- Work only a human can do (accounts, billing, pricing, legal, grading a golden set, going live) → list it in the backlog early so it never blocks you at the last minute.
- **Execution has a ceiling — no infinite loops. Two tiers.** The ceiling is only a backstop; the real stop signal is **lack of progress**, not hitting a count.
  - **Tier 1 — fixing the SAME failure (tight loop): 3 attempts max.** Missing the same failure three times means you don't understand the cause, not that you need another try. Another attempt just piles code around something you don't understand — that's how structure gets wrecked. After 3, CHANGE approach (re-read the spec/plan, add logging, shrink the repro); do not keep patching blind.
  - **Tier 2 — the whole task (different failures surfacing in sequence): 5 attempts max**, AND each one must be a NEW failure (real progress). Out of attempts, or the same failure returns → STOP, revert to the last green commit (never leave half-done code), and report to the human: which test fails, what you tried, what you suspect.
  - Subagent-driven work: every subagent gets the task plus both ceilings in its prompt; when it hits one it hands control back and NEVER raises its own ceiling. Stop earlier than the ceiling if fixing A breaks B, or if you have to edit files outside the task's scope → suspect the plan/spec and go back to the matching gate.
- **The pipeline loops; it is not one-way** — when a gate fails, go back instead of pushing forward: architecture breaks the spec → back to phase 2 to fix the spec (+ADR); QA/review fails (BLOCKING/CRITICAL) → back to phase 5; plan review is BLOCKING → back to phase 4; execution hits the retry ceiling → back to phase 4 (bad plan) or phase 2 (bad spec). Retro (phase 8) feeds the backlog, and the next round starts at phase 0. Any backward step that changes a settled artifact gets an ADR explaining why.
