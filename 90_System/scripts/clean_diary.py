import shutil, re
from pathlib import Path

VAULT = Path(r"D:\Obsidian\vault")
J = VAULT / "80_Archive" / "Journal"

diary_patterns = [
    r"^\d{4}-\d{2}-\d{2}\.md$",
    r"^\d{4}年\d{1,2}月\d{1,2}号.*日记",
    r"^每日总结",
    r"^每周总结",
    r"^无标题",
    r"getnote.*日记",
]

deleted = 0
for f in list(J.rglob("*.md")):
    if any(re.search(pat, f.name) for pat in diary_patterns):
        f.unlink()
        deleted += 1

print(f"Diary deleted: {deleted}")
print(f"Remaining in Journal: {sum(1 for _ in J.rglob('*.md'))} md")

# Clean empty dirs in 80_Archive
for d in sorted((VAULT / "80_Archive").rglob("*"), reverse=True):
    if d.is_dir() and not list(d.iterdir()):
        d.rmdir()

# Also clean empty dirs elsewhere
for dname in ["00_Inbox"]:
    dp = VAULT / dname
    if dp.exists():
        for sd in sorted(dp.rglob("*"), reverse=True):
            if sd.is_dir() and not list(sd.iterdir()):
                sd.rmdir()
        # If now empty
        if not list(dp.iterdir()):
            dp.rmdir()
            print(f"{dname}: removed (empty)")

# Final
print()
for d in sorted(VAULT.iterdir()):
    if d.is_dir() and not d.name.startswith("."):
        md = sum(1 for _ in d.rglob("*.md"))
        print(f"  {d.name}: {md} md")
