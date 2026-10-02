// Record captioned browser evidence: MP4 + per-step storyboard + state trace + PR snippet.
// Usage: import { recordEvidence } from '<skill>/scripts/evidence.mjs' from a spec file, then `node spec.mjs [outDir]`.
import { chromium } from 'playwright-core';
import { execFileSync } from 'node:child_process';
import { mkdirSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const ffmpeg = (...args) => execFileSync('ffmpeg', ['-v', 'error', '-y', ...args]);

const CAPTION_CSS =
  'position:fixed;left:0;right:0;bottom:0;padding:16px 24px;background:#000;color:#fff;' +
  'font:bold 20px ui-monospace,Menlo,monospace;z-index:2147483647;pointer-events:none';

/**
 * @param {object} o
 * @param {string} o.url            Page to record (e.g. http://localhost:3000/).
 * @param {string} o.slug           File prefix, e.g. "a3-keyboard".
 * @param {string} o.outDir         Where the artifacts go. Default: docs/qa/evidence/<slug>.
 * @param {string} o.ready          Selector that proves the app (not the chrome) rendered.
 * @param {(page) => Promise<object>} o.probe  Reads the state the claims are about. Must be JSON-serialisable.
 * @param {{caption: string, claim: string, act?: (page) => Promise<void>, traceOnly?: string}[]} o.steps
 *        caption: what the viewer reads (no number, it is added). claim: row text for the PR table.
 *        traceOnly: set when the claim cannot be seen on screen (e.g. native file dialog in headless) — says why.
 * @param {(page) => Promise<void>} [o.setup]  Runs in every document before page scripts (addInitScript body).
 * @param {{width: number, height: number}} [o.viewport]
 * @param {number} [o.holdMs]       Time each step's result stays on screen. Min 1000 so every caption lands in the video.
 */
export async function recordEvidence(o) {
  const viewport = o.viewport ?? { width: 1000, height: 500 };
  const holdMs = Math.max(1000, o.holdMs ?? 1500);
  const out = o.outDir ?? join('docs', 'qa', 'evidence', o.slug);
  mkdirSync(out, { recursive: true });
  const tmp = join(out, `.${o.slug}.tmp`);
  rmSync(tmp, { recursive: true, force: true });
  mkdirSync(tmp, { recursive: true });

  const browser = await chromium.launch({ channel: process.env.EVIDENCE_CHANNEL ?? 'chrome' });
  const context = await browser.newContext({ viewport, recordVideo: { dir: tmp, size: viewport } });
  if (o.setup) await context.addInitScript(o.setup);
  const page = await context.newPage();
  const videoStart = Date.now();
  await page.goto(o.url);
  await page.waitForSelector(o.ready);

  const setCaption = (text) =>
    page.evaluate(
      ([text, css]) => {
        let bar = document.getElementById('__evidence_caption');
        if (!bar) {
          bar = document.createElement('div');
          bar.id = '__evidence_caption';
          bar.style.cssText = css;
          document.body.appendChild(bar);
        }
        bar.textContent = text;
      },
      [text, CAPTION_CSS],
    );

  const trace = [];
  let firstStepAt;
  for (const [i, s] of o.steps.entries()) {
    const caption = `${i + 1}. ${s.caption}`;
    await setCaption(caption); // caption before acting
    if (s.act) await s.act(page);
    await setCaption(caption); // re-apply in case the action navigated
    await page.waitForTimeout(300); // let the result paint before probing/screenshotting
    const at = Date.now() - videoStart;
    firstStepAt ??= at - 300;
    trace.push({ step: i + 1, caption, t: at - firstStepAt, state: await o.probe(page) });
    // Storyboard frame = screenshot of this exact step, never a time-sampled video frame.
    await page.screenshot({ path: join(tmp, `frame-${String(i + 1).padStart(2, '0')}.png`) });
    await page.waitForTimeout(holdMs - 300);
  }

  await context.close();
  await browser.close();

  const raw = join(tmp, readdirSync(tmp).find((f) => f.endsWith('.webm')));
  const mp4 = join(out, `${o.slug}.mp4`);
  const storyboard = join(out, `${o.slug}.storyboard.png`);
  const strip = join(out, `${o.slug}.captions.png`);
  const traceFile = join(out, `${o.slug}.trace.json`);
  // ponytail: video offset assumes recordVideo starts at newContext; good to ~100ms, trace stays the timing source.
  const trimFrom = (firstStepAt / 1000).toFixed(2);
  ffmpeg('-ss', trimFrom, '-i', raw, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', mp4);

  const frames = readdirSync(tmp).filter((f) => f.startsWith('frame-'));
  const cols = frames.length <= 4 ? 2 : 3;
  const rows = Math.ceil(frames.length / cols);
  ffmpeg('-framerate', '1', '-i', join(tmp, 'frame-%02d.png'), '-vf', `tile=${cols}x${rows}:color=0x333333:padding=4`, '-frames:v', '1', storyboard);
  // Caption bar sampled at 4 fps across the whole MP4 — read it back to confirm every caption made it into the video.
  const barH = 60;
  ffmpeg('-i', mp4, '-vf', `crop=${viewport.width}:${barH}:0:${viewport.height - barH},fps=4,tile=1x${Math.ceil(((trace.length * holdMs) / 1000) * 4) + 2}`, '-frames:v', '1', strip);

  // Hard asserts: the three artifacts must describe the same steps.
  if (frames.length !== o.steps.length || trace.length !== o.steps.length) {
    throw new Error(`mismatch: ${o.steps.length} steps, ${trace.length} trace entries, ${frames.length} storyboard frames`);
  }
  trace.forEach((e, i) => {
    if (e.step !== i + 1) throw new Error(`step numbering gap at trace[${i}]`);
  });

  writeFileSync(traceFile, JSON.stringify(trace, null, 2) + '\n');
  rmSync(tmp, { recursive: true, force: true });

  const snippet = prSnippet(o, trace);
  writeFileSync(join(out, `${o.slug}.pr.md`), snippet);
  return { mp4, storyboard, strip, trace: traceFile, pr: join(out, `${o.slug}.pr.md`), steps: trace.length };
}

const fmt = (v) => (typeof v === 'string' ? `"${v}"` : JSON.stringify(v));

/** Table rows show only what changed versus the previous step, so each row states its own proof. */
function prSnippet(o, trace) {
  const rows = trace.map((e, i) => {
    const prev = trace[i - 1]?.state;
    const keys = Object.keys(e.state).filter((k) => !prev || fmt(prev[k]) !== fmt(e.state[k]));
    const result = keys.map((k) => `\`${k}: ${prev ? `${fmt(prev[k])} → ` : ''}${fmt(e.state[k])}\``).join(', ') || 'no change';
    const s = o.steps[i];
    const seen = s.traceOnly ? `trace only (${s.traceOnly})` : `frame ${i + 1}, ~${(e.t / 1000).toFixed(1)}s`;
    return `| ${i + 1} | ${s.claim} | ${result} | ${seen} |`;
  });
  return [
    '<!-- Replace {BASE} with where the files are hosted, e.g. https://github.com/<org>/<repo>/blob/<sha>/docs/qa/evidence/<slug> -->',
    '## PR evidence',
    '',
    `![Storyboard: ${trace.map((e) => e.caption.replace(/^\d+\.\s*/, '')).join(' → ')}]({BASE}/${o.slug}.storyboard.png?raw=true)`,
    '',
    `- Recording (MP4): {BASE}/${o.slug}.mp4`,
    `- State trace (JSON, read after each step): {BASE}/${o.slug}.trace.json`,
    '',
    '| Step | Claim | Trace result | Where to see it |',
    '|---|---|---|---|',
    ...rows,
    '',
  ].join('\n');
}
