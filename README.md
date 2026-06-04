# TCC × iNEST 双轨研究平台

> **TCC = 拓扑中心计算** (Topological Center Computing)  
> **iNEST = 智能涌现网络系统** (Intelligent Network Emergence Systems & Topology)  
> 中央仓库: https://gitee.com/iBrainNest/i-nest

---

## 两大研究方向

### TCC — 拓扑中心计算
以网络拓扑为中心的计算范式。研究复杂网络拓扑结构对计算效率、通信原语和智能涌现的根本性影响。

**核心命题**: 拓扑即计算 (Topology is Computation)
**关键概念**: 元拓扑、SDI化合键、集体通信原语、物理拓扑映射、中心计算
**标签**: `topology`, `center-computing`, `collective-communication`, `network-primitives`, `meta-topology`, `SDI-bond`

### iNEST — 智能涌现网络系统
物理复杂网络中的智能涌现机制。研究自组织临界态、FEP-STDP协同、超线性增益的工程实现。

**核心命题**: 网络即智能 (Network is Intelligence)
**关键概念**: 自组织临界态、FEP自由能原理、STDP脉冲时间依赖可塑性、超非线性增益、类脑计算
**标签**: `emergence`, `self-organization`, `criticality`, `FEP`, `STDP`, `neuromorphic`, `spiking`

---

## 仓库结构

```
i-nest/
├── papers/                  # 论文库
│   ├── iNEST/              # iNEST方向论文 (8篇)
│   └── TCC/                # TCC方向论文
├── iNEST_1_项目策划/        # iNEST项目策划
├── iNEST_2_论文撰写/        # iNEST论文撰写 (13篇)
├── iNEST_3_专利撰写/        # iNEST专利撰写 (7篇)
├── iNEST_4_工程开发/        # iNEST工程代码 + FPGA
├── TCC_1_项目策划/          # TCC项目策划 (海河实验室V8等)
├── TCC_2_论文撰写/          # TCC论文撰写 (CST理论V27等)
├── TCC_3_专利撰写/          # TCC专利撰写 (4篇)
├── TCC_4_工程开发/          # TCC工程架构文档
├── simulation/              # 仿真数据 (v9-v30)
├── 03_Topics/               # 主题研究
│   ├── TCC-SDI/            # TCC+SDI联合研究
│   ├── Concepts-Theory/    # 理论概念
│   └── ...
├── knowledge_graph/         # 知识图谱
├── scripts/                 # 同步脚本与工具
└── dashboard/               # 仪表盘
```

---

## 同步协议

三平台 (Obsidian / Genspark / Claw Computer) 通过 Gitee 同步：
- 触发词: **"同步gitee"**
- 策略: Pull-First → 分类提交 → Push
- 文档: `scripts/GITEE_SYNC_PROTOCOL.md`

## 版本历史
- v2 (2026-06-05): 全面清理，TCC定义修正为"拓扑中心计算"
- v1 (2026-06-03): 初始版本
