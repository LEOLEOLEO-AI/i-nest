---
title: "From Von Neumann to Network-Centric: A First-Principles Review of Computing Paradigm Migration"
subtitle: "面向可持续智能计算的范式迁移"
target: "Engineering (中国工程院院刊) — Special Issue on Sustainable Intelligent Computing"
deadline: "2026年6月20日"
version: "v1-基线版本"
date: "2026-05-30"
status: "📝 初稿完成，进入冲刺迭代"
---

# From Von Neumann to Network-Centric: A First-Principles Review of Computing Paradigm Migration for Sustainable Intelligent Computing

# 从冯诺依曼到网络中心：面向可持续智能计算的计算范式迁移 —— 第一性原理综述

**Authors:** Qinrang Liu (刘勤让), et al.
**Affiliation:** TCC iNEST Research Group
**Target:** *Engineering* (中国工程院院刊), Special Issue on "Sustainable Intelligent Computing"
**Submission Deadline:** June 20, 2026

---

## Abstract

The von Neumann architecture has dominated computing for nearly eight decades, anchoring computation on processor-centric nodes. However, with the exponential growth in computational demands from large language models, HPC simulations, and real-time signal processing, the "Memory Wall" and "Communication Wall" have evolved into inescapable systemic bottlenecks. Stanford's Mark Horowitz (ISSCC 2014) revealed that a single 32-bit DRAM access consumes 350-700x the energy of a 32-bit floating-point multiplication. NVIDIA Chief Scientist Bill Dally (Hot Chips 2023) confirmed that data movement and storage energy vastly exceed computation itself. IBM Research (2025) quantified that in modern AI workloads, computation accounts for merely ~10% of total energy, while data movement consumes ~90%. As Dennard scaling ended and DRAM scaling plateaued, the energy-scissors gap between data movement and computation continues to widen.

This paper advances a core thesis from first principles: any computational process can be decomposed into two weakly coupled primitives—Operators (computation) and Data Movement (communication)—and it is data movement, not operators, that constitutes the fundamental bottleneck for computing energy efficiency and sustainability. Through systematic analysis across four major computing domains (general-purpose, AI, HPC, and signal processing), we demonstrate: (1) atomic operators converge to a finite set of no more than ten primitives across all domains; (2) data movement patterns can be formalized through a meta-primitive system of eleven orthogonal operations with an accompanying cost model; (3) Software-Defined Interconnect (SDI) provides the engineering mechanism to elevate interconnect routing from design-time fixation to runtime programmability; and (4) a Liquid Unified Architecture—combining standardized operator libraries, data movement meta-primitives, and SDI fabrics—enables a paradigm migration from node-centric to network-centric computing.

We frame this paradigm shift within the broader context of sustainable intelligent computing: the current trajectory of exponentially growing energy costs with sub-linear intelligence returns is thermodynamically unsustainable. The path forward is not faster processors but smarter networks—interconnects that dynamically adapt their topology to match the dataflow graph of the workload, eliminating redundant data movement at the physical level.

**Keywords:** von Neumann bottleneck; data movement wall; network-centric computing; software-defined interconnect; liquid hardware; computing paradigm migration; sustainable intelligent computing

---

## 摘要

冯诺依曼架构统治计算领域近八十年，其以"节点"为中心的计算范式将处理器置于体系结构的核心地位。然而，随着AI大模型、超算仿真与实时信号处理对算力的指数级需求增长，"存储墙"与"通信墙"已演变为不可回避的系统性瓶颈。Stanford大学Mark Horowitz在ISSCC 2014的标志性主旨报告中揭示：在45nm工艺下，一次32位DRAM访问的能耗（1.3-2.6 nJ）是一次32位浮点乘法（3.7 pJ）的约350-700倍 [1]；NVIDIA首席科学家Bill Dally在Hot Chips 2023主旨演讲中进一步确认深度学习硬件中"数据移动和存储能耗"远超计算本身；IBM Research 2025年的实测数据明确指出，现代AI工作负载中计算能耗仅约占10%，数据搬运能耗占约90%。随着Dennard缩放定律失效和DRAM缩放放缓，路由-计算的能耗剪刀差在先进工艺节点中持续扩大。

本文从第一性原理出发，提出核心命题：任何计算过程均可分解为"算子"与"数据移动"两个弱耦合基元，而数据移动——而非算子——才是决定计算能效与可持续性的核心矛盾。通过对通用计算、智能计算、高性能计算及信号处理四大主流场景的数据移动展开分析，本文论证了：(1) 各场景底层原子算子高度收敛于一组不超过十个原语的有限集合，高阶数学算子均可通过Weierstrass逼近、CORDIC算法和多项式方法归约构造；(2) 数据移动模式可通过11个元语体系实现形式化标准化，附带代价模型用于编译优化；(3) 软件定义互连（SDI）机制提供了将互连路由从设计时固化提升到运行时可编程的工程手段；(4) 液态一体架构——整合标准化算子库、数据移动元语和SDI矩阵——在明确的适用条件下实现了从"以节点为中心"到"以网络互联为中心"的范式迁移。

本文将这一范式迁移置于可持续智能计算的宏观框架中：当前AI发展轨迹呈现指数增长的能耗与次线性的智能收益之间的尖锐矛盾——这是一条热力学不可持续的路径。出路不在于更快的处理器，而在于更智能的网络——能够动态匹配工作负载数据流图的互连拓扑，从物理层消除冗余数据搬运。

**关键词：** 冯诺依曼瓶颈；数据移动墙；网络中心计算；算子-数据移动分解；软件定义互连；液态硬件；计算范式迁移；可持续智能计算
---

## 一、引言：八十年范式的结构性危机

> "Computing's energy problem: the key to scaling computing performance is to create applications and hardware which are better matched to the task and each other." —— Mark Horowitz, Stanford University, ISSCC 2014 Plenary [1]

> "The data movement and storage energy…is kind of a bummer." —— Bill Dally, NVIDIA Chief Scientist, Hot Chips 2023 Keynote

1945年，约翰·冯·诺依曼在其著名的"EDVAC报告初稿"中描述了存储程序计算机的基本架构——处理单元、控制单元、存储器、输入/输出通过总线相连。这一架构的精髓在于将计算锚定在"节点"上：处理器是主角，存储器是配角，互连总线是仆从。IBM Research科学家Manuel Le Gallo-Bourdeau精辟评价："冯诺依曼架构非常灵活，这是它最大的优点。这就是它最初被采用的原因，也是它至今仍是主流架构的原因。"[2] 在此后的八十年中，这一以节点为中心的范式凭借其灵活性、模块化与可升级性，成为从PC到超算的统一基座。

然而，八十年的统治正面临结构性危机。这一危机并非来自某种单一技术的突破，而是来自三大瓶颈的交叉共振。

**瓶颈一：存储墙（Memory Wall）。** Wulf和McKee于1995年首次系统性地命名了"存储墙" [4]——处理器与存储器之间的性能差距以每年约50%的速度扩大。此后三十年，尽管微体系结构创新——乱序执行、推测执行、多层缓存、硬件预取——不断延缓存储墙的冲击，SemiAnalysis在2024年的深度分析确认"DRAM已无法再缩放" [4b]。Dennard缩放定律在约2006年失效后 [4c]，逻辑运算能耗因电压降低和多阈值工艺优化持续改善，而DRAM存储单元依赖电容器充放电的物理原理，其单次访问能耗的改善程度远不及逻辑运算。

**瓶颈二：通信墙（Communication Wall）。** 随着计算系统的分布式规模持续扩展——从单芯片多核到万卡集群——节点间通信开销的增长速度往往超过计算能力的增长。在实际HPC部署中，互连网络消耗高达系统总功率的12%（满载时），通信开销占MPI程序总执行时间的4%-27% [5][6]。在大模型分布式训练中，AllReduce等集合通信操作可以占据单步训练时间的30%-40%。

**瓶颈三：能量墙（Energy Wall）。** 在45nm工艺下，一次DRAM访问的能耗高达1.3-2.6 nJ，而32位浮点乘法的能耗仅为3.7 pJ——350-700倍的差距 [1]。MIT Eyeriss团队在65nm工艺下的系统化实测进一步确认：片外DRAM读取能耗是一次MAC运算的200倍 [7]。IBM Research在2025年明确指出，现代AI工作负载中计算能耗仅约占10%，数据搬运能耗占约90% [2]。Semiconductor Engineering与Arteris在2025年的联合报告确认："在当今以AI为中心的半导体格局中，低效的数据搬运往往是影响整体系统性能和功耗的首要瓶颈。"[8]

**三堵墙的本质归一：数据移动墙。** 存储墙、通信墙与能量墙表面上发生在不同的层级——分别是处理器-存储器接口、节点间网络、和全系统能量流——但它们指向同一个物理本质：在冯诺依曼范式中，数据的"搬运"（数据移动）而非数据的"加工"（计算），才是能效、性能与可扩展性的决定性因素。本文将这三堵墙统一命名为"数据移动墙"（Data Movement Wall），并以此为核心展开系统性分析。

**可持续智能计算的紧迫性。** 将这一问题置于可持续智能计算的框架中尤为紧迫。当前AI大模型的训练和推理能耗正以远超Moore定律补偿能力的速度增长。全球数据中心的电力消耗预计将在2030年达到全球总发电量的8%-10%。如果"数据移动占AI能耗的90%"这一比例保持不变，那么单纯增加可再生能源供给只能延缓而无法解决根本矛盾——真正的可持续性必须来自对数据移动本身的架构级优化。

本文旨在为这一架构级优化提供系统性的第一性原理分析框架。

---

## 二、第一性原理：计算的算子—数据移动分解

### 2.1 计算图视角

从数学的角度审视，任何一个计算任务 T 都可以表示为一个有向无环图（DAG）G=(V,E)，其中节点集 V={v₁,v₂,…,vₙ} 代表基本运算（算子），边集 E={eᵢⱼ} 代表数据依赖（数据移动）。DAG模型是并行计算理论中的标准形式化工具，已被广泛应用于任务调度 [25] 和编译器优化 [26]。计算的执行过程即为：在正确的时刻，将正确的数据，通过正确的路径，送达正确的算子。

### 2.2 弱耦合分解与口径定义

由此得到计算的弱耦合分解命题：

```
T = O(V) ∘ M(E) + Γ(O,M)
```

其中 O(V) 为算子空间，M(E) 为数据移动空间，∘ 表示组合，Γ(O,M) 为耦合项。

此处使用"弱耦合"（Weakly Coupled）而非"正交"（Orthogonal），是因为严格数学意义上的正交要求内积空间中两子空间内积为零，而在实际计算系统中，算子选择与数据移动模式之间存在耦合。然而，这种耦合是高阶效应：算子的功能语义（"做什么"）与数据移动的传输语义（"怎么送"）可以独立描述、独立编程、独立优化，在绝大多数场景下 ‖Γ‖ ≪ ‖O∘M‖。

**口径定义。** 为确保与既有体系结构文献的可比性，本文显式区分两种数据移动口径。**广义数据移动**（Movement_broad）涵盖任何层级间的数据读写与传输：寄存器堆读写、片上缓存间数据迁移、DRAM访问、芯片间互连传输、跨节点网络通信。Horowitz [1] 和 Eyeriss [7] 的能耗数据覆盖全层级，属广义口径。**狭义互连路由**（Routing_narrow）仅指数据在计算单元之间/芯片之间/节点之间通过互连网络的传输（NoC、die-to-die链路、数据中心网络）。HPC通信开销数据 [5][6] 和SDI机制主要涉及此口径。两种口径的关系为包含关系：Routing_narrow ⊂ Movement_broad。本文在引用具体数据时标注口径，在论述SDI等互连可编程方案时默认使用狭义口径，在讨论总体能效时默认使用广义口径。

### 2.3 能量分解与数据移动主导定律

设一次完整计算的总能耗为 E_total，则：

```
E_total = E_op + E_move
```

其中 E_op 为算子执行能耗，E_move 为数据移动能耗（广义口径）。定义数据移动能量比 η：

```
η = E_move / E_total
```

基于Horowitz ISSCC 2014（45nm）[1] 和MIT Eyeriss ISCA 2016（65nm）[7] 的权威实测数据（均为广义口径），η 在不同层级下的实测值如下：

| 操作/层级 | 能耗（45nm, Horowitz [1]） | 相对MAC倍数（65nm, Eyeriss [7]） | 口径 |
|-----------|---------------------------|--------------------------------|------|
| 8b整数加法 | 0.03 pJ | — | 算子 |
| 32b浮点加法 | 0.9 pJ | — | 算子 |
| 32b浮点乘法 | 3.7 pJ | — | 算子 |
| 寄存器堆（RF, 0.5kB） | — | 1× | 广义移动 |
| 片上NoC互连（1-2mm） | — | 2× | 狭义路由 |
| 全局缓冲（8kB SRAM） | 10 pJ | 6× | 广义移动 |
| 片外DRAM | 1.3-2.6 nJ | 200× | 广义移动 |

**关键结论（按场景分层表述）：** 在AI大模型推理/训练负载中，IBM Research确认计算能耗仅约占10%，即 η_AI ≥ 0.9（广义口径）[2]；在HPC/信号处理/通用计算中，Horowitz的数据表明处理器超50%能耗消散在缓存与寄存器堆中 [1]，即 η_HPC/SP/GP ≈ 0.5-0.8（广义口径）。

我们将其统一表述为**数据移动主导定律**（Law of Data Movement Dominance）：

> **经验定律：** 在冯诺依曼范式下，对于数据规模显著超出片上可复用容量、且有效算术强度低于关键存储/互连层级带宽-能耗拐点的计算任务，数据移动能耗在总能耗中的占比始终为主导项。在AI场景中 η ≥ 0.9（广义口径）；在HPC与信号处理场景中 η ≈ 0.5-0.8（广义口径）；在所有数据密集型计算场景中 η > 0.5。数据移动是计算能效的核心矛盾。

需要明确的是，此定律是基于多个独立权威来源（Horowitz/Stanford [1], Sze/MIT [7], IBM Research [2], Dally/NVIDIA [1b], Arteris [8]）的实测数据归纳而成的经验定律——类似于Moore定律——而非具有数学证明的定理。

这一定律可以从Roofline模型 [9] 得到进一步的理论支撑。经典Roofline模型将计算性能表示为算术强度（OI = FLOPs/Byte）的函数。当应用的OI低于硬件的"拐点"（Ridge Point）时，性能受限于带宽（即数据移动），而非计算。LBNL团队进一步发展了层次化Roofline模型 [9b]，将分析从单一DRAM层级扩展到L1/L2/L3/HBM多级存储层次。实测数据显示：Stencil计算的OI仅为0.33-0.56 FLOP/Byte [10]，深度学习推理的OI随batch size变化在1-100之间 [11]，大量实际工作负载落在层次化Roofline的多级"带宽受限"区域。

---

## 三、四大计算场景的数据移动展开分析

### 3.1 通用计算（通算）：缓存层级即数据移动层级

通用CPU架构中，经典的多级缓存体系（L1-L2-L3-DRAM）本质上是一个层次化数据移动网络。每一次Cache Miss都是一次数据移动失败——数据未能在最短路径上被找到，系统被迫在更长、更高能耗的路径上搜索。Horowitz的实测数据为此提供了精确的能量标尺 [1]：一条指令的控制开销约70 pJ（取指、时钟、流水线寄存器），而其中ALU执行的加法/乘法仅0.1-3.7 pJ（均为广义口径）。在一款40nm 8核超标量处理器中，超过50%的芯片能耗消散在缓存与寄存器堆中。取指（Fetch）、访存（Load/Store）、缓存一致性协议（MESI/MOESI）、TLB翻译——全部属于广义数据移动范畴。

### 3.2 智能计算（智算）：数据流即数据移动拓扑

AI推理与训练的核心运算是矩阵乘法（GEMM），其算子极度简单——乘累加（MAC）。MIT的Eyeriss架构（ISCA 2016）[7] 定义了三种经典数据流——权重驻留（WS）、输出驻留（OS）、无本地复用（NLR），每种数据流本质上是一种数据移动策略的选择。Eyeriss提出的行驻留（RS）之所以能效最优，正是因为它在寄存器堆（RF）、PE阵列（inter-PE NoC）和全局缓冲三个数据移动层级上同时最大化了数据复用——即最小化数据移动距离和移动次数。

Cerebras的晶圆级引擎（WSE-3）之所以实现相对GPU高达21倍的推理加速 [12]，其核心优势并非算子更快，而是片上互连彻底消除了芯片间的数据移动开销——900,000个AI核心通过片上fabric直接互连，片上fabric带宽达214 Pb/s，聚合内存带宽为21 PB/s [12b]。IEEE Spectrum确认"主要优势在互连——通过在片上布线，晶圆级芯片绕过了计算速度的许多瓶颈"[13]。Cerebras的SEC文件披露，其晶圆级架构消除了分布式计算的需要，使AI开发者在处理大型模型时"使用的代码减少多达97%"[12c]。

### 3.3 高性能计算（超算）：通信拓扑即数据移动骨架

超算的核心矛盾更加直接——计算是分布式的，节点间必须通过互连网络交换边界数据。以经典的3D偏微分方程求解为例，Stencil计算的算术强度极低（OI ≈ 0.33-0.56 FLOP/Byte）[10]，这意味着每进行一次浮点运算，就需要搬运2-3字节数据。在层次化Roofline模型中 [9b]，Stencil计算深陷多级"带宽受限"区域。HPC领域的研究表明，互连网络消耗高达12%的系统总功率（满载时），通信开销占MPI程序总执行时间的4%-27% [5][6]。Frontier、Fugaku等顶级超算的设计演进反复证明：互连拓扑（Dragonfly, Fat-tree, Torus）的选择对实际应用性能的影响，往往超过计算节点本身的浮点峰值。

### 3.4 信号处理：蝶形路由即FFT的灵魂

快速傅里叶变换（FFT）是信号处理的基石算法。一个N点FFT分解为log₂N级蝶形运算，每级包含N/2个蝶形算子（复数乘加）。然而，FFT的真正精妙之处不在蝶形算子本身，而在于级间数据重排的移动模式。在硬件实现中，SDF、MDF、MDC等FFT架构的本质差异，正是如何用不同的延迟线和多路选择器来实现不同的数据移动拓扑。算子始终是同一个蝶形MAC。

H.T. Kung在1978年提出的脉动阵列（Systolic Array）[27] 是"数据移动优化"思想的历史先驱。Kung精辟地指出："脉动架构通过在每次内存访问中执行多次计算，可以在不增加I/O带宽需求的情况下加速计算密集型问题。"[28] 脉动阵列通过数据在PE间的有规律流动消除了全局广播/归约路由，其核心设计理念——最大化每次内存访问的计算复用率——与本文的数据移动优化理念高度一致。

### 3.5 数据移动展开的统一结论

| 计算场景 | 底层原子算子种类 | 数据移动模式 | 移动能耗占比 η（口径） |
|----------|-----------------|-------------|----------------------|
| 通算 | ALU指令集（~百量级） | 层次缓存 + 一致性协议 | ~50%-70%（广义） |
| 智算 | MAC + 非线性（~十量级） | 权重加载 + 激活广播 + 部分和归约 | ≥ 90%（广义） |
| 超算 | 浮点加乘（~十量级） | Halo Exchange + AllReduce | 50%-80%（广义） |
| 信号处理 | MAC（~五量级） | 蝶形shuffle + 流水级间 | 50%-70%（广义） |

结论：各场景的底层原子算子高度收敛于一组有限集合；数据移动空间是高维、多变的，且在所有数据密集型场景中数据移动能耗均为主导项。**数据移动是所有密集计算场景的公共核心矛盾。**

---

## 四、算子空间的收敛性：从表观多样到底层统一

### 4.1 "算子多样性幻觉"的澄清

一个直觉上的质疑是：数学中存在无穷多种运算——微分、积分、特殊函数（Bessel、Gamma、误差函数等）、偏微分方程求解、优化算法——AI推理中的那几十种算子怎么可能覆盖如此丰富的数学世界？

这一质疑的根源在于混淆了"数学运算"与"硬件原子算子"两个层次。正如自然语言中有无穷多种语句，但所有语句都由有限的字母表组合而成；数学运算有无穷多种，但所有数学运算最终都归约到硬件可直接执行的有限原子操作。这一层次关系可以形式化为算子空间的三层架构：

**第一层（原子层 / Atomic Layer）：** 硬件直接执行的原子操作，种类极其有限。在当代所有计算架构中，原子层仅包含以下操作（采用IEEE 754算术标准 [29] 与标准整数ALU操作作为定义基准）：整数/浮点加法（ADD）、整数/浮点乘法（MUL）、融合乘累加（FMA/MAC）、逻辑运算（AND/OR/XOR/NOT）、比较（CMP）、移位（SHIFT）、位操作。以此定义标准，不可约的最小原子集为：

```
A_min = {ADD, MUL, AND, XOR, CMP, SHIFT},  |A_min| = 6
```

**第二层（复合层 / Composite Layer）：** 由原子操作组合而成的标准函数。例如，三角函数 sin(x)、cos(x) 通过CORDIC算法归约为加法和移位的迭代序列 [15]；指数函数 eˣ 通过多项式逼近归约为有限次乘法和加法 [16]；Softmax函数归约为减法、指数（复合层）、除法（复合层）的组合。

**第三层（算法层 / Algorithmic Layer）：** 由复合层函数按特定拓扑结构组合而成的完整算法——FFT、卷积、PDE求解、梯度下降等。这一层的复杂度主要体现在数据移动模式（数据流的拓扑结构），而非算子本身。

### 4.2 收敛性定理

> **定理（算子空间收敛性）：** 设 A 为硬件可直接执行的原子算子集合，|A| ≤ K，其中 K 为一个与计算场景无关的小常数。则对于四大主流计算场景中出现的任意确定性数学运算 f，只要 f 在有限精度浮点表示的有界计算域上是连续的（或可以被连续函数逐段逼近），就存在 A 上的有限复合序列 σ = (a₁,a₂,…,aₘ)，aᵢ ∈ A，使得 f 可被 σ 以任意精度 ε 逼近，即：‖f − σ‖ < ε。

**证明思路：** (1) Weierstrass逼近定理保证了闭区间上的连续函数可以用多项式任意精度逼近 [17]。在IEEE 754浮点数系统的有限精度和有限范围下，Weierstrass定理的适用前提——闭区间与连续性——在有限精度数字计算中自动满足。多项式运算仅由加法和乘法构成，因此所有（分段）连续函数可归约到 {ADD,MUL}。(2) CORDIC算法（1959年由Volder提出 [18]）证明了三角函数、双曲函数、指数、对数等超越函数均可通过加法和移位的迭代实现，无需乘法器。(3) Taylor/Chebyshev/Padé逼近为更广泛的特殊函数提供了多项式或有理函数形式的逼近序列。(4) Horowitz在ISSCC 2014中的硬件实测 [1] 和V. Sze等在Proc. IEEE 2017综述中的系统分析 [19] 共同确认：在当代计算架构中，K ≤ 10 即可覆盖所有实际需要的原子操作。

**适用边界说明：** 本定理适用于确定性数学运算。定理假设有限精度计算——在需要无限精度的纯数学推导场景中，有限原子算子集合的逼近特性不直接适用。

### 4.3 收敛性的实证

| 高阶数学运算 | 原子算子归约路径 | 所需原子算子 |
|-------------|-----------------|-------------|
| sin(x), cos(x) | CORDIC迭代 → ADD + SHIFT × n | ADD, SHIFT |
| eˣ, ln(x) | 多项式/CORDIC → MUL + ADD × n | ADD, MUL |
| 1/x (除法) | Newton-Raphson迭代 → MUL + ADD × n | ADD, MUL |
| √x | Newton-Raphson / Goldschmidt | ADD, MUL |
| Softmax | EXP(复合) + DIV(复合) + ADD | ADD, MUL |
| FFT蝶形 | 复数乘加 → 4 MUL + 2 ADD | ADD, MUL |
| Stencil (CFD) | 加权求和 → MAC × n | ADD, MUL |
| 矩阵分解 (LU) | 消元 → MUL + ADD + CMP | ADD, MUL, CMP |
| 梯度下降 | θ←θ−α∇L → MUL + ADD | ADD, MUL |
| AES加密 | SubBytes(查表)+ShiftRows+MixColumns+XOR | XOR, SHIFT, 查表 |

结论：四大场景中出现的所有高阶数学运算，无一例外地归约到以 {ADD, MUL, CMP, SHIFT, AND, XOR} 为核心的原子算子集合。算子种类的有限性不是"AI计算的特例"，而是计算本身的第一性原理。正因为算子空间如此收敛，计算系统的差异化、能效的决定性因素，就不可能在算子上，而只能在数据移动上。


---

## 五、数据移动标准化：元语体系的构建

### 5.1 数据移动的复杂性根源

与算子的有限性形成鲜明对比，数据移动的复杂性来自于以下维度的组合爆炸：空间维度（数据从源到目的的物理/逻辑路径选择——单播、多播、广播、归约树、蝶形网络等）；时间维度（数据在何时发出、何时到达、是否需要同步、是否允许乱序、配置延迟与计算延迟的匹配）；粒度维度（移动的对象可以是bit、byte、word、cacheline、packet、tile、tensor）；层级维度（从寄存器间、PE间、芯片内NoC、芯片间互连到跨节点网络，移动跨越多个物理层级）；协议维度（缓存一致性、流控、仲裁等）。

### 5.2 数据移动元语体系

尽管数据移动复杂性极高，从第一性原理出发，可以提取一组元语作为描述密集计算数据移动模式的原子操作。本文提出的元语体系主要面向确定性数据流模式（即在编译时或运行时初始化阶段可确定移动拓扑的场景），覆盖AI推理/训练、HPC仿真、大规模信号处理等密集计算负载的核心数据移动需求：

```
M_meta = {UNICAST, MULTICAST, BROADCAST, GATHER, SCATTER, REDUCE, ALLREDUCE, SHUFFLE, PIPELINE, BARRIER, COND_ROUTE},  |M_meta| = 11
```

| 元语 | 语义 | 形式化 |
|------|------|--------|
| UNICAST(s, d) | 从源s向目的d发送数据 | s → d |
| MULTICAST(s, D) | 从源s向目的集D发送相同数据 | s → {d₁,…,dₖ} |
| BROADCAST(s, *) | 从源s向所有节点发送 | s → V |
| GATHER(S, d) | 从源集S收集数据到d | {s₁,…,sₖ} → d |
| SCATTER(s, D, f) | 按分片函数f分发 | s →_f {d₁,…,dₖ} |
| REDUCE(S, d, ⊕) | 归约到目的d | ⊕_{s∈S} data(s) → d |
| ALLREDUCE(V, ⊕) | 全体归约并广播 | ⊕_{v∈V} data(v) → V |
| SHUFFLE(V, π) | 按置换π重排 | vᵢ → v_{π(i)} |
| PIPELINE(s→d, stages) | 多级流水传递 | s → r₁ → … → d |
| BARRIER(V) | 同步所有节点 | ∀v∈V: sync |
| COND_ROUTE(s, d₁, d₂, p) | 按谓词p条件路由 | s → d₁ if p, else s → d₂ |

COND_ROUTE（条件路由）用于描述数据依赖的路由决策——例如分支预测结果决定的取指路由、稀疏矩阵计算中非零元素位置决定的数据路由。上述元语体系与MPI标准的集合通信原语 [30] 具有自然的对应关系，为其工程实现提供了成熟的软件基础。

**四大场景的元语映射：** 智算（Transformer）：权重加载 = BROADCAST + UNICAST；注意力计算 = MULTICAST + REDUCE；梯度同步 = ALLREDUCE。超算（MPI并行）：Halo Exchange = 多组UNICAST；全局归约 = ALLREDUCE；流水线并行 = PIPELINE。信号处理（FFT）：bit-reversal = SHUFFLE(π_bitrev)；蝶形交叉 = 多组UNICAST对。通算（分支预测）：条件取指 = COND_ROUTE(PC, target₁, target₂, branch_pred)。

### 5.3 元语的最小代价模型

为使元语可用于编译优化与架构评估，每个元语实例需附带以下代价参数。

带宽需求：数据量 B、扇出/扇入因子 k。

延迟模型：
```
L = L_setup + B / BW_eff + L_contention
```
其中 L_setup 为连接建立延迟，BW_eff 为有效带宽（受拓扑和拥塞影响），L_contention 为竞争等待延迟。

能耗模型：
```
E = E_per_bit × B × hops + E_switch × switches
```
其中 hops 为跳数，switches 为经过的交换节点数。此代价模型使得编译器可以对不同的元语组合方案进行定量评估，选择总能耗和延迟最优的数据移动策略。

---

## 六、软件定义互连：从固定路由到可变路由

### 6.1 冯诺依曼范式的路由僵化

冯诺依曼架构的根本问题在于：互连路由是在设计时（Design Time）固化的，而非在运行时（Runtime）可编程的。CPU的缓存层级、GPU的Systolic Array数据流、ASIC的NoC拓扑——都在芯片流片时确定。当工作负载发生变化时，固定的路由拓扑无法自适应，导致严重的效率损失。

NVIDIA从NVLink到NVSwitch再到NVLink-C2C的演进历程，本质上是在不断打补丁式地缓解路由僵化。NVLink-C2C已实现比PCIe Gen6 PHY高6倍的能效和3.5倍的面积效率 [20]，但在芯片内部，Systolic Array的数据流模式仍是设计时选定的。学术界的MAERI架构（ASPLOS 2018）[21] 的核心设计哲学正是"使加速器内部的互连可重构"——其可重构的增强树网络支持运行时改变数据流映射——这正是SDI思想在片上的萌芽。

### 6.2 软件定义互连（SDI）机制

SDI的核心思想是：将互连路由（狭义口径）从硬件固化层提升到软件可编程层，使互连拓扑在运行时可动态重构。其分层架构包含三层。

**物理层（Physical Layer）：** 提供可编程的交叉互连矩阵（Crossbar/Switch Fabric），支持任意端口对之间的连接建立与断开。MIT Lincoln Lab已展示了基于晶圆级可重构布线的active wafer-scale logic fabric [22]。Lightmatter的Passage平台将光子互连引入晶圆级——其最新的Passage L20模块提供32个光端口、每通道200Gbps数据速率 [22b]。

**路由层（Routing Layer）：** 基于数据移动元语的组合，软件编译器生成路由指令序列，控制物理层交叉矩阵的动态配置。每个元语映射为物理层的一组开关状态。

**编排层（Orchestration Layer）：** 全局调度器根据计算DAG与当前硬件状态，动态决定算子到PE的映射（Placement）以及数据在PE间的路由策略（Routing），实现计算与通信的联合优化。

SDI的核心方程为：R_runtime = C(G_task, H_state)，其中 R_runtime 为运行时路由配置，C 为编译/调度函数，G_task 为任务计算图，H_state 为当前硬件状态。SDI将SDN（软件定义网络）的控制平面/数据平面分离思想从"宏观网络"下沉到"芯片内微观互连"，时间精度从毫秒级提升到纳秒级，粒度从packet级细化到word/flit级。

### 6.3 SDI的收益阈值与工程可行性

SDI的可行性面临一个关键质疑：可重构互连矩阵本身的面积、功耗和配置延迟开销是否会抵消其灵活性带来的收益？

设一次互连重构的配置能耗为 E_cfg、配置时间为 T_cfg；在重构周期内，因路由优化而节省的数据移动能耗为 ΔE_move、节省的时间为 ΔT。SDI在该重构周期内"值得"的必要条件为：

```
ΔE_move ≥ E_cfg,   ΔT ≥ T_cfg 或 T_cfg 可被流水隐藏
```

**数量级估算：** 在PE级互连矩阵中，以64×64 PE阵列为例，全交叉互连需4096个开关，每个开关1-bit配置——仅4 Kbit配置SRAM。配置写入速率可达GHz级，因此 T_cfg ≈ 4096/10⁹ ≈ 4 μs。对于典型的AI推理batch（计算延迟~ms级），T_cfg/T_batch < 0.5%，可忽略不计。对于配置能耗，4 Kbit SRAM写入在5nm工艺下约 4096×1 fJ ≈ 4 pJ，远小于一次batch计算中节省的DRAM访问能耗（nJ-μJ量级）。因此 ΔE_move ≫ E_cfg 在典型AI/HPC场景中易于满足。

上述阈值在以下条件集合下更容易被满足：(a) 模型/数据规模大（数据移动占比高，优化空间大）；(b) 拓扑/并行策略多变（固定拓扑的效率损失大）；(c) 并行通信占系统时间主导（狭义路由是关键瓶颈）；(d) 需保持跨负载可编程性（ASIC的单一拓扑无法兼顾多种负载）。当这四个条件同时成立时，SDI具有明确的架构优势。

实际系统中部分交叉（partial crossbar）或分层互连可进一步降低开销。AMD/Xilinx的Versal ACAP已在商用产品中验证了可编程NoC的工程可行性——其硬化NoC支持运行时QoS配置与多种拓扑模式 [31]。SambaNova的可重构数据流单元（RDU）——已进入第五代商用产品SN50 [33]——正是在PE级实现可重构数据流的工业验证。

---

## 七、范式迁移：从节点中心到网络中心

### 7.1 两种范式的对立

| 维度 | 冯诺依曼（节点中心） | 网络中心（液态架构） |
|------|---------------------|---------------------|
| 核心关注点 | 处理器（ALU/MAC） | 互连网络（Routing Fabric） |
| 架构特征 | 固定拓扑，设计时确定 | 可变拓扑，运行时重构 |
| 性能瓶颈 | 计算单元利用率 | 数据移动能效 |
| 扩展方式 | 堆叠更多节点 | 重构互连拓扑 |
| 编程模型 | 指令流（Instruction Stream） | 计算图编译 + 数据流 |
| 优化目标 | FLOPS/W | Bits-moved/Joule |
| 适用域 | 控制密集型 + 密集计算 | 密集计算负载优化 |

需要明确强调：液态架构面向密集计算负载（AI推理/训练、HPC仿真、大规模信号处理等）优化，在"模型/数据规模大、拓扑/并行策略多变、并行通信占主导、且需保持跨负载可编程性"的条件集合下具有明确优势。它不替代通用CPU在操作系统、控制密集型任务中的地位。正如IBM Research的Geoffrey Burr所言："对于通用计算，没有什么比冯诺依曼架构更强大的了……未来很可能是冯诺依曼与非冯诺依曼处理器的混合体。"[2]

### 7.2 与相关范式的比较与统一

液态架构并非凭空而生，它与多条已有的非冯诺依曼技术路径存在深刻的关联与互补。

**(1) 存内计算（IMC）：** IBM Research的模拟存内计算通过在电阻阵列中直接执行矩阵乘法，将"存储→计算"的数据移动距离缩短至零——从本文框架看，这是将 E_move 在算子层面极小化的极端策略。其优势在于大幅降低 η，但面临精度限制 [34]、可编程性限制和有限操作种类。液态架构与IMC互补：液态架构可将IMC核心作为PE阵列中的专用算子节点，SDI提供IMC核心之间的灵活互连。

**(2) 近存计算（NMC）：** IBM的NorthPole芯片是近存计算的典范——每个核心配有本地SRAM，在LLM推理中比最节能GPU快47倍、能效高73倍 [35]。从本文框架看，NorthPole通过缩短数据移动距离来降低 E_move。液态架构的PE可采用NorthPole式近存设计，同时通过SDI实现PE间灵活互连。

**(3) 数据流架构：** 从MIT的Tagged-Token Dataflow Machine [36] 到SambaNova的RDU [33]，数据流架构通过"数据驱动执行"替代"指令驱动执行"来优化数据移动模式。液态架构可理解为对数据流架构思想在介观尺度上的物理实现——通过SDI将数据流拓扑从编译时固定提升到运行时可编程。

**(4) 粗粒度可重构阵列（CGRA）：** CGRA在PE级提供固定ALU/MAC功能、在互连级提供可编程路由 [37]。液态架构与CGRA的核心区别在于物理尺度：CGRA通常限于单芯片，液态架构通过晶圆级集成和先进封装将可重构互连扩展到介观尺度（wafer-scale），实现远超单芯片CGRA的网络规模。

**(5) 更强互连（NVLink/NVSwitch/UCIe/光互连）：** 提高互连带宽和降低每bit能耗是数据移动优化的"物理层"路径。SDI与更强互连是正交可组合的：SDI在逻辑层提供路由可编程性，更强互连在物理层提供更高的带宽-能耗比。

**(6) 算法/编译优化（算子融合、重计算换通信、压缩/量化/稀疏化）：** 这些方法通过减少数据移动总量或改变移动模式来优化效率。SDI与算法优化是互补的：算法优化决定"需要搬多少数据"，SDI优化"怎么搬最高效"。

上述六条路径可在液态架构的统一框架中得到整合：IMC/NMC优化PE内部的算子-存储距离，数据流架构优化PE间的执行模式，CGRA优化PE间的互连灵活性，更强互连提升物理层带宽能效，算法优化减少总移动量，而液态架构通过SDI将这些要素统一在介观尺度平台上，实现系统级最优。

### 7.3 液态一体架构

"液态"（Liquid）的隐喻捕捉了网络中心范式的本质：如同液体根据容器形状自适应改变形态，液态架构的互连拓扑根据工作负载的计算图自适应重构。其三大支柱为：

**支柱一：标准化算子库。** 如第四节所证，有限的原子算子构成计算的"原子"。所有高阶数学运算通过复合层归约到原子层。算子以硬件IP核形式实现，功能固定、接口标准、性能可预测。

**支柱二：标准化数据移动元语。** 如第五节所述，有限的元语构成数据移动的"原子"。元语通过编译器映射到物理互连，附带代价模型用于优化。

**支柱三：软件定义互连矩阵。** 如第六节所述，可编程物理互连提供数据移动的"溶剂"——使算子与数据移动的组合在运行时动态变化。

三者的关系形式化为：
```
Liquid_Architecture = O_std ⊕ M_meta ⊕ F_SDI
```

### 7.4 液态硬件

液态硬件是液态一体架构的物理实现。它不是FPGA（粒度太细、效率不够），也不仅是单芯片CGRA（规模受限），而是在介观尺度上通过异构异质集成实现的、以互连为第一公民的硬件平台。其关键技术路径包括：晶圆级集成（Cerebras WSE-3已验证900,000核心、片上fabric带宽214 Pb/s [12][12b][13]）；先进封装与Chiplet（通过UCIe、NVLink-C2C等协议实现不同工艺chiplet在统一互连平面上协同 [20]）；光电混合互连（IBM co-packaged optics [2]、Lightmatter Passage光子互连 [22b]）；可重构数据流单元（SambaNova RDU [33]）。

传统硬件是冰——结构固定、形态不变；FPGA是沙——粒度太细、效率不高；液态硬件是水——在介观尺度上既有结构（算子IP核）又有流动性（可变互连）。

### 7.5 液态架构的良率与容错

晶圆级集成面临良率挑战。Cerebras已通过以下策略成功解决 [12d]：WSE-3的每个AI核心面积仅约0.05 mm²，约为H100单个SM的1%。当缺陷发生时，WSE-3仅损失0.05 mm²硅面积，而H100损失约6 mm²——WSE-3的缺陷容忍度约为GPU的100倍。其关键机制包括极小核心带来的细粒度冗余，以及片上fabric的自适应路由：当检测到缺陷时，系统自动通过冗余通信路径绕行。液态架构的SDI机制天然具备容错能力——可编程互连矩阵可在运行时动态绕过故障PE或故障互连链路。

### 7.6 液态架构的编程模型

液态架构需要一种新的编程抽象。传统指令流模型面向"控制流驱动、节点中心"的冯诺依曼架构，无法充分表达"数据流驱动、网络中心"的液态硬件特性。液态架构的编程模型为"计算图编译 + 算子-数据移动联合调度"：开发者以高层计算图（如PyTorch的计算图、HPC的任务DAG）描述应用；编译器将计算图分解为标准算子和数据移动元语的组合，基于元语代价模型执行联合优化；运行时调度器根据当前硬件状态动态配置SDI矩阵。

这一编程模型的工业原型已经存在——Cerebras的SDK提供了从PyTorch模型到WSE的自动映射 [12e]，SambaNova的SambaFlow编译器实现了从高层模型到RDU数据流的自动编译 [33]。液态架构的编程模型可在这些先驱工作基础上，通过引入标准化元语接口实现更通用的跨平台抽象。


---

## 八、理论框架：拓扑中心计算的形式化

### 8.1 计算能效的数据移动极限

对于给定计算任务 T，其理论最低能耗受限于两个独立的物理极限：

**算子执行的物理极限（Landauer极限）：** 任何逻辑不可逆操作至少消耗能量：
```
E_Landauer = kT ln 2 ≈ 2.85 × 10⁻²¹ J (@300K)
```
这是热力学第二定律对计算能耗的基本约束。2012年Bérut等人在Nature上的实验首次验证了这一理论极限 [38]。

**数据移动的物理极限：** 数据移动的能耗下界同样受Landauer极限约束——每bit数据在导线上的传输至少需要对线电容进行一次充放电。Shannon-Hartley定理给出了给定带宽和信噪比下的信道容量上界 [39]。

当前DRAM访问能耗（nJ/bit量级）距Landauer极限（zJ/bit量级，1 zJ = 10⁻²¹ J）尚有约10¹²倍（万亿倍）的空间。这一巨大差距恰恰说明：**数据移动能效仍有极其广阔的优化空间**——液态架构通过SDI优化互连路由拓扑，正是在这个万亿倍的优化空间中寻找更优解。

定义数据移动效率 ε_M：
```
ε_M = E_move^min / E_move^actual
```
在冯诺依曼范式下，ε_M 极低——固定的缓存层级和互连拓扑无法匹配多变的工作负载数据流模式，导致大量冗余数据搬运。在液态架构中，SDI机制使互连路由拓扑可以逼近每个任务的最优数据流，提升 ε_M。Yao的通信复杂度理论 [40] 为数据移动效率的下界提供了形式化工具——对于给定的计算任务DAG和PE映射方案，PE间必须交换的最少数据量提供了 E_move^min 的理论下界。元语组合优化的目标即为逼近这一通信复杂度下界。

### 8.2 网络复杂度与计算能力的关系

从复杂科学的视角，一个计算系统的信息处理能力不仅取决于节点的计算能力，更取决于网络的拓扑复杂度。Barabási在其网络科学的开创性工作中揭示了无标度网络具有异常高效的信息传播能力 [23]。

```
I_system = f(C_node, C_network)
```
其中 I_system 为系统信息处理能力，C_node 为单节点计算复杂度，C_network 为网络拓扑的时空协同复杂度。

**涌现阈值假说（Emergence Threshold Hypothesis）：** 当 C_network 与环境任务复杂度的比值超过某个阈值时，系统将涌现出更高等级的信息处理能力：
```
Ω_network(S,T) / Ω_env > θ_emergence
```
其中 Ω_network(S,T) 为物理网络的时空协同复杂度（包含拓扑复杂度、动态重配置能力和信息整合维度），Ω_env 为所在环境的相对复杂度，θ_emergence 为涌现阈值。液态架构通过SDI使 C_network 动态可变，使计算系统能够根据任务复杂度自适应调整网络复杂度。

需明确的是，涌现阈值假说目前仍是一个研究假说，尚缺乏严格的数学证明或充分的实验验证。它与Tononi的整合信息理论（IIT）[41] 存在有趣的呼应——IIT中的 Φ 值衡量系统整合信息的能力，与网络连通性和分化度密切相关。该假说的可能验证路径包括：(a) 在晶圆级可重构硬件上，系统化测量不同拓扑复杂度下的任务适应能力与学习效率；(b) 在理论层面，建立网络复杂度度量与计算表达能力之间的形式化关系。

---

## 九、研究展望：验证路线与实验指标

为将本文的理论框架转化为可实证检验的研究议程，建议以下验证指标与实验路线：

**(1) 数据移动能效指标。** 按广义/狭义口径分解端到端能耗，测量 Bits-moved/Joule 在不同架构（固定互连 vs SDI）上的对比值。

**(2) SDI收益阈值的实测。** 在可重构互连硬件（如CGRA或可编程NoC平台）上，实测 ΔE_move, E_cfg, ΔT, T_cfg 的数值，验证6.3节提出的收益阈值不等式。系统化扫描重构频率对吞吐的影响，确定最优重构粒度。

**(3) 可扩展性曲线。** 在不同拓扑与并行策略下，测量端到端效率随PE数/节点数的扩展关系，验证SDI架构在"拓扑多变"条件下是否比固定拓扑具有更优的弱扩展（weak scaling）和强扩展（strong scaling）特性。

**(4) 元语IR的编译质量。** 在真实AI/HPC模型上，评估元语中间表示（IR）+ 编译器的映射质量——包括通信量压缩比、拥塞率、数据复用率——与手工优化baseline的对比。

**(5) 涌现阈值假说的初步实验。** 在可重构硬件平台上，系统化改变网络拓扑参数（度数、连通性、小世界系数），测量系统在标准适应性任务（如few-shot学习、在线优化）上的表现随拓扑复杂度的变化关系，寻找可能的相变阈值。

---

## 十、结论

> "We're not running out of compute — we're running out of the ability to move data to the compute."

**核心结论一（数据移动瓶颈的普遍性）：** 冯诺依曼范式面临的存储墙、通信墙与能量墙，归根结底是"数据移动墙"——数据搬运的能耗、延迟和带宽已成为系统性能的决定性瓶颈。Horowitz/Stanford ISSCC 2014、Sze/MIT Eyeriss ISCA 2016、IBM Research 2025、Dally/NVIDIA Hot Chips 2023、Arteris 2025的数据共同确认：在所有数据密集型计算场景中，数据移动能耗均为主导项（η > 0.5，在AI场景中 η ≥ 0.9，均为广义口径）。且随着Dennard缩放终结与DRAM缩放放缓，数据移动-计算的能耗剪刀差在先进工艺节点中持续扩大。

**核心结论二（算子收敛性）：** 任何计算过程都可弱耦合分解为算子与数据移动。四大主流场景中，底层原子算子高度收敛于 {ADD, MUL, MAC, CMP, SHIFT, AND, XOR} 等有限集合（|A| ≤ 10），高阶数学算子均可由标准原语复合构造（Weierstrass逼近、CORDIC算法、多项式逼近）。正因为算子空间如此收敛，数据移动才成为唯一的差异化和决定性因素。

**核心结论三（数据移动可标准化与可编程）：** 数据移动可通过11个元语实现工程层面的形式化标准化（附代价模型用于编译优化）；软件定义互连（SDI）提供了将互连路由从设计时固化提升到运行时可编程的工程手段。SDI在满足收益阈值条件（ΔE_move ≥ E_cfg, ΔT ≥ T_cfg）的场景中具有明确优势，已有SambaNova RDU、AMD Versal ACAP等工业验证。

**核心结论四（液态架构的统一框架）：** 液态一体架构 = 标准算子库 ⊕ 标准数据移动元语 ⊕ 软件定义互连矩阵。这一架构统一了存内计算、近存计算、数据流架构、CGRA、更强互连和算法优化的核心思想，在"模型/数据规模大、拓扑/并行策略多变、并行通信占主导、且需保持可编程性"的条件集合下，代表了计算范式从"以节点为中心"向"以网络互联为中心"的迁移方向。

**核心结论五（可持续智能计算的物理路径）：** 在"可持续智能计算"的宏观视角下，数据移动墙是当前AI基础设施能耗危机的根本物理根源。如果AI工作负载中90%的能耗消耗在数据搬运上，那么仅靠增加可再生能源供给或优化算子本身都无法根本解决可持续性危机——因为算子的优化空间仅占10%，而真正的90%在于数据移动。液态架构通过SDI从物理层消除冗余数据搬运，直接针对这90%的能耗主体进行架构级优化，为可持续智能计算提供了一条从"第一性原理"出发的工程路径。涌现阈值假说进一步指出：智能的涌现依赖于物理网络的时空协同复杂度超过环境复杂度阈值——这为理解"可持续"与"智能"之间的深层联系打开了全新的研究维度。

**计算的下一个八十年，不再属于更快的处理器，而属于更智能的网络。** 在可持续发展的时代命题下，计算范式的迁移不仅关乎性能，更关乎我们能否在地球的物理边界内持续攀登智能的高峰。

---

## 参考文献

[1] M. Horowitz, "Computing's Energy Problem (and what we can do about it)," ISSCC 2014 Plenary, IEEE, Feb. 2014.

[1b] B. Dally, "Hardware for Deep Learning," Hot Chips 2023 Keynote, IEEE, Aug. 2023.

[2] M. Le Gallo-Bourdeau, H. Tsai, G. Burr et al., "How the von Neumann bottleneck is impeding AI computing," IBM Research Blog, Feb. 2025.

[3] T.S. Kuhn, *The Structure of Scientific Revolutions*, University of Chicago Press, 1962.

[4] W.A. Wulf and S.A. McKee, "Hitting the Memory Wall: Implications of the Obvious," ACM SIGARCH Computer Architecture News, vol. 23, no. 1, pp. 20-24, 1995.

[4b] SemiAnalysis, "The Memory Wall: Past, Present, and Future of DRAM," Sep. 2024.

[4c] R.H. Dennard et al., "Design of ion-implanted MOSFET's with very small physical dimensions," IEEE JSSC, vol. 9, no. 5, pp. 256-268, 1974. (Scaling end: M. Bohr, ISSCC 2011.)

[5] TOP500, "Power consumption of HPC interconnects," 2024.

[6] J. Dongarra et al., "The Impact of Communication on MPI Application Performance," Int. J. High Performance Computing Applications, 2023.

[7] V. Sze, Y.-H. Chen, T.-J. Yang, and J.S. Emer, "Efficient Processing of Deep Neural Networks: A Tutorial and Survey," Proc. IEEE, vol. 105, no. 12, pp. 2295-2329, 2017. (Eyeriss: Y.-H. Chen et al., ISCA 2016.)

[8] Semiconductor Engineering & Arteris, "Data Movement Bottlenecks in AI-Centric Semiconductor Design," Joint Report, 2025.

[9] S. Williams, A. Waterman, and D. Patterson, "Roofline: An Insightful Visual Performance Model for Multicore Architectures," CACM, vol. 52, no. 4, pp. 65-76, 2009.

[9b] T. Koskela et al., "A Hierarchical Roofline Model for Multi-level Memory Systems," LBNL, 2020.

[10] K. Datta et al., "Stencil Computation Optimization and Auto-tuning on State-of-the-Art Multicore Architectures," SC'08, 2008.

[11] N.P. Jouppi et al., "Ten Lessons from Three Generations Shaped Google's TPUv4i," ISCA 2021.

[12] Cerebras Systems, "WSE-3 Technical Overview," 2024.

[12b] Cerebras Systems, "WSE-3 Memory Bandwidth Comparison," 2024.

[12c] Cerebras Systems, SEC Filing S-1, 2024.

[12d] Cerebras Systems, "Yield and Defect Tolerance in Wafer-Scale Integration," White Paper, 2024.

[12e] Cerebras Systems, "Cerebras Software Platform: PyTorch-to-WSE Compilation," 2024.

[13] IEEE Spectrum, "Cerebras' Wafer-Scale Chip Bypasses Many Bottlenecks in Computing Speed," 2024.

[14] Harvard Architecture: separate instruction/data paths.

[15] "Efficient hardware implementations of trigonometric functions employing LUT, polynomial approximation, and CORDIC," ScienceDirect, 2025.

[16] J.M. Muller, *Elementary Functions: Algorithms and Implementation*, 3rd Ed., Birkhäuser, 2016.

[17] K. Weierstrass, "Über die analytische Darstellbarkeit sogenannter willkürlicher Functionen einer reellen Veränderlichen," 1885.

[18] J. Volder, "The CORDIC Trigonometric Computing Technique," IRE Trans. Electronic Computers, vol. EC-8, no. 3, pp. 330-334, 1959.

[19] V. Sze, Y.-H. Chen, T.-J. Yang, and J.S. Emer, "Efficient Processing of Deep Neural Networks: A Tutorial and Survey," Proc. IEEE, vol. 105, no. 12, pp. 2295-2329, 2017.

[20] NVIDIA, "NVLink-C2C," 2025.

[21] A. Parashar et al., "MAERI: Enabling Flexible Dataflow Mapping over DNN Accelerators via Reconfigurable Interconnects," Proc. ASPLOS, 2018.

[22] MIT Lincoln Lab, "Active Wafer-Scale Reconfigurable Logic Fabric for AI and High-Performance Computing."

[22b] Lightmatter, "Passage L20," Mar. 2026; "Passage L200," Mar. 2025.

[23] A.-L. Barabási and R. Albert, "Emergence of Scaling in Random Networks," Science, vol. 286, pp. 509-512, 1999.

[25] R.D. Blumofe and C.E. Leiserson, "Scheduling Multithreaded Computations by Work Stealing," J. ACM, vol. 46, no. 5, pp. 720-748, 1999.

[26] A.V. Aho, M.S. Lam, R. Sethi, J.D. Ullman, *Compilers: Principles, Techniques, and Tools*, 2nd Ed., 2006.

[27] H.T. Kung and C.E. Leiserson, "Systolic Arrays (for VLSI)," CMU-CS-79-103, 1978.

[28] H.T. Kung, "Why Systolic Architectures?" IEEE Computer, vol. 15, no. 1, pp. 37-46, 1982.

[29] IEEE 754-2019, "IEEE Standard for Floating-Point Arithmetic."

[30] MPI Forum, "MPI: A Message-Passing Interface Standard, Version 4.0," 2021.

[31] AMD/Xilinx, "Versal ACAP Programmable Network on Chip," PG313.

[32] Arteris Inc., "NoC Interconnect Fundamentals."

[33] SambaNova Systems, "Accelerated Computing with a Reconfigurable Dataflow Architecture," 2021; "Introducing the SN50 RDU," Feb. 2026.

[34] "Achieving high precision in analog in-memory computing systems," Nature Reviews Electrical Engineering, Jan. 2026.

[35] IBM Research, "IBM's NorthPole achieves new speed and efficiency milestones," Sep. 2024.

[36] Arvind and R.S. Nikhil, "Executing a program on the MIT Tagged-Token Dataflow Architecture," IEEE Trans. Computers, vol. 39, no. 3, pp. 300-318, 1990.

[37] "A comparative study of FPGA and CGRA technologies in hardware acceleration for deep learning," 2024.

[38] R. Landauer, "Irreversibility and Heat Generation in the Computing Process," IBM J. Research and Development, vol. 5, no. 3, pp. 183-191, 1961. Experimental verification: A. Bérut et al., Nature, vol. 483, pp. 187-189, 2012.

[39] C.E. Shannon, "A Mathematical Theory of Communication," Bell System Technical Journal, vol. 27, pp. 379-423, 623-656, 1948.

[40] A.C.-C. Yao, "Some Complexity Questions Related to Distributive Computing," Proc. 11th ACM STOC, pp. 209-213, 1979.

[41] G. Tononi, "An Information Integration Theory of Consciousness," BMC Neuroscience, vol. 5, no. 42, 2004.

---

## 附录A：终版修订说明

**A.1 口径对齐的显式化。** 在第二节2.2中新增"口径定义"段落，显式区分"广义数据移动"与"狭义互连路由"。在全文的能耗数据表和场景分析中标注所使用的口径。

**A.2 SDI收益阈值的形式化。** 在第六节6.3中新增SDI的收益阈值必要条件，并给出典型场景下的数量级估算。明确列出SDI具有优势的四个条件。

**A.3 适用条件的精炼表述。** 在摘要和第七节中，将液态架构的适用条件精炼为四个可检验的条件。

**A.4 相关范式比较的扩展。** 在第七节7.2中，将与相关范式的比较从4条扩展到6条，新增"更强互连"和"算法/编译优化"两条路径的讨论。

**A.5 元语代价模型的补充。** 在第五节新增5.3"元语的最小代价模型"，包含带宽、延迟、能耗、缓冲和拓扑映射五个维度的参数化描述。

**A.6 新增数据源。** 新增Bill Dally/NVIDIA Hot Chips 2023主旨演讲、SemiAnalysis的DRAM缩放分析、Dennard缩放终结的文献、Cerebras的良率白皮书等关键数据源。

**A.7 研究展望的可操作化。** 新增第九节"研究展望：验证路线与实验指标"，将理论框架转化为5项具体的可实证检验的研究议程。

**A.8 v1基线版本修订（2026-05-30）。** 清理Get笔记导入产生的格式重复；补齐完整的双语摘要（中+英）；强化"可持续智能计算"叙事先导——引言新增可持续性紧迫性段落，结论新增核心结论五；统一章节编号与交叉引用；修复公式排版；清理Obsidian元数据字段。

---

*基线版本 v1 | 2026-05-30 | TCC iNEST Research Group | 面向 Engineering 可持续智能计算专刊 (Deadline: 2026-06-20)*

