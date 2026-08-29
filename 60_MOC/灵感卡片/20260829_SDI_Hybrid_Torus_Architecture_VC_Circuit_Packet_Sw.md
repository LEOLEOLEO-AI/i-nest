---
title: 灵感·SDI_Hybrid_Torus_Architecture_VC_Circuit_Packet_Sw
source: "[[SDI_Hybrid_Torus_Architecture_VC_Circuit_Packet_Switching]]"
date: 2026-08-29 18:04
type: inspiration-card
method: llm
---

# 固定高阶Torus物理拓扑上，SDI控制平面将电路交换颜色路径用于确定性长流、分组交换虚通道用于突发流量，实现物理拓扑固定+逻辑拓扑可编程，兼顾低延迟确定性与灵活性。

**假设关联**: H5（SDI软件定义互连可实现类突触可塑性拓扑重构）。文章核心是SDI控制平面动态重配置逻辑拓扑与路径，正是类突触可塑性的硬件基础。

> **创新点**: 设计FPGA验证平台：2D Torus上实现4条CS-VC颜色路径+2条PS-VC，SDI控制器在线调整路径映射模拟突触重构；测量重配置延迟和确定性流抖动，验证H5。

**下一步**: [ ] 在RTL级实现8节点2D Torus的CS/PS混合交换机，并验证SDI重配置状态机与颜色分配算法。

**标签**: [[SDI]] · [[高阶Torus]] · [[电路交换]] · [[虚通道]] · [[可重构互连]]

---
*来源: [[SDI_Hybrid_Torus_Architecture_VC_Circuit_Packet_Switching]] | LLM 深度分析*