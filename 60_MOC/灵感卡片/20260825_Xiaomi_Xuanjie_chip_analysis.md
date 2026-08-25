---
title: 灵感·Xiaomi_Xuanjie_chip_analysis
source: "[[Xiaomi_Xuanjie_chip_analysis]]"
date: 2026-08-25 22:30
type: inspiration-card
method: llm
---

# 小米O100用6nm Wafer-on-Wafer混合键合，以28672根连线实现1.22TB/s带宽，并以拓扑动态切换（环形/广播）适配AI计算模式，直接验证了拓扑互连架构在近存计算中的实际可行性。

**假设关联**: 最相关H5（SDI软件定义互连实现类突触可塑性拓扑重构）：O100的矩阵总线支持拓扑动态切换，正是SDI在晶圆级堆叠中的工程实现雏形。

> **创新点**: 借鉴O100的分区拓扑动态切换，设计事件驱动spike传输的NoC：预填充对应全局广播，解码对应环形路由，用混合键合3D堆叠实现突触权重近存，验证H7延迟降低一个数量级。

**下一步**: [ ] 在FPGA原型上实现O100式双拓扑切换NoC，用MNIST事件流对比单拓扑延迟。

**标签**: [[3D-IC]] · [[Wafer-on-Wafer]] · [[拓扑重构]] · [[近存计算]] · [[NoC]]

---
*来源: [[Xiaomi_Xuanjie_chip_analysis]] | LLM 深度分析*