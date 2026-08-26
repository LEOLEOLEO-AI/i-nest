import json, os
from pathlib import Path

VAULT = Path(r"D:\Obsidian\vault")

def cnt(dirname):
    d = VAULT / dirname
    return sum(1 for _ in d.rglob("*.md")) if d.exists() else 0

for sub in ["31_Theory","32_Technology","33_Engineering","34_Projects","35_Simulation"]:
    print(f"TCC_{sub}: {cnt(f'30_TCC/{sub}')}")
for sub in ["41_Theory","42_Technology","43_Engineering","44_Projects","45_Simulation"]:
    print(f"INEST_{sub}: {cnt(f'40_iNEST/{sub}')}")
for sub in ["51_Papers","52_Patents","53_Monographs","54_Code","55_Guides"]:
    print(f"OUT_{sub}: {cnt(f'50_Output/{sub}')}")

now = __import__("time").time()
recent = []
for f in VAULT.rglob("*.md"):
    if now - f.stat().st_mtime < 7*86400:
        recent.append(str(f.relative_to(VAULT)))
print(f"RECENT: {len(recent)}")

try:
    data = json.loads((VAULT/"60_MOC"/"deepseek_analysis.json").read_text("utf-8"))
    th = sum(1 for r in data["results"] if r.get("direction")=="TCC" and r.get("paper") in ("高","中"))
    ih = sum(1 for r in data["results"] if r.get("direction")=="iNEST" and r.get("paper") in ("高","中"))
    print(f"HIGH_TCC: {th}")
    print(f"HIGH_INEST: {ih}")
except:
    print("HIGH_TCC: 0")
    print("HIGH_INEST: 0")

# Total
for dname in ["30_TCC","40_iNEST","50_Output","80_Archive","90_System","60_MOC"]:
    print(f"TOTAL_{dname}: {cnt(dname)}")
