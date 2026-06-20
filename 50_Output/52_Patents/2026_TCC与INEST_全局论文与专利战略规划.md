---
title: TCC与INEST：2026全局论文与专利战略规划清单
tags:
- brain
- chip
- complex-networks
- criticality
- emergence
- free-energy-principle
- large-language-model
- neural-networks
- neuron
- neuroscience
---
> **制定日期**: 2026-04-29
> **核心愿景**: 打通从“底层硬件互连拓扑（TCC）”到“顶层认知智能涌现（INEST）”的断层。将课题组的学术信仰（大道至简、拓扑即计算、时空复杂度自组织临界）转化为具备顶级学术影响力（Nature/Science子刊、CCF-A类系统结构/网络顶会）与极强工业壁垒的核心IP集群。

---

## 核心理论基座 (The Theoretical Core)
1. **拓扑中心计算 (TCC)**：计算不再以端节点（CPU/GPU）为核心，而是通过软件定义互连（SDI）将“线性代数路由操作（Route & Transform）”推向互连拓扑本身。
2. **复杂网络涌现智能 (INEST)**：智能不是硬编码的参数堆砌，而是系统在能量约束下，通过网络拓扑的空间复杂度（Spatial Complexity）与动态放电的时间复杂度（Temporal Complexity）的协同（CST），在自组织临界态（SOC）附近自然涌现的副产品。

---

## 一、 顶刊 / 顶会论文规划列表 (Paper Pipeline)

### 领域一：TCC (拓扑中心计算 & 硬件架构)

| 拟定题目 (Working Title)                                                                                                                | 核心创新点 (Key Innovation)                                                                             | 目标期刊/会议                        | 状态/依赖                              |
| :---------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- | :----------------------------- | :--------------------------------- |
| **1. Network-Centric Computing: A Paradigm Shift via Software-Defined Interconnects**<br>*(拓扑中心计算：基于SDI的第三次计算范式迁移)*                 | **范式奠基论文**：首次提出并证明大模型时代的“通信墙”需通过物理拓扑的重构来解决。将AllReduce等操作分解为网络原语，证明高复杂度网络×极简节点的相对智能指数优势。            | Nature Electronics / IEEE JSSC | 概念框架已成型 `[[SDI-CC论文框架_拓扑即计算新范式]]`  |
| **2. Optimal High-Dimensional Topology for Wafer-Scale LLM Inference: A Switch-Centric Approach**<br>*(面向晶圆级LLM推理的最优高维拓扑：一种交换中心架构)* | **晶圆级拓扑设计**：针对Wafer-Scale（如Sohu、Groq、Tesla Dojo）存在的“互连扩展墙”，提出一种无HBM情况下的高维最优扇出拓扑与路由算法，大幅提升Token生成率。 | ISCA / MICRO (CCF-A)           | 需拓扑仿真实验（Traffic Simulation）支撑      |
| **3. In-Network Binarized Neural Networks via Lookup-Table Optimization on FPGA NICs**<br>*(基于查找表优化的网内二值化神经网络)*                     | **网内计算落地**：利用FPGA SmartNIC或SDI交换机，将二值化神经网络的乘加操作转化为查找表（LUT）查表，实现极低延迟的网内AI推理加速。                      | IEEE/ACM IWQoS (已接收)           | **已达成** `近期成果展示_基于查找表优化的网内二值化神经网络` |

### 领域二：INEST (复杂网络与智能涌现)

| 拟定题目 (Working Title) | 核心创新点 (Key Innovation) | 目标期刊/会议 | 状态/依赖 |
| :--- | :--- | :--- | :--- |
| **4. A Unified Theory of Intelligence Emergence from Spatiotemporal Network Complexity (CST)**<br>*(基于时空网络复杂度的智能涌现统一理论)* | **涌现理论奠基**：用严格数学证明智能涌现等于空间复杂度与时间复杂度的非线性耦合。证明当CST越过关键物理常数（如$\pi, \delta$）时，系统发生相变并涌现出通用智能（对比LLM与生物脑）。 | Science / Nature Physics | 草稿中 `[[CST_Intelligence_Emergence_Paper_V22_Engineering_Format]]` |
| **5. Self-Organized Criticality in Wafer-Scale Spiking Neural Networks: Energy vs. Complexity**<br>*(晶圆级脉冲神经网络的自组织临界：能量与复杂度的博弈)* | **临界态工程实现**：借鉴自由能原理（FEP），在超大规模硬件（Wafer-Scale）中引入长程抑制反馈，展示系统如何自发悬停在“雪崩临界态”，实现最高的动态时空复杂度与最低功耗。 | Nature Machine Intelligence | 需结合脉冲神经网络（SNN）模拟框架跑出临界指数（幂律分布） |
| **6. Dynamic Spatiotemporal Pruning for Neuromorphic Hardware driven by Plasticity**<br>*(基于可塑性驱动的神经形态硬件动态时空剪枝)* | **算法与硬件协同**：在硬件限制下，通过模拟突触可塑性（STDP）实现网络连接的自适应生长与剪枝。证明“小世界（Small-World）”拓扑能在保持智能水平的同时极大地节约互连资源。 | HPCA / ASPLOS (CCF-A) | 需结合下载库中最新的 STDP/Pruning 论文进行理论验证 |

---

## 二、 核心专利布局清单 (Patent Portfolio)

针对大模型计算瓶颈、晶圆级互连、神经形态硬件，建立防守与进攻并重的专利池。

### 1. 架构与拓扑类 (Architecture & Topology)
- **专利1：一种支持拓扑中心计算的软件定义互连（SDI）系统架构及调度方法**
  - *核心Claim*：包含纯计算内核、通信原语核及液态重构控制器，在微秒级重组网络拓扑以卸载CPU/GPU集群中集合通信（AllReduce等）的硬件架构。
- **专利2：面向晶圆级大模型推理的高维最优扇出互连拓扑结构**
  - *核心Claim*：一种无需HBM的大规模SRAM片上/片间互连网络物理布局方法，通过特定维度的跳线设计降低最坏情况下的通信延迟。

### 2. 网内计算与算子类 (In-Network Computation)
- **专利3：基于查找表（LUT）的网内二值化神经网络硬件加速装置及方法**
  - *核心Claim*：在网络交换节点/网卡中，将神经网络计算映射为查找表路径，实现零计算开销（仅查表延迟）的数据面AI推理。
- **专利4：一种面向万亿参数大模型的网内原生AI梯度归约通信加速系统**
  - *核心Claim*：在交换机层级实现FP16/BF16浮点数的在网累加与门控同步，避免数据在计算节点和网络间往复搬运。

### 3. 神经形态与复杂网络涌现类 (Neuromorphic & Emergence)
- **专利5：基于时空协同复杂度（CST）的神经网络架构自适应演化方法**
  - *核心Claim*：一种训练时方法，通过实时监测每一层的空间与时间复杂度，动态调整神经元连接（剪枝或生长），使网络保持在自组织临界态。
- **专利6：一种模拟生物突触可塑性与稳态自由能的神经形态芯片资源分配方法**
  - *核心Claim*：在固定硬件互连资源下，将自由能原理（FEP）作为硬件反馈信号，惩罚长程无效连接，自动促成“小世界”高能效拓扑的生成。

---

## 三、 后续执行计划 (Next Steps & Action Plan)

为避免“想法分散、只写不练”的死循环，建议采用以下分工流水线推进：

### Phase 1: 理论锚定与语料消化 (本月)
- **动作**：Genspark (云端) 分析 `D:\iNEST\Download` 中近 200 篇前沿文献，提取**“Free Energy Principle”**, **“Wafer-scale Interconnect”**, **“Criticality in SNN”** 的最新数据指标。
- **产出**：将提取的关键指标与理论基线汇入 Vault 内的 `10_Knowledge/SSOT/00 SSOT 权威条目`，形成所有论文的统一引用源。

### Phase 2: 专利抢位与防守 (下月)
- **动作**：优先完成**专利1、专利2、专利4**的交底书撰写。这是因为硬件架构和互连拓扑最容易被工业界（如Groq, Etched, Tesla Dojo）卡位，必须先声夺人。
- **工具**：使用本地 TRAE 协助梳理专利的结构框图与权利要求书草稿。

### Phase 3: 实验复现与数据支撑 (未来3个月)
- **动作**：
  1. 搭建拓扑仿真器（例如使用 OMNeT++ 或 BookSim2），模拟大模型在 TCC 拓扑下的通信延迟。
  2. 搭建 SNN 自组织临界态仿真环境（例如使用 Brian2），观测不同拓扑下的雪崩分布（Avalanche distribution）与 CST 涌现阈值。
- **产出**：获取论文 1、2、4 的核心实验图表。

### Phase 4: 论文冲刺与顶会投稿 (未来半年)
- **动作**：基于 Phase 1 的理论 SSOT 与 Phase 3 的仿真图表，结合 Genspark 强大的学术推理与 LaTeX 撰写能力，优先冲刺《Network-Centric Computing 范式奠基》和《A Unified Theory of Intelligence Emergence (CST)》两篇旗舰论文。
