import re, json

fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

print("Before:", len(html))

# FIX 1: Filter chip onclick - replace \" with &quot; inside onclick handlers
# The pattern in the JS source: onclick=\"setIndexFilter(\\\"dim\\\",null)\"
# After HTML generation this becomes: onclick="setIndexFilter(\"dim\",null)"
# We need: onclick="setIndexFilter(&quot;dim&quot;,null)"
# 
# Strategy: find all onclick="setIndexFilter(...)" and replace inner \" with &quot;

def fix_onclick_quotes(m):
    s = m.group(0)
    # Replace \" with &quot; inside the onclick value
    # The escaped backslash-quote in JS source becomes " in HTML output
    s = s.replace('\\"', '&quot;')
    return s

pat = r'onclick="setIndexFilter\([^"]*\)"'
count = len(re.findall(pat, html))
html = re.sub(pat, fix_onclick_quotes, html)
print(f"Fixed {count} onclick handlers")

# Verify
if '&quot;dim&quot;' in html:
    print("OK: HTML entities in dim filter")
else:
    print("WARNING: dim filter may not be fixed")
if '&quot;cat&quot;' in html:
    print("OK: HTML entities in cat filter")
else:
    print("WARNING: cat filter may not be fixed")

# FIX 2: Make modal links clickable
# Find the pattern where e.link is displayed as <code> and replace with <a href>
old_link = '<code style=\\"background:var(--surface2);padding:4px 8px;border-radius:4px;font-size:0.85em;word-break:break-all\\">'
new_link = '<a href=\\"file:///D:/Obsidian/'

# Try to find and replace the code pattern in the link display
if old_link in html:
    html = html.replace(old_link, new_link)
    # Also fix the closing tag
    html = html.replace("'+e.link+'</code>", "'+e.link+'</a>")
    print("OK: Modal links now clickable")
else:
    print("INFO: Checking for alternate link patterns...")
    if "'+e.link+'</code>" in html:
        print("  Found closing code tag pattern")
    if "e.link" in html:
        print("  e.link references exist in HTML")

# FIX 3: Update daily to include 6/5 - replace the daily array
# The DEFAULT_DATA is embedded in the HTML. Let's find and update it.
# We'll find the daily array start and insert the 6/5 record
old_marker = '{"date":"2026-06-04","type":"yesterday"'
new_0605 = '{"date":"2026-06-05","type":"today","progress":[{"text":"看板v3迭代：修复筛选联动、文件超链接、新增14篇论文专利索引","dot":"done","dim":"TCC+iNEST"},{"text":"Meta-Topology SDI-Bond论文v3修订完成","dot":"done","dim":"TCC"},{"text":"CST Theory V26修订版定稿","dot":"done","dim":"TCC"},{"text":"SDI v30多区域拓扑仿真参数调优","dot":"ongoing","dim":"TCC"},{"text":"连接组数据下载管线搭建","dot":"ongoing","dim":"iNEST"}],"plan":[{"text":"SDI v30多区域跨尺度耦合验证","dot":"plan","dim":"TCC"},{"text":"FEP-STDP收敛性证明完成并写入专利","dot":"plan","dim":"iNEST"},{"text":"iNEST核心架构论文Results撰写","dot":"plan","dim":"iNEST"}]},' + old_marker

if old_marker in html:
    html = html.replace(old_marker, new_0605)
    print("OK: Added 6/5 daily record")
else:
    print("WARNING: 6/4 marker not found")
    # Try different marker
    alt = "2026-06-04"
    if alt in html:
        idx = html.find(alt)
        print(f"  Found 2026-06-04 at position {idx}")

with open(fpath, "w", encoding="utf-8") as f:
    f.write(html)
print("After:", len(html))
print("Done!")
