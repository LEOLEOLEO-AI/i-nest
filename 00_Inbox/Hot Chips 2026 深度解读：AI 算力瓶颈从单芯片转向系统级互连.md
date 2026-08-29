---
title: "Hot Chips 2026 深度解读：AI 算力瓶颈从单芯片转向系统级互连"
tags:
  - hardware
  - design
  - architecture
  - computing
  - semiconductor
  - network
  - chip
  - infrastructure
date: 2026-08-29 22:20
source: GetNotes
score: 32
---

## Original Note

---
note_id: 1919847969688537832
title: "Hot Chips 2026 深度解读：AI 算力瓶颈从单芯片转向系统级互连"
type: link
created: 2026-08-29 18:02:34
source: getnote
kb: 
---

# Hot Chips 2026 深度解读：AI 算力瓶颈从单芯片转向系统级互连

### 🏆 本届 Hot Chips 核心结论是什么？

**训练算力堆叠已触顶**，推理系统瓶颈转向**数据搬运与异构互连**。
- **基本信息**：第 38 届 Hot Chips 于 2026 年 8 月 25 日在斯坦福落幕，主题为 *Architectures for the Agentic Computing Era*。
- **议程分布**：共 48 个议题，AI 加速器 7 项、存储教程 6 项、CPU 6 项、GPU 与网络各 4 项，覆盖未来 18–24 个月数据中心技术路线。
- **主线转变**：单芯片峰值算力不再是核心叙事，系统有效算力由 **互连带宽、内存一致性、调度平面** 共同决定。

### 🔧 训练/推理分工发生了什么变化？

分工已从**软件调度下沉到芯片与封装层级**，由器件架构静态定义。
- **Google 第八代 TPU**：首次拆分为训练向 **TPU 8t** 与推理向 **TPU 8i**
  - TPU 8t：单 pod 9600 卡、121 FP4 ExaFLOPS、2PB 共享 HBM
  - TPU 8i：单卡 288GB HBM、片上 SRAM 为上代 3 倍、ICI 带宽 19.2 Tb/s
- **其他厂商动向**：
  - NVIDIA 引入 **LPU（低延迟推理加速器）** 与 GPU 并列
  - AMD 两周内收购 decode 专用芯片厂商并签署晶圆级合作
  - OpenAI 首次参会，披露与 Broadcom 协同设计的 **Jalapeño 推理 ASIC**，目标 2026 年底部署
  - 同场展示：Meta MTIA、微软 Maia 200（已在 Iowa 数据中心量产）、SambaNova SN50 RDU、Cerebras 晶圆级机架架构
- **技术含义**：加速器异构化提升 → 互连拓扑与内存一致性协议 = 决定整体利用率的关键变量

### 🌐 网络角色发生了什么升级？

网络从**外设演进为系统一级组件**，开放互连标准形成第二阵营。

| 维度 | 代表技术 |
| :--- | :--- |
| 纵向扩展 | NVLink 6（3.6 TB/s）、NVL144 单域 144 GPU |
| 横向扩展 | BlueField-4 DPU（800 Gb/s）、64 核 Grace CPU |
| 集群规模 | 10⁶ 卡 AI 集群互连演进目标 |
- **关键方案**：
  - NVIDIA BlueField-4 + Spectrum-X Multiplane：DPU = AI 工厂控制与数据平面 OS，多平面架构隔离集合通信流、抑制尾延迟与拥塞
  - Broadcom Thor Ultra：面向 AI/HPC 的 Ultra Ethernet NIC，延续以太网替代 InfiniBand/NVLink 的路径
  - Mojo Vision：基于 Micro-LED 的大规模并行光 I/O，片间光互连从板级向封装级迁移
- **开放互连标准推进**：
  - **UALink 2.0** 规范定稿：新增网络内计算、芯片定义、可管理性规范，由 AMD、Intel、Meta 等联盟对标 NVLink；1.0 器件 2026 下半年进实验室、2027 年量产
  - **UCIe**：已进入 Intel 客户端 SoC 的 die-to-die 互连
  - **CXL 3.0**：成为计算型内存的互连基础
  - **NVLink Fusion**：向 RISC-V 生态开放，支持非 NVIDIA 加速器接入
- **技术含义**：开放互连 = 解除单一供应商锁定 + 异构加速器构建一致系统，对国内智算基础设施具备更高架构弹性

### 💾 内存墙瓶颈有什么新变化？

瓶颈从**容量约束转为带宽与数据搬运开销约束**。
- **HBM4 产业化拐点**：
  - 三星：HBM Base Die 从 DRAM 工艺转向逻辑工艺，实现定制化
  - SK 海力士：MR-MUF 与混合键合先进封装，压缩间距与热阻
- **存算一体（PIM）落地**：
  - 三星 **LPDDR5X-PIM**：全球首个基于 LPDDR 的存内计算方案
  - XCENA MX1：基于 CXL 的计算型内存
  - d-Matrix 与 Meta 联合展示 3D DRAM 推理加速器
  说白了，就是把计算挪到数据旁边，减少数据来回搬运的浪费。
- **HBF（高带宽闪存）**：SanDisk/铠侠推动，用 NAND 补充 HBM 容量层级，缓解 KV cache 等长上下文内存占用
- **技术含义**：算力增长 vs 访存带宽增长失配持续放大 → 新增 FLOPS 大量时间闲置等待数据；Agentic 负载的串行调用与长上下文 decode 进一步放大访存与互连开销

### 📏 性能度量出现了什么新问题？

**度量口径不统一**，成为新的技术博弈维度。
- **边界说明**：Hot Chips 是架构披露平台，非独立基准测试平台，所有数据均为厂商自报，缺乏统一工作负载与第三方验证。
- **差异化口径**：厂商分别采用 tokens/MW、tokens/W、性能/美元 等不同指标，凸显各自优势。

### 💡 对智算互联业务有哪些工程启示？

未来竞争单元是**系统级有效算力**，而非单器件峰值。
- **开放互连集成**：构建 UCIe / CXL / 统一以太网 / 光互连的适配能力，定位异构加速器的互连与一致性层
- **调度 × 网络融合**：将 DPU / 网络遥测前置进编排平面，使调度器具备拓扑、带宽、尾延迟感知能力
- **近存/存内与光互连**：跟踪 PIM、CXL 计算内存、共封装光模块（CPO）产业化节奏，布局数据搬运效率瓶颈

### 📝 补充细节
- 本文由智算互联研究团队基于 Hot Chips 2026 公开议程与一线技术报道整理，所有参数均引自厂商披露口径，量产节奏以官方公告为准。
- 性能数据建议以独立基准实测结果交叉验证后采信。

---
*getnote | 2026-08-29 22:20*


---

## Related Notes

[[paper1_iNEST_core_architecture]]
[[SDI化合物键_四型架构]]
[[iNEST-MOC]]
[[FPGA原型]]
