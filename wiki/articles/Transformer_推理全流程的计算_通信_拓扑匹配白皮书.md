---
title: "Transformer 推理全流程的计算—通信—拓扑匹配白皮书"
type: article-summary
domain: TCC
created: 2026-08-05
auto: true
---
# Transformer 推理全流程的计算—通信—拓扑匹配白皮书

**Domain**: TCC
**Source**: 00_Inbox\04 Creating\Transformer 推理全流程的计算—通信—拓扑匹配白皮书.md
**Compiled**: 2026-08-05

## Summary
**副标题：从算子谱系到相位可重构互连——为什么 Prefill 要 bisection、Decode 要小直径、MoE 要高谱隙、KV 迁移要隔离带宽** **打印排版规范**：标题使用微软雅黑，正文使用宋体，强调使用楷体，英文与数字使用 Times New Roman，公式统一采用标准数学排版体，全文标点采用全角，段落首行缩进两字符，页面 A4 纵向、页边距 2.5 cm。 本白皮书完整拆解 Transformer 推理的全部算子谱系（共十九类运算），并逐一给出其计算强度、通信原语、消息尺度与主导瓶颈项，进而论证一个核心命题：**推理系统的互连需求不是单一指标，而是由矩阵形状的相变所驱动的四类正交图论诉求**。 具体而言，Prefill 阶段的厚矩阵通用矩阵乘（GEMM）产生大块归约流量，受制于二分带宽（bisection bandwidth）；Decode 阶段的瘦向量矩阵乘（GEMV）产生高频微型归约流量，受制于网络直径（diameter）；混合专家（MoE）的稀疏路由矩阵产生随机置换全对全流量，受制于图的谱隙（spectral gap）；键值缓存（KV Cache）迁移是零算

## Keywords
互连, 拓扑

---
*Auto-compiled by wiki_compiler.py*


## Related Concepts

[[Memory_Wall]]
[[MoE_Routing]]
[[Network_Topology_Design]]
[[TCC]]
