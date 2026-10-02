#!/usr/bin/env bash
# Stop hook: keep working while docs/status.md has a real next action and no human gate is open.
# Silent no-op on anything unexpected (no jq, no status.md).
command -v jq >/dev/null 2>&1 || exit 0
here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
input=$(cat)
[ "$(jq -r '.stop_hook_active // false' <<<"$input" 2>/dev/null)" = true ] && exit 0
cwd=$(jq -r '.cwd // empty' <<<"$input" 2>/dev/null)
[ -n "$cwd" ] && { cd "$cwd" 2>/dev/null || exit 0; }
s=docs/status.md
[ -f "$s" ] || exit 0
# shellcheck source=lib.sh
. "$here/lib.sh"
grep -qi 'waiting-on-human' "$s" || exit 0  # marker: only solo-sdlc status files
next=$(field "$s" next)
wait=$(field "$s" waiting-on-human)
case "$wait" in *"<"*">"*) exit 0 ;; esac  # unfilled placeholder = unknown
is_empty "$next" && exit 0
is_empty "$wait" || exit 0
# stop_hook_active (above): nudge once per turn, never loop.
jq -n --arg r "Next action pending: $next. No human gate is open (waiting-on-human: none); keep working instead of stopping to report." \
  '{decision:"block", reason:$r}'
