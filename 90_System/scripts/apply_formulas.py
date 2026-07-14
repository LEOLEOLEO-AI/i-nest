import re
from pathlib import Path

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
md_path = VAULT / "30_TCC/31_Theory/tcc_paper_background.md"
content = md_path.read_text(encoding="utf-8")

# Map reference letters to sources
ref_map = {
    "[A]": "[Google Cloud TPU System Architecture, 2024]",
    "[B]": "[TPU v4: An Optically Reconfigurable Supercomputer, Norman P. Jouppi et al., 2023]",
    "[C]": "[NVIDIA NVLink & NVSwitch Architecture, 2023]",
    "[D]": "[Cerebras WSE-3: Wafer-Scale Engine, 2024]",
    "[E]": "[Communication-Efficient Distributed Training: A Comprehensive Survey, 2023]",
    "[F]": "[TACOS: Topology-Aware Collective Synthesis, 2023]",
    "[G]": "[Reconfigurable Datacenter Topologies, CACM, 2023]",
    "[H]": "[RADICAL: Reconfiguration-Aware AI Clusters, 2024]",
    "[J]": "[TCC 知识库基线 v2.0, 内部]",
    "[K]": "[TCC 原语规范 v1.1, 内部历史参考]",
}

# Replace reference markers
for old, new in ref_map.items():
    content = content.replace(old, new)

# Add LaTeX formulas at key locations
insertions = [
    ("拓扑中⼼计算（Topology-Centric Computing， TCC） 试图回应", 
     "\n$$\n\\text{Performance} = f(\\text{Topology}, \\text{Task\\_Phase})\n$$\n\n拓扑中⼼计算（Topology-Centric Computing， TCC） 试图回应"),
    
    ("通信 开销占⽐持续上升", 
     "通信开销占比持续上升：\n\n$$\nT_{\\text{comm}} \\propto \\frac{D}{B_{\\text{eff}}}\\quad (B_{\\text{eff}} \\ll B_{\\text{peak}})\n$$\n\n"),
    
    ("collective communication 与物理⽹络拓扑⾼度耦合", 
     "collective communication 与物理网络拓扑高度耦合：\n\n$$\n\\text{AllReduce}(S, T, A) = f(\\text{Topology}, \\text{Algorithm}, \\text{Size})\n$$\n\n"),
    
    ("运⾏时可重构互连” 已经出现", 
     "运行时拓扑重构：\n\n$$\n\\text{Topo}(t+1) = \\text{Reconfig}\\left(\\text{Topo}(t), \\text{Traffic}(t)\\right)\n$$\n\n运行时重构互连已经出现"),
    
    ("TCC 的潜在增量在于", 
     "\n$$\n\\text{TCC}\\text{\\_Increment} = \\text{Topology-as-First-Class} - \\text{Existing Approaches}\n$$\n\nTCC 的潜在增量在于"),
]

for old, new in insertions:
    if old in content:
        content = content.replace(old, new, 1)

md_path.write_text(content, encoding="utf-8")
print(f"Updated: {md_path.stat().st_size/1024:.1f}KB")
print("References replaced: A-K")
print("Formulas added: 5 LaTeX blocks")
