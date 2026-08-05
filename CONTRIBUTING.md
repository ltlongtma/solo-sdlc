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
4. **Run `python3 docs/check-frontmatter.py`** if you touched any `SKILL.md`, agent, or command. Claude Code parses frontmatter leniently; every other harness does not, and one unquoted `": "` in a description aborts the whole package on install.
5. **Disclose agent-generated content.** If an agent wrote the change, say so and name the model. Not disqualifying — just weighted differently from a change grounded in a real session.

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
- **Pinning models or effort upward.** `model: inherit` respects the ceiling the user already chose, aliases don't rot the way full model IDs do, and frontmatter `effort` overrides the user's own `/effort` setting — so raising it here spends their money without asking. A cheaper model for a provably mechanical agent is welcome; the reverse needs evidence that the default actually misses findings. See *Tuning models and effort* in the README.

## Structure

```
.claude-plugin/     plugin.json + marketplace.json
apm.yml             APM manifest, for installs outside Claude Code
skills/sdlc/        the pipeline skill
agents/             five review agents
commands/           per-phase entry points
docs/               interactive workflow diagram
```

The layout is plugin-native, so nothing needs mirroring into an `.apm/` source tree — `apm pack` reads `skills/`, `agents/`, and `commands/` straight from the root, and copies the hand-written `.claude-plugin/plugin.json` into the bundle rather than synthesizing one from `apm.yml`.

The version therefore lives in **three** places and all three must move together, or consumers stop seeing updates: `.claude-plugin/plugin.json`, the plugin entry in `.claude-plugin/marketplace.json`, and `apm.yml`. Keep the README's phase table in sync too when the pipeline changes.
