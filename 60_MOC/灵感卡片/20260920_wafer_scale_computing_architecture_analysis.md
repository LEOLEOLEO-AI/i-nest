---
title: 灵感·wafer_scale_computing_architecture_analysis
source: "[[wafer_scale_computing_architecture_analysis]]"
date: 2026-09-20 03:03
type: inspiration-card
method: llm
---

# 晶圆级计算的本质是用消除物理边界换取τ累积归零；但Dojo层级数据显示跨封装边界带宽从2TB/s骤降至50GB/s，扩展性在机柜级断裂。

**假设关联**: H4——Dojo的25芯粒→Tile→Tray→Cabinet→ExaPOD阶梯提供晶圆级扩展实测标尺，跨边界带宽断崖直接证伪'线性扩展'。

> **创新点**: 设计'边界带宽密度扫描'实验：在仿真NoC上将跨die带宽由2TB/s逐级降至50GB/s，跑MoE/稀疏注意力，测出超加性增益(1+1>2)消失的临界带宽比B*，形成H1×H4联合判据。

**下一步**: [ ] 收集Dojo/Cerebras各层级带宽-延迟-算力数据，拟合τ累积曲线并标定B*临界点。

**标签**: [[晶圆级计算]] · [[Chiplet]] · [[拓扑中心计算]] · [[τ定律]] · [[超加性增益]]

---
*来源: [[wafer_scale_computing_architecture_analysis]] | LLM 深度分析*