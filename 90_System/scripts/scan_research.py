import json, re
from pathlib import Path

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")

# Target dirs with real research content
TARGET_DIRS = [
    "30_TCC/31_Theory", "30_TCC/32_Tech", "30_TCC/33_Dev",
    "40_iNEST/41_Theory", "40_iNEST/42_Tech", "40_iNEST/43_Dev",
]

research_files = []

for td in TARGET_DIRS:
    d = VAULT / td
    if not d.exists():
        continue
    for f in d.rglob("*.md"):
        size = f.stat().st_size
        if size < 2000:
            continue  # skip small/stub files
        content = f.read_text(encoding="utf-8", errors="ignore")
        if "可能重复" in content and len(content) < 300:
            continue  # skip dedup stubs
        # Skip obvious diary/journal entries
        name = f.name.lower()
        if any(kw in name for kw in ["日记", "每日", "无标题", "待办", "todo", "weekly"]):
            continue
        research_files.append({
            "path": str(f.relative_to(VAULT)),
            "size": size,
            "dir": td,
            "name": f.name,
        })

# Sort by size desc
research_files.sort(key=lambda x: -x["size"])

# Group by dir
from collections import Counter
dir_counts = Counter(r["dir"] for r in research_files)

print(f"Total substantial research files: {len(research_files)}")
print()
for d, c in dir_counts.most_common():
    print(f"  {d}: {c}")
print()

# Top files by size
print("=== Top 30 by size ===")
for r in research_files[:30]:
    kb = r["size"] / 1024
    print(f"  [{kb:.1f}KB] {r['name'][:80]}")

# Save list
(VAULT / "60_MOC" / "research_files.json").write_text(
    json.dumps(research_files, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nSaved: {len(research_files)} files to 60_MOC/research_files.json")
