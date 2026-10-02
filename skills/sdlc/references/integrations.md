# Integrations

**Rule:** harness-specific tool and model names appear ONLY in this file. Everything else in the plugin uses tier names (`strong` / `standard` / `fast`) and capabilities.

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

| Tier | Setting |
|---|---|
| `strong` | `model: opus` + `effort: high` |
| `standard` | `model: sonnet` |
| `fast` | `model: haiku` |

Set it in an agent's frontmatter, or pass `model` when spawning (alias `opus`, `sonnet`, `haiku`; `inherit` = main session's model). Order: spawn-time parameter, then frontmatter, then the main model. `effort` is a frontmatter field only.

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

### Other harnesses

Put the provider's model id for each tier in the project's `docs/preferences.md` (for example `strong: <id>`), and spawn with it.
