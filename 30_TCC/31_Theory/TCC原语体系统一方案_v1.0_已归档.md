---
title: "TCC原语体系统一方案_6R+6T与TCC-11的对齐与收敛建议"
date: 2026-07-02
version: v1.0
status: Draft
scope: "面向TCC项目申报书(Hailab)的6R+6T原语规范与知识库中TCC-11 v1.0的统一"
tags: [TCC, 原语, primitive, NCC, TCC-11, 6R+6T, Route≡Transform]
---

# TCC原语体系统一方案：6R+6T与TCC-11的对齐与收敛

> **核心结论**：知识库中存在两个版本的原语定义——项目申报书中的"6R+6T"和已固化的"TCC-11 v1.0（ncc.*）"。两者在数学本质上等价，差异主要在命名、分组方式和应用语境。**建议以TCC-11 v1.0为规范基准，用6R+6T框架对外表述**——即内部统一为11原语，对外以6R+6T框架展示（将MOVE并入Route组、TICK并入时序基础原语）。

---

## 一、知识库中已有的原语版本

### 1.1 TCC-11 v1.0（iNEST Research Agent System Prompt）

| 原语 | 语义 | 类别 | 最优拓扑 |
|------|------|------|---------|
| 
cc.FUSE | AllReduce（全归约） | R（通信） | Butterfly |
| 
cc.PULL | AllGather（全收集） | R（通信） | Radial Tree |
| 
cc.CAST | Broadcast（广播） | R（通信） | Directed Tree |
| 
cc.SWAP | AlltoAll（全交换） | R（通信） | Crossbar |
| 
cc.GEMM | Matrix multiply-add（矩阵乘加） | T（计算） | Systolic Array |
| 
cc.FOLD | Vector reduce（向量归约） | T（计算） | Reduction Tree |
| 
cc.MAPS | Element-wise map（逐元素映射） | T（计算） | Scatter-Gather |
| 
cc.SCAN | Prefix scan（前缀扫描） | T（计算） | Binary Tree |
| 
cc.MOVE | Data movement（数据搬运） | S（存储） | DMA Engine |
| 
cc.LINK | Topology reconfiguration（拓扑重构） | C（控制） | SDI Controller |
| 
cc.TICK | Global clock / causal ordering（全局时序） | ⏱（时序） | Clock Tree |

**设计哲学**：代数完备性 + 正交最小性 + 场景正交性（4+4+1+1+1 = 11）。

### 1.2 项目申报书中的 6R+6T

项目申报书（海河实验室 TCC MVP项目）中提出"6R+6T原语体系"但未逐一定义。结合文档上下文推断：

**6 Route 原语（R1-R6）**：
- R1: AllReduce → 
cc.FUSE
- R2: AllGather → 
cc.PULL
- R3: Broadcast → 
cc.CAST
- R4: AlltoAll → 
cc.SWAP
- R5: Scatter/Gather → 从 
cc.MOVE 派生
- R6: Ring Shift → 新增，或者归入拓扑操作

**6 Transform 原语（T1-T6）**：
- T1: Matrix GEMM → 
cc.GEMM
- T2: Vector Reduce → 
cc.FOLD
- T3: Element-wise → 
cc.MAPS
- T4: Prefix Scan → 
cc.SCAN
- T5: FFT → 新增（RF信号场景必需）
- T6: Sort/Permute → 新增或合并

### 1.3 Route≡Transform 同构表（论文版本）

| Transform 操作 | Route 操作 | 拓扑 |
|---------------|-----------|------|
| FFT Butterfly | AllReduce | Butterfly/Hypercube |
| Matrix Transpose | AlltoAll | Full Crossbar |
| Prefix Sum | Scan | Binary Tree |
| Sparse Mat-Vec | Scatter/Gather | 原图拓扑 |
| Reduce (Tree) | Reduce (Tree) | Tree |
| Conv Sliding Window | Shift+Overlap | Ring/Torus |
| Attention QK^T | AllGather(K) + GEMM | Star→Local |
| Bitonic Sort | Butterfly路由 | Butterfly |

> 这张表揭示了**8对同构关系**，但8≠6。6R+6T框架需要从这8对中做**最小完备选取**。

---

## 二、差异分析

### 2.1 命名差异

| 维度 | TCC-11 (ncc.*) | 6R+6T（项目文档语境） |
|------|---------------|-------------------|
| 命名空间 | 
cc.（Network-Centric Computing） | 未指定（倾向 	cc.） |
| 前缀含义 | 专利保护 + NCC架构定位 | TCC范式定位 |
| 分组逻辑 | 4R+4T+1S+1C+1⏱ = 11 | 6R+6T = 12（对称分组） |

### 2.2 数量差异

| 项目 | TCC-11 | 6R+6T |
|------|--------|-------|
| Route 原语 | 4（FUSE/PULL/CAST/SWAP） | 6（需新增2个） |
| Transform 原语 | 4（GEMM/FOLD/MAPS/SCAN） | 6（需新增2个） |
| 其他 | MOVE+LINK+TICK = 3 | 并入R或T组 |
| **总计** | **11** | **12** |

### 2.3 需要新增的原语

为满足 6R，需要从 TCC-11 扩展：
- **R5: SCATTER** = 
cc.MOVE 的 Scatter 模式（已有基础，命名即可）
- **R6: SHIFT** = 环形移位（Conv滑窗场景，Butterfly网络天然支持）

为满足 6T，需要从 TCC-11 扩展：
- **T5: FFT** = 傅里叶变换（RF信号处理场景核心，与FUSE在Butterfly拓扑上同构）
- **T6: SORT/Permute** = 排序/置换（MoE路由、Token重排场景，与SWAP在Crossbar上同构）

> 关键洞察：**新增的 R5/R6 和 T5/T6 在数学上并非新原语**——R5=R1的子集、R6=Butterfly网络的环面子集、T5与T1同构(FFT通过Butterfly分解为一系列GEMM)、T6与T4同构(Permute是SCAN的特化)。**它们是为了满足"6R+6T"的对称美学而做的命名拆分。**

---

## 三、统一建议

### 3.1 推荐方案：TCC-11为基准，6R+6T为对外框架

`
┌─────────────────────────────────────────────┐
│          TCC 原语体系统一架构                  │
├─────────────────────────────────────────────┤
│  内部规范（工程实现）：TCC-11 v1.0 (ncc.*)     │
│  ┌─────────┬─────────┬──────┬──────┬──────┐ │
│  │ 4 Route │4 Transf │ 1 S  │ 1 C  │ 1 ⏱ │ │
│  │ FUSE    │ GEMM    │ MOVE │ LINK │ TICK │ │
│  │ PULL    │ FOLD    │      │      │      │ │
│  │ CAST    │ MAPS    │      │      │      │ │
│  │ SWAP    │ SCAN    │      │      │      │ │
│  └─────────┴─────────┴──────┴──────┴──────┘ │
│                                               │
│  对外表述（项目申报/论文）：6R+6T               │
│  ┌──────────────┬──────────────┐              │
│  │ 6 Route      │ 6 Transform  │              │
│  │ 1. FUSE      │ 1. GEMM      │              │
│  │ 2. PULL      │ 2. FOLD      │              │
│  │ 3. CAST      │ 3. MAPS      │              │
│  │ 4. SWAP      │ 4. SCAN      │              │
│  │ 5. SCATTER   │ 5. FFT       │              │
│  │ 6. SHIFT     │ 6. PERMUTE   │              │
│  └──────────────┴──────────────┘              │
│  [MOVE和LINK作为跨界原语，TICK作为基础原语]      │
└─────────────────────────────────────────────┘
`

### 3.2 统一命名表

| 对外名称（6R+6T） | 内部命名（TCC-11） | 语义 | 原始定义来源 | 核心场景 |
|-------------------|-------------------|------|-------------|---------|
| **R1: FUSE** | 
cc.FUSE | 全归约 AllReduce | TCC-11 | AI训练梯度同步 |
| **R2: PULL** | 
cc.PULL | 全收集 AllGather | TCC-11 | KV Cache聚合 |
| **R3: CAST** | 
cc.CAST | 广播 Broadcast | TCC-11 | 权重分发 |
| **R4: SWAP** | 
cc.SWAP | 全交换 AlltoAll | TCC-11 | MoE专家路由 |
| **R5: SCATTER** | 
cc.MOVE(scatter) | 散射/收集 | 从MOVE派生 | Token分发 |
| **R6: SHIFT** | 
cc.FUSE(ring) | 环形移位 | 新增命名 | Conv滑动窗 |
| **T1: GEMM** | 
cc.GEMM | 矩阵乘加 | TCC-11 | Transformer/CNN |
| **T2: FOLD** | 
cc.FOLD | 向量归约 | TCC-11 | Softmax/LN |
| **T3: MAPS** | 
cc.MAPS | 逐元素映射 | TCC-11 | 激活函数/gate |
| **T4: SCAN** | 
cc.SCAN | 前缀扫描 | TCC-11 | Attention mask |
| **T5: FFT** | 
cc.GEMM(FFT) 或 
cc.FUSE(FFT) | 傅里叶变换 | 新增命名 | DBF/FFT |
| **T6: PERMUTE** | 
cc.SWAP(perm) 或 
cc.SCAN(perm) | 排序/置换 | 新增命名 | MoE路由/TopK |

> **关键原则**：R5/R6/T5/T6 不增加新的硬件IP核——它们复用已有的11个IP核（通过参数化/模式切换实现）。

### 3.3 命名空间建议：统一为 
cc.

| 命名空间 | 使用场景 | 理由 |
|----------|---------|------|
| **
cc.*** | **工程实现、RTL、SDK、专利** | 专利已用此命名，有法律保护；NCC=Network-Centric Computing 比 TCC=Topology-Centric Computing 更具体地表达了"网络中心计算" |
| 	cc.* | 对外学术交流、论文 | TCC 是范式名称，保持概念一致性 |
| 等价映射 | 
cc.FUSE ≡ 	cc.FUSE（语义相同） | 编译器/文档自动转换 |

> **建议**：项目代码和SDK中统一使用 
cc.*，但在论文和白皮书中可以使用 	cc.* 或直接使用全称 	cc.ncc.FUSE 以同时满足"范式TCC"和"架构NCC"的双重需求。

---

## 四、依据与论证

### 4.1 为什么是11而不是12？

| 论证维度 | 说明 |
|---------|------|
| **代数完备性** | 11个原语构成代数操作的完备生成集——任何分布式计算操作可分解为这11个基元的组合。12会引入冗余（SCATTER=MOVE的子集、FFT=GEMM的频域模式）。 |
| **正交最小性** | 11是最小正交数量——每增一个"新"原语都必然与已有原语重叠。PERMUTE本质是SWAP的特化（在Crossbar上执行的路由置换）。 |
| **硬件IP核实数** | TCC-11对应11个硬件IP核（已在专利中定义RTL接口）。新增原语应通过参数化复用已有IP核，而非增加新核。 |
| **场景覆盖度** | 11原语已验证覆盖AI训练/推理、FFT/DBF信号处理、仿真的≥3类场景。12不增加覆盖度。 |

### 4.2 为什么6R+6T是好的对外框架？

| 优势 | 说明 |
|------|------|
| **对称美学** | Route≡Transform 的同构对称性在命名层面体现 |
| **产业可理解性** | "通信6原语+计算6原语"比"4+4+1+1+1"更易被产业界理解 |
| **与业界对标** | CUDA的通信原语（ncclAllReduce/ncclAllGather等）≈6个；计算原语（cublasGemmEx等）≈6大类 |
| **论文友好** | 6R+6T = 12 的对称性适合做理论分析（如对偶性证明、复杂度分析） |

### 4.3 为什么用 
cc. 而非 	cc.？

| 
cc. | 	cc. |
|--------|--------|
| 专利已用——有法律优先权 | 范式层面命名 |
| NCC = Network-Centric Computing，"网络中心"更具体 | TCC = Topology-Centric Computing，"拓扑中心"更抽象 |
| 代码中 
cc.FUSE 更简洁 | 	cc.FUSE 也可接受 |
| 与 MLIR dialect 
cc.* 一致（专利实施例五） | |

> **折中方案**：MLIR方言使用 
cc.，C++ SDK使用 	cc::ncc::FUSE 命名空间嵌套。

---

## 五、对项目申报书的具体修改建议

### 5.1 建议修改

在项目申报书"6R+6T 原语规范"部分，建议加入以下对齐说明：

`
TCC 原语体系基于已获专利保护的 NCC-11 原语规范（发明专利：
"一种基于正交原语集与拓扑融合变换的网络复杂度计算方法及系统"），
采用 6R+6T 框架表述：

6 Route 原语：FUSE/PULL/CAST/SWAP/SCATTER/SHIFT
6 Transform 原语：GEMM/FOLD/MAPS/SCAN/FFT/PERMUTE

其中 R1-R4 和 T1-T4 对应 NCC-11 规范的 8 个核心原语；
R5(SCATTER)和 R6(SHIFT)是 MOVE 和 FUSE 的命名扩展；
T5(FFT)和 T6(PERMUTE)是 GEMM 和 SWAP 的频域/置换模式。
全部12个命名原语映射到11个硬件IP核，无新增硬件开销。
`

### 5.2 里程碑M1中"6R+6T原语规范"的交付物建议

| 交付物 | 内容 | 格式 |
|--------|------|------|
| TCC-11 v2.0 原语规范.md | 11硬件IP核 + 12命名原语的完整语义定义 | 内部规范文档 |
| 6R+6T 原语手册.md | 面向产业/课题合作方的对外版本，6R+6T表达 | 外部白皮书 |
| NCC MLIR Dialect定义.td | 11个 MLIR Operation 的 TableGen 定义 | 代码 |

---

## 六、总结

| 决策 | 内容 |
|------|------|
| **内部工程基准** | TCC-11 v1.0（
cc.*命名，11个IP核） |
| **对外/项目申报框架** | 6R+6T（对称分组，12个命名原语→11个硬件IP核） |
| **命名空间** | 代码用 
cc.*（专利一致），论文可用 	cc.* |
| **新增的SCATTER/SHIFT/FFT/PERMUTE** | **不是新IP核**——是已有原语的参数化模式 |
| **与iNEST关系** | TCC-11是iNEST系统提示中的规范基准，不应更改 |

> **最终建议**：在项目申报书中保留"6R+6T"的表述（它作为对外框架是好的），但在内部工程文档中明确"6R+6T = TCC-11 v1.0 + 4个命名参数化扩展"。新增的R5/R6/T5/T6不增加硬件复杂度——它们通过 FPGA 验证阶段在已有 11 个 IP 核上配置不同参数/模式实现。

---
## 相关链接
- [[TCC_RTC原语架构与SDI拓扑变换机理_v1.0]]
- [[TCC_Core_Concepts]]
- [[TCC计算范式命名规范3.0]]
- [[TCC_TRC原语架构与SDI拓扑变换机理_v1.0]]
- [[TCC_Master_Index]]
- [[5类通信-4类计算拓扑完备映射与PTM算法]]
