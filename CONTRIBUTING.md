# Contributing to solo-sdlc

Thanks for looking. This project is a set of behavior-shaping prompts, which changes what a good contribution looks like.

## The most valuable contribution

**A real session where the process failed you.** Open an issue with:

- which phase you were in
- what you asked for
- what the agent actually did
- what you expected instead

That's more useful than a proposed rewrite, because it tells us whether the rule was wrong or the wording was.

## Before opening a PR

1. **Use it first.** Skills and agents are prompts, not prose — a change that reads better can behave worse. Run the affected phase on a real task and say so in the PR.
2. **One problem per PR.** Bundled unrelated changes get split before review.
3. **Say what you tested on.** Which harness (Claude Code CLI / desktop / IDE), which model, and which other plugins were installed. Two plugins telling an agent contradictory things is a common cause of "the skill didn't trigger".
4. **Disclose agent-generated content.** If an agent wrote the change, say so and name the model. Not disqualifying — just weighted differently from a change grounded in a real session.

## What fits here

- Fixes to phase ordering, gate conditions, or agent checklists based on observed failures
- Sharper stop conditions (the retry ceiling and task-granularity rules both came from real burn)
- Support for another environment's equivalent tooling, added as *optional* ("when available")
- Language: prompts are English so any contributor can review them

## What doesn't fit

- **Hard dependencies on third-party tools.** Everything must work standalone. Integrations are opt-in and referenced conditionally.
- **Project-specific or stack-specific rules.** If it only helps Next.js apps or your company's conventions, keep it in your own repo's `docs/WORKFLOW.md` — the skill is designed for that override.
- **More phases.** Nine is already a lot. New process weight has to earn its place by naming the failure it prevents.
- **Removing human gates.** The gates are the point. If a gate is in the wrong place, argue for moving it, not deleting it.

## Structure

```
.claude-plugin/     plugin.json + marketplace.json
skills/sdlc/        the pipeline skill
agents/             five review agents
commands/           per-phase entry points
docs/               interactive workflow diagram
```

Version bumps go in `.claude-plugin/plugin.json`. Keep the version and the README's phase table in sync when the pipeline changes.
