import os

base = r"D:\Obsidian\home\work\.openclaw\workspace"
mono_dir = os.path.join(base, "专著")
os.makedirs(mono_dir, exist_ok=True)

monographs = [
    {"title": "网络时空协同复杂度涌现智能（iNEST）专著",
     "dim": "iNEST", "ver": "v2.5", "date": "2026-02-26", "status": "持续撰写",
     "priority": "高", "desc": "iNEST核心专著：基于网络时空协同复杂度的智能涌现统一理论。含前4章完整版+封面。最新版本：iNEST理论（专著）.pdf 6889KB。待确定最终题目与章节结构。",
     "src": r"D:\inest\专著\iNEST\iNEST理论（专著）.pdf",
     "chapter": "4章已完成", "target": "2026 Q3 完成全稿"},
    
    {"title": "iMESO理论：介观尺度智能涌现",
     "dim": "iNEST", "ver": "v1.0", "date": "2025-12-25", "status": "撰写中",
     "priority": "高", "desc": "介观尺度智能涌现理论专著。已完成1-4章、第5章、第8章、附录。含iNEST理论与iMESO工程实现全文。需确定与iNEST专著的关系与合并策略。",
     "src": r"D:\inest\专著\iMESO\iNEST理论与iMESO工程实现（全文）.docx",
     "chapter": "1-4章+5章+8章+附录", "target": "2026 Q2 确定合并/独立策略"},
    
    {"title": "晶上大脑：晶圆级类脑计算架构",
     "dim": "TCC", "ver": "v1.0", "date": "2025-11-01", "status": "规划中",
     "priority": "高", "desc": "晶上大脑专著：晶圆级集成平台上的类脑计算架构设计。含工程文件版本1559KB+1853KB。需与海河V8 SDI仿真验证数据整合，确定技术路线与章节。",
     "src": r"D:\inest\专著\晶上大脑.pdf",
     "chapter": "初稿+工程文件", "target": "2026 Q3 与SDI仿真整合后重启"},

    {"title": "基于时空协同复杂度的智能涌现统一理论",
     "dim": "TCC", "ver": "v1.0", "date": "2025-10-29", "status": "规划中",
     "priority": "高", "desc": "智能涌现统一理论专著（932KB）。从时空协同复杂度视角构建统一的智能涌现框架。需与CST理论（From Compute to Complexity）和Meta-Topology论文协调推进。",
     "src": r"D:\inest\专著\基于时空协同复杂度的智能涌现统一理论.pdf",
     "chapter": "初稿", "target": "2026 Q4 与CST论文同步推进"},

    {"title": "物理神经网络涌现智能",
     "dim": "iNEST", "ver": "v1.5", "date": "2025-11-12", "status": "撰写中",
     "priority": "高", "desc": "物理神经网络涌现智能专著（3238KB PDF + 387KB DOCX）。从物理第一性原理出发，阐述神经网络中智能涌现的机制。与FEP-STDP论文互为支撑。",
     "src": r"D:\inest\专著\物理神经网络涌现智能.pdf",
     "chapter": "PDF+DOCX双版本", "target": "2026 Q3 与FEP-STDP论文整合"},

    {"title": "类脑智能的介观尺度复杂度阈值范式",
     "dim": "iNEST", "ver": "v1.0", "date": "2025-10-05", "status": "规划中",
     "priority": "中", "desc": "类脑智能专著：介观尺度复杂度阈值范式（6852KB+3631KB双版本）。提出介观尺度作为类脑计算的关键尺度，复杂度阈值作为智能涌现的判断标准。",
     "src": r"D:\inest\专著\类脑智能：介观尺度复杂度阈值范式.pdf",
     "chapter": "初稿", "target": "2026 Q4 重启"},

    {"title": "iNEST理论迭代过程优化研究",
     "dim": "iNEST", "ver": "v1.0", "date": "2026-01-26", "status": "已规划",
     "priority": "中", "desc": "基于临界性科学的智能涌现框架迭代优化。已完成全部6步研究：理论基础梳理、权威资料整合、迭代机制优化、数学框架完善、自洽性检验、完整理论文档输出。含SCT_Main_Paper_Final等支撑材料。",
     "src": r"D:\inest\专著\iNEST\迭代\iNEST_Iteration_Research_Plan.md",
     "chapter": "全部完成", "target": "成果已整合入专著"},

    {"title": "iNEST十年规划",
     "dim": "iNEST", "ver": "v1.0", "date": "2026-01-06", "status": "已规划",
     "priority": "中", "desc": "iNEST十年发展路线图（31KB DOCX）。规划从理论验证、芯片流片、系统集成到产业落地的完整路径。",
     "src": r"D:\inest\专著\iNEST\iNEST十年规划.docx",
     "chapter": "路线图初稿", "target": "年度更新"},
]

# Create .md index files for each monograph
for m in monographs:
    safe = m["title"].replace("/", "-").replace(":", "-").replace("?", "").replace("*", "").replace('"', "").replace("|", "-").replace("\\", "-")
    if len(safe) > 80:
        safe = safe[:80]
    fname = safe + ".md"
    fpath = os.path.join(mono_dir, fname)
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write('title: "' + m["title"] + '"\n')
        f.write("dimension: " + m["dim"] + "\n")
        f.write("category: 专著\n")
        f.write("version: " + m["ver"] + "\n")
        f.write("date: " + m["date"] + "\n")
        f.write("status: " + m["status"] + "\n")
        f.write("priority: " + m["priority"] + "\n")
        f.write("chapters: " + m.get("chapter", "") + "\n")
        f.write("target: " + m.get("target", "") + "\n")
        f.write('source: "' + m["src"] + '"\n')
        f.write("---\n\n")
        f.write("# " + m["title"] + "\n\n")
        f.write("| 属性 | 值 |\n")
        f.write("|------|-----|\n")
        f.write("| 维度 | " + m["dim"] + " |\n")
        f.write("| 版本 | " + m["ver"] + " |\n")
        f.write("| 日期 | " + m["date"] + " |\n")
        f.write("| 状态 | " + m["status"] + " |\n")
        f.write("| 优先级 | " + m["priority"] + " |\n")
        f.write("| 章节进度 | " + m.get("chapter", "") + " |\n")
        f.write("| 目标 | " + m.get("target", "") + " |\n")
        f.write("| 源文件 | `" + m["src"] + "` |\n\n")
        f.write("## 描述\n\n")
        f.write(m["desc"] + "\n\n")
        f.write("---\n\n")
        f.write("> 由研发看板自动索引，遵循 Obsidian Wiki/LLM 知识管理规则。\n")
    
    print("Created: 专著/" + fname)

print("\nTotal: " + str(len(monographs)) + " monograph files")
print("Directory: " + mono_dir)
