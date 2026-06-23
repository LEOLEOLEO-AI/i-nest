fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

# FIX 1: Modal links - simple string replacement
# Find: <code style="...">'+e.link+'</code>
# Make it: <a href="file:///..."> with the link
# Just replace the closing tag and prepend the opening anchor
old_close = "'+e.link+'</code>"
new_close = "'+e.link+'</a>"
html = html.replace(old_close, new_close)

old_open = '<code style="background:var(--surface2);padding:4px 8px;border-radius:4px;font-size:0.85em;word-break:break-all">'
new_open = '<a href="file:///D:/Obsidian/'+"'"+'+e.link+'+"'"+'" style="color:var(--tcc);text-decoration:underline;word-break:break-all" target="_blank">'
html = html.replace(old_open, new_open)
print("Modal link: replaced")

# FIX 2: Update daily 6/5 progress 
old_p = '看板迭代：修正TCC/iNEST命名体系，修复交互Bug'
new_p = '看板v3：修复筛选联动、超链接、新增14篇论文专利索引文件'
html = html.replace(old_p, new_p)
print("Daily progress: " + ("updated" if old_p in html else "already updated"))

# Add new progress items to 6/5
# Insert after first progress item
marker = '{"text": "看板v3：修复筛选联动、超链接、新增14篇论文专利索引文件","dot":"done","dim":"TCC+iNEST"}'
insert = ',{"text": "Meta-Topology SDI-Bond论文v3修订完成","dot":"done","dim":"TCC"},{"text": "CST Theory V26修订版定稿","dot":"done","dim":"TCC"},{"text": "SDI v30多区域拓扑仿真参数调优中","dot":"ongoing","dim":"TCC"},{"text": "连接组数据下载管线搭建","dot":"ongoing","dim":"iNEST"}'
if marker in html:
    # Insert additional items after the marker, before the next ]
    old_segment = marker + ']'
    new_segment = marker + insert + ']'
    html = html.replace(old_segment, new_segment)
    print("Added extra progress items")
else:
    print("Marker not found for progress insertion")

with open(fpath, "w", encoding="utf-8") as f:
    f.write(html)
print("Done! Size:", len(html))
