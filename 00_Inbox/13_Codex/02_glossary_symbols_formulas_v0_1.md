---
title: "术语、符号与公式状态"
version: v0.1
status: baseline-draft
created: 2026-08-01
---

# 术语、符号与公式状态

| 术语 | 当前工作定义 | 状态 |
|---|---|---|
| SDSoW | 软件定义的晶圆级或介观可重构物理网络底座 | `[Working definition]` |
| SDI | 软件定义互连的控制与执行机制 | `[Engineering]` |
| CST | 可用时空协同复杂度度量框架 | `[Working definition]` |
| TCC | 拓扑中心计算：拓扑是一级可编程资源 | `[Engineering/research]` |
| CM | 系统与环境之间的复杂度匹配 | `[Hypothesis]` |
| CS | 多个复杂子系统的协同同步 | `[Hypothesis]` |
| EI | 通过操作化任务展示出的涌现智能能力 | `[Operational target]` |
| SDDE | 用于连续演化的随机时滞微分方程模型族 | `[Candidate model family]` |
| iNEST | 网络时空协同复杂度涌现智能的工程路线 | `[Engineering path]` |
| iMESO | 拟议的介观物理智能平台 | `[Planning]` |

## CST工作公式 `[Working definition]`

`C_ST_cap(t) = S_c(t) * T_c(t) * exp(alpha_eff(t) * Gamma_st_u(t))`

| 符号 | 拟议含义 | 测量状态 |
|---|---|---|
| `S_c` | 空间拓扑组织能力 | `[Pending]` 指标定义 |
| `T_c` | 时间演化与记忆能力 | `[Pending]` 指标定义 |
| `alpha_eff` | 有效可区分非平衡状态容量 | `[Pending]` 指标定义 |
| `Gamma_st_u` | 可用结构-动力学-需求协同因子 | `[Pending]` 指标定义 |

在量纲、归一化、估计器、误差界和校准数据冻结前，该公式不得用于性能主张。

## 相对智能指数 `[Working definition]`

`R_I(t) = C_ST_sys(t) / C_ST_env(t)`

`C_ST_env`包括环境状态、任务目标、扰动、时序约束和行动边界。`R_I < 1`、`R_I约等于1`和`R_I > 1`分别表示在指定任务协议下测得的能力不足、能力匹配和能力余量；它们不能独立证明智能已经出现。

## Route-Transform边界 `[Engineering hypothesis]`

对路径`rho = (e_1, ..., e_k)`，定义复合局部操作：

`T_rho = phi_e_k o ... o phi_e_1`

拓扑能够组织数据搬移、置换、聚合和局部操作调度，但其本身**不能**实现任意线性或非线性变换。只有在明确计算模型、局部算子集、物理映射、精度和成本模型后，才可以提出具体等价关系。

