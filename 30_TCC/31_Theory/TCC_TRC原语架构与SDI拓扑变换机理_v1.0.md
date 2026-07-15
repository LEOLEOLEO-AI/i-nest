---
title: "TCC R.T.C原语系统架构与SDI拓扑变换底层机理"
date: 2026-07-08
version: v1.0
status: authoritative
tags: [TCC, R.T.C, SDI, primitives, architecture, topology-switching]
---

# TCC R.T.C 原语系统架构与 SDI 拓扑变换底层机理

## 从纯推理到训练到训推一体到信号处理的完整工作流

---

## 第一章：R.T.C 三类原语在典型实现系统中的架构

### 1.1 Tile 微架构：TCC 的最小可复用计算单元

TCC 系统的基本组成单元是 **Tile**。一个 Tile 包含三类硬件引擎，分别对应 R.T.C 三层原语：

`
                    Tile 内部架构
  +--------------------------------------------------+
  |                    SYN (计算核心)                  |
  |  +-----------+  +-----------+  +-----------+     |
  |  | T.GEMM    |  | T.FOLD    |  | T.MAPS    |     |
  |  | Systolic  |  | Adder     |  | SIMD      |     |
  |  | Array     |  | Tree      |  | Lanes     |     |
  |  +-----------+  +-----------+  +-----------+     |
  |  +-----------+  +-----------+  +-----------+     |
  |  | T.SCAN    |  | T.LOOK    |  | T.SPEC    |     |
  |  | Parallel  |  | BRAM      |  | CORDIC    |     |
  |  | Prefix    |  | LUT       |  | Engine    |     |
  |  +-----------+  +-----------+  +-----------+     |
  +--------------------------------------------------+
         |                    |
    [C.MOVE DMA]      [C.TICK Clock]
         |                    |
  +--------------------------------------------------+
  |              SDI 交换矩阵 (T.* 路由层)             |
  |                                                  |
  |  Crossbar NxN  +  VC分配  +  Page寄存器          |
  |  +  C.LINK 控制器  +  C.SYNC 屏障逻辑            |
  +--------------------------------------------------+
         |           |           |           |
      出端口0     出端口1     出端口2     出端口3
         |           |           |           |
     [E-L键]    [I-L键]    [E-S键]    [I-S键]
    (固化骨架)  (侧抑制)   (学习通道)  (修剪通道)
`

### 1.2 三类原语的硬件分布与职责边界

| 原语层 | 前缀 | 数量 | 硬件载体 | 职责 | 数据域 |
|--------|------|------|---------|------|--------|
| **T.* Transform 原语** | T. | 6 | SYN 计算核心 | 节点内代数运算 | 节点本地数据 |
| **R.* Route 原语** | R. | 6 | SDI 交换矩阵 | 节点间数据传输 | 网络链路上数据 |
| **C.* Control 原语** | C. | 4 | Tile 全局控制器 | 拓扑配置/时钟/同步/DMA | 系统状态寄存器 |

> **核心设计哲学（助记）**：R = Route（数据在路上，on the wire），T = Transform（数据在节点，in the node），C = Control（系统在掌舵，at the helm）。三者天然正交，不存在跨层等效替代。

### 1.3 TCC-16 原语全表

#### R.* Route 原语（6个）——控制数据如何在网络拓扑中流动

| # | 原语名 | 发音 | 语义 | 数据流模式 | 最优物理拓扑 | 硬件实现 |
|---|--------|------|------|-----------|------------|---------|
| T1 | **T.FUSE** | /fju:z/ | AllReduce | 多节点归约后广播 | Butterfly | 蝶形交换网络 |
| T2 | **T.PULL** | /pul/ | AllGather | 每节点贡献一块，全节点收集 | Radial Tree | 多播汇聚树 |
| T3 | **T.CAST** | /kæst/ | Broadcast | 单源广播到全节点 | Sparse Tree | 有向广播树 |
| T4 | **T.SWAP** | /swɒp/ | AlltoAll | 全节点两两数据交换 | Full Crossbar | 全交换矩阵 |
| T5 | **T.PIPE** | /paɪp/ | ReduceScatter | 分段流水归约分散 | Ring Pipeline | 环+流水线 |
| T6 | **T.MESH** | /meʃ/ | Neighbor Exchange | 邻居节点局部通信 | 2D/3D Mesh/Torus | 网格互连 |

#### T.* Transform 原语（6个）——数据在节点内如何被计算/变换

| # | 原语名 | 发音 | 语义 | 物理实现 | 硬件成本 | 典型应用 |
|---|--------|------|------|---------|---------|---------|
| R1 | **R.GEMM** | /dʒem/ | 矩阵乘加 C=αAB+βC | Systolic Array | ~50K LUT | 全连接层/卷积/Attention |
| R2 | **R.FOLD** | /fold/ | 向量归约 y=Reduce(x,op) | Adder Tree | ~5K LUT | 梯度求和/池化/归一化 |
| R3 | **R.MAPS** | /mæps/ | 逐元素映射 y=f(x) | SIMD Lanes | ~10K LUT | ReLU/GELU/Dropout |
| R4 | **R.SCAN** | /skæn/ | 前缀扫描/蝶形FFT | Parallel Prefix | ~15K LUT | FFT/IFFT/DBF/Cumsum |
| R5 | **R.LOOK** | /lʊk/ | 查表/非线性变换 | BRAM LUT | ~5K LUT+BRAM | Softmax/LayerNorm/SiLU |
| R6 | **R.SPEC** | /spek/ | 特殊函数逼近 | CORDIC/分段 | ~8K LUT | exp/log/sin/cos/sqrt |

#### C.* Control 原语（4个）——系统如何被管理/配置/同步

| # | 原语名 | 发音 | 语义 | 硬件成本 | 关键功能 |
|---|--------|------|------|---------|---------|
| C1 | **C.LINK** | /lɪŋk/ | SDI拓扑配置/Page Commit | ~2K LUT | 原子切换物理连线拓扑 |
| C2 | **C.TICK** | /tɪk/ | 全局分布式逻辑时钟 | <500 LUT | Lamport因果序时钟 |
| C3 | **C.SYNC** | /sɪŋk/ | Epoch边界同步/排空检测 | ~1K LUT | 全局屏障同步 |
| C4 | **C.MOVE** | /mu:v/ | DMA数据搬运/地址重映射 | ~3K LUT | 存算传数据编排 |

### 1.4 多 Tile 组网：从 Tile 到 Macrotile 到系统

`
   Tile 0          Tile 1          Tile 2          Tile 3
  +------+        +------+        +------+        +------+
  | SYN  |        | SYN  |        | SYN  |        | SYN  |
  | R.*  |        | R.*  |        | R.*  |        | R.*  |
  +--+---+        +--+---+        +--+---+        +--+---+
     |               |               |               |
  +--+---------------+--+------------+--+------------+--+
  |                 SDI 交换矩阵 (T.* 路由层)            |
  |  Crossbar 4x4 + VC + Page寄存器                    |
  +--+---------------+--+------------+--+------------+--+
     |               |               |               |
  [C.LINK]       [C.TICK]       [C.SYNC]       [C.MOVE]
     |               |               |               |
  ====化合键层 (SDI Bond Layer)====
     |               |               |               |
  Tile 4          Tile 5          Tile 6          Tile 7
`

**扩展路径**：4 Tile → Macrotile（16-64 Tile，单 FPGA）→ 晶圆级（256-1024 Macrotile）→ 多晶圆/机柜级（10^4-10^6 Tile），通过 SDI 化合键 Kronecker 积分形级联实现规模无关性扩展。

---

## 第二章：SDI 改变物理拓扑的底层原理与实现机理

这是 TCC 架构最核心、最区别化的技术。SDI（Software-Defined Interconnect）不是传统意义上的"网络交换机"，而是一个**可编程物理互连矩阵**——它直接改变芯片内部和芯片之间的**物理走线连接关系**，而非在固定物理走线上通过数据包头做逻辑转发。

### 2.1 传统交换机 vs SDI：根本区别

| 维度 | 传统交换机（CLOS/Dragonfly/IB） | SDI 交换矩阵 |
|------|---------------------------|-----------|
| **工作层** | 链路层/网络层（L2/L3 Packet Forwarding） | 物理层（L1 Circuit Switching） |
| **改变什么** | 修改数据包头 + 查路由表决定转发端口 | 修改物理走线的通断状态（Crossbar 配置） |
| **物理拓扑是否改变** | 否——物理连线固定，逻辑覆盖变化 | **是——物理走线关系直接改变** |
| **切换时间** | ms-s 级（路由协议收敛） | **~100 ns（原子 Page Commit）** |
| **切换粒度** | 逐流/逐包 | 全交换矩阵原子切换 |
| **硬件本质** | 包缓冲+查表+调度 | 可编程 Crossbar + Page寄存器 |

### 2.2 SDI Crossbar：物理拓扑可编程的核心器件

SDI 交换矩阵的物理实现是一个 **N×N 可编程 Crossbar Switch**，辅以 VC（Virtual Channel）分配表和 Page 寄存器。

#### 2.2.1 Crossbar 基本结构

`
        输入端口 (N条)
        I0    I1    I2    I3
        |     |     |     |
   O0 --+--+--+--+--+--+--+-- 可编程交叉点
        |  X  |     |     |    (每个交叉点 = 1个传输门+1个配置位)
   O1 --+--+--+--+--+--+--+--
        |     |  X  |     |
   O2 --+--+--+--+--+--+--+--
        |     |     |  X  |
   O3 --+--+--+--+--+--+--+--
        |     |     |     |  X
        输出端口 (N条)

每个交叉点 "X" 受 1-bit 配置寄存器控制：
  bit=1: 闭合（I_i 连接到 O_j）
  bit=0: 断开（I_i 与 O_j 隔离）

对于 N=4 的 Crossbar：
  配置寄存器 = 4*4 = 16 bits (2 bytes)
  可表达 2^16 = 65536 种拓扑（去除非连通后 ~10^4 种有效拓扑）
`

#### 2.2.2 Crossbar 配置如何对应不同拓扑

**示例 1：配置为 Ring 拓扑 (4节点)**

`
Crossbar 配置矩阵 (O=I映射)：
    I0  I1  I2  I3
O0  0   1   0   0    -> O0 接收来自 I1 的数据 (Tile1->Tile0)
O1  0   0   1   0    -> O1 接收来自 I2 的数据 (Tile2->Tile1)
O2  0   0   0   1    -> O2 接收来自 I3 的数据 (Tile3->Tile2)
O3  1   0   0   0    -> O3 接收来自 I0 的数据 (Tile0->Tile3)

物理效果：0->3->2->1->0 的环形物理走线
`

**示例 2：配置为 Butterfly 拓扑 (4节点)**

`
Crossbar 配置矩阵 (O=I映射)：
    I0  I1  I2  I3
O0  0   0   1   0    -> 0<->2 配对
O1  0   0   0   1    -> 1<->3 配对
O2  1   0   0   0    -> 2<->0 配对
O3  0   1   0   0    -> 3<->1 配对

物理效果：[[0,2],[1,3]] 蝶形配对，支持 AllReduce 最优归约
`

#### 2.2.3 从 Crossbar 到全拓扑：多级 + VC + 化合键

单个 4×4 Crossbar 仅能表达 4 节点间的任意连接。扩展到更大规模需要三层机制：

**Layer 1: 多级 Crossbar 级联（物理规模扩展）**
`
   Tile 0-3           Tile 4-7           Tile 8-11
  [SDI 4x4]          [SDI 4x4]          [SDI 4x4]
      |                  |                  |
      +----[SDI 4x4]----+----[SDI 4x4]----+
                  |                  |
            [SDI Inter-Macrotile Crossbar]
`
多级级联将 N 个 4×4 Crossbar 组成规模为 4N 的等效交换网络，网络直径保持 O(log N)。

**Layer 2: VC（Virtual Channel）分配——同一物理走线上的多逻辑通道**
`
  物理走线 A-B (1对差分线)
    |
    +-- VC0: 训练梯度流 (高带宽, 低优先级)
    +-- VC1: 推理激活流 (低延迟, 高优先级)
    +-- VC2: 控制信令 (C.LINK/C.SYNC)
    +-- VC3: 预留
`
VC 使同一物理走线可同时承载多个逻辑通信流，在拓扑切换期间（Page Commit 窗口）由 Epoch 边界排空保证数据完整性。

**Layer 3: SDI 化合键（分形级联的数学基础）**
`
5 类化合键算子，将小规模拓扑合成为大规模拓扑：
  平行键（笛卡尔积）  : G1 □ G2  = 规模化复制 (如 4x4 -> 8x8 Mesh)
  交叉键（Kronecker积）: G1 ⊗ G2  = 分形自相似扩展 (关键！)
  融合键（强乘积）    : G1 ⊠ G2  = 紧耦合 (如 Ring ⊠ Tree)
  叠加键（图并集）    : G1 ∪ G2  = 松耦合异构融合
  替换键（图替换）    : G1 ⊲ G2  = 局部拓扑替换
`
Kronecker 积是最关键的化合键算子——通过对小"种子图"反复施加 Kronecker 积，可生成具有自相似分形结构的大规模网络，且保持幂律度分布、小世界特性和社区结构。**这是 TCC 从 10^2 核扩展到 10^8 核的数学基础。**

### 2.3 Page Commit：纳秒级拓扑切换的原子操作

Page Commit 是 SDI 实现拓扑液态化的关键控制原语（C.LINK）。其工作流程如下：

`
Epoch N (工作在拓扑 Page A)            Epoch N+1 (工作在拓扑 Page B)
  +----------------------+   切换窗口    +----------------------+
  | 计算 + 通信           | ~~~~~~~~~~>  | 计算 + 通信           |
  | 拓扑: Butterfly      |              | 拓扑: Ring           |
  +----------------------+              +----------------------+
         |                                      |
    检测到任务切换请求                       C.SYNC Barrier 释放
         |                                      |
    C.SYNC 排空在途数据                       新拓扑开始运行
         |
    C.LINK.PageCommit(page_B)
         |
    +---+---+---+---+
    | 并行写入所有 SDI |  <- 多 Bank BRAM 并行读取
    | Crossbar 配置位 |  <- 每个 Crossbar 16-256 bits
    | VC 分配表       |  <- 每个 Crossbar 64-512 bits
    | Epoch 掩码      |  <- 每个 Tile 1 bit
    +---+---+---+---+
         |
    ~100 ns 后：全交换矩阵已切换至 Butterfly
`

**切换时间分析**：
- 单个 Crossbar 4×4 配置：16 bits，1 个 BRAM 读取周期 ≈ 5 ns
- N 个 Crossbar 并行配置（多 Bank BRAM 同时读取）：仍 5-10 ns
- 加上排空+同步开销：总计 **<100 ns (16节点), <500 ns (256节点)**
- 对比传统交换机的路由协议收敛时间（ms-s 级）：**快 10^4-10^7 倍**

### 2.4 Topology Page 的预编译与存储

`
  FPGA Block RAM 中的 Page 存储布局：

  +--------------------------------------------------+
  | Page ID | 拓扑类型  | Crossbar配置 | VC表 | Epoch掩码 |
  +--------------------------------------------------+
  | P01     | Butterfly | 0x1248...    | ...  | 0xFF     |
  | P02     | Ring      | 0x2481...    | ...  | 0xFF     |
  | P03     | 2D Mesh   | 0x3614...    | ...  | 0xFF     |
  | P04     | Fat-Tree  | 0x482C...    | ...  | 0xFF     |
  | ...     | ...       | ...          | ...  | ...      |
  | P12     | Hybrid    | 0xFEDC...    | ...  | 0xFF     |
  +--------------------------------------------------+

  每个 Page: 1-4 KB (取决于 Crossbar 规模和 VC 表大小)
  12个 Page: ~50 KB (仅占 VU13P Block RAM 的 ~10%)
`

---

## 第三章：四种场景的完整工作流

### 3.1 场景一：纯推理 (Pure Inference)

**任务特征**：单向数据流（输入→各层→输出），低延迟要求，batch 可大可小。不需要反向传播和梯度同步。

`
时间轴
|
|  C.LINK.Commit(P08: Pipeline Ring)
|  C.SYNC Barrier
|
|  +-- Epoch 1: Pipeline Ring 推理 --+
|  |                                    |
|  |  Tile0      Tile1      Tile2       |
|  |  [Embed] -> [Layer1] -> [Layer2]   |
|  |    |          |          |         |
|  |  R.PIPE   R.PIPE    R.PIPE        |  <- 层间数据流水线传输
|  |    |          |          |         |
|  |  T.GEMM   T.GEMM    T.GEMM        |  <- 每层矩阵乘
|  |  T.LOOK   T.LOOK    T.LOOK        |  <- 每层 LayerNorm
|  |  T.MAPS   T.MAPS    T.MAPS        |  <- 每层 GELU
|  |    |          |          |         |
|  |  C.MOVE   C.MOVE    C.MOVE        |  <- KV Cache 管理
|  |                                    |
|  +-- 延迟: tau < 100us/batch ---------+
|
|  若 batch>1 需要 AllReduce（如多卡推理）：
|  C.LINK.Commit(P01: Butterfly)
|  T.FUSE(梯度/激活) + T.PIPE(层间) 混合
v
`

**推理场景 R.T.C 原语编排**：
| 阶段 | R.* Route 原语 | T.* Transform 原语 | C.* Control 原语 |
|------|------------|------------|------------|
| Layer Forward | R.PIPE（层间传递） | T.GEMM（矩阵乘）、T.LOOK（LayerNorm）、T.MAPS（激活） | C.MOVE（KV Cache读写） |
| Token Generation | R.PIPE（逐token） | T.GEMM + T.LOOK + T.MAPS | C.TICK（因果时钟序） |
| 多卡推理归约 | R.FUSE（AllReduce） | T.FOLD（归约） | C.SYNC（Epoch同步） |
| 拓扑切换 | — | — | C.LINK.Commit(P08→P01) |

### 3.2 场景二：纯训练 (Pure Training)

**任务特征**：双向数据流（前向+反向），梯度 AllReduce 同步是核心瓶颈，大规模 N 下通信效率决定扩展性。

`
时间轴
|
|  C.LINK.Commit(P01: Butterfly)  <- 梯度同步选Butterfly最优
|  C.SYNC Barrier
|
|  +-- Epoch 1: 训练迭代 --+
|  |                         |
|  |  [Forward Pass]         |
|  |  R.PIPE (层间前向)      |
|  |  T.GEMM + T.MAPS       |
|  |                         |
|  |  [Backward Pass]        |
|  |  R.PIPE (层间反向梯度)  |
|  |  T.GEMM (梯度计算)      |
|  |                         |
|  |  [AllReduce 梯度同步]   |
|  |  R.FUSE (Butterfly)     |  <- Butterfly 归约效率最高
|  |  T.FOLD (局部归约)      |  <- 节点内先局部归约
|  |                         |
|  |  若N>1024, 可切换:      |
|  |  C.LINK.Commit(P07: Dragonfly)
|  |  R.FUSE + R.SWAP (混合) |  <- 大规模下Dragonfly更优
|  +-------------------------+
v
`

**训练场景 R.T.C 原语编排**：
| 阶段 | R.* Route 原语 | T.* Transform 原语 | C.* Control 原语 |
|------|------------|------------|------------|
| Forward Pass | T.PIPE | T.GEMM + T.MAPS + R.LOOK | C.MOVE（激活检查点） |
| Backward Pass | T.PIPE | T.GEMM + T.MAPS | — |
| Gradient AllReduce | **T.FUSE**（Butterfly/Dragonfly） | T.FOLD（节点内归约） | C.SYNC |
| Weight Update | — | T.MAPS（逐元素 SGD/Adam） | — |
| Scale-out切换 | R.FUSE + R.SWAP | — | C.LINK.Commit(P01→P07) |

### 3.3 场景三：训推一体 (Train-Inference Unified)

**任务特征**：训练和推理交替或并发。需要拓扑在"梯度同步拓扑"（Butterfly/Dragonfly）和"推理流水线拓扑"（Pipeline Ring）之间快速切换。这是 TCC 液态拓扑最典型的应用场景。

`
时间轴
|
|  C.LINK.Commit(P01: Butterfly)
|  +-- Epoch N: 训练（前向+反向+梯度同步）--+
|  |  R.FUSE (Butterfly AllReduce 梯度)      |
|  |  R.PIPE (层间传输)                      |
|  |  R.GEMM + R.FOLD + R.MAPS              |
|  +----------------------------------------+
|
|  C.SYNC 排空训练梯度流
|  C.LINK.Commit(P08: Pipeline Ring)  <- 100ns 切换
|  C.SYNC Barrier
|
|  +-- Epoch N+1: 推理验证 --+
|  |  T.PIPE (流水线推理)     |
|  |  T.GEMM + T.LOOK + T.MAPS
|  |  C.MOVE (KV Cache)      |
|  +-------------------------+
|
|  C.SYNC 排空推理激活流
|  C.LINK.Commit(P01: Butterfly)  <- 100ns 切回
|
|  +-- Epoch N+2: 训练 --+
|  |  ...                  |
|  +-----------------------+
v

**关键指标**：
- kappa = 切换时间内有效计算保持率 >= 95%
- sigma = 训推切换性能退化率 <= 5%
- 切换开销 / Epoch长度 = 200ns / 10us = 2%（典型情况）

**混合拓扑 Page**（P09 Hybrid Mesh+Ring）：训练前向/反向使用 Mesh 邻居通信（减少拥塞），梯度 AllReduce 使用 Butterfly 归约（高效率），推理使用同一 Mesh 的部分子环（资源复用）。Page 切换在 Epoch 边界完成，切换开销 < 1%。

### 3.4 场景四：信号处理（FFT/DBF）

**任务特征**：FFT 蝶形计算图与 AllReduce 通信图存在图论同构（FFT-AllReduce 同构定理），可以在同一套物理走线上完成 AI 训练和信号处理，无需额外布线。DBF（数字波束形成）本质是 MIMO 矩阵运算，可映射为 R.GEMM + T.SWAP。

`
  FFT 蝶形计算图 (8点基-2 FFT, 3层)     AllReduce 通信图 (8节点超立方体)
                                           
  Stage 0    Stage 1    Stage 2          Dim 0    Dim 1    Dim 2
  x0--+      x0--+      x0--+            N0--+    N0--+    N0--+
      |          |          |                |        |        |
  x4--+      x2--+      x1--+            N4--+    N2--+    N1--+
  x2--+      x4--+      x2--+            N2--+    N4--+    N2--+
      |          |          |                |        |        |
  x6--+      x6--+      x3--+            N6--+    N6--+    N3--+
  x1--+      x1--+      x4--+            N1--+    N1--+    N4--+
      |          |          |                |        |        |
  x5--+      x3--+      x5--+            N5--+    N3--+    N5--+
  x3--+      x5--+      x6--+            N3--+    N5--+    N6--+
      |          |          |                |        |        |
  x7--+      x7--+      x7--+            N7--+    N7--+    N7--+

  定理 phi: B_k -> A_k 是同构映射 (FFT-AllReduce同构定理)
  phi(b_{l,i}) = a_{l,i}   (第l层蝶形单元 -> 第l维归约通信节点)
  物理走线完全相同！只需 SDI Page 切换重组连接关系。
`

**FFT 场景 R.T.C 原语编排**：
| 阶段 | R.* Route 原语 | T.* Transform 原语 | C.* Control 原语 |
|------|------------|------------|------------|
| 数据重排（Bit-Reversal） | T.SWAP（全交换） | — | C.MOVE（地址重映射） |
| 蝶形计算（Stage 0..k-1） | T.FUSE（AllReduce走线复用为蝶形） | **R.SCAN**（蝶形乘加单元） | C.TICK（Stage 同步） |
| 旋转因子乘 | — | R.SPEC（CORDIC sin/cos） | — |
| DBF 波束形成 | T.SWAP（天线数据全交换） | R.GEMM（波束权值矩阵乘） | C.SYNC（帧同步） |

**关键增益**：传统系统中 AI 训练需要 Butterfly 互连，FFT 需要蝶形互连，两者需要分别设计和布线（或通过总线共享导致带宽减半）。FFT-AllReduce 同构定理保证了同一套物理走线可以 100% 复用——通过 SDI Page 切换改变 Crossbar 配置，**同一组导线在 Epoch N 执行 AllReduce，在 Epoch N+1 执行 FFT 蝶形计算，物理上无任何改动，仅寄存器配置不同**。

---

## 第四章：总结——R.T.C 原语在三层架构中的协同

### 4.1 一次完整的拓扑切换生命周期

`
Step 1: [C.TICK] 记录 Epoch 结束时刻的全局逻辑时钟
Step 2: [C.SYNC] 全局排空——等待所有在途数据到达目的地
Step 3: [C.LINK] Page Commit——并行写入所有 SDI Crossbar 配置位
Step 4: [C.SYNC] Barrier 释放——确认所有节点完成配置
Step 5: [C.TICK] 记录新 Epoch 开始时刻
Step 6: R.* + T.* 在新拓扑上开始下一轮计算和通信

总切换延迟 = T_drain + T_commit + T_barrier
            = ~50ns  + ~10ns    + ~40ns
            = ~100ns (16节点, N=4 Crossbar)
            = ~500ns (256节点, 多级 Crossbar)
`

### 4.2 四场景拓扑切换总览

| 场景切换 | 源拓扑 Page | 目标拓扑 Page | 切换原因 | 切换频率 | 关键 T.* | 关键 R.* |
|---------|-----------|------------|---------|---------|---------|---------|
| 推理→训练 | P08 Pipeline Ring | P01 Butterfly | 需梯度 AllReduce | 每 Epoch | R.PIPE→R.FUSE | R.GEMM (共用) |
| 训练→推理 | P01 Butterfly | P08 Pipeline Ring | 推理验证 | 每 N Epoch | R.FUSE→R.PIPE | R.GEMM + R.LOOK |
| 训练→信号处理 | P01 Butterfly | P06 Hypercube | FFT 蝶形复用 | 按需 | R.FUSE→R.FUSE+T.SCAN | R.SCAN |
| 信号处理→训练 | P06 Hypercube | P01 Butterfly | 回归 AI 训练 | 按需 | T.SCAN→R.FUSE | T.SCAN→T.GEMM |
| 规模扩展 | P01 Butterfly(64卡) | P07 Dragonfly(1024卡) | N 超过阈值 | 配置级 | R.FUSE→R.FUSE+R.SWAP | — |
| 多传感器融合 | P08 Pipeline | P10 Multi-Tree | 多数据源汇聚 | 按需 | R.PIPE→R.CAST | T.GEMM→T.FOLD |

### 4.3 核心论断

1. **R.T.C 三层正交**：路由（R.*）操作节点间数据，变换（T.*）操作节点内数据，控制（C.*）操作系统状态。三者无重叠、无冗余，构成代数完备的 16 原语体系。

2. **SDI 是物理层可编程**：SDI 不是传统交换机——它直接改变 Crossbar 矩阵的物理通断状态，在物理层重构走线关系。切换通过 Page Commit 原子完成，**100 ns 内实现全交换矩阵拓扑切换**，比传统网络协议收敛快 10^4-10^7 倍。

3. **FFT-AllReduce 同构是关键武器**：FFT 蝶形计算图与 AllReduce 通信图在图论上严格同构，同一组物理走线在训练 Epoch 执行 AllReduce，在信号处理 Epoch 执行 FFT 蝶形——**物理布线 100% 复用**，这是 TCC 实现 AI+信号处理统一架构的数学基础。

4. **化合键分形级联解决扩展性**：5 类 SDI 化合键（平行/交叉/融合/叠加/替换）通过 Kronecker 积的自相似迭代，实现从单芯粒到晶圆到机柜的规模无关性扩展——**拓扑的涌现属性（模块化 Q、小世界性 sigma、雪崩指数 alpha）在六个数量级的规模变化中保持恒定**。

---

**关联条目**：[[TCC计算范式命名规范3.0]] | [[TCC_iNEST_LiquidTopology_v1.0]] | [[iNEST_Roadmap_v2.0_权威路线图]] | [[TCC_Core_Concepts]] | [[SDI_Four_Rules_v5_FINAL]] | [[基于元拓扑与SDI化合键的通信原语生成理论]]

---

*版本 v1.0 | 2026-07-08 | 基于 TCC 命名规范3.0 + SDI 架构知识库综合撰写*

---
## 相关链接
- [[TCC_RTC原语架构与SDI拓扑变换机理_v1.0]]
- [[tcc_first_principles]]
- [[TCC原语体系统一方案_v1.0_已归档]]
- [[2026-06-28_Getnote_2026-06-28_TCC BP]]
- [[GetNote_20260606_100554_kb_patent_getnote_1907743949763445776_一种基于正交原语集与拓扑融合变换的网络复杂度计算方法及系统]]
