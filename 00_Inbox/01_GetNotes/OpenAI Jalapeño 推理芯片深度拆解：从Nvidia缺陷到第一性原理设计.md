---
title: "OpenAI Jalapeño 推理芯片深度拆解：从Nvidia缺陷到第一性原理设计"
tags:
  - hardware
  - green-ai
  - infrastructure
  - design
  - network
  - semiconductor
  - transformer
  - architecture
  - energy
  - ai
  - computing
  - chip
  - llm
date: 2026-09-09 21:00
source: GetNotes
score: 21
---

## Original Note

---
note_id: 1920867543384469016
title: "OpenAI Jalapeño 推理芯片深度拆解：从Nvidia缺陷到第一性原理设计"
type: link
created: 2026-09-09 17:48:26
source: getnote
kb: 
---

# OpenAI Jalapeño 推理芯片深度拆解：从Nvidia缺陷到第一性原理设计

### 🏗️ 为什么要自研推理芯片，Nvidia哪里不够用？

Nvidia GPU 的**通用性设计**在 LLM 推理场景下代价高昂，实际性能仅达理论值的 10%。
- **性能差距**：1T 参数模型理论上可做到 **1000~2000 tokens/s/user**，但 B300 平台实际仅 100~200 tokens/s/user。
- **核心矛盾**：GPU 靠大量并发 warp 隐藏访存延迟 → 依赖大 batch → 推理小 batch 时机制失效，利用率暴跌。
- **架构缺陷三重奏**：
  - **统一内存子系统**：L2 分区跨区访问增加 **200~400 cycles** 延迟，HBM 带宽利用率仅 60%~70%。
  - **独立核异步推进**：全局 fence 需逐核确认，同步开销随规模放大。
  - **集中式网络仲裁**：多核心共享 DMA/网卡，仲裁逻辑成为吞吐与延迟瓶颈。
- **网络侧痛点**：RoCE 缺陷多、DPU 性能与安全问题突出；某 MaaS 业务用 CIPU eRDMA 替换后，**TTFT 直接降低 40%**。

### 🧠 推理芯片设计的第一性原理是什么？

核心目标是**在满足延迟 SLA 的前提下，最大化每瓦请求数**，而非峰值算力。
- **两大核心指标**：
  - 用户体验：**TTLT（time to last token）** + TBT（token 间隔）
  - 推理效率：**Energy / token**（也用 tokens/s/kW 衡量）
- **Pareto 前沿**：降低延迟通常提升单 token 能耗，提高 batch 则反之，需在两者间找最优平衡。
- **两大推论**：
  - **推论 A**：有用 token 靠低延迟下的高利用率，不能靠堆 batch
    → 缩短内存路径 + 提高单流 ILP + 适配小 batch 矩阵单元 + 消除启动同步开销
  - **推论 B**：芯片面积不是稀缺资源，闲置整机才是浪费
    → 拒绝异构分离 + 平衡算力/内存/通信配比 + 允许暗硅 + 全芯片功耗优化

### ⚙️ 推理业务的四个阶段对硬件需求差在哪？

四个阶段瓶颈完全不同，**专用异构集群会导致大量资源闲置**。
- **四阶段压力矩阵**：

| 阶段 | 计算压力 | 内存压力 | 通信瓶颈 |
| :--- | :--- | :--- | :--- |
| Prefill | 5/5（矩阵算力） | 2/5 | 带宽受限、易调度 |
| Decode | 2/5 | 5/5（权重带宽） | 5/5（同步延迟） |
| Draft（自回归） | 2/5 | 4/5 | 5/5（同步延迟） |
| Verify（树状） | 5/5 | 5/5 | 5/5（突发流量） |
- **异构集群的致命问题**：
  - 接受率、上下文长度、模型结构变化 → 各阶段负载动态波动
  - 一个池成瓶颈，其余池闲置但仍要付封装、HBM、网络、散热基线成本
  - 固定设备比例 = 锁死五个资源维度的比例，无法灵活调整
- **KVCache 代价**：PD 分离架构下 KV 跨设备搬运，带来额外功耗与同步开销；Jalapeño 选择将 KV 尽量留在本地。

### 🔬 Jalapeño 芯片架构核心做了哪些反常识选择？

放弃 UMA 和 SIMT，走 **NUMA + 乱序核 + 专用集合通信网络** 路线。
- **整体架构**：64 个 Core Slice 与 64 个 HBM Slice 一一配对，构建最低延迟本地访问路径。
- **三大反直觉设计**：
  1. **硬件管理 L1，而非软件 scratchpad** → 消除 barrier/DMA 固定开销
  2. **乱序核而非顺序核** → 小 shape 下也能吸收内存抖动
  3. **支持小矩阵维度** → 避免大型脉动阵列的分块断崖
- **Core Slice 内部（推测）**：
  - 16 个 64×64 Tensor Unit（激活 15 个，良率冗余）
  - SIMD 单元 + 标量单元 + 乱序调度核 + 依赖单元
  - **512KB L1 Cache**（硬件管理，三引擎共享）
  - 本地 HBM4 Slice：**240 GB/s 带宽 + 3.375 GiB 容量**

### 📡 片上网络和系统架构怎么设计？

双 NOC 架构 + 标准以太网 ScaleUP，**用成熟供应链换快速上市**。
- **片上网络**：
  - **Collective Network**：专用高带宽低延迟网络，负责 all-reduce / all-gather，直接连 L1
  - **General NoC**：低带宽高延迟，负责全局内存访问与 ScaleUP 桥接
- **系统规格**：
  - 单芯片：**13.4 PFLOPS（MXFP4）**、15.4 TB/s HBM4、216 GiB 容量、700W 功耗
  - 2048 芯片系统：27 EFLOPS 算力、32 PB/s 带宽、432 TiB 容量
  - ScaleUP：Local 域 128 卡 @ 600 GB/s，Global 域 2048 卡 @ 200 GB/s
- **机柜架构**：
  - CPU Tray（Katsu）：2× Turin X86、1.5TB 内存
  - Compute Tray（Vindaloo）：8 颗 Jalapeño ASIC
  - 交换机：采用 **BRCM Tomahawk 6** 标准以太网芯片，无需自研

### 💻 软件栈为什么敢放弃通用编译器？

用 **AI 搜索替代 cost model 预测**，把空间编程复杂度甩给大模型。
- **核心理念**：Spatial programming 对人类困难，但对前沿 AI 很简单。
- **六层软件栈**：

| 层级 | 组件 | 对应 CUDA 生态 |
| :--- | :--- | :--- |
| L5 服务 | Teacup | vLLM / SGLang |
| L4 执行体 | gigakernel | persistent kernel + CUDA Graph |
| L3 内核语言 | Gluon | CuTe / CUTLASS |
| L2 布局代数 | Linear Layouts + TensorInfo | CuTe Layout |
| L1 底层 | ~3000 行类汇编 + sanitizer | PTX/SASS + compute-sanitizer |
| L0 度量 | chilisim（周期精确） | Nsight Compute |
- **AI 优化效果**：DeepSeek MLA 案例中，五步优化从 0.31% 提升到 **88.9%** 峰值性能。

### 🛠️ 9个月流片是怎么做到的？

**先换硬件语言，再让 AI 介入**，把设计变成可搜索问题。
- **核心工具**：XLS（中级综合工具链）作为 AI 与设计者协作的基座。
- **XLS 的四大优势**：
  - 语义无歧义 → AI 生成代码行为可判定
  - 可控到流水级和位宽 → 不牺牲 PPA 上限
  - 快速反馈面积/时序 → 闭环周期短
  - 形式化验证 → AI 改错可自动拦截
- **人机分工**：
  - 人类：定义目标函数、选择主体架构、判断复杂度取舍、规划软硬件协同
  - AI：明确判据下的大规模穷尽搜索，替代手工调整面积/时序

### 🆚 Jalapeño vs Nvidia GPU 本质区别在哪？

两种延迟应对思路：**GPU 靠并发隐藏，Jalapeño 靠缩短距离消除**。
- **延迟机制对比**：

| 维度 | GPU | Jalapeño |
| :--- | :--- | :--- |
| 核心机制 | 时间复用 + 大量 warp 覆盖延迟 | 缩短路径 + 预取 + 乱序窗口 |
| 依赖条件 | 足够大的 batch | 单指令流 ILP |
| batch=1 时 | 流水线空转，机制失效 | 机制不变，不依赖并发 |
| 单并发 tok/s/user | 169 – 535 | 700 – 1,459 |
- **存储层次对比**：
  - GPU：寄存器 → L1/SMEM → DSMEM → 统一 L2 → HBM（层次厚重）
  - Jalapeño：L1 → 本地 HBM Slice（极简层次）
- **路线图**：A0 回片后 B0 预计还有 **25% 性能提升**，第二代将支持训练。

### 📝 补充细节
- **MXFP 支持**：原生支持 MXFP8 × MXFP4 混合精度，正好匹配 MoE 中激活 FP8 × 权重 FP4 的常见路径。
- **良率设计**：reticle-size 大芯片采用核级 + 通道级良率收割，坏核/坏通道熔断不影响其余部分。
- **暗硅更便宜**：单芯片内闲置模块可电源门控，比异构集群中整台闲置加速器的基线成本低得多。
- 说白了，Jalapeño 不是要做一块比 GPU 更快的通用芯片，而是把 LLM 推理里用不上的通用能力全砍掉，把省下来的面积和功耗全砸在"低延迟下的实际利用率"上。

---
*getnote | 2026-09-09 21:00*


---

## Related Notes

[[paper1_iNEST_core_architecture]]
[[FPGA原型]]
[[paper2_liquid_computing_chemistry]]
[[SDI化合物键_四型架构]]
[[iNEST-MOC]]
