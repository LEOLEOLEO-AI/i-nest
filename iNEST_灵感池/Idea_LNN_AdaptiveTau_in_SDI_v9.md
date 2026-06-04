# Idea: LNN 自适应 tau 引入 SDI v9 仿真

- **类型**: 技术想法
- **时间**: 2026-06-03
- **标签**: v9, LNN, 自适应tau, SDI仿真, FEP协同
- **关联**: v22_SelfEvolution_Design, sdi_network_v8

---

## 一、动机

v8 基线仿真中，E-L 过度固化（41.8%）的根因之一是**固定 theta 周期**无法随网络状态自适应调整。LNN 的 tau 机制提供了一种优雅的解决方案：让每个 SDI 节点的状态更新速率随局部惊讶度动态调整。

---

## 二、v9 升级设计

### 2.1 自适应 tau 节点

```
tau_i(t) = tau_base / (1 + alpha * surprise_i(t))
surprise_i(t) = |F_i(t) - mean(F_i[t-window:t])| / std(F_i[t-window:t])
```

### 2.2 与 v22 的协同

| v22 机制 | v9 补充 | 协同效果 |
|----------|---------|---------|
| 自适应 theta(t) ∝ L(t) | 自适应 tau_i(t) ∝ 1/surprise_i | theta 控制全局固化频率，tau 控制局部状态更新 |
| FEP 稳态惩罚 | tau 加速惊讶节点响应 | 惊讶节点快速调整，稳态惩罚防止过冲 |

### 2.3 预期效果

- 高惊讶度节点：tau 小，快速更新权重 -> 更快达到预测准确
- 低惊讶度节点：tau 大，慢速更新 -> 自然倾向于 E-L 固化
- **假设**：v9 应比 v8 更快收敛到 SOC 临界态，且 E-L 占比更健康

---

## 三、实验设计

| 条件 | 自适应 tau | v22 theta | 外部数据 | 预期 |
|------|-----------|-----------|---------|------|
| v9-A | Y | N | N | E-L% 降至 30-35%，sigma 升至 3.0-3.5 |
| v9-B | Y | Y | N | E-L% 降至 20-28%，sigma >= 3.5 |
| v9-C | Y | Y | MNIST | alpha 收敛至 1.5-2.0 |

---

## 四、实现计划

```
D:/Obsidian/phase1_workspace/
  sdi_v9_tau_adaptive.py    (新文件: 自适应 tau 节点 + STDP + FEP)
  v9_results/
    tau_vs_surprise.png     (tau-惊讶度关系图)
    convergence_v9.png      (收敛曲线对比)
```

---

> **Ideas 想法 | 2026-06-03**
