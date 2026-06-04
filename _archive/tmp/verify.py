import re
fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

# Verify filter fix
onclicks = re.findall(r'onclick="setIndexFilter\([^)]*\)"', html)
print(f"onclick handlers in HTML: {len(onclicks)}")
for o in onclicks:
    has_quot = '&quot;' in o
    print(f"  {'OK' if has_quot else 'BROKEN'}: {o[:100]}")

# Check modal link pattern
if "e.link" in html:
    # Find the openDetail function
    idx = html.find("function openDetail")
    if idx > 0:
        detail = html[idx:idx+1500]
        # Find link-related code
        link_idx = detail.find("e.link")
        if link_idx > 0:
            print(f"\nLink handling in openDetail:")
            print(detail[link_idx-50:link_idx+200])

# Check daily format
if '"daily"' in html:
    idx = html.find('"daily"')
    print(f"\nDaily section starts at: {idx}")
    print(html[idx:idx+300])
