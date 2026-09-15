---
direction: both
category: 技术
tags: [TPUv7, Ironwood, 推理优化, 性价比, Blackwell, SparseCore, TorchTPU, MoE, GDN, 硬件架构]
summary: "谷歌TPUv7 Ironwood推理性价比反超英伟达Blackwell的深度技术解析"
quality: high
processed: 2026-09-15 08:14
---
---
title: "谷歌TPUv7 Ironwood深度解析：推理性价比反超英伟达Blackwell的真相"
tags:
  - hardware
  - infrastructure
  - design
  - network
  - semiconductor
  - transformer
  - architecture
  - ai
  - computing
  - chip
  - llm
date: 2026-09-09 21:00
source: GetNotes
score: 24
---

## Original Note

---
note_id: 1920851239689187112
title: "谷歌TPUv7 Ironwood深度解析：推理性价比反超英伟达Blackwell的真相"
type: link
created: 2026-09-09 13:35:22
source: getnote
kb: 
---

# 谷歌TPUv7 Ironwood深度解析：推理性价比反超英伟达Blackwell的真相

### 🏆 TPUv7 Ironwood vs Blackwell，谁的性价比更高？

**TPUv7 性价比最高领先 B200 约 50%**，在多数场景下优于英伟达 Blackwell 系列。
- **测试条件**：Qwen3.5 397B 模型 / FP8 精度 / 8K1K 基准 / 无 MTP（推测解码）
- **每百万 token 成本（100 tok/s/用户）**：
  - TPUv7：**0.181 美元**
  - B200：0.222 美元（TPU 低 **19%**）
  - B300：0.276 美元（TPU 低 **34%**）
- **低吞吐场景（20 tok/s/用户）**：
  - TPUv7 原始吞吐量 **9,364 tok/s/芯片**，比 B200/B300 高约 5%
  - 每美元性能比 B200 高 **50.4%**，比 B300 高 **96.0%**
- **内部 TCO 视角（1.03 美元/芯片·小时）**：
  - 并发 256 时，每美元性能比 B200 高 **76.7%**，比 B300 高 **130.2%**
  - 代价 = 延迟更高：平均 TTFT 5.41 秒 vs B200 3.75 秒 vs B300 2.40 秒
- **端到端延迟（20 秒中位响应）**：
  - TPUv7：0.098 美元/百万 token
  - 比 B200 低 8%，比 B300 低 25%
- **英伟达优势项**：
  - FP4 计算：TPUv7 不支持 FP4，英伟达 FP4 仍领先
  - 30 秒左右中位响应时间区间，B200 略有优势

### 🆚 TPUv7 聚合 vs GB300 NVL72 解耦，差距有多大？

**目前 GB300 解耦服务在中端延迟性价比高约 30%**，TPU 解耦优化后有望追平。
- **当前对比（TPU 聚合 vs GB300 解耦）**：
  - 低延迟 + 高延迟场景：两者竞争力相当
  - 中端延迟：GB300 性价比高约 **30%**
- **TPU 解耦现状**：谷歌内部已深度优化解耦服务，但**外部堆栈尚未完全优化**
- **未来预期**：谷歌 + Inferact + RadixArk + SemiAnalysis 持续优化，**数月内差距将缩小**，TPUv7 可与 GB200/300 NVL72 媲美
- **TPU 独有优势**：TPUv7 pod 可通过低延迟 ICI 扩展到 **1000+ 芯片**，支持 NVL72 无法实现的大模型解耦和超宽 EP 优化

### 🔧 TorchTPU 是什么，和之前的方案有何不同？

**TorchTPU 让 TPU 成为原生 PyTorch 设备**，移除了 PyTorch→JAX 的转换层。
- **三代演进路径**：

| 阶段 | 方案 | 核心机制 |
| :--- | :--- | :--- |
| 第一代 | PyTorch/XLA | 惰性执行，收集操作编译成图 |
| 第二代（当前） | TorchAX + JAX | PyTorch 模型转 JAX 执行 |
| 第三代（未来） | TorchTPU | 原生 PyTorch 设备，直接调度 |
- **TorchTPU 技术路径**：
  - 使用 PyTorch PrivateUse1 后端扩展点，暴露 `device="tpu"`
  - ATen 操作 → PyTorch 调度器 → TPU 后端
  - 编译路径：TorchDynamo + AOTAutograd 生成 FX 图 → StableHLO → XLA → TPU 可执行文件
  - 编译器仍用 XLA，**不用 Inductor 和 Triton**
- **核心优势**：
  - 复用上游 vLLM/SGLang 模型代码、调度器、批处理、API 逻辑
  - 降低模型和引擎特性启动成本
  - 支持 DDP、FSDP2、DTensor 等标准分布式接口
- **时间节点**：截至 9 月初仍在内测，**预计 10 月中旬 PyTorch 大会期间开源**
- **社区合作**：Inferact、RadixArk、Red Hat 与谷歌深度合作推进 vLLM/SGLang 适配

### ⚡ TPU 推理做了哪些关键优化？

**从内核到系统的多层优化**，显著提升了 Qwen3.5 等模型的推理性能。
- **并行策略优化**：
  - **DEP8（DP注意力+EP8）**：八路注意力数据并行 + 八路专家并行，提升并发服务能力
  - 合并专家 ID + 路由权重为单次 all-gather，DeepSeek-V3 每层省 **80 微秒**，58 层共省约 4.64 毫秒
- **SparseCore 卸载**：
  - ReduceScatter 集体计算移到 SparseCore（适合不规则数据移动），释放 TensorCore
  - 双缓冲重叠本地归约 + 芯片间传输
  - 8k1k 并发 64~512 时，吞吐量提升 **4.1%~14.2%**；1k8k 并发 512 时提升 **26.1%**
  - 小集合保留在 TensorCore，设阈值动态判断（并发 64 提升 2.7%，并发 128 提升 5.7%）
- **MoE 路由与专家内核**：
  - 第二版 GroupedGEMM：移除冗余瓦片计算、专家权重三重缓冲、元数据生成融合
  - 专家 token 重组移到 SparseCore，8k1k 服务吞吐量提升 **12%**
  - 小批量专用置换算法：并发 64 提升 7.3%，并发 128 提升 5.1%
  - 排序键打包：排序延迟从 106.6 微秒降至 **21.7 微秒**
- **GDN（门控 DeltaNet）内核优化**：
  - 代数重排使 MXU 与 VPU 工作重叠，并发 64 提升 2.79%，并发 512 提升 4.48%
  - 减少向量寄存器溢出，64 位解码内核提速约 **20%**
  - 异步状态传输 + 双缓冲，并发 512 提升 **11.3%**
  - GDN v3 融合 Conv1D + GDN：内核级加速 解码 1.41x / 预填充 1.60x / 混合批次 2.14x
- **内存与分页注意力**：
  - 循环状态紧凑分配：回收约 **76 GiB HBM**，注意力块池扩大 71%，1k8k 并发 64 提升 18%
  - BF16 存储循环状态：HBM 占用减半，1k8k 并发 512 提升 15%
  - 序列通道布局：KV 页面数量翻倍（5141→10283），8k1k 并发 128 吞吐量提升 **16.5%**，TTFT 降低 95%
  - KV 获取/计算块大小分离：解码吞吐量从 64.9k → 96.3k tok/s，提升 **49%**
- **低并发优化**：
  - 请求元数据按活跃请求数分桶：GDN 调度开销从 283→97 微秒
  - 并发 4 场景：8k1k 提升 13.3%，1k1k 提升 15.5%
  - 深度低并发调优：并发 4 时 1k1k 综合提升 **22.9%**，并发 8 提升 18.1%
- **混合模型前缀缓存**：
  - 为 GDN 单独设置检查点槽 + 实时状态槽，避免前缀状态被覆盖
  - 支持 DP 的混合前缀缓存，适配多轮对话和代理工作负载

### 🏗️ TPU 硬件和网络架构有什么特点？

**芯片 + 互连 + 编译器协同设计**，是 TPU 性价比优势的核心来源。
- **Ironwood 芯片架构**：
  - 打破 v4/v5p MegaCore 设计 → 两颗独立计算芯片，各为独立逻辑设备
  - 每芯片 = **2 个 TensorCore + 4 个第三代 SparseCore**
  - HBM 容量约为 Trillium 的 **6 倍**
  - 首款**原生支持 FP8** 的 TPU（前代靠软件模拟）
- **MXU（矩阵乘法单元）**：
  - v6e 起从 128x128 升级到 **256x256 脉动阵列**，每周期 65,536 MAC，算力是前代 4 倍
  - 代价 = 对形状敏感：维度不匹配会产生填充，直接降低利用率
  - 例：Llama 3 8B 头维 128 → Ironwood 上 MXU 利用率上限仅 **50%**；头维 64 → 仅 25%
  说白了，TPU 的大矩阵单元算力很强，但模型形状不对的话，很多算力会被浪费在"填零"上。
- **3D 环面 ICI 网络**：
  - TPU v4 起用 3D 环面拓扑，每芯片连 6 个邻居（±X/±Y/±Z）
  - 基本模块 = **4x4x4 立方体（64 芯片）**，正好装一个机架
  - 环面环绕连接 + 扭曲环面设计，最坏跳数减半
  - 光路交换机（OCS）扩展到 **9216 芯片超级节点**，聚合 42.5 FP8 exaflops
  - OCS 优势：数秒内用镜像重连故障链路，无需人工熔接
  - 小型 EP 消息延迟甚至低于单跳 NVSwitch
- **TPUv8i Boardfly 新拓扑（下一代推理芯片）**：
  - 谷歌首次训练/推理芯片分线：TPU 8t（训练，3D环面）+ TPU 8i（推理，Boardfly）
  - Boardfly = 扁平分层高基数交换机结构（类似蜻蜓网络）
  - 1024~1152 芯片规模下，网络跳数从 ~16 → ~7，**直径减少 50%+**
  - ICI 带宽 **19.2 Tb/s**（上代 2 倍），片上 SRAM **384 MB**（上代 3 倍）
  - 原生 FP4 支持，可与 Rubin NVL72 媲美

### 🛣️ TPU 外部化下一步要做什么？

**软件栈仍需多层优化**，目标是全面对标并超越英伟达生态。
- **推测性解码（MTP）**：
  - 利用解码阶段带宽受限、计算单元空闲的特点，一次验证多个预测 token
  - 无损提升吞吐，是降本关键技术
- **预填充-解码解耦（PD分离）**：
  - 谷歌内部 Gemini 已在用，外部化刚启动数月
  - 开源 TPU-Sync（原 TPU-raiden）：零拷贝 KV 缓存传输
  - 支持 DRAM 卸载 + Mooncake Store 行业标准库 + P2P 池化 + NVMe 池化
  - 解耦落地后，TPUv7 性价比有望超越 GB200/GB300
- **模型支持扩展**：
  - 首发：Qwen3.5 397B
  - 规划：Kimi K3、GLM5.3、Gemma4 等开源模型
- **AgentX 代理工作负载**：
  - 适配多轮交互、长上下文、高前缀重用、子代理突发等特性
  - KV 缓存卸载是核心支撑技术
- **整体节奏**：TorchTPU 稳定 → vLLM/SGLang 原生支持 → 模型生态扩展 → 代理场景落地

### 📝 补充细节
- **Anthropic 采购**：承诺采购超 **100 万个 TPU**（约 40 万直接购买 + 60 万 GCP 租赁），主要用于训练也用于推理；预计 2029 年 TPU 使用量超过 DeepMind
- **TCO 口径差异**：外部 TPU TCO 为 1.21 美元/芯片·小时，内部 TCO 为 1.03 美元/芯片·小时；B200 为 1.73 美元/GPU·小时，B300 为 2.26 美元/GPU·小时
- **测试方**：Semianalysis 发布，基于 InferenceX 官方预览版的首个第三方推理测试
- **软件生态合作方**：谷歌 + PyTorch 社区 + vLLM 社区 + SGLang 社区 + Inferact + RadixArk + Red Hat

---
*getnote | 2026-09-09 21:00*


---

## Related Notes

[[paper1_iNEST_core_architecture]]
[[FPGA原型]]
[[paper2_liquid_computing_chemistry]]
[[SDI化合物键_四型架构]]
[[iNEST-MOC]]
