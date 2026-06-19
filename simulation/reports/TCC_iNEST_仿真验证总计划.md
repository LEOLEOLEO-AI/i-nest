---
title: TCC_iNEST_仿真验证总计划
date: 2026-06-19
tags: [simulation, connectome, validation, V26-V30]
version: v1.0
---

# TCC x iNEST 真实数据仿真验证总计划

> 核心原则：所有声称必须基于真实连接组数据。虚假参数仅用于概念验证。

---

## 已有真实数据资产

| 物种 | 文件 | 大小 | 来源 | 节点数 |
|------|------|------|------|--------|
| C.elegans | NeuronConnect.xls | 518KB | Varshney 2011 | 279 |
| Drosophila Larva | connectome_larval_cns.json | 2.16MB | Winding 2023 | 2952 |
| Drosophila Adult | flywire_connectome_*.mat | 82+107MB | FlyWire | ~130K |
| Macaque RM | connectome_macaque_rm.json | 80KB | RM Cortex | ~91 |
| Mouse Allen | allen_mouse_connectivity.json | 3.35MB | Allen Institute | 2992 inj |

---

## 五阶段仿真验证计划

### V26: C.elegans 四指标完整分析 [立即可做]
- 数据: NeuronConnect.xls (Varshney 2011)
- 指标: sigma, gamma, STC, alpha
- 对照组: ER随机, WS小世界, BA无标度
- 统计检验: KS test + bootstrap CI
- 代码: simulation/v26_celegans_full_analysis.py

### V27: Drosophila Larval FEP-STDP [1-2周]
- 数据: connectome_larval_cns.json (Winding 2023, N=2952)
- 实验: 真实拓扑上FEP-STDP vs 随机拓扑
- 指标: sigma(t), avalanche分布, E-L比
- 代码: simulation/v27_larval_fep_stdp.py

### V28: 跨物种涌现规律 [2-4周]
- 数据: 5物种 connectome
- 实验: sigma-alpha 跨物种相图，检验iNEST预测: sigma*alpha趋于常数
- 统计: 跨物种回归 + ANCOVA
- 代码: simulation/v28_cross_species.py

### V29: SDI工程参数映射 [并行V28]
- 输入: V26-V28生物参数
- 产出: SDI拓扑生成器 + 工程参数表

### V30: 规模涌现阈值 [4-6周]
- 实验: N=16->1024 芯粒扫描
- 产出: 最小可用规模 + 涌现相图

---

## 缺失数据下载地址

| 数据 | 下载地址 |
|------|----------|
| Hemibrain完整边列表 | https://www.janelia.org/project-team/flyem/hemibrain |
| C.elegans补充突触数据 | https://wormwiring.org/ |
| MICrONS mouse visual cortex | https://www.microns-explorer.org/ |

---

## 执行顺序

V26(本周) -> V27(1-2周) -> V28(2-4周)
              |              |
              +-- V29(并行) --+
                              |
                              +-- V30(4-6周)