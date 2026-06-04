fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

# FIX 1: Modal links - make file paths clickable hyperlinks
old_code = "<code style=\\\"background:var(--surface2);padding:4px 8px;border-radius:4px;font-size:0.85em;word-break:break-all\\\">'+e.link+'</code>"
new_link = "<a href=\\\"file:///D:/Obsidian/'+e.link+'\\\" style=\\\"color:var(--tcc);text-decoration:underline;word-break:break-all\\\" target=\\\"_blank\\\">'+e.link+'</a>"

if old_code in html:
    html = html.replace(old_code, new_link)
    print("OK: Modal code replaced with clickable link")
else:
    print("Trying alternative...")
    if "<code style=" in html and "e.link" in html:
        # Find exact pattern
        import re
        matches = list(re.finditer(r"<code style=\\\"[^\\]*\\\">'\+e\.link\+'</code>", html))
        print(f"Found {len(matches)} code+e.link patterns")
        for m in matches:
            old = m.group(0)
            print(f"  Old: {old[:80]}...")
            # Replace with anchor
            href = old.replace("<code style=\\", "<a href=\\"file:///D:/Obsidian/'+e.link+'\\" style=\\")
            href = href.replace("'>'+e.link+'</code>", "'>'+e.link+'</a>")
            html = html.replace(old, href)
            print("  Replaced")
    else:
        print("No code tag with e.link found")

# FIX 2: Update daily 6/5 content to reflect today's actual work
old_0605_progress = '"progress": [{"text": "SDI v30 多区域拓扑网络（multi-region）架构设计与初始仿真"'
new_0605_progress = '"progress": [{"text": "看板v3迭代：修复筛选联动、文件超链接、新增14篇论文专利索引文件","dot":"done","dim":"TCC+iNEST"},{"text": "Meta-Topology SDI-Bond论文v3修订完成","dot":"done","dim":"TCC"},{"text": "CST Theory V26修订版定稿（From Compute to Complexity）","dot":"done","dim":"TCC"},{"text": "SDI v30多区域拓扑仿真参数调优中","dot":"ongoing","dim":"TCC"},{"text": "连接组数据下载管线搭建（CONNECTOME_DOWNLOAD_TASK）","dot":"ongoing","dim":"iNEST"},{"text": "SDI v30 多区域拓扑网络（multi-region）架构设计与初始仿真"'

if old_0605_progress in html:
    html = html.replace(old_0605_progress, new_0605_progress)
    print("OK: Updated 6/5 progress")
else:
    print("6/5 progress pattern not found")

# Also update 6/5 plan
old_0605_plan = '"plan": [{"text": "SDI v30 多区域跨尺度耦合验证实验"'
new_0605_plan = '"plan": [{"text": "SDI v30多区域跨尺度耦合验证","dot":"plan","dim":"TCC"},{"text": "FEP-STDP收敛性数学证明完成并写入专利","dot":"plan","dim":"iNEST"},{"text": "iNEST核心架构论文Results章节撰写","dot":"plan","dim":"iNEST"},{"text": "SDI v30 多区域跨尺度耦合验证实验"'
if old_0605_plan in html:
    html = html.replace(old_0605_plan, new_0605_plan)
    print("OK: Updated 6/5 plan")
else:
    print("6/5 plan pattern not found")

with open(fpath, "w", encoding="utf-8") as f:
    f.write(html)
print("Done! Size:", len(html))
