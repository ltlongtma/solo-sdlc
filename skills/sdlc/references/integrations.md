# Integrations

**Rule:** harness-specific tool names appear only in this file, except Claude Code agent frontmatter fields (`model` / `effort` / `disallowedTools`) — the adapter layer. Everything else in the plugin uses tier names (`strong` / `standard` / `fast`) and capabilities.

## Capability → optional skills (use if present)

Never required. If a skill is absent, use the fallback and carry on.

| Capability | Skill | When | Produces | Fallback |
|---|---|---|---|---|
| Living architecture diagram | `archify` | phase 3; update on structural change | `docs/design/architecture.html` | hand-written HTML/SVG or a Mermaid block in the ADR |
| Browser oracle for UI and e2e | `@playwright/test` + `@axe-core/playwright` (npm, not a skill) | phase 5 (e2e), phase 6 (`qa-ui`) | repeatable e2e tests + automated a11y violations | manual checklist from the spec, recorded as unverified |
| Accessibility rules | `accessibility-a11y` | phase 5 UI code, phase 6 | a11y fixes and review notes | WCAG 2.2 AA checklist |
| Idea shaping | `minimalist-entrepreneur` | phase 0–1 | sharper problem, audience, smallest paid offer | the `product-critic` questions alone |
| Verified research | `deep-research` | phase 1 validation; any claim about market or competitors | cited findings | web search with sources noted; unverified claims marked as such |
| Impact before risky change | `blast-radius` | phase 4–5, before a task with a risk flag | callers, dependents, tests at risk | grep callers and tests by hand |
| Retro | `reflect` | phase 8 | lessons from the session | the retro template in `phase-8-retro.md` |
| Over-engineering review | `ponytail-review` | phase 4 (plan) and phase 6 (diff) | list of what to delete or simplify | YAGNI pass by `tech-lead-reviewer` |
| Design / microcopy | any design or copy skill | only when no mockup exists | layout, copy | plain, conventional UI; copy from the spec |

## Tier → model per harness

### Claude Code

Suggested defaults — the project's `docs/preferences.md` `## Models` table overrides them:

| Tier | Suggested setting |
|---|---|
| `strong` | `model: opus` + `effort: high` |
| `standard` | `model: sonnet` |
| `fast` | `model: haiku` |

Set it in an agent's frontmatter, or pass `model` when spawning (alias `opus`, `sonnet`, `haiku`; `inherit` = main session's model). Order: per-invocation `model` parameter, then agent frontmatter `model` (`inherit` = main conversation's model), then the `CLAUDE_CODE_SUBAGENT_MODEL` env var, then the main conversation's model (https://code.claude.com/docs/en/sub-agents). `effort` is a frontmatter field only. Because the per-invocation parameter wins over frontmatter, passing the `## Models` choice at spawn time overrides an agent's shipped default without editing the plugin.

Optional, in `~/.claude/settings.json` (your call, not required):
- Pin what an alias means: `ANTHROPIC_DEFAULT_OPUS_MODEL` / `_SONNET_MODEL` / `_HAIKU_MODEL` set to a full model ID. The spawn parameter takes aliases only, and an alias can lag a generation (`haiku` has resolved to Haiku 4.5).
- Catch a spawn that forgot `model`: `CLAUDE_CODE_SUBAGENT_MODEL` (for example `sonnet`). It sits below frontmatter, so agents keep their model, and an unnamed spawn lands there instead of the main session's model.

### omp

Define one `modelRoles` entry per tier (custom role names are allowed), then point each agent at a role with `task.agentModelOverrides`, using `"@<role>"` to reference it. Model strings are `<provider>/<model>[:<thinking>]`.

```yaml
modelRoles:
  sdlc-strong: <provider>/<strong-model>:high
  sdlc-standard: <provider>/<standard-model>
  sdlc-fast: <provider>/<fast-model>
task:
  agentModelOverrides:
    product-critic: "@sdlc-strong"
    solution-architect: "@sdlc-strong"
    tech-lead-reviewer: "@sdlc-strong"
    security-reviewer: "@sdlc-strong"
    qa-logic: "@sdlc-strong"
    qa-ui: "@sdlc-strong"
```

Implementer spawns use `"@sdlc-standard"`; quick lookups use `"@sdlc-fast"`.

### Other harnesses

Put the provider's model id for each tier in the `## Models` table of the project's `docs/preferences.md`, and spawn with it.

## Claude Code adapter (optional hooks)

The plugin ships two thin hooks in `hooks/` that only read `docs/status.md`: a `Stop` hook (`continue-or-stop.sh`) that blocks stopping while `next` is a real action and `waiting-on-human` is `none`, and a `SessionStart` hook (`session-start.sh`) that injects the status as context. They need `jq`, and do nothing without `docs/status.md`. They hold no logic the skill depends on; other harnesses can call the same scripts from their own hook systems (JSON on stdin with a `cwd` field).
