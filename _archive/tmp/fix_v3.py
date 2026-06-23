import re

fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

print("Before:", len(html))

# The bug: JS source has onclick="setIndexFilter(\"dim\",null)"
# The \" in JS strings becomes " in HTML output, creating nested quotes
# Fix: replace \" with &quot; INSIDE onclick handlers in the JS source
# 
# Match: onclick="setIndexFilter( ... )"  where ... may contain \"
# Replace inner \" with &quot;

def fix_handler(m):
    s = m.group(0)
    # Replace all \" inside with &quot;
    s = s.replace('\\"', '&quot;')
    return s

# Match each onclick="setIndexFilter(...)" pattern (greedy match to end quote)
pat = r'onclick="setIndexFilter\([^"]*(?:"[^"]*"[^"]*)*\)"'
count = 0
def count_fix(m):
    global count
    count += 1
    return fix_handler(m)

html = re.sub(pat, count_fix, html)
print(f"Fixed {count} onclick handlers")

# Verify the fix
if 'onclick="setIndexFilter(&quot;dim&quot;,null)"' in html:
    print("OK: dim filter uses &quot;")
if 'onclick="setIndexFilter(&quot;cat&quot;,' in html:
    print("OK: cat filter uses &quot;")  
if 'onclick="setIndexFilter(&quot;status&quot;,' in html:
    print("OK: status filter uses &quot;")

# FIX 2: Make modal links clickable - replace code tag with anchor
# The pattern in openDetail: <code style="...">'+e.link+'</code>
# Replace with: <a href="file:///D:/Obsidian/'+e.link+'" ...>'+e.link+'</a>
old = "<code style=\\"
if old in html:
    # Find the full code tag pattern
    code_idx = html.find("<code style=\\")
    # Find the closing context
    snippet = html[code_idx:code_idx+200]
    print(f"Found code tag: {snippet[:100]}...")
    
    # Replace the pattern
    old_full = "<code style=\\\"background:var(--surface2);padding:4px 8px;border-radius:4px;font-size:0.85em;word-break:break-all\\\">'+e.link+'</code>"
    new_full = "<a href=\\\"file:///D:/Obsidian/'+e.link+'\\\" style=\\\"color:var(--tcc);text-decoration:underline;word-break:break-all\\\" target=\\\"_blank\\\">'+e.link+'</a>"
    if old_full in html:
        html = html.replace(old_full, new_full)
        print("OK: Modal link now clickable")
    else:
        print("Full pattern not found, trying simpler...")
        # Try just replacing '</code>' near e.link
        if "'+e.link+'</code>" in html:
            html = html.replace("'+e.link+'</code>", "'+e.link+'</a>")
            # Also replace opening code tag
            html = html.replace("<code style=\\\"background:var(--surface2);padding:4px 8px;border-radius:4px;font-size:0.85em;word-break:break-all\\\">'+e.link+'", 
                               "<a href=\\\"file:///D:/Obsidian/'+e.link+'\\\" style=\\\"color:var(--tcc);text-decoration:underline;word-break:break-all\\\" target=\\\"_blank\\\">'+e.link+'")
            print("OK: Used simpler replacement")
else:
    # Try without backslash
    if "<code style=" in html and "e.link" in html:
        print("Code tag with e.link found - different format")
        # Search for the pattern
        idx = html.find("e.link")
        before = html[max(0,idx-100):idx+50]
        print(f"  Context: {before}")

# FIX 3: Add 6/5 daily record
old_day = '"daily": [{"date":"2026-06-04"'
if old_day in html:
    new_0605 = '"daily": [{"date":"2026-06-05","type":"today","progress":[{"text":"看板v3迭代：修复筛选联动、文件超链接、新增14篇论文专利索引","dot":"done","dim":"TCC+iNEST"},{"text":"Meta-Topology SDI-Bond论文v3修订完成","dot":"done","dim":"TCC"},{"text":"CST Theory V26修订版定稿","dot":"done","dim":"TCC"},{"text":"SDI v30多区域拓扑仿真参数调优","dot":"ongoing","dim":"TCC"},{"text":"连接组数据下载管线搭建","dot":"ongoing","dim":"iNEST"}],"plan":[{"text":"SDI v30多区域跨尺度耦合验证","dot":"plan","dim":"TCC"},{"text":"FEP-STDP收敛性证明完成并写入专利","dot":"plan","dim":"iNEST"},{"text":"iNEST核心架构论文Results撰写","dot":"plan","dim":"iNEST"}]},{"date":"2026-06-04"'
    html = html.replace(old_day, new_0605)
    print("OK: Added 6/5 daily record")
else:
    # Try with different format
    if '"2026-06-04"' in html:
        print("Found 6/4 date reference")
    else:
        print("WARNING: 6/4 not found in expected format")

with open(fpath, "w", encoding="utf-8") as f:
    f.write(html)
print("After:", len(html))
print("Done!")
