import json, shutil
from pathlib import Path

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
data = json.loads((VAULT / "60_MOC" / "deepseek_analysis.json").read_text(encoding="utf-8"))

moved = 0
tcc_count = 0
inest_count = 0

for r in data["results"]:
    rel_path = r["path"]
    fpath = VAULT / rel_path
    if not fpath.exists():
        continue
    d = r.get("direction", "TCC")
    if d == "iNEST":
        dst = VAULT / "40_iNEST" / "42_Tech" / fpath.name
        inest_count += 1
    else:
        dst = VAULT / "30_TCC" / "32_Tech" / fpath.name
        tcc_count += 1
    if not dst.exists():
        shutil.move(str(fpath), str(dst))
        moved += 1

print(f"Moved: {moved} (TCC: {tcc_count}, iNEST: {inest_count})")

for d in sorted(VAULT.iterdir()):
    if d.is_dir() and not d.name.startswith("."):
        md = sum(1 for _ in d.rglob("*.md"))
        print(f"  {d.name}: {md} md")
