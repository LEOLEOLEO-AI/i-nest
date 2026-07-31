---
title: SDI仿真平台搭建方案
date: 2026-07-04
tags: [SDI, simulation, platform, TCC, engineering, project]
status: draft
provenance: external
---

# SDI仿真平台搭建方案

> **目标**：建立模块化、可复现、支持从生物验证到工程指导的全链路 SDI 仿真平台。

---

## 一、现状盘点

### 1.1 已有代码资产

| 版本     | 文件名                              | 大小    | 功能定位                                          |
| ------ | -------------------------------- | ----- | --------------------------------------------- |
| v2-v6  | `sdi_network_v2~v6.py`           | —     | 早期探索（合成网络 → connectome 过渡）                    |
| **v8** | `sdi_network_v8.py`              | ~21KB | **生物基线**：C.elegans 真实 connectome + STDP + 化合键 |
| v22    | `sdi_v22_evolution.py`           | 26KB  | 自演化仿真                                         |
| v23    | `sdi_v23_fusion.py`              | 30KB  | FEP+STDP 融合                                   |
| v24    | `sdi_v24_fep_stdp_fusion.py`     | 31KB  | FEP-STDP 强化版                                  |
| v25    | `sdi_v25_physical_biological.py` | 33KB  | 物理-生物参数映射                                     |
| v26    | `sdi_v26_multiscale.py`          | 32KB  | C.elegans 四指标完整分析                             |
| v27    | `sdi_v27_multiscale.py`          | 31KB  | Drosophila Larval FEP-STDP                    |
| v28    | `sdi_v28_multiscale.py`          | 31KB  | 跨物种涌现规律                                       |
| FPGA   | `sdio_bond_core.v`               | —     | Verilog 化合键核心模块                               |

### 1.2 真实数据集

| 物种                    | N      | 来源               | 状态       |
| --------------------- | ------ | ---------------- | -------- |
| C.elegans             | 279    | Varshney 2011    | ✅        |
| C.elegans (Cook 2019) | 453    | Nature 2019      | ✅        |
| Drosophila Larva      | 2,952  | Winding 2023     | ✅        |
| Drosophila Hemibrain  | 21,739 | Xu 2020          | ✅        |
| Mouse Allen           | 2,992  | Allen Institute  | ✅        |
| Budapest 人脑           | 999    | Szalkai 2015     | ✅        |
| **Macaque RM**        | 91     | RM Cortex        | ✅        |
| Drosophila FlyWire    | ~130K  | Loomba 2024      | ⚠️ 过大需裁剪 |
| White 1986            | 302    | Phil Trans R Soc | ❌ 待下载    |

### 1.3 已有结果

`results/` 目录下有 v22-v28 共 **7 轮**仿真结果（含 PNG 图表）。

---

## 二、平台架构

### 2.1 总体分层

``
┌─────────────────────────────────────────────────┐
│              SDI 仿真平台 v2.0                    │
├─────────────────────────────────────────────────┤
│  Layer 4: 报告生成层                              │
│  ├─ 自动报告生成 (Markdown + PNG)                 │
│  ├─ 看板数据推送 (dashboard_data_v3.py)            │
│  └─ Genspark 项目快照                             │
├─────────────────────────────────────────────────┤
│  Layer 3: SDI工程映射层  ← 本方案重点              │
│  ├─ 拓扑生成器 (Meta-Topology + 化合键)            │
│  ├─ 信号传播仿真 (有向图 + 突触模型)               │
│  ├─ 并行任务能力测量                               │
│  └─ 规模涌现阈值扫描                               │
├─────────────────────────────────────────────────┤
│  Layer 2: 生物验证层 (已有)                        │
│  ├─ 真实 connectome 加载                          │
│  ├─ FEP-STDP 自演化                               │
│  ├─ σ/C/L/α 四指标计算                            │
│  └─ 跨物种对比分析                                 │
├─────────────────────────────────────────────────┤
│  Layer 1: 基础设施层                               │
│  ├─ 数据管理 (connectome 加载/缓存/预处理)          │
│  ├─ 仿真引擎 (NetworkX + NumPy/SciPy)              │
│  ├─ 参数配置 (YAML/JSON)                           │
│  └─ 日志与实验追踪                                  │
└─────────────────────────────────────────────────┘
``

### 2.2 目录结构

``
simulation/                        # 新建平台主目录
├── README.md                      # 平台总览
├── config/
│   ├── default.yaml               # 默认全局配置
│   ├── sdi_topology.yaml          # SDI 拓扑参数
│   └── species.yaml               # 物种数据集配置
├── core/
│   ├── __init__.py
│   ├── engine.py                  # 仿真引擎基类
│   ├── topology.py                # 拓扑生成器（WS/BA/SDI化合键）
│   ├── dynamics.py                # 信号传播动力学
│   ├── measures.py                # σ/C/L/α/CST 计算
│   └── datasets.py                # 真实数据集加载与预处理
├── experiments/
│   ├── bio/                       # Layer 2: 生物验证实验
│   │   ├── v26_celegans.py
│   │   ├── v27_larval_fep.py
│   │   └── v28_cross_species.py
│   └── sdi/                       # Layer 3: SDI 工程实验 ← 重点
│       ├── exp01_topology_scan.py  # 拓扑参数空间扫描
│       ├── exp02_signal_propagation.py  # 信号传播效率
│       ├── exp03_parallel_tasks.py     # 并行任务能力
│       ├── exp04_fault_tolerance.py    # 容错能力
│       └── exp05_scale_emergence.py    # 规模涌现阈值
├── reports/
│   ├── templates/
│   │   └── report_template.md
│   └── output/                    # 报告输出
├── results/                       # 统一结果输出（整合现有 results/）
│   ├── v26_results/
│   ├── v27_results/
│   └── v28_results/
├── data/                          # 真实数据集集中管理
│   ├── celegans/
│   ├── drosophila/
│   ├── mouse/
│   └── human/
└── fpga/                          # FPGA 硬件验证（已有 Verilog）
    └── sdio_bond_core.v
``

---

## 三、实施路线图

### Phase 0: 平台基础设施 (3-5天)

| 任务                                | 产出                    | 优先级   |
| --------------------------------- | --------------------- | ----- |
| 创建 `simulation/` 目录结构             | 框架搭建                  | 🔴 P0 |
| 实现 `datasets.py`：统一数据加载接口         | 一行加载任意物种              | 🔴 P0 |
| 实现 `measures.py`：σ/C/L/α/CST 计算   | 标准化指标输出               | 🔴 P0 |
| 实现 `engine.py`：仿真引擎基类             | 统一 run/record/save 接口 | 🔴 P0 |
| 迁移 v26-v28 代码为 `experiments/bio/` | 代码去重+模块化              | 🟡 P1 |

### Phase 1: SDI 拓扑生成器 (1-2周) ← 核心

| 任务                       | 产出              | 优先级   |
| ------------------------ | --------------- | ----- |
| `topology.py` 实现 4 种生成策略 | 策略矩阵            | 🔴 P0 |
| 化合键规则映射（元拓扑 → 边连接）       | 可配置的 bond_rules | 🔴 P0 |
| 端口约束仿真（k=8/16/32）        | 工程约束下的拓扑        | 🔴 P0 |
| 拓扑质量自动评分（σ≥4.0 检查）       | 自动验证            | 🟡 P1 |

**四种拓扑生成策略**：

| 策略          | 方法                    | 适用场景   |
| ----------- | --------------------- | ------ |
| ① 规则拓扑映射    | 环形→Mesh→Torus→超立方     | 确定性基线  |
| ② WS 小世界参数化 | 重连概率 p ∈ [0,1]        | 连续可调   |
| ③ **化合键规则** | 功能性簇 + 跨模块键合          | SDI 专有 |
| ④ 真实连接组迁移   | C.elegans → SDI N=128 | 生物启发   |

### Phase 2: SDI 功能仿真实验 (2-3周)

| 实验            | 核心问题                  | 关键指标          |
| ------------- | --------------------- | ------------- |
| **Exp1** 拓扑扫描 | 什么拓扑参数范围 σ 最优？        | σ vs 全局效率/延迟  |
| **Exp2** 信号传播 | 信息在有向 SDI 网络中如何传播？    | 传播延迟、吞吐量      |
| **Exp3** 并行任务 | 多路任务流能否并行处理？          | 功能分离度         |
| **Exp4** 容错能力 | 随机故障/针对性攻击下的退化？       | 鲁棒性曲线         |
| **Exp5** 规模涌现 | 从 N=16 到 N=1024 的质变点？ | CST(IIL) 跃迁阈值 |

### Phase 3: 报告与可视化 (1周)

- 自动生成 Markdown 报告（含图表嵌入）
- 「超线性增益」证据链汇总
- SDI 工程设计参数推荐表

---

## 四、关键设计决策

### 4.1 为什么需要模块化重构？

当前 v2-v28 的代码是**单文件演进**模式：每个版本都是完整拷贝加增量修改，导致：
- 核心逻辑（数据加载、指标计算）重复出现在 ~10 个文件中
- 修改一个指标公式需要改所有文件
- 新实验难以复用已有模块

→ 重构为 `core/` + `experiments/` 两层

### 4.2 数据原则（红线）

引用自 SDI仿真设计原则.md：
- ❌ 禁止合成网络替代真实数据
- ❌ 禁止硬编码文献参数代替实测
- ✅ 所有网络参数从真实数据集实测
- ✅ 缺失数据 → 该物种直接排除

### 4.3 仿真 vs 实测的边界

| 阶段      | 验证方式            | 数据来源               |
| ------- | --------------- | ------------------ |
| 拓扑验证    | 纯 NetworkX 计算   | 无需动力学              |
| 信号传播    | 简化为扩散/路由模型      | 可配置延迟              |
| 详细动力学   | Brian2/NEST（可选） | 仅关键场景              |
| FPGA 验证 | Verilog 仿真      | `sdio_bond_core.v` |

---

## 五、里程碑与时间线

``
Week 1-2:  Phase 0 基础设施 + Phase 1 拓扑生成器
Week 3-4:  Phase 2 Exp1-2 (拓扑扫描 + 信号传播)
Week 5-6:  Phase 2 Exp3-5 (并行任务 + 容错 + 规模涌现)
Week 7:    Phase 3 报告生成 + 设计参数推荐
Week 8:    完整仿真验证报告交付
``

| 里程碑          | 日期     | 交付物                         |
| ------------ | ------ | --------------------------- |
| M1: 平台可运行    | Week 2 | `simulation/` 目录 + v26 复现通过 |
| M2: SDI 拓扑生成 | Week 3 | 4 种策略可切换，σ≥4.0 自动验证         |
| M3: 功能仿真完成   | Week 6 | 5 个实验全部跑通                   |
| M4: 报告交付     | Week 8 | 完整仿真验证报告                    |

---

## 六、下一步行动

1. **立即**：创建 `simulation/` 目录结构
2. **本周**：实现 `core/datasets.py` + `core/measures.py`
3. **本周**：迁移 v26 为 `experiments/bio/v26_celegans.py` 验证框架可用性
4. **下周**：实现 `core/topology.py` 四种策略

> 📎 相关文档：[[40_iNEST/44_Projects/05_SDI技术路线仿真规划.md]] | [[40_iNEST/45_Simulation/reports/TCC_iNEST_仿真验证总计划.md]] | [[50_Output/54_Code/iNEST/SDI仿真设计原则.md]]
