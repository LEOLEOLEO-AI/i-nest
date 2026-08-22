---
title: "FreeToken 深度解析：消费级显卡跑 284B 大模型，端侧推理的新突破"
tags:
  - paper
  - architecture
  - design
  - llm
  - transformer
  - computing
  - infrastructure
  - research
  - ai
date: 2026-08-22 21:00
source: GetNotes
score: 15
---

## Original Note

---
note_id: 1919208050700620776
title: "FreeToken 深度解析：消费级显卡跑 284B 大模型，端侧推理的新突破"
type: link
created: 2026-08-22 20:29:43
source: getnote
kb: 
---

# FreeToken 深度解析：消费级显卡跑 284B 大模型，端侧推理的新突破

### **🚀 FreeToken 到底有多强？**

**单卡消费级 GPU**就能跑前沿大模型，速度远超现有推理框架。
- **核心成果**：
  - **笔记本 RTX 4060（8GB）**：跑 **Qwen3.6-35B** 达 **39.3 tok/s**，超过 Codex 生产环境中位速度（33 tok/s）。
  - **桌面 RTX 5090（32GB）**：跑 **DeepSeek-V4-Flash 284B** 达 **25 tok/s**。
  - **RTX PRO 6000**：跑 **GLM-5.2 753B** 达 **14.9 tok/s**。
- **速度对比**（相同硬件下）：
  - 比 **llama.cpp** 快 **1.46 倍**。
  - 比 **Ollama** 快 **2–4 倍**（部分场景最高达 3 倍）。
  - Ollama 甚至无法加载 284B 级别的模型。

### **👥 谁开发了 FreeToken？**

由 **UC Berkeley、MIT、UT Austin** 等机构联合研发，顶尖学者参与。
- **并列一作**：杨硕（UC Berkeley EECS 博士生）、范晓泽（UT Austin），两人本科均毕业于**上海交通大学**。
- **核心作者**：Ion Stoica、Matei Zaharia、Kurt Keutzer、韩松等领域知名学者。
- **开源地址**：GitHub（FlashML-org/FreeToken）、官网 flashml.ai，论文已上传 arXiv。

### **💻 消费级硬件能跑出什么体验？**

实现了**交互级实用速度**，解决了传统卸载方案的卡顿问题。
- **传统方案痛点**：CPU-GPU 权重卸载受 PCIe 带宽限制，推理速度仅每秒几 token，长 Prompt 下 I/O 阻塞严重。
- **FreeToken 表现**：
  - **首 Token 延迟（TTFT）**：处理 4–16k 长上下文时，比传统方案**降低 42–58%**。
  - **Agent 多轮交互**：引入状态复用后，后续轮次 TTFT **减少 65–80%**。
  - **显存不足也能跑**：显存被其他应用占用 4–8GB 时，传统方案会 OOM 崩溃，FreeToken 可**0 停机平滑降级**。
- **硬件要求参考**：跑 DeepSeek-V4-Flash（专家池约 140GB），建议 **32GB 显存 + 192GB 内存**。

### **⚙️ 为什么 FreeToken 能做到这么快？**

核心是**把 CPU、内存、PCIe、GPU 当成统一弹性平台调度**，而非只靠显存。
说白了，以前大模型必须全塞进显存才能跑，现在显存不够内存来凑，还能跑得很快。
- **全层双缓冲 Prefill**：GPU 计算第 l 层时，后台已通过 PCIe 预取第 l+1 层专家权重 → 计算与数据搬运完全重叠 → 消除 I/O 等待气泡。
- **带宽自适应混合调度**：
  - 实时探测 PCIe 带宽 + CPU 算力 → 动态算出最优分流比例。
  - 专家命中 GPU LRU 缓存直接算；未命中的部分传 GPU、部分留 CPU 并行算 → 硬件吞吐拉满。
  - 后台有高 I/O 任务抢总线时，自动提升 CPU 分流比例；总线空闲则多走 GPU。
- **面向 Agent 的状态复用**：
  - 在 `<think>`、`<tool_call>` 等特殊 Token 边界设轻量检查点。
  - 上下文修改（如加工具返回结果）时，只需从最近锚点恢复、增量 Prefill → 不用重算整段上下文。
- **弹性显存热扩缩容**：其他应用抢显存时，动态缩小 GPU 专家缓存大小 → 服务不中断、不崩溃。

### **📌 补充细节**
- **MoE 架构特性**：DeepSeek-V4-Flash 共 284B 参数、43 层、每层 256 个专家选 6 个，单 token 仅激活 13B 参数，活跃部分能塞进 32GB 显存，但完整专家池远超显存容量。
- **支持范围**：已支持超过 20 种 MoE 模型，覆盖编码、工具调用等 Agent 场景。
- **易用性**：提供 Windows / Linux 桌面 GUI 应用，也可通过 CLI 一行命令安装（`uv pip install "freetoken [accel]"`）。
- **测试覆盖**：在 PCIe 3.0 x8、PCIe 4.0 x16、PCIe 5.0 x16 等不同总线规格，以及 Intel i7、AMD Ryzen 9、Threadripper 等 CPU 上均做了验证。

---
*getnote | 2026-08-22 21:00*


---

## Related Notes

[[Papers-MOC]]
[[iNEST-MOC]]
[[paper2_liquid_computing_chemistry]]
