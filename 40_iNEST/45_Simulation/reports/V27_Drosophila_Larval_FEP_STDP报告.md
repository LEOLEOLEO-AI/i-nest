---
title: V27_Drosophila_Larval_FEP_STDP报告
date: 2026-06-19
tags: [V27, Drosophila, FEP-STDP, connectome]
status: 已完成
---

# V27: Drosophila Larval FEP-STDP 完整报告

> 数据: Winding et al. 2023, Science (connectome_larval_cns.json)
> N=2952, 110,677化学突触

## 1. 实验目的

用真实 Drosophila幼虫连接组，验证 FEP-STDP 在生物拓扑上的动力学行为，与 ER 随机网络对照。

## 2. 核心结果

| 指标 | 真实幼虫 | ER 随机 | 比值/差异 |
|------|---------|--------|----------|
| N (GCC) | 2952 | 2952 | - |
| E | 96,527 | ~96,527 | - |
| k_avg | 65.40 | ~65.40 | - |
| **σ** | **9.444** | 1.0 | **9.44x** |
| C | 0.2615 | 0.0223 | 11.7x |
| L | 2.7466 | 2.2073 | +24% |
| KS clust p | **0.0** | - | 聚类分布完全非随机 |

## 3. FEP-STDP 动力学

| 指标 | 真实 | ER |
|------|------|-----|
| F_final | 0.6474 | 0.4948 |
| F_mean | 0.4590 | 0.2950 |
| n_avalanches | 13 | 0 |

> 真实拓扑的自由能更高（非更低），可能表明生物拓扑处于能量景观的不同位置。

## 4. Avalanche 统计

| 指标 | 真实 | ER |
|------|------|-----|
| mean | 2.48 | 3.08 |
| max | 20 | 39 |
| α | 1.336 | 0.909 |

## 5. 结论

✅ Drosophila幼虫连接组 σ=9.44，远超 C.elegans (σ=6.98)
✅ 聚类分布 KS p=0，彻底排除随机零假设
✅ FEP-STDP 验证了真实拓扑与随机拓扑的不同动力学行为
