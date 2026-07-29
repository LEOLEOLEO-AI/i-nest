#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vault Health Repair v1.0 -- Fix broken links, populate MOCs, handle duplicates."""

import sys, re, json, hashlib, shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

sys.path.insert(0, r"D:\Obsidian\scripts")

VAULT = Path(r"D:\Obsidian\vault")
TODAY = datetime.now().strftime("%Y-%m-%d")

EXCLUDE = [
    ".obsidian", ".claude", ".claudian", ".trash", ".venv",
    ".neural_db", ".neural_memory", ".openclaw", ".tasks",
    "__pycache__", "node_modules", "scripts", "state",
    "99_Attachments", "99_Templates", "99_Journal",
    "collective_comm_naas", "fpga", "knowledge_graph",
    "results", "dashboard", "_archive", "_archive_02_Zettelkasten",
    "logs", "90_System"
]

# MOC page templates
MOC_TEMPLATES = {
    "30_TCC/TCC_Master_Index.md": """---
title: "TCC 拓扑中心计算 — 主索引"
date: {date}
type: MOC
tags: [TCC, MOC, index]
---

# TCC 拓扑中心计算 — 主索引

## 目录
- [31_Theory](31_Theory/) — 理论框架
- [32_Tech](32_Tech/) — 技术方案
- [34_Projects](34_Projects/) — 项目申报与策划
""",

    "40_iNEST/iNEST_Master_Index.md": """---
title: "iNEST 智能涌现系统 — 主索引"
date: {date}
type: MOC
tags: [iNEST, MOC, index]
---

# iNEST 智能涌现系统 — 主索引

## 目录
- [41_Theory](41_Theory/) — 理论框架
- [42_Tech](42_Tech/) — 技术方案
- [44_Projects](44_Projects/) — 项目申报与策划
""",

    "00_MOC/TCC-MOC.md": """---
title: "TCC — 全景导航 (Map of Content)"
date: {date}
type: MOC
tags: [TCC, MOC]
---

# TCC 拓扑中心计算 — 全景导航

> 拓扑中心计算范式：Chiplet互连、NoC、晶圆级集成

## 核心概念
- [[30_TCC/TCC_Master_Index|TCC 主索引]]
- [[iNEST_Academic_Belief_Core|学术信仰]]
- [[SDI — 软件定义互连（Software-Defined Interconnect）|SDI 技术]]

## 活跃论文
- P-Paradigm: 拓扑中心计算范式
- P-Mapping: 物理拓扑映射
- B0-Engineering: 基线工程版
""",

    "30_TCC/TCC 计算范式 — 全景导航 (Map of Content).md": """---
title: "TCC 计算范式 — 全景导航"
date: {date}
type: MOC
tags: [TCC, MOC, navigation]
---

# TCC 计算范式 — 全景导航

## 理论根基
- CST 智能涌现定理
- Route = Transform 等价原理
- 液态拓扑计算架构

## 工程路线
- SDI 软件定义互连
- 晶圆级集成 (Wafer-Scale)
- Chiplet 互连体系
""",

    "10_Library/Paper_Library.md": """---
title: "论文库 — 主索引"
date: {date}
type: MOC
tags: [papers, library, index]
---

# 论文库 — 主索引

## 分类
- [Papers](Papers/) — 学术论文笔记
- [Articles](Articles/) — 文章与简报
- [Web-Clips](Web-Clips/) — 网页剪藏
""",

    "20_Ideas/Idea_Garden.md": """---
title: "灵感花园 — 主索引"
date: {date}
type: MOC
tags: [ideas, index]
---

# 灵感花园 — 主索引

## 子目录
- [Fleeting](Fleeting/) — 闪念笔记
- [Insights](Insights/) — 深度洞察
- [Concepts](Concepts/) — 概念卡片
""",

    "40_iNEST/iNEST 论文总清单（唯一主文件）.md": """---
title: "iNEST 论文总清单"
date: {date}
type: index
tags: [iNEST, papers, index]
---

# iNEST 论文总清单

## 活跃论文
- CST-Emergence: CST 智能涌现 (V25 FINAL)
- iNEST-Core: iNEST 核心架构 (framework)
- Liquid-Computing: 液态计算化学 (framework)

## 相关条目
- [[TCC计算范式/01_论文/iNEST_项目布局与论文计划总清单|TCC 论文计划]]
""",

    "40_iNEST/iNEST_2_论文撰写.md": """---
title: "iNEST 论文撰写 — 工作区"
date: {date}
type: workspace
tags: [iNEST, papers, writing]
---

# iNEST 论文撰写 — 工作区

## 当前任务
- CST-Emergence V25 终稿
- iNEST-Core 框架完善
- Liquid-Computing 理论推导
""",

    "30_TCC/32_Tech/SDI — 软件定义互连（Software-Defined Interconnect）.md": """---
title: "SDI — 软件定义互连"
date: {date}
type: concept
tags: [TCC, SDI, interconnect]
---

# SDI — 软件定义互连（Software-Defined Interconnect）

> iNEST 课题组核心利剑技术

## 定义
软件定义互连（SDI）是在晶圆尺度赋予硅基网络"液态重构"与"时空演化"能力的独特架构创新。

## 相关
- [[SDI化合物键_四型架构]]
- [[iNEST_Academic_Belief_Core|学术信仰：SDI 为本]]
""",

    "30_TCC/32_Tech/SDI化合物键_四型架构.md": """---
title: "SDI 化合物键 — 四型架构"
date: {date}
type: concept
tags: [TCC, SDI, architecture]
---

# SDI 化合物键 — 四型架构

> SDI 互连的四种基本键型

## 四型
1. 刚性键 (Rigid Bond)
2. 柔性键 (Flexible Bond)
3. 可重构键 (Reconfigurable Bond)
4. 自适应键 (Adaptive Bond)
""",
}

# Top missing stubs to create
TOP_STUBS = {
    "iNEST": {
        "path": "40_iNEST/iNEST.md",
        "content": """---
title: "iNEST — 智能涌现系统"
date: {date}
type: concept
tags: [iNEST, emergence, neuromorphic]
---

# iNEST — intelligent Neural Emergence SysTems

> 智能神经涌现系统：基于自组织临界机制的硅基智能涌现

## 核心
- [[iNEST_Academic_Belief_Core|学术信仰：大道至简]]
- [[40_iNEST/iNEST_Master_Index|iNEST 主索引]]
- CST 智能涌现定理
"""
    },
    "FPGA原型": {
        "path": "30_TCC/32_Tech/FPGA原型.md",
        "content": """---
title: "FPGA 原型验证平台"
date: {date}
type: concept
tags: [TCC, FPGA, prototype, verification]
---

# FPGA 原型验证平台

> TCC/iNEST 硬件原型验证

## 用途
- SDI 柔性互连原型验证
- 神经形态加速器 FPGA 实现
- 低功耗边缘 AI 原型

## 相关
- [[30_TCC/TCC_Master_Index|TCC 主索引]]
"""
    },
    "自组织临界态SOC": {
        "path": "40_iNEST/41_Theory/自组织临界态SOC.md",
        "content": """---
title: "自组织临界态 (SOC)"
date: {date}
type: concept
tags: [iNEST, SOC, criticality, emergence]
---

# 自组织临界态 (Self-Organized Criticality)

> iNEST 学术信仰的核心物理机制

## 定义
系统在无外部调参的情况下，自发演化至临界态，在临界点附近表现出幂律分布的雪崩动力学。

## 关键指标
- 雪崩规模分布: P(S) ~ S^(-tau)
- tau ~ 1.5 (临界指数)
- 动态范围极大化

## 相关
- [[iNEST_Academic_Belief_Core|学术信仰]]
- [[CST理论]]
"""
    },
    "神经网络": {
        "path": "03_Topics/AI-ML/神经网络.md",
        "content": """---
title: "神经网络"
date: {date}
type: concept
tags: [AI, neural-network, concept]
---

# 神经网络

## 分类
- 脉冲神经网络 (SNN)
- 人工神经网络 (ANN)
- 储备池计算 (Reservoir Computing)

## 相关
- [[自组织临界态SOC]]
- [[神经形态计算]]
"""
    },
    "神经形态计算": {
        "path": "03_Topics/AI-ML/神经形态计算.md",
        "content": """---
title: "神经形态计算"
date: {date}
type: concept
tags: [neuromorphic, SNN, computing]
---

# 神经形态计算

> 基于生物神经系统原理的计算范式

## 关键要素
- 脉冲驱动
- 事件驱动
- 存算一体
- 异步并行

## 相关
- [[自组织临界态SOC]]
- [[iNEST]]
"""
    },
    "ANN动力学": {
        "path": "03_Topics/AI-ML/ANN动力学.md",
        "content": """---
title: "ANN 动力学"
date: {date}
type: concept
tags: [ANN, dynamics, neural-network]
---

# ANN 动力学

> 人工神经网络的动态行为分析

## 研究维度
- 相变与临界行为
- 混沌边缘
- 信息传播动力学
"""
    },
    "CST理论": {
        "path": "30_TCC/31_Theory/CST理论.md",
        "content": """---
title: "CST 智能涌现理论"
date: {date}
type: concept
tags: [TCC, CST, theory, emergence]
---

# CST 智能涌现理论

> Complexity-Structure-Time 定理：定量化智能涌现的物理条件

## 核心公式
CST = (Sc * Tc) * exp(alpha * Gamma_st)

## 五条公理
1. 有界性
2. 单调性
3. 耦合放大
4. 器件决定 alpha
5. 测量不变性

## 相关
- [[iNEST_Academic_Belief_Core|学术信仰]]
- [[自组织临界态SOC]]
"""
    },
    "Google Scholar": {
        "path": "00_MOC/Google_Scholar.md",
        "content": """---
title: "Google Scholar — 检索记录"
date: {date}
type: reference
tags: [search, literature]
---

# Google Scholar 检索记录

> 学术文献检索入口与记录
"""
    },
    "DOI": {
        "path": "00_MOC/DOI.md",
        "content": """---
title: "DOI 索引"
date: {date}
type: reference
tags: [DOI, reference, index]
---

# DOI 索引

> 论文 DOI 快速查找
"""
    },
    "PubMed": {
        "path": "00_MOC/PubMed.md",
        "content": """---
title: "PubMed — 检索记录"
date: {date}
type: reference
tags: [PubMed, literature, search]
---

# PubMed 检索记录

> 生物医学文献检索入口
"""
    },
}


def populate_mocs():
    """Fill empty MOC/index pages with proper content."""
    print("[1] Populating empty MOC/index pages...")
    count = 0
    for rel_path, template in MOC_TEMPLATES.items():
        target = VAULT / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.stat().st_size > 60:
            print(f"  SKIP (already populated): {rel_path}")
            continue
        content = template.format(date=TODAY)
        target.write_text(content.strip() + "\n", encoding="utf-8")
        print(f"  OK: {rel_path}")
        count += 1
    print(f"  {count} MOC pages populated\n")
    return count


def create_stubs():
    """Create stub pages for top missing link targets."""
    print("[2] Creating stub pages for top missing targets...")
    count = 0
    for name, info in TOP_STUBS.items():
        target = VAULT / info["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.stat().st_size > 60:
            print(f"  SKIP (exists): {info['path']}")
            continue
        content = info["content"].format(date=TODAY)
        target.write_text(content.strip() + "\n", encoding="utf-8")
        print(f"  OK: {info['path']}")
        count += 1
    print(f"  {count} stubs created\n")
    return count


def cleanup_tiny():
    """Clean up remaining tiny notes (<60 chars, not MOCs)."""
    print("[3] Cleaning tiny notes...")
    count = 0
    for md in VAULT.rglob("*.md"):
        rel = str(md.relative_to(VAULT))
        parts = Path(rel).parts
        if any(p in EXCLUDE or p.startswith(".") for p in parts):
            continue
        try:
            if md.stat().st_size < 60:
                # Skip if it"s in MOC_TEMPLATES (already handled)
                if rel in MOC_TEMPLATES:
                    continue
                # Move to _archive/tiny_cleanup
                archive_dir = VAULT / "_archive" / "tiny_cleanup" / str(Path(rel).parent)
                archive_dir.mkdir(parents=True, exist_ok=True)
                dest = archive_dir / md.name
                shutil.move(str(md), str(dest))
                print(f"  ARCHIVED: {rel}")
                count += 1
        except Exception as e:
            print(f"  ERROR: {rel} - {e}")
    print(f"  {count} tiny notes archived\n")
    return count


def handle_duplicates():
    """Identify and tag duplicate groups."""
    print("[4] Handling duplicates...")
    hashes = defaultdict(list)
    for md in VAULT.rglob("*.md"):
        rel = str(md.relative_to(VAULT))
        parts = Path(rel).parts
        if any(p in EXCLUDE or p.startswith(".") for p in parts):
            continue
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")
            h = hashlib.md5(text[:2000].encode()).hexdigest()
            hashes[h].append({"rel": rel, "path": md, "size": len(text)})
        except:
            pass

    dups = {k: v for k, v in hashes.items() if len(v) > 1}
    print(f"  Found {len(dups)} duplicate groups")

    # Strategy: for each group, keep the one in the most appropriate location,
    # archive the rest
    archive_count = 0
    for h, group in dups.items():
        # Sort: prefer shorter path (closer to root), then larger size
        group.sort(key=lambda x: (len(x["rel"].split("/")), -x["size"]))
        keeper = group[0]

        for dup in group[1:]:
            archive_dir = VAULT / "_archive" / "dedup" / str(Path(dup["rel"]).parent)
            archive_dir.mkdir(parents=True, exist_ok=True)
            dest = archive_dir / Path(dup["rel"]).name
            try:
                shutil.move(str(dup["path"]), str(dest))
                archive_count += 1
            except Exception as e:
                print(f"  ERROR moving {dup['rel']}: {e}")

    print(f"  {archive_count} duplicates archived\n")
    return archive_count


def link_orphans():
    """Add minimal links to orphan notes in Inbox."""
    print("[5] Linking orphans...")
    count = 0

    # Build file map
    all_names = set()
    for md in VAULT.rglob("*.md"):
        rel = str(md.relative_to(VAULT))
        parts = Path(rel).parts
        if any(p in EXCLUDE or p.startswith(".") for p in parts):
            continue
        all_names.add(md.stem)

    for md in VAULT.rglob("*.md"):
        rel = str(md.relative_to(VAULT))
        parts = Path(rel).parts
        if any(p in EXCLUDE or p.startswith(".") for p in parts):
            continue
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")
            links = re.findall(r"\[\[([^\]|#]+)", text)

            # Check if it has frontmatter
            has_frontmatter = text.strip().startswith("---")

            if len(links) == 0 and md.stat().st_size > 60:
                # Determine parent MOC
                parent = parts[0] if parts else "root"
                moc_map = {
                    "30_TCC": "TCC_Master_Index",
                    "40_iNEST": "iNEST_Master_Index",
                    "00_Inbox": "00_MOC",
                    "10_Library": "Paper_Library",
                    "20_Ideas": "Idea_Garden",
                }

                # Only handle Inbox orphans (non-Inbox might be intentional)
                if parent in ["00_Inbox"] and not has_frontmatter:
                    # Add frontmatter with backlink
                    header = f"""---
date: {datetime.fromtimestamp(md.stat().st_mtime).strftime('%Y-%m-%d')}
type: inbox-note
tags: [inbox, needs-review]
related: [[{moc_map.get(parent, 'Home')}]]
---

"""
                    new_text = header + text
                    md.write_text(new_text, encoding="utf-8")
                    count += 1
        except Exception as e:
            pass

    print(f"  {count} orphans linked\n")
    return count


def main():
    print("=" * 60)
    print("  Vault Health Repair v1.0")
    print("=" * 60)
    print()

    mocs = populate_mocs()
    stubs = create_stubs()
    tiny = cleanup_tiny()
    dups = handle_duplicates()
    orphans = link_orphans()

    print("=" * 60)
    print(f"  Summary: {mocs} MOCs + {stubs} stubs + {tiny} tiny cleaned")
    print(f"           {dups} duplicates archived + {orphans} orphans linked")
    print("=" * 60)


if __name__ == "__main__":
    main()