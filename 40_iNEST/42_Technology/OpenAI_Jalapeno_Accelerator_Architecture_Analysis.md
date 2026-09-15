---
direction: both
category: 技术
tags: [AI加速器, 芯片架构, LLM推理, 网络拓扑, 能效优化]
summary: "OpenAI Jalapeño从延迟SLA反推的推理专用芯片架构设计拆解"
quality: high
processed: 2026-09-15 08:13
---
---
title: "OpenAI Jalapeño AI 加速器深度拆解：从用户体验反推的芯片架构设计"
tags:
  - transformer
  - design
  - infrastructure
  - green-ai
  - network
  - energy
  - semiconductor
  - ai
  - llm
  - architecture
  - hardware
  - chip
  - computing
date: 2026-09-15 08:12
source: GetNotes
score: 21
---

## Original Note

---
note_id: 1921321994948345976
title: "OpenAI Jalapeño AI 加速器深度拆解：从用户体验反推的芯片架构设计"
type: link
created: 2026-09-14 15:22:27
source: getnote
kb: 
---

# OpenAI Jalapeño AI 加速器深度拆解：从用户体验反推的芯片架构设计

### 🏗️ Jalapeño 的设计出发点是什么？

**不以峰值FLOPs为目标，**从用户体验反推**，先满足延迟SLA再优化能效。
- **核心公式**：最大化「每秒每瓦请求数 → 约束条件 = 端到端延迟 ≤ SLA 目标
- **延迟指标**：TTFT（首token时间）、TPOT（每输出token时间）、末token时间
- **优先级**：TPOT 与端到端延迟 > 峰值算力

### ⚖️ 设计要权衡哪些核心矛盾？

AI加速器设计本质是穿越**多层Pareto前沿**，没有最优解只有取舍。
- **宏观三层权衡**
  - 智能 vs 服务成本 vs 延迟
  - 吞吐 vs 交互性
  - 计算密度 vs 每比特能耗 vs 光罩限制
- **系统级权衡**
  - 内存带宽 vs 容量 vs 每比特能耗（内存墙）
  - 交换radix vs 覆盖距离
  - 可编程性 vs 硅效率
  - 模型精度 vs 计算/内存密度

### 📊 现实中LLM推理的真实瓶颈在哪？

**HBM带宽不是瓶颈，**并行开销**才是实际token速率的主要限制。
- **理论上限**：128颗芯片聚合1+ PB/s HBM4带宽 → 每秒2000+次全模型权重读取
  - 无投机解码：1000–2000 tokens/s/user
  - 有投机解码：5000–10000 tokens/s/user
- **实际水平**：单用户仅 **20–200 tokens/s**
- **差距来源**：芯片间网络延迟、同步延迟、NoC路由争用 → HBM空转、利用率不足

### 🔄 LLM推理分哪几个阶段，各有什么特点？

prefill、speculate、decode三阶段**负载特征差异极大**，比例还会动态变化。

| 阶段 | 核心操作 | 资源瓶颈 | 关键指标 |
| :--- | :--- | :--- | :--- |
| Prefill | 并行处理提示、填充KV cache | 计算密集 | TTFT |
| Speculate | 轻量模型预测K个token | 通信密集 | 接受率 |
| Decode | 自回归逐token生成 | 内存密集 | TPOT |
- **专用芯片 vs 平衡芯片**
  - 专用异构集群：不同芯片各司其职 → 空闲芯片仍耗基础功耗（封装、HBM、I/O、散热）
  - 单颗平衡芯片：不同阶段激活不同模块 → 未用模块「暗硅」可关断
  - **核心结论**：暗硅比闲置加速器更便宜

### 🌐 为什么选了什么网络架构？

采用**半扁平化两跳Clos拓扑**，用Broadcom TH6交换机保证延迟可预测。
- **两级域划分**
  - 本地域（scale-up）：1颗TH6 → 128颗Jalapeño，每颗800Gbps，支撑张量并行
  - 全局域（scale-out）：8颗TH6 → 2048颗Jalapeño，支撑MoE并行
- **关键特性**：任意两颗芯片间最多两跳，延迟可预测
- **放弃的方案**
  - 两层Fat-Tree（3跳，尾延迟抖动大）
  - 3D/4D Torus/Mesh（平均跳数多，延迟不可预测）
  - Dragonfly（非均匀路径，需自适应路由）

### 🚀 投机解码用了什么方案？

选择**多token预测（MTP）**，用小模型草稿+大模型一次验证。
- **对比STP（单token预测）**：8次大模型前向 → 8个token
- **MTP（多token预测）**：7次小模型草稿 + 1次大模型验证 → 最多8个token
- **收益**：大模型前向次数最多减少8倍 → 更低延迟 + 更高吞吐
- **现状**：芯片为MTP从头设计，但目前先跑STP验证硅片

### 💻 芯片架构有什么特别之处？

采用**空间架构**，搭配自研Gluon编程语言兼顾效率与可编程性。
- **空间架构 vs GPU SIMT**
  - GPU：时间化SIMT，中央warp调度器统一调度数千线程
  - Jalapeño：独立core slice平铺，各核配专用HBM接口，核间直接流式传输
- **Gluon语言**：基于Triton构建，提供熟悉的SIMT抽象（thread block），无需手工构造空间数据流图
- **片上网络**：专用集合通信网络（高带宽低延迟）+ 通用NoC（灵活）

### 📐 具体规格参数是多少？

台积电3nm工艺，6颗HBM4，**700W功耗**，专为推理优化。
- **单芯片**
  - 算力：fp8 3.4 PFLOPS/s、fp4×fp8 6.7 PFLOPS/s、fp4 13.4 PFLOPS/s
  - 内存：15.4 TB/s带宽、216 GiB容量
  - 网络：本地128颗@600 GB/s、全局2048颗@200 GB/s
- **2048颗集群**
  - 总算力：27 EFlops/s（fp4）
  - 总内存：32 PB/s带宽、432 TiB容量
  - 规模：约28–32个机架
- **对比**：NVIDIA B200 9 PFLOPS/s（1000W+）、B300 15 PFLOPS/s（1000W+），但Jalapeño仅做推理

### 💡 关键洞察
- **设计顺序很重要**：先定延迟SLA，再优化能效，这个顺序决定了所有架构选择的自洽性
- **延迟来源**：不是硬件光速，而是统一内存争用、核心同步、集中式网络仲裁等架构性开销
- **通用性的价值**：机会成本 > 边际成本，宁可多付一点暗硅成本，也要保留应对未来负载的可编程性

---
*getnote | 2026-09-15 08:12*


---

## Related Notes

[[paper1_iNEST_core_architecture]]
[[iNEST-MOC]]
[[FPGA原型]]
[[SDI化合物键_四型架构]]
[[paper2_liquid_computing_chemistry]]
