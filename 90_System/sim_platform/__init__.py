# -*- coding: utf-8 -*-
"""sim_platform — 复杂网络涌现智能的仿真与验证平台。

对应工作流 SIM（复杂网络涌现智能仿真，含秀丽线虫等生物连接组的交叉仿真）。

设计目标（每一条都对应一个实测到的问题）:
  1. **跨物种交叉仿真** —— species.py 把 C. elegans / hemibrain / macaque 等
     统一成同一个 (adj, meta) 契约，"同一套分析跑在多个连接组上"才成为可能。
  2. **可复现** —— harness.run() 每次落 run_manifest.json：种子、配置哈希、
     依赖版本、git 提交、结果哈希。任何结论可追溯、可重跑。
  3. **治理版本蔓延** —— 实测同一实验有 24 个 v2…v19 并存；
     harness 用"一个实验一个规范脚本"的注册表取代它，并提供 lint 体检。
  4. **证据等级 [仿真]** —— 所有产物显式标注，避免仿真观测被当成实测结论。

入口:
    python -m sim_platform.run check          平台自检（数据/依赖/注册表）
    python -m sim_platform.run species        各物种连接组可用性
    python -m sim_platform.run lint           版本蔓延体检
    python -m sim_platform.run list           已登记实验
    python -m sim_platform.run run <exp_id>   跑实验
"""

__version__ = "1.0.0"
