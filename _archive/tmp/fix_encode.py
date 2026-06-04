fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

# Fix: add encodeURI() to the link href in openDetail
# Current: +e.link+'" style=
# Fixed: +encodeURI(e.link)+'" style=
old = "+e.link+'\" style=\"color:var(--tcc);text-decoration:underline;word-break:break-all\" target=\"_blank\">'+e.link+'</a>"
new = "+encodeURI(e.link)+'\" style=\"color:var(--tcc);text-decoration:underline;word-break:break-all\" target=\"_blank\">'+e.link+'</a>"

count = html.count(old)
html = html.replace(old, new)
print(f"Fixed {count} occurrences")

# Also check if there's a copyPath that needs the raw path
# copyPath uses the original unencoded path, which is correct for clipboard

# Verify
if "encodeURI(e.link)" in html:
    print("OK: encodeURI added to link href")
else:
    print("WARNING: encodeURI not found")

with open(fpath, "w", encoding="utf-8") as f:
    f.write(html)
print("Done:", len(html))
