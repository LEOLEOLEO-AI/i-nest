fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

# Fix: change base path from file:///D:/Obsidian/ to file:///D:/Obsidian/home/work/.openclaw/workspace/
old_base = "file:///D:/Obsidian/"
new_base = "file:///D:/Obsidian/home/work/.openclaw/workspace/"

count = html.count(old_base)
html = html.replace(old_base, new_base)
print(f"Fixed {count} occurrences")

# Also check for any 'D:/Obsidian/' in anchor hrefs
import re
anchors = re.findall(r'href="file:///[^"]*"', html)
print(f"href links after fix:")
for a in anchors[:3]:
    print(f"  {a[:130]}")

with open(fpath, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Done. Size: {len(html)}")
