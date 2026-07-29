---
title: "MoX: Efficient MoE Routing on Direct-Connect Topologies"
date: 2026-07-24
source: arXiv
track: TCC
authors: 
year: 2026
url: http://arxiv.org/abs/2607.20220v1
tags: [inbox, tcc, arxiv]
citations: 0
relevance: 3
status: inbox
---

# MoX: Efficient MoE Routing on Direct-Connect Topologies

**** (2026) | *N/A*
**Citations**: 0 | **References**: 0
**闁剧偓甯?*: [http://arxiv.org/abs/2607.20220v1](http://arxiv.org/abs/2607.20220v1)

## Abstract

Optically switched networks suit the regular communication of dense ML models, but MoE introduces sparse, runtime-dependent traffic. We show that efficient offline-optimized routing enables efficient MoE training and inference on direct-connect topologies without the need for MoE traffic matrix or dynamic topology reconfiguration. MoX constructs token-aware multicast trees to reduce bandwidth tax, then uses static, precomputed link weights to balance traffic by solving a restricted multicast tre

## TCC Insights

论文研究直接连接拓扑（direct-connect topologies）上的MoE路由优化，涉及光交换网络、离线预计算链路权重、令牌感知多播树等，与芯片互连（NoC/chiplet/interconnect）的拓扑设计和路由算法高度相关。

## iNEST Insights

论文涉及MoE（混合专家模型）的稀疏路由，但核心是网络层的路由效率，未讨论神经网络的临界性、涌现行为或神经形态计算，因此与iNEST项目关联较弱。

## Actionable

可关注其令牌感知多播树方法是否适用于chiplet间互连的带宽优化；静态预计算权重策略或可借鉴以降低动态重配置开销；建议评估该方法在典型NoC拓扑（如Mesh/Torus）上的适配性。

---
*2026-07-24 缁夋垹鐖虹粻锛勫殠v3.1閼奉亜濮╅幓鎰仹 | 閻╃鍙ф惔? 3/3*