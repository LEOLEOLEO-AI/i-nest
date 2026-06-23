fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

# Find the base path used in file:// links
import re
links = re.findall(r'file:///[^"\']*', html)
print(f"Found {len(links)} file:// links")
for l in links[:5]:
    print(f"  {l[:120]}")

# Check the actual base path
if "file:///D:/Obsidian/" in html:
    print("\nBase path: file:///D:/Obsidian/")
    print("This is WRONG - missing home/work/.openclaw/workspace/")
    
# The correct base should be:
# file:///D:/Obsidian/home/work/.openclaw/workspace/
