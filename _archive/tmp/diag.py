import re
fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

# Find onclick patterns containing setIndexFilter
pat = r'onclick="[^"]*setIndexFilter[^"]*"'
onclicks = re.findall(pat, html)
print(f"Found {len(onclicks)} onclick setIndexFilter patterns")
for i, o in enumerate(onclicks):
    print(f"  [{i}] {o[:150]}")

# Check for backslash-quote in onclick
if 'onclick="setIndexFilter(\\' in html:
    print("Has escaped quotes in onclick")
    idx = html.find('onclick="setIndexFilter(\\')
    print(f"  Sample: ...{html[idx:idx+100]}...")

# Check for double-double-quote issue  
if 'setIndexFilter("dim"' in html:
    print("WARNING: nested double quotes found!")
if 'setIndexFilter(&quot;dim&quot;' in html:
    print("OK: HTML entities used")

# Check the actual pattern around dim filter
idx = html.find('全部维度')
if idx > 0:
    context = html[idx-200:idx+50]
    print(f"\nContext around dim filter:\n{context}")
