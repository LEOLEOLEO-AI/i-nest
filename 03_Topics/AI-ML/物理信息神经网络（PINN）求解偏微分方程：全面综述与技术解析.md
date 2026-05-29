---
title: "物理信息神经网络（PINN）求解偏微分方程：全面综述与技术解析"
source: "https://mp.weixin.qq.com/s/64uqECf4mqdwISQ8PqI7HQ"
created: 2026-02-05
note_id: "1900810939465891880"
tags:
  - "AI链接笔记"
  - "物理信息神经网络（PINN）"
  - "AI for Science"
  - "偏微分方程（PDE）求解"
  - "get-笔记"
  - "学术论文"
---

# 物理信息神经网络（PINN）求解偏微分方程：全面综述与技术解析

## 摘要

### **🔬 引言：AI驱动的科学计算新范式**  **背景与意义** - **技术定位**：物理信息神经网络（Physics-informed Neural Networks, PINNs）是**AI for Science**领域的核心技术，通过将物理定律嵌入神经网络架构，实现数据拟合与物理规

## 正文

## 物理信息神经网络（PINN）求解偏微分方程：一篇全面综述

近年来，随着“AI for Science”的兴起，物理信息神经网络（Physics-informed Neural Networks,
PINNs）作为科学计算与深度学习交叉领域的一项变革性技术，为求解偏微分方程（PDEs）及其他复杂物理系统提供了一个强大而灵活的框架。通过将物理定律直接嵌入神经网络的架构中，PINNs能够整合领域先验知识，确保模型在拟合数据的同时遵守已知的物理规律。

### 引言

传统上，研究者依赖理论推导和实验验证来探索自然现象。然而，计算方法的出现引入了多种数值模拟技术，使得研究复杂现实系统成为可能。微分方程，特别是偏微分方程，在科学与工程领域扮演着核心角色，因为它们能够描述涉及多变量函数的复杂现象，如热传导、流体动力学和波传播等。传统的PDE数值解法包括有限元法、有限体积法等。尽管这些方法成熟且精确，但在处理高维问题、复杂几何或反问题时可能面临挑战。近年来，深度学习的迅猛发展为PDE求解提供了新的范式。物理信息机器学习（PIML）将传统机器学习技术与领域物理知识相结合，而PINNs作为其中的杰出代表，通过将控制PDE及其边界/初始条件编码到神经网络的损失函数中，利用自动微分指导训练，实现了物理约束与观测数据在统一框架下的无缝融合。

![null](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc201ddff45396c697e115257024e73a7?Expires=1780060401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=g8vMdCt9GIE4f38MUALFguznQW8%3D)

图 1 物理学信息机器学习的各种应用

### PINN基础

#### 问题公式化

PINN的核心思想是在神经网络训练过程中，将物理系统的控制方程作为约束条件强制执行。考虑一个PDE约束的优化问题，其解  为状态变量，其中  为空间坐标，
为时间。对应的PDE通常可写为：

并附有初始条件  和边界条件 。其中， 为PDE参数， 和  分别为求解域及其边界。

神经网络的目标是近似解 ，记作 ，其中  为网络参数。

![null](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc5f88ccf41caa789f18cd64f3cea5c59?Expires=1780060401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=tF%2BIBUg42P%2Bann1GCXwB%2BTOHrEc%3D)

图 2 PINN 框架示意图

#### 损失函数与训练

为了将PDE约束融入训练，PINN的损失函数由两部分组成：数据驱动损失和物理信息损失。

物理信息损失  进一步分解为PDE残差损失、边界条件损失和初始条件损失：

其中：

* •  衡量PDE残差：
* •  衡量边界条件误差：
* •  衡量初始条件误差：

数据损失  则衡量预测值与观测数据之间的误差：

通过梯度下降等优化算法最小化总损失，PINN能够从数据中直接学习系统的物理规律。

#### 性能评估

评估PINN的性能通常涉及以下几个关键指标：

* • **相对误差**：衡量预测解与真实解之间的整体偏差。
* • **均方根误差（RMSE）**：量化预测误差的离散程度。
* • **PDE残差**：衡量预测解满足PDE的程度。

### PINN的架构演进

PINN的成功离不开多样化的神经网络架构。早期工作主要利用多层感知机（MLP）的通用逼近能力。Raissi等人于2019年提出的vanilla
PINN奠定了这一领域的基础。随后，为了应对不同挑战，研究者们发展了一系列专用架构。

![null](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F950456e27e5fd3b316e3550cfc292e5d?Expires=1780060401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=iq9FF4rxHJVifNpDSrrvhVJfoko%3D)



![null](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0edc93c829afee5fdd0cc5b3302cd794?Expires=1780060401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=SZCssheOknu930CZkfXLN%2FRaaM8%3D)

#### 多层感知机（MLP）

MLP是PINN最基础的架构，其理论基础是通用逼近定理。一个具有单隐藏层和合适激活函数的MLP可以以任意精度逼近任何连续函数。在vanilla
PINN中，针对不同PDE问题（如薛定谔方程、Allen-Cahn方程），网络层数和每层神经元数通常根据经验选择。

![null](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7d80fe81196b1970a8af057481697aad?Expires=1780060401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=XbfWLo4%2F8n%2F6ACp7DDZLCfIKKkA%3D)

图：MLP框架示意图

#### 卷积神经网络（CNN）

CNN特别适合处理具有网格状拓扑结构的数据，如图像。其核心是卷积层和池化层，能有效提取空间特征。在PINN中，CNN被用于处理具有规则或规则化后几何域的问题。例如，PhyGeoNet通过椭圆坐标映射将不规则几何转换为规则域，从而应用标准CNN求解参数化稳态PDE。Spline-PINN则结合了PINN与CNN的优势，使用Hermite样条核实现网格表示的连续插值。

#### 循环神经网络（RNN）

RNN及其变体（如LSTM、GRU）专为处理序列数据设计，能捕捉时间依赖性。在求解时空PDE时，RNN架构表现出色。PhyCRNet是一种物理信息卷积-循环学习架构，利用编码器-解码器卷积LSTM网络进行空间特征提取和时间演化，无需标记数据即可求解时空PDE。

![null](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4f3dea29e9e3d6f6056b6c2e442bcaa4?Expires=1780060401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=G8JWq2%2BpQQ5OoU5ePAuasKmO1Tc%3D)

图：f-PICNN用于时间依赖PDE的神经网络架构，包含非线性卷积单元（NCUs）

![null](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F882f72d5e93473661ce582bf483fe6e0?Expires=1780060401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=RLyPEGMDZiDGD4wl8s8CpNbAusY%3D)

图：PhyCRNet框架

#### 生成对抗网络（GAN）

GAN包含一个生成器和一个判别器，通过对抗训练生成逼真数据。在PINN中，GAN被用于求解随机微分方程（SDE）和量化不确定性。例如，PI-GANs利用GAN框架解决基于有限测量数据的正向、反演及混合随机问题。Wasserstein
GAN也被用于量化PDE解中的不确定性。

#### Kolmogorov-Arnold网络（KAN）

KAN基于Kolmogorov-Arnold表示定理，将高维函数分解为单变量函数的有限组合。与将激活函数置于神经元上的MLP不同，KAN将可学习的激活函数置于网络边上，从而提升了模型的解释性和准确性。Kolmogorov-Arnold-Informed
Neural
Network（KINN）等基于KAN的PINN架构在精度和收敛速度上显示出优于传统MLP-PINN的潜力，尤其擅长处理多尺度、奇异性和非线性问题。

#### Transformer

Transformer凭借其自注意力机制，能够高效处理长程依赖关系，已在自然语言处理领域取得革命性成功。近年来，Transformer被引入PDE求解。Physical
Information
Transformer（PIT）基于Transformer架构学习PDE的解算子，利用注意力机制捕捉初始条件与查询点之间的关系。PINNsFormer则通过多头注意力机制捕捉时间依赖性，提升了PDE解的泛化能力和精度。Transolver则针对复杂几何上的PDE求解，引入了PhysicsAttention机制，以线性计算复杂度捕获复杂物理关联。

![null](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4cc761be73446e6a717ee6be9eee8ccf?Expires=1780060401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=DSsewbUbmeJTs1JcvO9ayq16dx8%3D)

图：PINNsFormer框架

#### 其他架构与领域分解

除了上述主流架构，还涌现出许多新颖的PINN变体。神经架构搜索（NAS）被用于自动化PINN超参数优化，如NAS-PINN。可分离PINN（SPINNs）通过逐轴处理输入而非逐点处理，缓解了维数灾难问题。PirateNets则通过自适应残差连接，使网络能从浅层开始并逐步加深，提高了训练稳定性。

对于大规模复杂问题，领域分解方法被引入PINN。该方法将整个求解域划分为多个子域，在每个子域内独立求解，并通过界面条件保证解的连续性。扩展PINN（XPINNs）和保守PINN（cPINNs）是其中的代表。

![null](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7d0bc4bb412d93777d247b1dab06c01e?Expires=1780060401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=e7iW1CN2ZzEteWnwQ9SWk8PVHr8%3D)

图：基于神经架构搜索的 PINN 框架 (NAS-PINN) (Wang 和 Zhong 2024)

![null](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbe0c6312cf4435fe684349b2e742b917?Expires=1780060401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=oDrLKjyfmsM2KOXQW5dkT4liXCc%3D)

图：PINN中的领域分解方法

### 提升PINN性能的关键技术

#### 自适应数据重采样

PINN的性能严重依赖于训练采样点的选择。固定采样策略（如均匀采样、随机采样）可能无法高效处理具有复杂解结构的问题。自适应采样策略能动态调整采样点分布，提高训练效率。

* • **残差自适应细化（RAR）**：在PDE残差较大的区域添加新的残差点。
* • **重要性采样**：根据损失函数比例分布采样配置点，加速收敛。
* • **R³采样（Retain-Resample-Release）**：通过逐步在高残差区域累积配置点，缓解解从边界/初始条件向内部点传播失败的问题。
* • **深度自适应采样（DAS-PINNs）**：利用深度生成模型（如KRnet）根据残差分布生成新配置点。
* • **高斯混合分布自适应采样（GAS）**：利用当前残差信息生成高斯混合分布来采样额外点。

![null](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F87c4943e884f497c901061ef226233be?Expires=1780060401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ZaIVgyOgL5QMs7sRClWd4zcKCqU%3D)

图：提出的HA采样方法在一维泊松方程上的性能表现

#### 损失函数与优化策略

损失函数的设计和优化策略直接影响PINN的收敛和性能。

**损失重加权**：由于PDE损失、边界损失和初始损失的量级和收敛速度可能不同，直接相加可能导致优化失衡。多种自适应损失重加权方法被提出：

* • **学习率退火与梯度统计**：利用梯度统计平衡复合损失函数。
* • **基于神经正切核（NTK）的梯度下降**：利用NTK的特征值分析不同损失分量的收敛速率差异，并据此平衡训练过程。
* • **自适应损失平衡PINN（lbPINNs）**：通过概率建模和最大似然估计，动态调整各损失项的权重。其损失函数形式为：
* • **SelectNet**：引入选择网络，自适应地对训练样本加权，在训练早期优先学习简单样本。
* • **自注意力PINN（SA-PINNs）**：为每个训练点分配完全可训练的自适应权重，使网络能自主聚焦于解的困难区域。
* • **损失注意力PINN（LA-PINN）**：通过损失注意力网络（LAN）为每个训练点的误差分配不同权重，并采用生成器与LAN之间的对抗训练机制动态调整。

**新型损失函数**：

* • **梯度增强PINN（gPINNs）**：在损失函数中额外加入PDE残差梯度的约束，强制残差的导数也为零，从而提升精度和泛化能力。其损失函数为：  
    
  其中  惩罚残差对第  个自变量的偏导。
* • **针对多尺度问题的损失函数**：通过分组正则化策略归一化不同损失分量的尺度，确保各项对总损失贡献均衡。
* • **损失**：研究表明，对于某些PDE（如Hamilton-Jacobi-Bellman方程），传统的损失可能不是最优的，而损失能带来更好的稳定性。相应的训练算法采用类似对抗训练的min-max优化策略。

#### 特征嵌入与增强

特征嵌入通过将输入映射到高维或特征空间，帮助神经网络更好地捕捉高频信息和复杂模式。

* • **傅里叶特征映射**：受NeRF（神经辐射场）中位置编码的启发，傅里叶特征映射能有效缓解坐标基MLP的频谱偏差（倾向于学习低频函数）。一种常见的映射形式为：
* • **先验字典PINN（PD-PINN）**：配备任务相关字典，增强模型的特征捕获能力和表示能力。
* • **正弦特征PINN（sf-PINN）**：对输入进行正弦映射，增加输入梯度的变异性，避免陷入局部极小值。
* • **维度增强PINN（DaPINN）**：通过副本增强、幂级数增强、傅里叶级数增强等方法，系统性地增加网络输入的维度，使神经网络能提取更具信息量的特征，从而提高求解精度。

![null](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fccf27212e5a1d8a2d1eda193ee34658b?Expires=1780060401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=O8X0oq2gKZLZ6YJ6KA4Y0lFHb0I%3D)

图：维度增强神经网络（DaPINN）框架

![null](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F03a4a2123bc03b25a746bc9363a8b1a4?Expires=1780060401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=wd6WDOpOdgYgSWhLYIce2i6oYPA%3D)

图：DaPINN在一维泊松方程上的性能表现及与PINN的对比

![null](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fcbe9b6afea3a27f82cf90dfc6d61ba05?Expires=1780060401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=5LvpxPfq8921k858%2BMP%2Ffp1BG%2Bs%3D)

图：DaPINN在Burgers方程上的性能表现

### PINN的应用领域

PINN的灵活性和强大能力使其在多个科学工程领域得到成功应用。

#### 流体动力学

在流体力学中，PINN为求解控制流体运动的Navier-Stokes方程提供了新途径。它们能够：

* • 从有限的观测数据（如平面粒子图像测速数据）中重建三维钝体尾流场的完整速度和压力场。
* • 模拟涉及激波的高速可压缩流动，即使在没有完整边界条件信息的情况下，也能利用密度梯度、表面压力等数据进行反演。
* • 应用于生物医学流体力学，如模拟血流动力学、估计血管壁剪切应力以及预测患者特定动脉网络中的脉搏波传播。

#### 固体力学

在固体力学中，PINN已成功应用于线性弹性、弹塑性、超弹性和断裂力学等问题。

* • 对于正问题，PINN能在给定输入下预测材料响应，在线性弹性动力学等问题上表现出比有限差分法和有限元法更高的精度和效率。
* • 对于反问题，PINN可用于识别本构方程参数或几何拓扑结构。

#### 电磁学与光学

PINN已被扩展用于求解光学和电磁学问题，如三维亥姆霍兹方程和拟线性PDE算子。

* • 在纳米光学和光子超材料领域，PINN被用于解决反散射问题，例如从涉及多个相互作用纳米结构或多元纳米粒子的散射系统中反演有效介电常数参数。

### 开源软件与工具

为了方便研究人员实现PINN，多个开源框架和库已被开发出来：

* • **DeepXDE**：一个专门用于使用PINN求解微分方程的开源Python库，提供高级接口，支持TensorFlow、PyTorch和JAX后端。
* • **IDRLnet**：一个用于通过PINN系统建模和求解问题的Python工具箱，提供了集成几何对象、数据源、神经网络、损失度量和优化器的结构化方式。
* • **NeuroDiffEq**：一个基于PyTorch的开源库，用于使用神经网络求解微分方程，提供灵活的用户自定义问题接口。
* • **SciANN**：一个基于Keras和TensorFlow构建的高级神经网络API，专为科学计算设计，便于将科学问题表述为深度学习任务。
* • **TensorDiffEq**：一个构建在TensorFlow之上的Python包，专注于为PINN提供可扩展高效的求解器，并完全支持自适应PINN求解器和多GPU计算。

### 挑战与未来展望

尽管PINN取得了显著成功，但仍面临一些挑战：

1. 1. **理论与理解**：PINN的泛化能力、鲁棒性以及“梯度病理”等问题需要更深入的理论分析。梯度病理源于数值刚性导致的反向传播梯度失衡，阻碍网络同时准确满足PDE约束和边界条件。
2. 2. **优化与训练**：传统优化器在处理具有快速变化或高频解的问题时可能收敛缓慢或效果不佳。针对PINN特点设计新的优化算法（如更复杂的损失函数、分层模型、高级优化策略）至关重要。
3. 3. **数据处理**：高效处理噪声或不全数据的能力仍需提升。多尺度、多物理场问题的可扩展性也是一个挑战。
4. 4. **数据与模型**：高质量实验数据集以及与之对应的精确、高效可计算的物理模型和参数的开发仍然匮乏，这限制了PINN在实际问题中的应用。

**未来方向：算子学习**  
一个重要的未来趋势是从PINN转向深度算子学习。与PINN侧重于求解特定PDE不同，算子学习旨在直接学习支配物理系统的底层算子（即输入函数到输出函数的映射）。这有望产生更具通用性的模型，无需显式的物理约束即可应用于更广泛的物理问题。未来的研究需要开发更鲁棒的训练算法以高效学习高维算子映射，并探索在数据稀疏或噪声情况下的数据驱动与物理模型集成，同时提高模型的可解释性。

### 结论

物理信息神经网络通过将物理定律直接嵌入神经网络的损失函数，为求解偏微分方程架起了传统数值方法与现代机器学习技术之间的桥梁。本文综述了PINN在理论基础、架构创新、性能提升技术、广泛应用以及软件工具等方面的最新进展。尽管在收敛精度、高维非线性问题处理等方面仍面临挑战，但通过持续的研究，特别是在算子学习等新兴范式上的探索，PINN有望进一步扩展其适用性，提升其可扩展性、可解释性和可靠性，从而继续推动科学发现和工程实践的进步。

**参考文献**:  
Luo, K., Zhao, J., Wang, Y., Li, J., Wen, J., Liang, J., Soekmadji, H., & Liao,
S. (2025). Physics-informed neural networks for PDE problems: a comprehensive
review. Artificial Intelligence Review, 58, 323.
https://doi.org/10.1007/s10462-025-11322-7

> **本平台免费推广｜科研论文｜期刊征稿｜国内外会议通知｜招生宣传｜ 请加微信cgx123me  
> 本平台付费合作服务｜商务推广｜深度学习代码定制｜科研图片代绘制｜科研合作等｜请加微信cgx123me**

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 09:13*