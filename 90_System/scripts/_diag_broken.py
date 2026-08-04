#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""临时诊断脚本：分析断链模式分类"""
import re
from pathlib import Path
from collections import defaultdict

VAULT = Path(r"D:/obsidian/vault")
link_re = re.compile(r'\[\[([^\]]+)\]\]')

# 收集所有笔记名和路径
note_basenames = set()
note_paths = set()
file_paths = set()
dirs_set = set()
aliases = set()

for f in VAULT.rglob('*'):
    rel = f.relative_to(VAULT).as_posix()
    if rel.startswith('.git') or rel.startswith('.workbuddy'):
        continue
    if f.is_dir():
        dirs_set.add(rel)
        continue
    if f.is_file():
        noext = rel[:-len(f.suffix)] if f.suffix else rel
        file_paths.add(rel)
        file_paths.add(noext)
        if f.suffix.lower() == '.md':
            note_paths.add(noext)
            note_paths.add(rel)
            note_basenames.add(f.stem)

# 解析 aliases
for f in VAULT.rglob('*.md'):
    rel = f.relative_to(VAULT).as_posix()
    if rel.startswith('.git') or rel.startswith('.workbuddy'):
        continue
    try:
        txt = f.read_text(encoding='utf-8', errors='ignore')
    except:
        continue
    if txt.startswith('---'):
        end = txt.find('\n---', 3)
        if end != -1:
            fm = txt[3:end]
            in_alias = False
            for ln in fm.split('\n'):
                s = ln.strip()
                if s.startswith('aliases:'):
                    in_alias = True
                    continue
                if in_alias:
                    if s.startswith('- '):
                        v = s[2:].strip().strip('"').strip("'")
                        if v:
                            aliases.add(v)
                    elif s and not s.startswith('#'):
                        in_alias = False

# 扫描断链
broken_freq = defaultdict(int)
for f in VAULT.rglob('*.md'):
    rel = f.relative_to(VAULT).as_posix()
    if rel.startswith('.git') or rel.startswith('.workbuddy'):
        continue
    try:
        txt = f.read_text(encoding='utf-8', errors='ignore')
    except:
        continue
    for m in link_re.findall(txt):
        raw = m.replace('\\|', '|')
        tgt = raw.split('|')[0].split('#')[0].strip().rstrip('\\').strip()
        if tgt:
            ok = (tgt in note_basenames) or (tgt in note_paths) or (tgt in file_paths) or (tgt in dirs_set) or (tgt in aliases)
            if not ok and not tgt.isdigit():
                broken_freq[tgt] += 1

# 分类断链
categories = defaultdict(int)
for tgt, c in broken_freq.items():
    if tgt.startswith('GetNote_') or 'getnote_' in tgt.lower():
        categories['GetNote_long'] += c
    elif re.match(r'^\d{4}[-_\xe5\xb9\xb4]\d{1,2}', tgt) or '\xe6\x97\xa5\xe8\xae\xb0' in tgt:
        categories['date_pattern'] += c
    elif '_S2_' in tgt or 'S2_' in tgt:
        categories['S2_papers'] += c
    elif tgt in ['\xe8\xae\xba\xe6\x96\x87', '\xe7\xac\x94\xe8\xae\xb0', '\xe5\xbc\x95\xe7\x94\xa8', 'PPT', '\xe9\x99\x84\xe4\xbb\xb6']:
        categories['generic'] += c
    else:
        categories['other'] += c

print('=== 断链分类统计 ===')
for k, v in sorted(categories.items(), key=lambda x: -x[1]):
    print(f'  {k}: {v}')
print(f'  总计: {sum(broken_freq.values())}')
print()

# other top 20
other_items = [(t, c) for t, c in broken_freq.items()
               if not (t.startswith('GetNote_') or 'getnote_' in t.lower()
                       or re.match(r'^\d{4}[-_\xe5\xb9\xb4]\d{1,2}', t)
                       or '\xe6\x97\xa5\xe8\xae\xb0' in t or '_S2_' in t or 'S2_' in t
                       or t in ['\xe8\xae\xba\xe6\x96\x87', '\xe7\xac\x94\xe8\xae\xb0', '\xe5\xbc\x95\xe7\x94\xa8', 'PPT', '\xe9\x99\x84\xe4\xbb\xb6'])]
other_items.sort(key=lambda x: -x[1])
print('=== Other 类别 top 20 ===')
for t, c in other_items[:20]:
    print(f'  ({c}) [[{t}]]')
