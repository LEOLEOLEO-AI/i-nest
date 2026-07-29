"""Dedup: keep largest+newest, move older duplicates to archive"""
import os, sys, hashlib
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from collections import defaultdict
from datetime import datetime

VAULT = Path(r"D:\Obsidian\vault")
ARCHIVE = VAULT / "80_Archive" / "duplicates"
ARCHIVE.mkdir(parents=True, exist_ok=True)

# Group by filename stem (case-insensitive)
groups = defaultdict(list)
for f in VAULT.rglob("*.md"):
    if any(p in f.parts for p in [".obsidian", ".git", ".venv", "node_modules", "__pycache__", ".trash", "80_Archive/duplicates"]):
        continue
    key = f.stem.lower()
    groups[key].append(f)

dupes = {k: v for k, v in groups.items() if len(v) > 1}
print(f"Found {len(dupes)} duplicate name groups")

moved = 0
kept = 0
log_lines = [f"# 去重日志 — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]

for name, files in sorted(dupes.items()):
    # Sort: largest first, then newest
    files.sort(key=lambda f: (f.stat().st_size, f.stat().st_mtime), reverse=True)
    keeper = files[0]
    dupes_to_move = files[1:]
    
    for dup in dupes_to_move:
        try:
            rel = dup.relative_to(VAULT)
            dest = ARCHIVE / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dup.rename(dest)
            log_lines.append(f"- ~~{rel}~~ → 80_Archive/duplicates/{rel} (kept: {keeper.relative_to(VAULT)})")
            moved += 1
        except Exception as e:
            log_lines.append(f"- FAILED: {rel}: {e}")
    kept += 1

# Save log
log_path = VAULT / "60_MOC" / "00_Dedup_Log.md"
log_path.write_text("\n".join(log_lines), encoding="utf-8")

print(f"Kept: {kept}, Moved to archive: {moved}")
print(f"Log: {log_path}")
