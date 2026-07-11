# -*- coding: utf-8 -*-
"""Obsidian Vault 全面诊断脚本 — Karpathy Wiki LLM v2.0 结构优化"""

import os, json, re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
TARGET_STRUCTURE = {
    "10_Inbox": "剪藏入口",
    "20_Processing": "内容加工",
    "30_TCC": "TCC拓扑中心计算",
    "40_iNEST": "iNEST神经形态",
    "50_Output": "产出",
    "60_MOC": "全景导航",
    "90_System": "系统脚本",
    "99_Archive": "归档",
    "99_Meta": "元数据",
    "dashboard": "研发看板",
}

KNOWN_LEGACY = {
    "00_KnowledgeBase_知识库": "旧知识库",
    "00_Inbox": "旧Inbox",
    "01_Concepts": "旧概念",
    "02_Papers": "旧论文",
    "02_Papers_论文": "旧论文2",
    "03_Projects": "旧项目",
    "05_Fleeting": "临时笔记",
    "10_Knowledge": "旧知识",
    "20_Projects": "旧项目2",
    "30_Outputs": "旧产出",
    "Inbox": "旧收件箱",
    "Journal": "旧日记",
    "KB": "知识库碎片",
    "knowledge": "知识碎片",
    "knowledge_graph": "知识图谱",
    "MEMORY": "记忆碎片",
    "NCC_IP_Portfolio": "旧IP投资组合",
    "Projects": "项目碎片",
    "research": "研究碎片",
    "ResearchTools": "研究工具",
    "results": "结果碎片",
    "sdi_paper": "SDI论文",
    "sdi_sim": "SDI仿真",
    "scripts": "旧脚本",
    "skills": "技能碎片",
    "state": "状态文件",
    "TCC计算范式": "旧TCC",
    "智能涌现范式": "旧涌现",
    "灵感库": "旧灵感",
    "upload": "上传临时",
    "iNEST_HW_Engineering": "iNEST硬件工程",
    "iNEST_Sim_Research": "iNEST仿真研究",
    "novnc_overlay": "noVNC覆盖",
    "plugins": "插件碎片",
    "copilot": "Copilot对话",
    "logs": "日志",
    ".claude": "Claude配置",
    ".claudian": "Claudian配置",
    ".neural_db": "神经数据库",
    ".neural_memory": "神经记忆",
    ".obsidian": "Obsidian配置",
    ".openclaw": "OpenClaw配置",
    ".smart-env": "Smart环境",
    ".tasks": "任务",
}

def scan_vault():
    stats = {
        "total_dirs": 0,
        "total_md_files": 0,
        "total_size": 0,
        "empty_files": [],
        "stub_files": [],
        "duplicate_names": defaultdict(list),
        "dir_summary": {},
        "unclassified_dirs": [],
        "needs_review": [],
    }
    
    name_index = defaultdict(list)
    
    for root, dirs, files in os.walk(VAULT):
        rel = Path(root).relative_to(VAULT)
        md_files = [f for f in files if f.endswith(".md")]
        
        for f in md_files:
            fpath = Path(root) / f
            fsize = fpath.stat().st_size
            stats["total_md_files"] += 1
            stats["total_size"] += fsize
            name_index[f.lower()].append(str(fpath.relative_to(VAULT)))
            
            if fsize == 0:
                stats["empty_files"].append(str(fpath.relative_to(VAULT)))
            elif fsize < 600:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                    content = fh.read()
                word_count = len(re.findall(r"[\u4e00-\u9fff\w]+", content))
                if word_count < 10:
                    stats["stub_files"].append(str(fpath.relative_to(VAULT)))
    
    for name, paths in name_index.items():
        if len(paths) > 1:
            stats["duplicate_names"][name] = paths
    
    return stats

def analyze():
    print("=" * 60)
    print(f"Obsidian Vault 诊断报告")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Vault 路径: {VAULT}")
    print("=" * 60)
    
    stats = scan_vault()
    
    # 1. 顶层目录分析
    print("\n## 1. 顶层目录分析")
    print(f"\n共有 {len(list(VAULT.iterdir()))} 个顶层条目\n")
    
    dirs = [d for d in VAULT.iterdir() if d.is_dir()]
    
    target_matched = []
    legacy_matched = []
    unknown = []
    hidden = []
    
    for d in sorted(dirs):
        name = d.name
        if name.startswith("."):
            hidden.append(name)
        elif name in TARGET_STRUCTURE:
            target_matched.append(name)
        elif name in KNOWN_LEGACY:
            legacy_matched.append(name)
        else:
            unknown.append(name)
    
    print("### 目标结构中的目录:")
    for n in target_matched:
        md_count = sum(1 for _ in VAULT.glob(f"{n}/**/*.md"))
        print(f"  ✅ {n} — {TARGET_STRUCTURE[n]} ({md_count} md)")
    
    print("\n### 已知遗留目录 (需合并/归档):")
    for n in legacy_matched:
        md_count = sum(1 for _ in VAULT.glob(f"{n}/**/*.md"))
        print(f"  ⚠️  {n} — {KNOWN_LEGACY[n]} ({md_count} md)")
    
    print("\n### 未分类目录:")
    for n in unknown:
        md_count = sum(1 for _ in VAULT.glob(f"{n}/**/*.md"))
        print(f"  ❓ {n} ({md_count} md)")
    
    print(f"\n### 隐藏目录:")
    for n in hidden:
        print(f"  🔒 {n}")
    
    # 2. 文件统计
    print(f"\n## 2. 文件统计")
    print(f"📄 总 Markdown 文件: {stats['total_md_files']}")
    print(f"📦 总大小: {stats['total_size'] / 1024 / 1024:.1f} MB")
    print(f"🗑️  空文件 (0 bytes): {len(stats['empty_files'])}")
    print(f"📝 桩文件 (<600B, <10词): {len(stats['stub_files'])}")
    print(f"🔄 重名文件组: {len(stats['duplicate_names'])}")
    
    # 3. 空文件清单(前50)
    if stats["empty_files"]:
        print(f"\n## 3. 空文件清单 (前50/{len(stats['empty_files'])}):")
        for f in stats["empty_files"][:50]:
            print(f"  🗑️  {f}")
        if len(stats["empty_files"]) > 50:
            print(f"  ... 及另外 {len(stats['empty_files']) - 50} 个")
    
    # 4. 桩文件清单(前50)
    if stats["stub_files"]:
        print(f"\n## 4. 桩文件清单 (前50/{len(stats['stub_files'])}):")
        for f in stats["stub_files"][:50]:
            print(f"  📝 {f}")
        if len(stats["stub_files"]) > 50:
            print(f"  ... 及另外 {len(stats['stub_files']) - 50} 个")
    
    # 5. 重名文件(前30)
    if stats["duplicate_names"]:
        print(f"\n## 5. 重名文件组 (前30/{len(stats['duplicate_names'])}):")
        items = list(stats["duplicate_names"].items())
        items.sort(key=lambda x: -len(x[1]))
        for name, paths in items[:30]:
            print(f"\n  🔄 '{name}' × {len(paths)}:")
            for p in paths[:5]:
                print(f"     - {p}")
            if len(paths) > 5:
                print(f"     ... 及另外 {len(paths)-5} 个")
    
    # 6. 优化建议
    print(f"\n## 6. 优化建议")
    print(f"\n### 合并映射建议:")
    print(f"以下目录建议合并到目标结构:")
    for name in legacy_matched + unknown:
        suggested = suggest_target(name)
        if suggested:
            print(f"  {name} → {suggested}")
    
    # 7. 总体方案
    print(f"\n## 7. 总体方案")
    print(f"""
**目标结构 (Karpathy Wiki LLM v2.0):**
```
workspace/
├── 10_Inbox/          剪藏入口
│   ├── 11_GetNotes/   得到大脑
│   ├── 12_Genspark/   Genspark Claw
│   └── 13_Codex/      Codex 剪藏
├── 20_Processing/     内容加工
│   ├── 21_TCC/        
│   └── 22_iNEST/      
├── 30_TCC/            TCC 拓扑中心计算
│   ├── 31_Theory/     理论攻关
│   ├── 32_Tech/       技术研究
│   ├── 33_Dev/        工程开发
│   ├── 34_Projects/   项目策划
│   └── 35_Simulation/ 仿真实验
├── 40_iNEST/          iNEST 神经形态
│   ├── 41_Theory/     理论攻关
│   ├── 42_Tech/       技术研究
│   ├── 43_Dev/        工程开发
│   ├── 44_Projects/   项目策划
│   └── 45_Simulation/ 仿真实验
├── 50_Output/         成果产出
│   ├── 51_Papers/     论文
│   ├── 52_Patents/    专利
│   ├── 53_Monographs/ 专著
│   ├── 54_Code/       工程代码/IP
│   └── 55_Guides/     项目指南
├── 60_MOC/            全景导航
├── 90_System/         系统脚本
│   └── scripts/
├── 99_Archive/        历史归档
├── 99_Meta/           元数据/看板
└── dashboard/         研发看板前端
```

**待清理量:**
- 空文件: {len(stats['empty_files'])} 个
- 桩文件: {len(stats['stub_files'])} 个
- 重名组: {len(stats['duplicate_names'])} 组
- 遗留目录: {len(legacy_matched)} 个
- 未分类目录: {len(unknown)} 个
""")
    
    return stats

def suggest_target(dirname):
    name_lower = dirname.lower()
    if any(kw in name_lower for kw in ["paper", "论文", "papers"]):
        return "50_Output/51_Papers"
    if any(kw in name_lower for kw in ["patent", "专利", "ip"]):
        return "50_Output/52_Patents 或 40_iNEST/43_Dev"
    if any(kw in name_lower for kw in ["sim", "仿真", "simulation"]):
        return "30_TCC/35_Simulation 或 40_iNEST/45_Simulation"
    if any(kw in name_lower for kw in ["project", "项目"]):
        return "30_TCC/34_Projects 或 40_iNEST/44_Projects"
    if any(kw in name_lower for kw in ["inbox", "剪藏"]):
        return "10_Inbox"
    if any(kw in name_lower for kw in ["journal", "日记"]):
        return "99_Archive (非研究内容归档)"
    if any(kw in name_lower for kw in ["tcc", "拓扑", "中心计算"]):
        return "30_TCC"
    if any(kw in name_lower for kw in ["inest", "神经", "类脑", "涌现", "智能涌"]):
        return "40_iNEST"
    if any(kw in name_lower for kw in ["knowledge", "知识", "concept"]):
        return "60_MOC 或 20_Processing"
    if any(kw in name_lower for kw in ["script", "脚本", "system"]):
        return "90_System/scripts"
    return "99_Archive (需人工确认)"

if __name__ == "__main__":
    analyze()
