---
title: "LNN-iNEST 深度机理对比：连续状态演化与工程实现差异"
date: 2026-06-03
tags: [LNN, iNEST, SDI, FEP, 液态神经网络, 微分方程, 状态演化]
topics: [Concepts-Theory, AI-ML]
---

## 核心微分方程对比

### LNN (Liquid Neural Network)
$$\frac{dx}{dt} = -\frac{1}{\tau} x(t) + f(x, I, t, \theta) \cdot (A - x(t))$$

- **漏电流项** $-\frac{1}{\tau}x(t)$：驱动状态向零衰减，$\tau$ 控制记忆长度
- **输入驱动项** $f(x,I,t,\theta)\cdot(A-x(t))$：非线性耦合函数 $f$ 与有界激活 $(A-x(t))$ 的乘积
- **有界性**：$A$ 保证状态始终在有界区间内，天然稳定

### iNEST (SDI 化合键框架)
$$\frac{dL_h(t)}{dt} = f_\theta(h(t), x(t), t) + \text{FEP}_{\text{驱动固化/断开}}$$

- **无漏电流**：状态不衰减，信息可无限保持
- **FEP 驱动**：自由能原理驱动连接固化（长期增强）或断开（长期抑制）
- **化合键机制**：化学键（长程）与电突触（短程）双通道

### v9 自适应 tau（LNN 桥接）
$$\tau_i(t) = \frac{\tau_{\text{base}}}{1 + \alpha \cdot \text{surprise}_i(t)}$$
$$\text{surprise}_i = \frac{|F_i(t) - \bar{F}_i|}{\sigma_{F_i}}$$

## 机制差异深度分析

| 维度 | LNN | iNEST |
|------|-----|-------|
| **时间常数** | 全局 $\tau$，固定或可学习 | 自适应 $\tau_i(t)$，惊讶度驱动 |
| **状态有界性** | 通过 $A$ 硬约束 | 通过 FEP 自由能最小化软约束 |
| **记忆机制** | 漏电流自然遗忘 | 无漏电流 + FEP 主动固化/断开 |
| **局部自适应** | $f$ 的非线性变换 | $f_\theta$ + STDP + 胶质细胞缩放 |
| **收敛路径** | 指数衰减到吸引子 | FEP 最小自由能路径 |
| **物理第一性** | ODE 数值稳定性 | 最小作用量 + 变分自由能 |

## 工程实现关键差异

### LNN 侧
- PyTorch/TF 可通过 `torchdiffeq` 或自定义 ODE solver 实现
- `ncps` (Neural Circuit Policies) 库可直接调用
- 推理时 ODE 步长可自适应调节
- 适合资源受限端侧部署（2万参数即可导航）

### iNEST 侧
- 需要维护 SDI 化合键状态矩阵（化学键 + 电突触双通道）
- FEP 计算需跟踪局部自由能 $F_i$
- STDP 窗口 + 不应期 + 突触疲劳的脉冲级仿真
- 胶质细胞缩放作为全局调控信号
- 最终目标：异步电路 + 脉冲驱动 → FPGA/ASIC

## 共同演进方向

1. **连续状态演化** → 都采用 ODE/SDE 描述，天然适配 SNN 脉冲编码
2. **局部自适应** → 都支持节点级参数自适应（tau / theta / weight）
3. **最小能量路径** → LNN 通过漏电流衰减，iNEST 通过 FEP 梯度下降
4. **物理可部署性** → LNN 已有 FPGA 实现（MIT），iNEST 目标异步脉冲电路
