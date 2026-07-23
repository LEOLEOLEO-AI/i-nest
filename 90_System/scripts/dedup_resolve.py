# -*- coding: utf-8 -*-
"""P7: Smart dedup - auto-resolve clear cases, flag ambiguous for review"""

import json, re, shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")

# Priority: higher = keep
DIR_PRIORITY = {
    "50_Output": 10,
    "40_iNEST": 8,
    "30_TCC": 8,
    "60_MOC": 7,
    "20_Processing": 5,
    "00_Inbox": 3,
    "80_Archive": 1,
    "90_System": 6,
    "70_Dashboard": 6,
}

def get_dir_priority(path_str):
    for prefix, pri in DIR_PRIORITY.items():
        if path_str.startswith(prefix):
            return pri
    return 0

def normalize_name(name):
    n = name.lower()
    n = re.sub(r"\s+\d+\.md$", ".md", n)
    n = re.sub(r"_\d+\.md$", ".md", n)
    n = re.sub(r"_\d+_\d+\.md$", ".md", n)
    return n

# Load report
report = json.loads((VAULT / "60_MOC" / "dedup_report.json").read_text(encoding="utf-8"))

SKIP_PATTERNS = ["skill.md", "readme.md", "changelog.md", "contributing.md", "license.md"]

auto_resolved = 0
manual_review = 0
skipped = 0
errors = []

review_items = []

for group in report["groups"]:
    nname = group["normalized_name"]
    files = group["files"]
    
    # Skip structural files
    if nname in SKIP_PATTERNS:
        skipped += len(files)
        continue
    
    # Skip if all files are in different skill/project contexts
    if nname == "skill.md":
        skipped += len(files)
        continue
    
    # Score each file: priority * 1000 + size
    for f in files:
        f["score"] = get_dir_priority(f["path"]) * 1000000 + f["size"]
    
    files.sort(key=lambda x: -x["score"])
    winner = files[0]
    losers = files[1:]
    
    # Check if auto-resolve is safe: winner must have clearly higher score
    # and be in a target directory
    if get_dir_priority(winner["path"]) >= 5:
        # Check if losers are clearly inferior
        all_clear = True
        for loser in losers:
            loser_pri = get_dir_priority(loser["path"])
            # If loser is also in a high-priority dir and similar size, flag for review
            if loser_pri >= 7 and loser["size"] > winner["size"] * 0.9:
                all_clear = False
                break
        
        if all_clear:
            # Auto-resolve
            for loser in losers:
                loser_path = VAULT / loser["path"]
                if loser_path.exists():
                    winner_name = Path(winner["path"]).stem
                    callout = f'> [!note]- 可能重复: [[{winner_name}]]\n> 此文件与 [[{winner_name}]] 内容重复，已保留高质量版本。\n'
                    try:
                        loser_path.write_text(callout, encoding="utf-8")
                        auto_resolved += 1
                    except Exception as e:
                        errors.append(f"{loser['path']}: {e}")
        else:
            manual_review += len(files)
            review_items.append(group)
    else:
        # Winner is in low-priority dir, needs review
        manual_review += len(files)
        review_items.append(group)

print(f"Auto-resolved: {auto_resolved} files marked as duplicates")
print(f"Manual review needed: {len(review_items)} groups ({manual_review} files)")
print(f"Skipped (structural): {skipped}")
if errors:
    print(f"Errors: {len(errors)}")

# Save review items
review_report = {
    "timestamp": datetime.now().isoformat(),
    "total_groups": len(review_items),
    "groups": review_items
}
(VAULT / "60_MOC" / "dedup_review.json").write_text(
    json.dumps(review_report, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nReview items saved to: 60_MOC/dedup_review.json")
