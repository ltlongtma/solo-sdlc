#!/usr/bin/env bash
# Scaffold the solo-sdlc document set into a repo.
#
# Idempotent: never overwrites an existing file, reports what it skipped. Safe to re-run on a repo
# that adopted the process halfway.
#
#   ./scaffold.sh [--dry-run] [target-dir]
#
# Run it AFTER `git init` — the guard below refuses to scaffold outside a git repo, because the
# expensive mistake is creating docs/ in a home directory.
set -euo pipefail

TEMPLATES="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/templates"
DRY_RUN=0
TARGET="."

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    -h|--help) sed -n '2,10p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) TARGET="$arg" ;;
  esac
done

cd "$TARGET"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "error: $(pwd) is not a git repository." >&2
  echo "A repo is the artifact of deciding to BUILD. Run git init first, or pass the right target." >&2
  exit 1
fi

VERSION="$(sed -n 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
  "$(dirname "$TEMPLATES")/../../.claude-plugin/plugin.json" 2>/dev/null | head -1)"
VERSION="${VERSION:-unknown}"
TODAY="$(date +%Y-%m-%d)"

created=(); skipped=()

say() { [ "$DRY_RUN" -eq 1 ] && echo "would $*" || echo "$*"; }

mkdirp() {
  [ -d "$1" ] && return 0
  say "mkdir  $1"
  [ "$DRY_RUN" -eq 1 ] || mkdir -p "$1"
}

# copy <template> <destination>
copy() {
  local src="$TEMPLATES/$1" dst="$2"
  if [ -e "$dst" ]; then
    skipped+=("$dst")
    return 0
  fi
  say "create $dst"
  if [ "$DRY_RUN" -eq 0 ]; then
    mkdir -p "$(dirname "$dst")"
    sed -e "s/__SOLO_SDLC_VERSION__/$VERSION/g" -e "s/__DATE__/$TODAY/g" "$src" > "$dst"
  fi
  created+=("$dst")
}

for d in business specs plans decisions design releases retro templates; do
  mkdirp "docs/$d"
done

# The project's own copies, so every artifact has a shape even with no plugin installed.
for t in spec plan adr validation runbook release retro; do
  copy "$t.md" "docs/templates/$t.md"
done

copy backlog.md  docs/backlog.md
copy WORKFLOW.md docs/WORKFLOW.md
copy AGENTS.template.md AGENTS.md # named .template so a nested AGENTS.md is not read as instructions
copy env.example .env.example
copy ci.yml      .github/workflows/ci.yml
copy gitignore   .gitignore

echo
echo "── created ─────────────────────────────"
printf '  %s\n' "${created[@]:-none}"
if [ ${#skipped[@]} -gt 0 ]; then
  echo "── already existed, left untouched ─────"
  printf '  %s\n' "${skipped[@]}"
  case " ${skipped[*]} " in
    *" .gitignore "*)
      echo
      echo "  ! .gitignore was kept. Check it ignores .env* (and allows .env.example)"
      echo "    — compare against $TEMPLATES/gitignore" ;;
  esac
fi

cat <<'EOF'

── fill these in before the next gate ──
  .github/workflows/ci.yml   replace the placeholder commands with this project's real ones.
                             "CI green" is the phase 6 gate; wrong commands fail loudly, which is
                             the correct failure. A missing workflow fails silently.
  AGENTS.md                  track, phase in flight, and the real test/build commands.
  docs/WORKFLOW.md           the track this project runs; record any deliberate deviation.
  .env.example               every variable name the app needs. Placeholder values only.

── how the templates get used ──
  new spec      cp docs/templates/spec.md  docs/specs/<slug>.md
  new plan      cp docs/templates/plan.md  docs/plans/$(date +%Y-%m-%d)-<slug>.md
  new ADR       cp docs/templates/adr.md   docs/decisions/<NNNN>-<slug>.md
  runbook       cp docs/templates/runbook.md docs/runbook.md   (at the first release)
EOF
