#!/usr/bin/env bash
# SessionStart hook: inject docs/status.md (first 300 words) as session context. No-op without it.
command -v jq >/dev/null 2>&1 || exit 0
input=$(cat)
cwd=$(jq -r '.cwd // empty' <<<"$input" 2>/dev/null)
[ -n "$cwd" ] && { cd "$cwd" 2>/dev/null || exit 0; }
[ -f docs/status.md ] || exit 0
ctx=$(awk '{for(i=1;i<=NF;i++){if(++n>300)exit}; print}' docs/status.md)
jq -n --arg c "Project status (docs/status.md):
$ctx" '{hookSpecificOutput:{hookEventName:"SessionStart", additionalContext:$c}}'
