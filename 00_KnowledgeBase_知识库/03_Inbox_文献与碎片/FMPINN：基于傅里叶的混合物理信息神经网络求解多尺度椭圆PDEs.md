---
title: "FMPINN：基于傅里叶的混合物理信息神经网络求解多尺度椭圆PDEs"
source: "https://mp.weixin.qq.com/s/1AQmyLhLKVw8Esp5ahWnHA"
created: 2025-11-15
note_id: "1893233357656093816"
tags:
  - "AI链接笔记"
  - "物理信息神经网络"
  - "FMPINN"
  - "多尺度椭圆PDEs"
  - "get-笔记"
  - "AI研究"
  - "重要"
---

# FMPINN：基于傅里叶的混合物理信息神经网络求解多尺度椭圆PDEs

## 摘要

🔬 **研究背景与问题** - **核心挑战**：多尺度椭圆偏微分方程（PDEs）在材料科学、油藏模拟中广泛存在，但传统PINN因"频率偏好"对粗糙系数（高频振荡）失效 - **传统方法局限**：有限元法（FEM）需网格分辨率小于振荡尺度ε，导致计算量爆炸；传统PINN在ε=0.001时相对误差达9

## 正文

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F17c723df432fbc5eb74bcf67ded7f4b8?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=%2Fz1QC8BM8IH69E1a0XGw4wGcSBM%3D)

**PINNs****｜精选 · 论文推荐**

AI for Science｜第二十七期

**基于傅立叶的混合物理信息神经网络**

**求解一类多尺度椭圆 PDEs**

Solving a class of multi-scale elliptic PDEs by Fourier-based mixed physics
informed neural networks

**第一作者：Xi'an Li**

**作者单位:**Ceyear Technologies Co., Ltd（中国青岛）

Journal of Computational Physics

**论文主页：**

**https://www.sciencedirect.com/science/article/pii/S0021999124002614**

**论文｜PDF 下载 ↓**

**https://www.jianguoyun.com/p/DWq831kQ7P3jDRjm55gGIAA**

**开源代码 ↓**

**https://github.com/Blue-Giant/FMPINN**

点击打印论文信息

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F57eebd54872766d45af10f4732d12861?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=UdiDXiM8IpfEIOvWK3wqt7vUb1A%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbf612be9540de8e1c05b633843e31cfb?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=8L7PNzrjeOrlXHNYxkuLMzHQC%2Fw%3D)

Published 2024-07

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1934f1c1b64716367e2a473a26ae0623?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=igVcMaHKvVN3DkbHzq%2Fv4%2Bu65O4%3D)

多尺度偏微分方程是材料科学、油藏模拟等领域的核心难题，但**传统PINN因'频率偏好'在粗糙系数面前频频失效。**Ceyear
Technologies与澳大利亚天主教大学联合团队在计算物理顶刊JCP发表研究，**提出FMPINN框架**——通过**引入通量变量和傅里叶特征映射**，在8维空间仍能保持10⁻⁴级精度。这项研究为科学计算开辟了数据与机理深度融合的新路径。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F04dc8c4c5a7c502c53958c5738c77a73?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=7%2BJ8rOnHTIi4rcTPk7hl2l4BaM8%3D)

**研究背景 · 问题意识**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F94fdb3fe1bf47169c59d442e87cf3c2b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=unK8VuxdWpEOMOATVMLP%2FYP2frU%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hWy3Emw0gw6vMp5ke6JseJ4p4eE%3D)

**研究背景**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hWy3Emw0gw6vMp5ke6JseJ4p4eE%3D)

多尺度椭圆型PDE描述复合材料、多孔介质等物质的跨尺度行为，其**系数A^ε(x)在微观尺度剧烈振荡**。**传统有限元法**(FEM)需网格分辨率小于振荡尺度ε，导致**计算量爆炸**。**物理信息神经网络**(PINN)虽是无网格方法，但存在**'谱偏差**'——优先拟合低频成分，对高频振荡无能为力。

近年来，MscaleDNN通过多尺度输入变换尝试解决谱偏差，但**在粗糙系数下，PINN的神经网络切向核(NTK)矩阵条件数随ε→0而恶化，训练过程极度困难**。2022年Leung等的NH-PINN虽能求解，却将低维问题转化为高维，计算负担更重。这些瓶颈限制了PINN在真实工程中的应用。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hWy3Emw0gw6vMp5ke6JseJ4p4eE%3D)

**问题意识**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hWy3Emw0gw6vMp5ke6JseJ4p4eE%3D)

核心矛盾在于：**粗糙系数A^ε(x)的梯度信息在自动微分中'泄漏'，导致网络无法同时捕捉宏观解和微观振荡。**如同用一把尺子同时测量山脉起伏和岩石纹理，传统PINN的单网络架构在多尺度特征面前顾此失彼。研究团队的关键洞察是——**借鉴混合有限元方法，将通量φ=A^ε∇u作为独立变量，把二阶问题降为一阶系统。**

**研究意义 · 方法论 · 创新点**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hWy3Emw0gw6vMp5ke6JseJ4p4eE%3D)

**研究意义**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hWy3Emw0gw6vMp5ke6JseJ4p4eE%3D)

FMPINN将降阶思想与傅里叶特征深度融合，理论上通过混合 formulation
规避了NTK病态问题，应用上**实现了'宏观-微观'解耦求解**。对于ε=0.001的强振荡问题，传统PINN相对误差高达99%（基本失效），而FMPINN可达9.28×10⁻⁵，精度提升超过千倍。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hWy3Emw0gw6vMp5ke6JseJ4p4eE%3D)

**方法论**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hWy3Emw0gw6vMp5ke6JseJ4p4eE%3D)

**①
问题重构：**引入通量变量φ(x)=A^ε(x)∇u^ε(x)，将原问题-div(A^ε∇u)=f转化为-div(φ)=f和φ-A^ε∇u=0两个一阶方程。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F97f7696b985ccd8c3a4abb81d24bf669?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Qg9p47z7CFb1qeFAHSXSmzHo3FA%3D)

**②
网络架构：**采用MscaleDNN包含24个子网络，每个子网络5层隐藏层。输入x通过24个不同尺度因子(1,2,3,...,100)缩放后分别进入子网络，输出加权融合。这相当于用24个'放大镜'同时观察不同频率成分。

**③ 傅里叶激活**：第一隐藏层使用傅里叶特征映射ζ(x)=[cos(κx);
sin(κx)]，将输入映射到高频空间；后续层采用(sin+cos)/2激活函数，保证Lipschitz连续性。

**④ 损失函数**：L = L\_in + γL\_bd，其中L\_in包含两部分——物理残差‖-div(φ\_NN)-f‖²和通量残差‖φ\_NN -
A^ε∇u\_NN‖²，平衡参数β和γ动态调整。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4006396b6c76f24ae62ee5f6345bd80b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ByRWEHWIFyI0bOk6e9yXPGbQKDQ%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hWy3Emw0gw6vMp5ke6JseJ4p4eE%3D)

**创新点**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hWy3Emw0gw6vMp5ke6JseJ4p4eE%3D)

**① 双变量耦合**：u和φ由同一多输出网络学习，共享底层特征但独立输出，避免训练两个网络的冗余。  
**② NTK正则****化**：通量残差项将条件数从O(1/ε²)降至O(1)，训练稳定性显著提升。  
**③ 频率解耦**：多尺度输入+傅里叶映射让每个子网络专注特定频段，克服谱偏差。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb32fbff8015921b792f9be1ea170d76b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=08eDnkfkPoB2mjR2D0NtgYcu7s0%3D)

**实验结果 · 研究结论 ·**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hWy3Emw0gw6vMp5ke6JseJ4p4eE%3D)

**实验结果**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hWy3Emw0gw6vMp5ke6JseJ4p4eE%3D)

团队在1D到8D Euclidean空间设计6个典型案例。

**在1D测试中**，ε从0.1到0.001（振荡频率提升1000倍），FMPINN的L²相对误差始终保持在10⁻⁶~10⁻⁴量级，而MPINN在ε=0.01时误差达87.4%，ε=0.001时完全失效。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F6d83f6c5490603c873c3fe3df44ad742?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=31PVB6PQM7aHQCUfrx079%2FCSfJg%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F6d1b7f61c9a7b6657d1d8e5c5e08c521?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=r2aKpNWvMR2cv2rj0YLQtpvVNw0%3D)

**2D多频率系数测试显示**，FMPINN相对误差1.39%，比MPINN（99%）提升两个数量级，计算时间仅为MPINN一半。最惊人的是8D问题——当MPINN因内存爆炸无法运行时，FMPINN仍保持1.38%误差，证明其维度扩展性。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1a612ff508239903e4242bd395671748?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=wDkmrAqoHnXUy6xMUZuP%2BjA4sZo%3D)

**对比实验**还显示，当配点数为1000时，FMPINN精度比FEM高一个数量级；虽然FEM在50万点时精度反超，但计算时间缩短为FMPINN的1/13，体现无网格方法的优势。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F8a6c13647aa62dc00355d41673abcd78?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=SQGa06445%2B%2BtRKgPPPBf9Ydm15c%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hWy3Emw0gw6vMp5ke6JseJ4p4eE%3D)

**研究结论**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hWy3Emw0gw6vMp5ke6JseJ4p4eE%3D)

**FMPINN通过混合formulation和傅里叶特征，有效解决了粗糙系数导致的多尺度PDE求解难题。**核心发现是：将二阶导数计算转化为一阶系统，不仅降低计算复杂度（自动微分次数减半），更重要的是改善了损失景观的平滑性。这为科学计算提供了新范式——当物理方程具有特殊结构时，重构问题形式比单纯增加网络容量更有效。

**论文评价 · 未来展望**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hWy3Emw0gw6vMp5ke6JseJ4p4eE%3D)

**领域贡献**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hWy3Emw0gw6vMp5ke6JseJ4p4eE%3D)

这项工作在多维、多频率、粗糙系数下系统验证PINN可行性的研究，发表于计算物理顶刊JCP。其学术价值在于**揭示了NTK条件数与问题形式的深层联**系，应用价值在于为复合材料设计、油藏数值模拟等提供高效代理模型。代码已开源，推动了社区对混合PINN范式的探索。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hWy3Emw0gw6vMp5ke6JseJ4p4eE%3D)

**局限不足**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hWy3Emw0gw6vMp5ke6JseJ4p4eE%3D)

方法有三个客观局限：

**① 网格依赖性消除后，配点采样策略成为新瓶颈**——均匀采样在低维可行，高维面临维数灾难；

**② 通量变量φ无显式边界条件**，网络需额外学习其分布，导致内存占用比传统PINN高约30%；

**③ 损失函数三项目前手动调权**，缺乏理论指导，不同问题需反复实验。

此外，傅里叶特征映射的尺度因子选择仍依赖先验知识，自适应学习机制尚未建立。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hWy3Emw0gw6vMp5ke6JseJ4p4eE%3D)

**未来方向**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hWy3Emw0gw6vMp5ke6JseJ4p4eE%3D)

**方向1-自适应残差采样**：借鉴重要性采样思想，根据通量残差‖φ-A^ε∇u‖²动态调整配点密度，在解变化剧烈区域加密。

**方向2-混合精度的通量约束**：对φ施加H(div)正则化，利用Raviart-Thomas有限元空间的基函数作为网络约束，保证通量守恒。

**方向3-多物理场耦合**：将FMPINN扩展至流固耦合、热-力耦合问题，为每个物理场设计独立子网络但共享通量信息。

**方向4-不确定性量化**：引入贝叶斯MscaleDNN，对粗糙系数和通量变量建模为随机过程，获取解的置信区间。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F04dc8c4c5a7c502c53958c5738c77a73?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=7%2BJ8rOnHTIi4rcTPk7hl2l4BaM8%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F66efc16a4f195d5ed12bbbdd2d70888f?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=zaytzdtdz2xGS2Pf7a3Htl9Bfzs%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd757d42b1b97b77a0b64f19cf9cd55a1?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=jgNF1VrzFi3cw%2FaZ4DoefEiZXBI%3D)

**# 启示与讨论>>**

**作为科学机器学习从业者，你更看好FMPINN这类混合方法，还是XPINN、cPINN这类域分解方法？当物理方程存在模型误差（如忽略湍流小尺度效应）时，你认为该如何平衡物理先验与数据修正？**

**启示1：**物理方程不仅是约束，更是正则化器——将NTK病态条件数从O(1/ε²)降至O(1)，小数据下优势凸显。

**启示2：**问题重构或许比网络重构更重要——将二阶PDE降为一阶系统，计算量减少50%且精度提升千倍。

**启示3：**多尺度问题的本质是频率解耦——子网络+傅里叶映射让不同频段独立学习，避免高频信号被低频淹没。

***声明：本系列推文仅代表个人解读与观点，******旨在抛砖引玉，不代表研究团队立场。******若内容涉及版权或事实错误，欢迎通过后台指正。***

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe9fed27d8e244b76bd2a8639dd7425e7?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=NZUPhD3%2FUnC%2FQKUdKpseML1MCcU%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc5818a1fd7701f607c1df8634974c2e4?Expires=1780064210&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=6k6pgwg1v0SsXETZKpLAVB9k3L0%3D)

关注**智核学术｜**少走弯弯路

**↙↙↙  点击下方 “阅读原文”  查看相关论文合集**

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 10:16*