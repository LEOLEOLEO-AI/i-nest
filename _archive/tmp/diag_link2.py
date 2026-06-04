fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

# Find the modal link generation in openDetail
idx = html.find("function openDetail")
if idx > 0:
    chunk = html[idx:idx+800]
    # Find the link HTML generation
    link_idx = chunk.find("file:///")
    if link_idx > 0:
        print("=== Link generation in openDetail ===")
        print(chunk[link_idx:link_idx+200])
    else:
        print("No file:// found in openDetail")

# Check what a sample link looks like
import re
file_links = re.findall(r"file:///[^'\"]*\+e\.link\+[^'\"]*", html)
print(f"\n=== Dynamic file link templates: {len(file_links)} ===")
for l in file_links:
    print(f"  {l[:150]}")

# Check if encodeURI is used
if "encodeURI" in html:
    print("\nencodeURI: used")
else:
    print("\nencodeURI: NOT used - this is the bug!")
