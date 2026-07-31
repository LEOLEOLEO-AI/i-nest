---
title: "The Drosophila Connectome as a Computational Reservoir for Time-Series Prediction"
date: 2026-07-01
source: S2
track: iNEST
authors: Leone Costi, Alexander Hadjiivanov, Dominik Dold, Zachary F. Hale, Dario Izzo
year: 2025
url: https://www.semanticscholar.org/paper/5de0829640010f9565293d101554dc3a3e5acefb
tags: [洞察, inest, 来自s2]
citations: 6
relevance: 3
status: 洞察
provenance: external
---

# The Drosophila Connectome as a Computational Reservoir for Time-Series Prediction

**Leone Costi, Alexander Hadjiivanov, Dominik Dold, Zachary F. Hale, Dario Izzo** (2025) | *Biomimetics*
**引用数**: 6 | **参考文献数**: 64
**领域**: Medicine
**DOI**: 10.3390/biomimetics10050341
**链接**: [https://www.semanticscholar.org/paper/5de0829640010f9565293d101554dc3a3e5acefb](https://www.semanticscholar.org/paper/5de0829640010f9565293d101554dc3a3e5acefb)

## 一句话总结

This work explores the possibility of using the topology and weight distribution of the connectome of a Drosophila, or fruit fly, as a reservoir for multivariate chaotic time-series prediction and shows that the connectome-based architecture is significantly more resilient to overfitting than the standard implementation.

## 摘要

In this work, we explore the possibility of using the topology and weight distribution of the connectome of a Drosophila, or fruit fly, as a reservoir for multivariate chaotic time-series prediction. Based on the information taken from the recently released full connectome, we create the connectivity matrix of an Echo State Network. Then, we use only the most connected neurons and implement two possible selection criteria, either preserving or breaking the relative proportion of different neuron classes which are also included in the documented connectome, to obtain a computationally convenient reservoir. We then investigate the performance of such architectures and compare them to state-of-the-art reservoirs. The results show that the connectome-based architecture is significantly more resilient to overfitting compared to the standard implementation, particularly in cases already prone to overfitting. To further isolate the role of topology and synaptic weights, hybrid reservoirs with the connectome topology but random synaptic weights and the connectome weights but random topologies are included in the study, demonstrating that both factors play a role in the increased overfittin

## TCC 启示

**关键词匹配**: topology, resilience

**理论贡献**: 复杂网络拓扑性质对TCC的元拓扑设计有直接指导意义。若揭示新的"拓扑-功能"映射关系，应纳入TCC拓扑设计空间。

## iNEST 启示

**关键词匹配**: echo state, connectome

**计算范式**: 储备池计算天然处于"临界边缘"，其不需要训练内部权重的特性，与iNEST"拓扑即计算"高度一致。

**基准系统**: C. elegans connectome是iNEST验证小世界拓扑→计算涌现的最小完整模型系统。新连接组数据可直接更新仿真基准。

## 可执行行动

📄 较新/冷门论文（6引用），关注其创新点，选择性阅读。
🔬 包含具体方法/框架，可在CST仿真中复现验证。
📦 含公开数据/代码，可直接下载集成到工具链。

---
*2026-07-01 科研管线v3.1自动提炼 | 相关度: 3/3*

---
## 相关链接
- [[2026-07-01_S2_Hierarchical communities in the larval Drosophila connectome]]
- [[2026-06-25_S2_The growing topology of the C. elegans connectome]]
- [[2026-07-01_S2_Causal Emergence of Consciousness through Learned Multiscale]]
- [[2026-06-25_S2_Machine Learning-Based Prediction Framework for Complex Neur]]
- [[2026-07-01_S2_Coalescent embedding in the hyperbolic space unsupervisedly ]]
