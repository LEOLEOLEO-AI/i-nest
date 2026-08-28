---
title: 灵感·SDI_Hybrid_Torus_Architecture_VC_Circuit_Packet_Sw
source: "[[SDI_Hybrid_Torus_Architecture_VC_Circuit_Packet_Switching]]"
date: 2026-08-28 10:19
type: inspiration-card
method: llm
---

# 固定物理Torus上，将VC分为电路交换颜色路径和分组交换通道，由SDI控制平面按RWA做颜色分配，可实现确定性长流与弹性短流混合，兼具低延迟和利用率。

**假设关联**: H5：SDI软件定义互连可实现拓扑重构。文章用CS-VC颜色路径与PS-VC混合，在固定物理拓扑上动态重构逻辑通信路径，为类突触可塑性提供硬件机制。

> **创新点**: 将SNN同步脉冲映射为颜色CS-VC组播树，突发spike走PS-VC自适应通道；在Torus上仿真混合模式相对纯分组交换的延迟、能耗与死锁表现。

**下一步**: [ ] 搭建Torus片上网络仿真器，对比CS-VC/PS-VC/混合模式在spike流量下的延迟和能耗。

**标签**: [[SDI]] · [[Torus]] · [[混合交换]] · [[虚通道]] · [[颜色路由]]

---
*来源: [[SDI_Hybrid_Torus_Architecture_VC_Circuit_Packet_Switching]] | LLM 深度分析*