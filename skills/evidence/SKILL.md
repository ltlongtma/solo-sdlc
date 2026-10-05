---
name: evidence
description: "Use when a PR, bug fix or UI acceptance criterion needs browser proof: records a captioned MP4, a per-step storyboard PNG, a state trace JSON and a ready-to-paste PR evidence section whose rows match the storyboard tiles 1:1. Good for keyboard/focus flows, multi-step interactions, loading states, bug before/after, or when asked for \"video evidence\", \"record the flow\", \"storyboard\" or \"screenshots for the PR\". Portable: Node + playwright-core + ffmpeg."
---

# Browser evidence

Three artifacts that must tell the same story, plus the PR text built from them. Default output: `docs/qa/evidence/<A-id or slug>/` (the place `qa-ui` expects; pass `outDir` to override).

| File | For | Built from |
|---|---|---|
| `<slug>.mp4` | Inline video player in the PR | Playwright `recordVideo`, trimmed to the first step |
| `<slug>.storyboard.png` | Inline image in the PR | **One screenshot per step**, taken right after that step's probe |
| `<slug>.trace.json` | Proof of claims the eye can't check | `probe()` after every step |
| `<slug>.captions.png` | Your own check | Caption bar of the MP4 sampled at 4 fps |
| `<slug>.pr.md` | Paste into the PR | Trace diff per step, one row per storyboard tile |

Static end states don't need this; a screenshot is enough.

## Rules

A time-sampled storyboard can silently drop a step (a caption with 0 video frames shows tiles 1, 2, 4 while the table says 4 steps). These rules make that impossible:

1. **Storyboard = per-step screenshots**, never evenly time-sampled video frames. (Time-sampled grids only for motion claims: scroll, drag, animation, and then in addition.)
2. **Hard assert:** steps == trace entries == storyboard tiles, numbered 1..N with no gap. The script throws otherwise.
3. **Hold >= 1000 ms per step** so every caption lands in the video.
4. **Read back `captions.png`**: every caption `1..N` must appear. Read back the storyboard: each tile shows what its caption claims.
5. **One table row per tile.** A claim the screen can't show (native file dialog in headless, a network call) is marked `trace only (<reason>)`, never implied by a frame.
6. **Captions are user-facing text:** proofread. Phrase as the user acts: "Press Tab: focus moves to the button".

## Setup (once per machine)

```bash
cd <this skill>/scripts && npm i            # playwright-core
npx playwright-core install ffmpeg           # Playwright's video encoder
which ffmpeg                                 # system ffmpeg for trim/tile (brew install ffmpeg)
```

Uses installed Google Chrome (`channel: 'chrome'`). Set `EVIDENCE_CHANNEL=chromium` after `npx playwright-core install chromium` if Chrome is absent.

## Workflow

1. **Write claims first.** One step per user action, each with the claim it proves and the state field(s) that prove it. In the sdlc pipeline, tie the slug to the acceptance id (`a3-keyboard`).
2. **Start the app** and note its URL (e.g. `http://localhost:3000`).
3. **Write a spec** in a scratch dir (not the repo), modelled on `examples/keyboard-flow.mjs`:
   - `ready`: selector scoped to the app root, so hidden markup can't match.
   - `setup`: init-script to instrument what headless can't show (see Gotchas).
   - `probe`: return only the fields the claims are about.
   - `steps`: `{ caption, claim, act?, traceOnly? }`. Real input only (`page.keyboard`, `page.mouse`); never set state via `evaluate` to fake an interaction.
4. **Run:** `node spec.mjs [outDir]`. It throws on any step/trace/tile mismatch.
5. **Verify** before citing anything:
   - Open `<slug>.storyboard.png`: N tiles, captions 1..N, each tile shows its claim.
   - Open `<slug>.captions.png`: every caption present.
   - `ffprobe -v error -show_entries format=duration:stream=width,height -of compact <slug>.mp4`.
   - Check frames for secrets / personal data before anything leaves the machine.
6. **Host the trace** (ask the user before any commit/push): commit `<slug>.trace.json` to a dedicated branch (never the PR's code branch), push, and use the pinned commit URL as `{BASE}`, e.g. `https://github.com/<org>/<repo>/blob/<sha>/docs/qa/evidence/<slug>`. Never host the MP4 this way: GitHub shows a repo-blob `.mp4` as a download link, not a player.
7. **Fill the PR** from the output directory, uploading the media with GitHub CLI >= 2.102 (needs push access to the repo):
   ```bash
   gh pr edit <n> --body-file <slug>.pr.md --attach ./<slug>.storyboard.png --attach ./<slug>.mp4
   ```
   `--attach` uploads each file to `github.com/user-attachments/assets/…` (the drag-drop store, the only host GitHub renders as a video player) and swaps the matching `./<slug>.*` reference for the uploaded URL. If you adapt the section into a repo template, keep each `![](./<slug>.mp4)` alone in its own paragraph; inside a sentence or list item it renders as a link. Size cap: 10 MB per video on free plans, 100 MB on paid. Without `gh --attach`, drag-drop the MP4 into the PR editor instead; never fall back to a blob link.
   Re-read the body (`gh pr view <n> --json body`): every video line must be a lone `https://github.com/user-attachments/assets/…` URL.
8. **Ledger (sdlc):** reference the files from `docs/qa/ledger.tsv` evidence column (e.g. `docs/qa/evidence/a3-keyboard/a3-keyboard.storyboard.png`).

## PR evidence section

`<slug>.pr.md` generates this generic section; paste it where the repo wants evidence, or adapt it to the repo's own PR template (keep the template's sections and order, fill only its screenshots/testing parts):

```markdown
## PR evidence

![Storyboard: …](./<slug>.storyboard.png)

![](./<slug>.mp4)

- State trace (JSON, read after each step): {BASE}/<slug>.trace.json

| Step | Claim | Trace result | Where to see it |
|---|---|---|---|
| 1 | … | `field: value` | frame 1, ~0.3s |
| 3 | … | `fileInputClickCount: 0 → 1` | trace only (headless has no native file dialog) |
```

If some rows are trace-only, add one line saying why those frames look identical.

## Gotchas

- **Native file dialog:** headless can't show it. In `setup`, wrap `HTMLInputElement.prototype.click` and count calls where `this.type === 'file'`; mark those rows `traceOnly`.
- **Focus ring:** probe `el.matches(':focus-visible')`, not a class name.
- **First load can be slow.** The MP4 is trimmed to the first step, so load time doesn't matter; the `ready` selector does.
- **Trace timing** comes from the wall clock; video offsets in the table are approximate (`~`). Timing claims cite the trace.
- **Navigation** removes the caption bar; the script re-applies it after each `act`.
- **Motion claims:** add mid-transition probes inside `act` and, if useful, a time-sampled grid (`ffmpeg -i <slug>.mp4 -vf "fps=12/<D>,scale=400:-1,tile=4x3" -frames:v 1 motion.png`) *in addition to* the per-step storyboard.
