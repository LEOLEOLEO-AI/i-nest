---
title: "Physically-Aware Preemptive Virtual Channels for Deadlock-Free AXI Networks-on-Chip"
date: 2026-07-05
source: arXiv
track: TCC
authors: 
year: 2026
url: http://arxiv.org/abs/2607.01430v1
tags: [深度分析, tcc, 来自arxiv]
citations: 0
relevance: 3
status: 深度阅读
---

# Physically-Aware Preemptive Virtual Channels for Deadlock-Free AXI Networks-on-Chip

**** (2026) | *未知期刊*
**引用数**: 0 | **参考文献数**: 0
**链接**: [http://arxiv.org/abs/2607.01430v1](http://arxiv.org/abs/2607.01430v1)

## 摘要

As many-core Systems-on-Chip (SoCs) continue to scale, Networks-on-Chip (NoCs) must sustain increasingly high memory bandwidth while preserving deadlock freedom. In AXI4 systems, protocol-level dependencies between read and write traffic can create circular waits at the network endpoints, even when the routing algorithm itself is deadlock-free. Decoupling these traffic classes avoids such dependencies, but exposes a key implementation trade-off: multiplane NoCs duplicate wide physical links and

## 核心创新
本论文提出了一种物理感知的抢占虚拟通道技术，用于AXI网络-on-chip（NoC），以实现死锁自由的数据传输。这种技术通过解耦读写流量，避免了协议级别的依赖关系，从而防止了网络端点的循环等待。同时，作者们还考虑了多平面NoC的实现-trade-off，包括物理链路的复制和资源的利用率。

## 与TCC的关系
本论文与TCC有直接关联，特别是在网络拓扑和NoC设计方面。作者们提出的物理感知抢占虚拟通道技术，可以应用于TCC的网络拓扑设计中，以提高网络的吞吐量和降低延迟。
- **拓扑启示**: 本论文涉及的拓扑概念包括网络端点的依赖关系和循环等待的防止，这些概念在TCC的网络拓扑设计中非常重要。
- **工程启示**: 本论文提供了一个工程启示，即在NoC设计中，需要考虑物理链路的复制和资源的利用率，以实现高效的数据传输。

## 与iNEST的关系
本论文与iNEST无直接关联，因为它主要关注网络拓扑和NoC设计，而不是涌现、复杂性或神经动力学等iNEST的研究领域。

## 研究启发
本论文的研究启发包括：
1. 将物理感知抢占虚拟通道技术应用于TCC的网络拓扑设计中，以提高网络的吞吐量和降低延迟。
2. 研究多平面NoC的实现-trade-off，包括物理链路的复制和资源的利用率，以优化NoC的设计。
3. 探索将NoC设计中的依赖关系和循环等待的防止应用于其他领域，例如分布式系统或并行计算。

## 可执行行动
- [ ] 研究物理感知抢占虚拟通道技术在TCC网络拓扑设计中的应用。
- [ ] 开发多平面NoC的仿真平台，以评估物理链路的复制和资源的利用率。
- [ ] 探索将NoC设计中的依赖关系和循环等待的防止应用于其他领域的可能性。

---
*2026-07-05 深度分析 | 相关度: 3/3 | TCC论文*