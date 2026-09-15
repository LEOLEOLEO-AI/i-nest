---
direction: both
category: 理论
tags: [PhyDNet, 视频预测, 物理先验, PDE, ConvLSTM, 解耦表示, 卡尔曼滤波]
summary: "PhyDNet将物理动力学与残差信息在潜空间解耦的视频预测模型"
quality: high
processed: 2026-09-15 08:13
---
---
title: "PhyDNet 深度解析：把物理规律和神经网络拆开用的视频预测模型"
tags:
  - paper
  - neuroscience
  - neural
  - research
  - network
  - first-principles
  - architecture
  - design
  - physics
date: 2026-09-13 07:18
source: GetNotes
score: 10
---

## Original Note

---
note_id: 1920968219565241984
title: "PhyDNet 深度解析：把物理规律和神经网络拆开用的视频预测模型"
type: link
created: 2026-09-10 19:51:08
source: getnote
kb: 
---

# PhyDNet 深度解析：把物理规律和神经网络拆开用的视频预测模型

### 🌱 这篇文章在讲什么核心问题？

**物理驱动 vs 数据驱动**的矛盾，是视频预测领域的核心痛点。
- **任务本质**：给过去若干帧二维图像 → 推演未来几帧，和降水临近预报高度相似。
- **经典做法**：把雷达/降水图输入 **ConvLSTM、ConvGRU** 等网络，让模型自己学时空演变。
- **灵魂拷问**：真实运动本来受物理规律控制，为什么神经网络要从零开始"猜"？
- **主角登场**：**2020年 CVPR**，Vincent Le Guen 和 Nicolas Thome 提出 **PhyDNet**（Physical Dynamics Network）。

### 🧠 PhyDNet 之前，两条路线各有什么问题？

纯数据驱动和纯物理约束**各有短板**，谁都没法单独搞定现实问题。

| 路线 | 优点 | 缺点 |
| :--- | :--- | :--- |
| 纯深度学习（ConvLSTM 等） | 什么都能学 | 什么都得学，物理规律隐式藏在参数里 |
| 纯物理约束（PDE 方法） | 有先验、参数少、可解释 | 现实世界不完全服从简单物理模型 |
- **数据驱动代表**：ConvLSTM → PredRNN、Causal LSTM、MIM、E3D-LSTM 等时空 RNN。
  - 说白了，ConvLSTM 不知道"平流方程"是什么，只能看大量样本后自己总结"这种形状下一帧常往东北挪一点"。
- **物理驱动代表**：PDE-Net 等，利用**卷积核可近似微分算子**的特性，把 PDE 数值离散和卷积网络结合起来。
  - 已有物理约束方法的前提：**物理规律明确已知** + **系统状态能被完全观测** → 一般视频预测不满足。

### 💡 PhyDNet 的核心思路是什么？

**物理部分交给物理，残差部分交给 AI**，两者在潜在空间里相加。
- **核心假设**：潜在空间 H 中，系统状态 h = hᵖ（物理分量） + hʳ（残差分量）。
- **变化拆分**：∂h/∂t = Mₚ(hᵖ, u) + Mᵣ(hʳ, u) → 物理能解释的变化 + 解释不了的变化。
- **为什么不在原始图像上套 PDE**：像素空间不是物理方程最适合工作的地方，单个像素值≠完整物理状态变量。
  - 所以 PhyDNet 先通过 Encoder 把图像映射到**潜在空间 Latent Space H**，让模型自己找一个适合 PDE 工作的特征空间。

### 🏗️ PhyDNet 的整体架构长什么样？

**Encoder → 双分支循环单元 → 相加 → Decoder**，是典型的 seq2seq 结构。
- **流程链路**：输入图像 u_t → Encoder E → E(u_t) → 分两路进入 PhyCell 和 ConvLSTM → 得到 hᵖ_(t+1) 和 hʳ_(t+1) → 相加得 h_(t+1) → Decoder D → 预测下一帧 û_(t+1)。
- **关键设计**：两条分支**不是各出一张图再平均**，而是在 latent space 先相加，再统一 Decoder 重建。
- **多步预测**：预测阶段只有 ConvLSTM 分支会把上一步预测结果回灌当输入，PhyCell 分支不回灌。

### ⚙️ 左边的 PhyCell 具体是怎么工作的？

PhyCell 采用**预测—校正（Prediction → Correction）**结构，借鉴了资料同化思想。

#### 第一步：Prediction（物理先往前走一步）
- **公式**：h̃_(t+1) = h_t + Φ(h_t) → 当前状态 + 物理动力项 = 背景预测。
- **Φ 是什么**：一类通用线性 PDE，是各阶空间偏导数的加权和（i+j ≤ q 阶）。
  - 一阶导数 → 对应平流特征
  - 二阶导数 → 对应扩散特征
  - 更高阶项 → 描述更复杂空间变化
  - 可覆盖热方程、波动方程、平流—扩散方程等经典形式。
- **怎么算偏导数**：用**可学习卷积核**近似不同阶微分算子，再用 **1×1 Conv** 学习各阶项的权重 c_ij。
  - 说白了，就是让卷积网络自己学"哪个物理项重要、权重多大"，比手工固定微分核更灵活。

#### 第二步：Correction（用新观测修正一下）
- **公式**：h_(t+1) = (1-K_t)·h̃_(t+1) + K_t·E(u_t) → 物理预测和观测输入按比例融合。
- **K_t 的作用**：模型学习出的门控量，类似**卡尔曼增益（Kalman Gain）**，决定相信物理还是相信数据。
  - K_t = 0 → 完全相信物理预测
  - K_t = 1 → 完全相信当前观测
- 这种门控机制在功能上和 LSTM/GRU 的 gating 有相似之处。

### 🤖 右边为什么还要放一个 ConvLSTM？

**不是所有东西都该硬塞进 PDE**，细节和纹理交给 ConvLSTM 更合适。

| 分支 | 负责内容 |
| :--- | :--- |
| PhyCell | 结构、位置、动力演变、物理规律 |
| ConvLSTM | 物理模型解释不了的细节、纹理、残差信息 |
- **例子（Moving MNIST）**：PhyCell 主要捕捉数字的**粗略位置**，ConvLSTM 捕捉数字的**精细形状**（笔画、边缘、纹理）。
- **定位**：PhyDNet 不是"用物理替代深度学习"，而是让物理先验和数据驱动模型**各干自己擅长的事**。

### 🔮 论文最后提到了哪些未来方向？

未来可从**数值格式**和**预测类型**两方面继续扩展。
- **数值离散升级**：把简单的 Euler 离散升级到 **Runge–Kutta** 等更复杂的数值格式。
- **预测类型扩展**：进一步扩展到带不确定性的**概率预测**。

### 📝 补充细节
- **论文信息**：V. Le Guen and N. Thome, "Disentangling Physical Dynamics From Unknown Factors for Unsupervised Video Prediction," 2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), Seattle, WA, USA, 2020, pp. 11471-11481, doi: 10.1109/CVPR42600.2020.01149.
- **正式名称**：论文将这种设计称为 **physical dynamics 与 residual information 的解耦**。
- **降水场景对应**：降水回波的位置变化可部分用平流解释，但强度变化涉及水汽输送、辐合、垂直运动、微物理、对流发展、地形影响等，难以用简单 PDE 全部解释。

---
*getnote | 2026-09-13 07:17*


---

## Related Notes

[[paper1_iNEST_core_architecture]]
[[iNEST-MOC]]
[[Papers-MOC]]
