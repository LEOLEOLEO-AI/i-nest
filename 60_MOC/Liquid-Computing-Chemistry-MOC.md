---
title: 液态计算化学 — 全景导航 (Map of Content)
tags:
  - moc
  - liquid-computing
  - chemistry
  - inest
  - paradigm
  - emergence
---

> Liquid Computing Chemistry (LCC) = 将化学概念（原子、键、价、活化能、自由能、相变）映射到计算基元的新范式

---

## 核心概念

- [[SDI化合物键_四型架构]] — 碳sp3杂化类比，4键型×N条动态通道
- [[STDP-FEP梯度下降统一映射]] — STDP是FEP在忆阻器上的自然实现
- [[三原理协同_FEP_STDP_最小作用量]] — ms/s/min-h三级时间尺度协同
- [[键状态机_六规则完整定义]] — E-S↔E-L固化/衰减/I-S断开/新建
- [[自组织临界态SOC]] — σ≥4.0, α∈[1.5,2.5], F全局极小
- [[BCM滑动阈值]] — 催化加速收敛，惊讶度耦合

## 工程实现

- [[SDI节点]] — 软件定义互连，4通道+2路SYN
- [[忆阻器]] — HfO2基质，天然STDP物理
- [[异步脉冲AER协议]] — 无全局时钟，事件驱动
- [[FPGA原型]] — Gen1单FPGA，Gen5晶圆级集成
- [[五世代路线图]] — 2027(C.elegans) → 2035(人脑)

## 论文与专利

- [[paper1_iNEST_core_architecture]] — iNEST核心架构论文
- [[paper2_liquid_computing_chemistry]] — 液态计算化学 Perspective
- [[专利组合总览]] — 8项专利，P1-P3最高优先级

## 仿真验证

- [[v28多尺度仿真结果]] — N=279~1953, σ≥4.0, bonds∝N^1.02
- [[V29仿真推进计划]] — 趋光/趋化/模式补全/时序预测
- [[标度律验证]] — 时间∝N^1.22, 度分布k(N)∝N^0.14

## 产业影响

- [[绿色AI]] — 目标20W, 150,000x能效提升
- [[安全可解释AI]] — 每键有物理含义
- [[AI民主化]] — 无需超算，无需海量标注数据
- [[智涌脑]] — 智能作为物质的自组织相变

---

## Related Notes
- [[iNEST-MOC]]
- [[TCC-MOC]]
- [[Concepts-Theory-MOC]]
- [[Papers-MOC]]
