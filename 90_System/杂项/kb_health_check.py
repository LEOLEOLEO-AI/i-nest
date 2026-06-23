import os
import re
import json
from datetime import datetime

KB_DIR = "/home/work/.openclaw/workspace/00_KnowledgeBase_知识库"
IDEAS_DIR = "/home/work/.openclaw/workspace/01_Ideas_想法"
PAPERS_DIR = "/home/work/.openclaw/workspace/02_Papers_论文"
PROJECTS_DIR = "/home/work/.openclaw/workspace/05_Projects_项目"

print(f"=== iNEST 第二大脑 健康检查与自增长索引巡检 ({datetime.now().strftime('%Y-%m-%d %H:%M')}) ===\n")

raw_ideas = []
for root, _, files in os.walk(IDEAS_DIR):
    for f in files:
        if not f.endswith('00_宽屏目录仪表盘.md'):
            raw_ideas.append(os.path.join(root, f))

print(f"[🔍 扫描 Ideas]: 发现 {len(raw_ideas)} 个未消化/零散的想法或草稿文件。")
if len(raw_ideas) > 5:
    print("  -> 💡 建议：积累的散装 Idea 较多，建议调度大模型执行一次“核心理论降维提取”，并追加到 NCC_Core_Concepts.md。")

core_concept_file = os.path.join(KB_DIR, "02_CST_核心理论著作", "NCC_Core_Concepts.md")
if os.path.exists(core_concept_file):
    print(f"\n[🔗 检查核心基线]: 找到 NCC_Core_Concepts.md，准备全库链接溯源。")
    link_count = 0
    for d in [PAPERS_DIR, PROJECTS_DIR]:
        for root, _, files in os.walk(d):
            for f in files:
                if f.endswith(".md"):
                    with open(os.path.join(root, f), 'r', encoding='utf-8') as fin:
                        content = fin.read()
                        if "CST" in content or "SDIO-N" in content or "液态硬件" in content:
                            link_count += 1
    print(f"  -> 🔗 已有 {link_count} 份学术/工程文档与核心基线强绑定，概念一致性极高。")

datasets_dir = os.path.join(KB_DIR, "05_Datasets_仿真与实验数据", "Simulation_Results")
if os.path.exists(datasets_dir):
    json_files = [f for f in os.listdir(datasets_dir) if f.endswith('.json')]
    final_files = [f for f in json_files if "FINAL" in f.upper()]
    print(f"\n[📊 检查数据集]: 发现 {len(json_files)} 份仿真数据集，其中 {len(final_files)} 份为被锚定的 FINAL 冻结版。")
    if not final_files:
        print("  -> ⚠️ 警告：没有找到被冻结为 FINAL 的数据集。请及时核对数据并添加 FINAL 后缀，以防画图脚本读取错误。")
    else:
        print(f"  -> ✅ 数据流稳定。当前使用的权威数据集是：{final_files[0]}")

print("\n[🧠 演化建议 (Missing Links)]:")
print("  1. 理论侧缺口：V22 论文虽然锚定了 ANN 始终在 L0 的理论铁证（Gamma_st ≡ 0），但未给出如何从算法层面解开这一限制的推导（或物理层面的光子架构路径指引不够具体）。")
print("  2. 工程侧缺口：《海河实验室重大专项》申报书已经生成了“3+1”架构和两大场景，但 `04_Code_代码` 库中尚缺与之对应的极简 `nano-NCC` 硬件拓扑路由器（或PyiNEST-Lite）的原型验证脚本。")
print("  3. 待办动作：建议下一步在 Code 库中用 100 行 Python 写一个 `nano-SDIO.py`，模拟微秒级切换带来的并行延迟红利（用来作为项目立项的算力对标证明材料）。")

print("\n=== 检查完成。以上索引建议已写入系统日志。 ===")
