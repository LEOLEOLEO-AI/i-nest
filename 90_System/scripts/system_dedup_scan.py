import os, json
from pathlib import Path
from collections import defaultdict

# All directories to scan
SCAN_ROOTS = [
    Path(r"D:\Obsidian"),
    Path(r"D:\iNEST"),
    Path(r"D:\Output"),
]

# But limit depth to avoid scanning everything
EXCLUDE_PATTERNS = [".git", ".venv", "node_modules", ".obsidian", ".trash", ".neural_db", ".neural_memory"]

def count_md(root, max_depth=3):
    md_files = []
    try:
        for item in root.rglob("*.md"):
            # Limit depth
            depth = len(item.relative_to(root).parts)
            if depth > max_depth:
                continue
            # Skip excluded
            if any(ex in item.parts for ex in EXCLUDE_PATTERNS):
                continue
            md_files.append({
                "path": str(item),
                "size": item.stat().st_size,
                "mtime": item.stat().st_mtime,
                "name": item.name,
            })
    except PermissionError:
        pass
    return md_files

all_files = []
for root in SCAN_ROOTS:
    if root.exists():
        files = count_md(root)
        print(f"{root}: {len(files)} md files")
        all_files.extend(files)

# Build name index
name_index = defaultdict(list)
for f in all_files:
    name_index[f["name"].lower()].append(f)

# Find duplicates (same normalized name, different path)
dups = {k: v for k, v in name_index.items() if len(v) > 1}
print(f"\nDuplicate groups: {len(dups)}")

# Show top dup groups
sorted_dups = sorted(dups.items(), key=lambda x: -len(x[1]))
for name, files in sorted_dups[:30]:
    # Check if any are in the vault
    in_vault = [f for f in files if "vault" in f["path"]]
    outside = [f for f in files if "vault" not in f["path"]]
    print(f"\n{name} x{len(files)} (vault:{len(in_vault)}, outside:{len(outside)})")
    for f in files[:5]:
        loc = "VAULT" if "vault" in f["path"] else "OUTSIDE"
        size_kb = f["size"] / 1024
        path_short = f["path"].replace("D:\\", "")
        print(f"  [{loc}] {size_kb:.1f}KB {path_short[:100]}")

