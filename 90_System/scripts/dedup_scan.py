# -*- coding: utf-8 -*-
"""P7: Full dedup scan - find all duplicate filename groups with details"""

import os, re, json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")

# Normalize filename: remove number suffixes like " 1", " 2", "_1", "_v1", etc.
def normalize_name(name):
    n = name.lower()
    n = re.sub(r'\s+\d+\.md$', '.md', n)
    n = re.sub(r'_\d+\.md$', '.md', n)
    n = re.sub(r'_\d+_\d+\.md$', '.md', n)
    return n

# First pass: collect all files
name_map = defaultdict(list)

for root, dirs, files in os.walk(VAULT):
    # Skip hidden dirs and certain paths
    rel = Path(root).relative_to(VAULT)
    rel_str = str(rel)
    if any(part.startswith('.') for part in rel.parts):
        continue
    for f in files:
        if f.endswith('.md'):
            fpath = Path(root) / f
            nname = normalize_name(f)
            name_map[nname].append({
                'path': str(fpath.relative_to(VAULT)),
                'size': fpath.stat().st_size,
                'name': f,
            })

# Find duplicates
dups = {k: v for k, v in name_map.items() if len(v) > 1}

# Sort by number of duplicates (descending)
sorted_dups = sorted(dups.items(), key=lambda x: -len(x[1]))

print(f"Total duplicate groups: {len(sorted_dups)}")
print(f"Total files involved: {sum(len(v) for v in dups.values())}")
print()

# Show top 50
for i, (name, files) in enumerate(sorted_dups[:50]):
    sizes = [str(f['size']) for f in files]
    max_size = max(f['size'] for f in files)
    print(f"\n{i+1}. '{name}' x{len(files)} (max: {max_size}B)")
    for f in files[:6]:
        flag = ' ★LARGEST' if f['size'] == max_size and len(files) > 1 else ''
        print(f"   [{f['size']:>6}B] {f['path']}{flag}")
    if len(files) > 6:
        print(f"   ... and {len(files)-6} more")

# Save full report as JSON
report = {
    'timestamp': datetime.now().isoformat(),
    'total_groups': len(sorted_dups),
    'groups': []
}

for name, files in sorted_dups:
    report['groups'].append({
        'normalized_name': name,
        'count': len(files),
        'files': [{'path': f['path'], 'size': f['size'], 'name': f['name']} for f in files]
    })

report_path = VAULT / '60_MOC' / 'dedup_report.json'
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"\n\nFull report saved to: 60_MOC/dedup_report.json")
print(f"Total groups: {len(sorted_dups)}")
