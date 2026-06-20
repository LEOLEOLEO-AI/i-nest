---
title: "v10 FEP自由能最小化仿真分析：坍缩诊断与v11改进方向"
date: 2026-06-03
tags: [iNEST, FEP, SDI, v10, 仿真分析, 坍缩诊断, v11]
topics: [Concepts-Theory, AI-ML]
---

## v10 核心发现汇总

| 指标 | v9 (tau only) | v10 (FEP+tau+JEPA) | 变化 | 目标 |
|------|---------------|---------------------|------|------|
| E-L Ratio | 8.35% | **94.4%** | ↑86pp | 15-28% |
| Free Energy F | 持续上升 | **0.36→0.71 发散** | 恶化 | 单调递减 |
| Avg tau | 2.47 | 2.45 | 持平 | 稳定 |
| Entropy | N/A | **0.000 (完全坍缩)** | — | >0.3 |
| Convergence | N/A | 95.0% | — | 高但须健康 |
| Glia events | ? | 59 | — | 适度 |
| Scaling events | 9718 | 199 | ↓97% | 适度 |

## 坍缩根因诊断

### 1. 局部FEP贪婪优化的内在矛盾

FEP梯度下降在**局部节点级**执行最小化：

w_{ij} \leftarrow w_{ij} - \eta \cdot \frac{\partial F_i}{\partial w_{ij}}

问题：当每个节点独立最小化其局部自由能时，**全局自由能反而发散**。类似 n 体系统只做局部松弛→过度耦合→能量陷阱。

**证据**：F_local 单节点下降（convergence 95%）但 F_global 从 0.36 升至 0.71。

### 2. JEPA正则β=0.05严重不足

F_i = D_{KL}[q||p] + \lambda \cdot \text{complexity} - \beta \cdot H(q)

β=0.05 意味着熵惩罚仅占总自由能的 5%，在 FEP 强力梯度驱动下几乎无抑制效果。

**证据**：entropy 从初始值迅速坍缩至 0.000，所有节点收敛到同质状态。

### 3. E-L比爆炸的连接固化正反馈

FEP最小化→预测误差下降→更低的F→更强的梯度→更多的固化。导致 E-L 比从 8.35% 暴增至 94.4%。这是一个正反馈循环：

F_i \downarrow \Rightarrow \text{固化加速} \Rightarrow \text{连接增多} \Rightarrow \text{复杂度} F_{\text{comp}} \uparrow \Rightarrow \text{全局F} \uparrow

### 4. 缺少全局能量约束

v10 只有节点级 F_local，没有系统级的能量预算。生物大脑有全局代谢约束（脑重仅占体重2%却消耗20%能量），需要引入系统级约束。

## v11 改进方案

### 改进1：强JEPA熵正则（β=0.5→2.0 自适应）

\beta_{\text{eff}}(t) = \beta_0 \cdot \left(1 + \gamma \cdot \frac{H_{\text{target}} - H(t)}{H_{\text{target}}}\right)

当熵低于目标时自动增强正则强度。

### 改进2：全局自由能约束

引入系统级 F_global 目标函数：

\mathcal{L}_{\text{global}} = \sum_i F_i + \lambda_{\text{global}} \cdot |F_{\text{global}} - F_{\text{target}}|

### 改进3：FEP梯度裁剪 + 自适应学习率

\nabla F_i^{\text{clipped}} = \text{clip}(\nabla F_i, -c, c)
\eta_{\text{eff}} = \eta_0 / (1 + \delta \cdot |\nabla F_i|)

### 改进4：E-L比目标正则

\mathcal{L}_{\text{EL}} = \lambda_{\text{EL}} \cdot |\text{EL}_{\text{ratio}} - \text{EL}_{\text{target}}|^2

将 E-L 比约束直接加入损失函数。

### 改进5：FEP目标方向修正

从"最小化 F_i"改为"引导 F_i 收敛到吸引子"：

\Delta w_{ij} = -\eta \cdot \text{sign}(F_i - F_i^{\text{basin}}) \cdot |\nabla F_i|

只在 F_i 高于盆地值时才应用梯度下降，避免推动到零。

## v11 预期目标

| 指标 | v10 实际 | v11 目标 |
|------|----------|----------|
| E-L Ratio | 94.4% | 15-28% |
| F_global trend | 发散 ↑ | 单调递减 ↓ |
| Entropy final | 0.000 | >0.3 |
| F_convergence | 95% | 60-80% (健康范围) |
| tau_mean | 2.45 | 3.0-5.0 (更多样化) |

## 理论意义

v10 验证了一个重要假设：**纯局部 FEP 最小化不足以产生健康的自组织**。需要：
1. 全局约束（总能量预算）
2. 多样性保护（熵正则）
3. 目标导向（吸引子收敛而非零收敛）

这恰好印证了 Karl Friston 的预测编码层级模型——自组织需要**层级化的预测-误差**结构，而非扁平的局部优化。
