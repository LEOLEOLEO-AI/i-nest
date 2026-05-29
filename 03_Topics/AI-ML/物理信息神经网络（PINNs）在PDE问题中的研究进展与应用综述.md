---
title: "物理信息神经网络（PINNs）在PDE问题中的研究进展与应用综述"
source: "https://mp.weixin.qq.com/s/f7XKFZqvU63CBZuGk369vw"
created: 2025-09-11
note_id: "1887156687601769832"
tags:
  - "AI链接笔记"
  - "物理信息神经网络（PINNs）"
  - "偏微分方程（PDEs）"
  - "科学计算"
  - "get-笔记"
  - "AI研究"
---

# 物理信息神经网络（PINNs）在PDE问题中的研究进展与应用综述

## 摘要

🔬 **研究背景与意义**   偏微分方程（PDEs）是刻画物理现象的核心工具（如热传导、流体动力学），传统数值方法（FEM、FVM等）在高维问题中受限。物理信息神经网络（PINNs）通过将物理定律嵌入神经网络架构，融合领域知识与数据驱动方法，为求解复杂PDE问题提供了变革性框架。  📌 **PIN

## 正文

**点击蓝字，立即关注**

![1757511428964(1).png](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fba3ee325ee71dfa6ea00e95a7cdd2874?Expires=1780067375&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=g8%2B6iD4ZInXFaIUmwq8vPqgFqnQ%3D)

**摘要**

## 

随着“人工智能促进科学研究”（AI for Science）的不断发展，物理信息神经网络（Physics-informed Neural Networks, PINNs）已在科学计算与深度学习领域中展现出变革性作用。PINNs 提供了一种稳健而灵活的框架，用于求解偏微分方程（PDEs）及其他复杂物理系统。其核心思想是将物理定律直接嵌入神经网络架构中，从而融合领域知识，确保模型在拟合数据的同时满足已知物理规律。**本文全面综述了 PINNs 在 PDE 问题中的最新进展与应用，重点介绍了 PINN 架构、数据重采样方法、损失与激活函数、特征嵌入方法等。此外，文章还讨论了 PINNs 的潜在未来方向及预期发展。本文旨在为 PDE 问题的 PINN 研究提供有价值的见解，期望能推动这一前沿方向的进一步探索。**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7980cbf8e13997801dc14788ea60dced?Expires=1780067375&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=MVbqfBpzM0bXRF96kgrGdWmnzPU%3D)

---

---

**0****1**

**研究背景与意义**

**在科学与工程领域，偏微分方程（PDEs）是刻画物理现象的重要工具，例如热传导、流体动力学、波动传播等。传统数值方法包括有限元法（FEM）、有限体积法（FVM）、有限胞元法（FCM）等，但在高维复杂问题上往往受到限制。随着深度学习的发展，物理信息机器学习（PIML）逐渐兴起，其中 PINNs 成为一种高效求解 PDE 的方法。PINNs 将 PDE 及其边界、初始条件直接融入损失函数，通过自动微分优化网络参数，实现“数据—物理”融合.**

![1757512546074(1).png](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3e5dc9c70ed035779899a4f869af928f?Expires=1780067375&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=CLxVuDMgzwYkfQH5W%2B0Zv%2FELv3g%3D)

---

**0****2**

**PINNs 的基本框架**

**PINNs 的基本思想是利用神经网络近似 PDE 的解。其损失函数由两部分组成：**

* **物理约束项**（L\_physics）：保证 PDE、边界条件和初始条件成立；
* **数据项**（L\_data）：拟合观测数据。

综合损失形式为：

L = L\_physics + L\_data

这种方法的优势在于，即使数据稀缺或存在噪声，PINNs 仍能依靠物理约束保持稳定。性能评价指标包括 **L2 相对误差、均方根误差（RMSE）、PDE
残差**等。

![1757512366540.png](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1ca4d026dfedeb94d3a00641017c6f29?Expires=1780067375&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=%2BOPiTlmT3wYQmR3qkDa1JZ9Els0%3D)

---

**0****3**

**PINN 的主要研究进展**

**1. 网络架构（见 Table 2）**

* **MLP（多层感知机）**：最早使用的 PINN 框架（Raissi et al., 2019）。
* **CNN（卷积神经网络）**：如 PhyGeoNet，适合不规则几何域。
* **RNN（循环神经网络）**：例如 PhyCRNet，处理时空 PDE 问题。
* **GAN（生成对抗网络）**：PI-GANs 解决随机 PDE 问题。
* **KAN（Kolmogorov–Arnold 网络）**：在多尺度与非线性 PDE 上展现潜力。
* **Transformer**：如 PINNsFormer、Transolver，用于高维复杂几何 PDE。
* **其他框架**：NAS-PINN、SPINN、PirateNets 等。

![1757512698517(1).png](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3604b5479343e5150b0fcec02f6fb98c?Expires=1780067375&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=rIURqG6bJgVDqh7ul5e3A%2BK2AIg%3D)

**2. 域分解方法（见 Fig.9）**

将复杂区域拆分为多个子域，可提升计算效率并便于并行训练：

* XPINNs：空间与时间同时分解；
* cPINNs：确保守恒律连续性。

![1757512801308(1).png](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1d5ce048b449c31a00f39b7521a83c7e?Expires=1780067375&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=osXolQP5R5MhOeCTa8Qn5NrM648%3D)

**3. 激活函数**

研究者提出了多种新型激活函数：

* 自适应激活函数；
* 物理驱动激活函数（PAFs）；
* 基于核函数的 PIKFNNs。

  这些方法在收敛速度和精度上优于传统 tanh、ReLU。

**4. 数据重采样策略（见 Fig.10）**

PINNs 的性能高度依赖采样点分布。自适应采样方法（如 RAR、RAR-D、R3、DAS-PINNs、DMIS、GAS、PINNACLE、AAS
等）通过在高残差区域增加采样点，显著提升训练效率与准确性。

![1757512852840.png](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe9169c5c4b55692264911b5b1e538af4?Expires=1780067375&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=7vU%2F6XIf6Ir6tEzO%2BZnrRn8QEw8%3D)

**5. 损失函数设计**

* **再加权方法**：如 lbPINNs、SelectNet、SA-PINNs、LA-PINN，解决不同损失项收敛速度不一致。
* **新型损失函数**：如 gPINNs 将 PDE 残差的梯度也纳入约束，提高对 PDE 解的光滑性逼近能力。

---

**0****4**

**PINNs 的应用场景**

**PINNs 在多个学科展现出应用前景：**

* **流体力学**：湍流建模、Navier–Stokes 方程求解；
* **气候与地球科学**：天气预报与气候建模；
* **量子物理**：薛定谔方程求解与量子态预测；
* **材料与力学**：裂纹扩展、非线性材料行为模拟；
* **生物医学**：扩散与传输过程建模。

例如，CNN-PINNs 在 Navier–Stokes 方程中收敛更快；Transformer-PINNs 在复杂几何 PDE 上表现优于传统 PINNs。

---

**0****5**

**挑战与未来方向**

**当前 PINNs 的挑战包括：**

1. **高维问题的计算开销**：维度升高带来训练资源瓶颈；
2. **损失函数权重平衡难题**：不同约束项的重要性难以合理设定；
3. **收敛与稳定性问题**：可能陷入局部极小值或出现梯度病态；
4. **泛化能力不足**：对复杂几何与未知边界条件的适应性有限。

**未来方向包括：**

* 与算子学习（operator learning）结合；
* 融合自适应网格技术；
* 优化训练算法与新型激活函数；
* 借助高性能计算（GPU/TPU）进一步提升规模与效率。

---

**结论**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd2f46cd2dbd1cef8635b2caa1d9118a8?Expires=1780067375&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=l1cFAF9bwPziKnMSfosLnLXSCWU%3D)

本文全面综述了物理信息神经网络（PINNs）在偏微分方程问题中的最新研究进展。PINNs 将深度学习与物理约束相结合，为求解复杂 PDE 提供了新范式。本文总结了不同的 PINN 架构、采样策略、损失函数设计及特征嵌入方法，并分析了其在流体力学、量子物理、材料科学、生物医学等领域的应用。尽管 PINNs 在多个场景中展现出优势，但仍存在计算成本高、收敛不稳定和泛化能力不足等挑战。未来 PINNs 有望与算子学习等新兴方法结合，进一步提升效率与适用性。总体而言，PINNs 代表了 AI for Science 领域中极具前景的一条研究路径，为解决复杂 PDE 问题和推动科学发现提供了新的可能。

---

DOI:10.1007/s10462-025-11322-7

本推文仅对原文献进行简要分享，研究团队的相关信息已在开头注明，如有侵权或信息不准确之处，请通过后台联系。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0729ef0d9d43a0484fd15fc0c14c7828?Expires=1780067375&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=rMCLYc6hWSXd7n9MUyeQGI60EE4%3D)

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 11:09*