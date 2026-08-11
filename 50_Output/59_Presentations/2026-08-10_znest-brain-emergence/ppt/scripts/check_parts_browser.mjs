import { chromium } from 'file:///C:/Users/LEO/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs';

const BASE = 'http://127.0.0.1:8899/vault/50_Output/59_Presentations/2026-08-10_znest-brain-emergence/ppt';
const PARTS = ['part1', 'part2', 'part3'];

const browser = await chromium.launch({ headless: true, executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });

let failed = false;
for (const part of PARTS) {
  const consoleErrors = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  await page.goto(`${BASE}/${part}/index.html`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1800);
  await page.evaluate(() => window.__setLowPowerMode?.(true, { persist: false }));
  await page.waitForTimeout(300);
  const report = await page.evaluate(() => {
    const slides = [...document.querySelectorAll('.slide')];
    const overflow = [];
    slides.forEach((s, i) => {
      const r = s.getBoundingClientRect();
      if (s.scrollWidth > Math.ceil(r.width) + 1 || s.scrollHeight > Math.ceil(r.height) + 1) {
        overflow.push(`${i + 1}:${s.scrollWidth}/${Math.ceil(r.width)} ${s.scrollHeight}/${Math.ceil(r.height)}`);
      }
    });
    const imgs = [...document.querySelectorAll('img[data-image-slot]')];
    return {
      total: slides.length,
      overflow,
      images: imgs.length,
      imagesLoaded: imgs.filter((i) => i.complete && i.naturalWidth > 0).length,
      title: document.title,
    };
  });
  console.log(JSON.stringify({ part, ...report, consoleErrors }, null, 2));
  if (report.total !== 51 || report.overflow.length || report.imagesLoaded !== report.images || consoleErrors.length) failed = true;
}

await browser.close();
console.log(failed ? 'BROWSER CHECK FAILED' : 'BROWSER CHECK PASSED');
process.exit(failed ? 1 : 0);
