# LNN vs SDI 工程实现对照手册

- **类型**: 工程笔记
- **时间**: 2026-06-03
- **标签**: 工程实现, LTC, CfC, SDI, PyTorch, NetworkX, 异步电路
- **关联**: sdi_network_v8.py, sdi_v9_tau_adaptive.py

---

## 一、LNN 端到端实现栈

```
训练: PyTorch LTC/CfC + ODE solver (torchdiffeq)
  ↓ ONNX 导出 (CfC 闭式解友好)
推理: ONNX Runtime / TensorRT -> NVIDIA Jetson / x86
  ↓ 进一步压缩
边缘: 脉冲编码 -> Intel Loihi 2 (Nengo/Lava 框架)
```

### 关键代码片段 (LTC Cell)

```python
class LTC_Cell(nn.Module):
    def __init__(self, input_size, hidden_size):
        self.tau_net = nn.Linear(input_size + hidden_size, hidden_size)
        self.gate_net = nn.Linear(input_size + hidden_size, hidden_size)

    def forward(self, x, h_prev):
        combined = torch.cat([x, h_prev], dim=-1)
        tau = torch.sigmoid(self.tau_net(combined)) * 10.0
        gate = torch.sigmoid(self.gate_net(combined))
        A = 1.0
        dh = -(1.0 / tau) * h_prev + gate * (A - h_prev)
        return h_prev + dh
```

---

## 二、SDI 端到端实现栈

```
仿真: Python NetworkX + NumPy (sdi_v8 -> v9)
  ↓ 行为模型
数字原型: Amaranth/PyRTL -> SystemVerilog RTL
  ↓ FPGA 验证
FPGA: Xilinx Kria KR260 / Alveo U50
  ↓ 量产
ASIC: SkyWater 130nm 开源工艺
```

### 关键代码片段 (SDI Node FEP Decision)

```python
class SDI_Node:
    def fep_decision(self):
        for i, (target, btype, w) in enumerate(self.bonds):
            prediction = self.predict_activation(target)
            actual = target.activation
            F_local = (prediction - actual)**2
            if btype == "E-S" and w > self.w_threshold:
                self.bonds[i] = (target, "E-L", w)  # 固化
            elif btype in ("E-S", "I-S") and w < 1e-6:
                self.bonds.pop(i)  # 断开
```

---

## 三、部署路径对比

| 阶段 | LNN | iNEST SDI |
|------|-----|-----------|
| 训练/演化 | GPU 训练（监督学习） | CPU 仿真（FEP 自演化） |
| 模型导出 | ONNX (CfC 闭式解) | 键状态矩阵 JSON |
| 边缘部署 | TensorRT -> Jetson | FPGA 异步电路 |
| 在线学习 | 需重新训练 | 原生支持（FEP 不停运行） |

---

## 四、异步电路映射要点

### LNN -> 异步电路（困难）

- tau 是浮点参数，需 DAC 转换
- ODE 需要积分器，模拟电路实现复杂
- 每层 tau_net/gate_net 需要矩阵乘法器

### SDI -> 异步电路（天然）

- 键状态机 = 4 种离散状态（E-L/I-L/E-S/I-S），直接映射为 2-bit FSM
- FEP 决策 = 比较器 + 计数器（STDP 累积）-> 阈值触发
- 脉冲传播 = AER（Address Event Representation）编码
- **无需乘法器，无需积分器**

---

> **工程笔记 | 2026-06-03**
