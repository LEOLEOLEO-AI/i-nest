---
title: 2026-06-28_2026 ODCC夏季全会ScaleUP互联技术深度观察_NetMem创新与SUE_UALink协议对比分析
date: 2026-06-28
source: Getnote
track: TCC
tags: [剪藏, getnote]
relevance: 2
status: 待处理
provenance: external
---

# 2026-06-28_2026 ODCC夏季全会ScaleUP互联技术深度观察_NetMem创新与SUE_UALink协议对比分析

> 来源: 得到Getnote 剪藏 | 日期: 2026-06-28

## 摘要

title: "2026 ODCC夏季全会ScaleUP互联技术深度观察：NetMem创新与SUE/UALink协议对比分析"

## 原始内容

---
note_id: 1914075848249217760
title: "2026 ODCC夏季全会ScaleUP互联技术深度观察：NetMem创新与SUE/UALink协议对比分析"
type: link
created: 2026-06-28 12:47:27
source: getnote
kb: 
---

# 2026 ODCC夏季全会ScaleUP互联技术深度观察：NetMem创新与SUE/UALink协议对比分析

### **🏛️ 会议背景与前沿技术动态**

本次内容来自2026年ODCC（开放数据中心委员会）夏季全会的一线产业观察，核心聚焦AI算力互联领域的**ScaleUP（纵向扩展）互联**方向的最新产业变化，同时回顾了多项技术的演进脉络：
1.  **NetMem技术复兴**：5~6年前提出的NetDAM相关工作在本次会议被重新拾起，该技术属于内存资源网络化池化的前沿方向。
2.  **RDMA技术落地进展**：作者团队3年前就完成了RDMA多路径算法、跨可用区（AZ）/跨Region场景的生产落地，当前eRDMA规模高速增长阶段几乎无客户故障工单，例如某自动驾驶模型训练客户长期未出现RoCE类网络中断/拥塞投诉，对比之下Mellanox（Nvidia）的相关方案仍在迭代，OAI推出的MRC方案表现不佳。作者同时指出传统PFC/DCQCN从设计之初就存在本质缺陷。

### **💡 NetMem（Network Attached Memory）技术解析**

NetMem是本次会议上云豹分享的创新内存架构，属于内存资源网络化池化的典型实践，核心特性如下：

#### 架构核心逻辑

NetMem的设计思路并非完全从零创新，而是对现有技术的重构优化，其等效逻辑可归纳为：
| 等效公式 | 核心含义 |
| :--- | :--- |
| NETMEM ≈ UB MEMORY POOL - UB + ETH | 从统一内存池架构中剥离UB组件，替换为以太网实现 |
| NETMEM ≈ CPU/GPU + SU_Port - (xPU)Cores | 计算单元剥离核心算力，仅保留ScaleUP互联接口 |
| NETMEM ≈ (Sort of) DPU? | 形态上接近专用内存处理单元，与DPU定位有部分相似性 |

#### 正式定义与核心参数

NetMem是一款专用芯片，通过4x800Gbps以太网端口将LPDDR5X DRAM资源接入Scale Up域网络，实现内存资源的网络化池化与共享，让任意计算节点可通过标准以太网访问远程内存，突破单节点内存容量上限。其核心架构参数如下：
| 模块 | 关键规格 |
| :--- | :--- |
| 以太网PHY&MAC | 4x800Gbps |
| Semantic Fabric交换能力 | 400GB/s |
| LPDDR5X控制器规格 | 24通道，总带宽460GB/s |
| 核心延迟指标 | 协议解析到内存事务零拷贝映射，延迟低于50ns |
| 支持协议 | UALINK / SUE / OISA / UnifiedBus等多种Scale Up协议 |
| 管理单元 | RISC-V MCU负责带外管理 |

### **⚖️ ScaleUP两大主流协议SUE与UALink深度对比**

本次会议中产业界对ScaleUP互联的争议将在2026年10月迎来明确结论，核心参考两个标杆事件：AWS下一代Trainium产品对比NVLink Fusion和UALink的性能差异，以及AMD的UALink over Ethernet方案与纯UALink方案的性能差距。两大协议的核心差异可从多维度展开：

#### 协议栈架构本质区别

| 维度 | SUE (Scale Up Ethernet) | UALink (Ultra Accelerator Link) |
| :--- | :--- | :--- |
| 设计思路 | 扩展标准以太网，基于现有以太网协议栈逐层扩展 | 从物理层到协议层全新设计自定义Flit（流片）协议 |
| 传输单元 | 可变长以太网帧，MTU范围64B - 9KB | 固定大小Flit传输：64B TL Flit、640B DL Flit、680B Codeword |
| 核心调度逻辑 | Per-Destination Queue + WRR（按目的地XPU分离队列，加权轮询调度） | Unified Buffer + DL Flit Aggregation（统一缓冲区聚合多目的地TL Flit） |
| 链路利用率 | 受单帧单目的地约束，链路利用率上限较低 | DL Flit内可混合不同目的地TL Flit，最大化链路利用率 |

#### 交换机转发行为差异
- **SUE转发流程**：发送端I/O Die按`{dst XPU, VC}`分离队列，机会性将同目的地命令打包为最大4096B的PDU，通过标准L2以太网交换机按整帧转发，交换机每个出口对应独立Egress队列。在Incast（多对一并发）场景下，大量发往同一目的地的帧会在出口队列积压，触发PFC背压，引发Head-of-Line（队头）阻塞。
- **UALink转发流程**：发送端生成不区分目的地的64B TL Flit，统一存入缓冲区凑满640B DL Flit后发送，自定义ASIC交换机终结DL层，逐个解析TL Flit的目的地信息路由，在出口重新聚合为DL Flit转发。本质是细粒度的Flit级Crossbar交换机，转发粒度从SUE的4096B~9000B降低到64B。

#### Incast场景抗拥塞能力对比

| 场景表现 | SUE | UALink |
| :--- | :--- | :--- |
| 拥塞形态 | 整包级出口拥塞，4096B大帧同时涌入同一出口队列 | 64B细粒度调度，无整包积压 |
| 阻塞影响 | 触发PFC XOFF，队头阻塞扩散到整个链路，长尾延迟不可控 | Credit耗尽自然限流，无HOL阻塞，延迟线性可控 |
| 调度粒度 | 4096B级粗粒度 | 64B级细粒度，压力降低64倍 |

### **📜 技术演进的历史脉络与选型建议**
1.  **技术溯源**：作者是以太网ScaleUP方向的最早提出者，2020-2021年伴随NetDAM项目启动相关研发，曾向博通（BRCM）提出类似Nvidia FinePack的多TL Flit聚合设计需求，但厂商仅参考了论文表层实现，导致SUE协议当前存在打包机制的固有缺陷。
2.  **架构适配选型指南**：
    - 针对DSA类专用加速架构（如TPU，Tensor Core规模256x256/320x320，片上大Buffer）：大尺寸Tensor Tile对细粒度Flit需求低，SUE和UALink均可适配。
    - 针对GPGPU类通用加速架构（如CUDA兼容GPU，Tensor Core规模16x16，SM上SMEM容量有限）：对低延迟、低长尾的细粒度传输需求极强，UALink是更适配的唯

<!-- orphan-cleanup: linked to MOC -->
## 来源回链

- [[TCC_Master_Index]]
