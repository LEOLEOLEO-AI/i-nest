# 在 FPGA 上实现并行脉冲神经网络（Spiking Neural Net）

- **笔记本**: 我的剪贴板
- **时间**: 2026-01-08 02:38

---

原文链接: https://mp.weixin.qq.com/s/pQ3C69JkTCI-k5Xf7WFH-A

这个项目展示了如何在 FPGA 上实现一个并行的 脉冲神经网络（Spiking Neural Network, SNN），包括神经元模型、突触模型、学习机制等核心部分，在硬件中用 Verilog 语言进行建模与验证。
参数设置和模型输出示例如下所示：
https://people.ece.cornell.edu/land/courses/ece5760/DDA/NeuronIndex.htm脉冲神经网络是模仿生物神经元工作方式的神经网络，与传统人工神经网络不同，它在信息传递上使用离散脉冲（spike）进行交流，更接近生物神经系统的信息处理机制。该项目的核心目标是：
- 
使用 FPGA 实现快速的数值积分和时间步更新；
- 
在硬件上模拟具有生物学意义的神经元与突触行为；
- 
支持学习机制（如 STDP）来调整网络连接权重。
## 🧠 神经元模型：Izhikevich 动力学该设计采用了 Eugene Izhikevich 提出的简化神经元模型作为基本单元。该模型使用两个状态变量：这两个状态按照特定微分方程进行更新，从而在硬件上模拟神经元“发放脉冲”的动态行为。该模型在硬件上的数值积分可借助快速 FPGA 并行计算实现。
## 🧩 主要模块说明整个神经网络在 FPGA 上由多个 Verilog 模块组成，各模块均可配置参数并可用于扩展更复杂的网络：🔹 1. 神经元本体（Soma）模拟细胞体和脉冲发放机制；使用固定时间常数和可配置参数（a, b, c, d, I）；每个神经元以 1/16 ms（每步 1/16 毫秒）为单位更新状态。🔹 2. 脉冲传播延迟（Axon）用于模拟脉冲在轴突中的传播延迟；延迟范围可设为 1 到 64 个时间步。🔹 3. 化学突触（Chemical Synapse）由前突触放电控制的恒流源；指数衰减时间常数可配置（如 4、8、16、32 等时间步）；突触权重可设置为抑制（negative）或兴奋（positive）。🔹 4. 电突触（Electrical Synapse）电流由突触之间的电导和膜电位差决定；支持前向/反向整流或对称模式；可配合偏置电流一起使用。🔹 5. STDP 学习模块基于脉冲时序的权重塑性（Spike-Timing Dependent Plasticity）；如果后突触脉冲紧随前突触，则权重增加（因果增强）；如果前后顺序相反，则权重减弱（非因果减弱）；学习时间常数与权重调整范围可配置。
## 🔌 示例网络结构本项目提供了两个示例网络拓扑，用于演示神经元和突触之间的交互行为：
## 🧠 示例一：4 个神经元的拓扑在这个级联结构中：
- 
神经元 1 的脉冲可传递给神经元 2、神经元 3（通过电突触）和指示灯；
- 
神经元 2、3 和 4 之间也有类似连接；电突触将不同神经元的膜电位连接，使某些神经元在弱兴奋耦合下同步发放。这个例子展示了如何在 FPGA 中用 Verilog 实现多个神经元之间的 双向与电性耦合。
## 🧠 示例二：带 STDP 学习的神经元对另一个拓扑展示了三神经元结构：
- 
神经元 1 与神经元 3 之间通过 STDP 可学习突触连接；初始时两者不同步；随着脉冲传递和 STDP 权重调整，神经元 3 最终与神经元 1 同步。这个例子模拟了生物大脑中突触可塑性的变化过程，使得在硬件上出现学习现象。下图展示了初始的非同步电压（底部为神经元 1，顶部为神经元 3）、中间状态以及由上方 Verilog 模块生成的最终收敛状态。初始状态下，两个神经元均处于自发活动状态，但彼此之间的突触连接权重为零。通过调整赫布突触，在几千次脉冲后，神经元之间的耦合逐渐建立。在中间状态下，可以看到神经元 1 的每隔一次脉冲都会触发神经元 3 的一个脉冲，同时也可以看到由阈下耦合产生的微小电压。最终的平衡状态显示，神经元 1 的每次脉冲都会触发神经元 3 的一个脉冲。

## 参考
Ruben Guerrero-Rivera, et al, Programmable Logic Construction Kits for Hyper-Real-Time Neuronal Modeling, Neural Computation, Volume 18 , Issue 11 (November 2006) Pages: 2651 - 2679
https://hackaday.io/project/260-spiking-neural-net-in-parallel-fpga-hardware/details
https://people.ece.cornell.edu/land/courses/ece5760/DDA/NeuronIndex.htm
Eugene M. Izhikevich , Simple Model of Spiking Neurons, IEEE Transactions on Neural Networks (2003) 14:1569- 1572
## 项目代码
https://github.com/suisuisi/FPGATechnologyGroup/
🔍 项目意义这个 FPGA SNN 项目将生物神经系统的行为映射到硬件逻辑中，通过可配置的 Verilog 模块实现：
- 
生物学水平的脉冲神经元模型；
- 
化学与电性突触连接；
- 
基于时序的权重调整机制；
- 
并行结构提高计算效率。这样的实现不仅是神经网络模拟的实验平台，也为硬件加速的 SNN 研究提供了良好起点。

---
**Tags:** #BrainInspired
