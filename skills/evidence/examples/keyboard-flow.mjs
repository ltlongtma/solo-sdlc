// Example: keyboard evidence for a button on a local app. Adapt url, selectors, probe and steps.
// Run: node keyboard-flow.mjs [outDir]   (app on :3000; default outDir docs/qa/evidence/<slug>)
import { recordEvidence } from '../scripts/evidence.mjs';

const target = '#submit'; // placeholder selector

const result = await recordEvidence({
  url: 'http://localhost:3000/',
  slug: 'a1-keyboard',
  outDir: process.argv[2],
  ready: target,
  // Instrument what headless cannot show, e.g. count file-input clicks (no native dialog in headless).
  setup: () => {
    window.__fileInputClicks = 0;
    const orig = HTMLInputElement.prototype.click;
    HTMLInputElement.prototype.click = function () {
      if (this.type === 'file') return void window.__fileInputClicks++;
      return orig.call(this);
    };
  },
  probe: (page) =>
    page.evaluate((sel) => {
      const a = document.activeElement;
      return {
        activeId: a?.id || a?.tagName || null,
        targetFocusVisible: document.querySelector(sel)?.matches(':focus-visible') ?? false,
        fileInputClickCount: window.__fileInputClicks,
      };
    }, target),
  steps: [
    { caption: 'Start: nothing focused', claim: 'Target not yet focused' },
    { caption: 'Press Tab: focus moves to the target', claim: 'Target is Tab-reachable and shows a focus ring', act: (p) => p.keyboard.press('Tab') },
    { caption: 'Press Enter: opens the file dialog', claim: 'Enter opens the file dialog', act: (p) => p.keyboard.press('Enter'), traceOnly: 'headless has no native file dialog' },
  ],
});
console.log(result);
