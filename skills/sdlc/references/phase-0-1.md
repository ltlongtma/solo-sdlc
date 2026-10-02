# Phases 0–1 — Triage and Validate

## Phase 0 — Triage / Idea

- **Artifact:** an entry in `docs/backlog.md` (in scratch for a fresh idea).
- **Driven by:** an idea-level brainstorm (business: what, for whom).
  - No idea, or an idea still vague → run skill `find-idea` first (evidence-first internet sweep → a 2–3 candidate shortlist, in scratch, no repo).
  - A clear idea in hand → triage it directly.
  - `superpowers:brainstorming` when open-ended exploration fits better than market evidence.
- **Exit:** worth doing, and which track. The track choice is a T decision (record it in the backlog entry).

### Four rigor tracks

- **Trivial** (typo, one line, config): skip phases 1–4. Branch → PR → CI → merge.
- **Feature** (one screen / endpoint inside a product that exists): 0 → 2 → 2.5 → 4 → 8. Skip phase 1; phase 3 only if it touches architecture. One plan file, one review round.
- **Subsystem / high-risk** (schema, money, auth, migrations, deleting data): like Feature, plus phase 3 REQUIRED, two adversarial review rounds, `security-reviewer` REQUIRED, and a canary on deploy.
- **New product / big bet** (new project, pivot, more than ~2 weeks of work): full 0 → 8; phases 1 and 3 are REQUIRED. NO-GO at phase 1 → stop, write the reason into the backlog, no regrets.

### Three kinds of "brainstorm" — in this order

1. **Idea / business** — what to build and for whom (phase 0; no idea or a vague one → `find-idea`).
2. **Solution / WHAT** — how the feature behaves, what the requirements are (phase 2).
3. **Technical / HOW** — architecture and stack (phase 3).

No jumping ahead. If "brainstorm" is ambiguous, infer the kind from where the work stands (the earliest kind not yet done) and say which one you picked. Discussing stacks or libraries while in (1) or (2) means you are in the wrong phase — pull it back.

## Phase 1 — Validate (new-product track only)

- **Artifact:** `docs/business/<idea>-validation.md` (verdict + competitors + unit economics + risks / incidents).
- **Driven by:** agent `product-critic` (attacks market, pricing, ROI, distribution). Relay its verdict and conditions verbatim — never soften a NO-GO.
- **Gate:** every fatal assumption has a cheap test, then **GO / NO-GO — a B gate** (`decision-policy.md`).

## Fresh idea — no repo until GO

A repo is the artifact of the decision to BUILD, not of deciding whether to build. Do not `git init` yet.

1. Run phases 0–1 in a scratch directory (backlog + validation live in scratch). The idea can still come back NO-GO — don't spawn an orphan repo.
2. Raise GO / NO-GO as one B item that also carries the repo location and name as options with a default.
3. On GO → `git init` → scaffold → move the validation out of scratch into `docs/business/` (first commit) → phase 2.
4. On NO-GO → no repo; the idea survives as one line in a personal backlog.

Tracks other than new-product already have a repo — this deferral does not apply.

## Scaffold

Run this skill's `scaffold.sh` from the repo root. It is idempotent (never overwrites, reports what it skipped), so it is also the tool for an existing repo adopting the process. It creates the `docs/` tree, `docs/backlog.md`, `docs/WORKFLOW.md`, `docs/status.md`, `docs/gates.md`, `AGENTS.md`, `.gitignore`, `.env.example`, a CI workflow, `scripts/sdlc/check-*.py` and a pre-push hook.

- Fill what it lists as unfilled — **CI commands and `AGENTS.md` before the next gate**: the phase 6 gate reads CI, and the next session reads `AGENTS.md` first.
- A pre-existing `.gitignore` is kept: check it ignores `.env*`. `security-reviewer` audits `git log --all -- '*.env*'` at phase 6, and a secret committed once lives in history forever.
- **Every artifact starts from `docs/templates/`** — `cp docs/templates/spec.md docs/specs/<slug>.md`, and the same for plans, ADRs, validation, releases, retros and the runbook. Required sections are slots in those templates. **Do not delete a section marked REQUIRED** — a gate reads it.
- Existing repo with code but no `docs/WORKFLOW.md` → scaffold, then enter the pipeline at its real phase.
- Existing repo with no CI → adding it is task 1 of the first plan.
