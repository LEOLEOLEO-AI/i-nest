---
direction: both
category: 理论
tags: [network-centric-computing, route-transform, topology, primitive-library, paradigm]
summary: "网络中心计算范式主索引，拓扑即计算，Route≡Transform定理体系。"
quality: high
processed: 2026-09-04 08:16
---
---
title: "【iNEST知识库】NCC_Paradigm_Master_Index"
tags:
  - green-ai
  - research
  - top-journal
  - energy
  - sdi-bond
  - architecture
  - network
  - emergence
  - design
  - fpga
  - physics
  - hardware
  - first-principles
  - paper
  - criticality
date: 2026-08-31 07:23
source: GetNotes
score: 31
---

## Original Note

【iNEST知识库】NCC_Paradigm_Master_Index

# 网络中心计算（NCC）范式——研究主索引与任务列表
# Network-Centric Computing Paradigm — Master Index & Task Board
#
# 创建：2026-04-20
# 维护：iNEST课题组
# 路径：00_KnowledgeBase_知识库/02_CST_核心理论著作/NCC_Paradigm_Master_Index.md

---

## 一、范式定位

**核心命题**：物理拓扑即计算。在分布式系统中，通信操作（Route）与计算操作（Transform）存在结构同构关系——这不是工程技巧，是可以严格证明的数学事实。

**第三计算范式**：
```
第一范式：冯·诺依曼 (1945)   — 串行指令流 + 存储器分离
第二范式：Dataflow/并行计算   — 数据驱动 + 众核并行
第三范式：NCC (iNEST, 2026)  — 拓扑即计算，通信与计算统一
```

**护城河**：Route≡Transform 定理（数学证明）→ NCC-11 原语集（代数完备）→ SDI 硬件（微秒级重构）→ 液态切换（跨场景零切换成本）

---

## 二、知识库文件地图

### 2.1 理论基础

| 文件 | 内容 | 状态 |
|------|------|------|
| `NCC_Core_Concepts.md` | 第一性原理、元拓扑、SDI-Bond代数、CST锚点 | ✅ 已建立 |
| `NCC_Naming_Convention_v2.md` | **NCC-11原语命名规范 v2.0（权威版）** | ✅ 已建立 |
| `NCC_Naming_Convention_v1.md` | NCC-8规范（已废止，仅供历史参考） | ⚠️ 已废止 |

### 2.2 专利文件（→ `02_Papers_论文/00_专利清单.md`）

| 代号 | 名称 | 状态 |
|------|------|------|
| **P1** | 基于SDI拓扑重构的NCC方法与系统（核心方法专利） | 📋 框架完成，待精细化 |
| **P2** | 可重构原语硬件IP核阵列（硬件架构专利） | 📋 框架完成，待精细化 |
| **P3** | 基于拓扑重构的FFT方法与DBF应用（FFT同构专利） | 📋 框架完成 |
| **P4** | NCC原语到NCCL/MPI/BLAS编译映射方法（SDK专利） | 📋 框架完成 |

### 2.3 论文文件（→ `02_Papers_论文/B组_SDI-CC互连体系/`）

| 论文 | 标题 | 目标 | 状态 |
|------|------|------|------|
| **论文A（B7）** | *Route≡Transform: A Unified Algebraic Theory...* | ASPLOS'27 Sep | 📋 框架完成，待写作 |
| **论文B（B5）** | *NCC-11: A Minimal Complete Primitive Library...* | ASPLOS/MICRO'27 | 📋 框架完成，待RTL实验数据 |
| **论文C（B3）** | *From Horowitz Wall to Topology Computing...* | Nature Electronics | 📋 框架完成，待论文A/B完成后 |
| B2 | P-Mapping：原语完备性 | IEEE TPDS | 📋 素材V3完备 |

### 2.4 工程文件

| 文件 | 内容 |
|------|------|
| `B7_Route-Transform_素材_V1.md` | B7论文四定理体系、场景映射、投稿策略 |
| `B2_P-Mapping_素材_V3.md` | 原语完备性证明、Γst(O,C)框架 |
| `[V3] P-Mapping_论文全文_IEEE_TPDS.md` | B2论文全文 |
| `[V1]_P-Paradigm_NatureElectronics_综述大纲_Liquid_OODA.md` | B3论文大纲 |

---

## 三、核心理论框架速查

### 3.1 Route≡Transform 四定理体系

| 定理 | 陈述摘要 | 证明方法 | 对应专利 |
|------|---------|---------|---------|
| **定理1**（分解） | 任意分布式计算 C = T_m∘R_m∘…∘T_1∘R_1 | BSP构造性分解 | P1权利要求1 |
| **定理2**（同构） | FFT蝶形图 ≅ Butterfly-AllReduce通信图（图同构） | Cooley-Tukey vs 超立方体维度有序AllReduce | P1权利要求2, P3权利要求1 |
| **定理3**（完备） | NCC-11在7类目标工作负载上100%覆盖 | 对每类构造显式原语映射 | P1权利要求1, P4 |
| **定理4**（能效） | Route-Transform融合使等效通信量从O(N·D)降至O(D) | Horowitz能耗模型定量推导 | P1 |

### 3.2 NCC-11 原语集（完整版）

$$\text{NCC-11} = \{\underbrace{\text{FUSE, PULL, CAST, SWAP}}_{\text{通信×4}}, \underbrace{\text{GEMM, FOLD, MAPS, SCAN}}_{\text{计算×4}}, \underbrace{\text{MOVE}}_{\text{数据×1}}, \underbrace{\text{LINK, TICK}}_{\text{控制×2}}\}$$

**关键代数关系**：
```
FUSE(x,op) ≡ FOLD(PULL(x), op)     [AllReduce = AllGather + local Reduce]
SCAN(x,op) ≢ 任意O(log N)的{FUSE,PULL,CAST,FOLD}组合  [不可替代！]
SWAP(x)    ≢ 任意O(N)的{FUSE,PULL,CAST}组合           [不可替代！]
MOVE(x,s,d) ≡ SWAP(x·mask(s,d))   [P2P=sparse AlltoAll，但能耗N×]
```

### 3.3 三场景同构核心对照

| 场景 | 计算操作 | 通信操作 | NCC实现 | 拓扑 |
|------|---------|---------|---------|------|
| FFT（雷达/通信） | 蝶形运算 | AllReduce（维度有序） | MAPS+FUSE | Butterfly |
| MoE推理（AI） | 专家选择+分发 | AlltoAll | SWAP | Crossbar |
| CFAR（雷达检测） | 滑窗前缀和 | Scan（前缀归约） | SCAN | Linear Chain |
| 注意力（AI） | QK^T+V | AllGather(K)+本地GEMM | PULL+GEMM | Star→Local |
| SpMV（HPC） | 稀疏矩阵×向量 | 图着色+Scatter/Gather | FOLD+MAPS | 原始图拓扑 |

---

## 四、任务列表（Task Board）

> 优先级：🔴 立即启动 | 🟡 本月内 | 🟢 本季度 | ⬜ 待排期

### T0：知识产权（最高优先级——专利先于论文公开）

- [🔴] **T0-1** 精细化 P1 权利要求书：独立权利要求1（方法类）+ 权利要求7（系统类）+ 权利要求10（兼容层类），确保保护范围最大化
  - 先行排除分析：NVIDIA SHARP US11645534B2（仅覆盖"triggered AllReduce offload"），Google光互连EP2025（仅覆盖"reconfigurable pods via optical"）——两者均不涉及通用原语集和拓扑重构等价性
  - 目标：**2026年5月提交CNIPA**（在论文A投稿前）
- [🔴] **T0-2** 精细化 P2 权利要求书（硬件IP核阵列），目标 **2026年7月提交**
- [🟡] **T0-3** P3（FFT同构）撰写与提交，目标 **2026年12月**
- [🟡] **T0-4** P4（SDK编译映射）撰写与提交，目标 **2027年1月**
- [🟢] **T0-5** P1 PCT国际申请（12个月窗口），目标 **2027年5月前**

### T1：论文A——Route≡Transform理论核心（B7）

- [🔴] **T1-1** 完成 §3.2 Lemma 2a（FFT-Butterfly同构严格证明）：比较Cooley-Tukey蝶形图与超立方体维度有序AllReduce的节点连接矩阵，证明图同构
- [🔴] **T1-2** 完成 §3.4 定理3完备性证明：为7类工作负载逐一构造原语分解映射，整理成覆盖矩阵表格
- [🟡] **T1-3** 完成 §3.5 定理4最小性下界论证（SWAP/SCAN/MOVE各自的Ω(N)退化证明）
- [🟡] **T1-4** 完成 §3.3 Lemma 2b（AlltoAll-Transpose）和 Lemma 2c（Scan-Pipeline）
- [🟡] **T1-5** 撰写 §1 Introduction 和 §2 Background（2页，含Horowitz数据引用）
- [🟢] **T1-6** 整合 §5 Hardware Prototype 和 §6 Evaluation（依赖FPGA实验数据）
- [🟢] **T1-7** 投稿 ASPLOS'27 Sep cycle，**截止：2026年9月9日**

### T2：RTL硬件IP核实现

- [🔴] **T2-1** 设计并实现 `ncc_link` IP核（SDI控制器：交叉开关+连接矩阵寄存器，配置延迟≤100ns）——**所有IP核的基础，最高优先**
- [🔴] **T2-2** 实现 `ncc_fuse` IP核（AllReduce，Butterfly/Ring双拓扑，支持SUM/MAX/MIN）
- [🔴] **T2-3** 实现 `ncc_gemm` IP核（脉动阵列，M≥8×K≥8，INT4/INT8/FP16/BF16）
- [🔴] **T2-4** 实现 `ncc_maps` IP核（逐元素+可编程LUT，深度≥256，支持ReLU/GELU/SiLU/旋转因子）
- [🟡] **T2-5** 实现 `ncc_scan` IP核（Brent-Kung或Kogge-Stone前缀树，inclusive/exclusive可配）
- [🟡] **T2-6** 实现 `ncc_fold` / `ncc_pull` / `ncc_cast` / `ncc_swap` IP核
- [🟡] **T2-7** 实现 `ncc_move` / `ncc_tick` IP核
- [🟢] **T2-8** 4节点VCK190板级集成，GTY 25.78 Gbps板间互连调试
- [🟢] **T2-9** 三场景实验数据采集：1024点FFT延迟（目标800ns）、Gemma-4推理（目标5.2tok/s）、场景切换（目标<1μs）

### T3：SDK开发

- [🟡] **T3-1** Python功能仿真器 `ncc-sim v0.1`（NumPy实现11原语全覆盖，`import ncc`直接调用，无需硬件）
- [🟡] **T3-2** `ncc.compat.nccl`模块：注册为PyTorch c10d后端，验证标准DDP训练脚本零修改运行
- [🟢] **T3-3** NCC MLIR Dialect定义（TableGen，含11种操作类型）+ StableHLO lowering pass
- [🟢] **T3-4** Graph Compiler三个pass：拓扑自动插入、原语融合（softmax/layernorm/flash_attn模式）、内存规划
- [🟢] **T3-5** VCK190 HAL驱动层（AXI寄存器映射、DMA引擎、中断处理）
- [⬜] **T3-6** `ncc.compat.mpi` 模块（MPI-4.0 collective子集）
- [⬜] **T3-7** `ncc.compat.blas` + `ncc.compat.fftw` 映射层

### T4：论文B——NCC-11系统实现与评测（B5）

- [🟢] **T4-1** 撰写 §3 Hardware Architecture（依赖T2完成后提取微架构数据）
- [🟢] **T4-2** 撰写 §4 SDK and Compilation Flow（依赖T3-1至T3-4）
- [🟢] **T4-3** 撰写 §5 Evaluation（依赖T2-8/T2-9实测数据）
- [⬜] **T4-4** 投稿 ASPLOS'27 Apr cycle（截止2027年4月15日）或 MICRO'27

### T5：论文C——Nature Electronics综述（B3）

- [🟢] **T5-1** 撰写 §1 Horowitz Wall（已有引用，需整理成NE格式，~1500字）
- [⬜] **T5-2** 撰写 §5 Scaling Roadmap四阶段定量推导（FPGA→28nm→7nm→晶圆级）
- [⬜] **T5-3** 撰写 §6 Landauer极限比较（kT·ln2定量计算，证明还有~10^7×空间）
- [⬜] **T5-4** 投稿 Nature Electronics（2027年9月，在论文A/B发表后）

### T6：B2 P-Mapping论文推进

- [🟡] **T6-1** 运行 `collective_comm_sim_v2.py` 获取6类原语实际Γst测量值（T_overlap/T_total）
- [🟡] **T6-2** 基于 `B2_P-Mapping_素材_V3.md` 完成正式论文各节撰写
- [🟢] **T6-3** 投稿 IEEE TPDS 或 ICS'27

---

## 五、里程碑时间线

```
2026年
──────────────────────────────────────────────────────────
Q2 (4-6月)           Q3 (7-9月)          Q4 (10-12月)
│                    │                   │
├─ P1专利提交(5月)    ├─ P2专利提交(7月)  ├─ P3专利提交(12月)
├─ T1-1,2开始        ├─ T2-1~4完成       ├─ T3-1,2完成
├─ T2-1启动(ncc_link)├─ T1-1~5完成       ├─ T1-6整合FPGA数据
│                    ├─ 论文A投ASPLOS'27  └─ T6-1 Γst仿真
│                    │  Sep(9月9日)
│                    └─ T3-1启动

2027年
──────────────────────────────────────────────────────────
Q1 (1-3月)           Q2 (4-6月)          Q3 (7-9月)
│                    │                   │
├─ P4专利提交(1月)    ├─ 论文B投ASPLOS'27 ├─ 论文C投
├─ T2-8 板级集成      │  Apr(4月15日)     │  Nature Electronics
├─ T4-1,2撰写        ├─ P1 PCT申请       ├─ 论文A预期发表
└─ T5-1撰写          └─ T3-3~5完成       └─ 全栈开源准备
```

---

## 六、深入研究起点——待展开的开放问题

以下问题是从当前框架自然涌现的研究方向，每一个都可以展开为独立的研究分支或论文：

### 6.1 理论深化方向

**Q1：拓扑选择的计算复杂度**
给定工作负载的原语调用序列，求最优拓扑切换方案（最小切换次数 + 最小通信延迟）是 NP-hard 还是多项式可解？
- 初步猜想：对固定拓扑库（ring/butterfly/crossbar/tree）是多项式的，对任意拓扑是NP-hard
- 研究路径：转化为带约束的最短路问题或图着色问题

**Q2：Route≡Transform 的反向设计**
能否从"我需要什么计算"反推"我需要什么通信协议"？即 Transform→Route 的逆映射是否总是存在且唯一？
- 初步猜想：唯一性不成立（FFT可以用多种拓扑实现），但最优映射在能效意义下是唯一的
- 研究路径：定义"拓扑等价类"，研究商群结构

**Q3：TICK的最小性**
TICK 的存在是否真的必要？即 GALS 系统中，能否仅用 LINK.barrier() 代替显式逻辑时钟？
- 初步答案：barrier() 解决同步，TICK 解决因果序（不同），对数据依赖关系的追踪必须有 TICK
- 研究路径：构造反例，展示无 TICK 时分布式 SCAN 的结果不确定性

**Q4：NCC-11 的量子扩展**
量子纠错码的稳定器电路是否也满足 Route≡Transform 结构？即量子纠缠 = 量子通信 + 量子门的某种同构？
- 与量子计算的接口：SWAP 门是量子计算的通信原语，Hadamard/CNOT 是计算原语，两者的拓扑关系有待研究

### 6.2 工程深化方向

**Q5：MAPS 的 LUT 动态重加载延迟**
权利要求书承诺 LUT 重加载 ≤100 个时钟周期。实际测量是多少？能否进一步降低到 10 个周期？
- 关键路径：LUT SRAM 的多端口读写时序，写使能信号的 setup/hold 约束

**Q6：ncc_link 的交叉开关面积**
N=16 节点的 16×16 交叉开关在 TSMC 7nm 下的面积是多少？是否超过 1mm²（超过则需要考虑分层拓扑）？
- 估算：1×1 交叉点 ~0.5-1 μm²，256 个交叉点 ~256 μm²，加上信号缓冲约 ~0.5mm²，可接受

**Q7：VCK190 AI Engine 与 NCC IP 核的协同**
VCK190 的 AI Engine 

…（内容已截断，完整版见Obsidian）

Tags: 
Source: openapi

---

## Related Notes

[[自组织临界态SOC]]
[[Papers-MOC]]
[[FPGA原型]]
[[paper1_iNEST_core_architecture]]
[[SDI化合物键_四型架构]]
[[iNEST-MOC]]
[[paper2_liquid_computing_chemistry]]
