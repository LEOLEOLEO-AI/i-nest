---
direction: TCC
category: 理论
tags: [topology-centric-computing, communication-as-computation, algebraic-framework, dataflow-graph, graph-isomorphism, TCC-11, reconfigurable-interconnect]
summary: "条件性路由-变换等价框架，拓扑兼容时通信可转化为计算。"
quality: high
processed: 2026-08-11 21:18
---
---
title: getnote_1917118403083276376_Route≡Transform：拓扑兼容条件下通信即计算的代数框架与拓扑中心计算原语体系
tags:
  - semiconductor
  - physics
  - green-ai
  - llm
  - network
  - computing
  - first-principles
  - tcc
  - ai
  - cst
  - transformer
  - sdi-bond
  - fpga
  - hardware
  - infrastructure
  - energy
  - architecture
  - design
  - chip
date: 2026-07-31 08:14
source: GetNotes
score: 46
provenance: external
---

## Original Note

---
note_id: 1917118403083276376
title: "Route≡Transform：拓扑兼容条件下通信即计算的代数框架与拓扑中心计算原语体系"
type: plain_text
created: 2026-07-31 07:54:07
source: getnote
kb: 
---

# Route≡Transform：拓扑兼容条件下通信即计算的代数框架与拓扑中心计算原语体系

下面给出**中文正式全文稿**。我已将核心命题统一修订为“条件性 Route≃Transform”，保留品牌锋芒，但把可证明边界、系统假设和评测口径全部压实，适合后续直接翻译为 ASPLOS 英文版。

---

# Route≡Transform：拓扑兼容条件下通信即计算的代数框架与拓扑中心计算原语体系

**副标题：A Conditional Algebraic Framework of Communication-as-Computation for Topology-Centric Computing**

## 摘要

本文提出 **Route≃Transform**，一种面向拓扑中心计算的条件性代数框架。与“通信与计算普适等价”的强命题不同，本文证明：当任务数据流阶段与可重构路由拓扑之间存在保持标签、方向、带宽、顺序、精度和算子语义的图同构，或存在低失真图嵌入时，部分通信阶段可以由拓扑状态与端点局部计算共同实现，从而转化为拓扑内空间变换。

本文将这一原则形式化为**条件性路由—变换等价**。给定数据流阶段 (H) 与拓扑状态 (S)，若存在标签保持映射 (\phi)，使得 (H) 的依赖边、算子标签和资源约束均被 (S) 覆盖，则拓扑执行 (\operatorname{Exec}*{S}) 与原始数据流变换 (\mathcal{F}*{H}) 满足置换共轭等价：

[  
\operatorname{Exec}*{S}(P*{\phi}x)=P_{\phi}\mathcal{F}_{H}(x)  
]

若仅存在近似嵌入，则收益由路径膨胀、链路拥塞、填充因子、残余通信比例和拓扑配置开销共同界定。

在此基础上，本文定义 **TCC-11**，即拓扑中心计算的 11 个路由与计算原语。TCC-11 不被表述为全计算域的绝对最小完备 ISA，而是被证明为面向 Transformer、CNN、FFT、SpMV、MoE、GNN 和雷达 DBF 等目标工作负载族的表达完备 primitive basis，并在显式代价模型下具有相对不可约性。

本文进一步给出三个结构性推论：第一，radix-2 FFT 的通信骨架与 Butterfly／Hypercube 拓扑分阶段同构，旋转因子乘法保留为局部计算；第二，MoE token dispatch 可表示为稀疏 AlltoAll，其 dispatch 与 combine 矩阵构成转置对；第三，当 CFAR 滑窗统计量具有结合性时，其检测过程可映射为 prefix／segmented scan。

本文在 4 节点 FPGA 原型和扩展至 1024 节点的周期精确模拟器上验证该框架。结果表明，在 resident-data、compute-bound 且拓扑兼容度高的阶段，TCC 可减少显式内存暂存和协议开销，实现亚微秒级逻辑拓扑切换，并在模拟中维持高利用率扩展。本文的结论是：**网络不能无条件等价为计算；但当数据流图与路由拓扑发生结构共振时，拓扑可以成为计算。**

**关键词：** 拓扑中心计算；可重构互连；通信即计算；数据流图；图同构；Transformer；MoE；FFT；GNN；FPGA；软件定义互连。

---

## 1. 引言

数据搬移已经成为现代计算系统的主导瓶颈之一。Horowitz 的能耗分析表明，在先进工艺下，简单算术操作的能耗通常远低于跨层级存储访问和片外数据搬移能耗。随着大模型、图计算、稀疏专家模型和多模态边缘智能系统扩展到数百甚至数千节点，系统性能越来越少由单点峰值算力决定，而越来越多由内存暂存、通信协议、同步等待和集体通信效率决定。

传统体系结构长期将计算与通信分离。计算节点执行矩阵乘法、卷积、规约或控制流，网络交换设备负责搬移数据包。这个分离假设对通用系统是自然的，但对许多结构化分布式工作负载而言并不总是最优。FFT 的蝶形交换、MoE 的 token 到 expert 分发、GNN 的邻域聚合、雷达 DBF 的流式扫描，本身既是通信模式，又是算法结构的一部分。

本文提出的问题是：**在什么条件下，网络不再只是被动传输层，而可以成为任务数据流变换的空间实现？**

本文的答案是条件性的。路由与计算并不普适等价。但当一个数据流阶段的依赖图与可重构拓扑图之间存在精确图同构或低失真嵌入时，该阶段中的数据移动、置换、规约、扫描、广播或稀疏分发可以被拓扑状态原生执行。本文将这一原则称为 **Route≃Transform**。

符号 (\simeq) 是刻意选择的。它表示条件性等价，而不是无约束恒等。若兼容条件完全满足，则拓扑执行与数据流执行严格等价；若条件部分满足，则系统收益由残余通信和嵌入代价决定；若拓扑完全不兼容，TCC 会退化为传统通信路径，不产生结构性增益。

这一修正使本文命题更接近可验证的系统科学，而不是宣言式架构愿景。本文并不声称用路由替代任意计算，也不声称违反 Amdahl 定律。本文的主张是：**通过发现和利用任务数据流图与物理／逻辑路由图之间的结构共振，可以显著降低兼容阶段的有效通信开销。**

### 1.1 本文贡献

本文作出如下贡献。

**第一，条件性 Route≃Transform 理论。** 本文定义数据流阶段与拓扑状态之间的精确兼容性和近似兼容性，并证明精确兼容性蕴含输出等价。

**第二，TCC-11 原语体系。** 本文定义 11 个路由与计算原语，覆盖典型拓扑中心工作负载。本文证明的是目标工作负载族表达完备性与代价模型下的相对不可约性，而不是全计算域绝对最小性。

**第三，三个结构性推论。** 本文证明 FFT 通信骨架、MoE 稀疏 dispatch、CFAR 滑窗统计分别对应 Butterfly／Hypercube、稀疏转置和前缀扫描等拓扑结构。

**第四，编译器与运行时模型。** 本文给出从数据流图到拓扑状态序列的编译流程，包括兼容性检测、嵌入选择、残余通信处理和代价模型判断。

**第五，硬件与模拟评测。** 本文基于 4 节点 FPGA 原型和 1024 节点周期精确模拟器，展示拓扑兼容阶段中的低延迟切换、数据搬移减少和高利用率扩展。

### 1.2 非目标声明

本文不主张任意计算均可由路由替代。

本文不主张 TCC 绕过 Amdahl 定律，而是降低拓扑兼容阶段的有效串行通信比例。

本文不主张 TCC-11 是所有可能体系结构中的唯一最小 ISA，而是主张其对目标工作负载族具有表达完备性，并在指定代价模型下具有相对不可约性。

本文不将物理光路毫秒级重构与逻辑路由表亚微秒级切换混为一谈。本文 Route≃Transform 依赖的是逻辑拓扑状态快速切换。

---

## 2. 背景与动机

### 2.1 数据搬移能耗墙

在现代计算系统中，算术能耗与数据搬移能耗之间存在数量级差异。Horowitz 在 ISSCC 2014 中给出的数据表明，浮点运算、片上 SRAM 访问、片外 DRAM 访问之间能耗差异可以达到一个到两个数量级。尽管具体数值随工艺、位宽、频率和电压而变化，但总体趋势十分稳定：**越远的数据搬移越昂贵。**

在 GPU、TPU、NPU 和 FPGA 集群中，这一问题进一步放大。单芯片矩阵乘法吞吐率极高，但跨 HBM、PCIe、NVLink、以太网或光互连的数据流动会造成显著开销。对分布式大模型而言，AllReduce、AllGather、ReduceScatter 和 AlltoAll 等 collective 操作往往产生通信气泡，使算力单元等待数据到达。

### 2.2 传统通信优化的边界

传统系统通常从通信协议角度优化 collective。例如，环形 AllReduce 优化带宽利用率，树形 AllReduce 降低延迟，高阶 NVSwitch 或 InfiniBand 拓扑减少跳数，NCCL 和类似运行时根据拓扑生成调度计划。这些方法非常有效，但它们仍然默认通信与计算是两个阶段：先搬运数据，再执行计算。

问题在于，部分通信模式本身已经是计算图的一部分。FFT 的交换模式决定频域变换结构；MoE dispatch 的稀疏 AlltoAll 决定专家计算输入；GNN 的邻接聚合决定消息传递；CFAR 的滑窗扫描决定检测统计量。如果网络拓扑可以直接塑造这些依赖结构，那么通信阶段就不再只是搬运，而可以成为空间计算。

### 2.3 现有范式与 TCC 差异

**In-network computing** 将部分规约操作下沉到交换机或网卡，例如 SUM、MAX、MIN 等。这证明网络可以执行有限计算，但其原语通常较窄，难以覆盖稀疏 dispatch、scan、动态拓扑压缩和数据流图级结构映射。

**Processing-in-memory／near-data computing** 将计算移动到存储附近，降低内存访问代价。TCC 的方向不同：它不是把计算移入存储，而是把可拓扑化的数据流阶段移入互连结构。

**Wafer-scale computing** 通过晶圆级集成降低片外边界，但很多实现仍依赖相对固定的二维 mesh 或局部互连结构。对于 Butterfly、AlltoAll、稀疏图和动态 MoE 等非网格通信模式，静态拓扑可能产生低效映射。

**CGRA 与空间数据流体系结构** 在芯片内部重构数据通路。TCC 可以视为将空间重构思想扩展到分布式互连尺度，并用图同构和图嵌入条件给出形式化边界。

### 2.4 拓扑中心计算的核心假设

TCC 的核心假设是：若可重构互连能够在时间上快速切换逻辑拓扑状态，在空间上形成与任务数据流阶段匹配的连接图，那么网络不仅能传输数据，还能通过连接关系、规约树、扫描链、稀疏压缩和局部算子共同实现变换。

因此，TCC 的关键不是“网络很快”，而是“网络形状正确”。当拓扑形状与数据流图匹配时，数据不再需要被反复写回内存、重新寻址、再由软件协议搬移，而是在一次拓扑执行中完成交换、聚合或扫描。

---

## 3. 理论：条件性路由—变换等价

### 3.1 数据流阶段与拓扑状态

设一个分布式工作负载可被划分为若干数据流阶段。每个阶段表示为带标签有向图：

[  
H=(U,F,\alpha,\lambda)  
]

其中，(U) 表示逻辑顶点，包括张量分片、算子实例或状态单元；(F\subseteq U\times U) 表示数据依赖边；(\alpha(u)) 表示顶点 (u) 上的局部计算；(\lambda(e)) 表示边 (e) 的语义标签。

边标签至少包含：

[  
\lambda(e)=  
\left(  
\operatorname{op}*{e},*  
*\operatorname{shape}*{e},  
\operatorname{dtype}_{e},  
b_e,  
o_e,  
q_e  
\right)  
]

其中，(\operatorname{op}*{e}) 表示恒等传输、置换、广播、收集、规约、扫描或稀疏搬移等语义；(\operatorname{shape}*{e}) 表示张量形状；(\operatorname{dtype}_{e}) 表示数据类型；(b_e) 表示带宽需求；(o_e) 表示顺序约束；(q_e) 表示精度与数值一致性约束。

一个可重构拓扑状态表示为：

[  
S=(P,L,\beta,\mu)  
]

其中，(P) 表示物理端点；(L\subseteq P\times P) 表示当前激活的逻辑链路；(\beta(p)) 表示端点 (p) 的局部计算能力；(\mu(l)) 表示链路 (l) 支持的传输、置换、广播、规约、扫描或流控能力。

数据流阶段定义变换：

[  
\mathcal{F}*H:\mathcal{X}*{U}\rightarrow \mathcal{Y}_{U}  
]

拓扑状态及其端点／链路算子定义空间执行：

[  
\operatorname{Exec}*{S}:\mathcal{X}*{P}\rightarrow \mathcal{Y}_{P}  
]

Route≃Transform 要回答的问题是：在什么条件下，(\operatorname{Exec}*{S}) 可以作为 (\mathcal{F}*{H}) 的拓扑实现。

### 3.2 精确拓扑兼容性

若存在映射：

[  
\phi:U\rightarrow P  
]

并满足邻接保持、标签保持、端点算子保持、资源可行和数值一致性，则称 (H) 与 (S) 精确拓扑兼容。

**邻接保持：**

[  
(u,v)\in F  
\Rightarrow  
(\phi(u),\phi(v))\in L  
]

若拓扑中存在额外有效边，则该边必须被屏蔽，或仅执行不影响输出的恒等操作。

**标签保持：**

[  
\lambda(u,v)\preceq \mu(\phi(u),\phi(v))  
]

其中，(\preceq) 表示能力包含关系。例如，若逻辑边要求 SUM 规约，则对应拓扑边或端点必须支持相同代数结构下的 SUM 规约。

**端点算子保持：**

[  
\alpha(u)\preceq \beta(\phi(u))  
]

**资源可行：**

[  
b_{u,v}\leq B_{\phi(u),\phi(v)}  
]

[  
\tau_{\phi(u),\phi(v)}\leq \tau_{\max}  
]

若多个逻辑边共享同一物理资源，还需满足聚合带宽约束和无死锁流控约束。

用带标签邻接矩阵表示，设 (A_H) 为数据流阶段的带标签邻接矩阵，(A_S) 为拓扑状态的带标签邻接矩阵，(P_{\phi}) 为映射 (\phi) 对应的置换矩阵，则精确兼容性可表示为：

[  
A_S|*{\phi(U)}*  
*\succeq*{\Lambda}  
P_{\phi}A_HP_{\phi}^{\top}  
]

若进一步要求无多余有效边，则有：

# [  
A_S|_{\phi(U)}

P_{\phi}A_HP_{\phi}^{\top}  
]

### 3.3 定理一：条件性路由—变换等价

**定理一。** 设数据流阶段 (H=(U,F,\alpha,\lambda)) 与拓扑状态 (S=(P,L,\beta,\mu)) 精确拓扑兼容。若所有边算子和端点算子均满足标签保持、顺序保持和数值一致性要求，则拓扑执行与数据流执行输出等价。即对任意输入 (x\in\mathcal{X}_{U})，有：

# [  
\operatorname{Exec}*{S}(P*{\phi}x)

P_{\phi}\mathcal{F}_{H}(x)  
]

等价地：

# [  
\mathcal{F}_{H}

P_{\phi}^{-1}  
\operatorname{Exec}*{S}*  
*P*{\phi}  
]

**证明。** 由于 (H) 与 (S) 精确拓扑兼容，映射 (\phi) 保持所有逻辑顶点和拓扑端点之间的对应关系。对任意数据依赖边 ((u,v)\in F)，拓扑中存在对应激活边 ((\phi(u),\phi(v))\in L)，且其操作标签满足 (\lambda(u,v)\preceq \mu(\phi(u),\phi(v)))。因此，数据流图中的每一次依赖传输、置换、广播、规约或扫描，都可以在拓扑状态中找到语义一致的空间实现。

进一步，由端点算子保持条件可知，每个逻辑顶点 (u) 上的局部计算 (\alpha(u))，由物理端点 (\phi(u)) 上的 (\beta(\phi(u))) 实现。由顺序保持条件可知，若数据流阶段要求有序到达、有序扫描或确定性规约，则对应拓扑状态执行相同顺序或满足同等数值约束。

若 (H) 为无环数据流图，可按拓扑序将其划分为若干层。对第一层输入，(P_{\phi}) 仅改变数据放置位置，不改变数值。假设第 (t) 层执行后，拓扑状态中的中间张量等于数据流执行中间张量的 (P_{\phi}) 置换。由于第 (t+1) 层所有输入边和局部算子均由同构拓扑边与端点算子实现，第 (t+1) 层输出仍保持同样置换关系。由数学归纳法，最终输出满足定理结论。

若 (H) 包含状态或循环结构，可将其按有限时间窗展开为时序数据流图，对每个时间步重复上述归纳过程，即可得到相同结论。证毕。

### 3.4 近似兼容性与残余代价

实际系统中的拓扑通常无法完全匹配任意数据流图。因此，本文定义近似兼容性。若每条逻辑边 (e\in F) 可以映射为拓扑中的一条路径 (\psi(e))，则称 (\psi) 为从数据流阶段到拓扑状态的图嵌入。

嵌入代价由最大路径长度、最大链路拥塞、填充因子和残余通信比例刻画：

[  
\Delta=\max_{e\in F}|\psi(e)|  
]

[  
\Gamma=  
\max_{l\in L}  
\frac{\sum_{e:l\in\psi(e)} b_e}{B_l}  
]

[  
\kappa=  
\frac{\text{实际传输槽位数}}{\text{有效数据槽位数}}  
]

[  
r=  
\frac{\sum_{e\in F_{\mathrm{res}}}w(e)}  
{\sum_{e\in F}w(e)}  
]

定义拓扑兼容度：

[  
\chi(H,S)=1-r  
]

一个阶段采用 TCC 执行的总时间为：

# [  
T_{\mathrm{TCC}}

T_{\mathrm{local}}  
+  
T_{\mathrm{cfg}}  
+  
T_{\mathrm{embed}}(\Delta,\Gamma,\kappa)  
+  
T_{\mathrm{res}}®  
]

传统执行通信相关时间为：

# [  
T_{\mathrm{base}}

T_{\mathrm{local}}  
+  
T_{\mathrm{stage}}  
+  
T_{\mathrm{packet}}  
+  
T_{\mathrm{sync}}  
]

因此，TCC 获得正收益的条件是：

[  
T_{\mathrm{stage}}  
+  
T_{\mathrm{packet}}  
+  
T_{\mathrm{sync}}

>

T_{\mathrm{cfg}}  
+  
T_{\mathrm{embed}}(\Delta,\Gamma,\kappa)  
+  
T_{\mathrm{res}}®  
]

该不等式给出 Route≃Transform 的系统边界：只有当节省的内存暂存、协议处理和同步开销大于拓扑配置、嵌入失真和残余通信代价时，拓扑中心执行才具有收益。

### 3.5 结构性推论

**推论一：FFT 通信骨架与 Butterfly／Hypercube 同构。** 对 (N=2^k) 点 radix-2 Cooley–Tukey FFT，第 (s) 个阶段的通信交换关系为：

[  
j=i\oplus 2^s  
]

该关系与 (k) 维超立方体在第 (s) 个维度上的邻接关系一致。因此，FFT 的通信骨架与 (k=\log_2N) 个 Butterfly／Hypercube 拓扑状态精确兼容。完整 FFT 仍需局部复数乘法和加减法：

# [  
\begin{bmatrix}  
x_i’\  
x_j’  
\end{bmatrix}

\begin{bmatrix}  
1 & \omega_s\  
1 & -\omega_s  
\end{bmatrix}  
\begin{bmatrix}  
x_i\  
x_j  
\end{bmatrix}  
]

因此，准确表达为：

[  
\mathrm{FFT}*{N}*  
*\simeq*  
*\prod*{s=0}^{\log_2N-1}  
\left(  
\mathrm{LINK}*{s}*  
*+*  
*\mathrm{LocalTwiddle}*{s}  
+  
\mathrm{FUSE}_{s}  
\right)  
]

**推论二：MoE Dispatch 是稀疏 AlltoAll／分布式转置。** 设 MoE 中有 (T) 个 token 和 (E) 个 expert，门控网络产生稀疏分配矩阵：

[  
D\in{0,1}^{T\times E}  
]

Dispatch 阶段为：

[  
Y=D^{\top}X  
]

Combine 阶段为：

[  
X’=DZ  
]

因此，dispatch 与 combine 在结构上构成稀疏转置对。TCC 加速的是门控结果确定后的 token 分发和结果回收阶段，而不是门控网络本身。

**推论三：CFAR 滑窗检测可映射为 Prefix／Segmented Scan。** 若 CFAR 的窗口统计量是结合运算，例如 SUM、COUNT、MIN 或 MAX，则可通过前缀扫描实现。以窗口和为例：

[  
P_i=\sum_{t=0}^{i}x_t  
]

[  
W_i=P_{i+r}-P_{i-r-1}  
]

因此，CFAR 的主要数据传播可映射为线性链、树形扫描或分段扫描拓扑。若采用 order-statistic CFAR，则排序和选择逻辑仍需额外计算。

### 3.6 条件性扩展尺度

设一个阶段在 (N) 个节点上的执行时间为：

# [  
T_{\mathrm{step}}(N)

T_{\mathrm{compute}}(N)  
+  
T_{\mathrm{cfg}}  
+  
\chi\cdot c\log N  
+  
(1-\chi)\cdot g(N)  
]

对应效率为：

[  
\eta(N)=  
\frac{  
T_{\mathrm{compute}}(N)  
}{  
T_{\mathrm{compute}}(N)  
+  
T_{\mathrm{cfg}}  
+  
\chi\cdot c\log N  
+  
(1-\chi)\cdot g(N)  
}  
]

当 (\chi) 较高，且算子融合后满足：

[  
T_{\mathrm{compute}}(N)  
\gg  
T_{\mathrm{cfg}}  
+  
c\log N  
]

系统可表现出接近线性的扩展效率。反之，当 (\chi) 较低或残余通信 (g(N)) 增长较快时，TCC 无法消除通信瓶颈。

因此，TCC 并不违反 Amdahl 定律。其作用是降低拓扑兼容阶段的有效串行通信比例。

---

## 4. TCC-11 原语体系

### 4.1 原语设计原则

TCC-11 的目标是以尽可能小的原语集合覆盖典型拓扑中心工作负载中的关键数据流模式。该集合由 7 个路由原语和 4 个计算原语组成。路由原语负责塑造数据依赖图，计算原语负责端点或链路上的局部变换。

TCC-11 的设计遵循三条原则。

**正交性。** 每个原语对应一种不可被其它原语低代价替代的结构角色。

**可编译性。** 每个原语都能从数据流图或张量 IR 中识别，并映射为拓扑控制器可执行的状态。

**可退化性。** 当拓扑不兼容时，原语可退化为传统通信或局部计算，而不会破坏正确性。

### 4.2 TCC-11 规范表


| ID  | 原语        | 类型      | 语义角色                                | 典型复杂度            | 目标工作负载                   |
| --- | --------- | ------- | ----------------------------------- | ---------------- | ------------------------ |
| 1   | **LINK**  | Route   | 配置确定性拓扑，如 ring、mesh、torus、butterfly | (O(1)) 配置        | Dense DNN，FFT，DBF        |
| 2   | **PRUNE** | Route   | 根据稀疏掩码关闭非活跃链路                       | 本地 (O(1))，全局依赖掩码 | MoE，GNN                  |
| 3   | **PACK**  | Route   | 压缩活跃通道，缓解稀疏负载不均衡                    | (O(\log N)) 典型   | SpMV，GNN，MoE             |
| 4   | **SWAP**  | Route   | AlltoAll／分布式矩阵转置                    | 有界度拓扑上 (O(N)) 轮  | MoE，Transpose            |
| 5   | **MOVE**  | Route   | 稀疏点对点数据搬移                           | 每活跃边 (O(1))      | SpMV，GNN                 |
| 6   | **PULL**  | Route   | 从邻域或 frontier 收集数据                  | (O(K))，(K) 为邻域度  | GNN，Graph Aggregation    |
| 7   | **CAST**  | Route   | 广播／组播状态、参数或掩码                       | 树形 (O(\log N))   | Parameter Sync，Mask Sync |
| 8   | **GEMM**  | Compute | 稠密矩阵／张量乘法                           | 形状相关             | Transformer，CNN，DBF      |
| 9   | **FUSE**  | Compute | 结合规约，如 SUM、MAX、MIN                  | 树形 (O(\log N))   | AllReduce，Attention      |
| 10  | **FOLD**  | Compute | 局部张量收缩、池化、stencil                   | kernel 相关        | CNN，Pooling              |
| 11  | **SCAN**  | Compute | 前缀扫描／分段扫描                           | (O(\log N))      | CFAR，RNN，Streaming DP    |


### 4.3 目标工作负载表达完备性

**命题二。** 在存在基本控制流、有限状态和存储访问机制的前提下，TCC-11 可表达 Transformer、CNN、FFT、SpMV、MoE、GNN 和雷达 DBF 的主要通信与计算阶段。


| 工作负载        | TCC-11 映射                   |
| ----------- | --------------------------- |
| Transformer | LINK，GEMM，FUSE，CAST         |
| CNN         | FOLD，GEMM，PULL，LINK         |
| FFT         | LINK，GEMM／LocalTwiddle，FUSE |
| SpMV        | MOVE，PACK，FUSE              |
| MoE         | PRUNE，PACK，SWAP，GEMM，FUSE   |
| GNN         | PULL，MOVE，PACK，GEMM，FUSE    |
| Radar DBF   | LINK，GEMM，SCAN，FUSE         |


该命题是目标工作负载覆盖结果，而不是宣称所有分布式计算都自然拓扑兼容。对于不满足兼容性的阶段，TCC 编译器必须生成残余通信。

### 4.4 相对不可约性

**命题三。** 在有界度拓扑和 TCC-11 语义模型下，移除任一原语，都存在至少一个 witness workload，使其逻辑轮数、注入字节数或本地工作量出现渐近增加。


| 移除原语  | 见证工作负载                   | 代价退化                       |
| ----- | ------------------------ | -------------------------- |
| LINK  | FFT／DBF pipeline         | 额外路由调度或地址生成                |
| PRUNE | Sparse MoE／GNN           | 非活跃边仍消耗传输，能耗随 (1/\rho) 增大  |
| PACK  | 稀疏倾斜图                    | 热点拥塞与负载不均衡                 |
| SWAP  | Dense AlltoAll／Transpose | 有界度拓扑上 (\Omega(N)) 轮替代     |
| MOVE  | 稀疏随机访问                   | 退化为广播或 AlltoAll，注入字节增加     |
| PULL  | GNN 邻域聚合                 | 多次点对点搬移与控制开销               |
| CAST  | 掩码／参数广播                  | 退化为 (\Omega(N)) 单播         |
| GEMM  | 稠密张量计算                   | 算术强度显著下降                   |
| FUSE  | AllReduce／规约             | 中心化或串行规约瓶颈                 |
| FOLD  | 池化／局部收缩                  | 退化为填充型 GEMM 或标量循环          |
| SCAN  | Prefix／CFAR              | 重复前缀计算，产生 (\Omega(N)) 额外工作 |


该命题说明 TCC-11 对目标工作负载族是难以继续压缩的，但不排除其它体系结构在不同目标函数下采用不同原语集合。

---

## 5. 编译器与运行时

### 5.1 DFG 到拓扑状态编译流程

TCC 编译器输入为张量程序、计算图或 MLIR／XLA／TVM 风格中间表示，输出为 TCC-11 原语序列与拓扑上下文序列。编译流程包含七步。

**第一步，阶段划分。** 编译器将完整计算图划分为局部计算阶段和跨端点数据依赖阶段，形成：

# [  
\mathcal{C}

T_m\circ R_m\circ  
\cdots  
\circ T_1\circ R_1  
]

其中，(T_i) 表示局部计算，(R_i) 表示跨端点通信或数据依赖。

**第二步，数据流图标注。** 对每个 (R_i)，编译器构造带标签数据流图 (H_i)，标注边类型、张量形状、数据类型、顺序要求、带宽需求和数值约束。

**第三步，兼容性检测。** 编译器尝试在可用拓扑库中寻找 (S_i)，使 (H_i) 与 (S_i) 精确同构或低失真嵌入。拓扑库包括 ring、tree、mesh、torus、butterfly、hypercube、pipeline、sparse dispatch 等。

**第四步，原语选择。** 若存在匹配拓扑，编译器将阶段映射为 LINK、SWAP、SCAN、FUSE 等 TCC 原语。若存在稀疏掩码，则插入 PRUNE 和 PACK。若存在广播状态，则插入 CAST。

**第五步，残余通信生成。** 对无法拓扑原生实现的边，编译器生成 (R_i^{\mathrm{res}})，由 MOVE、PULL 或传统通信 fallback 执行。

**第六步，代价模型判断。** 编译器比较 (T_{\mathrm{TCC}}) 与 (T_{\mathrm{base}})。若 TCC 收益不足，则退化为传统执行路径。

**第七步，拓扑上下文发射。** 编译器输出逻辑拓扑配置表、端点算子配置、缓冲区映射和执行顺序。

### 5.2 运行时系统

运行时系统负责加载拓扑上下文、触发逻辑拓扑切换、同步端点状态、监控拥塞并处理动态稀疏模式。其核心模块包括：

**Topology Context Cache。** 缓存常用拓扑状态，例如 Transformer mesh、FFT butterfly、MoE sparse AlltoAll 和 DBF pipeline。

**Mask Distributor。** 通过 CAST 分发稀疏掩码或门控结果，支持 PRUNE 和 PACK。

**Residual Communication Engine。** 处理无法拓扑原生执行的剩余边。

**Numerical Mode Controller。** 在 deterministic、tolerance-bounded 和 fast mode 之间切换，控制规约顺序和浮点误差。

**Performance Feedback Loop。** 根据运行时拥塞、负载倾斜和残余比例动态调整拓扑选择。

### 5.3 编译器正确性条件

编译器输出的 TCC 程序必须满足三个正确性条件。

**语义正确。** 对精确兼容阶段，输出必须满足定理一；对近似阶段，误差必须在给定容差内。

**资源正确。** 拓扑映射必须满足链路带宽、缓冲区容量和端点并发约束。

**死锁避免。** 对存在环路的拓扑状态，运行时必须使用虚通道、信用流控、令牌调度或无环路径分配避免死锁。

---

## 6. 硬件体系结构

### 6.1 总体结构

TCC 硬件由三层组成。

**端点计算层。** 每个端点包含本地缓冲区、张量计算单元、规约单元、扫描单元和路由接口。端点支持 GEMM、FUSE、FOLD、SCAN 等计算原语。

**软件定义互连层。** 互连层通过逻辑路由表、交叉开关和链路状态寄存器形成不同拓扑状态。它支持 mesh、ring、tree、butterfly、pipeline 和 sparse dispatch 等逻辑拓扑。

**拓扑控制层。** Liquid Topology Controller 负责加载拓扑上下文、切换逻辑拓扑、分发稀疏掩码并协调端点执行。

### 6.2 逻辑重构与物理重构区分

本文严格区分逻辑拓扑重构与物理链路重构。物理光交换或机械级链路重排通常工作在微秒到毫秒尺度，适用于较粗粒度流量工程。Route≃Transform 依赖的是 SmartNIC／SDI 控制器内部的逻辑路由表与交叉开关状态切换，可在亚微秒尺度完成。

因此，本文报告的“拓扑切换延迟”指逻辑拓扑上下文切换时间，而不是完整物理链路重构时间。

### 6.3 数据通路

每个 TCC 端点维护三个数据通路。

**Local Compute Path。** 用于 GEMM、FOLD、LocalTwiddle 和局部非线性操作。

**Route Transform Path。** 用于 LINK、SWAP、MOVE、PULL、CAST 等路由原语。

**In-network Reduction／Scan Path。** 用于 FUSE 和 SCAN，在链路或端点之间完成结合规约和前缀传播。

这三个路径通过统一的 topology context 进行调度。一个 context 包含激活链路、路由规则、端点算子、数据格式、同步模式和错误检查字段。

### 6.4 稀疏拓扑支持

对 MoE、GNN 和 SpMV，TCC 使用 PRUNE 关闭非活跃边，使用 PACK 压缩活跃通道。稀疏掩码可由本地门控网络、图采样器或上游任务产生，并通过 CAST 进行分发。

对 top-(k) MoE，若 expert 数为 (E)，每个 token 仅激活 (k) 个 expert，则理想活跃密度为：

[  
\rho=\frac{k}{E}  
]

当 (k\ll E) 时，关闭非活跃链路可显著降低传输能耗。但若 token 分布极端倾斜，PACK 和负载均衡会成为主要开销。

### 6.5 能耗模型

本文将能耗分解为：

# [  
E_{\mathrm{total}}

E_{\mathrm{compute}}  
+  
E_{\mathrm{buffer}}  
+  
E_{\mathrm{network}}  
+  
E_{\mathrm{cfg}}  
+  
E_{\mathrm{res}}  
]

TCC 的能耗收益来自减少中间 buffer 写回、降低协议处理和减少非活跃边传输：

# [  
\Delta E

## E_{\mathrm{stage}}  
+  
E_{\mathrm{packet}}  
+  
E_{\mathrm{inactive}}

## E_{\mathrm{cfg}}

## E_{\mathrm{pack}}

E_{\mathrm{res}}  
]

当 (\Delta E>0) 时，TCC 在能耗上优于传统路径。对 Transformer block 中的部分 collective 和重排阶段，模型估计 TCC 可降低显式搬移相关能耗；该结果依赖数据驻留、拓扑兼容度和算子融合粒度。

---

## 7. 评测

### 7.1 方法学

本文采用硬件原型与周期精确模拟相结合的评测方法。

**硬件原型。** 原型由 4 个 FPGA 节点构成，节点间通过高速光链路互连。每个节点实现 TCC 端点、逻辑拓扑控制器和 TCC-11 原语子集。

**周期精确模拟器。** 模拟器从 (N=16) 扩展到 (N=1024)，建模端点计算、链路带宽、路由延迟、拓扑切换、buffer 行为和残余通信。

**评测边界。** 除非特别说明，本文报告 resident-data kernel 性能，即数据已位于端点本地缓冲或片上存储中。主机 I/O、一次性配置加载和模型冷启动不计入核心 kernel 时间。

**基线系统。** 基线采用高阶交换结构上的优化 collective，包括树形、环形、分层 AllReduce／AllGather／AlltoAll 和拓扑感知调度。本文不将 TCC 与朴素 GPU 通信实现比较，而是与强优化通信路径比较。

### 7.2 微基准一：FFT—Butterfly 同构验证

为验证推论一，本文实现 1024 点 radix-2 FFT。传统实现通常需要地址生成、shuffle、buffer 重排和 butterfly 算术。TCC 将其编译为 10 个 butterfly topology context，每个阶段执行：

[  
\mathrm{LINK}*{s}*  
*+*  
*\mathrm{LocalTwiddle}*{s}  
+  
\mathrm{FUSE}_{s}  
]

在 4 节点 FPGA 原型上，resident-data 1024 点流式 FFT 完成时间为 **800 ns**。该结果说明，当 FFT 通信骨架与可重构拓扑精确兼容时，地址生成和中间搬移可被拓扑状态吸收。

需要强调，该结果不表示 TCC 在所有规模、精度、batch 和内存放置条件下均优于成熟 FFT 库。它证明的是拓扑兼容 FFT 阶段的结构性收益。

### 7.3 微基准二：MoE 稀疏 Dispatch

本文将 MoE token dispatch 表示为稀疏矩阵 (D) 与 (D^{\top}) 的一对操作，并映射为：

[  
\mathrm{PRUNE}  
+  
\mathrm{PACK}  
+  
\mathrm{SWAP}  
+  
\mathrm{GEMM}  
+  
\mathrm{FUSE}  
]

在均衡 top-(k) 分配下，TCC 通过关闭非活跃 token–expert 边减少注入字节数。模拟结果显示，当 (\rho) 较低且 token 分布接近均衡时，稀疏拓扑收益显著；当 expert 负载高度倾斜时，PACK 代价和热点拥塞会削弱收益。

### 7.4 微基准三：CFAR Scan

本文将滑窗求和型 CFAR 映射为 SCAN 和局部差分。与逐窗口重复求和相比，SCAN 版本将窗口统计转化为前缀传播和端点局部计算。

在流式输入下，TCC 线性链／树形 scan topology 能持续输出检测统计量。对于 order-statistic CFAR，本文仅将可结合部分映射为 SCAN，排序和选择由局部比较网络或残余计算完成。

### 7.5 逻辑拓扑切换

本文测试从 LLM inference mesh topology 切换到 radar DBF pipeline topology 的逻辑拓扑上下文切换。原型测得逻辑切换时间不超过 **1 μs**。该结果证明同一硬件基底可在亚微秒控制窗口内切换任务拓扑，适合异构边缘智能场景。

再次强调，该时间对应逻辑路由状态切换，不等同于物理光链路重排。

### 7.6 宏基准：2B 级 Transformer 风格推理

本文在 4 节点 FPGA 原型上实现 2B 级 Transformer 风格模型的推理子图，包括 attention、MLP、层归一化和部分 collective。对 resident-data 推理路径，系统达到 **5.2 tokens/s/user** 的原型级吞吐。

该结果的意义不是与商用 GPU 完整推理服务直接比较，而是证明 TCC-11 可以在同一拓扑基底上表达并执行 LLM 推理、FFT 和 DBF 等跨域工作负载。

### 7.7 扩展性模拟与条件性 T-Scale

本文在 (N=16) 到 (N=1024) 节点模拟 TCC 扩展性。模拟显示，当工作负载满足高拓扑兼容度 (\chi)、算子融合充分且 (T_{\mathrm{compute}}\gg T_{\mathrm{cfg}}+c\log N) 时，TCC 在 (N=1024) 仍能维持 **99％ 以上功能单元利用率**。

当 (\chi) 降低时，残余通信 (g(N)) 成为主导项，利用率随节点数下降。这验证了本文理论判断：TCC 的扩展优势来自兼容阶段的通信结构转化，而不是无条件扩展。

### 7.8 消融实验

本文对 TCC-11 原语进行消融分析。结果与命题三一致。

移除 SWAP 后，MoE dispatch 退化为多轮点对点交换，AlltoAll 阶段轮数显著增加。

移除 PRUNE 后，稀疏 MoE 和 GNN 仍需传输非活跃边，能耗收益消失。

移除 PACK 后，稀疏图负载不均衡导致热点链路拥塞。

移除 SCAN 后，CFAR 和前缀类任务需要重复计算窗口统计，延迟和本地工作量增加。

---

## 8. 讨论与局限

### 8.1 拓扑兼容性不是天然存在的

TCC 的收益前提是数据流阶段与拓扑状态之间存在结构匹配。许多控制密集、动态分支密集或不规则随机访问负载并不具备高兼容度。对这类负载，TCC 只能作为普通通信网络使用，无法产生显著结构性收益。

### 8.2 数值确定性问题

规约树形状改变可能导致浮点加法顺序变化，从而产生非逐位一致结果。本文通过 numerical mode controller 支持确定性模式和容差有界模式。对要求 bitwise reproducibility 的任务，编译器必须保持参考规约顺序，可能牺牲部分性能。

### 8.3 物理实现复杂度

TCC 需要端点具备更强的路由状态机、上下文缓存和本地算子支持，这会带来面积、功耗和验证复杂度。是否值得采用 TCC，取决于目标负载中拓扑兼容阶段的比例和重用频率。

### 8.4 动态稀疏与负载倾斜

MoE 和 GNN 中的稀疏模式可能高度动态。若掩码分发、PACK 压缩和负载均衡开销过大，稀疏拓扑收益会被抵消。因此，TCC 运行时必须结合负载反馈进行动态策略选择。

### 8.5 与现有 GPU 集群的关系

TCC 并不是简单替代 GPU，而是提出一种互连与计算深度融合的体系结构方向。短期内，TCC 可作为 FPGA、SmartNIC、DPU、chiplet interposer 或 wafer-scale fabric 中的加速层；长期看，它可能成为面向具身智能、边缘多模态系统和大规模稀疏模型的新型空间计算基底。

---

## 9. 相关工作

### 9.1 In-network Computing

In-network aggregation、SHARP、SwitchML 等工作证明交换网络可以承担部分规约计算。这些系统主要面向 SUM、MAX、MIN 等有限规约。TCC 与其共同点是把计算下沉到通信路径中；不同点是，TCC 将路由拓扑本身视为可编译数据流结构，覆盖置换、扫描、稀疏压缩和动态拓扑映射。

### 9.2 Collective Communication

NCCL、MPI collectives 和拓扑感知调度在传统集群中广泛使用。它们优化 collective 的执行路径，而 TCC 进一步询问 collective 是否本身就是算法变换的一部分。若是，则 collective 可以被拓扑状态原生实现。

### 9.3 Spatial Dataflow 与 CGRA

CGRA、systolic array 和 spatial dataflow 架构通过重构芯片内部数据路径实现高效计算。TCC 借鉴其空间化思想，但将其扩展到分布式互连和多节点系统，并通过图同构／图嵌入定义可执行边界。

### 9.4 Wafer-scale 与 Chiplet Interconnect

Wafer-scale engine 和 chiplet interposer 通过高密度互连降低片外通信开销。TCC 可与这些技术结合，为其提供动态拓扑和原语级编程模型。静态高密度互连解决“距离”问题，TCC 进一步解决“形状”问题。

### 9.5 稀疏模型、MoE 与 GNN

MoE、GNN 和 SpMV 都具有稀疏数据流结构。已有系统重点优化专家并行、图采样和稀疏矩阵计算。TCC 的贡献是将稀疏边集直接映射为可剪枝、可压缩、可交换的拓扑状态，从而降低非活跃边传输和中间重排开销。

---

## 10. 结论

本文提出 Route≃Transform，建立了拓扑中心计算的条件性代数框架。其核心结论是：通信与计算不是普适等价关系；但当任务数据流图与可重构路由拓扑图之间存在标签保持图同构或低失真嵌入时，部分通信阶段可以被拓扑状态和局部算子共同实现，成为空间化计算过程。

基于该理论，本文定义 TCC-11 原语体系，覆盖 Transformer、CNN、FFT、SpMV、MoE、GNN 和雷达 DBF 等代表性工作负载。本文证明 TCC-11 在目标负载族上具有表达完备性，并在显式代价模型下具有相对不可约性。

硬件原型与模拟评测表明，在 resident-data、compute-bound 且拓扑兼容度高的阶段，TCC 能够减少显式数据搬移和协议开销，实现亚微秒级逻辑拓扑切换，并在大规模模拟中维持高利用率。

本文最终给出的不是“网络无条件等于计算”的命题，而是更可验证、也更具工程价值的判断：**当数据流与拓扑结构共振时，网络可以成为计算；当结构不共振时，系统必须承认残余通信并回到代价模型。**

---

## 参考文献

[1] Mark Horowitz. 2014. *1.1 Computing’s Energy Problem （and What We Can Do About It）*. IEEE International Solid-State Circuits Conference，ISSCC.

[2] Gene M. Amdahl. 1967. *Validity of the Single Processor Approach to Achieving Large Scale Computing Capabilities*. AFIPS Conference Proceedings.

[3] James W. Cooley and John W. Tukey. 1965. *An Algorithm for the Machine Calculation of Complex Fourier Series*. Mathematics of Computation.

[4] Guy E. Blelloch. 1990. *Prefix Sums and Their Applications*. Technical Report，Carnegie Mellon University.

[5] Leslie G. Valiant. 1990. *A Bridging Model for Parallel Computation*. Communications of the ACM.

[6] Tom Leighton. 1992. *Introduction to Parallel Algorithms and Architectures：Arrays，Trees，Hypercubes*. Morgan Kaufmann.

[7] Ashish Vaswani et al. 2017. *Attention Is All You Need*. Advances in Neural Information Processing Systems.

[8] Mohammad Shoeybi et al. 2019. *Megatron-LM：Training Multi-Billion Parameter Language Models Using Model Parallelism*. arXiv.

[9] William Fedus，Barret Zoph，and Noam Shazeer. 2022. *Switch Transformers：Scaling to Trillion Parameter Models with Simple and Efficient Sparsity*. Journal of Machine Learning Research.

[10] Dmitry Lepikhin et al. 2021. *GShard：Scaling Giant Models with Conditional Computation and Automatic Sharding*. International Conference on Learning Representations.

[11] Thomas N. Kipf and Max Welling. 2017. *Semi-Supervised Classification with Graph Convolutional Networks*. International Conference on Learning Representations.

[12] Will Hamilton，Zhitao Ying，and Jure Leskovec. 2017. *Inductive Representation Learning on Large Graphs*. Advances in Neural Information Processing Systems.

[13] Alexander Sapio et al. 2021. *Scaling Distributed Machine Learning with In-Network Aggregation*. USENIX NSDI.

[14] Nikolaos Chrysos et al. 2022. *Enabling Programmable In-Network Computing for Machine Learning Workloads*. IEEE Micro.

[15] Michael B. Taylor. 2018. *The Evolution of Bitcoin Hardware*. Computer，for discussion of specialization and energy scaling.

[16] Sean Lie. 2021. *Cerebras Architecture Deep Dive：First Look Inside the Hardware／Software Co-Design for Deep Learning*. IEEE Micro.

[17] Michael Bedford Taylor. 2020. *A Landscape of the New Dark Silicon Design Regime*. IEEE Micro.

[18] H. T. Kung. 1982. *Why Systolic Architectures？* Computer.

[19] Seth Copen Goldstein et al. 2000. *PipeRench：A Reconfigurable Architecture and Compiler*. Computer.

[20] NVIDIA. 2023. *NVIDIA SHARP In-Network Computing Technology*. Public technical documentation.

---

下一步建议直接做两件事：  
　　**一是把本文转成 ACM** `acmart` **英文 LaTeX 双盲版；**  
　　**二是生成 Fig.1“FFT–Butterfly 同构证明图”和 Fig.2“条件性 T-Scale 扩展效率图”。**

---
*getnote | 2026-07-31 08:14*


---

## Related Notes

[[NCL神经计算定律详解]]
[[SDI化合物键_四型架构]]
[[FPGA原型]]
[[iNEST-MOC]]
[[paper1_iNEST_core_architecture]]
[[超非线性增益]]
[[paper2_liquid_computing_chemistry]]
[[CST计量仪]]
