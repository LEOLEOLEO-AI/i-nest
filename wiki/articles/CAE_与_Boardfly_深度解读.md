# CAE 与 Boardfly 深度解读

**Domain**: TCC
**Source**: 00_Inbox\04 Creating\拓扑简史与谷歌TPU V8.md
**Compiled**: 2026-08-06

## Summary
读 TPU 8i 的技术博客，最值得停下来的不是任何一个数字，而是一个反问句： > **“Why move away from the torus for TPU 8i? It comes down to network diameter.”** > （TPU 8i 为什么要放弃环面？归结为网络直径。） 这句话的分量需要背景才能体会。3D Torus 是 Google 从 TPU v2 一路走到 v7 的招牌，2023 年那篇著名的 TPU v4 论文（arXiv:2304.01433）用 4096 芯片证明了"光重构 3D Torus"的优雅，业界跟着抄了三年。而现在，同一家公司在同一代产品里**把产品线劈成两半**：训练那半继续用 3D Torus 并把规模推到 9600 芯片，推理那半彻底改 这不是技术迭代，这是**公开承认一张拓扑无法同时服务两类负载**。而这恰恰是 TCC 从第一天起就在讲的那句话。区别只在于解法：Google 掏出两颗芯片，TCC 主张一张基座配四张可翻的页。

## Keywords
STDP, TCC, chiplet, 互连, 拓扑, 晶圆, 芯粒

---
*Auto-compiled by wiki_compiler.py*


## Related Concepts

[[Chiplet_Heterogeneous_Integration]]
[[Network_Topology_Design]]
[[STDP_Plasticity]]
[[TCC]]
[[Wafer_Scale_Integration]]
