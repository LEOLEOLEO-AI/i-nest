---
title: "3DLS: A 3D Logic-Stacked Architecture for Disaggregated LLM Serving"
date: 2026-07-05
source: arXiv
track: TCC
authors: 
year: 2026
url: http://arxiv.org/abs/2607.01617v1
tags: [深度分析, tcc, 来自arxiv]
citations: 0
relevance: 3
status: 深度阅读
provenance: external
---

# 3DLS: A 3D Logic-Stacked Architecture for Disaggregated LLM Serving

**** (2026) | *未知期刊*
**引用数**: 0 | **参考文献数**: 0
**链接**: [http://arxiv.org/abs/2607.01617v1](http://arxiv.org/abs/2607.01617v1)

## 摘要

Large language model (LLM) serving increasingly combines prefill-decode (PD) disaggregation with tensor parallelism (TP) to support large models and long contexts. In conventional 2D/2.5D chiplet architectures, layer-wise prefill-to-decode KV-cache transfer decode-side TP collectives share the same lateral die-to-die (D2D) interconnect, creating mixed-traffic contention on the decode critical path. This contention increases communication latency, prolongs token generation intervals, and degrades

## 核心创新
本论文提出了一种三维逻辑堆叠架构（3DLS），用于大规模语言模型（LLM）的分离式服务。这种架构通过将预填充和解码单元分离到不同的芯片层，减少了层间的KV-cache传输和解码侧的张量并行收集通信，从而降低了通信延迟和提高了token生成速度。这种创新性的架构设计解决了传统2D/2.5D芯片架构中的混合交通争用问题。

## 与TCC的关系
本论文与TCC研究轨道有直接关联，特别是在网络拓扑和互连方面。论文提出的3DLS架构，通过将预填充和解码单元分离到不同的芯片层，减少了层间的通信延迟和提高了token生成速度。这与TCC的网络拓扑和互连研究方向相关。
- **拓扑启示**: 本论文的3DLS架构为网络拓扑设计提供了新的思路，特别是在多层次和多维度的网络设计方面。
- **工程启示**: 本论文的研究结果表明，通过优化网络拓扑和互连结构，可以显著提高LLM服务的性能和效率。

## 与iNEST的关系
本论文与iNEST的关系不是非常直接，因为iNEST主要关注涌现、临界性、自组织、神经动力学和复杂性等方面的研究。然而，LLM服务的性能和效率优化可以被视为一个复杂系统的优化问题，这与iNEST的研究方向有一定的关联。
- **涌现启示**: 本论文的研究结果可以被视为一个复杂系统的涌现行为，即通过个体组件的交互和协作，产生了更高层次的性能和效率。
- **动力学启示**: 本论文的研究结果也可以被视为一个动力学系统的行为，即通过优化网络拓扑和互连结构，改变了系统的动力学行为和性能。

## 研究启发
本论文的研究结果为我们提供了以下研究启发：
1. 如何设计和优化网络拓扑和互连结构，以提高LLM服务的性能和效率？
2. 如何将3DLS架构应用于其他类型的机器学习模型和应用场景？
3. 如何将iNEST的研究方向和方法应用于LLM服务的性能和效率优化问题？

## 可执行行动
- [ ] 研究和设计新的网络拓扑和互连结构，以提高LLM服务的性能和效率。
- [ ] 将3DLS架构应用于其他类型的机器学习模型和应用场景，评估其性能和效率。
- [ ] 探索iNEST的研究方向和方法在LLM服务性能和效率优化问题中的应用和价值。

---
*2026-07-05 深度分析 | 相关度: 3/3 | TCC论文*

<!-- orphan-cleanup: linked to MOC -->
## 来源回链

- [[TCC_Master_Index]]
