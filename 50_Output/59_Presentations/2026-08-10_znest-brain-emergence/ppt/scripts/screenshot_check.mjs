import { chromium } from 'file:///C:/Users/LEO/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';

const BASE = 'http://127.0.0.1:8899/vault/50_Output/59_Presentations/2026-08-10_znest-brain-emergence/ppt';
const OUT = join('D:/Obsidian/vault/50_Output/59_Presentations/2026-08-10_znest-brain-emergence/ppt', 'shots');
mkdirSync(OUT, { recursive: true });

const targets = [
  { part: 1, pos: 1, file: 'part1_cover.png' },
  { part: 1, pos: 4, file: 'part1_p3_energy_gap.png' },
  { part: 1, pos: 18, file: 'part1_p17_neuron.png' },
  { part: 1, pos: 51, file: 'part1_closing.png' },
  { part: 2, pos: 13, file: 'part2_p61_intelligence_scale.png' },
  { part: 2, pos: 51, file: 'part2_closing.png' },
  { part: 3, pos: 3, file: 'part3_p100_tcc_topology.png' },
  { part: 3, pos: 51, file: 'part3_appendix.png' },
];

const browser = await chromium.launch({ headless: true, executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });

for (const t of targets) {
  const url = `${BASE}/part${t.part}/index.html?slide=${t.pos}`;
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2600);
  await page.screenshot({ path: join(OUT, t.file) });
  const imgState = await page.evaluate(() => {
    const imgs = [...document.querySelectorAll('img[data-image-slot]')];
    return { imgs: imgs.length, loaded: imgs.every((i) => i.complete && i.naturalWidth > 0) };
  });
  console.log(`${t.file}: slide=${t.pos} imgs=${imgState.imgs} loaded=${imgState.loaded}`);
}

await browser.close();
console.log(`screenshots written to ${OUT}`);
