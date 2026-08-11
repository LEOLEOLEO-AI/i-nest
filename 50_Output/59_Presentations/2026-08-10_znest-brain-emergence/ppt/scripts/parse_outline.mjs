import { readFileSync, writeFileSync } from 'node:fs';

const src = process.argv[2] ?? 'outline_108.md';
const dst = process.argv[3] ?? 'outline.json';
const text = readFileSync(src, 'utf8').replace(/\uFEFF/g, '');
const lines = text.split(/\r?\n/);

const slides = [];
let current = null;
let act = '';

const pushCurrent = () => {
  if (!current) return;
  current.act = act;
  current.raw = current.raw.join('\n').trim();
  current.lines = current.lines.filter((l) => l.trim().length > 0);
  slides.push(current);
  current = null;
};

for (const line of lines) {
  const trimmed = line.trim();
  if (!trimmed) continue;

  const pageMatch = trimmed.match(/^P(\d+)\s*[｜|]\s*(.*)$/);
  if (pageMatch) {
    pushCurrent();
    current = {
      num: Number(pageMatch[1]),
      title: pageMatch[2].trim(),
      raw: [],
      lines: [],
      fields: {},
    };
    current.raw.push(trimmed);
    current.lines.push(trimmed);
    continue;
  }

  const actMatch = trimmed.match(/^(序幕|第[一二三四五六七八九十]+幕).*$/);
  if (actMatch && !pageMatch) {
    act = trimmed;
  }

  if (current) {
    current.raw.push(trimmed);
    current.lines.push(trimmed);
  }
}
pushCurrent();

const clean = (s) =>
  s
    .replace(/^[：:\s]+/, '')
    .replace(/\s+/g, ' ')
    .replace(/[ \t]+/g, ' ')
    .trim();

for (const s of slides) {
  for (const line of s.lines) {
    const m = line.match(/^(主体|备注|依据|公式|图示|关键任务|符号说明|层次结构声明|主体（要点式|主体（表格|主体（表格式)(.*)$/);
    if (m) {
      const label = m[1];
      const rest = m[2] ?? '';
      const key = label.startsWith('主体') ? 'body' : label;
      if (key === 'body') {
        s.fields.body = clean(rest.replace(/^（.*?）/, '').replace(/^[:：]/, ''));
      } else {
        s.fields[key] = clean(rest.replace(/^[:：]/, ''));
      }
    }
  }
  if (!s.fields.body) {
    const inline = s.title.match(/主体（\d+字）[—–-]+\s*(.*)$/);
    if (inline) s.fields.body = inline[1].trim();
  }
}

const out = { total: slides.length, acts: [...new Set(slides.map((s) => s.act).filter(Boolean))], slides };
writeFileSync(dst, JSON.stringify(out, null, 2), 'utf8');
console.log(`Parsed ${slides.length} slides -> ${dst}`);
