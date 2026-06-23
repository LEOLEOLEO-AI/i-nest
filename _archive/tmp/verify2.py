fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

# Check modal link
if "<a href=" in html and "e.link" in html:
    # Find the anchor with e.link
    idx = html.find("<a href=")
    if idx > 0:
        # Find one near e.link
        e_idx = html.find("e.link", idx)
        if e_idx > 0 and e_idx - idx < 500:
            print("Link fix: OK - anchor tag found near e.link")
            print("  Sample:", html[idx:idx+150])
        else:
            print("Link fix: anchor found but not near e.link")
else:
    print("Link fix: no anchor with e.link")

# Check onclick fix
if 'onclick="setIndexFilter(&quot;' in html:
    print("Filter fix: OK - &quot; entities present")
else:
    print("Filter fix: MISSING")

# Check daily
if "2026-06-05" in html:
    print("Daily: 6/5 present")
    idx = html.find("2026-06-05")
    print("  Context:", html[idx:idx+200])
