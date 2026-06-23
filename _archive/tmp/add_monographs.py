import json

fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

# Add monograph entries
# Find the closing bracket of entries array
entries_start = html.find('"entries": [')
# Find matching close bracket
depth = 0
close_pos = entries_start
for i in range(entries_start, len(html)):
    if html[i] == '[':
        depth += 1
    elif html[i] == ']':
        depth -= 1
        if depth == 0:
            close_pos = i
            break

# Find last entry before closing bracket
last_brace = html.rfind('}', entries_start, close_pos)
print(f"Insert at: {last_brace + 1}")

mono_entries = [
    {"id":54,"dim":"iNEST","cat":"项目指南策划","title":"[专著] 网络时空协同复杂度涌现智能（iNEST）","ver":"v2.5","status":"持续撰写","date":"2026-02-26","desc":"iNEST核心专著，4章已完成。待确定最终题目与章节结构，目标2026 Q3完成全稿","priority":"高","link":"专著/网络时空协同复杂度涌现智能（iNEST）专著.md"},
    {"id":55,"dim":"iNEST","cat":"项目指南策划","title":"[专著] iMESO理论：介观尺度智能涌现","ver":"v1.0","status":"撰写中","date":"2025-12-25","desc":"介观尺度智能涌现理论专著，1-4章+5+8+附录完成。需确定与iNEST专著合并策略","priority":"高","link":"专著/iMESO理论：介观尺度智能涌现.md"},
    {"id":56,"dim":"TCC","cat":"项目指南策划","title":"[专著] 晶上大脑：晶圆级类脑计算架构","ver":"v1.0","status":"规划中","date":"2025-11-01","desc":"晶圆级类脑计算架构专著。需与海河V8 SDI仿真整合后重启，目标2026 Q3","priority":"高","link":"专著/晶上大脑：晶圆级类脑计算架构.md"},
    {"id":57,"dim":"TCC","cat":"项目指南策划","title":"[专著] 基于时空协同复杂度的智能涌现统一理论","ver":"v1.0","status":"规划中","date":"2025-10-29","desc":"统一理论专著。与CST论文和Meta-Topology论文协调推进，目标2026 Q4","priority":"高","link":"专著/基于时空协同复杂度的智能涌现统一理论.md"},
    {"id":58,"dim":"iNEST","cat":"项目指南策划","title":"[专著] 物理神经网络涌现智能","ver":"v1.5","status":"撰写中","date":"2025-11-12","desc":"物理第一性原理阐述神经网络智能涌现。与FEP-STDP论文互为支撑，目标2026 Q3","priority":"高","link":"专著/物理神经网络涌现智能.md"},
    {"id":59,"dim":"iNEST","cat":"项目指南策划","title":"[专著] 类脑智能的介观尺度复杂度阈值范式","ver":"v1.0","status":"规划中","date":"2025-10-05","desc":"介观尺度复杂度阈值范式专著。提出介观尺度为类脑计算关键尺度，目标2026 Q4","priority":"中","link":"专著/类脑智能的介观尺度复杂度阈值范式.md"},
    {"id":60,"dim":"iNEST","cat":"项目指南策划","title":"[专著] iNEST理论迭代过程优化研究","ver":"v1.0","status":"已完成","date":"2026-01-26","desc":"基于临界性科学的智能涌现框架迭代优化，6步研究全部完成，成果已整合入专著","priority":"中","link":"专著/iNEST理论迭代过程优化研究.md"},
    {"id":61,"dim":"iNEST","cat":"项目指南策划","title":"[专著] iNEST十年规划","ver":"v1.0","status":"已规划","date":"2026-01-06","desc":"iNEST十年发展路线图：理论验证->芯片流片->系统集成->产业落地","priority":"中","link":"专著/iNEST十年规划.md"},
]

insert_json = ""
for me in mono_entries:
    insert_json += ",\n    " + json.dumps(me, ensure_ascii=False)

html = html[:last_brace + 1] + insert_json + html[last_brace + 1:]

# Also update daily progress to mention monograph tracking
old_daily = '连接组数据下载管线搭建（CONNECTOME_DOWNLOAD_TASK）","dot":"ongoing","dim":"iNEST"}'
new_daily = '连接组数据下载管线搭建（CONNECTOME_DOWNLOAD_TASK）","dot":"ongoing","dim":"iNEST"},{"text": "专著/白皮书体系梳理：8部专著索引归档至知识库，确定跟踪事项与推进计划","dot":"done","dim":"TCC+iNEST"}'
if old_daily in html:
    html = html.replace(old_daily, new_daily)
    print("Updated daily progress with monograph note")

with open(fpath, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Done. Size: {len(html)} bytes")
print(f"Added {len(mono_entries)} monograph entries (id:54-61)")
