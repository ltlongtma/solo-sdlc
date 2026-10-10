# Preferences — standing orders

Numbered rules the AI applies without asking. Each one removes a question you would otherwise be
asked every time. To reverse one, delete its line (or strike it and note the date); the AI re-asks
from the next session. To change one, edit it in place.

1. <e.g. Use pnpm, never npm or yarn.>
2. <e.g. Commit messages in English, Conventional Commits.>
3. <e.g. Prefer boring, well-known libraries over new ones.>
4. <e.g. Never ask me about naming or file layout; decide and record it.>

## Models

Your choice. The AI passes these at every spawn and never edits this table on its own. Shown: the
plugin's suggested defaults — change any cell (alias or full model ID). Until `Confirmed:` is filled,
the AI asks you once per session (without blocking work).

Confirmed: <date, filled when you answer>

| Tier | Used by | Model |
|---|---|---|
| strong | product-critic, solution-architect, tech-lead-reviewer, qa-logic, qa-ui, security-reviewer; `Tier: strong` tasks | opus |
| standard | `Tier: standard` tasks; re-review of a fix diff without risk flags | sonnet |
| fast | lookups, log summaries, release notes, commit messages | haiku |

Per-role override (optional): <e.g. qa-ui: sonnet>
