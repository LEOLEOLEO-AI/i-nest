import os, json

base = r"D:\Obsidian\home\work\.openclaw\workspace"

# 1. Recreate the index file with a shorter, reliable name
title = "From Compute to Complexity: A Physical Theory of Intelligence Emergence"
safe = title.replace("/", "-").replace(":", "-").replace("?", "").replace("*", "").replace('"', "").replace("|", "-")
short = safe[:80]
fname = short + ".md"
fpath = os.path.join(base, "papers", "TCC", fname)

with open(fpath, "w", encoding="utf-8") as f:
    f.write('---\n')
    f.write('title: "' + title + '"\n')
    f.write("dimension: TCC\n")
    f.write("category: 论文\n")
    f.write("version: V27\n")
    f.write("date: 2026-06-05\n")
    f.write("status: 撰写中\n")
    f.write("priority: 高\n")
    f.write('source: "TCC_2_论文撰写/A1_CST_Theory_V27_FINAL.md"\n')
    f.write("---\n\n")
    f.write("# " + title + "\n\n")
    f.write("| 属性 | 值 |\n")
    f.write("|------|-----|\n")
    f.write("| 版本 | V27 (2026-06-05 01:17) |\n")
    f.write("| 状态 | 撰写中 |\n")
    f.write("| 源文件 | TCC_2_论文撰写/A1_CST_Theory_V27_FINAL.md |\n\n")
    f.write("CST理论核心论文：智能涌现的物理理论及其对AGI的启示。\n\n")
    f.write("---\n")
    f.write("> 由研发看板自动索引\n")

print("Created: " + fname)

# 2. Update kanban HTML - fix link path and update to V27
html_path = os.path.join(base, "dashboard", "index.html")
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Fix the link and version for this entry
old_link = '"link": "papers/TCC/From Compute to Complexity- A Physical Theory of Intelligence Emergence and Its Implications for AGI.md"'
new_link = '"link": "papers/TCC/' + fname + '"'
if old_link in html:
    html = html.replace(old_link, new_link)
    print("Fixed link path")
else:
    print("Old link not found, trying partial...")
    if "From Compute to Complexity" in html and "AGI" in html:
        # Find and replace the link
        import re
        html = re.sub(r'"link": "papers/TCC/From Compute to Complexity.*?\.md"', 
                     '"link": "papers/TCC/' + fname + '"', html)
        print("Fixed via regex")

# Update V26 to V27
old_ver = '"title": "From Compute to Complexity: A Physical Theory of Intelligence Emergence", "ver": "V26"'
new_ver = '"title": "From Compute to Complexity: A Physical Theory of Intelligence Emergence", "ver": "V27"'
if old_ver in html:
    html = html.replace(old_ver, new_ver)
    print("Updated V26 -> V27")
else:
    # Try with space after colon
    old_ver2 = '"ver": "V26", "date": "2026-06-04"'
    new_ver2 = '"ver": "V27", "date": "2026-06-05"'
    idx = html.find('"From Compute to Complexity"')
    if idx > 0:
        chunk = html[idx:idx+200]
        if 'V26' in chunk:
            html = html[:idx] + html[idx:].replace('"ver": "V26"', '"ver": "V27"', 1)
            html = html[:idx] + html[idx:].replace('"date": "2026-06-04"', '"date": "2026-06-05"', 1)
            print("Updated V26->V27 and date via position")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)
print("Kanban updated")
