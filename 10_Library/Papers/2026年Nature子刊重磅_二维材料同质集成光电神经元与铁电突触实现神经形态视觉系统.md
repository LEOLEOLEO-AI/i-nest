---
title: 2026年Nature子刊重磅：二维材料同质集成光电神经元与铁电突触实现神经形态视觉系统
tags:
- brain
- chip
- chiplet
- dynamics
- literature
- neural-networks
- neuron
- neuroscience
- paper
- simulation
---
- **类型**: link
- **时间**: 2026-02-18 15:13:53
- **标签**: AI链接笔记, 神经形态视觉, 二维材料集成, 光电神经元
- **来源**: https://mp.weixin.qq.com/s/jQY7l0gvOq3HeuaZ6RLioA

## 内容

### **📌 研究背景与核心突破**

#### **传统机器视觉的瓶颈**

传统机器视觉系统中，"传感器-存储器-处理器"为**异质分立结构**，存在连线复杂、数据搬运成本高、延迟大等问题。北大杨玉超团队提出**同质集成（homogeneous integration）策略**，将光电编码器（神经元）和非易失突触（权重存储）在**同一材料体系与工艺流程**下实现互连，大幅简化封装与工艺接口，降低集成复杂度并支持高密度互连。

#### **研究核心成果**

在同一片基底上实现**MoS₂光电晶体管（PT）型光电子LIF神经元**与基于**HZO铁电层的MoS₂ FeFET突触**的联合阵列，构建小规模**存感算一体（in-sensor）SNN骨架**，成功演示色彩识别与复杂场景目标检测任务。

### **🔬 核心技术架构**

#### **1. 光电神经元（MoS₂ PT + 外部神经元电路）**
- **核心原理**：采用少层MoS₂光电晶体管，利用**光生载流子俘获/释放机制**实现无电容（capacitor-less）膜电位累积，配合比较器电路形成完整**LIF动力学**（积分→达阈→触发脉冲→自动重置）。
- **关键特性**：
  - 光谱响应：支持450nm（蓝）、520nm（绿）、650nm（红）多波长响应
  - 编码策略：支持**频率编码（rate coding）** 与**首脉冲时间编码（TTFS）**
  - 脉冲参数：6V幅值、~20μs宽度（实验读出值）

#### **2. 铁电突触（MoS₂ FeFET, MFMIS结构）**
- **器件结构**：采用**TiN/HZO/TiN（MFM）** 与**Al₂O₃/MoS₂（MIS）** 叠层的MFMIS结构，通过HZO极化切换实现非易失电导调节。
- **性能参数**：

| 指标                | 数值/特性                          |
|---------------------|-----------------------------------|
| **可编程电导态**    | ~50个离散电导态                   |
| **动态范围**        | 约8×（Gmax/Gmin=8）               |
| **工作偏压**        | 0–1V低偏压范围，I–V特性近线性     |
| **保持特性**        | 零偏下>100s（演示级）             |
| **耐久性能**        | ≥5,000次脉冲循环（实验尺度）      |

#### **3. 同质集成与阵列实现**
- **实验平台**：1×4 MoS₂ PT阵列 + 4×4 FeFET阵列（机械剥离MoS₂片转移至预制栅栈）
- **信号链路**：PT编码输出→PCB神经元电路→FeFET阵列执行MAC（加权累加）
- **器件一致性**：
  - PT阵列Vth变异：~12.7%（4个器件）
  - FeFET阵列Vth变异：~7.7%（16个器件）
- **映射策略**：采用差分4-bit电导映射实现系统仿真

### **📊 性能实测与验证**

#### **系统级任务表现**

| 任务类型          | 数据集/方法               | 准确率   | 实现方式                     |
|-------------------|--------------------------|----------|------------------------------|
| **颜色识别**      | RGB patterns             | 91.7%    | 混合硬件-仿真流程            |
| **目标检测**      | Karlsruhe dataset        | 93.5%    | SEW ResNet18风格SNN模型      |

#### **关键器件参数**
- **光电PT**：稳定实现频率与TTFS编码，脉冲参数6V/20μs
- **FeFET突触**：50个可编程电导态，动态范围8×，D2D Vth变异7.7%

### **⚖️ 技术优势与局限性**

#### **核心优势**
1. **同质集成架构**：避免异质互联的工艺难题，简化封装与接口
2. **多波段响应**：MoS₂光电响应天然支持RGB多光谱编码
3. **高效计算**：FeFET架构支持低偏压多级权重调节与直接MAC运算

#### **当前局限**
1. **材料制备**：依赖机械剥离MoS₂，尚未实现晶圆级生长与转移一致性
2. **可靠性指标**：FeFET保持（>100s）与耐久（5,000次）为演示级，距工业级要求（数年保留/≥10⁶次循环）差距显著
3. **系统规模**：当前为小规模原型（1×4 PT + 4×4 FeFET），需验证大规模集成可行性
4. **能耗延迟**：系统级能耗与延迟数据未直接交付，需与商业化神经形态芯片对标优化

### **📝 补充细节**
- **HZO材料**：Hf-Zr-O（铪锆氧化物）铁电层，是近年来铁电存储器领域的研究热点
- **LIF神经元**：Leaky Integrate-and-Fire神经元模型，模拟生物神经元的脉冲发放特性
- **MAC运算**：Multiply-Accumulate（乘累加）运算，神经网络核心计算单元
- **SNN**：Spiking Neural Network（脉冲神经网络），具有事件驱动、低功耗特性

## 原文

这里是类脑智能计算，大家新年快乐！今天带大家解读2026年2月7日刚刚发表在 Nature Communications 上的重磅论文。论文题目： Homogeneous integration of two-dimensional material-based optoelectronic neurons and ferroelectric synapses for neuromorphic vision

DOI: 10.1038/s41467-026-68905-3 关键词： 二维材料 / 全同质集成 / 神经形态视觉 / 光电神经元 / 铁电突触 / 存感算一体

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd72916434b43f7d86d5943e63c6aa695?Expires=1776346034&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=5OFUuCU0lHPa%2Bkaj9jkUdr0LmKE%3D)

# 背景介绍

在传统机器视觉中，“眼睛（传感器）—记忆—处理器”常常是异质分立的多芯片系统，连线、搬运与延迟成本高。北大杨玉超团队提出并实验了同质集成（homogeneous integration）策略：把光电编码器（眼/神经元）和非易失突触（权重存储）在同一材料体系与工艺流程下实现互连，从而大幅简化封装与工艺接口，降低集成复杂度并有利于高密度互连。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3960e66f00a09eb5aa297103356a2981?Expires=1776346034&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=z1oOr8t270mozvv0WS7gV6SsMiE%3D)

图 1｜MoS₂-based in-sensor neuromorphic computing（体系示意）

(a) 系统示意：光学输入由 MoS₂ 光电神经元（PT+neuron circuit）转换为时域稀疏脉冲，再由同一基底上的 FeFET 阵列执行加权累加（MAC），实现 in-sensor 的感知与初步处理。In：MAC 输出电流；Vm：输入电压；Gmn：编程电导。

(b) 实验原型：1×4 的 PT 阵列与 4×4 的 FeFET 阵列的光学/电气连接与 SNN 映射框图（图中强调“同一 MoS₂ 平台上的器件集成”）。

# 一句话解释

作者在同一片基底上实现了MoS₂ 光电晶体管（phototransistor, PT）型的 optoelectronic LIF 神经元与基于 HZO（hafnium–zirconium oxide）铁电层的 MoS₂ FeFET 突触的联合阵列，并把两者联成了一个小规模的 in-sensor SNN 骨架，用以演示色彩识别与复杂场景的目标检测任务。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9c55029b6ea3f3488e24aa122ef07179?Expires=1776346034&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=7%2F7PvM4Lh8EqngxqvRh2xeKhR58%3D)

图 2｜MoS₂ optoelectronic LIF neuron（器件与编码）

(a) 器件+电路示意：PT 在光激励下通过光生俘获/释放机制实现膜电位累积（无需外部积分电容），当 Vmembrane ≥ Vreference 比较器触发脉冲并同步触发 reset 机制；（Inset）示例脉冲：6 V、~20 μs。

(b) 光吸收谱与 RGB 响应（插图为同功率下的转移曲线），显示 MoS₂ 的多光谱响应能力。

(c) 在不同光功率下的阈位移曲线，(d–i) 展示了频率编码（F）與 TTFS（Ttrigger）随波长与功率的调制关系。

# 核心技术

## 1. 光电神经元（MoS₂ PT + 外部神经元电路）

采用少层 MoS₂ 光电晶体管，利用photogating（光生载流子俘获/释放）机制实现无电容（capacitor-less）的膜电位累积；配合比较器电路形成完整的 Leaky Integrate-and-Fire（LIF）动力学：积分 → 达阈 → 触发脉冲 → 自动重置。设备对 450/520/650 nm 等波长均有响应，支持rate coding与time-to-first-spike (TTFS)两种编码策略。脉冲示例：6 V 幅值、~20 μs 宽度（实验读出）。这些特性使 PT 能直接把光强转成稀疏脉冲流。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F2939a3ef1d537e556114f6407b7e1402?Expires=1776346034&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=jB7H7BbxzeAprIGrDNNvqQNnurk%3D)

图 3｜MoS₂ FeFET（MFMIS 结构与可编程电导）

(a) 器件截面与工作原理（MFMIS：TiN / HZO / TiN + Al₂O₃ / MoS₂），说明如何通过调节 MFM/MIS 面积比调整电压分配与记忆窗口。

(b–c) TEM/EDS 与 HRTEM 展示了 HZO 多晶铁电层与层状堆栈的结构证据。

(d–h) 传输/滞回与多级编程：展示 counterclockwise hysteresis、可实现约 50 个离散电导态与 LTP/LTD 编程策略。

(i–j) 保持 (>100 s) 与耐久（≥5,000 脉冲）实验结果说明设备的演示级可靠性。

## 2. 铁电突触（MoS₂ FeFET, MFMIS 结构）

FeFET 采用 TiN / HZO / TiN（MFM）与 Al₂O₃ / MoS₂（MIS）叠层的 MFMIS 结构，利用 HZO 的极化切换实现非易失的多级电导调节（论文展示了 ~50 个离散电导态、动态范围约 8×）。该结构可通过调节 MFM/MIS 面积比获得可控的记忆窗口，并在 0–1 V 低偏压范围内表现出近线性的 I–V，利于做 MAC。保留与耐久：论文给出在零偏下 100 s 以上的保持（retention）与 5,000 次循环的耐久演示（实验尺度，尚非长期年级工程指标）。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F2e8e3cc9f43d31b857e05a9cfff8559d?Expires=1776346034&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=TjLGXs%2FHE8ytGhE9MI6zT4chbrY%3D)

Fig 4｜Neuron-synapse integrated array & SNN mapping

(a) 系统连线图（PT → neuron circuit → FeFET array → MAC），说明如何把 PT 的脉冲转为 FeFET 的输入信号（通过电阻分压以匹配电平）。

(b–d) 光学显微照片与 D2D 统计：展示 1×4 PT 与 4×4 FeFET 的物理阵列与 Vth 变异（PT ≈12.7%，FeFET ≈7.7%）。

(e–g) 基于实验器件参数的 SNN 仿真流程与 RGB 分类准确率（91.7%），以及 4-bit 差分电导映射策略的说明。

## 3. 同质集成与阵列实现

实验平台包含一个1×4 的 MoS₂ PT 阵列与一个4×4 的 FeFET 阵列（器件由机械剥离的 MoS₂ 片制成并转移到预制栅栈上），并把 PT 的编码输出通过 PCB 上的神经元电路送到 FeFET 阵列做 MAC。论文给出器件间变异：4 个 PT 的 Vth 变异 ~12.7%，16 个 FeFET 的 Vth 变异 ~7.7%，并展示了 4×4 突触矩阵的累加（MAC）功能与多级映射策略（差分 4-bit 映射用于系统仿真）。这些都是重要的工程数据点，但也表明目前规模仍处于样片/原型阶段。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc94b10f7482d0658494e3ad0a2cfa7a3?Expires=1776346034&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=u%2BtCsGuaY40rpMK%2FR4Sjd4gd54g%3D)

Fig 5｜Object detection（道路场景）

(a) Spike encoding：TTFS 与 rate coding 的数学关系与设备参数映射（设备 F、Ttrigger 与光强 P 的经验拟合公式详见论文）。

(b–f) SEW

---
**Tags:** [[BrainInspired]] [[SDSoW]] [[Chiplet]]
