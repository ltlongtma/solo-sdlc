#!/usr/bin/env python3
"""Fail if any skill, agent, or command frontmatter is not strict YAML.

Claude Code parses frontmatter leniently, so a description containing an
unquoted ": " loads fine there and silently breaks every other harness. APM
aborts the whole package with "mapping values are not allowed in this context",
which is how this check earned its place.

Usage: python3 docs/check-frontmatter.py   (from the repo root)
"""

import glob
import sys

import yaml

TARGETS = (
    glob.glob("skills/**/SKILL.md", recursive=True)
    + glob.glob("agents/*.md")
    + glob.glob("commands/*.md")
)

failures = []
for path in sorted(TARGETS):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---\n"):
        failures.append((path, "no frontmatter block"))
        continue
    try:
        data = yaml.safe_load(text.split("---\n", 2)[1])
    except yaml.YAMLError as exc:
        failures.append((path, str(exc).splitlines()[0]))
        continue
    if not isinstance(data, dict):
        failures.append((path, "frontmatter is not a mapping"))
    elif "description" not in data:
        failures.append((path, "no description field"))

for path, why in failures:
    print(f"FAIL {path}: {why}", file=sys.stderr)

if failures:
    sys.exit(f"\n{len(failures)} file(s) with unusable frontmatter.")
print(f"{len(TARGETS)} frontmatter blocks parse as strict YAML.")
