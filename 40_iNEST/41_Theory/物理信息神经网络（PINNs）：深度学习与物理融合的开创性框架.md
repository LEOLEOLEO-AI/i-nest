---
title: "物理信息神经网络（PINNs）：深度学习与物理融合的开创性框架"
source: "https://mp.weixin.qq.com/s/X_ze-6RI4ZBRbVuXWqqV6Q"
created: 2025-10-20
note_id: "1890812602418829792"
tags:
  - "AI链接笔记"
  - "物理信息神经网络（PINNs）"
  - "偏微分方程（PDE）"
  - "AI for Science"
  - "get-笔记"
  - "学术论文"
---

# 物理信息神经网络（PINNs）：深度学习与物理融合的开创性框架

## 摘要

🔬 **论文核心信息**   - **标题**：Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear parti

## 正文

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F17c723df432fbc5eb74bcf67ded7f4b8?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=4tL3Jt7BHXJZgVUA3Jn%2BilHjG7w%3D)

**PINNs****｜精选 · 论文推荐**

AI for Science｜第一期

**物理信息神经网络：解决涉及非线性偏微分方程的****正向和逆向问题的深度学习框架**

Physics-informed neural networks: A deep learning framework for solving forward
and inverse problems involving nonlinear partial differential equations.

**第一作者：M. Raissi**

**作者单位：**美国布朗大学应用数学系

Journal of Computational Physics

**论文主页：**

**https://www.sciencedirect.com/science/article/pii/S0021999118307125?via%3Dihub**

**论文｜PDF 下载 ↓**

**https://www.jianguoyun.com/p/DYjCwXIQ7P3jDRiTrpUGIAA**

点击打印论文信息

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F57eebd54872766d45af10f4732d12861?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=j8TpLbT9IK8a18OTmReqa%2BUGJik%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbf612be9540de8e1c05b633843e31cfb?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=gfEv24%2BPpiy7E9BYKI6t4oevsBQ%3D)

Published 2019-02

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1934f1c1b64716367e2a473a26ae0623?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=dWS4vzJv0yXTbLr8WGBph41W1%2B0%3D)

当传统数值方法遇到复杂偏微分方程时，往往需要精细的网格划分和巨大的计算成本。**布朗大学Raissi团队在计算物理顶刊JCP上提出的物理信息神经网络(PINN)**，通过将物理定律直接嵌入神经网络训练过程，实现了用少量数据精准求解复杂方程。这项研究不仅为科学计算带来新范式，更**开启了深度学习与数学物理深度融合的新时代。**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F04dc8c4c5a7c502c53958c5738c77a73?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=%2Fd7IhHHsp0siZuVQaUqxlBsskU0%3D)

**研究背景 · 问题意识**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4ac6242623a1c73e4b64916214da8bbb?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=kWTzUtnZ%2FaActcy5wqse2k0JRZ4%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vdsEa5EuWshxUV6kdjtNOtV7UA8%3D)

**研究背景**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vdsEa5EuWshxUV6kdjtNOtV7UA8%3D)

偏微分方程(PDE)是描述自然界物理现象的数学语言，从天气预报到材料设计都离不开它。**传统数值方法需要对时空进行精细网格划分，计算成本高昂**。而深度学习虽然在图像识别等领域表现出色，但面对物理问题时往往需要海量数据，缺乏对物理规律的理解。

近年来，机器学习在科学计算领域的应用面临两大挑战：

一是**数据稀缺问题**——在物理实验和工程中，获取数据往往代价高昂，传统深度学习的"大数据"假设难以满足；

二是**可解释性困境**——黑箱模型无法保证预测结果符合基本物理定律(如质量守恒、能量守恒)，导致在安全关键领域难以应用。更关键的是，物理系统中蕴含的大量先验知识(如物理方程、对称性、守恒律)在传统机器学习中被白白浪费。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vdsEa5EuWshxUV6kdjtNOtV7UA8%3D)

**问题意识**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vdsEa5EuWshxUV6kdjtNOtV7UA8%3D)

核心问题是，**如何让神经网络在学习数据的同时，自动满足已知的物理定律**？传统方法要么纯数值求解(忽略数据)，要么纯数据驱动(忽略物理)。

Raissi
研究团队的切入点是利用自动微分技术，让神经网络的输出不仅拟合观测数据，还必须满足控制方程——这就是物理信息神经网络的核心思想：**物理定律不再是外部约束，而是内嵌于网络训练过程的"智能正则化器"**。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0f1639046b6d3a7861a52c7e03f1cac8?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=6v5u0wT0lafRnmubWkK%2BAb3RDF0%3D)

**研究意义 · 方法论 · 创新点**

**研究意义**

PINNs **首次**把任意非线性PDE作为可微分约束嵌入损失，通过自动微分精确计算残差，实现数据与机理的端到端协同。理论上，它为PDE正反问题提供了统一的函数逼近框架；应用上，可用少量观测完成流场重建、参数反演，为实时预测、数字孪生提供轻量级求解器。

**方法论**

**①**用一个前馈网络同时逼近待求场变量u(x,t)；

**②**将PDE左右两边差值定义残差f，通过自动微分得到∂u/∂t、∇²u等高阶导数；

**③**损失函数=数据MSE + PDE残差MSE + 边界MSE，权重共享同时训练；

**④**对时间依赖问题，提出连续与离散两种策略：连续型在全域采样配点，离散型借隐式Runge–Kutta把任意阶时间步长写进网络输出，实现一步大跨度预测。

**创新点**

**①**将自动微分用于输入坐标向量求导(而非仅对参数求导)，使神经网络天然满足微分算子形式；

**②**物理方程残差作为正则化项，在小数据下防止过拟合；

**③**离散时间模型首次实现超高阶(>100级)隐式格式，单步跨越大时间间隔。相比传统方法需数百万步迭代，PINN可一步到位，计算效率提升显著

**实验结果 · 研究结论 ·**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F6b4f94a92a3f435c52ff5ea2f343621b?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=L1hIS42KQO3gTKwfy2lnN13S5HM%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vdsEa5EuWshxUV6kdjtNOtV7UA8%3D)

**实验结果**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vdsEa5EuWshxUV6kdjtNOtV7UA8%3D)

研究团队**在多个经典物理问题上验证了方法的有效性**。在**薛定谔方程**(量子力学)中，仅用256个初始数据点预测复数解，相对误差仅0.2%；在**Navier-Stokes方程**(流体力学)中，用圆柱绕流的1%稀疏速度数据，成功识别出雷诺数(误差<5%)并重构完整压力场——尽管训练时完全没有压力观测值；在**KdV方程**(浅水波)中，仅用两个相隔很远的时间快照，就准确反推出方程参数(误差<0.06%)。

所有案例均采用L-BFGS优化器，在单块GPU上训练时间仅几十秒至数分钟。对比传统谱方法和有限元方法，PINNs在数据稀缺场景下展现出数量级的精度优势。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vdsEa5EuWshxUV6kdjtNOtV7UA8%3D)

**研究结论**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vdsEa5EuWshxUV6kdjtNOtV7UA8%3D)

核心发现是：物理约束是比数据更强大的正则化器。当物理定律已知且方程适定时，PINNs能以极少数据逼近真实解，本质原因是**物理方程将无限维的函数空间缩减到有限维的"可行解流形"上**。

研究还揭示，隐式高阶时间格式与神经网络的结合，可以突破经典数值方法的稳定性限制，**实现"一步到位"的长时预测**。这为跨尺度多物理场耦合问题提供了新思路：不再需要在每个尺度精细求解，而是让神经网络学习宏观规律的同时自动满足微观物理约束。

**论文评价 · 未来展望**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vdsEa5EuWshxUV6kdjtNOtV7UA8%3D)

**领域贡献**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vdsEa5EuWshxUV6kdjtNOtV7UA8%3D)

**这篇论文是PINNs领域的开山之作**，截至目前引用量超过11000次，催生了整个研究方向。其学术贡献在于：**提出了通用的物理嵌入框架，适用于任何可微物理定律；证明了深度学习与科学计算融合的可行性；为数据驱动建模提供了物理可解释性**。

应用影响遍及气候预测、航天设计、药物研发等领域，多家科技巨头已将PINNs集成到仿真平台中。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vdsEa5EuWshxUV6kdjtNOtV7UA8%3D)

**局限不足**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vdsEa5EuWshxUV6kdjtNOtV7UA8%3D)

方法存在三个主要局限：

其一是**维度灾难**，高维问题(如3D流场)需要指数级增长的配点数量，导致训练成本激增；

其二是**架构选择缺乏理论**，网络层数、宽度、激活函数的选择仍依赖经验，不同方程最优架构差异大；

其三是**训练不稳定性**，对于刚性方程或激波等间断解，梯度消失或爆炸问题严重，需要精心设计学习率策略。

此外，方法假设物理方程已知且准确，**对于未知或模型误差较大的系统效果受限**。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vdsEa5EuWshxUV6kdjtNOtV7UA8%3D)

**未来方向**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vdsEa5EuWshxUV6kdjtNOtV7UA8%3D)

**方向1-自适应配点策略：**开发基于残差的动态采样算法，在解变化剧烈区域加密配点，减少总计算量。

**方向2-多尺度网络架构：**设计编码器-解码器结构捕捉多尺度物理特征，结合小波变换处理间断解。

**方向3-不确定性量化：**引入贝叶斯神经网络提供置信区间，使PINNs可用于安全关键决策。

**方向4-数据+模型混合驱动：**当物理模型不完美时，自动学习修正项，平衡物理先验与数据拟合。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vdsEa5EuWshxUV6kdjtNOtV7UA8%3D)

**欢迎讨论**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vdsEa5EuWshxUV6kdjtNOtV7UA8%3D)

你认为 PINNs 下一步最该啃或最难啃的‘硬骨头’是三维湍流, 是多相流界面追踪, 还是其他方面? **欢迎在****评论区分享你的思考！**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F04dc8c4c5a7c502c53958c5738c77a73?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=%2Fd7IhHHsp0siZuVQaUqxlBsskU0%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc5818a1fd7701f607c1df8634974c2e4?Expires=1780065289&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=6mBAXzJ3v4Joykl6jpRCHry%2BawY%3D)

关注**智核学术｜**少走弯弯路

**↙↙↙  点击下方 “阅读原文”  按钮查看相关论文合集**

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 10:34*

## Related Notes

- [[守恒型物理信息神经网络（cPINN）：域分解策略提升守恒律方程求解精度]]
- [[FMPINN：基于傅里叶的混合物理信息神经网络求解多尺度椭圆PDEs]]
- [[物理信息神经网络（PINNs）研究综述：从理论框架到科学计算革命]]
