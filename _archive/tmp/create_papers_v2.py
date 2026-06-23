import os

base = r"D:\Obsidian\home\work\.openclaw\workspace"

# Clean old dashboard/papers
old_dir = os.path.join(base, "dashboard", "papers")
for f in os.listdir(old_dir):
    os.remove(os.path.join(old_dir, f))
print("Cleaned old paper index files")

papers = [
    {"title": "From Compute to Complexity: A Physical Theory of Intelligence Emergence and Its Implications for AGI",
     "dim": "TCC", "cat": "论文", "ver": "V26", "date": "2026-06-04", "status": "撰写中", "priority": "高",
     "folder": "papers/TCC", "src": "TCC_2_论文撰写/A1_CST_Theory_V26_REVISED.md",
     "desc": "CST理论核心论文：从计算到复杂性，智能涌现的物理理论及其对AGI的启示"},
    
    {"title": "Meta-Topology and SDI-Bond: Variational Framework for Communication Primitive Generation and Fractal Network Evolution",
     "dim": "TCC", "cat": "论文", "ver": "v3", "date": "2026-06-04", "status": "撰写中", "priority": "高",
     "folder": "papers/TCC", "src": "iNEST_2_论文撰写/P-Theory_v3_Revised.md",
     "desc": "元拓扑与SDI化合物键：最小作用量原理下通信原语生成与分形网络演化的变分框架"},
    
    {"title": "5类通信-4类计算拓扑完备映射与PTM算法",
     "dim": "TCC", "cat": "论文", "ver": "v2", "date": "2026-06-03", "status": "撰写中", "priority": "高",
     "folder": "papers/TCC", "src": "iNEST_2_论文撰写/P-Theory_v2_MetaTopology_SDI_Bond_Draft.md",
     "desc": "B2核心论文：5通信加4计算原语拓扑完备映射，含FFT-AllReduce图同构定理"},
    
    {"title": "海河V8 SDI仿真验证数据补充报告",
     "dim": "TCC", "cat": "仿真程序", "ver": "v1", "date": "2026-06-04", "status": "已完成", "priority": "高",
     "folder": "TCC_1_项目策划", "src": "TCC_1_项目策划/海河V8_SDI仿真验证数据补充.md",
     "desc": "海河V8平台上的SDI仿真验证数据补充与实验报告"},
    
    {"title": "SDI Compound-Bond Self-Evolving Network: Physics-First Architecture for Intelligence Emergence",
     "dim": "iNEST", "cat": "论文", "ver": "draft-v5", "date": "2026-06-04", "status": "撰写中", "priority": "高",
     "folder": "papers/iNEST", "src": "phase1_workspace/papers/paper1_iNEST_core_architecture.md",
     "desc": "iNEST核心架构论文：物理优先的自组织智能涌现网络架构"},
    
    {"title": "Liquid Computing Chemistry: FEP-driven Self-organization in Artificial Neural Substrates",
     "dim": "iNEST", "cat": "论文", "ver": "draft-v2", "date": "2026-06-03", "status": "撰写中", "priority": "高",
     "folder": "papers/iNEST", "src": "phase1_workspace/papers/paper2_liquid_computing_chemistry.md",
     "desc": "液态计算化学：FEP驱动的人工神经基质自组织与涌现"},
    
    {"title": "FEP-STDP Deep Fusion: Physics-Grounded Self-Evolving Neural Architecture",
     "dim": "iNEST", "cat": "论文", "ver": "draft-v1", "date": "2026-06-03", "status": "撰写中", "priority": "高",
     "folder": "papers/iNEST", "src": "iNEST_4_工程开发/论文1_FEP-STDP深度融合_框架与专利清单.md",
     "desc": "FEP-STDP深度融合：面向绿色安全可扩展智能的物理自演化神经架构"},
    
    {"title": "SDI化合物键四型架构：通信原语生成与分形网络演化的变分框架",
     "dim": "TCC", "cat": "论文", "ver": "v1", "date": "2026-06-03", "status": "撰写中", "priority": "高",
     "folder": "03_Topics/Concepts-Theory", "src": "03_Topics/Concepts-Theory/08_SDI化合物键_四型架构.md",
     "desc": "四种SDI化合物键类型在通信原语生成中的应用"},
    
    {"title": "STDP-FEP梯度下降统一映射：脉冲时间依赖可塑性与自由能原理的数学桥接",
     "dim": "iNEST", "cat": "论文", "ver": "v1", "date": "2026-06-03", "status": "撰写中", "priority": "高",
     "folder": "03_Topics/Concepts-Theory", "src": "03_Topics/Concepts-Theory/08_STDP-FEP梯度下降统一映射.md",
     "desc": "建立STDP与FEP之间的严格数学对应关系"},
    
    {"title": "面向网络中心计算的软件定义互连系统架构及调度方法",
     "dim": "TCC", "cat": "专利", "ver": "申请稿-v1", "date": "2026-06-04", "status": "撰写中", "priority": "高",
     "folder": "TCC_3_专利撰写", "src": "TCC_3_专利撰写/00_专利布局总览.md",
     "desc": "P0优先级：覆盖TCC加SDI系统架构原语核和重构控制，海河实验室重大专项"},
    
    {"title": "面向晶圆级大模型推理的高维最优扇出互连拓扑结构",
     "dim": "TCC", "cat": "专利", "ver": "构思-v1", "date": "2026-06-04", "status": "规划中", "priority": "高",
     "folder": "TCC_3_专利撰写", "src": "TCC_3_专利撰写/00_专利布局总览.md",
     "desc": "P0优先级：针对晶圆级高维互连拓扑的关键卡位专利"},
    
    {"title": "面向万亿参数大模型的网内原语AI梯度归约通信加速系统",
     "dim": "TCC", "cat": "专利", "ver": "构思-v1", "date": "2026-06-04", "status": "规划中", "priority": "高",
     "folder": "TCC_3_专利撰写", "src": "TCC_3_专利撰写/00_专利布局总览.md",
     "desc": "P0优先级：针对AllReduce等集合通信的直接工程专利"},
    
    {"title": "一种基于自由能原理的自组织网络拓扑优化方法",
     "dim": "iNEST", "cat": "专利", "ver": "申请稿-v1", "date": "2026-06-03", "status": "撰写中", "priority": "高",
     "folder": "iNEST_3_专利撰写", "src": "phase1_workspace/patents/patent_portfolio_detailed.md",
     "desc": "FEP驱动的网络拓扑自适应优化方法"},
    
    {"title": "神经网络功能涌现检测与量化方法",
     "dim": "iNEST", "cat": "专利", "ver": "构思-v1", "date": "2026-06-03", "status": "规划中", "priority": "中",
     "folder": "iNEST_3_专利撰写", "src": "phase1_workspace/patents/patent_portfolio_detailed.md",
     "desc": "基于信息论与拓扑指标的神经网络功能涌现自动检测"},
]

for p in papers:
    folder = os.path.join(base, p["folder"])
    os.makedirs(folder, exist_ok=True)
    
    safe = p["title"]
    for ch in ['/', ':', '?', '*', '"', '|', '\\']:
        safe = safe.replace(ch, '-')
    if len(safe) > 90:
        safe = safe[:90]
    fname = safe + ".md"
    fpath = os.path.join(folder, fname)
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write('title: "' + p["title"] + '"\n')
        f.write("dimension: " + p["dim"] + "\n")
        f.write("category: " + p["cat"] + "\n")
        f.write("version: " + p["ver"] + "\n")
        f.write("date: " + p["date"] + "\n")
        f.write("status: " + p["status"] + "\n")
        f.write("priority: " + p["priority"] + "\n")
        f.write('source: "' + p["src"] + '"\n')
        f.write("---\n\n")
        f.write("# " + p["title"] + "\n\n")
        f.write("| 属性 | 值 |\n")
        f.write("|------|-----|\n")
        f.write("| 维度 | " + p["dim"] + " |\n")
        f.write("| 分类 | " + p["cat"] + " |\n")
        f.write("| 版本 | " + p["ver"] + " |\n")
        f.write("| 日期 | " + p["date"] + " |\n")
        f.write("| 状态 | " + p["status"] + " |\n")
        f.write("| 优先级 | " + p["priority"] + " |\n")
        f.write("| 源文件 | `" + p["src"] + "` |\n\n")
        f.write("## 描述\n\n")
        f.write(p["desc"] + "\n\n")
        f.write("---\n\n")
        f.write("> 由研发看板自动索引，遵循 Obsidian Wiki/LLM 知识管理规则。\n")
        f.write("> 原始内容请查看源文件。\n")
    
    print("Created: " + p["folder"] + "/" + fname)

print("\nTotal: " + str(len(papers)) + " files")
