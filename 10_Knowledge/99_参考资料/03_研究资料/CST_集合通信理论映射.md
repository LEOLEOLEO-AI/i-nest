# CST理论 × 集合通信硬件化：理论基础

## 核心命题

> 集合通信（Allreduce/Alltoall）的效率瓶颈，本质是**网络拓扑复杂度与通信任务复杂度的失配**。
> CST理论提供了量化这一失配的数学工具：RI = C_ST(network) / E_env(task)

## CST方程到通信优化的映射

```
I ∝ CST = (Sc · Tc) · e^(α·Γst)

通信优化语境下：
  Sc（空间复杂度）= 网络拓扑的连通性 × 层级性 × 模块性
  Tc（时间复杂度）= 通信调度的临界性 × 同步性 × 多时间尺度
  Γst（时空耦合）= 数据流与网络拓扑的匹配度

RI = CST(network) / E_env(Allreduce_task)
   → RI越高，网络对该通信任务的加速能力越强
   → SDI的目标：最大化RI
```

## SDI化学键机制的物理含义

| 化学键类型 | 物理对应 | 集合通信作用 |
|-----------|---------|------------|
| E-S键（短程兴奋） | 芯粒间直接物理链路 | 局部归约（Ring Allreduce每一跳） |
| E-L键（长程兴奋） | 跨模块高速互连 | 跨Ring汇总、Tree根节点广播 |
| I-S键（短程抑制） | 流控/背压机制 | 防止雪崩、维持临界态 |
| I-L键（长程抑制） | Hub节点调度控制 | 全局负载均衡 |

## 小世界网络与集合通信效率的关系

```
σ = (C/Cr) / (L/Lr)   ← 小世界指数

集合通信效率 ∝ σ：
  C高（聚类强）= 局部归约效率高（Ring每跳延迟低）
  L短（路径短）= 全局广播跳数少（Tree深度浅）

目标：σ ≥ 1.8（已在SDI仿真v22-v25中验证）
生物参照：
  C.elegans σ=5.81，果蝇FLY_L σ=8.31，人脑Budapest σ=13.48
  → 生物演化出的最优通信网络天然具备强小世界性
  → SDSoW工程目标：在硅上复现这种拓扑特性
```

## 硬件化Allreduce的CST分析

### Ring-Allreduce（适合小规模）
```
通信步数 = 2(N-1)，N = 芯粒数
CST贡献：Sc靠Ring局部聚类，Tc靠STDP固化最优转发路径
RI指标：对于N≤16的集群，Ring是σ最高的拓扑选择
```

### Tree-Allreduce（适合中规模）
```
通信步数 = 2·log(N)
CST贡献：Sc靠层级性（Hub-IL机制），Tc靠临界分支比B≈1
RI指标：N=16~64时，Tree的RI高于Ring
```

### Mesh-Alltoall（适合大规模MoE）
```
通信步数 = N-1（全交换）
CST贡献：Sc靠模块性（2D/3D Mesh分区），Tc靠γ节律调度
RI指标：N>64时，2D Mesh配合SDI动态重构的RI最优
```


---
**Tags:** [[NaaS]] [[BrainInspired]] CST [[SDSoW]] SDI [[Chiplet]]
