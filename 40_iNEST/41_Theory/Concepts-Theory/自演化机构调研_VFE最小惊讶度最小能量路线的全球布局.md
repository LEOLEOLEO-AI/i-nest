---
title: "自演化机构调研：VFE/最小惊讶度/最小能量路线的全球布局"
date: 2026-06-03
tags: [FEP, 变分自由能, 自演化, 开源IP, FPGA, 脉冲神经网络]
topics: [Concepts-Theory, Chip-Hardware, Neuroscience]
---

## 核心路线：物理第一性驱动的神经网络自演化

> 不是人为设计非线性激活函数，而是靠变分自由能、最小惊讶度和最小能量消耗来让神经网络遵从物理第一性，自演化收敛到结构流形的吸引子上。

## 全球机构布局

### 1. Karl Friston 团队 (UCL, VERSES AI)
- **路线**：Active Inference + Free Energy Principle
- **开源**：`pymdp` (Python), `rxinfer` (Julia)
- **硬件**：VERSES AI 的 Genius™ 平台（基于 Active Inference 的智能体）
- **借鉴价值**：⭐⭐⭐⭐⭐ FEP 理论的完整数学框架

### 2. MIT CSAIL (Ramin Hasani, Daniela Rus)
- **路线**：Liquid Neural Networks (LNN) + Closed-form Continuous-time (CfC)
- **开源**：`ncps` (Neural Circuit Policies), `keras-cfcn`, `pytorch-cfc`
- **硬件**：FPGA LNN 实现（无人机导航）
- **借鉴价值**：⭐⭐⭐⭐⭐ 最接近的工程实现参考

### 3. Intel Loihi / Lava 生态
- **路线**：脉冲神经网络 + 片上可塑性 (STDP)
- **开源**：`lava-nc`, `lava-dl`, `lava-optimization`
- **硬件**：Loihi 2 芯片
- **借鉴价值**：⭐⭐⭐⭐ 异步脉冲电路的商业级实现

### 4. SynSense (时识科技)
- **路线**：类脑脉冲神经网络芯片
- **开源**：`sinabs` (PyTorch-based SNN library)
- **硬件**：Speck™, DYNAP-CNN, Xylo™
- **借鉴价值**：⭐⭐⭐⭐ 低功耗 SNN 芯片的商业标杆

### 5. IBM Research (Dharmendra Modha)
- **路线**：TrueNorth + NorthPole 芯片
- **开源**：`TrueNorth` 编程框架
- **借鉴价值**：⭐⭐⭐ 大规模脉冲网络的架构参考

### 6. 清华大学 (施路平, 吴华强)
- **路线**：天机芯 (Hybrid SNN+ANN), 忆阻器阵列
- **借鉴价值**：⭐⭐⭐⭐ 国内最成熟的类脑芯片路线

### 7. 中科院计算所 / 自动化所
- **路线**：晶上系统 + 类脑计算
- **借鉴价值**：⭐⭐⭐⭐ 晶上SDI的直接合作方

## 可直接使用的开源 IP

| 项目 | 用途 | 许可证 |
|------|------|--------|
| `pymdp` | Active Inference / FEP 仿真 | MIT |
| `ncps` | LNN 网络构建 | Apache 2.0 |
| `torchdiffeq` | ODE 求解器 | MIT |
| `lava-nc` | SNN 仿真 (Loihi兼容) | BSD-3 |
| `sinabs` | SNN 训练与推理 | AGPL-3.0 |
| `snnTorch` | SNN 梯度学习 | MIT |
| `brian2` | 脉冲神经网络仿真 | CECILL-2.1 |
| `nengo` | 神经工程框架 | Free for non-commercial |

## FPGA 落地参考

### 已有 FPGA 脉冲网络项目
- **ODIN**：在线学习 SNN (Verilog)
- **SpiNNaker**：大规模 SNN 仿真
- **LNN-FPGA**：MIT 的 LNN 硬件加速器

### iNEST 的 FPGA 路线
1. Phase 1：Xilinx RFSoC / VCK190 上实现 SDI 化合键 + 自适应 tau
2. Phase 2：HLS 综合 + Vivado IP 封装
3. Phase 3：异步电路综合（NULL Convention Logic / Click 元件）
