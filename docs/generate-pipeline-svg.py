#!/usr/bin/env python3
"""Generate the README pipeline diagram as two static SVGs (light + dark).

Static SVG, not mermaid: GitHub's mermaid renderer collapsed this graph, and a
2110px-wide interactive canvas scaled into a ~900px README column produces
4px text. This is sized for the README column instead.

Inline presentation attributes only — no <style>, no script, no emoji — so it
renders identically wherever GitHub serves it.

    python3 docs/generate-pipeline-svg.py
"""

from pathlib import Path

W, H = 1168, 712
BOX_W, BOX_H, GAP = 200, 150, 22
COL_X = [40 + i * (BOX_W + GAP) for i in range(5)]
ROW_Y = [128, 352]

MONO_PX = 12.5                  # body/label size
MONO_CH = MONO_PX * 0.6         # monospace advance width
MAX_CH = int((BOX_W - 30) / MONO_CH)   # chars that fit inside a box line

THEMES = {
    "light": dict(
        bg="#FAF9F5", surface="#FFFFFF", ink="#141413", body="#3D3D3A",
        muted="#87867F", line="#D1CFC5", zone="#F4F2EA",
        clay="#D97757", claysoft="#FBEFE9", olive="#788C5D", olivesoft="#EFF2E8",
        gold="#B08A3E", goldsoft="#FAF3E2", blue="#4E7189",
    ),
    "dark": dict(
        bg="#141413", surface="#1F1F1D", ink="#FAF9F5", body="#D1CFC5",
        muted="#8F8E86", line="#3D3D3A", zone="#1A1A18",
        clay="#E48A6E", claysoft="#2E211C", olive="#9DB07C", olivesoft="#22261C",
        gold="#D4B36F", goldsoft="#2A2418", blue="#7FA3BC",
    ),
}

# (col, row, kicker, name, line1, line2_or_None, tag, kind)
# line2 is replaced by an agent chip when one is registered for that cell.
PHASES = [
    (0, 0, "PHASE 0", "Triage / Idea", "docs/backlog.md", "idea-level brainstorm", "pick 1 of 4 tracks", "plain"),
    (1, 0, "PHASE 1", "Validate", "docs/business/*.md", None, "B GATE  GO / NO-GO", "gate"),
    (2, 0, "PHASE 2", "Spec", "docs/specs/*.md", "+ acceptance checks", "check-spec (pre-push)", "plain"),
    (3, 0, "PHASE 2.5", "Clarify", "spec: Clarifications", "answers -> the spec", "nothing left in chat", "plain"),
    (4, 0, "PHASE 3", "Architecture", "docs/decisions/ ADR", None, "T: AI picks, ADR", "plain"),
    (0, 1, "PHASE 4", "Plan", "docs/plans/*.md", None, "check-plan (pre-push)", "plain"),
    (1, 1, "PHASE 5", "Execute", "feat/* branch", "red -> green -> commit", "ceiling 3/5 -> revert", "plain"),
    (2, 1, "PHASE 6", "QA / Review", "PR + docs/reviews/", None, "check-gate exit 0 (CI)", "plain"),
    (3, 1, "PHASE 7", "Release", "tag + runbook.md", "smoke + rollback", "B GATE  prod deploy", "gate"),
    (4, 1, "PHASE 8", "Retro", "docs/retro/*", "lessons written down", "feeds the backlog", "plain"),
]

# agent chips: (col, row, label) — occupies the line2 slot
AGENTS = [
    (1, 0, "product-critic"),
    (4, 0, "solution-architect"),
    (0, 1, "tech-lead-reviewer"),
    (2, 1, "qa-logic/qa-ui +2 more"),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(t):
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
      f'font-family="ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif" '
      f'role="img" aria-label="solo-sdlc nine phase pipeline">')
    a(f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>')
    a('<defs>')
    for name, col in (("ar", t["muted"]), ("arc", t["clay"]), ("arb", t["blue"])):
        a(f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
          f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>')
    a('</defs>')

    mono = 'ui-monospace, SFMono-Regular, Menlo, Consolas, monospace'

    # ── scratch enclosure around phases 0-1 ────────────────────────────
    sx, sy = COL_X[0] - 14, ROW_Y[0] - 40
    sw = (COL_X[1] + BOX_W + 14) - sx
    a(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{BOX_H + 54}" rx="14" fill="{t["zone"]}" '
      f'stroke="{t["line"]}" stroke-width="1" stroke-dasharray="5 5"/>')
    a(f'<text x="{sx + 14}" y="{sy + 22}" font-family="{mono}" font-size="13" fill="{t["muted"]}" '
      f'letter-spacing="0.08em">RUNS IN SCRATCH &#8212; NO REPO YET</text>')

    # ── forward arrows within each row ─────────────────────────────────
    for row in range(2):
        for c in range(4):
            x1 = COL_X[c] + BOX_W
            y = ROW_Y[row] + BOX_H / 2
            a(f'<path d="M{x1},{y} L{x1 + GAP - 4},{y}" stroke="{t["muted"]}" stroke-width="1.8" '
              f'fill="none" marker-end="url(#ar)"/>')

    # ── wrap arrow: phase 3 (row 0, col 4) -> phase 4 (row 1, col 0) ───
    wy = ROW_Y[0] + BOX_H + 52
    a(f'<path d="M{COL_X[4] + BOX_W / 2},{ROW_Y[0] + BOX_H} L{COL_X[4] + BOX_W / 2},{wy} '
      f'L{COL_X[0] + BOX_W / 2},{wy} L{COL_X[0] + BOX_W / 2},{ROW_Y[1] - 4}" '
      f'stroke="{t["muted"]}" stroke-width="1.8" fill="none" marker-end="url(#ar)"/>')

    # ── GO -> git init label on the 1 -> 2 hand-off ────────────────────
    gx = COL_X[1] + BOX_W + GAP / 2
    a(f'<text x="{gx}" y="{ROW_Y[0] - 10}" font-family="{mono}" font-size="13" fill="{t["gold"]}" '
      f'text-anchor="middle">GO &#8594; git init</text>')

    # ── loop-backs (blue, dashed) ──────────────────────────────────────
    # Labels sit clear of the curve: an "above" loop puts its text over the
    # apex, a "below" loop puts its text under the lowest point.
    def loop(c_from, c_to, row, depth, label, above=False):
        x0 = COL_X[c_from] + BOX_W * 0.35
        x1 = COL_X[c_to] + BOX_W * 0.65
        if above:
            y0 = ROW_Y[row]
            ym = y0 - depth
            ty = y0 - depth * 0.75 - 9
        else:
            y0 = ROW_Y[row] + BOX_H
            ym = y0 + depth
            ty = y0 + depth * 0.75 + 17
        a(f'<path d="M{x0},{y0} C{x0},{ym} {x1},{ym} {x1},{y0}" stroke="{t["blue"]}" '
          f'stroke-width="1.5" stroke-dasharray="4 4" fill="none" marker-end="url(#arb)" opacity="0.85"/>')
        a(f'<text x="{(x0 + x1) / 2}" y="{ty}" font-family="{mono}" font-size="12.5" '
          f'fill="{t["blue"]}" text-anchor="middle">{esc(label)}</text>')

    loop(4, 2, 0, 58, "architecture breaks the spec", above=True)
    loop(1, 0, 1, 34, "retry ceiling hit", above=False)
    loop(2, 1, 1, 72, "BLOCKING / CRITICAL", above=False)

    # retro -> phase 0, along the bottom
    ry = ROW_Y[1] + BOX_H + 104
    a(f'<path d="M{COL_X[4] + BOX_W * 0.5},{ROW_Y[1] + BOX_H} L{COL_X[4] + BOX_W * 0.5},{ry} '
      f'L{COL_X[0] + BOX_W * 0.2},{ry} L{COL_X[0] + BOX_W * 0.2},{ROW_Y[0] + BOX_H + 4}" '
      f'stroke="{t["blue"]}" stroke-width="1.5" stroke-dasharray="4 4" fill="none" '
      f'marker-end="url(#arb)" opacity="0.85"/>')
    a(f'<text x="{COL_X[3] + BOX_W / 2}" y="{ry - 8}" font-family="{mono}" '
      f'font-size="12.5" fill="{t["blue"]}" text-anchor="middle">'
      f'next round starts at phase 0</text>')

    # ── NO-GO exit ─────────────────────────────────────────────────────
    nx = COL_X[1] + BOX_W * 0.62
    ny = ROW_Y[0] + BOX_H
    a(f'<path d="M{nx},{ny} L{nx},{ny + 14}" stroke="{t["muted"]}" stroke-width="1.5" '
      f'stroke-dasharray="4 4" fill="none"/>')
    a(f'<text x="{nx + 8}" y="{ny + 28}" font-family="{mono}" font-size="12.5" fill="{t["muted"]}">'
      f'NO-GO: no repo, no regrets</text>')

    # ── phase boxes ────────────────────────────────────────────────────
    agent_at = {(c, r): lbl for c, r, lbl in AGENTS}
    for c, r, kicker, name, line1, line2, tag, kind in PHASES:
        x, y = COL_X[c], ROW_Y[r]
        fill = t["claysoft"] if kind == "gate" else t["surface"]
        stroke = t["clay"] if kind == "gate" else t["line"]
        a(f'<rect x="{x}" y="{y}" width="{BOX_W}" height="{BOX_H}" rx="11" fill="{fill}" '
          f'stroke="{stroke}" stroke-width="1.6"/>')
        a(f'<text x="{x + 15}" y="{y + 25}" font-family="{mono}" font-size="12" '
          f'fill="{t["clay"] if kind == "gate" else t["muted"]}" letter-spacing="0.08em">{kicker}</text>')
        a(f'<text x="{x + 15}" y="{y + 51}" font-size="19" font-weight="600" '
          f'fill="{t["ink"]}">{esc(name)}</text>')
        a(f'<text x="{x + 15}" y="{y + 76}" font-family="{mono}" font-size="{MONO_PX}" '
          f'fill="{t["body"]}">{esc(line1)}</text>')
        tagcol = t["clay"] if kind == "gate" else t["muted"]
        a(f'<text x="{x + 15}" y="{y + 137}" font-family="{mono}" font-size="{MONO_PX}" '
          f'fill="{tagcol}">{esc(tag)}</text>')
        chip = agent_at.get((c, r))
        if chip:
            a(f'<rect x="{x + 11}" y="{y + 90}" width="{BOX_W - 22}" height="28" rx="7" '
              f'fill="{t["olivesoft"]}" stroke="{t["olive"]}" stroke-width="1"/>')
            a(f'<text x="{x + BOX_W / 2}" y="{y + 109}" font-family="{mono}" font-size="{MONO_PX}" '
              f'fill="{t["olive"]}" text-anchor="middle">{esc(chip)}</text>')
        elif line2:
            a(f'<text x="{x + 15}" y="{y + 100}" font-family="{mono}" font-size="{MONO_PX}" '
              f'fill="{t["muted"]}">{esc(line2)}</text>')

    a(f'<text x="40" y="{H - 52}" font-family="{mono}" font-size="{MONO_PX}" fill="{t["muted"]}">'
      f'B = money, GO/NO-GO, prod deploy, destructive data, legal, scope cut, brand. '
      f'State lives in git; no one-phase-one-session.</text>')

    # ── legend ─────────────────────────────────────────────────────────
    ly = H - 24
    items = [
        (t["claysoft"], t["clay"], "B gate: the human stops here"),
        (t["olivesoft"], t["olive"], "agent: fresh ctx, opus/high"),
        (None, t["blue"], "loop-back when a gate fails"),
    ]
    lx = 40
    for fill, stroke, label in items:
        if fill:
            a(f'<rect x="{lx}" y="{ly - 11}" width="16" height="14" rx="4" fill="{fill}" '
              f'stroke="{stroke}" stroke-width="1.4"/>')
        else:
            a(f'<path d="M{lx},{ly - 4} L{lx + 16},{ly - 4}" stroke="{stroke}" stroke-width="1.8" '
              f'stroke-dasharray="4 4"/>')
        a(f'<text x="{lx + 25}" y="{ly}" font-family="{mono}" font-size="{MONO_PX}" '
          f'fill="{t["muted"]}">{esc(label)}</text>')
        lx += 25 + len(label) * MONO_CH + 34
    assert lx < W, f"legend overflows the canvas: {lx:.0f} > {W}"
    a('</svg>')
    return "\n".join(o) + "\n"


def check_widths():
    """Fail loudly rather than silently shipping text that overflows a box."""
    chips = {lbl for _, _, lbl in AGENTS}
    bad = []
    for c, r, kicker, name, line1, line2, tag, kind in PHASES:
        for field, s in (("line1", line1), ("line2", line2), ("tag", tag)):
            if s and len(s) > MAX_CH:
                bad.append(f"{name}.{field}: {len(s)} chars > {MAX_CH} ({s!r})")
    for lbl in chips:
        if len(lbl) > MAX_CH:
            bad.append(f"agent chip: {len(lbl)} chars > {MAX_CH} ({lbl!r})")
    if bad:
        raise SystemExit("text too wide for a %dpx box:\n  %s" % (BOX_W, "\n  ".join(bad)))


if __name__ == "__main__":
    check_widths()
    out = Path(__file__).parent
    for theme, palette in THEMES.items():
        p = out / f"pipeline-{theme}.svg"
        p.write_text(build(palette))
        print(f"wrote {p.relative_to(out.parent)} ({p.stat().st_size} bytes)")
