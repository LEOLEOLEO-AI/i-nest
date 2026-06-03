# TCC-iNEST Research Platform

> 综合技术研究、专利撰写、论文撰写和工程代码开发的综合平台

## 概述

本平台围绕 **TCC** (Trusted Computing Cloud) 和 **iNEST** (Intelligent Network Systems for Edge and Edge Computing) 两个研究方向，提供：

- **论文抓取**: 每天自动从 arXiv、IEEE、ACM、知网等源搜索最新论文
- **知识图谱**: 基于 Neo4j 的双向标签知识图谱，连接 TCC 和 iNEST 两个方向的研究
- **灵感引擎**: 基于新导入论文自动生成研究灵感，指导论文、专利和代码开发
- **看盘系统**: Web 看盘，跟踪每日进度，与 Office 协同工作
- **双向同步**: Obsidian ↔ Gitee ↔ Genspark 自动同步
- **技能管理**: Auto Research、Paper Writer、Patent Writer 等智能体技能
- **自动验证**: 确定想法后自动进行验证、仿真、开发代码

## 目录结构

`
research_platform/
├── config.json              # 平台配置
├── main.py                  # 主调度器
├── setup.py                 # 初始化脚本
├── install_skills.py        # 技能安装
├── requirements.txt         # Python 依赖
├── start.bat               # Windows 启动脚本
├── README.md               # 本文档
├── papers/                 # 抓取的论文
│   ├── TCC/               # TCC 方向论文
│   └── iNEST/             # iNEST 方向论文
├── knowledge_graph/        # 知识图谱数据
│   └── neo4j_data/
├── inspiration_engine/     # 灵感库
├── dashboard/              # Web 看盘
│   ├── index.html          # 主页面
│   └── data.json           # 数据源
├── code_generator/         # 代码生成器
│   └── projects/
├── auto_verify/            # 自动验证
├── agent_skills/           # 智能体技能
│   └── installed/
├── reports/                # 进度报告
├── scripts/                # 核心模块
│   ├── paper_scraper.py
│   ├── knowledge_graph.py
│   ├── inspiration_engine.py
│   ├── sync_manager.py
│   ├── scheduler.py
│   ├── progress_report.py
│   ├── auto_verify.py
│   ├── code_generator.py
│   └── agent_skills.py
└── logs/                   # 日志
`

## 快速开始

### 1. 安装依赖

`ash
pip install -r requirements.txt
`

### 2. 初始化平台

`ash
python setup.py
`

### 3. 配置 Gitee

编辑 config.json，设置你的 Gitee 仓库地址:

`json
"sync": {
    "gitee_repo": "https://gitee.com/your-username/research-platform.git"
}
`

### 4. 安装智能体技能

`ash
python install_skills.py
`

### 5. 启动看盘

`ash
start.bat
# 选择 7. 启动看盘
`

或直接打开: dashboard/index.html

### 6. 运行论文抓取

`ash
python main.py --paper-scrape
`

## 每日工作流

1. **09:00** - 论文自动抓取 (cron)
2. **10:00** - 灵感自动生成
3. **每小时** - 知识图谱更新
4. **每30分钟** - 数据同步
5. **18:00** - 每日进度报告

## 双向标签系统

平台使用双向标签连接 TCC 和 iNEST 两个方向:

- **TCC 标签**: trust, security, cloud, verifiable, enclave, attestation
- **iNEST 标签**: edge, networking, intelligent, distributed, topology, scale-free

每篇论文自动分类到对应方向，知识图谱中建立跨方向的连接。

## 同步机制

`
Obsidian ←→ Gitee ←→ Genspark
    ↑           ↑
    └──→ Platform Sync Manager ←──┘
`

- **Obsidian → Gitee**: Obsidian 笔记自动同步到 Gitee
- **Gitee → Obsidian**: 每次打开 Obsidian 时拉取最新版本
- **Platform → Gitee**: 平台生成的论文、灵感、报告自动推送
- **Gitee → Platform**: 平台启动时拉取最新代码和知识

## License

MIT
