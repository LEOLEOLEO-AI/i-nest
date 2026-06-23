# LNN tau 向 SDI 键稳定性的理论映射

- **类型**: 理论笔记
- **时间**: 2026-06-03
- **标签**: tau映射, 键稳定性, LNN, SDI, 活化能, 连续时间
- **关联**: 12_三原理协同_FEP_最小作用量_STDP, 11_SDI节点接口规范

---

## 一、核心映射公式

```
LNN:  tau_effective = g(I, theta_tau)           # 输入->时间常数
SDI:  bond_stability = {E-S: Ea=0.15, E-L: Ea=0.85}  # 键型->活化能

映射:  tau_effective  <->  1 / Ea_bond
       大tau(慢衰减)   ~   高Ea(高稳定)
       小tau(快衰减)   ~   低Ea(低稳定)
```

---

## 二、理论深化：tau 的物理含义

LNN 的 tau 本质是**信息保留时间**：
- tau 大: 状态衰减慢 -> 长期依赖 -> 类比 SDI 的 E-L 键（固化骨架）
- tau 小: 状态衰减快 -> 短期响应 -> 类比 SDI 的 E-S 键（STDP 学习通道）

**关键差异**：
- LNN 的 tau 是标量参数，由反向传播训练
- SDI 的 Ea 是键类型的固有属性，键类型由 FEP 自由能最小化选择

---

## 三、v9 融合方案：自适应 tau 节点

```python
class SDI_Node_v9(SDI_Node_v8):
    def compute_tau(self):
        # 根据邻域惊讶度动态计算时间常数
        surprise = abs(self.F_local - self.F_history.mean())
        tau = 1.0 / (surprise + 1e-6)  # 惊讶度大 -> tau 小 -> 快速响应
        return min(tau, 10.0)

    def update_state(self):
        tau = self.compute_tau()
        dh = -(1.0/tau) * self.h + self.input_drive
        self.h += dh
```

---

## 四、与 FEP 协同

```
惊讶度高 -> tau 小 -> 状态更新快 -> 预测误差下降 -> F 下降
惊讶度低 -> tau 大 -> 状态更新慢 -> 趋于稳定 -> E-S -> E-L 固化
```

本质上是**时间尺度的 FEP 自适应调谐**。

---

> **CST 核心理论 | 2026-06-03**
