import json, re
from pathlib import Path
from collections import defaultdict

v = Path(r"D:\Obsidian\home\work\.openclaw\workspace")

all_files = []
for d in ["30_TCC", "40_iNEST", "50_Output/51_Papers"]:
    p = v / d
    if p.exists():
        for f in p.rglob("*.md"):
            all_files.append({"name": f.name, "stem": f.stem, "path": str(f.relative_to(v)), "size": f.stat().st_size, "dir": d})

def normalize_strict(name):
    n = name.lower()
    n = re.sub(r"[_\-\.]v\d+(\.\d+)*", "", n)
    n = re.sub(r"[_\-\.]V\d+", "", n)
    n = re.sub(r"[_\-\.]ver[\s\.]*\d+", "", n)
    n = re.sub(r"[_\-\.]version[\s\.]*\d+", "", n)
    n = re.sub(r"[_\-\.](FINAL|final|DRAFT|draft|clean|dup|copy|WIP)", "", n)
    n = re.sub(r"[_\-\.]\d{8}", "", n)
    n = re.sub(r"[_\-\.]\d{4}[-\.]\d{2}[-\.]\d{2}", "", n)
    n = re.sub(r"^\d+[_\-\.]+", "", n)
    n = re.sub(r"[_\-\.]重新生成版", "", n)
    n = re.sub(r"[_\-\.]副本", "", n)
    n = re.sub(r"\s+", " ", n)
    return n.strip("_- .")[:50]

groups = defaultdict(list)
for f in all_files:
    key = normalize_strict(f["stem"])
    groups[key].append(f)

multi = [(k, v) for k, v in groups.items() if len(set(f["dir"] for f in v)) > 1]
print(f"Cross-directory duplicate groups: {len(multi)}")

for key, files in sorted(multi, key=lambda x: len(x[1]), reverse=True)[:25]:
    dirs = set(f["dir"] for f in files)
    print(f"  [{len(files)} copies in {len(dirs)} dirs] {key[:60]}")
    for f in files:
        print(f"    - [{f['dir']}] {f['name'][:70]}")

# Summary
total_copies = sum(len(files) for _, files in multi)
total_unique = len(groups) - len(multi) + sum(1 for _, files in multi if len(files) > 0)
print(f"\nTotal cross-dir duplicates: {total_copies} copies across {len(multi)} groups")
