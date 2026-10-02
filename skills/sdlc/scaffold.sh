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

for d in business specs plans decisions design releases retro templates reviews qa; do
  mkdirp "docs/$d"
done

# The project's own copies, so every artifact has a shape even with no plugin installed.
for t in spec plan adr validation runbook release retro; do
  copy "$t.md" "docs/templates/$t.md"
done

copy review.md   docs/templates/review.md
copy status.md   docs/status.md
copy gates.md    docs/gates.md
copy preferences.md docs/preferences.md
copy ledger.tsv  docs/qa/ledger.tsv

# The CI gate needs docs/reviews/ to exist in a fresh checkout; git does not track empty dirs.
if [ -e docs/reviews/.gitkeep ]; then
  skipped+=("docs/reviews/.gitkeep")
else
  say "create docs/reviews/.gitkeep"
  [ "$DRY_RUN" -eq 1 ] || : > docs/reviews/.gitkeep
  created+=("docs/reviews/.gitkeep")
fi

# Contract checkers, run by the pre-push hook and by CI.
for c in spec plan gate; do
  copy "../scripts/check-$c.py" "scripts/sdlc/check-$c.py"
  case " ${created[*]:-} " in *" scripts/sdlc/check-$c.py "*) [ "$DRY_RUN" -eq 1 ] || chmod +x "scripts/sdlc/check-$c.py" ;; esac
done

# pre-push hook: lint specs and plans before they leave the machine.
if [ -e .githooks/pre-push ]; then
  skipped+=(".githooks/pre-push")
else
  say "create .githooks/pre-push"
  if [ "$DRY_RUN" -eq 0 ]; then
    mkdir -p .githooks
    cat > .githooks/pre-push <<'HOOK'
#!/usr/bin/env bash
# Blocks the push when a spec or plan fails its contract check. Silent when there is nothing to check.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 1
rc=0
specs=(docs/specs/*.md); plans=(docs/plans/*.md)
[ -e "${specs[0]}" ] && { python3 scripts/sdlc/check-spec.py "${specs[@]}" || rc=1; }
for p in "${plans[@]}"; do
  [ -e "$p" ] && { python3 scripts/sdlc/check-plan.py "$p" || rc=1; }
done
[ "$rc" -eq 0 ] || echo "pre-push: contract check failed; fix the lines above (bypass: git push --no-verify)" >&2
exit "$rc"
HOOK
    chmod +x .githooks/pre-push
  fi
  created+=(".githooks/pre-push")
fi

hooks_path="$(git config --get core.hooksPath || true)"
if [ -z "$hooks_path" ]; then
  if [ "$DRY_RUN" -eq 1 ]; then echo "would set git config core.hooksPath .githooks"
  else git config core.hooksPath .githooks && echo "set git config core.hooksPath .githooks"; fi
elif [ "$hooks_path" != ".githooks" ]; then
  echo "warning: core.hooksPath is already '$hooks_path'; left unchanged. Call .githooks/pre-push from there." >&2
fi

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
                             The `gate` job stays red until the real e2e step replaces the `{}`
                             placeholder report. That is intended: the gate fails closed.
  AGENTS.md                  track, phase in flight, and the real test/build commands.
  docs/WORKFLOW.md           the track this project runs; record any deliberate deviation.
  .env.example               every variable name the app needs. Placeholder values only.

── how the templates get used ──
  new spec      cp docs/templates/spec.md  docs/specs/<slug>.md
  new plan      cp docs/templates/plan.md  docs/plans/$(date +%Y-%m-%d)-<slug>.md
  new ADR       cp docs/templates/adr.md   docs/decisions/<NNNN>-<slug>.md
  runbook       cp docs/templates/runbook.md docs/runbook.md   (at the first release)
EOF
