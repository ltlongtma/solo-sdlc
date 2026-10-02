#!/usr/bin/env bash
# Stop hook: keep working while docs/status.md has a real next action and no human gate is open.
# Silent no-op on anything unexpected (no jq, no status.md).
command -v jq >/dev/null 2>&1 || exit 0
input=$(cat)
cwd=$(jq -r '.cwd // empty' <<<"$input" 2>/dev/null)
[ -n "$cwd" ] && { cd "$cwd" 2>/dev/null || exit 0; }
s=docs/status.md
[ -f "$s" ] || exit 0
# shellcheck source=lib.sh
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
next=$(field "$s" next)
wait=$(field "$s" waiting-on-human)
is_empty "$next" && exit 0
is_empty "$wait" || exit 0
# No stop_hook_active check on purpose: Claude Code caps consecutive Stop continuations itself.
jq -n --arg r "Next action pending: $next. No human gate is open (waiting-on-human: none); keep working instead of stopping to report." \
  '{decision:"block", reason:$r}'
