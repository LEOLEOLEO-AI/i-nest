---
title: 灵感·3D-TokSIM_LLM_Inference_Acceleration_Architecture
source: "[[3D-TokSIM_LLM_Inference_Acceleration_Architecture]]"
date: 2026-09-01 04:09
type: inspiration-card
method: llm
---

# 3D-TokSIM用混合键合堆叠DRAM和逻辑die，搭配Token驻留存内计算数据流，将投机解码的多token并行验证与内存带宽匹配，解决LLM推理的存储墙瓶颈。

**假设关联**: H6：Chiplet异构集成CMOS+忆阻器crossbar实现存算一体神经形态加速。本文的TS-CIM与3D堆叠正是该假设的实例化验证。

> **创新点**: 借鉴TS-CIM，将Token驻留改为Spike事件驻留：事件驱动SNN中，输入脉冲驻留CIM阵列，权重由3D DRAM流式传输，配合NoC路由降低延迟，验证H7与H6的联合增益。

**下一步**: [ ] 设计仿真对比：TS-CIM数据流在Transformer vs SNN加速器上的吞吐与能效，评估事件驻留优势。

**标签**: [[3D堆叠]] · [[存内计算]] · [[投机解码]] · [[LLM推理]] · [[数据流]]

---
*来源: [[3D-TokSIM_LLM_Inference_Acceleration_Architecture]] | LLM 深度分析*