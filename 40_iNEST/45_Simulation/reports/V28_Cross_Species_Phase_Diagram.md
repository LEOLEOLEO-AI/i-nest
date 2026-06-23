---
title: V28_Cross_Species_Phase_Diagram
date: 2026-06-19
tags: [V28, cross-species, sigma, alpha, emergence]
status: 已完成
---

# V28: 跨物种 Sigma-Alpha 涌现相图

> 数据: 4 物种真实连接组
> 检验 iNEST 预测: sigma * alpha 趋于常数

## 1. 实验目的

测量 4 物种连接组的 sigma 和 avalanche alpha，检验跨物种 σ·α 是否常数。

## 2. 数据来源

| 物种 | N | σ | α | σ·α |
|------|---|---|---|-----|
| C.elegans | 279 | 6.976 | 1.879 | 13.108 |
| Drosophila Larva | 2952 | 9.444 | 1.744 | 16.47 |
| Macaque RM | 82 | 1.35 | 1.34 | 1.809 |
| Drosophila Adult (Hemibrain) | 1000 | 2.648 | 1.015 | 2.686 |

## 3. 跨物种分析

| 指标 | 值 |
|------|-----|
| σ·α 均值 | 8.519 |
| σ·α 标准差 | 6.39 |
| CV | 0.75 |
| 常数假设 | ⚠️ 弱支持 |
| σ ∝ N^β | β=0.398, R²=0.692 |

## 4. 结论

σ·α CV=0.75，物种间差异显著，需更多数据。
σ ∝ N^{0.398} (R²=0.692)。
