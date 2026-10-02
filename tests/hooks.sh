#!/usr/bin/env bash
# Tests for hooks/*.sh. Needs jq.
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1
H="$PWD/hooks"; fail=0
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
chk() { [ "$2" = "$3" ] || { echo "  hooks FAIL: $1"; fail=1; }; }
status() { mkdir -p "$d/$1/docs"; printf -- '- **next:** %s\n- **waiting-on-human:** %s\n' "$2" "$3" > "$d/$1/docs/status.md"; }
stop() { jq -n --arg c "$d/$1" '{cwd:$c}' | "$H/continue-or-stop.sh"; }

status a "write the parser" none
chk "pending next + none blocks" "$(stop a | jq -r '.decision')" block
chk "block reason has next" "$(stop a | jq -r '.reason' | grep -c 'write the parser')" 1
status b "write the parser" "G2 human sign-off"
chk "open gate allows stop" "$(stop b)" ""
mkdir -p "$d/c"
chk "no status.md is a no-op" "$(stop c)" ""
status e "<the single next action>" "none | <gate id>"
chk "placeholders are no-ops" "$(stop e)" ""
status f none none
chk "next none is a no-op" "$(stop f)" ""
mkdir -p "$d/g/docs"; printf 'next: do it\nwaiting-on-human: none\n' > "$d/g/docs/status.md"
chk "plain lines parse" "$(stop g | jq -r '.decision')" block

ss() { jq -n --arg c "$d/$1" '{cwd:$c}' | "$H/session-start.sh"; }
chk "session-start injects" "$(ss a | jq -r '.hookSpecificOutput.additionalContext' | grep -c 'write the parser')" 1
chk "session-start no-op" "$(ss c)" ""

[ "$fail" -eq 0 ]
