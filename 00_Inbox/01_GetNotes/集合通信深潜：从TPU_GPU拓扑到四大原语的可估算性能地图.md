---
title: "集合通信深潜：从TPU_GPU拓扑到四大原语的可估算性能地图"
tags:
  - architecture
  - semiconductor
  - physics
  - hardware
  - chip
  - research
  - network
  - paper
  - first-principles
date: 2026-09-22 22:24
source: GetNotes
score: 20
---

## Original Note

---
note_id: 1922055932918036608
title: "集合通信深潜：从TPU/GPU拓扑到四大原语的可估算性能地图"
type: link
created: 2026-09-22 13:14:40
source: getnote
kb: 
---

# 集合通信深潜：从TPU/GPU拓扑到四大原语的可估算性能地图

### 🏗️ 这篇文章在讲什么，为什么重要？

集合算法**只有懂底层物理拓扑**才真的成立，是推理Transformer性能的基础。
- **核心框架**：TPU拓扑 → 四大集合原语实现 → NVIDIA GPU集群拓扑与分层算法
- **覆盖范围**：7大部分、35张图，绑定拓扑、带宽层级与原语一起讲
- **实用价值**：给出一条**用数字估算**训练/推理性能的路径

### 🧩 TPU集群拓扑长什么样？

TPU是**均匀近邻直连**的torus结构，带宽从片上到DCN逐层递减。
- **连接模式**：
  - **2D torus（4邻）**：v2 / v3 / v5e / v6e
  - **3D torus（6邻）**：v4p / v5p / TPU7x / 8t
- **规模单位**：
  - **Pod（Superpod）**：最大ICI连通岛；v4 pod = 16³ = **4096颗**，v5p = 16×20×28 = **8960颗**
  - **Slice**：单pod内经ICI连通的一块，通信重的应用尽量选能保住torus的形状（如4×4×8）
- **带宽层级（v5e）**：
  | 层级 | 带宽 | 说明 |
  | :--- | :--- | :--- |
  | VMEM（SRAM） | ~17.6 TB/s | 128 MiB容量，约22× HBM带宽 |
  | HBM | 820 GB/s | 16 GB容量 |
  | ICI | 45 GB/s | 芯片间互连，单向 |
  | PCIe | 16 GB/s | 连host CPU |
  | DCN | 3.125 GB/s | 数据中心骨干，跨pod |
- **关键分界点**：单向ICI 45GB/s × 1μs = **45KB** → 消息小于这个量级，延迟主导，纯带宽估算失效
- **性能惩罚**：失去wrap退化成mesh时，该轴向ring型集合大约**慢2×**

### 🔄 All-Gather有哪些实现方式？

All-Gather是**把所有分片复制给每颗芯片**，大消息主推ring结构。
- **1D双向ring**：
  - 步数 = N/2，总时间 = D / BW_bi_ici
  - 吞吐主导下，总时间**与分片数无关**
- **1D单向ring**：
  - 步数 = N-1，渐近时间 = D / BW_uni_ici
  - 比双向ring**渐近慢2×**
- **1D path/chain**：无wrap的slice退化形态，性能同单向ring
- **2D双向ring**：同时动用全部4条ICI邻居链路 → 比1D约**2×提速**
- **通用规律**：N轴连通 → 总时间 ≈ D / (N_axes × BW_bi_ici)

### ➕ Reduce-Scatter和All-Reduce怎么来的？

Reduce-Scatter是All-Gather的**对偶操作**，二者叠加就是All-Reduce。
- **Reduce-Scatter**：
  - 通信schedule与All-Gather相近，shard边传边reduce（sum/max/mean等）
  - 吞吐主导下时间量级与All-Gather**完全相同**
  - 大消息下reduce计算可与通信重叠，无需单独建模
- **All-Reduce = Reduce-Scatter + All-Gather**：
  - 总成本 = 单一原语的 **2×**
  - 前向用All-Gather的场景，后向通常对应Reduce-Scatter，反之亦然
- **多轴扩展**：横跨多轴可并行多条ICI，总时延随所用拓扑轴数近似反比减少

### 🔀 All-to-All是做什么的？

All-to-All本质是**分片式转置**，主要用于MoE专家并行场景。
- **使用场景**：MoE中token按expert ID路由，每chip把token送到对应expert所在芯片
- **操作特点**：开始按源芯片分组，结束按目的expert分组
- **实现方式**：同样支持双向ring、单向ring、chain/path三种拓扑形态
- **GPU节点内优势**：NVSwitch全连下，均衡All-to-All比双向1D torus ring**少约一半时间**

### 🌳 NVIDIA GPU集群拓扑有什么不同？

GPU是**分层交换网**，而非TPU式近邻直连，以fat tree组织。
- **层级结构**：
  - **Node**：DGX H100 = 8颗GPU经NVSwitch全连；GB200 NVL72 = 72颗
  - **SU（Scalable Unit）**：32个node经IB leaf switch组成
  - **多SU**：由spine switch相连，构成fat tree
- **关键带宽数值**：
  - NVSwitch：**450 GB/s/GPU**（全双工）
  - DGX H100 node IB注入：**400 GB/s**（单向）
  - 8颗node内向bisection：1.8 TB/s ↔ 双向3.6 TB/s
  - SU（32颗）：6.4 TB/s（双向12.8 TB/s）
  - 64/64切分：25.6 TB/s（双向51.2 TB/s）
- **满fat tree = 无oversubscribe**：每层上行带宽 = 下行注入带宽，才有full bisection bandwidth

### ⚡ GPU节点内集合通信怎么做？

节点内是NVSwitch全连，ring是**逻辑构造**而非物理路径，还有SHARP硬件加速。
- **Ring vs Tree**：
  - **Ring**：适合大消息，流水效率高，有效带宽好
  - **Tree（recursive doubling）**：步数 = log₂N，延迟低，大消息带宽不及ring
  - NCCL会按消息大小与拓扑在ring/tree/hybrid间自动选择
- **SHARP（网内归约）**：
  - 原理：switch芯片自带归约计算单元，直接在网络里做reduce
  - 理论加速：接近2×，8-GPU node理想约**1.75×**
  - 实测加速：仅约**1.3×**（归约与multicast pipeline无法完美重叠）
  - H100 NVSwitch SHARP FP32归约吞吐：400 GFLOP/s
- **NVLink multicast**：也加速All-Gather，但源GPU也会收到重复数据，白耗1/8带宽

### 🌐 GPU跨节点集合通信怎么做？

跨节点用**分层算法**，大消息下一阶近似由node级IB带宽决定。
- **核心心智**：满fat tree下，可想象整集群挂一个跨node的ring
- **时间估算**：
  - 一阶近似：T_tot ≈ D / BW_node = D / 400e9
  - 更精确：分层集合的scale-out（IB）与node内（NVSwitch）可流水 → 总时 ≈ max(D/BW_gpu, D/BW_node)
- **四种原语的分层实现**：
  - All-Gather / All-Reduce：节点内归约压缩后再跨节点，再扩散
  - Sharded All-Reduce：只对对应shard的replica归约，不跨tensor-parallel rank
  - All-to-All：无法本地归约压缩，每chunk都要送到特定目的
- **rail优化**：要吃到node级满带宽，需rail-aware rank摆放与跨路径均衡

### 📝 补充细节
- **理想带宽模型的前提**：消息足够大（GPU常到GB级才接近峰值）、满fat tree、无拥塞
- **校准方法**：具体集群务必跑microbenchmark，不要直接照搬论文理论数字
- **GB200 NVL72特殊点**：MoE推理中72颗只挑8个expert时，通信变稀疏，不再是均匀All-to-All
- **对偶关系**：多数分片模式下，前向All-Gather ↔ 后向Reduce-Scatter，反之亦然

---
*getnote | 2026-09-22 22:23*


---

## Related Notes

[[Papers-MOC]]
[[SDI化合物键_四型架构]]
[[paper1_iNEST_core_architecture]]
[[iNEST-MOC]]
[[FPGA原型]]
