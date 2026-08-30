---
title: "3D-TokSIM：基于3D堆叠内存与Token驻留存内计算的LLM推理加速架构"
tags:
  - chip
  - hardware
  - energy
  - llm
  - neural
  - green-ai
  - first-principles
  - computing
  - physics
  - architecture
  - design
  - transformer
  - infrastructure
  - semiconductor
  - ai
  - neuroscience
date: 2026-08-31 07:23
source: GetNotes
score: 25
---

## Original Note

3D-TokSIM：基于3D堆叠内存与Token驻留存内计算的LLM推理加速架构

### **🔍 核心背景与挑战**

**大语言模型(LLM)推理瓶颈**：
- **存储墙问题**：自回归解码特性导致每生成1个token需从DRAM加载完整模型参数，GPU利用率不足25%。
- **架构失衡**：3D堆叠存储虽能提供TB/s级带宽，但逻辑层设计不当会导致计算能力成为新瓶颈。

**研究动机**：提出跨层优化架构，解决LLM推理中"内存访问耗时>>计算耗时"的Memory Bound困境。

### **🎯 核心方案概述**

**3D-TokSIM架构定义**：通过**混合键合(Hybrid Bonding)** 将DRAM垂直堆叠在逻辑芯片上，结合**Token驻留存内计算(Token-Stationary Compute-in-Memory)** 数据流，专门加速大模型的**投机解码(Speculative Decoding)** 推理。

### **💡 三大技术创新点**

#### **一、3D堆叠存储与计算协同设计**

![3D堆叠架构示意图]
- **物理实现**：多层DRAM Die通过Cu Pillar（铜柱）混合键合技术与逻辑Die垂直集成，突破传统2D内存带宽限制。
- **架构演进**：从"内存受限"到"计算受限"再到"平衡状态"的三级优化：

| 架构方案 | 关键改进 | 性能瓶颈 |
| :------- | :------- | :------- |
| **2D-Memory** | 传统DDR协议 | 内存访问耗时占比极高（Memory Bound） |
| **3D-PNM** | 3D堆叠+近存计算 | 计算能力不足（Compute Bound） |
| **PNM+SD+CIM** | 投机解码+存内计算 | 内存-计算平衡（Balanced） |

#### **二、投机解码的并行化优化**

![推测解码机制对比图]
- **传统自回归解码**：串行生成token（t0→t1→t2→...），每步需重新加载模型参数，效率低下。
- **3D-TokSIM投机策略**：
  1. **高效草稿生成**：Drafter模块一次性生成k个候选token（t1*~tk*）
  2. **并行验证**：LLM模型对k+1个token（含t0）进行并行验证
  3. **效率提升**：将k步解码压缩为1步，代价是单步计算量增至k+1倍

#### **三、Token驻留存内计算数据流(TS-CIM)**
- **传统权重驻留(WS)局限**：LLM权重过大无法存入SRAM，导致频繁读写能耗激增。
- **TS-CIM创新**：
  - **数据流向反转**：将用户输入的Token嵌入（t0,t1...tk）锁定在CIM阵列中，DRAM流式传输权重进行计算
  - **能效优势**：利用3D DRAM低功耗传输特性，避免SRAM频繁访问损耗
  
  | 投机步长(k) | 2 | 4 | 6 | 8 | 10 |
  | :---------- | :--- | :--- | :--- | :--- | :--- |
  | **TS相对WS能效提升** | 1.18× | 1.16× | 1.14× | 1.13× | 1.12× |

### **🔬 系统级优化与限制**
- **辅助优化技术**：
  - Output Buffer消除优化
  - Residual Buffer数据重用
  - DRAM带宽与CIM算力动态平衡
- **当前局限**：
  - 基于Post-Layout Simulation的理论验证，尚未物理流片
  - 缺乏端到端大模型部署测试数据

### **📝 补充细节与未来方向**
- **神经形态应用扩展**：架构设计可支持CNN/储备池/SNN/光谱仪等多种神经形态任务
- **潜在突破点**：结合更先进的3D集成工艺（如1μm以下键合间距）可进一步提升带宽密度

Tags: AI链接笔记, LLM推理加速, 3D堆叠内存, 存内计算(CIM)
Source: wechat

---

## Related Notes

[[iNEST-MOC]]
[[FPGA原型]]
[[SDI化合物键_四型架构]]
[[paper2_liquid_computing_chemistry]]
