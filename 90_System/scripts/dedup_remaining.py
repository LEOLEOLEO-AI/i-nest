import os, re, collections

vault = r'D:\Obsidian\vault'
title_files = collections.defaultdict(list)
skip_dirs = {'.obsidian', '.venv', '.git', '.neural_db', '.neural_memory', '.smart-connections', '.trash', 'copilot'}

for root, dirs, files in os.walk(vault):
    dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]
    for f in files:
        if not f.endswith('.md'):
            continue
        full = os.path.join(root, f)
        rel = os.path.relpath(full, vault)
        base = re.sub(r'[_\s]*\d+\.md$', '.md', f)
        base = re.sub(r'\s*\(\d+\)\.md$', '.md', base)
        size = os.path.getsize(full)
        title_files[base].append((rel, size))

dupes = []
for base, files in title_files.items():
    if len(files) <= 1:
        continue
    non_stubs = [(r,s) for r,s in files if s >= 600]
    if len(non_stubs) > 1:
        dupes.append((base, len(non_stubs), len(files), files))

dupes.sort(key=lambda x: -x[1])
priority = ['30_TCC', '40_iNEST', '50_Output', '03_Topics', '00_MOC']

processed = 0
for base, non_stub_count, total, files in dupes:
    if re.match(r'^\d{4}-\d{2}-\d{2}\.md$', base):
        continue
    if base == 'README.md':
        continue
    if '宽屏目录仪表盘' in base:
        continue

    best = None
    best_score = -1
    for rel, size in files:
        if size < 600:
            continue
        score = size
        for i, p in enumerate(reversed(priority)):
            if p in rel:
                score += (i+1) * 10000
                break
        if score > best_score:
            best_score = score
            best = rel

    if not best:
        continue

    for rel, size in files:
        if rel == best:
            continue
        if size < 600:
            continue
        full = os.path.join(vault, rel)
        stub = '---\nmerged_into: "' + best.replace('\\','/') + '"\nmerged_date: 2026-07-03\n---\n\n> \U0001f4ce Merged -> [[' + best.replace('\\','/') + ']]'
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w', encoding='utf-8') as fh:
            fh.write(stub)
        processed += 1
        print('STUB: ' + rel + ' -> ' + best)

print('')
print('Total stubs created: ' + str(processed))
