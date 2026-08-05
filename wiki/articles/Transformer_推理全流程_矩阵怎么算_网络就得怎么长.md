---
title: "Transformer 推理全流程：矩阵怎么算，网络就得怎么长"
type: article-summary
domain: TCC
created: 2026-08-05
auto: true
---
# Transformer 推理全流程：矩阵怎么算，网络就得怎么长

**Domain**: TCC
**Source**: 00_Inbox\04 Creating\Transformer 推理全流程：矩阵怎么算，网络就得怎么长.md
**Compiled**: 2026-08-05

## Summary
**Transformer 推理的四个相位，本质是同一组矩阵乘法在"形状"上的四次剧变；形状一变，通信原语跟着变，拓扑的最优解也跟着变。** 所以那四句话不是四条调参经验，而是四个矩阵形状对物理网络提出的**原生结构诉求**： 矩阵形状  ──→  并行切分  ──→  通信原语  ──→  拓扑指标 ───────────────────────────────────────────────────── 厚矩阵 GEMM      张量/上下文并行   大块 all-reduce    二分带宽 bisection

## Keywords
拓扑

---
*Auto-compiled by wiki_compiler.py*


## Related Concepts

[[Memory_Wall]]
[[Network_Topology_Design]]
[[TCC]]
