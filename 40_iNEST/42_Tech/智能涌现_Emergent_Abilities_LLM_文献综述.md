---
direction: iNEST
title: "智能涌现 Emergent Abilities LLM 文献综述"
created: 2026-07-07
modified: 2026-07-07
provenance: external
---
﻿---
title: "智能涌现：大语言模型涌现能力文献综述"
date: 2026-07-07
source: arXiv
track: iNEST
tags: [涌现, emergence, scaling_law, phase_transition, LLM, 深度阅读]
status: 深度阅读
---

# 智能涌现 (Emergent Abilities)：大语言模型涌现能力文献综述

## 核心概念

**涌现 (Emergence)** 指大语言模型在规模跨越某个临界阈值后，突然表现出小模型中不存在的能力——这些能力并非被显式训练，而是随规模自然出现。

---

## 必读论文 (5 篇核心)

### 1. Emergent Abilities of Large Language Models (Wei et al., 2022)
- **链接**: https://arxiv.org/abs/2206.07682
- **地位**: 奠基性论文，首次系统定义"涌现能力"
- **核心发现**: 多种能力（算术、多语言、思维链等）在模型达到特定规模前几乎为零，之后陡然上升
- **对 iNEST 启示**: 涌现的阈值条件是否适用于网络架构？

### 2. Why are LLMs'' abilities emergent? (2025)
- **链接**: https://arxiv.org/abs/2508.04401
- **核心**: 从理论分析和经验观察两个维度解释涌现的根源
- **方法**: DNN 涌现性质的认识论分析
- **对 iNEST 启示**: 涌现的"认识论挑战"——如何从工程角度预测涌现？

### 3. Evidence of Phase Transitions in Small Transformer-Based Language Models (2025)
- **链接**: https://arxiv.org/abs/2511.12768
- **核心**: 在小规模 Transformer 中直接观测到相变现象
- **关键问题**: 模型/数据缩放下的相变阈值、log-scale 下的涌现
- **对 iNEST 启示**: 小规模相变是否意味着涌现是普遍现象？

### 4. A Simple Explanation for the Phase Transition in Large Language Models with List Decoding (2023)
- **链接**: https://arxiv.org/abs/2303.13112
- **核心**: 用序列到序列随机函数 + List Decoding 给出相变的简单解释
- **方法**: 理论建模——将 LLM 建模为随机函数
- **对 iNEST 启示**: 理论模型是否适用于网络系统的涌现？

### 5. Berezinskii--Kosterlitz--Thouless transition in a context-sensitive random language model (2024)
- **链接**: https://arxiv.org/abs/2412.01212
- **核心**: 将 BKT 相变理论引入语言模型，发现与物理系统相似的标度律
- **创新**: 跨学科——统计物理 ↔ 语言模型
- **对 iNEST 启示**: 网络系统的相变是否也遵循 BKT 类型？

---

## 延伸阅读

### Scaling Laws
- **Neural Scaling Universality** (2026): 标度律指数由通用机制决定 → https://arxiv.org/abs/2606.25008
- **Scaling limit of the Random Language Model** (2026): 随机语言模型的标度极限 → https://arxiv.org/abs/2606.28105
- **Phase structure of the Random Language Model** (2026): 随机语言模型的相结构 → https://arxiv.org/abs/2606.28103

### Emergent Misalignment
- **Persona-Model Collapse in Emergent Misalignment** (2025): 涌现失调中的人格模型坍缩 → https://arxiv.org/abs/2605.12850

### Collective Intelligence
- **Superminds Test** (2025): 大规模 Agent 社会中集体智能是否涌现？ → https://arxiv.org/abs/2604.22452

---

## 与 TCC + iNEST 的关联

| 论文方向 | TCC 潜在关联 | iNEST 潜在关联 |
|---------|-------------|---------------|
| 涌现能力 | 网络拓扑规模涌现 | 智能网络自组织 |
| 相变理论 | 网络拥堵相变 | 架构相变设计 |
| Scaling Laws | NoC 规模扩展律 | 分布式智能标度 |
| 集体智能 | 网络节点协同涌现 | 多 Agent 网络智能 |

---

## 待深入问题

1. 涌现的阈值条件是否普遍？——网络规模 vs 模型规模
2. 相变是否可以「设计」而非等待涌现？
3. iNEST 的自组织网络架构是否可以主动诱导有益的涌现行为？
4. 涌现是否可逆？——如果模型压缩，能力是否连续衰减？


<!-- orphan-cleanup: linked to MOC -->
## 来源回链

- [[iNEST_Master_Index]]
