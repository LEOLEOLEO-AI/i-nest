import json, os

fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

# Extract all link values from entries
import re
links = re.findall(r'"link":\s*"([^"]+)"', html)
print(f"Total links: {len(links)}")
print()

workspace_base = r"D:\Obsidian\home\work\.openclaw\workspace"
broken = []
ok = []

for link in links:
    full = os.path.join(workspace_base, link.replace("/", "\\"))
    exists = os.path.exists(full)
    
    if not exists:
        # Try from Obsidian root
        full2 = os.path.join(r"D:\Obsidian", link.replace("/", "\\"))
        exists2 = os.path.exists(full2)
        if exists2:
            broken.append((link, "outside workspace"))
        else:
            broken.append((link, "not found anywhere"))
    else:
        ok.append(link)

print("=== OK (inside workspace) ===")
for l in ok:
    print(f"  OK: {l}")

print(f"\n=== BROKEN ({len(broken)}) ===")
for l, reason in broken:
    print(f"  BROKEN ({reason}): {l}")
