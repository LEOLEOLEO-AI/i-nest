---
title: "EPnG: Adaptive Expert Prune-and-Grow for Parameter-Efficient MoE Fine-tuning"
date: 2026-07-05
source: arXiv
track: TCC
authors: 
year: 2026
url: http://arxiv.org/abs/2607.01789v1
tags: [深度分析, tcc, 来自arxiv]
citations: 0
relevance: 3
status: 深度阅读
provenance: external
---

# EPnG: Adaptive Expert Prune-and-Grow for Parameter-Efficient MoE Fine-tuning

**** (2026) | *未知期刊*
**引用数**: 0 | **参考文献数**: 0
**链接**: [http://arxiv.org/abs/2607.01789v1](http://arxiv.org/abs/2607.01789v1)

## 摘要

Mixture-of-Experts (MoE) models scale efficiently but remain costly to adapt due to redundant experts and uniform parameter allocation. Existing parameter-efficient fine-tuning (PEFT) methods such as LoRA ignore MoE routing dynamics, leading to suboptimal resource use. We propose EPnG, an adaptive prune-and-grow framework that reallocates LoRA capacity based on expert importance derived from router gate probabilities. EPnG prunes under-utilized experts and expands high-importance experts via ran

## 核心创新
本论文提出了一种自适应的剪枝和增长框架EPnG，用于参数高效的MoE模型微调。EPnG根据专家重要性重新分配LoRA容量，实现了更有效的资源利用。这种方法通过剪枝低利用率的专家和扩展高重要性专家，优化了MoE模型的性能。

## 与TCC的关系
本论文与TCC有关，因为它涉及到MoE模型的网络拓扑和路由动态。具体来说，EPnG框架考虑了专家之间的路由关系和权重分配，优化了模型的参数利用率。
- **拓扑启示**: 本论文中的MoE模型可以被视为一个动态的网络拓扑，其中专家之间的连接和权重会根据输入数据而变化。EPnG框架通过剪枝和增长专家，实现了网络拓扑的自适应调整。
- **工程启示**: 本论文表明，通过优化MoE模型的路由动态和参数分配，可以实现更高效的资源利用和模型性能。

## 与iNEST的关系
本论文与iNEST有关，因为它涉及到MoE模型的复杂性和动态行为。具体来说，EPnG框架通过分析专家重要性和路由概率，实现了模型参数的自适应调整。
- **涌现启示**: 本论文中的EPnG框架可以被视为一个涌现系统，其中专家之间的交互和竞争导致了模型参数的自适应调整。
- **动力学启示**: 本论文表明，MoE模型的动态行为可以通过分析专家重要性和路由概率来理解和优化。

## 研究启发
本论文为TCC和iNEST研究带来了以下启发：
1. 如何设计更高效的MoE模型路由算法，以优化模型的参数利用率和性能。
2. 如何将EPnG框架应用于其他类型的神经网络模型，以实现更高效的参数利用率和模型性能。
3. 如何分析和理解MoE模型的复杂性和动态行为，以设计更好的模型架构和训练算法。

## 可执行行动
- [ ] 研究和实现更高效的MoE模型路由算法，以优化模型的参数利用率和性能。
- [ ] 将EPnG框架应用于其他类型的神经网络模型，以实现更高效的参数利用率和模型性能。
- [ ] 分析和理解MoE模型的复杂性和动态行为，以设计更好的模型架构和训练算法。

---
*2026-07-05 深度分析 | 相关度: 3/3 | TCC论文*

<!-- orphan-cleanup: linked to MOC -->
## 来源回链

- [[iNEST_Master_Index]]
