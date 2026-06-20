---
title: "国际自演化神经形态计算IP与开源代码全景清单"
date: 2026-06-03
tags: [IP清单, 开源代码, 神经形态, FEP, SNN, FPGA, 自演化]
topics: [AI-ML, Chip-Hardware, Concepts-Theory]
---

## 一、可直接借鉴的开源项目

### 1. 脉冲神经网络 (SNN) 框架

| 项目 | 机构 | 语言 | 关键特性 | 借鉴价值 |
|------|------|------|---------|---------|
| **snnTorch** | UC Santa Cruz | Python/PyTorch | 梯度替代训练，支持STDP | STDP模块可直接复用 |
| **Brian2** | 全球社区 | Python | 生物物理精确SNN模拟器 | tau/不应期/突触疲劳建模 |
| **NEST** | 欧洲HBP | Python/C++ | 大规模SNN模拟 (>10^8神经元) | 规模扩展参考 |
| **Lava** | Intel | Python | Loihi 2 软件框架，支持在线STDP | 片上学习映射参考 |
| **Sinabs** | SynSense | Python | DYNAP-SE2 事件相机处理 | 脉冲编码/解码管线 |
| **Rockpool** | SynSense | Python | 异构SNN训练（Xylo/DYNAP） | FPGA→ASIC迁移路径 |

### 2. 神经形态硬件SDK

| 项目 | 机构 | 硬件 | 关键特性 |
|------|------|------|---------|
| **Lava-dl** | Intel | Loihi 2 | 片上STDP + 自适应阈值 |
| **Samsung SNP SDK** | Samsung | SNP芯片 | 脉冲驱动ANN-SNN转换 |
| **IBM aIHWKit** | IBM | NorthPole/模拟 | 模拟存算一体 + 漂移补偿 |

### 3. FEP/主动推理开源实现

| 项目 | 机构 | 语言 | 关键特性 |
|------|------|------|---------|
| **pymdp** | VERSES AI | Python | 主动推理库，POMDP框架 |
| **DEM Toolbox** | UCL (Friston) | MATLAB | 动态期望最大化，变分贝叶斯 |
| **spm** | UCL | MATLAB/Python | 统计参数映射，DCM动态因果建模 |
| **infer-actively** | MIT-IBM | Python | 主动推理+强化学习融合 |

### 4. 异步电路/脉冲电路

| 项目 | 机构 | 语言 | 关键特性 |
|------|------|------|---------|
| **ACT** | Columbia/UNM | C/HLS | 异步电路综合工具链 |
| **Balsa** | Manchester | HLS | NCL异步电路描述语言 |
| **Workcraft** | Newcastle | Java | 异步电路形式化验证 |

---

## 二、关键研究机构与团队

### 物理第一性 + 自演化路线

| 机构 | 团队 | 路线 | 可借鉴IP |
|------|------|------|---------|
| **UCL** | Karl Friston | 自由能原理 + 主动推理 | DEM/SPM工具链，预测编码层级模型 |
| **VERSES AI** | Friston+团队 | 空间网络智能，主动推理标准化 | pymdp, Spatial Web协议 |
| **MIT CSAIL** | Daniela Rus/Ramin Hasani | 液态神经网络LNN + FPGA实现 | ncps库, LNN-FPGA架构 |
| **Intel Labs** | Mike Davies | Loihi 2 + 片上STDP | Lava框架, 在线学习算法 |
| **SynSense** | Giacomo Indiveri | 脉冲神经形态芯片(DYNAP-SE2) | Sinabs/Rockpool, 事件驱动架构 |
| **IBM Research** | Dharmendra Modha | NorthPole存算一体架构 | aIHWKit, 模拟存算 |
| **Stanford** | Kwabena Boahen | Neurogrid/模拟神经形态 | 亚阈值电路设计 |
| **Heidelberg** | Karlheinz Meier | BrainScaleS (HBP) | 模拟加速神经形态 |
| **清华** | 施路平团队 | 天机芯片(ANN+SNN异构融合) | 异构计算架构参考 |
| **中科院计算所** | 陈云霁/陈天石 | 寒武纪/达武芯片 | 国产AI芯片IP |

### KAN + 函数权重路线

| 机构 | 团队 | 路线 | 可借鉴IP |
|------|------|------|---------|
| **MIT** | Ziming Liu/Max Tegmark | KAN (Kolmogorov-Arnold Networks) | pykan库, B样条激活函数 |
| **Caltech** | Anima Anandkumar | Fourier Neural Operator | 连续函数映射 |
| **Brown** | George Karniadakis | PINN/DeepONet | 物理约束网络 |

---

## 三、FPGA/ASIC 开源参考实现

| 项目 | 描述 | 链接 |
|------|------|------|
| **OpenNPD** | 开源神经处理单元 | RISC-V + 脉冲加速 |
| **ODIN** | 在线学习脉冲神经形态处理器 | 28nm FD-SOI验证 |
| **SpiNNaker2** | Manchester 第二代脉冲神经网络芯片 | ARM M4F×152核 |
| **TrueNorth** | IBM 开源工具链 | Corelet编程模型 |
| **Tonic** | 事件相机脉冲编码库 | 多种编码方案 |
| **Norse** | PyTorch脉冲网络库 | 梯度替代训练 |
| **SNNTorch** | 脉冲网络训练框架 | 支持STDP+替代梯度 |

---

## 四、iNEST 快速搭建路线图

### 第一步：仿真平台（本周可完成）
```
sdi_v8_patched.py（基线）→ sdi_v22_evolution.py（自适应θ+FEP稳态）
→ sdi_action_observer.py（最小作用量观测器接入真实数据）
```

### 第二步：原型验证（1-2月）
```
Python行为仿真 → Verilog bond_core.v → VCK190 单bond验证
→ 100节点原型
```

### 第三步：规模扩展（3-6月）
```
100节点 → 302节点（线虫）→ 1000节点 → 10000节点（果蝇部分）
```

### 最优先行动
1. **修复 v22+ 观测器的 σ 锁定问题**：接入 v8 的真实 connectome + bond 创建/删除机制
2. **运行 v22 完整仿真**：验证自适应 θ 是否能让 σ≥4.0
3. **单 bond FPGA 原型**：写 bond_core.v testbench + Vivado 综合

---

> 构建时间: 2026-06-03
> 注：以上开源项目均可在 GitHub 直接获取，许可证以 Apache 2.0 / MIT / BSD 为主
