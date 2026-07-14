# P2 综述框架 — 知识库缺口补充（2026-07-07）

## 缺口 1：NVLink 6.0 (Rubin) 最新参数 ✅ 已部分补充

### 来源：知识库 GTC 2026 深度解析

**Vera Rubin GPU 核心参数（GTC 2026 披露）：**
- 架构定位：与 LPU 构成"两引擎架构"（two-engine architecture）
  - Vera Rubin GPU：负责 Prefill、长上下文处理、Decode 阶段 Attention（依赖 KV Cache）
  - LPU：专攻低时延 Decode 阶段 FFN 和 MoE 专家层
- **LPU SRAM 带宽**：150 TB/s 片上带宽
- **网络协议**：推测推出 NVLINKoE 协议（NVLink over Ethernet 优化版）
- **时延优先级**：时延 > 协议效率 > 带宽（与训练场景相反）

### 仍需补充
| 参数 | 状态 |
|------|------|
| NVLink 6.0 单链路带宽 | ⚠️ 待确认（预估值 ~200GB/s per lane） |
| NVL144/NVL288 超节点规模 | ⚠️ 待确认 |
| Rubin GPU 具体互联拓扑 | ⚠️ 待从 NVIDIA GTC 2026 官方 Keynote 补充 |

### 推荐补充来源
- NVIDIA GTC 2026 Keynote (Jensen Huang)
- NVIDIA Rubin Architecture White Paper

---

## 缺口 2：Google TPU ICI 互连最新架构 ✅ 已充分补充

### 来源：知识库《谷歌TPU五代技术演进深度分析》+ Google TPU 3D拓扑设计

**Ironwood TPU (2025) 核心参数：**
| 指标 | 数值 | 相比 TPU v2 |
|------|------|-------------|
| 峰值 BF16 性能 | 2,307 TFLOPS | **50倍** |
| 峰值 FP8 性能 | 4,614 TFLOPS | — |
| HBM 容量 | 192 GiB | 12倍 |
| HBM 带宽 | 7,300 GB/s | 10倍 |
| 超级计算机规模 | 9,216 节点 | 36倍 |
| 超级计算机性能 | 21.3 EFlops | **3,600倍** |
| 每瓦性能 | 29.3倍 | 30倍 |

**ICI 互连拓扑（从 v4 到 Ironwood 不变）：**
- 3D Torus 拓扑：4×4×4 立方体构建块
- 立方体内 16 TPU 通过铜互连（每条链路 50 GB/s）
- 立方体间通过 96 条光链路连接 48 个 OCS（每条光链路 100 GB/s）
- 任意两点通信 ≤ 3 跳
- OCS（光电路交换机）实现拓扑动态重构、增量部署、故障隔离
- 通信延迟相比 2D NoC 降低 40%，聚合带宽提升 3 倍

**架构稳定性：**
- TPU v2 (2017) 至 Ironwood (2025)，双 TensorCore 核心架构保持不变
- SparseCore 从专用嵌入训练单元演变为通用计算卸载引擎（处理 AllReduce 等集合操作）
- XLA 编译框架保持核心地位，JAX 成为首选语言

**David Patterson 等作者，IEEE Micro (2026年7-8月) 发表**

---

## 缺口 3：AMD Infinity Fabric 最新参数 ⚠️ 部分补充

### 来源：知识库《VLSI 2025：AMD AI硬件平台架构趋势》

**已知信息：**
- AMD 采用 Chiplet 架构：MI300 = 13 Chiplet + 8 HBM3 堆栈（1460亿晶体管）
- CDNA 3 架构，3D 堆叠 + 有源中介层
- UALink 联盟开发开放 Scale-Up 互连标准（AMD 参与）
- Scale-Up 仍以铜缆为主，Scale-Out 以光纤为主

### 仍需补充
| 参数 | 状态 |
|------|------|
| MI355X / MI400 Infinity Fabric 带宽 | ⚠️ 待从 AMD 技术白皮书补充 |
| UALink 1.0 规格 | ⚠️ 需要最新联盟发布文档 |
| Infinity Fabric 4.0 具体参数 | ⚠️ 待查 |

---

## 缺口 4：光互连部署数据 ⚠️ 部分补充

### 来源：知识库《VLSI 2025：AMD AI硬件平台架构》

- 铜互连限制：信号衰减限制铜缆长度（~1m for passive copper）
- 光学互连在计算层面即将采用
- 挑战：短距离冷却、硅封装尺寸、激光可靠性、成本
- 未来若成本功耗足够低，可能取代铜缆作为本地互连
- 主流方案：CPO (Co-packaged Optics)、NPO (Near-packaged Optics)、LPO (Linear-drive Pluggable Optics)

### 推荐补充来源
- OFC 2026 会议论文
- TSMC COUPE (Compact Universal Photonic Engine) 白皮书
- Ayar Labs / Lightmatter 等初创公司最新产品参数

---

## 缺口 5：Cerebras Condor Galaxy 集群真实数据 ⚠️ 基础信息

### 来源：知识库

**已知：**
- Cerebras WSE-2：2.6万亿晶体管，85万核心，单芯片=整张晶圆
- SwarmX 网络架构
- CS-3 预计搭载 WSE-3（但知识库中无具体参数）

### 仍需补充
| 参数 | 状态 |
|------|------|
| WSE-3 晶体管数/核心数 | ⚠️ 待查 Cerebras 官方发布 |
| Condor Galaxy 集群训练吞吐量 | ⚠️ 待从客户案例/白皮书补充 |
| SwarmX 网络架构带宽延迟 | ⚠️ 已有基础文件（WSE SwarmX 优化方案） |

---

## 缺口 6：国内超节点最新进展 ✅ 已充分覆盖

### 来源：知识库

**华为灵衢（UB-Mesh）：**
- Hot Chips 2025 披露：统一总线互连，挑战 NVLink
- 即将开源（知识库文件记载）
- 华为 UB-Mesh 与 SDSoW 形成端到端互连方案

**华为昇腾：**
- Atlas 900 超节点集群
- HCCS (Huawei Cache Coherence System) 互连

**SDSoW（软件定义晶上系统）：**
- 中国原创架构：软件定义互连 + 正交原语集 + 拓扑融合
- "十五五"国家重大工程布局（2026-2035）
- 与 DeepSeek 组成"双子星"方案
- TSMC SoW-X 竞品定位

**ODCC 2026 超节点大会：**
- AI 基础设施 Scale-Up 技术路线圆桌讨论
- 铜缆 vs 光互连、Scale-Up vs Scale-Out 辩论

---

## 总结：缺口补充情况

| 缺口 | 状态 | 可信度 |
|------|:--:|:--:|
| NVLink 6.0 / Rubin | ⚠️ 部分 | 中（来自第三方 GTC 分析，非一手数据） |
| Google TPU ICI | ✅ 充分 | 高（IEEE Micro 论文 + 谷歌官方数据） |
| AMD Infinity Fabric | ⚠️ 弱 | 低（数据停留在 2023 MI300） |
| 光互连部署数据 | ⚠️ 部分 | 中（VLSI 2025 报告） |
| Cerebras Condor Galaxy | ⚠️ 弱 | 低（缺少 WSE-3/CS-3 数据） |
| 国内超节点进展 | ✅ 充分 | 高（多源交叉验证） |

> **建议：** 缺口 1、3、4、5 需进一步通过以下渠道补充后，方可写入综述正文：
> - NVIDIA/AMD/Google 官方技术白皮书（2025-2026）
> - OFC 2026 / Hot Chips 2025-2026 会议论文
> - Cerebras 官网 + 客户案例
> - arXiv 最新 preprint（搜索 "NVLink Rubin"、"Infinity Fabric MI400"、"CPO AI cluster"）
