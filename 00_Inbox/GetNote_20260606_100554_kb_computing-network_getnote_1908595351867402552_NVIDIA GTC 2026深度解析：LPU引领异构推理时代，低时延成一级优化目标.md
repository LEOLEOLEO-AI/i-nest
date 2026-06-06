---
title: kb_computing-network_getnote_1908595351867402552_NVIDIA GTC 2026深度解析：LPU引领异构推理时代
tags:
  - semiconductor
  - chip
  - first-principles
  - top-journal
  - neural
  - computing
  - infrastructure
  - network
  - paper
  - physics
  - neuroscience
  - fpga
  - hardware
  - design
  - architecture
date: 2026-06-06 10:05
source: GetNotes
score: 24
---

## Original Note

---
note_id: 1908595351867402552
title: "NVIDIA GTC 2026深度解析：LPU引领异构推理时代，低时延成一级优化目标"
type: link
created: 2026-04-30 10:58:57
source: getnote
kb: computing-network
---

# NVIDIA GTC 2026深度解析：LPU引领异构推理时代，低时延成一级优化目标

### **🚀 LPU的战略意义：低时延推理成为独立架构方向**

**核心判断**  
LPU（Language Processing Unit）的推出标志着**低时延推理**从"GPU的子任务"升级为独立优化的一级问题。其核心价值在于：  
- **异构分工**：与Vera Rubin GPU形成"两引擎架构"（two-engine architecture），GPU负责高吞吐Prefill与Attention，LPU专攻低时延Decode阶段的FFN（前馈网络）和MoE专家层  
- **系统重构**：推动推理从单一硬件优化走向多引擎协同，解决算力资源错配问题  

### **🔄 推理架构演进：从PD分离到AFD的解耦深化**

#### **(一) 推理解耦的三个阶段**

![推理架构演进图示](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ffdba558f007d65a71b36c282660346a4?Expires=1783303350&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=QE7NTPBAkH0Gf%2Bit8mW0kN4btuo%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)

| 阶段 | 核心特征 | 代表技术 | 解决问题 |
|------|----------|----------|----------|
| **阶段一：混合部署** | Prefill与Decode共享GPU资源 | 单体架构 | - |
| **阶段二：PD分离** | Prefill与Decode物理分离 | DistServe、Splitwise、Mooncake | 阶段间资源错配 |
| **阶段三：AFD分离** | Decode内部Attention与FFN解耦 | Janus、MegaScale-Infer、Step-3 | 算子级资源错配 |

#### **(二) PD分离与AFD的本质差异**

| 维度 | PD分离（阶段级解耦） | AFD分离（算子级解耦） |
|------|----------------------|-----------------------|
| **分离对象** | Prefill与Decode阶段 | Decode内部Attention与FFN/MoE |
| **核心矛盾** | 算力需求（Prefill）vs 带宽需求（Decode） | 状态依赖（Attention）vs 无状态计算（FFN） |
| **通信特征** | 低频大块KV Cache迁移（GB级） | 高频小包激活传输（MB级） |
| **主要约束** | **带宽墙**（Bandwidth Wall） | **时延墙**（Latency Wall） |
| **网络优先级** | 带宽 > 时延 > 协议效率 | 时延 > 协议效率 > 带宽 |

### **⚙️ 异构推理分工：Rubin GPU与LPU的协同机制**

#### **(一) 功能划分**
- **Vera Rubin GPU**：负责Prefill、长上下文处理、Decode阶段的Attention计算（依赖KV Cache）  
- **Groq LPU**：专注Decode阶段的FFN/MoE执行，利用片上SRAM实现确定性低时延  

#### **(二) LPU选择FFN的技术逻辑**
1. **无状态特性**：FFN仅依赖当前token激活，无需访问历史KV Cache（对比Attention需持续读取GB级状态）  
2. **确定性执行**：匹配LPU编译器驱动的显式数据流控制，压缩抖动（Jitter）  
3. **SRAM带宽优势**：150TB/s片上带宽适配小批量、低时延计算需求  
4. **系统减负**：释放GPU HBM资源用于KV Cache存储，提升并发能力  

### **🔧 LPX系统架构：从芯片到网络的全栈设计**

#### **(一) 两种拓扑形态对比**

| 指标 | NVIDIA官方方案（8 LPU/Tray） | SemiAnalysis方案（16 LPU/Tray） |
|------|------------------------------|----------------------------------|
| **单Rack Tray数量** | 32 | 16 |
| **每Tray LPU数** | 8 | 16 |
| **总LPU数** | 256 | 256 |
| **CPU:LPU配比** | 1:8 | 1:16 |
| **拓扑特征** | 简化工程实现，1U标准形态 | 52层PCB+Belly-to-Belly布局，密度更高 |
| **C2C链路分配** | Tray内56条/跨Tray31条/扩展4条/FEL5条 | Tray内60条/跨Tray30条/扩展4条/FEL2条 |

#### **(二) FEL/FPGA的关键作用**

**Fabric Expansion Logic**是LPU系统的"神经中枢"，承担四大角色：  
1. **协议转换**：C2C转PCIe/以太网，连接LPU与外部系统  
2. **抖动隔离**：平滑外部网络波动，保障LPU确定性执行  
3. **容量扩展**：管理256GB外部DRAM，构建分层存储  
4. **可编程适配**：支持动态调整路由规则与通信协议  

### **🌐 网络战略：以太网成为异构推理统一底座**

#### **(一) 从CMX到LPX的以太网演进**
- **CMX（ICMS）**：PD分离场景下承载KV Cache等状态数据  
- **LPX**：AFD场景下承载FFN激活等高优先级流量  

#### **(二) 以太网替代专用互连的核心原因**
1. **异构兼容性**：统一连接GPU/LPU/CPU/DPU等多元节点  
2. **可扩展性**：支持多级交换、故障隔离与动态路由  
3. **运维成熟度**：兼容现有数据中心QoS/遥测体系  
4. **成本优势**：供应链成熟度与端口经济性  

### **📈 市场影响：推理系统价值函数的重构**

#### **(一) 性能指标变迁**
- **香草时代**：关注TPS/MW（每瓦吞吐）  
- **Agentic AI时代**：核心指标转向TPS/User（每用户吞吐）与**超低时延推理（ultra-low-latency inference）**  

#### **(二) 商业逻辑转变**
- **技术路径**：从"单一最强GPU"转向"GPU+专用引擎"异构协同  
- **价值主张**：高价值交互场景（如Agent长链推理）的体验优化成为竞争焦点  

### **📝 补充细节**
1. **关键术语解释**  
   - **TTFT**：首token延迟，用户感知第一指标  
   - **TPOT**：每输出token延迟，影响流式生成流畅度  
   - **AFD**：Attention-FFN Disaggregation，算子级解耦架构  

2. **潜在风险点**  
   - FEL实现质量决定端到端时延，可能成为系统瓶颈  
   - 以太网小包效率（如RoCE协议开销）需专用优化（推测NVLINKoE协议）  

3. **行业影响**  
   - 推动模型设计向"硬件友好型"演进（如算子拆分优化）  
   - 加速推理数据中心网络重构，通信时延成为性能上限

---
*getnote | 2026-06-06 10:02*


---

## Related Notes

[[iNEST-MOC]]
[[FPGA原型]]
[[paper1_iNEST_core_architecture]]
[[SDI化合物键_四型架构]]
[[Papers-MOC]]
