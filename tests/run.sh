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
    gate) python3 $S/check-gate.py --spec "$d/spec.md" --reports "$d"/reports/*.json --ledger "$d/ledger.tsv" \
            --gates "$d/gates.md" --reviews "$d/reviews" --sha 3f9c2a1b7d4e ;;
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

# 3. scaffold idempotency
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
snap() { (cd "$tmp" && find . -path ./.git -prune -o -print | sort); }
git init -q "$tmp"
if bash skills/sdlc/scaffold.sh "$tmp" >/dev/null 2>&1; then
  a="$(snap)"; ha="$(git -C "$tmp" config core.hooksPath || true)"
  bash skills/sdlc/scaffold.sh "$tmp" >/dev/null 2>&1 || true
  b="$(snap)"; hb="$(git -C "$tmp" config core.hooksPath || true)"
  if [ "$a" = "$b" ] && [ "$ha" = "$hb" ]; then ok scaffold-idempotent; else bad scaffold-idempotent; fi
else
  bad "scaffold-idempotent (first run failed)"
fi

# 4. version sync
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
