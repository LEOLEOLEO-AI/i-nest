---
title: V32-V36 后诊断实验计划
date: 2026-06-23
tags: [plan, V32-V36, diagnosis, connectome, TCC, iNEST]
status: 执行中
based_on: 2026-06-23-comprehensive_diagnosis.md
---

# V32-V36: 后诊断阶段仿真验证计划

## 背景

诊断报告（2026-06-23）识别出 5 大系统性问题：
1. 数据真实性（已修复：V26-V31 均使用真实连接组）
2. 公式实现（已修复：NetworkX + scipy 实际计算）
3. 对照实验（已修复：ER 随机对照网络）
4. 统计检验（已修复：KS + permutation + bootstrap）
5. 时间动力学（部分修复：V27 FEP-STDP, V31 热核扩散）

V26-V31 已完成，综合评分从 1.5/5 提升到 4.0/5。剩余差距在：
- 多阈值 Avalanche 分析
- Hemibrain 全脑验证
- 跨物种 Avalanche 普适性
- 工程参数 v2

---

## 实验清单

| 版本 | 优先级 | 名称 | 数据 | 目标 | 时间 |
|------|--------|------|------|------|------|
| V35 | P0 | C.elegans 发表级报告包 | V26+V31 | 图表+统计+论文草稿 | 本周 |
| V32 | P0 | 多阈值 Avalanche 验证 | C.elegans + Drosophila Larva | 雪崩临界性跨阈值检验 | 本周 |
| V33 | P0 | Hemibrain Drosophila Adult 全分析 | Hemibrain v1.2 | 大尺度连接组四指标 | 1-2周 |
| V34 | P1 | 跨物种 Avalanche 普适性 | 4 连接组 | 雪崩指数跨物种对比 | 2-3周 |
| V36 | P1 | SDI 工程映射 v2 | V29 + 硬件参数 | 硬件约束下的参数映射 | 3-4周 |

---

## V35: C.elegans 发表级报告包 [P0] [本周]

### 目标
将 V26 + V31 的结果整合为可投稿的图表和统计报告。

### 输入数据
- V26: C.elegans Four-Index (σ=6.98, γ_t=..., γ_s=..., STC=...)
- V31: SC-FC Coupling (enrichment=2.3x, p=0.008)

### 产出
1. **Figure 1**: 连接组可视化（布线和度分布）
2. **Figure 2**: 四指标柱状图 + ER/WS/BA 对照
3. **Figure 3**: SC-FC 耦合热图（按神经元类别）
4. **Table 1**: 完整统计表（含 p-value 和 CI）
5. **论文草稿**: 3000 字（方法 + 结果 + 讨论）

### 代码
- v35_publish_package.py

---

## V32: 多阈值 Avalanche 验证 [P0] [本周]

### 目标
检验 SOC 雪崩标度律在多个阈值下的稳定性。

### 方法
- 在 C.elegans (N=279) 和 Drosophila Larva (N=2,952) 上
- 阈值从 P50 到 P95（6 个阈值）
- 每个阈值计算：avalanche size distribution → power-law exponent τ
- 对照：同规模 ER 网络

### 成功标准
- τ 在不同阈值下保持稳定（CV < 15%）
- 真实网络 τ 显著不同于 ER（permutation p < 0.01）

### 代码
- v32_avalanche_validation.py

---

## V33: Hemibrain Drosophila Adult 全分析 [P0] [1-2周]

### 目标
在 Hemibrain 大尺度连接组上跑完整四指标分析。

### 数据
- traced-total-connections.csv (Hemibrain v1.2)
- N ≈ 21,739, E ≈ 3.3M

### 实验
1. 加载真实 Hemibrain 边列表
2. 计算四指标 (σ, γ_t, γ_s, α) + 度分布
3. 对照：同规模 ER + Configuration Model
4. 统计：KS test + bootstrap CI

### 挑战
- 21K 节点 × 3.3M 边 = 中等规模计算
- 最短路径需要高效算法（近似或采样）

### 代码
- v33_hemibrain_full.py

---

## V34: 跨物种 Avalanche 普适性 [P1] [2-3周]

### 目标
检验 SOC 雪崩指数是否在四个物种间保持一致。

### 数据
| 物种 | N | E |
|------|---|---|
| C.elegans | 279 | 1,961 |
| Drosophila Larva | 2,952 | ~30K |
| Drosophila Adult | 21,739 | ~3.3M |
| Macaque RM | 82 | ~500 |

### 实验
- 每个物种跑 Avalanche 模拟（3 阈值）
- 提取 power-law τ
- 跨物种回归 τ ~ N^β
- 检验 τ 是否收敛到普适常数

### 代码
- v34_cross_species_avalanche.py

---

## V36: SDI 工程映射 v2 [P1] [3-4周]

### 目标
将 V29 的生物→工程参数映射扩展到硬件约束。

### 输入
- V29 参数映射表
- 文献中的硬件参数（功耗/延迟/面积）
- Loihi 2 / TrueNorth / GPU 对标数据

### 产出
- 硬件约束下的参数映射表
- 功耗/延迟/面积 vs σ 的关系图
- 推荐硬件配置

### 代码
- v36_sdi_hardware_v2.py

---

## 4周执行时间表

| 周 | V35 | V32 | V33 | V34 | V36 | 里程碑 |
|----|-----|-----|-----|-----|-----|--------|
| W1(6/23) | 图表+统计 | Avalanche启动 | 数据准备 | - | - | V35完成 |
| W2(6/30) | 论文草稿 | Avalanche完成 | 全分析启动 | - | - | V32完成 |
| W3(7/7) | - | - | 全分析完成 | 普适性启动 | 参数收集 | V33完成 |
| W4(7/14) | - | - | - | 普适性完成 | 映射v2 | V34+V36完成 |

---

## 成功指标

- [ ] V35: 3 张发表级图表 + 完整统计表
- [ ] V32: τ 跨阈值 CV < 15%，p < 0.01
- [ ] V33: Hemibrain 四指标 + KS p < 0.001
- [ ] V34: 跨物种 τ 一致性检验
- [ ] V36: 硬件参数映射表
- [ ] 综合评分: 4.5/5 (90%) → 可投稿 eLife/PLoS CB

---

*基于 2026-06-23-comprehensive_diagnosis.md 生成*
