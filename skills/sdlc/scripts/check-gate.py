#!/usr/bin/env python3
"""check-gate: the QA gate. Exit 0 only when every gate condition holds.

Conditions (all must hold):
  1. every A<n> verified by e2e has >=1 passing Playwright test, and every A<n>
     verified by integration|unit has >=1 passing Vitest test, whose title contains
     "[A<n>]"; no test carrying "[A<n>]" is failed, skipped, fixme, pending or todo;
     a Vitest report with success=false or any test file not "passed" fails;
  2. every human-B A<n> is answered in the gates file;
  3. every reviews/*.md has the four bucket headings, and no unresolved blocking
     finding sits in any ## section except "## Return summary"; every
     --require-review NAME has a *-NAME-*.md file in review format;
  4. UI spec: every UI A<n> (Verify by: e2e) has a ledger row whose verdict is
     live-ui-verified at a SHA that counts for --sha: same commit (prefix match,
     >=7 chars), or an earlier commit with no non-docs/ change since then.

Report formats are auto-detected per file:
  Playwright JSON reporter: top-level "config" + "suites"
  Vitest JSON reporter:     top-level "testResults" (Jest-compatible)

Any missing or unreadable input that a condition needs is a failure, never a skip.
Output: one "path:line: problem" per failure, then "gate: PASS" or "gate: FAIL (<n> problems)".
"""
import argparse
import functools
import fnmatch
import glob
import itertools
import json
import os
import re
import subprocess
import sys

VERIFY_RE = re.compile(r"Verify by:\s*(e2e|integration|unit|human-B)\b")
AID_RE = re.compile(r"\*\*(A\d+)\*\*")
PLACEHOLDER_RE = re.compile(r"<[^>]*>")
TESTED_KINDS = ("e2e", "integration", "unit")
UNANSWERED = ("", "tbd", "-", "?")
BUCKETS = ("act on", "consider", "noted", "dismissed")
MARKER_RE = re.compile(r"(?<![\w-])(?:BLOCKING\b|(?i:blocking):)")
SCOPE_RE = re.compile(r"\bScope:\s*`?([0-9a-fA-F]{7,40})\b")

problems = []


def problem(path, line, msg):
    problems.append(f"{path}:{line}: {msg}")


def read_lines(path, what):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read().splitlines()
    except OSError as e:
        problem(path, 0, f"cannot read {what}: {e.strerror or e}")
        return None


def sections(lines):
    """Yield (heading_text, [(lineno, line), ...]) for each '## ' section; the heading line
    itself is the first body entry."""
    name, body = None, []
    for i, line in enumerate(lines, 1):
        if line.startswith("## "):
            if name is not None:
                yield name, body
            name, body = line[3:].strip(), [(i, line)]
        elif name is not None:
            body.append((i, line))
    if name is not None:
        yield name, body


# ---------- spec ----------

def header_value(lines, field):
    for line in lines:
        if line.startswith("## "):
            break
        m = re.match(r"\s*-\s*\*\*" + field + r":\*\*\s*(.*)$", line, re.I)
        if m:
            return m.group(1).strip().strip("`").strip()
    return ""


def parse_spec(path):
    """Return (is_ui, [(aid, kind, lineno)]) or None if unreadable."""
    lines = read_lines(path, "spec")
    if lines is None:
        return None
    design = header_value(lines, "Design source")
    design_set = bool(design) and design.lower() != "none" and not PLACEHOLDER_RE.search(design)
    is_ui = header_value(lines, "UI").lower() == "yes" or design_set

    items, seen, found_section = [], set(), False
    for name, body in sections(lines):
        if not name.lower().startswith("acceptance"):
            continue
        found_section = True
        for n, line in body:
            if not re.match(r"\s*-\s*\[[ xX]\]", line):
                if AID_RE.search(line):
                    problem(path, n, "acceptance id on a non-checkbox line (use '- [ ]' or '- [x]')")
                continue
            aid, kind = AID_RE.search(line), VERIFY_RE.findall(line)
            if not aid or len(kind) != 1:
                problem(path, n, "acceptance line needs **A<n>** and exactly one 'Verify by: e2e|integration|unit|human-B'")
                continue
            if aid.group(1) in seen:
                problem(path, n, f"duplicate acceptance id {aid.group(1)}")
                continue
            seen.add(aid.group(1))
            items.append((aid.group(1), kind[0], n))
    if not found_section:
        problem(path, 0, "no '## Acceptance' section")
    elif not items:
        problem(path, 0, "no acceptance items found")
    return is_ui, items


# ---------- reports ----------

def playwright_tests(report):
    """Yield (title, outcome, where) for every test in a Playwright JSON report."""
    def walk(suite):
        for spec in suite.get("specs") or []:
            where = f"{spec.get('file', '?')}:{spec.get('line', '?')}"
            for t in spec.get("tests") or []:
                yield spec.get("title", ""), playwright_outcome(t), where
        for child in suite.get("suites") or []:
            yield from walk(child)
    for suite in report["suites"]:
        yield from walk(suite)


def playwright_outcome(t):
    kinds = {a.get("type") for a in t.get("annotations") or []}
    if t.get("status") == "skipped" or t.get("expectedStatus") == "skipped" or kinds & {"fixme", "skip"}:
        return "fixme" if "fixme" in kinds else "skipped"
    results = t.get("results") or []
    # flaky = failed then passed on retry; the final result decides.
    if (t.get("status") in ("expected", "flaky") and t.get("expectedStatus") == "passed"
            and results and results[-1].get("status") == "passed"):
        return "passed"
    return "failed"


def vitest_tests(report, path):
    if report.get("success") is not True:
        problem(path, 0, "Vitest run did not succeed (success is not true)")
    for f in report["testResults"]:
        where = f.get("name", "?")
        asserts = f.get("assertionResults") or []
        if f.get("status") != "passed":
            problem(path, 0, f"test file {where} is {f.get('status')}: {(f.get('message') or '').strip()[:200]}")
        for a in asserts:
            status = a.get("status")
            outcome = status if status in ("passed", "failed") else (status or "unknown")
            yield a.get("title", ""), outcome, where


def load_tests(paths):
    tests = []  # (title, outcome, report_path, where, runner)
    for path in paths:
        try:
            with open(path, encoding="utf-8") as f:
                report = json.load(f)
        except OSError as e:
            problem(path, 0, f"cannot read report: {e.strerror or e}")
            continue
        except ValueError as e:
            problem(path, 0, f"malformed JSON report: {e}")
            continue
        if isinstance(report, dict) and isinstance(report.get("suites"), list) and "config" in report:
            for err in report.get("errors") or []:
                msg = err.get("message", "") if isinstance(err, dict) else str(err)
                problem(path, 0, f"Playwright run error: {msg.strip()[:200]}")
            found, runner = playwright_tests(report), "Playwright"
        elif isinstance(report, dict) and isinstance(report.get("testResults"), list):
            found, runner = vitest_tests(report, path), "Vitest"
        else:
            problem(path, 0, "unrecognized report format (expected Playwright or Vitest JSON reporter output)")
            continue
        tests += [(title, outcome, path, where, runner) for title, outcome, where in found]
    return tests


def check_tests(spec_path, items, tests):
    for aid, kind, n in items:
        if kind not in TESTED_KINDS:
            continue
        tag = f"[{aid}]"
        runner = "Playwright" if kind == "e2e" else "Vitest"
        mine = [t for t in tests if tag in t[0]]
        for title, outcome, rpath, where, _ in mine:
            if outcome != "passed":
                problem(rpath, 0, f"{aid}: test '{title}' ({where}) is {outcome}")
        if not any(t[1] == "passed" and t[4] == runner for t in mine):
            problem(spec_path, n, f"{aid} (Verify by: {kind}) has no passing test titled with '{tag}' in a {runner} report")


# ---------- gates ----------

def check_gates(spec_path, items, gates_path):
    human = [(aid, n) for aid, kind, n in items if kind == "human-B"]
    if not human:
        return
    if not gates_path:
        problem(spec_path, 0, f"human-B items {', '.join(a for a, _ in human)} need --gates")
        return
    lines = read_lines(gates_path, "gates file")
    if lines is None:
        return
    answered, blocks, answer = set(), set(), ""
    for line in lines + ["## end"]:
        if re.match(r"#{2,} ", line):  # every ##/### heading starts a new gate block
            if answer.lower() not in UNANSWERED and not PLACEHOLDER_RE.search(answer):
                answered |= blocks
            blocks, answer = set(), ""
            continue
        m = re.match(r"\s*-\s*\*\*(Blocks|Answer):\*\*\s*(.*)$", line, re.I)
        if m and m.group(1).lower() == "blocks":
            blocks |= set(re.findall(r"\bA\d+\b", m.group(2)))
        elif m:
            answer = m.group(2).strip()
    for aid, n in human:
        if aid not in answered:
            problem(spec_path, n, f"{aid} (human-B) is not answered in {gates_path}")


# ---------- reviews ----------

def check_reviews(reviews_dir, sha, required=()):
    if not os.path.isdir(reviews_dir):
        problem(reviews_dir, 0, "reviews directory not found")
        return
    valid = []  # (basename, scope sha) of files in review format
    for path in sorted(glob.glob(os.path.join(reviews_dir, "*.md"))):
        lines = read_lines(path, "review")
        if lines is None:
            continue
        secs = list(sections(lines))
        names = [name.lower() for name, _ in secs]
        missing = [b for b in BUCKETS if not any(n.startswith(b) for n in names)]
        if missing:  # fail closed: a file without the buckets is not a review the gate understands
            problem(path, 0, "not in review format (missing headings: " + ", ".join(missing) + ")")
        else:
            preamble = itertools.takewhile(lambda line: not line.startswith("## "), lines)
            scope = next((m.group(1) for m in map(SCOPE_RE.search, preamble) if m), "")
            valid.append((os.path.basename(path), scope))
        # Every ## section counts, heading included, except the return summary (prose for the
        # caller). The preamble before the first ## is instructions, not findings.
        for name, body in secs:
            if name.lower().startswith("return summary"):
                continue
            for n, line in body:
                # Marker: uppercase BLOCKING, or "blocking:" in any case ("NON-BLOCKING" and
                # prose like "no blocking issues" are not); only literal "[resolved]" resolves it.
                if MARKER_RE.search(line) and "[resolved]" not in line:
                    problem(path, n, f"unresolved BLOCKING finding: {line.strip()[:200]}")
    for name in required:
        mine = [scope for f, scope in valid if fnmatch.fnmatch(f, f"*-{name}-*.md")]
        if not mine:
            problem(reviews_dir, 0, f"required review '{name}' missing: no *-{name}-*.md in review format")
        elif not any(scope and sha_counts(scope, sha) for scope in mine):
            problem(reviews_dir, 0, f"required review '{name}' is stale: no *-{name}-*.md has a 'Scope: <sha>' that counts for {sha}")


# ---------- ledger ----------

@functools.lru_cache(maxsize=None)
def sha_counts(row_sha, sha):
    """A ledger row at row_sha counts for sha when they are the same commit (prefix match,
    >=7 chars), or row_sha resolves in git and nothing outside docs/ changed between them."""
    a, b = row_sha.strip().lower(), sha.strip().lower()
    if not re.fullmatch(r"[0-9a-f]{7,40}", a) or len(b) < 7:
        return False
    if a.startswith(b) or b.startswith(a):
        return True
    git = lambda *cmd: subprocess.run(["git", *cmd], capture_output=True).returncode == 0
    return git("cat-file", "-e", a + "^{commit}") and git("diff", "--quiet", a, b, "--", ":(top)", ":(top,exclude)docs/")


def check_ledger(spec_path, items, ledger_path, sha):
    ui_items = [(aid, n) for aid, kind, n in items if kind == "e2e"]
    if not ui_items:
        return
    if not ledger_path:
        problem(spec_path, 0, "UI spec has e2e acceptance items but no --ledger given")
        return
    lines = read_lines(ledger_path, "ledger")
    if lines is None:
        return
    header = lines[0].split("\t") if lines else []
    if not all(c in header for c in ("acceptance_id", "sha", "verdict")):
        problem(ledger_path, 1, "ledger header must include acceptance_id, sha, verdict (tab-separated)")
        return
    col = {name: header.index(name) for name in ("acceptance_id", "sha", "verdict")}
    last = {}  # aid -> verdict of the last row that counts for this sha (ledger is append-only)
    for row in lines[1:]:
        cells = row.split("\t")
        if len(cells) < len(header):
            continue
        if sha_counts(cells[col["sha"]], sha):
            last[cells[col["acceptance_id"]].strip()] = cells[col["verdict"]].strip()
    for aid, n in ui_items:
        verdict = last.get(aid)
        if verdict != "live-ui-verified":
            got = f"last verdict '{verdict}'" if verdict else "no row"
            problem(spec_path, n, f"{aid} (UI) has no live-ui-verified ledger row at sha {sha} ({got})")


def main():
    ap = argparse.ArgumentParser(description="QA gate: exit 0 only when every gate condition holds.")
    ap.add_argument("--spec", required=True, help="spec markdown (docs/specs/<slug>.md)")
    ap.add_argument("--reports", required=True, nargs="+", help="Playwright and/or Vitest JSON reporter files")
    ap.add_argument("--ledger", help="QA ledger TSV (docs/qa/ledger.tsv); required for UI specs")
    ap.add_argument("--gates", help="gates file (docs/gates.md); required when spec has human-B items")
    ap.add_argument("--reviews", required=True, help="reviews directory (docs/reviews/)")
    ap.add_argument("--require-review", action="append", default=[], metavar="NAME",
                    help="fail unless --reviews has a *-NAME-*.md file in review format (repeatable)")
    ap.add_argument("--sha", required=True, help="commit SHA under test (>=7 hex chars)")
    args = ap.parse_args()

    if not re.fullmatch(r"[0-9a-fA-F]{7,40}", args.sha):
        problem("--sha", 0, f"invalid sha '{args.sha}' (need 7-40 hex chars)")

    spec = parse_spec(args.spec)
    tests = load_tests(args.reports)
    if spec is not None:
        is_ui, items = spec
        check_tests(args.spec, items, tests)
        check_gates(args.spec, items, args.gates)
        if is_ui:
            check_ledger(args.spec, items, args.ledger, args.sha)
    check_reviews(args.reviews, args.sha, args.require_review)

    for p in problems:
        print(p)
    if problems:
        print(f"gate: FAIL ({len(problems)} problems)")
        return 1
    print("gate: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
