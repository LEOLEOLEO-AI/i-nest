import json, shutil
from pathlib import Path

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
data = json.loads((VAULT / "60_MOC" / "deepseek_analysis.json").read_text(encoding="utf-8"))

moved = 0
tcc = 0
inest = 0

for r in data["results"]:
    p = r.get("path", "")
    if not p:
        print(f"SKIP: no path - {r.get('file', '?')}")
        continue
    fpath = VAULT / p
    if not fpath.exists():
        continue
    d = r.get("direction", "TCC")
    if d == "iNEST":
        dst = VAULT / "40_iNEST" / "42_Tech" / fpath.name
        inest += 1
    else:
        dst = VAULT / "30_TCC" / "32_Tech" / fpath.name
        tcc += 1
    if not dst.exists():
        shutil.move(str(fpath), str(dst))
        moved += 1

print(f"Moved: {moved} (TCC:{tcc}, iNEST:{inest})")
for d in sorted(VAULT.iterdir()):
    if d.is_dir() and not d.name.startswith("."):
        print(f"  {d.name}: {sum(1 for _ in d.rglob('*.md'))} md")
