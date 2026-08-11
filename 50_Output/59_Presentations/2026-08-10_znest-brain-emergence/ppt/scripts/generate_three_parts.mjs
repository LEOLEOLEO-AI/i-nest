#!/usr/bin/env node
/*
 * Generates the three-part academic deck from outline.json using the guizang
 * Swiss template. Each part is a standalone single-file HTML deck.
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const SKILL_ROOT = 'C:/Users/LEO/.codex/skills/guizang-ppt-skill';
const template = readFileSync(join(SKILL_ROOT, 'assets/template-swiss.html'), 'utf8');
const outline = JSON.parse(readFileSync(join(ROOT, 'outline.json'), 'utf8'));
const slides = outline.slides;

const DECK_TITLE = '智涌脑 · iNEST';
const IMAGES = new Map([
  [1, 'cover_network_glow.png'],
  [3, 'energy_gap.png'],
  [4, 'four_walls.png'],
  [5, 'scaling_collapse.png'],
  [17, 'neuron_vs_synapse.png'],
  [20, 'water_phases.png'],
  [22, 'crystal_lattices.png'],
  [23, 'insulin_disulfide.png'],
  [24, 'connectome_302.png'],
  [25, 'topology_function.png'],
  [32, 'linear_vs_nonlinear.png'],
  [34, 'cascade_gain.png'],
  [36, 'emergence_physics.png'],
  [46, 'cst_formula.png'],
  [61, 'intelligence_scale.png'],
  [72, 'sdde_echo.png'],
  [80, 'local_rules_loop.png'],
  [87, 'criticality_powerlaw.png'],
  [97, 'sdi_control.png'],
  [100, 'tcc_topology.png'],
  [116, 'three_generations.png'],
  [122, 'five_partners.png'],
  [126, 'funding_channels.png'],
  [139, 'industry_radar.png'],
  [146, 'closing_soil_glow.png'],
]);

const FALLBACK_LAYOUT = {
  2: 'S03', 6: 'S03', 7: 'S03', 8: 'S19', 9: 'S03',
  10: 'S13', 11: 'S21', 12: 'S03', 13: 'S03', 14: 'S03', 15: 'S03', 16: 'S03',
  18: 'S04', 19: 'S03', 21: 'S02', 26: 'S03', 27: 'S03', 28: 'S03',
  29: 'S16', 30: 'S12', 31: 'S03', 33: 'S12', 35: 'S22', 36: 'S03',
  37: 'S22', 38: 'S12', 39: 'S03', 40: 'S08', 41: 'S09', 42: 'S05',
  43: 'S03', 44: 'S04', 45: 'S04', 47: 'S03', 48: 'S04', 49: 'S04',
  50: 'S13', 51: 'S13', 52: 'S13', 53: 'S22', 54: 'S22', 55: 'S22', 56: 'S03',
  57: 'S03', 58: 'S03', 59: 'S09', 60: 'S12', 62: 'S22', 63: 'S09',
  64: 'S03', 65: 'S20', 66: 'S07', 67: 'S14', 68: 'S03', 69: 'S03',
  70: 'S09', 71: 'S03', 73: 'S03', 74: 'S03', 75: 'S09', 76: 'S03',
  77: 'S22', 78: 'S03', 79: 'S03', 81: 'S03', 82: 'S03', 83: 'S03',
  84: 'S03', 85: 'S03', 86: 'S19', 88: 'S14', 89: 'S04', 90: 'S22',
  91: 'S03', 92: 'S09', 93: 'S19', 94: 'S22', 95: 'S22', 96: 'S03',
  98: 'S03', 99: 'S03', 101: 'S16', 102: 'S22', 103: 'S22', 104: 'S03',
  105: 'S22', 106: 'S07', 107: 'S04', 108: 'S22', 109: 'S03', 110: 'S03',
  111: 'S19', 112: 'S21', 113: 'S19', 114: 'S22', 115: 'S19', 117: 'S04',
  118: 'S05', 119: 'S22', 120: 'S12', 121: 'S04', 123: 'S05', 124: 'S22',
  125: 'S16', 127: 'S16', 128: 'S16', 129: 'S16', 130: 'S16', 131: 'S22',
  132: 'S03', 133: 'S20', 134: 'S20', 135: 'S20', 136: 'S19', 137: 'S16',
  138: 'S11', 140: 'S04', 141: 'S11', 142: 'S03', 143: 'S16', 144: 'S22',
  145: 'S04',
};

const LAYOUTS_BY_IMAGE = {
  3: 'S22', 4: 'S22', 17: 'S22', 20: 'S22', 22: 'S22', 23: 'S22',
  24: 'S22', 25: 'S22', 34: 'S22', 35: 'S22', 37: 'S22', 46: 'S22',
  53: 'S22', 54: 'S22', 55: 'S22', 61: 'S22', 62: 'S22', 72: 'S22',
  77: 'S22', 80: 'S22', 87: 'S22', 90: 'S22', 94: 'S22', 95: 'S22',
  97: 'S22', 100: 'S22', 102: 'S22', 103: ' ',
};

const ACT_INDEX = new Map();
outline.acts.forEach((act, i) => {
  const m = act.match(/^(第.+幕)\s*(.+?)（P(\d+)–P(\d+)）$/);
  if (m) ACT_INDEX.set(i + 1, { label: m[1], name: m[2], start: +m[3], end: +m[4] });
});

function esc(s = '') {
  return String(s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function pad(n) { return String(n).padStart(2, '0'); }

function splitItems(text) {
  const cleaned = String(text || '')
    .replace(/[ \t]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  if (!cleaned) return [];
  const parts = cleaned
    .split(/[；;。！？!?]|(?:——|—|：|:)/)
    .map((p) => p.replace(/^[①②③④⑤⑥⑦⑧⑨⑩]|^[一二三四五六七八九十]+、?/, '').replace(/^\s+|\s+$/g, ''))
    .filter((p) => p && p.length >= 2);
  if (!parts.length) return [cleaned];
  return parts;
}

function cardTitle(item) {
  const t = item.replace(/^[（(【\[]?[^）)】\]]*[）)】\]]?\s*/, '').trim();
  const cut = t.length > 14 ? t.slice(0, 14) + '…' : t;
  return cut;
}

function chrome(part, num, total, label = '') {
  return `<div class="chrome-min"><div class="l">${esc(DECK_TITLE)} · PART ${part} ${label ? '· ' + esc(label) : ''}</div><div class="r">${pad(num)} / ${pad(total)}</div></div>`;
}

function titleBlock(title, opts = {}) {
  const len = [...String(title)].length;
  let size = 'min(5.4vw,9.4vh)';
  if (len <= 8) size = 'min(6.2vw,10.8vh)';
  else if (len <= 12) size = 'min(5.6vw,9.8vh)';
  else if (len <= 18) size = 'min(4.9vw,8.6vh)';
  else size = 'min(4.4vw,7.8vh)';
  return `<div data-anim="line" style="display:flex;flex-direction:column;gap:1.4vh">
    <div class="t-cat accent">${esc(opts.kicker || 'BRAIN SCIENCE · EMERGENCE')}</div>
    <h2 class="h-xl-zh" style="font-size:${size};line-height:1.08;color:${opts.color || 'var(--text-primary)'}">${esc(title)}</h2>
  </div>`;
}

function sourceLine(slide, dark = false) {
  const parts = [];
  const f = slide.fields || {};
  if (f['依据']) parts.push('[引用] ' + f['依据']);
  if (f['公式']) parts.push('[推导] ' + f['公式']);
  if (f['备注'] && !parts.length) parts.push('[引用] 提纲备注：' + f['备注']);
  if (f['图示'] && !parts.length) parts.push('[引用] 提纲图示：' + f['图示']);
  if (!parts.length) parts.push('[引用] 提纲 P' + slide.num);
  const color = dark ? 'rgba(255,255,255,.6)' : 'var(--text-helper)';
  return `<div class="t-meta" style="color:${color};margin-top:2.2vh">${esc(parts.join(' · '))}</div>`;
}

function footnoteBlock(text, dark = false) {
  if (!text) return '';
  const color = dark ? 'rgba(255,255,255,.58)' : 'var(--text-helper)';
  return `<div class="t-meta" style="color:${color};margin-top:2.4vh">${esc(text)}</div>`;
}

function cardGrid(items, opts = {}) {
  const cols = opts.cols || (items.length === 6 ? 3 : items.length === 4 ? 4 : 3);
  const rows = items.length > 6 ? 2 : 1;
  const cards = items.map((item, i) => {
    const accent = opts.accentIndex != null ? i === opts.accentIndex : i === items.length - 1;
    const fill = accent ? 'card-accent' : 'card-fill';
    const titleColor = accent ? 'var(--accent-on)' : 'var(--text-primary)';
    const bodyColor = accent ? 'rgba(255,255,255,.88)' : 'var(--text-secondary)';
    return `<article class="${fill}" style="padding:2.4vh 1.5vw;display:flex;flex-direction:column;gap:1vh;min-height:24vh">
      <div class="t-meta" style="color:${accent ? 'rgba(255,255,255,.72)' : 'var(--text-helper)'}">${pad(i + 1)} / ${pad(items.length)}</div>
      <h3 class="t-h-prod" style="font-size:max(20px,1.35vw);color:${titleColor}">${esc(cardTitle(item))}</h3>
      <p class="t-body-sm" style="font-size:max(18px,1.06vw);color:${bodyColor};margin-top:auto">${esc(item)}</p>
    </article>`;
  });
  return `<div data-anim="up" style="display:grid;grid-template-columns:repeat(${cols},1fr);grid-template-rows:repeat(${rows},1fr);gap:1.6vh 1.5vw;margin-top:5vh;flex:1;align-content:stretch">${cards.join('')}</div>`;
}

/* ---------- layout builders ---------- */

function layoutS22(slide, part, num, total, imgFile, bodyItems) {
  const f = slide.fields || {};
  const stats = bodyItems.slice(0, 3);
  const statHtml = stats.map((item, i) => {
    const valMatch = item.match(/(\d+(?:\.\d+)?(?:\s*[万亿兆])?(?:\s*[⁰¹²³⁴⁵⁶⁷⁸⁹]+)?(?:\s*[–—~～-]\s*\d+(?:\.\d+)?(?:\s*[万亿兆])?)?\s*(?:W|MW|瓦|倍|%|级)?)/);
    const val = valMatch ? valMatch[1].trim() : (['A', 'B', 'C'][i]);
    const label = ['KEY 01', 'KEY 02', 'KEY 03'][i];
    return `<div style="display:flex;flex-direction:column;gap:.6vh">
      <div style="height:1px;background:var(--ink)"></div>
      <div class="t-meta">${label}</div>
      <div style="font-family:var(--sans);font-weight:200;font-size:min(4vw,6.8vh);line-height:.98;letter-spacing:-.02em;color:${i === 2 ? 'var(--accent)' : 'var(--text-primary)'}">${esc(val)}</div>
      <div style="height:1px;background:var(--border-subtle);margin-top:auto"></div>
      <p class="body-sm" style="font-size:max(16px,.98vw)">${esc(item)}</p>
    </div>`;
  }).join('');
  const note = f['备注'] ? `<p class="t-body-sm" style="font-size:max(17px,1vw);color:var(--text-secondary)">${esc(f['备注'])}</p>` : '';
  return `<section class="slide" data-layout="S22" data-animate="image-hero">
  <div class="canvas-card" style="padding:0;display:flex;flex-direction:column;overflow:hidden">
    <div data-anim="img" style="position:relative;flex:0 0 58%;overflow:hidden;background:var(--grey-1)">
      <img src="../images/${imgFile}" alt="P${slide.num} 配图" loading="eager" data-image-slot="s22-hero-21x9" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 42%">
      <div class="chrome-min" style="position:absolute;top:0;left:0;right:0;color:rgba(255,255,255,.92);padding:3.6vh 5vw 0">
        <div class="l">${esc(slide.act || 'BRAIN SCIENCE')}</div>
        <div class="r">${pad(num)} / ${pad(total)}</div>
      </div>
      <div data-anim="title-block" style="position:absolute;left:5vw;top:8vh;background:var(--paper);padding:2.8vh 2.8vw;max-width:46vw">
        <div class="t-cat accent" style="margin-bottom:1vh">${esc(f['依据'] ? 'EVIDENCE · SOURCED' : 'VISUAL EVIDENCE')}</div>
        <div style="font-family:var(--sans),var(--sans-zh);font-weight:700;font-size:min(3.8vw,6.8vh);line-height:1.06;letter-spacing:0;color:var(--text-primary)">${esc(slide.title)}</div>
      </div>
    </div>
    <div data-anim="kpi" class="image-hero-body">
      <div style="display:flex;flex-direction:column;gap:1.6vh">
        <div class="t-cat accent">CORE CLAIM</div>
        <div style="font-family:var(--sans),var(--sans-zh);font-weight:700;font-size:max(20px,1.5vw);line-height:1.42;color:var(--text-primary)">${esc(bodyItems.join('；') || f['body'] || '')}</div>
        ${note}
        <div class="t-meta" style="color:var(--text-helper);margin-top:auto">[引用] 提纲 P${slide.num}</div>
      </div>
      <div class="image-hero-stats" style="gap:2.6vw">${statHtml}</div>
    </div>
  </div>
</section>`;
}

function layoutS03(slide, part, num, total, items) {
  const f = slide.fields || {};
  const leftText = items.slice(0, 3).join('<br/>');
  const rightItems = items.slice(3);
  const note = f['备注'] || f['图示'] || '';
  const source = sourceLine(slide);
  return `<section class="slide split" data-layout="S03" data-animate="statement">
  <div class="canvas-card">
    <div class="split-half">
      <div class="half b-accent" style="padding:5.6vh 3.6vw 4.4vh;justify-content:space-between;position:relative;overflow:hidden">
        <canvas class="ascii-bg" aria-hidden="true"></canvas>
        <div class="chrome-min" style="margin-bottom:0;position:relative;z-index:1"><div class="l">${esc(slide.act || 'STATEMENT')}</div><div class="r">${pad(num)} / ${pad(total)}</div></div>
        <div data-anim="left" style="display:flex;flex-direction:column;gap:2.4vh;position:relative;z-index:1">
          <div class="t-meta" style="color:rgba(255,255,255,.78);letter-spacing:.22em">CORE STATEMENT</div>
          <h2 style="font-family:var(--sans),var(--sans-zh);font-weight:700;font-size:min(4.6vw,8vh);line-height:1.12;letter-spacing:0;color:#fff">${esc(leftText)}</h2>
        </div>
        <div data-anim="left" class="t-meta" style="color:rgba(255,255,255,.62);position:relative;z-index:1">${esc(f['公式'] ? '公式：' + f['公式'] : (note || '全文主张均附证伪条件'))}</div>
      </div>
      <div class="half b-grey" style="padding:5.6vh 3.6vw 4.4vh;justify-content:space-between">
        <div class="chrome-min"><div class="l">${esc(slide.title)}</div><div class="r">${pad(num)} / ${pad(total)}</div></div>
        <div data-anim="right" style="display:flex;flex-direction:column;gap:2.2vh;max-width:36ch">
          <h3 class="t-h-prod" style="font-size:max(20px,1.8vw);color:var(--accent)">${esc(slide.title)}</h3>
          ${rightItems.map((it) => `<p class="t-body" style="font-size:max(20px,1.15vw)">${esc(it)}</p>`).join('') || `<p class="t-body" style="font-size:max(20px,1.15vw)">${esc(bodyText(slide))}</p>`}
          ${note ? `<p class="t-body-sm" style="font-size:max(17px,1vw);color:var(--text-secondary)">${esc(note)}</p>` : ''}
        </div>
        <div data-anim="right" class="t-meta" style="color:var(--text-helper);text-align:right">${esc(source.replace(/<[^>]+>/g, '') || '源：提纲 P' + slide.num)}</div>
      </div>
    </div>
  </div>
</section>`;
}

function layoutS09(slide, part, num, total, items) {
  const f = slide.fields || {};
  const text = items.join('<br/>') || f['body'] || f['备注'] || slide.title;
  const note = f['备注'] || sourceLine(slide);
  return `<section class="slide dark" data-layout="S09" data-animate="statement">
  <div class="canvas-card">
    <span class="dot-mat" style="position:absolute;right:0;top:0;width:34vw;height:34vw;color:var(--accent-bright)"></span>
    <span class="ring-mat" style="position:absolute;left:4vw;bottom:4vh;width:16vw;height:16vw;color:rgba(255,255,255,.18)"></span>
    <div class="chrome-min"><div class="l">${esc(slide.act || 'DECLARATION')}</div><div class="r">${pad(num)} / ${pad(total)}</div></div>
    <h1 data-anim="line" style="align-self:center;font-family:var(--sans),var(--sans-zh);font-weight:700;font-size:min(5vw,8.8vh);line-height:1.2;letter-spacing:0;color:var(--paper);max-width:30ch">${esc(text)}</h1>
    <div class="t-meta" style="color:rgba(255,255,255,.62);text-align:right">${esc(String(note).replace(/<[^>]+>/g, ''))}</div>
  </div>
</section>`;
}

function layoutS04(slide, part, num, total, items) {
  const f = slide.fields || {};
  const blocks = items.length >= 6 ? items.slice(0, 6) : items;
  while (blocks.length < 6) blocks.push('');
  const cells = blocks.map((item, i) => {
    const accent = i === 5;
    const cls = accent ? 'sub-card accent' : 'sub-card';
    return `<div class="${cls}"><i data-lucide="${['layers', 'network', 'cog', 'activity', 'gauge', 'sparkles'][i]}" class="lucide"></i><span class="nb-corner">${pad(i + 1)}</span><div class="ttl">${esc(cardTitle(item) || '维度 ' + (i + 1))}</div><div class="desc">${esc(item || (i === 5 ? '综合收束' : '见提纲 P' + slide.num))}</div></div>`;
  }).join('');
  return `<section class="slide" data-layout="S04" data-animate="grid-reveal">
  <div class="canvas-card">
    ${chrome(part, num, total, slide.act)}
    ${titleBlock(slide.title, { kicker: slide.act || 'SIX DIMENSIONS' })}
    <div class="sub-grid-3-2">${cells}</div>
    ${footnoteBlock('[引用] 提纲 P' + slide.num + (f['备注'] ? ' · ' + f['备注'] : ''))}
  </div>
</section>`;
}

function layoutS19(slide, part, num, total, items) {
  const f = slide.fields || {};
  const blocks = items.slice(0, 4);
  while (blocks.length < 4) blocks.push('见提纲 P' + slide.num);
  const cols = blocks.map((item, i) => `<div style="padding-top:1.6vh;border-top:1px solid var(--border-subtle)">
    <div class="t-meta">— ${pad(i + 1)} / ${['KEY', 'DIMENSION', 'PILLAR', 'TAKEAWAY'][i]}</div>
    <h3 class="t-h-prod" style="font-size:max(20px,1.5vw);margin:1.4vh 0">${esc(cardTitle(item))}</h3>
    <p class="body-sm" style="font-size:max(18px,1.04vw)">${esc(item)}</p>
  </div>`).join('');
  return `<section class="slide" data-layout="S19" data-animate="four-cards">
  <div class="canvas-card">
    ${chrome(part, num, total, slide.act)}
    <div data-anim="line" style="display:flex;flex-direction:column;gap:2vh">
      <div style="height:3px;background:var(--accent);width:80px"></div>
      ${titleBlock(slide.title, { kicker: slide.act || 'FOUR PILLARS' })}
    </div>
    <div data-anim="up" style="display:grid;grid-template-columns:repeat(4,1fr);gap:1.6vw;margin-top:6vh;align-items:start">${cols}</div>
    ${footnoteBlock('[引用] 提纲 P' + slide.num + (f['备注'] ? ' · ' + f['备注'] : ''))}
  </div>
</section>`;
}

function layoutS16(slide, part, num, total, items) {
  const f = slide.fields || {};
  const blocks = items.slice(0, 6);
  while (blocks.length < 6) blocks.push('见提纲 P' + slide.num);
  const cards = blocks.map((item, i) => {
    const accent = i === 5;
    const cls = accent ? 'card-accent' : 'card-fill';
    return `<div class="${cls}" style="padding:2.4vh 1.6vw;display:flex;flex-direction:column;justify-content:space-between;min-height:23vh">
      <div class="t-h-prod" style="font-size:max(20px,1.3vw);color:${accent ? 'var(--accent-on)' : 'var(--text-primary)'}">${esc(cardTitle(item))}</div>
      <p class="t-body-sm" style="font-size:max(18px,1.04vw);color:${accent ? 'rgba(255,255,255,.9)' : 'var(--text-secondary)'}">${esc(item)}</p>
      <div class="t-meta" style="color:${accent ? 'rgba(255,255,255,.72)' : 'var(--text-helper)'}">BRIEF ${pad(i + 1)}</div>
    </div>`;
  }).join('');
  return `<section class="slide grey" data-layout="S16" data-animate="field-notes">
  <div class="canvas-card">
    ${chrome(part, num, total, slide.act)}
    ${titleBlock(slide.title, { kicker: slide.act || 'FIELD NOTES' })}
    <div data-anim="up" style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.6vh 1.4vw;margin-top:6vh;flex:1">${cards}</div>
    ${footnoteBlock('[引用] 提纲 P' + slide.num + (f['备注'] ? ' · ' + f['备注'] : ''))}
  </div>
</section>`;
}

function layoutS05(slide, part, num, total, items) {
  const f = slide.fields || {};
  const blocks = items.slice(0, 3);
  while (blocks.length < 3) blocks.push('见提纲 P' + slide.num);
  const stack = blocks.map((item, i) => {
    const cls = i === 1 ? 'stack-block b-accent' : i === 2 ? 'stack-block b-ink' : 'stack-block b-grey';
    return `<div class="${cls}"><span class="layer-nb">STAGE ${pad(i + 1)}</span><div class="layer-ttl">${esc(cardTitle(item))}</div><p class="layer-desc">${esc(item)}</p><div class="layer-tag">提纲 P${slide.num} · ${pad(i + 1)} / ${pad(3)}</div></div>`;
  }).join('');
  return `<section class="slide" data-layout="S05" data-animate="stack-build">
  <div class="canvas-card">
    ${chrome(part, num, total, slide.act)}
    ${titleBlock(slide.title, { kicker: slide.act || 'THREE STAGES' })}
    <div class="stack-row">${stack}</div>
    ${footnoteBlock('[引用] 提纲 P' + slide.num + (f['备注'] ? ' · ' + f['备注'] : ''))}
  </div>
</section>`;
}

function layoutS02(slide, part, num, total, items) {
  const f = slide.fields || {};
  const nodes = items.slice(0, 5).map((item, i) => {
    const yr = (item.match(/\b(19|20)\d{2}\b/) || [])[0] || String(1956 + i * 14);
    return `<div class="tl-node${i === 1 ? ' accent' : ''}"><div class="tl-axis"><span class="dot"></span></div><span class="yr">${yr}</span><span class="multi">${pad(i + 1)}<small class="unit">步</small></span><p class="desc">${esc(item)}</p></div>`;
  }).join('');
  const kpis = items.slice(0, 4).map((item, i) => {
    const num = (item.match(/\d+(?:\.\d+)?/) || [])[0] || pad(i + 1);
    return `<div class="kpi-cell"><div class="lbl">STEP ${pad(i + 1)}</div><div class="nb">${esc(num)}</div><div class="note">${esc(item.slice(0, 24))}</div></div>`;
  }).join('');
  return `<section class="slide dark" data-layout="S02" data-animate="progression">
  <div class="canvas-card">
    ${chrome(part, num, total, slide.act)}
    ${titleBlock(slide.title, { kicker: slide.act || 'EVIDENCE CHAIN', color: 'var(--paper)' })}
    <div class="timeline-v">${nodes}</div>
    <div class="kpi-row-4">${kpis}</div>
    ${footnoteBlock('[引用] 提纲 P' + slide.num + (f['依据'] ? ' · ' + f['依据'] : ''), true)}
  </div>
</section>`;
}

function layoutS07(slide, part, num, total, items) {
  const f = slide.fields || {};
  const bars = items.slice(0, 6).map((item, i) => {
    const pct = (item.match(/(\d+(?:\.\d+)?)\s*%/) || [])[1] || (i === 0 ? 100 : 60 - i * 8);
    return `<div class="row-lbl">${esc(cardTitle(item))}</div><div class="row-track"><div class="row-fill${i === 1 ? ' accent' : ''}" style="width:${Math.min(100, Math.max(10, +pct))}%"></div></div><div class="row-val">${esc(pct)}<span class="unit">%</span></div>`;
  }).join('');
  return `<section class="slide dark" data-layout="S07" data-animate="bar-grow">
  <div class="canvas-card">
    ${chrome(part, num, total, slide.act)}
    ${titleBlock(slide.title, { kicker: slide.act || 'QUANTITATIVE VIEW', color: 'var(--paper)' })}
    <div class="h-bar-chart" style="margin-top:5vh">${bars}</div>
    ${footnoteBlock('[引用] 提纲 P' + slide.num + (f['依据'] ? ' · ' + f['依据'] : ''), true)}
  </div>
</section>`;
}

function layoutS20(slide, part, num, total, items) {
  const f = slide.fields || {};
  const rows = items.slice(0, 6).map((item, i) => {
    const val = (item.match(/\d+(?:\.\d+)?(?:\s*[万亿兆])?/) || [])[0] || pad(i + 1);
    return `<div class="ledger-row"><div class="ledger-num">${esc(val)}</div><div class="ledger-label">${esc(item)}</div><i data-lucide="file-text" class="ledger-icon" style="width:2vw;height:2vw;stroke-width:1.4"></i></div>`;
  }).join('');
  return `<section class="slide dark" data-layout="S20" data-animate="stacked-ledger">
  <div class="canvas-card">
    ${chrome(part, num, total, slide.act)}
    ${titleBlock(slide.title, { kicker: slide.act || 'LEDGER', color: 'var(--paper)' })}
    <div data-anim="ledger" style="display:flex;flex-direction:column;margin-top:4vh">${rows}</div>
    ${footnoteBlock('[引用] 提纲 P' + slide.num + (f['备注'] ? ' · ' + f['备注'] : ''), true)}
  </div>
</section>`;
}

function layoutS13(slide, part, num, total, items) {
  const f = slide.fields || {};
  const left = items[0] || f['body'] || slide.title;
  const cards = items.slice(1, 4).map((item, i) => `<article class="card-fill" style="padding:2.6vh 1.8vw;display:grid;grid-template-columns:auto 1fr;gap:1.6vw;align-items:start">
    <div style="font-family:var(--sans);font-weight:700;font-size:min(4vw,7vh);color:var(--accent);line-height:.9">${pad(i + 1)}</div>
    <div><h3 class="t-h-prod" style="font-size:max(20px,1.35vw)">${esc(cardTitle(item))}</h3><p class="t-body-sm" style="font-size:max(18px,1.05vw)">${esc(item)}</p></div>
  </article>`).join('');
  return `<section class="slide" data-layout="S13" data-animate="three-forces">
  <div class="canvas-card">
    ${chrome(part, num, total, slide.act)}
    ${titleBlock(slide.title, { kicker: slide.act || 'THREE FORCES' })}
    <div data-anim="up" style="display:grid;grid-template-columns:5fr 7fr;gap:2vw;margin-top:5vh;align-items:stretch;flex:1">
      <div class="card-ink" style="padding:3.2vh 2.2vw;display:flex;flex-direction:column;justify-content:space-between">
        <div class="t-meta" style="color:rgba(255,255,255,.6)">CORE CLAIM</div>
        <div style="font-family:var(--sans),var(--sans-zh);font-weight:700;font-size:min(2.6vw,4.8vh);line-height:1.24;color:var(--paper)">${esc(left)}</div>
      </div>
      <div style="display:flex;flex-direction:column;gap:1.6vh">${cards}</div>
    </div>
    ${footnoteBlock('[引用] 提纲 P' + slide.num + (f['依据'] ? ' · ' + f['依据'] : ''))}
  </div>
</section>`;
}

function layoutS08(slide, part, num, total, items) {
  const f = slide.fields || {};
  const left = items[0] || '传统路径';
  const right = items[1] || items[2] || '新路径';
  return `<section class="slide" data-layout="S08" data-animate="duo-mirror">
  <div class="canvas-card">
    ${chrome(part, num, total, slide.act)}
    ${titleBlock(slide.title, { kicker: slide.act || 'DUO COMPARE' })}
    <div class="duo-compare">
      <div class="col">
        <div class="col-tag"><span class="num">A</span>${esc(f['依据'] ? 'EVIDENCE A' : 'PATH A')}</div>
        <div class="col-ttl" style="font-size:min(3.4vw,6vh)">${esc(cardTitle(left))}</div>
        <div class="col-desc">${esc(left)}</div>
      </div>
      <span class="vrule"></span>
      <div class="col accent">
        <div class="col-tag"><span class="num">B</span>${esc(f['图示'] ? 'EVIDENCE B' : 'PATH B')}</div>
        <div class="col-ttl" style="font-size:min(3.4vw,6vh)">${esc(cardTitle(right))}</div>
        <div class="col-desc">${esc(right)}</div>
      </div>
    </div>
    ${footnoteBlock('[引用] 提纲 P' + slide.num + (f['备注'] ? ' · ' + f['备注'] : ''))}
  </div>
</section>`;
}

function layoutS12(slide, part, num, total, items) {
  const f = slide.fields || {};
  const main = items[0] || f['body'] || slide.title;
  const note = f['备注'] || f['图示'] || '';
  return `<section class="slide" data-layout="S12" data-animate="manifesto">
  <div class="canvas-card">
    ${chrome(part, num, total, slide.act)}
    <div data-anim="line" style="display:grid;grid-template-columns:7fr 5fr;gap:4vw;align-items:start;padding-top:2vh">
      <div style="display:flex;flex-direction:column;gap:1.6vh">
        <div class="t-cat accent">${esc(slide.act || 'MANIFESTO')}</div>
        <div style="font-family:var(--sans),var(--sans-zh);font-weight:700;font-size:min(4.6vw,8.2vh);line-height:1.12;letter-spacing:0">${esc(main)}</div>
      </div>
      <div style="display:flex;flex-direction:column;gap:1.2vh;padding-top:1vw">
        <p class="t-body" style="font-size:max(20px,1.2vw)">${esc(slide.title)}</p>
        ${note ? `<p class="t-body-sm" style="font-size:max(17px,1vw)">${esc(note)}</p>` : ''}
      </div>
    </div>
    <div data-anim="hero" style="margin-top:auto;background:var(--ink);color:var(--paper);padding:4vh 3.4vw;display:grid;grid-template-columns:auto 1fr;gap:3vw;align-items:center">
      <div class="bottom-hero" style="font-family:var(--sans),var(--sans-zh);font-weight:700;font-size:min(3.6vw,6.4vh);line-height:1.1;letter-spacing:0;white-space:normal">${esc(main)}</div>
      <div style="display:flex;flex-direction:column;gap:1vh">
        <div class="t-meta" style="color:rgba(255,255,255,.62)">TAKEAWAY · P${slide.num}</div>
        <div class="t-body-sm" style="color:rgba(255,255,255,.86);font-size:max(17px,1vw)">[引用] 提纲 P${slide.num}${f['依据'] ? ' · ' + f['依据'] : ''}</div>
      </div>
    </div>
  </div>
</section>`;
}

function layoutS11(slide, part, num, total, items) {
  const f = slide.fields || {};
  const blocks = items.slice(0, 5);
  while (blocks.length < 5) blocks.push('见提纲 P' + slide.num);
  const nodes = blocks.map((item, i) => {
    const yr = (item.match(/\b(19|20)\d{2}\b/) || [])[0] || pad(i + 1);
    return `<div class="th-node ${i % 2 === 0 ? 'up' : 'down'}${i === blocks.length - 1 ? ' accent' : ''}"><span class="dot"></span><span class="label"><span class="yr">${esc(yr)}</span><span class="name">${esc(cardTitle(item))}</span><span class="desc">${esc(item.slice(0, 40))}</span></span></div>`;
  }).join('');
  return `<section class="slide grey" data-layout="S11" data-animate="timeline-walk">
  <div class="canvas-card">
    ${chrome(part, num, total, slide.act)}
    ${titleBlock(slide.title, { kicker: slide.act || 'TIMELINE' })}
    <div class="timeline-h"><div class="tl-row">${nodes}</div></div>
    ${footnoteBlock('[引用] 提纲 P' + slide.num + (f['备注'] ? ' · ' + f['备注'] : ''))}
  </div>
</section>`;
}

function layoutS14(slide, part, num, total, items) {
  const f = slide.fields || {};
  const steps = items.slice(0, 4);
  while (steps.length < 4) steps.push('见提纲 P' + slide.num);
  const stepHtml = steps.map((item, i) => `<div><div class="t-meta">${pad(i + 1)}</div><div class="t-body" style="font-size:max(20px,1.2vw)">${esc(item)}</div></div>`).join('');
  return `<section class="slide dark" data-layout="S14" data-animate="loop-form">
  <div class="canvas-card">
    ${chrome(part, num, total, slide.act)}
    ${titleBlock(slide.title, { kicker: slide.act || 'CO-EVOLUTION LOOP', color: 'var(--paper)' })}
    <div data-anim="up" style="display:grid;grid-template-columns:1fr 1fr;gap:4vw;align-items:center;margin-top:5vh;flex:1">
      <div style="display:flex;flex-direction:column;gap:2.4vh">${stepHtml}</div>
      <div style="display:flex;justify-content:center">
        <svg viewBox="0 0 320 320" width="min(30vw,50vh)" height="min(30vw,50vh)" aria-hidden="true" style="color:var(--paper)">
          <defs>
            <marker id="arr${num}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="var(--accent-bright)"></path></marker>
          </defs>
          <circle cx="160" cy="160" r="128" fill="none" stroke="currentColor" stroke-width="1" opacity=".35"></circle>
          <circle cx="160" cy="160" r="96" fill="none" stroke="var(--accent-bright)" stroke-width="1" opacity=".55"></circle>
          <circle cx="160" cy="52" r="8" fill="var(--accent-bright)"></circle>
          <circle cx="268" cy="160" r="8" fill="var(--accent-bright)"></circle>
          <circle cx="160" cy="268" r="8" fill="var(--accent-bright)"></circle>
          <circle cx="52" cy="160" r="8" fill="var(--accent-bright)"></circle>
          <path d="M 160 44 A 148 148 0 0 1 274 160" fill="none" stroke="var(--accent-bright)" stroke-width="1.4" marker-end="url(#arr${num})"></path>
          <path d="M 274 160 A 148 148 0 0 1 160 276" fill="none" stroke="var(--accent-bright)" stroke-width="1.4" marker-end="url(#arr${num})"></path>
          <path d="M 160 276 A 148 148 0 0 1 46 160" fill="none" stroke="var(--accent-bright)" stroke-width="1.4" marker-end="url(#arr${num})"></path>
          <path d="M 46 160 A 148 148 0 0 1 160 44" fill="none" stroke="var(--accent-bright)" stroke-width="1.4" marker-end="url(#arr${num})"></path>
        </svg>
      </div>
    </div>
    ${footnoteBlock('[引用] 提纲 P' + slide.num + (f['依据'] ? ' · ' + f['依据'] : ''), true)}
  </div>
</section>`;
}

function layoutS21(slide, part, num, total, items) {
  const f = slide.fields || {};
  const kpis = items.slice(0, 3).map((item, i) => {
    const val = (item.match(/\d+(?:\.\d+)?(?:\s*[万亿兆])?(?:\s*[⁰¹²³⁴⁵⁶⁷⁸⁹]+)?/) || [])[0] || pad(i + 1);
    return `<div style="display:flex;flex-direction:column;gap:1vh"><div style="height:3px;background:var(--accent)"></div><div class="kpi-num" style="font-size:min(3.4vw,6vh)">${esc(val)}</div><div class="t-meta">KPI ${pad(i + 1)}</div><div class="t-body-sm" style="font-size:max(16px,1vw)">${esc(item)}</div></div>`;
  }).join('');
  const formula = f['公式'];
  return `<section class="slide" data-layout="S21" data-animate="tech-spec">
  <div class="canvas-card">
    ${chrome(part, num, total, slide.act)}
    <div data-anim="line" style="display:flex;flex-direction:column;gap:1.4vh">
      <div class="t-cat accent">${esc(slide.act || 'TECH SPEC')}</div>
      <h2 class="h-xl-zh" style="font-size:min(5vw,8.8vh)">${esc(slide.title)}</h2>
    </div>
    <div data-anim="up" style="display:grid;grid-template-columns:repeat(3,1fr);gap:2vw;margin-top:6vh;align-items:start">${kpis}</div>
    ${formula ? `<div data-anim="hero" style="margin-top:auto;background:var(--ink);color:var(--paper);padding:3.4vh 3vw;display:grid;grid-template-columns:auto 1fr;gap:2.4vw;align-items:center">
      <div class="bottom-hero" style="font-family:var(--mono),var(--sans);font-weight:700;font-size:min(2.2vw,4vh);line-height:1.2;letter-spacing:0">${esc(formula)}</div>
      <div class="t-body-sm" style="color:rgba(255,255,255,.85);font-size:max(17px,1vw)">[推导] 提纲 P${slide.num} · ${esc(f['备注'] || '公式为理论表达，数值待实验标定')}</div>
    </div>` : ''}
    ${footnoteBlock('[引用] 提纲 P' + slide.num + (f['依据'] ? ' · ' + f['依据'] : ''))}
  </div>
</section>`;
}

function coverSlide(part, num, total, subtitle) {
  return `<section class="slide accent" data-layout="SWISS-COVER-ASCII" data-animate="hero">
  <div class="canvas-card">
    <canvas class="ascii-bg" aria-hidden="true"></canvas>
    <div class="chrome-min">
      <div class="l">智涌脑 · iNEST — 脑科学智能涌现分享</div>
      <div class="r">PART ${part} · ${pad(num)} / ${pad(total)}</div>
    </div>
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr auto;gap:2.6vh">
      <div data-anim="kicker" class="t-meta" style="color:rgba(255,255,255,.78);letter-spacing:.22em">BRAIN SCIENCE · EMERGENT INTELLIGENCE · PART ${part}</div>
      <h1 data-anim="title" style="align-self:center;font-family:var(--sans),var(--sans-zh);font-weight:700;font-size:min(6.4vw,11.2vh);line-height:1.05;letter-spacing:0;color:#fff">网络时空协同复杂度<br/>与<span style="font-style:italic;font-weight:300">智能涌现</span> · ${part}</h1>
      <div data-anim="bottom" style="display:grid;grid-template-rows:auto auto;gap:1.6vh;border-top:1px solid rgba(255,255,255,.22);padding-top:2vh">
        <div data-anim="lead" class="lead" style="max-width:56ch;color:rgba(255,255,255,.86);font-weight:700">${esc(subtitle)}</div>
        <div style="display:flex;justify-content:space-between;align-items:end">
          <div class="t-meta" style="color:rgba(255,255,255,.6)">iNEST · 智涌脑 Z-Brain Ⅰ / Ⅱ / Ⅲ</div>
          <div class="t-meta" style="color:rgba(255,255,255,.6)">→ swipe / arrow keys</div>
        </div>
      </div>
    </div>
  </div>
</section>`;
}

function closingSlide(part, num, total, lines) {
  return `<section class="slide split" data-layout="SWISS-CLOSING-ASCII" data-animate="split-statement">
  <div class="canvas-card">
    <div class="split-half">
      <div class="half b-accent" style="padding:5.6vh 3.6vw 4.4vh;justify-content:space-between;position:relative;overflow:hidden">
        <canvas class="ascii-bg" aria-hidden="true"></canvas>
        <div class="chrome-min" style="margin-bottom:0;position:relative;z-index:1"><div class="l">${pad(num)} / ${pad(total)}</div><div class="r">PART ${part} · CLOSING</div></div>
        <div data-anim="manifesto" style="display:flex;flex-direction:column;gap:2vh;position:relative;z-index:1">
          <div class="t-meta" style="color:rgba(255,255,255,.78);letter-spacing:.22em;margin-bottom:1.6vh">PART ${part} · MANIFESTO</div>
          <h2 style="font-family:var(--sans),var(--sans-zh);font-size:min(5.6vw,10vh);line-height:1.08;letter-spacing:0;font-weight:700;color:#fff">${esc(lines[0])}</h2>
          <div style="font-family:var(--sans),var(--sans-zh);font-size:max(16px,1.05vw);line-height:1.6;color:rgba(255,255,255,.82);font-weight:700;max-width:38ch;margin-top:1.4vh">${esc(lines[1] || '')}</div>
        </div>
        <div data-anim="signature" style="display:flex;justify-content:space-between;align-items:end;border-top:1px solid rgba(255,255,255,.22);padding-top:2vh;position:relative;z-index:1">
          <div class="t-meta" style="color:rgba(255,255,255,.62)">智涌脑 · iNEST</div>
          <div class="t-meta" style="color:rgba(255,255,255,.62)">2026.08</div>
        </div>
      </div>
      <div class="half" style="padding:5.6vh 3.6vw 4.4vh;justify-content:space-between">
        <div class="chrome-min"><div class="l">TAKEAWAYS · PART ${part}</div><div class="r">03 RULES</div></div>
        <div data-anim="rules" style="display:flex;flex-direction:column;gap:0">
          ${lines.slice(2).map((item, i) => `<div style="display:grid;grid-template-columns:auto 1fr;gap:2vw;align-items:start;padding:2.6vh 0;border-top:1px solid var(--border-subtle);${i === 2 ? 'border-bottom:2px solid var(--accent)' : ''}">
            <div style="font-family:var(--sans);font-weight:700;font-size:min(4vw,7vh);line-height:.9;color:${i === 2 ? 'var(--accent)' : 'var(--text-primary)'}">${pad(i + 1)}</div>
            <div><h3 style="font-family:var(--sans),var(--sans-zh);font-weight:700;font-size:max(20px,1.8vw);line-height:1.2;color:${i === 2 ? 'var(--accent)' : 'var(--text-primary)'};margin-bottom:1vh">${esc(item.split('：')[0])}</h3><p class="t-body-sm" style="font-size:max(18px,1.05vw)">${esc(item.split('：')[1] || item)}</p></div>
          </div>`).join('')}
        </div>
        <div data-anim="foot" class="t-meta" style="color:var(--text-helper);text-align:right">→ 本部分完 · CONTINUE TO PART ${part + 1}</div>
      </div>
    </div>
  </div>
</section>`;
}

function bodyText(slide) {
  return (slide.fields && slide.fields['body']) || slide.raw || '';
}

function renderSlide(slide, part, num, total) {
  const f = slide.fields || {};
  const items = splitItems(f['body']);
  const img = IMAGES.get(slide.num);
  const layout = img ? 'S22' : (FALLBACK_LAYOUT[slide.num] || (items.length === 1 ? 'S03' : items.length === 3 ? 'S05' : items.length === 4 ? 'S19' : items.length === 6 ? 'S04' : 'S16'));
  if (img) return layoutS22(slide, part, num, total, img, items.length ? items : [f['body'] || slide.title]);
  switch (layout) {
    case 'S03': return layoutS03(slide, part, num, total, items);
    case 'S09': return layoutS09(slide, part, num, total, items);
    case 'S04': return layoutS04(slide, part, num, total, items);
    case 'S19': return layoutS19(slide, part, num, total, items);
    case 'S16': return layoutS16(slide, part, num, total, items);
    case 'S05': return layoutS05(slide, part, num, total, items);
    case 'S02': return layoutS02(slide, part, num, total, items);
    case 'S07': return layoutS07(slide, part, num, total, items);
    case 'S20': return layoutS20(slide, part, num, total, items);
    case 'S13': return layoutS13(slide, part, num, total, items);
    case 'S08': return layoutS08(slide, part, num, total, items);
    case 'S12': return layoutS12(slide, part, num, total, items);
    case 'S11': return layoutS11(slide, part, num, total, items);
    case 'S14': return layoutS14(slide, part, num, total, items);
    case 'S21': return layoutS21(slide, part, num, total, items);
    default: return layoutS19(slide, part, num, total, items);
  }
}

const STYLE_OVERRIDE = `
  :root{--sans-zh:"Microsoft YaHei UI","Microsoft YaHei","微软雅黑","PingFang SC","Noto Sans SC",var(--sans-zh)}
  .slide h1,.slide h2,.slide h3,.slide h4,.slide h5,.lead,.t-body,.t-body-sm,.body-sm,.h-xl-zh,.h-hero-zh,.t-h-prod,.ttl,.col-desc,.col-list li,.layer-desc,.tl-node .desc,.row-lbl{font-family:"Microsoft YaHei UI","Microsoft YaHei","微软雅黑",var(--sans-zh),sans-serif !important;font-weight:700 !important;letter-spacing:0 !important}
  .t-body,.body-sm,.lead{font-size:max(20px,1.55vw)}
  .t-body-sm{font-size:max(18px,1.12vw)}
  .t-meta,.t-cat{font-size:max(15px,1.05vw);font-weight:600 !important}
  .h-xl-zh{font-size:min(5.4vw,9.6vh)}
  .chrome-min,.chrome-min .l,.chrome-min .r{font-family:"Microsoft YaHei UI","Microsoft YaHei","微软雅黑",var(--mono),sans-serif !important;font-weight:600 !important;font-size:max(15px,1vw) !important;letter-spacing:.06em !important}
  .h-bar-chart .row-lbl,.h-bar-chart .row-val{font-size:max(19px,1.3vw)}
  .kpi-cell .nb{font-size:min(3.6vw,6.4vh)}
  .tl-node .multi{font-size:min(3.4vw,6vh)}
`;

function injectOverride(html) {
  const idx = html.lastIndexOf('</style>');
  if (idx === -1) throw new Error('template has no </style>');
  return html.slice(0, idx) + STYLE_OVERRIDE + '\n</style>' + html.slice(idx + '</style>'.length);
}

function buildPart(part, slideRange, subtitle, closingLines, titleSuffix, extraSlides = []) {
  const slidesHtml = [];
  const total = slideRange.length + 2; // cover + closing
  slidesHtml.push(coverSlide(part, 1, total, subtitle));
  slideRange.forEach((s, i) => {
    slidesHtml.push(renderSlide(s, part, i + 2, total));
  });
  slidesHtml.push(closingSlide(part, total, total, closingLines));
  slidesHtml.push(...extraSlides);

  let html = template;
  html = html.replace(/<title>[^<]*<\/title>/, `<title>${DECK_TITLE} · 第${part}部分 ${titleSuffix} · 脑科学智能涌现分享</title>`);

  // Insert generated sections between the template's SLIDES comment and the
  // deck closing div, using ASCII-only anchors (the Chinese comment text is
  // not used as a match anchor to avoid encoding surprises).
  const deckStart = html.indexOf('<div id="deck">');
  if (deckStart === -1) throw new Error('template has no deck div');
  const deckEnd = html.indexOf('</div>\n\n<div id="nav">');
  if (deckEnd === -1) throw new Error('template has no deck closing div');

  // Strip the template's instruction comment block (everything between the
  // deck opening div and the first generated section), then insert slides.
  const insertAt = html.indexOf('<!--', deckStart);
  const blockEnd = html.indexOf('-->', insertAt) + 3;
  const head = html.slice(0, insertAt);
  const tail = html.slice(deckEnd);
  html = head + '<!-- SLIDES GENERATED FROM outline.json · ' + new Date().toISOString() + ' -->\n\n' + slidesHtml.join('\n\n') + '\n' + tail;
  html = injectOverride(html);
  return html;
}

const part1 = slides.filter((s) => s.num >= 1 && s.num <= 49);
const part2 = slides.filter((s) => s.num >= 50 && s.num <= 98);
const part3 = slides.filter((s) => s.num >= 99 && s.num <= 146);

const builds = [
  {
    part: 1,
    range: part1,
    subtitle: '从第一性原理到度量体系：问题、四墙、Scaling 坍塌、结构立论、连接证据、非线性入场，以及 CST 的完整定义。',
    closingLines: ['先造尺子，再造系统。', '本部分完成：问题、立论、连接证据、非线性与 CST 度量。', '范式差距：可测量性', '结构优先：拓扑即功能', '乘性放大：非线性即入场券'],
    titleSuffix: 'P1–P49 立论与度量',
  },
  {
    part: 2,
    range: part2,
    subtitle: '从 CST 到工程控制：智能定义与六级量表、SDDE 动力学、四条局部规则、临界态与 SDI 控制律。',
    closingLines: ['不设计结果，只设计势能面。', '本部分完成：智能度量、动力学、自组织临界与 SDI 控制。', '智能相对化：RI 比值', '动力学：时滞即维度', '控制：可控涌现'],
    titleSuffix: 'P50–P98 动力学与控制',
  },
  {
    part: 3,
    range: part3,
    subtitle: '从范式到产业：TCC 与介观尺度、SDSoW、三代智涌脑、五方联合体、资金通道、成果与生态路线。',
    closingLines: ['智能不是算出来的，是长出来的。', '本部分完成：范式、三代工程、协同组织与产业生态。', '范式：拓扑中心计算', '工程：三代样机路线', '生态：定义度量者定义赛道'],
    titleSuffix: 'P99–P146 范式与产业',
  },
];

const appendixHtml = `\n<section class="slide grey" data-layout="S04" data-animate="grid-reveal">
  <div class="canvas-card">
    <div class="chrome-min"><div class="l">智涌脑 · iNEST · PART 3</div><div class="r">附录 / APPENDIX</div></div>
    <div data-anim="line" style="display:flex;flex-direction:column;gap:1.4vh">
      <div class="t-cat accent">APPENDIX · A1–A10</div>
      <h2 class="h-xl-zh" style="font-size:min(5vw,8.8vh)">附录：术语与材料</h2>
    </div>
    <div class="sub-grid-3-2">
      ${['A1 术语表', 'A2 符号说明', 'A3 公式清单', 'A4 参考文献', 'A5 判决性实验协议', 'A6 门径评审细则', 'A7 预算与里程碑', 'A8 组织与分工', 'A9 产业地图细表', 'A10 风险与备份'].map((t, i) => `<div class="sub-card${i === 9 ? ' accent' : ''}"><i data-lucide="book-open" class="lucide"></i><span class="nb-corner">${pad(i + 1)}</span><div class="ttl">${t}</div><div class="desc">${i === 9 ? '风险总台账与触发信号。' : '对应正文第 ' + ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11'][i] + ' 幕内容。'}</div></div>`).join('')}
    </div>
    <div class="t-meta" style="color:var(--text-helper);margin-top:2.4vh">[引用] 原始笔记附录 A1–A10 · 本页为附录目录</div>
  </div>
</section>`;

for (const b of builds) {
  const outDir = join(ROOT, 'part' + b.part);
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, 'index.html'), buildPart(b.part, b.range, b.subtitle, b.closingLines, b.titleSuffix, b.part === 3 ? [appendixHtml] : []), 'utf8');
  console.log(`part${b.part}: ${b.range.length + 2} slides written -> ${outDir}/index.html`);
}
