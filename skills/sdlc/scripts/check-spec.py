#!/usr/bin/env python3
"""Check a spec file: requirement IDs, acceptance lines, UI states.

Usage: check-spec.py SPEC.md [SPEC.md ...]
Prints `path:line: problem` per failure; exit 1 if any, else 0.
"""
import re
import sys

KINDS = "e2e|integration|unit|human-B"


def sections(lines):
    """Map lowercase heading -> (heading line no, [(line no, text)]). Header bullets under ''."""
    out, cur = {"": (0, [])}, ""
    for n, text in enumerate(lines, 1):
        if text.startswith("## "):
            cur = text[3:].strip().lower()
            out[cur] = (n, [])
        else:
            out[cur][1].append((n, text))
    return out


def find(secs, prefix):
    for name, val in secs.items():
        if name and name.startswith(prefix):
            return val
    return None


def table_rows(body):
    """Data rows of the first table: (line no, cells); skips header and separator."""
    rows = [(n, [c.strip() for c in t.strip().strip("|").split("|")])
            for n, t in body if t.lstrip().startswith("|")]
    return [r for r in rows[1:] if not re.fullmatch(r"[\s:|-]+", "|".join(r[1]))]


def header_value(body, key):
    for _, t in body:
        m = re.match(rf"\s*-\s*\*\*{key}:\*\*\s*(.*)", t)
        if m:
            return m.group(1).strip()
    return ""


def is_set(v):
    return v.lower() not in ("", "none") and not re.fullmatch(r"<.*>", v)


def check(path):
    with open(path, encoding="utf-8") as f:
        secs = sections(f.read().splitlines())
    errs = []

    req = find(secs, "requirements")
    if req is None:
        errs.append((1, "missing section: ## Requirements"))
    else:
        for n, cells in table_rows(req[1]):
            if not re.fullmatch(r"R\d+", cells[0]):
                errs.append((n, f"requirement row has no R<n> id: {cells[0]!r}"))

    acc = find(secs, "acceptance")
    if acc is None:
        errs.append((1, "missing section: ## Acceptance"))
    else:
        seen = {}
        for n, t in acc[1]:
            if not re.match(r"\s*-\s*\[[ xX]\]", t):
                if re.search(r"\*\*A\d+\*\*", t):
                    errs.append((n, "acceptance id on a non-checkbox line (use '- [ ]' or '- [x]')"))
                continue
            m = re.search(r"\*\*(A\d+)\*\*", t)
            if not m:
                errs.append((n, "acceptance line has no **A<n>** id"))
            elif m.group(1) in seen:
                errs.append((n, f"duplicate acceptance id {m.group(1)} (first at line {seen[m.group(1)]})"))
            else:
                seen[m.group(1)] = n
            if len(re.findall(rf"Verify by:\s*(?:{KINDS})\b", t)) != 1 or t.count("Verify by:") != 1:
                errs.append((n, f"acceptance line needs exactly one 'Verify by: {KINDS}'"))

    head = secs[""][1]
    if header_value(head, "UI").lower() == "yes" or is_set(header_value(head, "Design source")):
        ui = find(secs, "ui states")
        if ui is None:
            errs.append((1, "UI spec but missing section: ## UI states"))
        elif not any(not re.search(r"<[^>]*>", "|".join(c)) for _, c in table_rows(ui[1])):
            errs.append((ui[0], "UI spec needs at least one UI states row without <placeholder>"))

    return [f"{path}:{n}: {msg}" for n, msg in sorted(errs)]


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if argv else 1
    problems = [p for path in argv for p in check(path)]
    print("\n".join(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
