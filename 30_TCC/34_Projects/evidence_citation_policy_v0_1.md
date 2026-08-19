---
direction: both
category: 项目
tags: [证据规范, 引用规则, 验证标准, 研究流程]
summary: "制定证据标签与引用规则，禁止无证据声明，强制关键指标验证记录。"
quality: high
processed: 2026-08-12 20:00
---
---
title: "证据与引用规范"
version: v0.1
status: active
created: 2026-08-01
---

# 证据与引用规范

## 证据标签

| 标签 | 含义 | 最小记录 |
|---|---|---|
| `[Measured]` | 已识别硬件上的物理实测 | 搭建、校准、原始/汇总数据和不确定性 |
| `[Simulated]` | 可复现仿真 | 代码版本、环境、配置、种子和输出 |
| `[Literature]` | 已发表或官方来源 | DOI/官方URL和被支持的精确主张 |
| `[Derived]` | 基于已声明假设的数学推导 | 假设、推导、适用范围和反例 |
| `[Pending]` | 已定义但未测量的指标或主张 | 验证任务和验收判据 |
| `[Planning]` | 路线图、拟议架构或目标 | 负责人、依赖条件和决策门 |

## 规则

1. 禁止使用未标注的性能、能耗、面积、成本、时延或吞吐数字。
2. 禁止将提案、仿真结果或模型推导估计写成硬件实测结果。
3. 关于自然常数、普适阈值、普适扩展或智能涌现的主张，必须有独立证据和明确适用范围。
4. 保留负结果、无效映射和重构成本超过收益的情况。
5. 引用只能支持来源中实际存在的命题；生物学类比不能替代工程验证。

## 必填验证记录

每项关键指标都必须包含：编号、负责人、证据标签、基线、方法、数据/代码版本、验收条件、不确定性处理和失败判据。

TCC非线性增益主张使用[E-07至E-10验证协议](http://127.0.0.1:8899/tmp_gh/50_Output/Reports/2026-07-20_TCC_System_Nonlinear_Gain_Verification_Protocol.md)。



## 相关链接
- [[baseline_overview_sdsow_to_inest_v0_1]]
- [[sdsow_to_inest_baseline_navigation]]
- [[Nested_Learning_Illusion_of_Deep_Learning_Architecture_Analysis]]
- [[TCC超非线性增益_研究进展与数学证明路线图_v1.0]]
- [[_Nature_Commun__模拟芯片告别_调参地狱__自适应E_I可塑性让硬件自动_愈合__鲁棒工作记忆实测达成]]
