---
direction: both
category: 技术
tags: [FFN稀疏性, 推理加速, 异构计算, LLM]
summary: "FFN神经元高度稀疏，可通过预测跳过与冷热混合推理实现2-11倍加速。"
quality: high
processed: 2026-08-23 19:06
---
---
title: "FFN 稀疏性深度拆解：90% 神经元白吃算力，怎么靠跳过它们提速 11 倍？"
tags:
  - paper
  - neural
  - architecture
  - design
  - neuroscience
  - llm
  - transformer
  - computing
  - infrastructure
  - research
  - ai
date: 2026-08-22 21:00
source: GetNotes
score: 18
---

## Original Note

---
note_id: 1919109459725663344
title: "FFN 稀疏性深度拆解：90% 神经元白吃算力，怎么靠跳过它们提速 11 倍？"
type: link
created: 2026-08-21 18:59:23
source: getnote
kb: 
---

# FFN 稀疏性深度拆解：90% 神经元白吃算力，怎么靠跳过它们提速 11 倍？

### 🔍 FFN 的稀疏到底有多严重？

不同模型稀疏度差异极大，**ReLU 系天然远高于 SwiGLU 系**。

| 模型 | 激活函数 | 稀疏度 |
| :--- | :--- | :--- |
| OPT-30B | ReLU | **97%** |
| OPT-175B | ReLU | ~80% |
| LLaMA2-13B | SwiGLU | 43% |
| Yi-34B | SwiGLU | 53% |
| ProSparse-LLaMA2-7B | ReLU（改造） | 89% |
- **差异根源**：
  - **ReLU** = max(0, x) → 负值直接清零，**天然制造稀疏**
  - **SwiGLU/GELU** → 输出连续值，不会精确为零，但大量值"接近零"可安全跳过
- **反常识选择**：现代 LLM（LLaMA、GPT-4）大多用 **SwiGLU** 而非 ReLU → 主动放弃天然稀疏，换取**训练梯度更稳定**

### 📊 稀疏是随机的吗，有没有规律可抓？

神经元激活服从**幂律分布**，少数热门神经元跨任务稳定激活。
- **核心规律**：
  - OPT-30B（ReLU）：**26%** 神经元贡献 80% 激活
  - LLaMA2-70B ReGLU：43% 贡献 80%
  - LLaMA2-70B SwiGLU：69% 贡献 80%
- **跨任务稳定性**：同一组"热门"神经元在不同任务间 **90%+ 重合**
  说白了，不管是做题、聊天还是写代码，模型里总有一小撮"劳模"神经元一直在干活，剩下的大部分只是偶尔出场。

### ⚡ Deja Vu 怎么靠预测跳过神经元？

用轻量 MLP 提前预判活跃神经元，**OPT-175B 实现 2 倍加速**。
- **核心思路**：上下文稀疏 → 每层只需一小部分神经元就能得到与稠密模型几乎相同的输出
- **三步设计**：
  1. **训练轻量预测器**：每层一个小 MLP（比主模型小 100x+），输入上层输出 → 预测当前层哪些神经元激活
  2. **异步预测**：算第 L 层时，预测器已在算第 L+1 层的激活名单
  3. **只算活跃神经元**：跳过预测为沉默的部分
- **效果**：
  - 比 FasterTransformer **2x 加速**，比 HuggingFace **6x 加速**
  - 预测准确率 **93%+**，模型精度（perplexity、下游任务）不降
- **局限**：要求整个模型都在 GPU 上，对消费级显卡不友好

### 🚀 PowerInfer 怎么让消费级显卡追上 A100？

热神经元放 GPU、冷神经元放 CPU，**RTX 4090 最高提速 11.69 倍**。
- **核心架构**：利用幂律分布 → 热的常驻高速显存，冷的留在主存
- **四步设计**：
  1. **离线 profiling**：统计每个神经元激活频率，划分 hot/cold
  2. **智能放置**：hot 预加载到 GPU，cold 留在 CPU 内存
  3. **在线预测**：每层推理前用轻量预测器判断哪些 cold 被激活
  4. **独立计算**：GPU 算 hot + 少量 cold，CPU 算大量 cold，**几乎无 PCIe 传输**
- **实测效果（RTX 4090）**：
  - 量化模型：13.20 tokens/s → 比 llama.cpp 加速 **8x**
  - 非量化模型：8.32 tokens/s → 比 llama.cpp 加速 **11.69x**
  - 对比 A100（¥14万）：仅慢 **18%**（RTX 4090 售价 ¥1.4万）
- **本质区别**：传统 offloading（llama.cpp）按"层"切分 → 每层都要搬大量数据；PowerInfer 按"神经元"切分 → 绝大多数计算天然在本地完成

### 🧪 ProSparse 怎么人为造出更高稀疏度？

把 SwiGLU 换成 ReLU + 渐进正则，**稀疏度从 43% 推到 89%+**。
- **三步改造**：
  1. **激活函数替换**：SwiGLU → ReLU，引入天然稀疏
  2. **渐进式 L1 正则化**：正弦曲线缓慢增加 L1 惩罚，逼迫更多神经元输出趋近零
  3. **阈值偏移（FATReLU）**：激活阈值从 0 上移，"接近零"的值也算不活跃
- **效果**：
  - LLaMA2-7B：**89.32%** 稀疏
  - LLaMA2-13B：88.80% 稀疏
  - MiniCPM-1B：87.89% 稀疏
  - 基准测试精度与原版 Swish 可比，配合 PowerInfer 实现 **4.52x 加速**
- **不损精度的原因**：FFN 本来就是稀疏字典，绝大多数 key 本来就不匹配当前 token；ProSparse 只是把"几乎不匹配"显式化为"完全不匹配"

### 🔮 下一步：稀疏还能再升级吗？

稀疏粒度从**单个神经元**升级到**整个 Transformer 层**，即 Mixture of Depths（MoD）。
- 简单 token 直接走残差连接，**87.5% 的 token 可绕过整个 block**
- 下一篇主题：《Mixture of Depths——连整层都可以跳过》

### 📝 补充细节
- **三篇核心论文**：
  - Deja Vu（ICML 2023）：上下文稀疏预测
  - PowerInfer（SOSP 2024）：GPU-CPU 冷热混合推理
  - ProSparse（COLING 2025，清华 + 腾讯）：主动制造稀疏
- **加速倍数区间**：利用 FFN 稀疏可实现 **2–11x** 推理加速，且不损模型精度

---
*getnote | 2026-08-22 21:00*


---

## Related Notes

[[Papers-MOC]]
[[iNEST-MOC]]
[[paper2_liquid_computing_chemistry]]
