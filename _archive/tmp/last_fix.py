fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

# Update 6/5 daily progress to reflect today's actual work
old_0605 = '看板迭代：修正TCC/iNEST命名体系，修复交互Bug'
new_0605 = '看板v3完成：14篇论文专利文件按Obsidian知识库规则归档至papers/TCC、papers/iNEST、TCC_3_专利撰写等目录'
if old_0605 in html:
    html = html.replace(old_0605, new_0605)
    print("Updated 6/5 daily text")
else:
    print("Old text not found")

# Also add additional 6/5 items
old_sdi = '"text": "SDI v30 多区域拓扑网络（multi-region）架构设计与初始仿真"'
new_sdi = '"text": "Meta-Topology SDI-Bond论文v3修订完成","dot":"done","dim":"TCC"},{"text": "CST Theory V26定稿","dot":"done","dim":"TCC"},{"text": "SDI v30 多区域拓扑网络（multi-region）架构设计与初始仿真"'
if old_sdi in html:
    html = html.replace(old_sdi, new_sdi)
    print("Added extra 6/5 progress items")
else:
    print("SDI text not found")

# Check new entries
count_48 = html.count('"id":48')
count_53 = html.count('"id":53')
print(f"New entries: id:48={count_48}, id:53={count_53}")

with open(fpath, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Final size: {len(html)}")
