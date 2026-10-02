#!/usr/bin/env bash
# Single test runner. Run from anywhere; operates from the repo root.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
ROOT="$PWD"
S=skills/sdlc/scripts
fail=0

ok()  { echo "ok   $1"; }
bad() { echo "FAIL $1"; fail=$((fail + 1)); }

# 1. frontmatter
if python3 docs/check-frontmatter.py >/dev/null 2>&1; then ok frontmatter; else bad frontmatter; fi

# 2. fixtures: good exits 0; every bad-* exits 1 and prints expected.txt
run_check() { # family dir
  local d="$1"
  case "$2" in
    spec) python3 $S/check-spec.py "$d/spec.md" ;;
    plan) python3 $S/check-plan.py --spec "$d/spec.md" --no-git "$d/plan.md" ;;
    gate) # optional extra flags in "$d/args"
          # shellcheck disable=SC2046
          python3 $S/check-gate.py --spec "$d/spec.md" --reports "$d"/reports/*.json --ledger "$d/ledger.tsv" \
            --gates "$d/gates.md" --reviews "$d/reviews" --sha 3f9c2a1b7d4e $(cat "$d/args" 2>/dev/null) ;;
  esac
}
for fam in spec plan gate; do
  for d in tests/fixtures/$fam/*/; do
    d="${d%/}"; name="$fam/$(basename "$d")"
    set +e; out="$(run_check "$d" "$fam" 2>&1)"; rc=$?; set -e
    if [[ "$d" == */good ]]; then
      [ "$rc" -eq 0 ] && ok "$name" || bad "$name (exit $rc)"
    else
      if [ "$rc" -eq 1 ] && grep -qF -- "$(cat "$d/expected.txt")" <<<"$out"; then ok "$name"; else bad "$name (exit $rc)"; fi
    fi
  done
done

# --list must also run the checks (resume drift) and exit 1 on a ticked task with no hash
set +e; out="$(python3 $S/check-plan.py --list --spec tests/fixtures/plan/bad-ticked-no-hash/spec.md --no-git tests/fixtures/plan/bad-ticked-no-hash/plan.md 2>&1)"; rc=$?; set -e
if [ "$rc" -eq 1 ] && grep -q "todo (no hash)" <<<"$out"; then ok plan-list-drift; else bad "plan-list-drift (exit $rc)"; fi

# 3. gate cases that a fixture directory cannot express
G=tests/fixtures/gate/good
gate() { python3 "$ROOT/$S/check-gate.py" --spec "$ROOT/$G/spec.md" --reports "$ROOT/$G"/reports/*.json \
           --gates "$ROOT/$G/gates.md" "$@"; }
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT

# a review copied from the template, with no findings, passes
mkdir "$tmp/reviews" && cp skills/sdlc/templates/review.md "$tmp/reviews/"
if gate --ledger "$G/ledger.tsv" --reviews "$tmp/reviews" --sha 3f9c2a1b7d4e >/dev/null; then
  ok gate-template-review; else bad gate-template-review; fi

# --require-review passes when a matching review file in review format exists
if gate --ledger "$G/ledger.tsv" --reviews "$ROOT/tests/fixtures/gate/bad-missing-required-review/reviews" \
     --require-review qa-logic --sha 3f9c2a1b7d4e >/dev/null; then
  ok gate-required-review-present; else bad gate-required-review-present; fi

# --reviews is required
set +e; gate --ledger "$G/ledger.tsv" --sha 3f9c2a1b7d4e >/dev/null 2>&1; rc=$?; set -e
[ "$rc" -eq 2 ] && ok gate-reviews-required || bad "gate-reviews-required (exit $rc)"

# ledger row at an earlier SHA counts only while nothing outside docs/ changed since
r="$tmp/shas"; git init -q "$r"
c() { mkdir -p "$r/$(dirname "$1")"; echo "$RANDOM" >> "$r/$1"; git -C "$r" add -A
      git -C "$r" -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm "$1"
      git -C "$r" rev-parse HEAD; }
s1="$(c src/app.txt)"; s2="$(c docs/notes.md)"; s3="$(c src/app.txt)"
printf 'acceptance_id\tsha\tverdict\nA1\t%s\tlive-ui-verified\n' "$s1" > "$tmp/ledger.tsv"
lg() { (cd "$r" && gate --ledger "$tmp/ledger.tsv" --reviews "$ROOT/$G/reviews" --sha "$1"); }
if lg "$s2" >/dev/null; then ok gate-sha-docs-only-change; else bad gate-sha-docs-only-change; fi
set +e; out="$(lg "$s3")"; rc=$?; set -e
if [ "$rc" -eq 1 ] && grep -q "A1 (UI) has no live-ui-verified" <<<"$out"; then ok gate-sha-code-change
else bad "gate-sha-code-change (exit $rc)"; fi

# 4. scaffold idempotency
s="$tmp/scaffold"; git init -q "$s"
snap() { (cd "$s" && find . -path ./.git -prune -o -print && find . -path ./.git -prune -o -type f -exec shasum {} +) | sort; }
if bash skills/sdlc/scaffold.sh "$s" >/dev/null 2>&1; then
  a="$(snap)"; ha="$(git -C "$s" config core.hooksPath || true)"
  if bash skills/sdlc/scaffold.sh "$s" >/dev/null 2>&1; then
    b="$(snap)"; hb="$(git -C "$s" config core.hooksPath || true)"
    if [ "$a" = "$b" ] && [ "$ha" = "$hb" ]; then ok scaffold-idempotent; else bad scaffold-idempotent; fi
  else
    bad "scaffold-idempotent (second run failed)"
  fi
else
  bad "scaffold-idempotent (first run failed)"
fi

# scaffold leaves a custom core.hooksPath alone
h="$tmp/hooks"; git init -q "$h"; git -C "$h" config core.hooksPath custom-hooks
bash skills/sdlc/scaffold.sh "$h" >/dev/null 2>&1 || true
[ "$(git -C "$h" config core.hooksPath)" = custom-hooks ] && ok scaffold-keeps-hookspath || bad scaffold-keeps-hookspath

# 5. version sync
vers="$(python3 - <<'PY'
import json, re
p = json.load(open(".claude-plugin/plugin.json"))["version"]
m = json.load(open(".claude-plugin/marketplace.json"))
m = next(x for x in m["plugins"] if x["name"] == "solo-sdlc").get("version", "?")
a = re.search(r"^version:\s*(\S+)", open("apm.yml").read(), re.M).group(1)
print(p, m, a)
PY
)"
if [ "$(tr ' ' '\n' <<<"$vers" | sort -u | wc -l)" -eq 1 ]; then ok "version-sync ($vers)"; else bad "version-sync ($vers)"; fi

echo "---"
[ "$fail" -eq 0 ] && echo "all checks passed" || echo "$fail check(s) failed"
[ "$fail" -eq 0 ]
