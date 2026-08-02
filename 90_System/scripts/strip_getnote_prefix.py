# -*- coding: utf-8 -*-
"""Strip all getnote_ / getnote / 18-digit numeric ID prefixes from filenames."""
import re
import sys
from pathlib import Path

VAULT = Path(r"D:/obsidian/vault")
APPLY = "--apply" in sys.argv

rename_ops = []

# Pattern: "getnote" optionally followed by "_" then optionally 18-digit number then "_"
# We want to strip ALL leading getnote blocks before first meaningful content
GETNOTE_RE = re.compile(r'^(getnote_)+(\d{16,20}_)?')
# Also handle directory name getnote_external -> external
GETNOTE_DIR_RE = re.compile(r'^getnote_external$')

for f in VAULT.rglob("*"):
    if not f.is_file():
        continue
    if any(s in f.relative_to(VAULT).parts for s in {'.git', '.workbuddy', 'node_modules'}):
        continue
    if f.suffix.lower() != '.md':
        continue

    name = f.name
    if 'getnote' not in name.lower():
        continue

    newname = name
    # Strip all leading getnote_ blocks with optional numeric ID
    newname = GETNOTE_RE.sub('', newname)
    # Strip any remaining getnote_ that wasn't at the very start
    newname = re.sub(r'_getnote_(\d{16,20}_)?', '_', newname)
    # Clean up double underscores
    newname = re.sub(r'_{2,}', '_', newname)

    if newname != name and newname:
        rename_ops.append((f, f.parent / newname))

# Also handle directory renames
dir_rename = []
for d in VAULT.rglob("*"):
    if not d.is_dir():
        continue
    if any(s in d.relative_to(VAULT).parts for s in {'.git', '.workbuddy', 'node_modules'}):
        continue
    if d.name == 'getnote_external':
        dir_rename.append((d, d.parent / 'external_imports'))

print(f"文件重命名: {len(rename_ops)}")
print(f"目录重命名: {len(dir_rename)}")
print()

# Show samples
for src, dst in rename_ops[:10]:
    print(f"  {src.name}")
    print(f"  → {dst.name}")
    print()

if APPLY:
    # Do dir renames first
    for src, dst in dir_rename:
        if dst.exists():
            print(f"SKIP dir: {dst.name} already exists")
            continue
        print(f"  {src.name} → {dst.name}")
        src.rename(dst)

    # Then file renames
    ok = fail = skip = 0
    for src, dst in rename_ops:
        if dst.exists():
            print(f"SKIP: {dst.name} exists")
            skip += 1
            continue
        try:
            if not dst.parent.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
            src.rename(dst)
            ok += 1
        except Exception as e:
            print(f"FAIL: {src.name} — {e}")
            fail += 1

    print(f"\n完成: {ok} 成功, {fail} 失败, {skip} 跳过")
else:
    print("DRY RUN。加 --apply 真正执行。")
