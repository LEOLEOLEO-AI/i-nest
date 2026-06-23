---
authors: Haeyeon Kim, Junghyun Lee, Seonguk Choi, Federico Berto, Taein Shin
category: Chip-Hardware
date: 2026-06-23
entities:
- chiplet placement
- signal integrity
processed: '2026-06-24T00:41:04.865325'
source: S2
source_file: 2026-06-23_S2_Advanced Chiplet Placement and Routing Optimization Consider.md
status: inbox
summary: 提出信号完整性感知的分层MDP方法，实现芯粒布局布线优化，眼图孔径平均0.869 UI，优于随机搜索和深度RL 44.8%。
tags:
- from-s2
- reinforcement learning
- auto-crawl
- chiplet
- tcc
- signal integrity
title: Advanced Chiplet Placement and Routing Optimization Considering Signal Integrity
track: TCC
url: https://www.semanticscholar.org/paper/7e67bda8176814b8b44526e8d5e3e0360c06060b
year: 2025
---

# Advanced Chiplet Placement and Routing Optimization Considering Signal Integrity

**Source**: S2 | **Track**: TCC | **Date**: 2026-06-23
**Authors**: Haeyeon Kim, Junghyun Lee, Seonguk Choi, Federico Berto, Taein Shin | **Year**: 2025
**URL**: [https://www.semanticscholar.org/paper/7e67bda8176814b8b44526e8d5e3e0360c06060b](https://www.semanticscholar.org/paper/7e67bda8176814b8b44526e8d5e3e0360c06060b)

## Abstract

This article addresses the critical challenges of chiplet placement and routing optimization in the era of advanced packaging and heterogeneous integration. We present a novel approach that formulates the problem as a signal integrity (SI)-aware hierarchical Markov decision process (MDP), leveraging the place-to-route (P2R) algorithm. Our method uniquely incorporates the universal chiplet interconnect express (UCIe) eye mask specifications to ensure compliance with datarate-dependent signal integrity requirements. Tested on ten benchmark problems, P2R achieved superior results with an average eye-diagram aperture of 0.869 unit interval (UI) in a single iteration, outperforming random search and deep reinforcement learning (RL) by 44.8%. By addressing the combinatorial complexity and hard c

## Relevance to TCC / iNEST

(TBD — process_inbox will auto-classify)

---
*Auto-crawled 2026-06-23 by Research Pipeline v3.0 | Inbox — needs classification*