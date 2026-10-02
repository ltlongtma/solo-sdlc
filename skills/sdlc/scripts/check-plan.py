#!/usr/bin/env python3
"""Lint a solo-sdlc plan against its spec. Prints `path:line: problem`; exit 1 on any failure."""
import argparse, os, re, subprocess, sys

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("plan")
ap.add_argument("--spec", help="spec path (default: the plan's **Spec:** header)")
ap.add_argument("--no-git", action="store_true", help="skip commit-hash resolution")
ap.add_argument("--list", action="store_true", help="print id, name, tier, status per task")
a = ap.parse_args()

try:
    lines = open(a.plan, encoding="utf-8").read().splitlines()
except OSError as e:
    sys.exit(f"{a.plan}: cannot read: {e}")

fails = 0
def out(path, n, msg, warn=False):
    global fails
    fails += not warn
    print(f"{path}:{n}: {'warning: ' if warn else ''}{msg}")

def section(ls, name):
    """(line_no, text) pairs under the `## name*` heading, case-insensitive prefix."""
    res, on = [], False
    for i, l in enumerate(ls, 1):
        if l.startswith("## "):
            on = l[3:].strip().lower().startswith(name.lower())
        elif on:
            res.append((i, l))
    return res

def field(block, name):
    for i, l in block:
        m = re.match(rf"\s*- \*\*{name}[^*]*:\*\*\s*(.*)", l, re.I)
        if m:
            return i, m.group(1).strip()
    return None

# --- tasks ---
tasks, cur = [], None
for i, l in enumerate(lines, 1):
    m = re.match(r"### Task (\d+) — (.*)", l)
    if m:
        cur = {"id": int(m[1]), "name": m[2].strip(), "line": i, "block": []}
        tasks.append(cur)
    elif l.startswith("#"):
        cur = None
    elif cur:
        cur["block"].append((i, l))

# --- status ---
status = {}  # task id -> (line, ticked, hash)
for i, l in section(lines, "Task status"):
    m = re.match(r"- \[([ xX])\] Task (\d+)\b", l)
    if m:
        h = re.findall(r"`([^`]*)`", l)
        status[int(m[2])] = (i, m[1] != " ", h[-1] if h else "")

if a.list:
    for t in tasks:
        _, ticked, h = status.get(t["id"], (0, False, ""))
        tier = (field(t["block"], "Tier") or (0, "?"))[1]
        print(f"{t['id']} · {t['name']} · {tier} · {'done ' + h if ticked else 'todo'}")
    sys.exit(0)

# --- spec ---
spec = a.spec
if not spec:
    for l in lines:
        m = re.match(r"- \*\*Spec:\*\*\s*`?([^`\s]+)", l)
        if m:
            spec = m[1]
            break
spec_lines = None
if spec:
    try:
        spec_lines = open(spec, encoding="utf-8").read().splitlines()
    except OSError:
        out(a.plan, 1, f"cannot read spec {spec}")
else:
    out(a.plan, 1, "no **Spec:** header and no --spec")

ui, aids = False, []
if spec_lines is not None:
    for l in spec_lines:
        if l.startswith("## "):
            break
        m = re.match(r"- \*\*(UI|Design source):\*\*\s*(.*)", l)
        if m:
            v = m[2].strip().strip("`").lower()
            ui |= (v == "yes") if m[1] == "UI" else v not in ("", "none") and not v.startswith("<")
    for i, l in section(spec_lines, "Acceptance"):
        m = re.match(r"\s*- \[[ xX]\] \*\*(A\d+)\*\*", l)
        if m:
            aids.append(m[1])

if ui and not any(t["id"] == 0 and t["name"].lower().startswith("verification harness") for t in tasks):
    out(a.plan, 1, "UI spec but no '### Task 0 — Verification harness'")

# --- per-task checks ---
covered = set()
for t in tasks:
    b, at = t["block"], t["line"]
    f = {k: field(b, k) for k in ("Covers", "Files", "Test", "Verify", "Tier", "Risk flags")}
    for k, v in f.items():
        if not v:
            out(a.plan, at, f"Task {t['id']}: missing **{k}**")
    if f["Covers"]:
        covered |= set(re.findall(r"A\d+", f["Covers"][1]))
    if f["Files"]:
        n = len([x for x in f["Files"][1].split(",") if x.strip()])
        if not 1 <= n <= 3:
            out(a.plan, f["Files"][0], f"Task {t['id']}: Files count {n}, must be 1-3")
    tier = f["Tier"][1].strip("` ").lower() if f["Tier"] else None
    if f["Tier"] and tier not in ("strong", "standard", "fast"):
        out(a.plan, f["Tier"][0], f"Task {t['id']}: Tier '{tier}' not strong|standard|fast")
    if f["Risk flags"] and f["Risk flags"][1].strip("` ").lower() not in ("", "none") and tier != "strong":
        out(a.plan, f["Risk flags"][0], f"Task {t['id']}: risk flag without strong tier")

for x in aids:
    if x not in covered:
        out(spec, 1, f"{x}: A-id with no covering task")

# --- status checks ---
for tid, (i, ticked, h) in status.items():
    if not ticked:
        continue
    if not re.fullmatch(r"[0-9a-f]{7,40}", h):
        out(a.plan, i, f"Task {tid}: ticked without commit hash")
    elif not a.no_git and subprocess.run(["git", "cat-file", "-e", h + "^{commit}"],
                                         capture_output=True).returncode:
        out(a.plan, i, f"Task {tid}: commit {h} does not resolve")

# --- size warnings (cwd-relative, only if present) ---
for p, cap in (("AGENTS.md", 1500), ("docs/status.md", 300)):
    if os.path.isfile(p):
        w = len(open(p, encoding="utf-8").read().split())
        if w > cap:
            out(p, 1, f"{w} words, over {cap}", warn=True)

sys.exit(1 if fails else 0)
