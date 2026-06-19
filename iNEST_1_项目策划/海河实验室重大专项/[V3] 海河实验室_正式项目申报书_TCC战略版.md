---
title: 海河实验室2026年度重大专项正式项目申报书（V3·TCC战略版）
tags:
  - brain
  - chip
  - chiplet
  - complex-networks
  - dynamics
  - paper
  - patent
  - project
  - simulation
  - topology
  - TCC
  - FPGA
  - SDSoW
  - SDI
  - LiquidHardware
  - StrategicProposal
  - TCC-11
last_revised: 2026-06-19
---

**项目名称：面向拓扑中心计算（TCC）范式的液态硬件FPGA原型验证平台——海河实验室软件定义晶上系统（SDSoW）先导项目**

**申报单位：天津大学微电子学院**
**项目负责人：刘勤让**
**申报经费：2000万元**
**项目周期：2026年10月—2029年9月（3年）**

---

# 第一部分：战略背景与范式机遇

## 1.1 计算架构70年未变之困局

自1945年冯·诺依曼确立"存储程序"概念以来，计算架构的核心范式始终如一：**计算在节点内完成，通信是节点间的附属操作**。这一"节点中心"范式支撑了Moore定律的持续兑现，但至2026年，三重趋势正将其推向物理极限：

**趋势一：大模型向边缘端渗透，通信瓶颈从数据中心蔓延至端侧。** Meta Llama 4系列覆盖8B至405B全谱系，8B模型可在边缘设备以INT4精度运行。但当多路并发推理时，各节点中间特征融合（AllReduce）的开销占端到端延迟的40%~60%。传统SoC的固化片上网络（如2D Mesh）对此束手无策——它被设计为承载均匀流量的"通用公路"，而非针对特定算法数据流的"专用高铁"。

**趋势二：智能传感器融合对异构计算提出终极考验。** L4自动驾驶需同时处理8-12路摄像头、4-6路毫米波雷达、1-3路激光雷达。视觉推理依赖矩阵乘密集计算（GEMM），雷达信号处理依赖快速傅里叶变换（FFT）——两者的最优数据流拓扑截然相反，而传统芯片只能用一套固定互连同时应对两种需求，**如同用高速公路同时跑F1赛车和越野卡车**。

**趋势三：国际竞争格局加速演变，互连技术成为博弈制高点。** NVIDIA通过NVLink 5 + NVSwitch 4构建GB300 NVL72的72-GPU私有互连生态（2025），以封闭协议锁定高端AI训练市场。UCIe 2.0（2024）虽统一了芯粒间物理层标准，但**协议层以上仍是空白**——如何让不同厂商的芯粒在同一块晶圆上协同计算，如何让物理网络随算法需求动态重构，这是UCIe尚未触及、也是中国可以抢占的战略窗口。

## 1.2 全球技术竞速：晶圆级计算与可重构架构的最新进展

| 代表系统 | 规模 | 拓扑 | 根本局限 | TCC的超越点 |
|---------|------|------|---------|------------|
| **Cerebras WSE-3** (2024) | 4万亿晶体管<br>90万核心<br>晶圆级单片 | 2D Mesh<br>均匀网格 | 拓扑完全固化，<br>无法按算法优化 | 复杂拓扑+动态重构<br>算法自适应 |
| **NVIDIA GB300 NVL72** (2025) | 72 GPU<br>NVSwitch全互连 | Fat-Tree<br>静态树 | 互连协议私有，<br>拓扑不可编程 | TCC-Link开放标准<br>拓扑可重构指令集 |
| **Groq LPU** (2024) | 确定性调度<br>Tensor Streaming | 固定数据流<br>单向流水线 | 仅适用于编译器定制，<br>无通用性 | 拓扑即编译器目标<br>算法无关 |
| **SambaNova RDA** (2023) | 可重构数据流<br>SN40L | 动态数据流<br>粗粒度重构 | 重构在核级，<br>不在拓扑级 | 微秒级拓扑级<br>液态重构 |
| **Tenstorrent** (2024) | Tensix核心<br>RISC-V | 2D BiMesh<br>可扩展 | 仍为固定拓扑，<br>无软件定义互连 | 拓扑成为一级<br>可编程对象 |

**核心洞察**：全球领先者已在晶圆级集成和可重构计算两个方向分别取得突破，但**尚无任何一家将二者结合**——即在晶圆级规模上实现软件定义的拓扑重构。这正是TCC范式的历史性窗口。

## 1.3 海河实验室的战略机遇：SDSoW先导项目

海河实验室在"软件定义晶上系统（SDSoW）"方向上已有系统性布局。TCC范式是SDSoW的理论内核，TCC-Link是SDSoW的标准基础，"液态硬件"是SDSoW的工程表达。本项目作为**SDSoW的先导与奠基性项目**，承担三大战略使命：

1. **范式验证**：用FPGA原型证明"物理拓扑即计算"在工程上可行
2. **标准抢位**：在UCIe尚未覆盖的协议层/语义层建立中国主导的TCC-Link标准
3. **产业锚点**：为后续ASIC流片、晶圆级集成和产业化孵化提供经过验证的技术底座

**本项目不追求9颗芯粒的全定制流片。战略逻辑清晰：以1945年ENIAC验证"存储程序"的方式，用FPGA验证TCC范式——范式成立后再推进流片，分步降低风险。**

---

# 第二部分：Route-Transform理论体系——范式级创新

## 2.1 从"节点中心"到"拓扑中心"：计算架构的范式跃迁

传统计算架构的核心假设是：**计算发生在节点内部，互连网络仅负责数据搬运**。这一假设在稀疏通信场景下成立，但在密集通信场景中，通信开销主导系统性能。

TCC范式的核心颠覆：**将互连网络从"数据搬运工"提升为"计算执行者"**。当物理拓扑本身可以原生承载通信/变换操作时，通信操作不再需要经过节点——它在网络传输的过程中就已经完成。

```
传统范式：  数据 → 节点A → [搬运] → 节点B → 计算 → 输出
                        ↑ 通信开销（无效能量）

TCC范式：  数据 → 节点A → [拓扑原生计算] → 输出
                        ↑ 通信即计算（零额外开销）
```

## 2.2 路由-变换分解定理（Theorem 1）

**定理**：任意分布式张量计算任务 $\mathcal{C}$，可唯一分解为路由操作（Route, $\mathcal{R}$）与变换操作（Transform, $\mathcal{T}$）的交替复合序列：

$$\mathcal{C} = \mathcal{T}_k \circ \mathcal{R}_k \circ \cdots \circ \mathcal{T}_1 \circ \mathcal{R}_1$$

**物理意义**：该定理证明，Route与Transform是分布式计算的两个正交基。任何一个"计算"都可以被分解为"数据如何在节点间流动（Route）"和"节点对数据做了什么（Transform）"。当硬件可以分别加速这两类基元操作时，任意分布式计算均可映射到同一套硬件上——无需为每个算法定制芯片。

## 2.3 路由即变换同构定理（Theorem 2）——理论核心

**定理**：特定类别的Route操作与Transform操作之间存在严格的图同构关系。这不是巧合，而是分布式计算深层数学结构的体现。

**"杀手级图表"**——8对Route-Transform同构映射：

| 变换操作 (Transform) | 路由操作 (Route) | 同构类型 | 共享拓扑 |
|---------------------|-----------------|---------|---------|
| FFT蝶形运算 | AllReduce（维度有序） | 图同构 $\mathcal{B}_k \cong \mathcal{A}_k$ | Butterfly |
| 矩阵转置 | AlltoAll | 置换同构 | Crossbar |
| 前缀和 | Scan（前缀归约） | 操作同构 | Binary Tree |
| Reduce（树形归约） | Reduce（树形通信） | 恒等映射（完全相同） | Tree |
| 卷积滑窗 | Shift + Overlap通信 | 循环同构 | Ring/Torus |
| 注意力QK^T | AllGather(K) + 本地GEMM | 功能分解 | Star→Local |
| 排序网络 | Butterfly通信 | 图同构 | Butterfly |
| 稀疏矩阵×向量 | Scatter/Gather | 邻接同构 | 原始图拓扑 |

**这张表的震撼之处**：它表明，我们以为截然不同的"计算操作"和"通信操作"，在拓扑层面竟然是同一件事。这不是偶然——这是分布式计算的深层数学结构。

**工程推论**：当硬件拥有可重构的物理拓扑时，同一组物理连线可以在AI推理中承担AllReduce通信，在雷达信号处理中承担FFT蝶形变换——连线完全不变，仅需切换端点的操作模式。TCC范式正是将这一数学洞察转化为硬件架构。

## 2.4 TCC范式的学术演化定位

```
第一代：节点中心计算（Node-Centric, 1945-）
  "计算在节点，通信是附庸"
  代表：冯·诺依曼架构, x86, ARM, GPU, NPU
  瓶颈：通信墙（Communication Wall）

第二代：拓扑中心计算（Topology-Centric, 2026-）
  "物理拓扑即计算，Route ≡ Transform"
  代表：本项目 NCC-Edge 液态硬件
  突破：消除通信瓶颈，一套硬件多场景自适应

第三代：涌现计算（Emergent Computing, 远期）
  "物理网络自发涌现计算与智能行为"
  关键：拓扑相变临界态 + 自适应集体动力学
```

本项目为**第二代范式的首次系统性工程验证**。

---

# 第三部分：TCC-11原语体系与三阶段演进战略

## 3.1 TCC-11原语库——三分类完备体系

TCC原语库v1.0定义了由11个原语构成的完备计算代数系统。遵循三条设计原则：**代数完备性**（任意分布式计算可在有限步内由原语组合表达）、**正交最小性**（任何一个原语不能被其余原语在O(1)或O(log N)步内等价替代）、**硬件可映射性**（每个原语对应面积≤50K LUT等效门的独立RTL IP核）。

命名规则：统一前缀 `tcc.`，后接四字母可发音英语动词助记符。

```
┌─────────────────────────────────────────────────────────────────┐
│                     TCC-11 PRIMITIVE LIBRARY v1.0                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  通信原语 (Route, 4个) ─── 定义数据在节点间的流动模式             │
│  ┌──────────┬──────────┬──────────┬──────────┐                 │
│  │ tcc.FUSE │ tcc.PULL │ tcc.CAST │ tcc.SWAP │                 │
│  │    ⊕     │    ⇊     │    ⇈     │    ⥂     │                 │
│  │ AllReduce│ AllGather│ Broadcast│ AlltoAll │                 │
│  └──────────┴──────────┴──────────┴──────────┘                 │
│                                                                 │
│  计算原语 (Transform, 4个) ─── 定义节点对数据的变换操作           │
│  ┌──────────┬──────────┬──────────┬──────────┐                 │
│  │ tcc.GEMM │ tcc.FOLD │ tcc.MAPS │ tcc.SCAN │                 │
│  │    ⊗     │    ⊐     │    ⨀     │    ⤓     │                 │
│  │ 矩阵乘加  │ 向量归约  │逐元素映射 │ 前缀扫描  │                 │
│  └──────────┴──────────┴──────────┴──────────┘                 │
│                                                                 │
│  流动原语 (Flow, 3个) ─── 定义数据与控制的物理调度                │
│  ┌──────────┬──────────┬──────────┐                            │
│  │ tcc.MOVE │ tcc.LINK │ tcc.TICK │                            │
│  │    ↗     │    ⚙     │    ⏱     │                            │
│  │点对点搬移 │ 拓扑控制  │ 同步屏障  │                            │
│  └──────────┴──────────┴──────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

**完备性验证**：TCC-11已通过7个典型场景（LLM推理、视频目标检测、雷达DBF、SpMV、FFT、MoE训练、图神经网络）的逐原语覆盖验证，覆盖率100%。关键发现：**MAPS和LINK是唯二在所有场景中都出现的原语**——"逐元素映射"和"拓扑控制"是TCC范式的两大绝对核心。

## 3.2 从FPGA原型到SDSoW的完整演进链

```
Phase 1 (本项目, 2026-2029): FPGA原型验证 —— 证明范式可行
  ├── "3+1"架构FPGA实现（FUSE/GEMM/MAPS/LINK）
  ├── TCC-Link v1.0标准发布（覆盖L1-L4全栈）
  ├── 双场景（AI+DBF）液态切换验证
  └── TRL-5（系统级原型验证）

Phase 2 (2029-2031): ASIC产品化 —— 端侧双模芯片
  ├── 基于验证IP的28nm/12nm ASIC流片（扩展至TCC-11全集）
  ├── NCC-Edge-ASIC产品原型（RT-Infer-30边缘推理卡）
  ├── 孵化公司独立运营
  └── TRL-7（工程样机）

Phase 3 (2031-2035): SDSoW晶圆级 —— 大规模液态计算
  ├── 晶圆级复杂拓扑互连（连接规模>10^8）
  ├── Chiplet + 3D堆叠异质集成
  ├── TCC-Link成为国内行业标准
  └── TRL-9（量产部署）
```

**本项目聚焦Phase 1，所有架构决策（IP核接口、TCC-Link标准、SDK API）均预留Phase 2/3的迁移路径。**

## 3.3 Phase 1技术路线关键决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 验证载体 | FPGA（非ASIC流片） | 规避流片风险；FPGA天然可重构＝"液态硬件"最佳物理载体 |
| 原语数量 | 4个（非TCC-11全集） | FUSE/GEMM/MAPS/LINK是Route-Transform同构的最小完备验证集 |
| 工艺节点 | FPGA（等效16nm）+ 可选28nm流片 | 28nm成熟可靠、成本可控，作为ASIC可行性预研 |
| 场景数量 | 2主+1扩 | AI推理和DBF是拓扑差异最大的应用对 |
| 标准策略 | L1/L2兼容UCIe + L3/L4颠覆创新 | 降低物理层风险，集中创新于协议/语义层 |
| 软件栈 | TCCL兼容层 + tcc Python API | 最大化现有AI生态即插即用性 |

---

# 第四部分："3+1"液态硬件极简架构

## 4.1 架构设计哲学

TCC-11原语库定义了三类原语。Phase 1的FPGA原型聚焦于验证原语的最小完备子集——恰好是"3个数据原语 + 1个控制原语"：

- **tcc.FUSE**：通信原语。蝴蝶网归约/变换引擎，是Route-Transform同构的物理证明载体
- **tcc.GEMM**：计算原语。脉动阵列矩阵乘，是AI推理和DBF波束成形的共享算力源
- **tcc.MAPS**：计算原语。逐元素映射，是FFT旋转因子乘法、激活函数、归一化的执行单元
- **tcc.LINK**：流动原语。拓扑重构控制器，管理蝴蝶网络在AllReduce模式和FFT模式间的微秒级切换

**设计原则**：原语级特化——每个IP核只加速一类原语操作，极致优化面积与功耗。LINK使物理拓扑成为一级可编程资源。

## 4.2 四核心IP深度设计

### IP-1: tcc.FUSE — 蝶形网络双模归约/变换引擎

**定位**：Route-Transform同构定理的物理证明载体。在同一个蝶形网络硬件上，通过操作模式切换，同时实现AllReduce归约和FFT蝶形加减——**连线完全不变，仅改变节点内部操作类型**。

**微架构**：

```
             tcc.FUSE 蝶形网络引擎
        ┌─────────────────────────────────┐
        │  16路输入 × 256b                │
        │      ↓                          │
        │  Stage 0: 16→8                  │
        │  ┌──────────────────────┐       │
        │  │ 8个可配置运算单元      │       │
        │  │ 模式A: REDUCE_SUM    │       │  ← AllReduce归约
        │  │ 模式B: BUTTERFLY_ADDSUB│      │  ← FFT蝶形加减
        │  └──────────────────────┘       │
        │      ↓                          │
        │  Stage 1: 8→4 (同上)            │
        │  Stage 2: 4→2 (同上)            │
        │  Stage 3: 2→1 (同上)            │
        │      ↓                          │
        │  广播路径: 1→2→4→8→16           │
        │  (AllReduce share阶段，时分复用) │
        └─────────────────────────────────┘
```

**关键设计创新**：归约路径（叶→根）与广播路径（根→叶）共享同一组蝶形连线，通过LINK控制数据流向实现时分复用，节省约40%的连线资源。

**关键指标**：
- 16节点FP16 AllReduce延迟：<2μs
- FFT蝶形加减吞吐：每级<500ns（1024点=10级，总计<5μs）
- 模式切换（REDUCE_SUM ↔ BUTTERFLY_ADDSUB）：<100ns
- RTL规模：~5,500行 SystemVerilog

### IP-2: tcc.GEMM — 可配置脉动阵列矩阵乘引擎

**定位**：AI推理骨干网络和DBF波束成形权重的共享矩阵乘加速器。可在线切换阵列尺寸和数值精度。

**微架构**：

```
            tcc.GEMM 脉动阵列
        ┌─────────────────────────┐
        │   权重 (沿列方向广播)     │
        │   ↓  ↓  ↓  ↓           │
        │   [MAC][MAC][MAC][MAC] →│ 部分和
        │   [MAC][MAC][MAC][MAC]  │
        │   [MAC][MAC][MAC][MAC]  │  可配置:
        │   [MAC][MAC][MAC][MAC]  │  32×32 / 64×16
        │      ↓  ↓  ↓  ↓        │  INT8 / FP16
        │   部分和累加输出          │
        └─────────────────────────┘
```

**在线可配置性**：通过LINK指令在运行时切换阵列尺寸和数值精度。AI推理场景使用INT8 32×32高吞吐配置；DBF场景使用FP16 16×16+32×16（复数乘法需要更高的数值精度）。

**关键指标**：
- INT8峰值算力：≥1 TOPS（FPGA，等效ASIC 28nm约8 TOPS）
- FP16峰值算力：≥250 GFLOPS（FPGA）
- MAC利用率：>80%
- RTL规模：~6,000行 SystemVerilog

### IP-3: tcc.MAPS — 逐元素映射引擎

**定位**：执行所有逐元素操作——FFT旋转因子乘法、神经网络激活函数、归一化、阈值过滤。在TCC-11完备性验证中，MAPS是唯二在所有7个场景中都出现的原语之一。

**微架构**：

```
          tcc.MAPS 逐元素映射引擎
        ┌──────────────────────────┐
        │  256b 向量输入            │
        │      ↓                   │
        │  ┌──────────────────┐    │
        │  │  操作码解码        │    │
        │  │  · TWIDDLE_MUL    │    │  ← FFT旋转因子复数乘
        │  │  · ACTIVATION     │    │  ← SiLU/GELU/ReLU
        │  │  · NORMALIZE      │    │  ← LayerNorm/RMSNorm
        │  │  · THRESHOLD      │    │  ← NMS/CFAR阈值
        │  │  · CAST           │    │  ← 数据类型转换
        │  └──────────────────┘    │
        │      ↓                   │
        │  ┌──────────────────┐    │
        │  │ 16路并行SIMD ALU  │    │
        │  │ (INT8/FP16可配)   │    │
        │  └──────────────────┘    │
        │      ↓                   │
        │  256b 向量输出            │
        └──────────────────────────┘
```

**关键指标**：
- 16路SIMD并行：256b/周期
- 操作延迟：2-4周期（依操作类型）
- 支持的FP16逐元素操作：≥15种
- RTL规模：~4,200行 SystemVerilog

### IP-4: tcc.LINK — 拓扑重构控制器

**定位**：液态硬件的"神经中枢"，TCC-Link标准的硬件实现载体。LINK是TCC-11流动原语的核心——它管理拓扑的配置、切换和监控，使物理网络从静态连线变为可编程资源。

**微架构**：

```
        tcc.LINK 拓扑重构控制器
    ┌────────────────────────────────────┐
    │  ┌──────────┐  ┌──────────────┐   │
    │  │ 指令解码  │  │ 拓扑配置SRAM  │   │
    │  │ (TR-ISA) │  │ (16×2048b)   │   │
    │  └────┬─────┘  └──────┬───────┘   │
    │       │               │           │
    │  ┌────┴───────────────┴──────┐    │
    │  │      拓扑执行引擎         │    │
    │  │  - 路由表并行加载         │    │
    │  │  - FUSE模式原子切换       │    │
    │  │  - 链路训练与校准         │    │
    │  └────────────┬──────────────┘    │
    │               │                   │
    │  ┌────────────┴──────────────┐    │
    │  │   流控与链路监控           │    │
    │  │  - Credit-based flow ctrl │    │
    │  │  - 误码率实时监测         │    │
    │  │  - 温度/功耗感知          │    │
    │  └───────────────────────────┘    │
    └────────────────────────────────────┘
```

**关键指标**：
- 拓扑热切换延迟：≤1μs（从RECONFIG_ATOMIC指令到所有连线模式切换完成）
- 预设拓扑容量：≥16个完整配置
- 单节点路由表在线更新：<100ns
- RTL规模：~5,000行 SystemVerilog

## 4.3 "3+1"完备性论证：为什么这四个就够了

| TCC范式验证目标 | 所需原语 | 验证方式 |
|---------------|---------|---------|
| Route-Transform分解定理 | FUSE + MAPS + GEMM | 通信原语+计算原语协同映射 |
| Route-Transform同构定理 | FUSE + LINK | FUSE双模（REDUCE_SUM/BUTTERFLY_ADDSUB）在同一LINK拓扑上切换 |
| 通信硬件化 | FUSE | AllReduce在物理网络中完成，CPU零参与 |
| AI推理全链路 | GEMM + MAPS + FUSE + LINK | 矩阵乘骨干+激活MAPS+AllReduce FUSE+LINK拓扑管理 |
| DBF信号处理 | LINK + MAPS + FUSE + GEMM | FFT = LINK(butterfly_stage) + MAPS(twiddle) + FUSE(butterfly) ×10级 + GEMM(波束权重) |
| 液态切换 | LINK | ≤1μs AI↔DBF拓扑热切换 |

**结论**：4个原语构成Route-Transform同构验证的最小完备集。TCC-11其余7个原语（PULL/CAST/SWAP/FOLD/SCAN/MOVE/TICK）在Phase 1的SDK中以软件回退方式实现，Phase 2的ASIC流片时硬件化。

---

# 第五部分：TCC-Link接口标准——兼容与超越

## 5.1 标准定位：中国主导的拓扑可重构芯粒互连标准

TCC-Link是本项目的核心标准输出。战略定位：**在UCIe尚未覆盖的协议层与语义层，建立由中国主导、原生支持拓扑可重构指令集的下一代芯粒互连标准。**

UCIe 2.0（2024）统一了芯粒间物理层与链路层的电气/管脚规范。但其协议层仍是**点对点、静态互连**——它定义了"如何可靠传输数据"，但没有定义"如何让网络随算法变化"。TCC-Link填补的正是这个空白。

```
UCIe 2.0（已完成）：                  TCC-Link v1.0（本项目）:
┌──────────────────────┐         ┌──────────────────────┐
│ 物理层 (L1)          │         │ 物理层 (L1)          │
│ 电气/管脚规范         │         │ ← 完全兼容 UCIe 2.0  │
├──────────────────────┤         ├──────────────────────┤
│ 链路层 (L2)          │         │ 链路层 (L2)          │
│ Flit格式/CRC/重传    │         │ ← 兼容UCIe + 扩展     │
├──────────────────────┤         ├──────────────────────┤
│ 协议层 (L3)          │         │ 协议层 (L3) ← 创新   │
│ 仅点对点传输          │  --->   │ 拓扑可重构指令集(TR-ISA)│
│ 无拓扑概念            │         │ 源路由 + 多跳         │
├──────────────────────┤         ├──────────────────────┤
│ (空白)               │         │ 语义层 (L4) ← 创新   │
│                      │         │ TCC原语事务语义        │
│                      │         │ (tcc.fuse/pull/...)   │
└──────────────────────┘         └──────────────────────┘
     静态互连标准                        动态液态互连标准
```

## 5.2 TCC-Link四层架构详解

### L1 — 物理层（全面兼容UCIe 2.0）

| 参数 | 规格 | 说明 |
|------|------|------|
| 信号制式 | 差分NRZ/PAM4 | 与UCIe 2.0 Advanced Package一致 |
| 单lane速率 | 16 GT/s (NRZ) / 32 GT/s (PAM4) | 满足FPGA GTY/GTM SerDes能力 |
| 延迟 | <2ns（芯粒间）/ <10ns（板间） | 端到端，不含协议开销 |
| 功耗效率 | <1 pJ/bit | 对标UCIe标准功耗包络 |

### L2 — 链路层（兼容+扩展）

在UCIe标准Flit（64B）基础上扩展1B拓扑控制字段。当TopoCtrl字段为全零时，Flit与UCIe标准格式完全一致，确保基本互通。

### L3 — 协议层（颠覆创新）：拓扑可重构指令集（TR-ISA）

TCC-Link区别于所有现有互连标准的根本特征——在协议层原生定义六条拓扑重构指令：

| 指令 | 操作码 | 功能 | 执行延迟 |
|------|--------|------|---------|
| RECONFIG_TOPO | 0xF0 | 加载预设拓扑ID，并行更新所有受影响节点的路由表和连线模式 | <500ns |
| RECONFIG_NODE | 0xF1 | 在线更新单节点路由表（增量拓扑调整） | <100ns |
| RECONFIG_QUERY | 0xF2 | 查询指定节点当前路由表和链路状态 | <200ns |
| RECONFIG_ATOMIC | 0xF3 | 原子拓扑切换：冻结数据流→批量更新→恢复传输 | ≤1μs |
| RECONFIG_TRAIN | 0xF4 | 触发指定链路重新训练（SerDes CDR/均衡器校准） | <10μs |
| RECONFIG_LOCK | 0xF5 | 锁定/解锁拓扑配置（防误操作） | <50ns |

**TR-ISA指令以带内数据帧传输**——无需额外配置总线或JTAG链路，拓扑重构像发送数据包一样简单。

### L4 — 语义层（颠覆创新）：TCC原语事务

L4定义面向上层软件的TCC-11原语事务接口。上层通过 `tcc.fuse()`、`tcc.gemm()` 等Python API发出原语调用，L4将其封装为标准事务帧，L3通过TR-ISA管理拓扑，L2/L1负责物理传输。

## 5.3 标准输出路径

| 里程碑 | 时间 | 内容 |
|--------|------|------|
| v0.5 内部草案 | 2027 Q1 | L1-L4完整规范初稿，FPGA级验证 |
| v1.0 公开发布 | 2027 Q4 | 经FPGA验证修正的正式规范白皮书 |
| CCIA标准提案 | 2028 Q2 | 向中国通信工业协会提交标准立项 |
| UCIe对齐与互操作 | 2028 Q4 | v1.1，与UCIe 2.x规范对齐验证 |
| 行业标准推进 | 2029+ | 基于ASIC验证的v2.0 |

---

# 第六部分：FPGA原型验证平台

## 6.1 硬件方案

| 组件 | 选型 | 数量 | 关键参数 |
|------|------|------|---------|
| 主FPGA | Xilinx VCU128 (VU13P) | 2块 | ~1.7M LUTs, ~6.8K DSPs, 16×GTY(28Gbps) |
| 辅助节点 | Kria K26 SOM | 4块 | 多节点端侧设备模拟 |
| 板间互连 | 自定义PCB背板 + FMC+ | 1套 | 8 lane × 16Gbps |
| 测试仪器(租赁) | Keysight 20GHz示波器/Anritsu误码仪 | 按需 | 信号完整性验证 |

## 6.2 FPGA资源预评估（单颗VU13P）

| 模块 | LUTs | DSPs | BRAM(36Kb) | 占比 |
|------|------|------|-----------|------|
| tcc.FUSE ×4 | ~80K | ~200 | ~200 | 15% |
| tcc.GEMM (32×32) ×2 | ~120K | ~1024 | ~300 | 22% |
| tcc.MAPS ×2 | ~50K | ~400 | ~150 | 10% |
| tcc.LINK | ~40K | 0 | ~50 | 8% |
| SerDes wrapper ×16 | ~40K | 0 | ~80 | 8% |
| DDR4/PCIe/基础设施 | ~60K | 0 | ~130 | 12% |
| **合计** | **~390K** | **~1624** | **~910** | **~75%** |

**75%利用率为安全区间**，25%余量应对布局布线拥挤和后期功能扩展。若时序收敛困难，可降级为单GEMM实例和2个FUSE实例（降至~55%）。

## 6.3 五级验证闭环

```
L0: 模块级仿真（cocotb + Verilator）→ 覆盖率>95%
L1: 子系统级（FUSE+LINK互联；MAPS+FUSE+GEMM FFT协同）
L2: 单FPGA全系统集成（时序收敛 @ 250MHz）
L3: 双FPGA互联系统（SerDes 16Gbps跨板通信）
L4: 上位机可视化演示（实时拓扑动画 + 数据流 + 性能指标）
```

---

# 第七部分：双场景融合验证

## 7.1 场景A：端侧多路并发AI视觉推理

**场景**：4路摄像头同时输入，每路运行YOLO-nano目标检测，中间特征经硬件AllReduce融合。

**原语映射（AI模式）**：

```
# 每路K26运行YOLO-nano骨干
tcc.GEMM(im2col(frame), W_conv)     # 卷积
tcc.MAPS(SiLU(x))                    # 激活
tcc.MAPS(normalize(x, μ, σ))         # BatchNorm

# 4路进入主FPGA融合
tcc.LINK.config("tree_4way")          # 蝶形归约树拓扑
tcc.FUSE(features, SUM)               # ★ 硬件AllReduce（CPU零参与）
```

**核心验证指标**：

| 指标 | 目标值 | 对比基线 |
|------|--------|---------|
| 4路AllReduce融合延迟 | <5μs | NCCL软件AllReduce ~100μs |
| 通信带宽利用率 | >85% | PCIe方案 ~40% |
| 端到端推理延迟(P99) | <2ms | CPU软件融合 ~10ms |

## 7.2 场景B：阵列雷达数字波束成形（DBF）——同构定理现场演示

**场景**：16通道雷达IQ数据，经FFT变换+波束成形，输出16个空间波束。

**原语映射（DBF模式）——FFT的TCC-11实现**：

```
# FFT的核心洞见：FFT不是独立原语，而是 LINK+MAPS+FUSE 的组合！

for k in range(10):                     # 1024点 = 10级蝶形
    tcc.LINK.config(f"butterfly_stage_{k}")  # ← 每级配置蝶形拓扑
    tcc.MAPS(data[i] * twiddle[k][i])        # ★ 旋转因子逐元素乘
    tcc.FUSE(a, b, mode=BUTTERFLY_ADDSUB)    # ★ FUSE双模切换！蝶形加减

# 波束成形
tcc.LINK.config("crossbar_beam")             # 切换到波束级拓扑
tcc.GEMM(freq_data, beam_weights)            # 复数波束权重矩阵乘
```

**★ Route-Transform同构定理的现场证明**：

```
AI模式下的 FUSE:                    DBF模式下的 FUSE:
  FUSE(a, b, mode=REDUCE_SUM)        FUSE(a, b, mode=BUTTERFLY_ADDSUB)
     归约加法树                          蝶形复数加减
          ↓                                  ↓
    === 同一组物理蝶形连线，同一个 tcc.FUSE，同一个 tcc.LINK 拓扑 ===
          ↓                                  ↓
   AllReduce通信 ≈ FFT计算  （在拓扑层面，它们是同一件事）
```

**上位机可视化**：动画展示连线从"红色（AI归约路径）"切换为"蓝色（DBF蝶形路径）"——连线结构完全相同，仅颜色和操作标注变化。

**核心验证指标**：

| 指标 | 目标值 | 对比基线 |
|------|--------|---------|
| 1024点FFT延迟 | <5μs | 软件FFTW ~50μs |
| 全链路DBF延迟 | <20μs | 传统DSP方案 ~200μs |
| 物理路径复用率 | ≥30% | 独立实现需2套互连 |
| AI→DBF拓扑切换 | ≤1μs | 传统方案需换硬件设备 |

## 7.3 场景C：液态切换压力测试

循环1000次：AI模式30秒 → RECONFIG_ATOMIC → DBF模式30秒。

- 切换成功率：≥99.99%
- 单次切换延迟P99：≤1μs
- 数据完整性：零丢失/零错误
- 链路稳定性：1000次后SerDes误码率无退化

---

# 第八部分：软件栈与生态——TCC Python SDK + 兼容层

## 8.1 PyiNEST-Lite 全栈SDK架构

TCC范式的成功取决于软件生态能否让现有AI开发者零门槛使用。PyiNEST-Lite的策略：**用户继续写PyTorch代码，底层自动映射到TCC原语硬件。**

```
┌─────────────────────────────────────────────────────────────────┐
│              用户应用层（零修改）                                  │
│  import torch; model = torch.nn.DataParallel(model)              │
│  output = model(data)  # 代码完全不变                             │
├─────────────────────────────────────────────────────────────────┤
│            TCCL 兼容层（NCCL/MPI/Gloo API 映射）                    │
│  ncclAllReduce(...) → tcc.fuse(buf, op=SUM, topo=BUTTERFLY)     │
│  MPI_Allgather(...)  → tcc.pull(buf)                             │
│  fftw_execute(...)   → for k: tcc.link+ tcc.maps + tcc.fuse    │
├─────────────────────────────────────────────────────────────────┤
│         PyiNEST-Lite Runtime（Python + C++）                       │
│  Graph Compiler: 原语调用序列优化为执行图                          │
│  Topology Planner: 自动生成最优拓扑切换序列                        │
│  Memory Manager: 片上SRAM/片外DRAM统一管理                        │
├─────────────────────────────────────────────────────────────────┤
│         PyiNEST-Lite Driver（C + 内核模块）                         │
│  PCIe Gen3 DMA引擎（P2P零拷贝）  |  tcc.LINK 寄存器映射（MMIO）     │
│  中断管理：完成/错误/热插拔        |  Credit-based流控硬件接口      │
├─────────────────────────────────────────────────────────────────┤
│            NCC-Edge FPGA 液态硬件                                  │
└─────────────────────────────────────────────────────────────────┘
```

**关键创新：TCCL兼容层**

TCCL是NCCL的API级兼容实现，拦截所有NCCL调用并翻译为对应的TCC原语事务。同时兼容MPI collective、Gloo、FFTW等API——使PyTorch/TensorFlow/JAX/MATLAB用户无需修改代码即可直调液态硬件。

```python
# TCCL兼容层核心逻辑
class TCCLAllReduce:
    def __call__(self, sendbuff, recvbuff, count, datatype, op, comm, stream):
        topo_id = self.topo_selector.select(count, comm.nranks)
        if topo_id != self.current_topo:
            self.link.reconfig_atomic(topo_id)     # tcc.LINK触发拓扑切换
        return self.tcc.fuse(sendbuff, op=op)       # tcc.FUSE执行硬件AllReduce
```

## 8.2 tcc Python API

```python
import tcc

# 通信原语
tcc.fuse(buf, op=tcc.SUM, topo=tcc.BUTTERFLY)   # AllReduce
tcc.pull(buf)                                     # AllGather
tcc.cast(buf, root=0)                             # Broadcast
tcc.swap(sendbuf, recvbuf)                        # AlltoAll

# 计算原语
tcc.gemm(A, B, C, alpha=1.0, dtype=tcc.INT8)     # 矩阵乘加
tcc.fold(buf, op=tcc.ARGMAX)                      # 向量归约
tcc.maps(buf, op=tcc.SILU)                        # 逐元素映射
tcc.scan(buf, op=tcc.SUM)                         # 前缀扫描

# 流动原语
tcc.link.config(tcc.BUTTERFLY, stage=3)           # 拓扑控制
tcc.move(src, dst, nbytes)                        # 点对点搬移
tcc.tick.stamp()                                  # 同步屏障
```

## 8.3 开源生态

| 开源组件 | 规模 | 许可证 | 发布 |
|---------|------|--------|------|
| "3+1"核心RTL | ≥20K行 SystemVerilog | Apache 2.0 | 2028 Q2 |
| PyiNEST-Lite SDK | ≥15K行 Python/C++ | Apache 2.0 | 2028 Q2 |
| TCCL兼容层 | ≥5K行 C/C++ | BSD 3-Clause | 2028 Q3 |
| DSE拓扑探索工具 | ≥8K行 Python | Apache 2.0 | 2028 Q4 |

CI/CD：GitHub Actions + 自建Runner，每PR自动执行cocotb仿真 + Verilator lint + 集成测试。社区：季度Workshop + GitHub Discussions。

---

# 第九部分：项目推进路线图

## 9.1 三年详细计划（含18个月分布式缓冲）

```
         2026 Q4      2027 Q1-Q4           2028 Q1-Q4           2029 Q1-Q3
         ────────     ─────────────────    ─────────────────    ───────────

理论      ██████████  Route-Transform      ─                     ─
                      分解+同构严格证明
                      
TCC-Link  ██ v0.3     ██ v0.5 ██ v1.0发布  CCIA提案 █ UCIe对齐   ██ 定稿 █

tcc.FUSE  ██ 设计     █ FPGA实现 ██████ 双模优化                  ─

tcc.GEMM  █ RTL设计   █ FPGA实现 ██████████ 优化                  ─

tcc.MAPS  ██ 设计     █ FPGA实现 ██████ 操作扩展                  ─

tcc.LINK  █ 设计      █ FPGA实现 ██████ 热切换优化                ─

软件栈    █ 骨架搭建  █ SDK开发 ███ TCCL ████ DSE ████            █ 文档 █

场景A     ─           █ 单路验证  ██ 4路集成 ██ 优化              验收 █

场景B     ─           ─            DBF单路 ██ 全链路集成 ██████   验收 █

场景C     ─           ─            ─            热切换压测 ██████ 验收 █

论文      理论投稿    █ 同构投HPCA  ██ 系统投SC ██                 发表 █

专利      申请≥5项    申请≥5项              申请≥5项               授权≥8项

█ = 关键路径  ─ = 缓冲期
```

**分布式缓冲设计**：

| 缓冲位置 | 时长 | 用途 |
|---------|------|------|
| 2027 Q2-Q4 | 6个月 | FPGA集成调试、时序收敛、首次SerDes互联调通 |
| 2028 Q3-Q4 | 6个月 | 全系统压力测试、上位机可视化演示系统开发 |
| 2029 Q1-Q3 | 6个月 | 验收准备、论文返修、标准定稿 |

## 9.2 可选验证流片（不影响核心验收）

| 里程碑 | 时间 | 内容 | 预算 | 前提条件 |
|--------|------|------|------|---------|
| MPW NRE | 2028 Q1 | 28nm MPW启动 | 50万 | FPGA验证通过 + 经费充裕 |
| GDSII交付 | 2028 Q3 | FUSE+GEMM+MAPS+LINK四合一测试芯片 | — | RTL冻结 |
| 回片测试 | 2029 Q1-Q2 | FPGA对比测试 | 150万 | 流片成功 |

**风险隔离**：流片为"锦上添花"加分项，核心指标100%在FPGA上交付。流片失败不影响项目结题。

---

# 第十部分：经费预算（2000万元）

## 10.1 总预算分配

| 经费类别 | Year 1 | Year 2 | Year 3 | 合计 | 占比 |
|---------|--------|--------|--------|------|------|
| 人员费用 | 250万 | 280万 | 270万 | **800万** | 40% |
| FPGA硬件与仪器 | 150万 | 100万 | 50万 | **300万** | 15% |
| 云服务与EDA工具 | 120万 | 100万 | 80万 | **300万** | 15% |
| 可选验证流片 | 0 | 50万 | 150万 | **200万** | 10% |
| 软件生态与开源 | 50万 | 80万 | 70万 | **200万** | 10% |
| 合作交流/专利/发表 | 40万 | 80万 | 80万 | **200万** | 10% |
| **合计** | **610万** | **690万** | **700万** | **2000万** | 100% |

## 10.2 人员配置

| 岗位 | 人数 | 年薪 | 3年总计 | 职责 |
|------|------|------|---------|------|
| PI（项目负责人） | 1人 | — | — | 总体架构、理论指导、产业对接 |
| 博士后（理论方向） | 1人 | 40万 | 120万 | Route-Transform分解+同构严格证明 |
| 博士后（标准方向） | 1人 | 40万 | 120万 | TCC-Link标准撰写、CCIA/UCIe对接 |
| 高级FPGA工程师 | 2人 | 50万 | 300万 | 4个IP核RTL开发、FPGA集成、时序收敛 |
| 高级软件工程师 | 1人 | 45万 | 135万 | PyiNEST-Lite SDK、TCCL兼容层 |
| 软件工程师 | 1人 | 30万 | 90万 | DSE工具、CI/CD、社区运营 |
| 博士生（≥4名） | 4人 | 劳务 | 劳务 | 分担RTL模块、论文撰写 |
| 硕士生（≥6名） | 6人 | 劳务 | 劳务 | 验证、测试、上位机开发 |
| **合计** | **约16人** | | **约800万** | |

## 10.3 经费弹性

| 资助额度 | 调整方案 |
|---------|---------|
| 2000万（满额） | 全栈交付：含验证流片 + 全功能SDK + 双场景全验证 |
| 1600万 | 裁减流片(-200万)、压缩1名工程师(-150万)、SDK裁剪(-50万) |
| 1200万（下限） | 仅FPGA原型 + 核心SDK，不流片，人员精简至12人 |

---

# 第十一部分：风险管控矩阵

## 11.1 技术风险

| # | 风险描述 | 概率 | 影响 | 缓解策略 |
|---|---------|------|------|---------|
| **R1** | Route-Transform同构定理在FPGA频率下存在时序不可收敛边界条件 | 中 | 高 | Year 1优先完成≥1000节点timing-accurate仿真；发现边界条件则限定适用范围 |
| **R2** | ≤1μs热切换在硬件上无法稳定实现 | 中 | 中 | 分级目标：≤1μs→≤10μs→≤100μs。即使100μs也远超传统秒级方案 |
| **R3** | SerDes 16Gbps自定义PCB信号完整性不达标 | 中 | 中 | 降速至8Gbps或改用FMC+标准子卡 |
| **R4** | FPGA时序收敛困难（全系统集成） | 中 | 中 | 降配：降DDR频率→降GEMM阵列→拆分为双FPGA |
| **R5** | MAPS+ FUSE FFT精度不满足DBF旁瓣抑制要求 | 低 | 中 | 默认FP16；若不达标，升级FP32（仅增~15%资源） |

## 11.2 管理与外部风险

| # | 风险描述 | 概率 | 影响 | 缓解策略 |
|---|---------|------|------|---------|
| **R6** | 关键工程师离职 | 中 | 高 | 核心IP双人负责；GitLab强制管理；薪酬+股权留任 |
| **R7** | 博士生毕业导致知识断层 | 高 | 中 | 工程师Code Review+内部Wiki+高低年级梯队交叠 |
| **R8** | TCC-Link标准CCIA立项受阻 | 中 | 低 | 白皮书本身即为学术成果；CCIA为加分项非必要条件 |
| **R9** | 可选验证流片失败 | 中 | 低 | **流片不依赖核心验收**；V3核心交付均在FPGA上 |
| **R10** | 不可抗力致实验室中断 | 低 | 高 | FPGA开发可远程；关键板卡提前备件；6个月缓冲 |

---

# 第十二部分：预期效益与战略意义

## 12.1 科学价值——推动计算架构范式跃迁

**范式级贡献**：本项目将为"拓扑中心计算（TCC）"范式提供全球首个系统性工程验证。如果成功，其科学意义可类比1945年ENIAC对"存储程序"概念的验证——以原型系统证明新范式可行，为后续大规模实现奠定基础。

**理论突破**：
- Route-Transform分解定理（Theorem 1）的实验验证，将"通信"与"计算"这对传统上割裂的概念在数学层面统一
- Route-Transform同构定理（Theorem 2）——8对同构映射的FPGA实证，开辟"拓扑-算法联合设计"新方向
- TCC-11原语完备性定理（Theorem 3）的7场景覆盖验证，证明11个原语构成分布式计算的完备基底

**学术影响**：预期在体系结构四大顶会（ISCA/HPCA/MICRO/ASPLOS）和信号处理顶刊（IEEE TSP）发表论文≥5篇，推动TCC范式进入主流学术议程。

## 12.2 技术价值——建立自主标准与原语IP体系

**TCC-Link标准**：国内首个原生支持拓扑可重构指令集（TR-ISA）的芯粒互连标准。策略性选择L1/L2兼容UCIe（降低产业采纳门槛），L3/L4实现范式级创新（抢占下一代言片互连标准话语权）。

**"3+1"验证IP核库**：经FPGA充分验证的tcc.FUSE/GEMM/MAPS/LINK四个原语级IP核，RTL质量达到直接迁移至28nm ASIC的成熟度。开源≥20K行SystemVerilog代码。

**TCCL兼容层**：NCCL/MPI/Gloo/FFTW多API兼容，PyTorch/TensorFlow/JAX/MATLAB零修改对接——证明TCC可无缝嵌入现有AI和信号处理生态。

## 12.3 产业价值——为SDSoW建立技术底座

| 阶段 | 产出 | 预期影响 |
|------|------|---------|
| 项目期内 | NCC-Edge液态硬件原型 + TCC-Link v1.0 | 吸引后续流片/产业化投资 |
| 项目结束后1年 | 基于验证IP的28nm ASIC（扩展至TCC-11全集） | TRL-5 |
| 项目结束后2年 | NCC-Edge-ASIC产品原型 + 孵化公司 | 端侧AI推理/DBF双模市场 |
| 远期 | SDSoW晶圆级液态硬件 | 下一代计算架构基础设施 |

**目标市场**：边缘AI推理芯片市场预计2030年达$50B+。TCC差异化切入：L4自动驾驶感知融合、智能安防多路视频分析、相控阵雷达/通信一体化。

## 12.4 人才培养

- 博士后：2名（TCC理论 + TCC-Link标准）
- 博士：4名（体系结构2+集成电路2）
- 硕士：8名（RTL/验证/软件/应用各2）
- 企业联合：华为昇腾、中芯国际联合培养通道

## 12.5 战略意义——"跟跑→并跑→领跑"

本项目是海河实验室"软件定义晶上系统（SDSoW）"战略方向的先导项目。承担三大使命：

1. **探路者**：用最低风险的FPGA方式验证SDSoW核心理论（TCC）和核心标准（TCC-Link）
2. **播种者**：输出开源IP核库、SDK和验证数据集，成为SDSoW生态"种子"
3. **架桥者**：建立"理论→原型→产业化"完整通路

**一句话概括**：本项目如果成功，中国将在"软件定义互连"这一下一代计算架构的战略制高点上，完成从"跟跑"（兼容UCIe）到"并跑"（TCC-Link标准）再到"领跑"（TCC范式定义权）的关键一步。

---

# 第十三部分：与项目指南的对齐声明

本申报书（V3·TCC战略版）严格对齐海河实验室2026年度重大专项指南（正式发布版）中关于"晶上网络中心计算范式架构研究与端侧原型验证"的全部要求：

| 指南核心要求 | V3响应 | 对齐程度 |
|------------|--------|---------|
| **液态硬件FPGA原型验证** | FPGA唯一验证载体；可选流片为锦上添花 | ✅ 完全对齐 |
| **兼容并超越UCIe的互连标准** | TCC-Link: L1/L2兼容UCIe 2.0 + L3(TR-ISA)/L4(原语事务)颠覆创新 | ✅ 完全对齐 |
| **"3+1"极简MVP架构** | tcc.FUSE + tcc.GEMM + tcc.MAPS + tcc.LINK | ✅ 完全对齐（TCC-11命名） |
| **计算与信号处理双场景验证** | 场景A(AI推理) + 场景B(DBF+同构演示) + 场景C(切换压测1000次) | ✅ 超出 |
| **NCCL/CUDA生态适配** | TCCL兼容层: NCCL/MPI/Gloo/FFTW全API兼容 | ✅ 超出 |
| **开源生态与孵化基础** | ≥20K行RTL + SDK + CI/CD + DSE工具 + 社区运营 | ✅ 完全对齐 |
| **经费2000万元** | 详列人员(800万)/平台(300万)/EDA(300万)/流片(200万)/软件(200万)/交流(200万) | ✅ 完全对齐 |
| **SDSoW先导与奠基** | 明确定位为SDSoW战略先导，Phase 1→2→3三阶段演进 | ✅ 战略级对齐 |

---

# 参考文献

1. Luo, M. et al. "SHARP: Scalable Hierarchical Aggregation and Reduction Protocol." *SC ''17*, 2017.
2. Hoefler, T. et al. "SparCML: High-Performance Sparse Communication for Machine Learning." *SC ''19*, 2019.
3. Sapio, A. et al. "Scaling Distributed Machine Learning with In-Network Aggregation." *NSDI ''21*, 2021.
4. Hammoud, M. et al. "MaPU: A Novel Mathematical Computing Architecture." *HPCA ''16*, 2016.
5. Vahdat, A. et al. "A Look at Network Topology Choices in Data Centers." *NSDI ''09*, 2009.
6. Liu, Q. et al. "Route-Transform Decomposition: Toward a Unified Theory of Communication and Computation in Distributed Systems." iNEST Technical Report, 2026.
7. Liu, Q. et al. "Route ≡ Transform: On the Structural Isomorphism of Communication and Computation." iNEST Technical Report, 2026.
8. Liu, Q. et al. "TCC-11 Primitive Library v1.0: A Complete Specification for Topology-Centric Computing." iNEST Technical Report, 2026.
9. UCIe Consortium. "Universal Chiplet Interconnect Express (UCIe) 2.0 Specification." 2024.
10. Rocki, K. et al. "Cerebras WSE-3: 4 Trillion Transistor Wafer-Scale Engine." *Hot Chips ''24*, 2024.
11. NVIDIA Corporation. "GB300 NVL72: NVLink 5 and NVSwitch 4 Architecture." Whitepaper, 2025.
12. Groq Inc. "Language Processing Unit: Deterministic Tensor Streaming Architecture." Whitepaper, 2024.
13. SambaNova Systems. "SN40L: Reconfigurable Dataflow Architecture." Whitepaper, 2023.

---

**项目负责人签字：刘勤让**

**申报单位公章：天津大学微电子学院**

**申报日期：2026年6月**


---

**Tags:** #NaaS #StrategicProposal #TCC #SDSoW #SDI #FPGA #LiquidHardware #Chiplet #TCC-11

## Related Notes

- [[[V8]_海河实验室_项目指南_晶上拓扑中心计算_正式发布版]]
- [[TCC 原语库 v1.0 最终版规范]]
- [[B4_Route_IS_Transform_Isomorphism_Draft]]
- [[iNEST 国家重大专项项目布局 · 双轨战略框架]]
- [[路由即变换——分布式系统中通信与计算的结构同构性]]
- [[TCC_Core_Concepts]]
