import json
from pathlib import Path
from collections import defaultdict

# Target scan: only directories known to contain Obsidian/research files
SCAN_DIRS = [
    Path(r"D:\Obsidian\vault"),  # Main vault
    Path(r"D:\Obsidian\iNEST_vault"),                      # Old vault
    Path(r"D:\Obsidian"),                                  # Root loose files (depth=1 only)
    Path(r"D:\iNEST"),                                     # Research files
    Path(r"D:\Output\Genspark"),                           # Genspark output
    Path(r"c:\tmp"),                                       # Temp files
]

# Only look at top-level of root dirs, but full depth for named dirs
def scan_dir(path, max_depth=99):
    md_files = []
    try:
        for item in path.rglob("*.md"):
            depth = len(item.relative_to(path).parts)
            if depth > max_depth:
                continue
            if any(x in item.parts for x in [".git", ".venv", "node_modules", ".obsidian", ".trash", ".neural_db"]):
                continue
            md_files.append({
                "path": str(item),
                "size": item.stat().st_size,
                "mtime": item.stat().st_mtime,
                "name": item.name,
            })
    except (PermissionError, FileNotFoundError, OSError):
        pass
    return md_files

VAULT_ROOT = r"D:\Obsidian\vault"
all_files = []

for d in SCAN_DIRS:
    if not d.exists():
        print(f"SKIP (not found): {d}")
        continue
    depth = 1 if d == Path(r"D:\Obsidian") else 50  # root-level only for Obsidian root
    files = scan_dir(d, max_depth=depth)
    in_vault = sum(1 for f in files if VAULT_ROOT in f["path"])
    outside = len(files) - in_vault
    print(f"{d}: {len(files)} md (vault:{in_vault}, other:{outside})")
    all_files.extend(files)

# Build name index
name_index = defaultdict(list)
for f in all_files:
    name_index[f["name"].lower()].append(f)

# Find cross-location duplicates
dups = []
for name, files in name_index.items():
    if len(files) <= 1:
        continue
    # Only count if at least one is in vault AND one is outside
    in_vault = any(VAULT_ROOT in f["path"] for f in files)
    outside_vault = any(VAULT_ROOT not in f["path"] for f in files)
    if in_vault and outside_vault:
        dups.append((name, files))

print(f"\nCross-location dups: {len(dups)} groups")

# Show top 40
for name, files in sorted(dups, key=lambda x: -len(x[1]))[:40]:
    vault_files = [f for f in files if VAULT_ROOT in f["path"]]
    other_files = [f for f in files if VAULT_ROOT not in f["path"]]
    total_size_other = sum(f["size"] for f in other_files) / 1024
    print(f"\n{name} | vault:{len(vault_files)} other:{len(other_files)} ({total_size_other:.1f}KB waste)")
    for f in other_files[:3]:
        path_short = f["path"].replace("D:\\", "").replace("c:\\", "")
        print(f"  → DEL: {path_short[:120]}")
    if len(other_files) > 3:
        print(f"  ... and {len(other_files)-3} more outside vault")

# Save full report
report = []
for name, files in dups:
    vault_files = [f for f in files if VAULT_ROOT in f["path"]]
    other_files = [f for f in files if VAULT_ROOT not in f["path"]]
    report.append({
        "name": name,
        "vault_count": len(vault_files),
        "vault_paths": [f["path"] for f in vault_files],
        "outside_count": len(other_files),
        "outside_paths": [f["path"] for f in other_files],
        "waste_kb": sum(f["size"] for f in other_files) / 1024,
    })

vault_path = Path(r"D:\Obsidian\vault\60_MOC\system_dedup_report.json")
vault_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nReport saved: 60_MOC/system_dedup_report.json")
