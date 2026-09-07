---
title: 灵感·TCC_project_proposal_defense_notes
source: "[[TCC_project_proposal_defense_notes]]"
date: 2026-09-08 06:53
type: inspiration-card
method: llm
---

# 系统瓶颈是拓扑刚性：任务通信模式随训练/推理变化，物理拓扑却焊死。TCC将互连拓扑本身作为可编程对象，以Route/Transform原语+Topology Page+Epoch Commit实现'网络即计算'，支持μs级拓扑液态切换。

**假设关联**: H5最相关：SDI软件定义互连可实现类突触可塑性拓扑重构。文中'拓扑页+Epoch原子提交'恰是突触可塑性所需的在线、快速、可重构机制。

> **创新点**: 将SNN的突触权重映射为Topology Page，学习规则转化为Epoch原子提交条件；用FPGA验证液态拓扑切换，使spike路由路径随STDP实时重构，实现iNEST的突触可塑性硬件化。

**下一步**: [ ] 设计'拓扑页即突触权重页'映射方案，并在VU13P上搭建FPGA验证回路。

**标签**: [[拓扑即计算]] · [[软件定义互连]] · [[训推一体]] · [[突触可塑性]] · [[FPGA]]

---
*来源: [[TCC_project_proposal_defense_notes]] | LLM 深度分析*