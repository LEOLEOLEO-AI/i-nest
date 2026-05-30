---
title: "物理信息神经网络（PINNs）研究综述：从理论框架到科学计算革命"
source: "https://mp.weixin.qq.com/s/OKY4hQCcwbEnQE-eO6NXyg"
created: 2025-12-05
note_id: "1895033079949581520"
tags:
  - "AI链接笔记"
  - "物理信息神经网络（PINNs）"
  - "偏微分方程求解"
  - "科学计算第四范式"
  - "get-笔记"
  - "AI研究"
  - "重要"
---

# 物理信息神经网络（PINNs）研究综述：从理论框架到科学计算革命

## 摘要

### **🔬 核心概念与科学意义**  **定义**：物理信息神经网络（Physics-informed neural networks, PINNs）是一种**融合物理定律与深度学习**的计算范式，通过将偏微分方程（PDEs）、初始条件（IC）和边界条件（BC）编码进损失函数，实现数据驱动与物理

## 正文

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F17c723df432fbc5eb74bcf67ded7f4b8?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ZsEoEfkIJV1KaZZGGFfbtPv8l8w%3D)

**AI4PDE****｜综述 · 论文推荐**

AI for Science｜Review｜第八期

**物理信息神经网络**

**在偏微分方程问题中的应用：全面综述**

Physics-informed neural networks for PDE problems: a comprehensive review

**通讯作者：Shaolin Liao**

**作者单位:**中山大学电子与信息工程学院

Artificial Intelligence Review

**综述范围：**

**涵盖了从1990年代早期尝试到2025年的最新进展，引用文献约160篇。内容囊括PINN的基础理论、多样化架构（MLP, CNN, RNN, GAN,
Transformer, KAN）、数据重采样技术、损失函数优化、特征嵌入方法以及在流体、固体力学等领域的应用。**

**论文链接：**

**https://link.springer.com/article/10.1007/s10462-025-11322-7**

**PDF 下载 ↓**

**https://www.jianguoyun.com/p/Df-woHoQ7P3jDRjttZsGIAA**

点击打印论文信息

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F57eebd54872766d45af10f4732d12861?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=FmJDzIbSEh2pRV4X%2BSh3sKHLdDg%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbf612be9540de8e1c05b633843e31cfb?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=12183p08JAtWlEUOpXIvIhSuuvQ%3D)

Published 2025-07

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1934f1c1b64716367e2a473a26ae0623?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=WOIMRJkt6iMsrkSP2KJ8p1mzyuc%3D)

在科学探索的漫长历史中，我们习惯于依靠理论推导和实验验证来认识世界。随着计算机的出现，数值模拟成为了第三大支柱。而现在，**一种融合了物理定律与深度学习的全新范式——物理信息神经网络（PINNs），正试图打破数据与原理之间的壁垒**，为解决复杂的物理系统问题提供前所未有的灵活性

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F04dc8c4c5a7c502c53958c5738c77a73?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=mx1fsDz8EtRwdpGJe4qxLGSSWDk%3D)

**缘起与原理：当神经网络学会物理**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1e90abc638b56904f8b85f4253ba2dac?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=XInzvAvbnqj1Itxl6mB1XW2hoqw%3D)

让我们先回到故事的起点，看看仅仅依靠数据的神经网络，是**如何一步步学会“遵守物理定律”的**。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2cCt50ZycQ2%2F%2Bhv4AWXYb2kOml0%3D)

**从黑盒到物理感知（1994-2019）**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2cCt50ZycQ2%2F%2Bhv4AWXYb2kOml0%3D)

早在20世纪90年代，Dissanayake等人就开始尝试用神经网络求解偏微分方程（PDE），但**受限于当时的算法和算力**，这些尝试并未引起巨大反响。

**真正的转折点发生在2019年，Raissi等人正式提出了PINN模型**。不同于传统深度学习仅依赖标签数据，PINN的创新在于它将物理方程（PDEs）、初始条件和边界条件直接编码进了损失函数中。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F2144fa62060289acc45662a6cafd3470?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=E995nf8%2BEqn0yi11zXle8xiREXg%3D)

这意味着，**网络在训练过程中不仅要拟合观测数据，还要接受物理定律的“惩罚”**——如果预测结果违背了物理方程，Loss就会变大。这种机制让PINN在数据稀缺甚至无标签的情况下也能通过自动微分技术求解复杂问题。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F66efc16a4f195d5ed12bbbdd2d70888f?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=oi3U0djCJEM1zCiOZ%2FPQiHYTNvM%3D)

**有了核心理念，为了应对不同类型的物理问题，PINN的“大脑”结构也在不断进化。**

**架构演进：为物理问题定制大脑**

标准的神经网络并不总是最适合求解PDE的。为了提高精度和效率，**研究者们引入了多种先进的架构。**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbf33d006fa85ee80067e4fce7b30786c?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=f4MUoag%2BqsCL7JW2%2Bt2%2FJNk6bUg%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2cCt50ZycQ2%2F%2Bhv4AWXYb2kOml0%3D)

**经典与变体：CNN与RNN的跨界**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2cCt50ZycQ2%2F%2Bhv4AWXYb2kOml0%3D)

最基础的PINN使用的是**多层感知机（MLP）**，但在处理特定问题时显得力不从心。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3bf8e0eef14903ee14f0675ad96767ef?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=TzqqX8EK%2FF63C4pvxChJvydbySU%3D)

于是，擅长处理网格数据的**卷积神经网络（CNN）**被引入。2021年，Gao等人提出的**PhyGeoNet**是一个里程碑：它通过椭圆坐标映射将不规则几何变换为规则域，使得标准CNN得以应用。在球面上求解PDE时，Lei等人开发的**PICNN**（Physics-Informed
CNN）展现了优异性能，甚至建立了理论误差界。最近，Yuan等人提出的**f-PICNN**进一步将CNN扩展到时空域，通过非线性卷积单元和记忆机制处理具有剧烈梯度的多尺度PDE。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbf53ce88a47d29fa42f5b3174637d3d9?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=rIaW%2FjaoVz3pZmcFFlpY4LeyC1s%3D)

这些工作表明，CNN不仅能处理图像，也能成为强大的PDE求解器，特别是在规则几何上。

对于时间依赖问题，**循环神经网络（RNN）**及其变体（如LSTM）展现了优势。**PhyCRNet**结合了卷积和循环网络，无需标签数据即可高效求解时空PDE
。此外，基于生成对抗网络（GAN）的**PI-GANs**也被用于处理随机微分方程和不确定性量化问题。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fdc44b064503b1ed19d01ca2c30aeff8d?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=z0zluZ6Fm6MFnPI27XlZDRV6Q2o%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2cCt50ZycQ2%2F%2Bhv4AWXYb2kOml0%3D)

**前沿架构：KAN与Transformer的加入**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2cCt50ZycQ2%2F%2Bhv4AWXYb2kOml0%3D)

近年来，更前沿的架构开始崭露头角。基于柯尔莫哥洛夫-阿诺德表示定理的**KAN网络（Kolmogorov-Arnold
Networks）**，通过在边上而非节点上设置激活函数，提供了更好的可解释性和精度，甚至能发现物理公式。另一方面，**Transformer架构**也被引入PDE求解。例如，**PINNsFormer**利用多头注意力机制捕捉长距离依赖，显著提升了泛化能力；

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbfb3ac75cd167d9699a160c1b8e21f32?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=kw%2FUmEtYG9fx9lV8JztpdkuyIOo%3D)

而Transolver则通过PhysicsAttention机制，在线性复杂度下处理复杂几何上的PDE。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe34450a6cda03011521263587cf70496?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=4Hx71Zq4a3wP6i4zgbN1KrSDq2s%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F66efc16a4f195d5ed12bbbdd2d70888f?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=oi3U0djCJEM1zCiOZ%2FPQiHYTNvM%3D)

**拥有了强大的架构还不够，如何让网络在训练中“关注”到重点区域，是提升效率的关键。**

**训练策略：自适应采样与损失平衡**

在物理场中，剧烈变化的区域（如激波）往往最难拟合。**如何让PINN“聪明”地分配注意力？**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2cCt50ZycQ2%2F%2Bhv4AWXYb2kOml0%3D)

**自适应重采样：好钢用在刀刃上**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2cCt50ZycQ2%2F%2Bhv4AWXYb2kOml0%3D)

传统的固定采样点往往效率低下。Lu等人提出的**RAR**（Residual-based Adaptive
Refinement）方法是**自适应采样**的先驱，它会在PDE残差大的地方自动增加采样点。此后，RAD、DAS-PINNs等方法进一步结合了概率密度函数和生成模型，**动态调整采样分布，确保网络专注于难以学习的区域。**作者团队提出的混合自适应（HA）采样方法，平衡了随机性和残差导向，进一步提升了精度。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2cCt50ZycQ2%2F%2Bhv4AWXYb2kOml0%3D)

**损失函数工程与特征嵌入**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2cCt50ZycQ2%2F%2Bhv4AWXYb2kOml0%3D)

PINN的损失函数包含多个项（PDE残差、边界条件等），它们之间的数量级差异可能导致训练失败。**自适应权重**（如Loss
Reweighting）技术应运而生，动态调整各项的权重以平衡训练。此外，为了解决“频谱偏差”问题（神经网络倾向于先学习低频特征），**研究者引入了傅里叶特征嵌入（Fourier
feature embedding），帮助网络捕捉高频、多尺度的物理细节。**gPINNs更是将梯度的导数也加入损失函数，显著提升了平滑度。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F66efc16a4f195d5ed12bbbdd2d70888f?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=oi3U0djCJEM1zCiOZ%2FPQiHYTNvM%3D)

**这些理论和技术的进步，最终都要在实际应用中接受检验。**

**应用版图：从流体到光子**

PINN不仅停留在论文中，它正在流体力学、材料科学等多个硬核领域解决传统方法难以处理的问题。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2cCt50ZycQ2%2F%2Bhv4AWXYb2kOml0%3D)

**流体与生物医学**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2cCt50ZycQ2%2F%2Bhv4AWXYb2kOml0%3D)

在流体力学中**，PINN被用于求解纳维-斯托克斯方程（NSE）**，特别是在只有部分观测数据的情况下重建流场（如圆柱绕流的压力场重建）。在生物医学领域，**PINN被用于模拟血液动力学**，通过MRI数据无创预测动脉血压和壁面剪切应力，这是传统CFD难以做到的。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fddf7052b5151f714b3fa5f55f76ef76f?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=GmUooBFiLl1ooz1gnb8TgP90r70%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2cCt50ZycQ2%2F%2Bhv4AWXYb2kOml0%3D)

**固体力学与电磁学**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2cCt50ZycQ2%2F%2Bhv4AWXYb2kOml0%3D)

**在固体力学方面**，PINN成功应用于线弹性、弹塑性甚至断裂力学问题，能够反演材料的本构方程。**在电磁学和光学领域**，PINN被用于设计光子超材料和纳米光学器件，解决了复杂的逆散射问题，帮助研究者反推纳米结构的介电常数参数。

**挑战与机遇：未解之谜与未来之路**

尽管战果累累，但PINN的发展并非一帆风顺，前方仍有迷雾。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2cCt50ZycQ2%2F%2Bhv4AWXYb2kOml0%3D)

**当前挑战**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2cCt50ZycQ2%2F%2Bhv4AWXYb2kOml0%3D)

PINN面临的核心挑战可以归结为三类。

**①理论挑战：**我们仍然缺乏对PINN收敛性和误差界的深入理解。Krishnapriyan等人发现的‘梯度病理’问题——即不同损失项的梯度在训练过程中出现不平衡——至今没有得到根本解决。

**②实践挑战：**PINN对超参数极其敏感，网络架构、学习率、损失权重等都需要精心调节，这限制了它的易用性。对于高频、多尺度问题，PINN往往难以捕捉到精细结构。

**③应用挑战：**真正的多物理耦合问题、三维实际问题、长时间演化等，都对当前PINN提出了超出能力范围的要求。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2cCt50ZycQ2%2F%2Bhv4AWXYb2kOml0%3D)

**新兴方向：从PINN到算子学习**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2cCt50ZycQ2%2F%2Bhv4AWXYb2kOml0%3D)

面对这些挑战，研究者们开始思考更根本的解决方案。一个激动人心的新方向是「**算子学习」**（Operator Learning）。

与传统PINN学习特定PDE的解不同，算子学习试图学习PDE解算子本身——即从输入函数到输出函数的映射。Lu等人的DeepONet和Santos等人的PIT都是这一方向的先驱。这种方法的优势是泛化性：**一旦学会了某个物理系统的算子，就能快速预测不同输入条件下的解，而无需重新训练。**这类似于人类物理学家掌握物理定律后，能预测各种情况下的系统行为。

从PINN到算子学习，标志着从「解题」到「学规律」的范式升级。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F905fea7c267485446d31337686aeb858?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=gLfHF3wT0qVd5m81UF2VsP7cWEU%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2cCt50ZycQ2%2F%2Bhv4AWXYb2kOml0%3D)

**结束语**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2cCt50ZycQ2%2F%2Bhv4AWXYb2kOml0%3D)

站在2025年的时点回望，**PINN已经从一个学术概念成长为解决实际科学问题的有力工具。**展望未来，随着理论基础的夯实、技术生态的完善、应用领域的拓展，**PINN有望成为科学计算的主流方法之一。**更重要的是，它代表了AI
for
Science的核心范式：**不是让AI取代物理定律，而是让AI在尊重物理的前提下增强我们的科学发现能力。**在这个人工智能与科学研究深度融合的时代，**PINN的故事才刚刚开始。**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F04dc8c4c5a7c502c53958c5738c77a73?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=mx1fsDz8EtRwdpGJe4qxLGSSWDk%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F66efc16a4f195d5ed12bbbdd2d70888f?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=oi3U0djCJEM1zCiOZ%2FPQiHYTNvM%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd757d42b1b97b77a0b64f19cf9cd55a1?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=62E%2B3pvQhbGDO4yfAgZ%2F8rR8PFM%3D)

**# 启示与讨论>>**

**你认为PINNs最终会取代传统数值方法，还是与之互补共存？**

**① 架构决定上限：**针对不同物理问题（如多尺度、长时依赖），选择合适的架构（如KAN, Transformer）至关重要

**② 采样即训练****：**自适应重采样技术（如RAR, HA）能显著提升训练效率，解决难点区域的拟合问题

**③ 优化即核心：**解决梯度病态和频谱偏差（通过特征嵌入和损失加权）是保证PINN收敛的关键

**④ 工具生态：**DeepXDE、SciANN等开源工具的成熟，极大地降低了PINN的应用门槛

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc1e0aac78cc4af106f9136b27d7ffab6?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=aY2g0cDn17AFn%2FrJ6zGY1%2FLyUN0%3D)

***声明：本系列推文仅代表个人解读与观点，******旨在抛砖引玉，不代表研究团队立场。******若内容涉及版权或事实错误，欢迎通过后台指正。***

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe9fed27d8e244b76bd2a8639dd7425e7?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=s4wX3wKjcWbCcSVRc5i90Cjhmng%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc5818a1fd7701f607c1df8634974c2e4?Expires=1780063519&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=7cYy%2B0hPN84sES3d2ftTZbf%2BnsA%3D)

关注**智核学术｜**少走弯弯路

**↙↙↙  点击下方 “阅读原文”  查看相关论文合集**

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 10:05*

## Related Notes

- [[AI编码代理的质的飞跃：v3.3透明化与v3.4连续性技术解析]]
- [[FMPINN：基于傅里叶的混合物理信息神经网络求解多尺度椭圆PDEs]]
- [[Ψ-NN：通过知识蒸馏自动发现物理信息神经网络结构的新方法]]
