---
title: "Hot Chips 2026 芯片大会全景：8 大厂商 AI 加速器全梳理"
tags:
  - chip
  - design
  - first-principles
  - infrastructure
  - network
  - semiconductor
  - hardware
  - llm
  - computing
  - physics
  - ai
  - transformer
  - architecture
date: 2026-09-04 21:00
source: GetNotes
score: 34
---

## Original Note

---
note_id: 1920402001141888048
title: "Hot Chips 2026 芯片大会全景：8 大厂商 AI 加速器全梳理"
type: link
created: 2026-09-04 17:22:16
source: getnote
kb: 
---

# Hot Chips 2026 芯片大会全景：8 大厂商 AI 加速器全梳理

### 🏭 今年大会的核心主题是什么？

**Agentic AI（智能体AI）** 和 **企业级推理** 是两大核心方向。

### 🟢 NVIDIA 拿出了什么方案？

**7 颗自研芯片协同**，组成完整 AI 工厂平台。
- **平台名称**：Vera Rubin
- **核心思路** = 计算 + 网络 + 存储 + 编排全栈自研，不单打独斗

| 芯片 | 定位 | 关键规格 |
| :--- | :--- | :--- |
| **Rubin GPU** | 大模型计算/长上下文 | 288GB HBM4，22TB/s 带宽；NVFP4 推理 50PFLOPS（Blackwell 的 5 倍） |
| **Groq 3 LPX** | 超低延迟 Token 生成 | 单机柜 256 颗 LPU，Gemma 4 31B 下 **3,431 tokens/s** |
| **BlueField-4 DPU** | 智能网卡/内存编排 | 64 核 Grace CPU，800Gbps，KV 缓存加速 |
| **ConnectX-9 SuperNIC** | 高速网络接口 | 每 GPU 1.6Tb/s 横向扩展带宽 |
| **NVLink 6 Switch** | GPU 间互联 | 单 GPU 全互连 3.6TB/s |
| **Spectrum-6 交换机** | 数据中心以太网 | 102.4T 芯片，CPO 共封装光模块 |
| **Vera CPU** | 智能体编排 | 88 核自研 Olympus 核心，1.5TB 内存 |
- **100MW AI 工厂规模**：NVFP4 推理 2 ZFLOPS + 训练 1.4 ZFLOPS + 11PB HBM4 + 800PB/s 带宽

### 🔴 AMD 的 MI400 系列有什么亮点？

**旗舰 MI455X 配 432GB HBM4**，主打系统级容错。
- **架构**：全新 CDNA 5，台积电 **2nm** 制程
- **封装**：CoWoS-L，最多 8 个 XCD 计算芯片 + 独立 MID 芯片
- **系统方案**：Helios AI 机架，单机架 **31TB HBM4**

| 型号 | 定位 | 关键规格 |
| :--- | :--- | :--- |
| **MI455X** | 旗舰训练/推理 | 432GB HBM4，19.6TB/s 带宽；FP4 40PFLOPS |
| **MI430X** | 双精度科学计算 | 支持 FP64，已获橡树岭国家实验室订单 |
| **MI440X** | 企业本地 AI | 面向企业端推理部署 |
- **容错设计**：Scale-up 网络支持单链路、单交换机、整交换托盘故障，硬件层自动恢复软错误

### 🔵 Intel 两款加速器分别打什么市场？

**数据中心 + 客户端两端覆盖**，Crescent Island 纯做 AI 推理。

| 加速器 | 定位 | 关键规格 |
| :--- | :--- | :--- |
| **Crescent Island GPU** | 数据中心 Agentic AI 推理 | 32 个 Xe3P 核心，480GB LPDDR5x，350W 风冷 |
| **Wildcat Lake NPU** | 客户端/边缘 AI | 最高 **17 TOPS** 混合算力，集成 Xe3 图形 |
- **Crescent Island 特色**：
  - 支持 FP4/MXFP4 到 FP64 **全精度**
  - 移除 3D 渲染模块，晶体管全给 AI
  - 支持推测解码，每轮退役 **2.9–4.9 个 token**
- **软件生态**：原生适配 vLLM、SGLang、PyTorch

### ⚫ IBM 大型机 AI 加速有什么不一样？

**双架构核心 + 片上多加速器**，主打企业级可靠性。
- **核心设计**：每个物理核心原生支持 z/Architecture + AArch64，**纳秒级切换**
- **制程工艺**：2nm，11 核心，主频 **>5.7GHz**
- **缓存层级**：36MB 私有 L2 + 432MB Virtual-L3 + 3.5GB virtual-L4

| 加速器 | 定位 | 关键规格 |
| :--- | :--- | :--- |
| **2nd Gen AI Accelerator** | GenAI 推理 | 16 活跃 +1 冗余核心；600+ FP8 TOPS（上代 4 倍）；96GB HBM3e |
| **片上 Crypto 加速器** | 硬件密码学 | 对 z/Architecture 和 AArch64 均暴露 |
| **GZIP 压缩加速器** | 数据压缩 | 企业级压缩加速 |
| **排序加速器** | 数据排序 | 硬件级排序加速 |

### 🟠 OpenAI 自研芯片 Jalapeño 什么水平？

**专为推理优化**，性能对标 Blackwell，成本省一半。
- **合作方**：与 **Broadcom（博通）** 联合开发
- **研发周期**：从 RTL 到流片仅 **9 个月**
- **优化方向**：针对 Prefill 和通信阶段优化，减少数据移动
- **能效成本**：每瓦性能优于当前最先进水平，相比典型 GPU 节省约 **50% 成本**
- **性能定位**：与 NVIDIA Blackwell、Google TPU 相当
- **部署节奏**：2026 年底小批量 → 2027 年大规模 → 下一代 2028 年

### 🟡 Cerebras 晶圆级引擎进化到哪一步了？

**CS-4 集成 3 块晶圆**，推理速度比传统 GPU 快 30 倍。
- **核心架构**：晶圆级集成，延续 **90 万核心** 设计
- **片上缓存**：44GB SRAM
- **性能提升**：FP16 稀疏算力和内存带宽 = 前代 **2 倍**
- **系统级**：CS-4 集成 3 块 WSE-3 Turbo，片间互连延迟 **2μs**
- **实测数据**：运行 GPT-OSS 模型达 **4,465 tokens/s**，较传统 GPU 提升 30 倍
- **使用方式**：可作专用解码单元，与异构预填充硬件协同

### 🔵 Google TPU8 有什么已知信息？

**第八代 TPU 确认参展**，架构细节将在大会披露。
- 文件列表确认演讲文档：HotChips2026GoogleTPU8FinalFix.pdf

### 📋 还有哪些厂商参展？

| 厂商 | 方向 |
| :--- | :--- |
| **SambaNova** | 自定义 AI 推理芯片 |
| **dmatrix** | AI 推理加速器 |
| **Marvell** | 与 Google 合作定制 AI 推理/存储/网络芯片 |
| **Arm** | AGI CPU（Neoverse V3，最高 136 核，TSMC N3P） |
| **Infineon** | RISC-V 汽车电子加速器 |
| **Waymo** | 自动驾驶芯片技术 |

### 📈 今年整体技术趋势是什么？

**推理取代训练**成为头号战场，五大方向清晰。
1. **推理优先**：几乎所有厂商都把 Agentic AI 推理作为核心目标
2. **内存为王**：HBM4 / LPDDR5x / SRAM 多路并进，大容量高带宽成焦点
3. **异构协同**：单芯片不够用，多芯片、多架构协同成主流
4. **能效比至上**：从"拼总算力"转向"拼每瓦吞吐量"和"每 Token 成本"
   说白了，大家不再比谁算得快，而是比谁花一度电、一块钱能生成更多 token。
5. **专用化爆发**：推理专用、Token 生成专用、晶圆级引擎等专用加速器百花齐放

---
*getnote | 2026-09-04 21:00*


---

## Related Notes

[[paper2_liquid_computing_chemistry]]
[[iNEST-MOC]]
[[FPGA原型]]
[[SDI化合物键_四型架构]]
[[paper1_iNEST_core_architecture]]
