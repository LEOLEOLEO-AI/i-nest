import os

paper_dir = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\papers"
os.makedirs(paper_dir, exist_ok=True)

papers = [
    {"title": "Meta-Topology and SDI-Bond: Variational Framework for Communication Primitive Generation and Fractal Network Evolution", "ver": "v3", "date": "2026-06-04", "src": "iNEST_2_论文撰写/P-Theory_v3_Revised.md", "dim": "TCC"},
    {"title": "From Compute to Complexity: A Physical Theory of Intelligence Emergence and Its Implications for AGI", "ver": "V26", "date": "2026-06-04", "src": "TCC_2_论文撰写/A1_CST_Theory_V26_REVISED.md", "dim": "TCC"},
    {"title": "SDI Compound-Bond Self-Evolving Network Architecture", "ver": "draft-v5", "date": "2026-06-04", "src": "phase1_workspace/papers/paper1_iNEST_core_architecture.md", "dim": "iNEST"},
    {"title": "Liquid Computing Chemistry - FEP-driven Self-organization in Artificial Neural Substrates", "ver": "draft-v2", "date": "2026-06-03", "src": "phase1_workspace/papers/paper2_liquid_computing_chemistry.md", "dim": "iNEST"},
    {"title": "SDI化合物键四型架构 - 通信原语生成与分形网络演化的变分框架", "ver": "v1", "date": "2026-06-03", "src": "03_Topics/Concepts-Theory/08_SDI化合物键_四型架构.md", "dim": "TCC"},
    {"title": "STDP-FEP梯度下降统一映射 - 脉冲时间依赖可塑性与自由能原理的数学桥接", "ver": "v1", "date": "2026-06-03", "src": "03_Topics/Concepts-Theory/08_STDP-FEP梯度下降统一映射.md", "dim": "iNEST"},
    {"title": "NCL神经计算定律详解 - 零约定逻辑在拓扑中心计算中的应用", "ver": "v1", "date": "2026-06-03", "src": "03_Topics/Concepts-Theory/08_NCL神经计算定律详解.md", "dim": "TCC"},
    {"title": "自演化机制全景总结 - 最小作用量原理到物理智能", "ver": "v1", "date": "2026-06-03", "src": "03_Topics/Concepts-Theory/iNEST_自演化机制全景总结_最小作用量到物理智能.md", "dim": "iNEST"},
    {"title": "v24 FEP-STDP融合 - 双目标首次达成分析报告", "ver": "v1", "date": "2026-06-03", "src": "03_Topics/Concepts-Theory/v24_FEP-STDP融合_双目标首次达成.md", "dim": "iNEST"},
    {"title": "v28 全部关键指标物理含义与生物权威来源对照", "ver": "v1", "date": "2026-06-03", "src": "03_Topics/Concepts-Theory/v28_全部关键指标_物理含义_生物权威来源.md", "dim": "iNEST"},
    {"title": "JEPA-LNN-iNEST借鉴路径与快速验证策略", "ver": "v1", "date": "2026-06-03", "src": "03_Topics/AI-ML/JEPA-LNN-iNEST_借鉴路径与快速验证策略.md", "dim": "iNEST"},
    {"title": "海河V8 SDI仿真验证数据补充报告", "ver": "v1", "date": "2026-06-04", "src": "TCC_1_项目策划/海河V8_SDI仿真验证数据补充.md", "dim": "TCC"},
    {"title": "CONNECTOME数据下载与预处理任务说明", "ver": "v1", "date": "2026-06-04", "src": "phase1_workspace/CONNECTOME_DOWNLOAD_TASK.md", "dim": "iNEST"},
    {"title": "V29功能性涌现仿真推进计划", "ver": "v1", "date": "2026-06-03", "src": "phase1_workspace/V29_Simulation_Advancement_Plan.md", "dim": "iNEST"},
]

for p in papers:
    safe = p["title"].replace("/", "-").replace(":", "-").replace("?", "").replace("*", "").replace('"', "").replace("|", "-")
    if len(safe) > 80:
        safe = safe[:80]
    fname = safe + ".md"
    fpath = os.path.join(paper_dir, fname)
    
    content = "# " + p["title"] + "\n\n"
    content += "- 维度: " + p["dim"] + "\n"
    content += "- 版本: " + p["ver"] + "\n"
    content += "- 日期: " + p["date"] + "\n"
    content += "- 源文件: " + p["src"] + "\n\n"
    content += "---\n\n"
    content += "此文件由研发看板自动索引生成。\n"
    content += "原始内容请查看源文件。\n"
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Created: " + fname)

print("\nTotal: " + str(len(papers)) + " files in " + paper_dir)
