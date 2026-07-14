"""Move stub files (<600 bytes, <10 words) to archive"""
import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
ARCHIVE = VAULT / "80_Archive" / "stubs"
ARCHIVE.mkdir(parents=True, exist_ok=True)

SKIP = {".obsidian", ".git", ".venv", "node_modules", "__pycache__", ".trash", "80_Archive"}

moved = 0
log_lines = [f"# 桩文件清理日志 — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]

for f in VAULT.rglob("*.md"):
    if any(p in f.parts for p in SKIP):
        continue
    size = f.stat().st_size
    if size > 600:
        continue
    try:
        content = f.read_text(encoding="utf-8", errors="replace")
        words = len(re.findall(r'\w+', content))
        if words >= 10:
            continue
        # Stub: move to archive
        rel = f.relative_to(VAULT)
        dest = ARCHIVE / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        f.rename(dest)
        log_lines.append(f"- {rel} ({size}B, {words}w)")
        moved += 1
    except:
        pass

log_path = VAULT / "60_MOC" / "00_Stub_Cleanup_Log.md"
log_path.write_text("\n".join(log_lines), encoding="utf-8")
print(f"Stubs moved to archive: {moved}")
