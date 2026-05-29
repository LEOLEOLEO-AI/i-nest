# 生物启发的脉冲神经网络（SNN）设计与研究进展

- **类型**: link
- **时间**: 2025-07-22 19:50:01
- **标签**: AI链接笔记, 脉冲神经网络(SNN), 类脑人工智能, 神经元模型
- **来源**: https://mp.weixin.qq.com/s?src=11&timestamp=1753184688&ver=6128&signature=6mBDUl3l2hTDvGfM*tJ05SB81wYN8kpXKlk7COu13CtEsyUYFhESVy8IXDM-*uLq*WG8yxUQ6Rv4AcNlUuPMgU*DuPpouKQy9hAX6NWDloNHlj62ITgceLM0TOrYLIQh&new=1

## 内容

### 🔬 SNN概述
- **第三代神经网络模型**：1997年由Wolfgang Maass提出，基于脉冲神经元构建，具有时序信息整合和阈上脉冲活动特性
- **核心优势**：生物合理性、低能耗、神经形态硬件适配潜力
- **发展趋势**：从生物模拟转向性能优化，ANN2SNN转换和代理梯度反向传播技术成熟

### 🧠 神经元模型分类

![脉冲神经元模型分类](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F2679762ad3fcf0e9bddb60e0e3f7a896?Expires=1776345007&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=NQbtjMBlKD%2BLi2eURWdeAQ4X4cY%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)

| 模型类型       | 典型代表                  | 特点                                       | 应用场景               |
|----------------|---------------------------|--------------------------------------------|------------------------|
| 多房室模型     | 详细房室模型、缩减房室模型 | 高生物真实性，空间结构复杂                 | 神经科学研究           |
| 单房室模型     | Hodgkin-Huxley模型        | 离子通透性模拟，动力学精确                 | 神经元放电机制研究     |
|                | FitzHugh-Nagumo模型       | 非线性动力学分岔，简化生物神经元           | 理论分析               |
|                | LIF模型                   | 固定阈值和复位机制，计算简单               | 大规模网络模拟         |

### 🔄 神经元异质性研究

![神经元异质性对网络性能的影响](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb88e2128b61fc5e434180d4840055d86?Expires=1776345007&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=IG%2BjTGJ1bcGNRxhDPwKYD0dQhMs%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)
- **关键发现**：异质化神经元网络表现出更优学习特性
  - 基于动力学参数筛选实现神经元异质化
  - 随机初始化和训练诱导神经元异质化
  - 混合发放模式网络在多任务上性能优于单一模式网络

### 📡 编码方式比较

![多尺度动力学编码框架](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F2a9abb31c98ad208adcca4713697c3f5?Expires=1776345007&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=J24ebMwXBrsDvP6%2BvLcvsyO4klY%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)

| 编码方式       | 原理                          | 优势                     | 局限                     |
|----------------|-------------------------------|--------------------------|--------------------------|
| 频率编码       | 离散时间内脉冲发放频率        | 实现简单，应用广泛       | 忽略时间信息             |
| 时序编码       | 脉冲发放时间编码信息          | 精度高，生物合理性强     | 推理延迟高，复杂度大     |
| 群体编码       | 神经元群体协同表征信息        | 抗干扰性强，表征空间大   | 需要较多神经元           |
| 稀疏编码       | 少量神经元响应特定信息        | 低能耗，抗干扰           | 信息容量有限             |

### 📚 学习算法演进

![近似反向传播算法的发展](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F092dc2240650f9c90ee778bc9f22c483?Expires=1776345007&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Sm3wKEEaAmHoiyPN5cgF8H%2Faq6E%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)
- **生物启发算法**
  - 赫布学习规则：基于突触前后活动相关性
  - STDP（脉冲时序依赖可塑性）：权重更新依赖脉冲发放时序
  - 三因子学习规则：引入神经调制信号（如多巴胺奖励）

- **深度学习融合算法**
  - ANN2SNN转换：将训练好的人工神经网络转换为SNN
  - 代理梯度反向传播：解决脉冲发放不可微分问题
  - 反馈对齐算法：解耦双向矩阵相干性，降低生物实现难度

### 🔌 突触动力学机制

![突触动力学模型](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1bf7274424008dd8ae1469601c778027?Expires=1776345007&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=7wfpx2DWzlfvNE6Kz65a7tGfQAc%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)
- **短时程可塑性**
  - STD（短时程抑制）：高频输入导致突触效能降低
  - STF（短时程增强）：低频输入导致突触效能增强
  - 功能：复杂化信息表征、稳态维持、工作记忆支持

- **二阶吸引子突触**：构建膜电位平衡系统，实现动态信息处理

### 🏗️ 网络结构设计

![元结构特征抽取](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9b1e4a427fef6fda5c88343c3bca9875?Expires=1776345007&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=GVoypQq8iSWwL1o6p3WWWMZV71Y%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)
- **局部连接模式**
  - Motif环路单元：三点Motif频率实现听视觉环路融合
  - 侧向交互作用：模拟马赫带现象，增强特征提取和噪声抑制

- **全脑图谱启发**
![全脑图谱与脑区功能](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F687cbed0d2bdef846caa9a119c2e136e?Expires=1776345007&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2fybaEjNfPTYskVCiWN3TLi%2BXqc%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)
  - 研究思路：先减法（解析脑区特定功能）后加法（构建通用智能）
  - 关键结构：丘脑信息路由、视觉大环结构、基底节决策环路

### 🔮 总结与展望
- **核心价值**：类脑启发为突破现有AI瓶颈提供新思路
- **挑战方向**：生物合理性与计算性能平衡、全脑结构整合、神经形态硬件适配
- **跨学科意义**：AI与神经科学协同发展，相互启发机制解释与模型优化

## 原文

单击上方“**图灵人工智能**”，选择“星标”公众号

您想知道的人工智能干货，第一时间送达

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ffedbb31c5920eb1e0f6534c2fb5e6197?Expires=1776346188&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vad4if%2Bs7iASuysHjdoA49f56FU%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb72fd5e59a4c936ba3eab3ec12bbb96b?Expires=1776346188&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=U8QjqfDMOR35u6Aqa4I8AjuknRw%3D)

**导语**

**1997年，计算机科学家 Wolfgang Maass 就提出，由脉冲神经元构成的网络——脉冲神经网络（SNN）会成为继人工神经网络后的“第三代神经网络模型”。作为神经科学和人工智能最前沿的交叉点之一，脉冲神经网络的研究从神经元节点的生物合理化出发，并有可能进一步整合类脑启发，突破现今人工神经网络在能量消耗、鲁棒稳定、连续学习等层面的瓶颈。在集智俱乐部「[计算神经科学读书会](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247680541&idx=1&sn=3e8f6f04ff96462f44cf772c3b6c01f7&chksm=e8995890dfeed18623b4b88d0eb5c625931b945872f86b2da3d4169dec7f943b5c5a4ff5790e&scene=21#wechat_redirect)」中，中科院自动化所博士生程翔从几个不同方面介绍了生物启发的脉冲神经网络设计的实例和思想。**

****************研究领域：**计算神经科学，类脑人工智能，脉冲神经网络，神经元模型，复杂网络******************

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4063c4158ddbcc4efe7fca7c8f18bbd4?Expires=1776346188&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=mCjHIhcc%2FK%2BDOWvPAVhFIwI56NQ%3D)

程翔 **| 作者**

**目录**

**1. 神经元模型**

**2. 编码方式**

**3. 学习算法**

**4. 网络结构**

**5. 总结和展望**

1997年，Wolfgang Maass于《Networks of spiking neurons: The third generation of neural network models》一文中提出，由脉冲神经元构成的网络——**脉冲神经网络**（SNN），能够展现出更强大的计算特性，会成为继人工神经网络后的“第三代神经网络模型”[6]。在SNN发展的早期，其训练过程更偏向于使用突触可塑性规则以追求生物合理性。但由于赫布学习和脉冲时序依赖可塑性等规则的局部权重优化特性，SNN 在计算特性上的优势没有被很好地发掘[12,13]。随着深度学习的复兴，SNN研究也更多地转向对性能的追求，ANN2SNN 的转换方法和基于代理梯度的反向传播方法日趋成熟。目前，在AI应用中，具有充足模拟时间的SNN已经能够获得与ANN相媲美的性能，这为SNN的进一步发展和神经形态硬件的研发提供了信心。

在这篇文章中，我想从四个方向对生物启发SNN设计的一些实例和思想进行介绍，包括神经元模型、编码方式、学习算法、网络结构，最后总结并展望类脑启发对于面向AI应用的SNN研究的意义。

### ******1. 神经元模型******

为了模拟生物神经元的活动模式，计算神经科学提出了一系列脉冲神经元模型。与使用激活函数的人工神经元相比，脉冲神经元普遍具有时序信息整合，阈上脉冲活动的特点。依照树突和轴突建模的空间复杂性，脉冲神经元可以分为单房室模型、缩减房室模型和详细房室模型。单房室模型中也存在着对可兴奋膜不同的建模方式，例如建模不同离子通透性的 Hodgkin-Huxley 模型和 Morris-Lecar 模型，基于非线性动力学分岔的 FitzHugh-Nagumo 模型和 Hindmarsh-Rose 模型，和基于固定阈值和复位机制的整合发放（integrate-and-fire）模型和振荡发放（resonate-and-fire）模型。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F2679762ad3fcf0e9bddb60e0e3f7a896?Expires=1776346188&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=qu8Wxe5R0Jt%2FRUrAPkDo2eaQziY%3D)

图1. 脉冲神经元的模型

由于计算复杂性的原因，大多数的脉冲神经元模型都不适用于类似人工神经网络的大规模模拟。Wolfgang Maass 在提出SNN时使用的是相对简单的整合发放模型，而带泄漏整合发放（leaky integrate-and-fire，LIF）模型[1]则是目前在面向AI的SNN研究中最为常用的脉冲神经元。一些面向SNN学习算法的工作将LIF神经元与循环神经元进行类比，这使得SNN能够更好地融入深度学习的框架之中。

> [1] Dayan P, Abbott L F. Theoretical neuroscience: computational and mathematical modeling of neural systems [M]. MIT press, 2005.

虽然LIF模型具有脉冲神经元的基本性质，但其一维线性动力学的膜电位整合过程也被认为“过于简单而不能产生皮层神经元一般丰富的发放模式”。一个常见的增强神经元动力学特性的方法，是引入自适应变量与膜电位形成一个二维系统，这种做法可以被解释为自适应的阈值变化或是内部的恢复变量。Izhikevich 神经元[2]在此基础上进一步将线性动力学替换为非线性动力学，并通过一组参数产生发放模式的异质性。该模型启发的相关工作表明，**异质化的发放模式能够影响网络处理不同类型信息的能力****，****且混合网络能够在多类任务上同时获得性能优势**。另一些实验表明，基于训练和初始化得到的时间常数异质性赋予SNN鲁棒性，使其能在广泛的环境中学习[3]。

> [2] Izhikevich E M. Simple model of spiking neurons [J]. IEEE transactions on neural networks, 2003, 14(6): 1569-1572.
>
> [3] Perez-Nieves N, Leung V C H, Dragotti P L, et al. Neural heterogeneity promotes robust learning[J]. Nature communications, 2021, 12(1): 5791.

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb88e2128b61fc5e434180d4840055d86?Expires=1776346188&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=avMwwZ42Yu7EtHFRwdQ66w8eoio%3D)

图2. 神经元异质性

### ******2. 编码方式******

脉冲神经元的内在时序结构催生脉冲神经网络对非序列输入信息序列化的需求。根据生物神经系统对外界刺激的编码方式，许多能有效将信息存储到脉冲序列的编码方式被提出，包括频率编码（rate coding）、时序编码（temporal coding）、群体编码（population coding）、稀疏编码（sparse coding）和多种编码方式混合编码等。其中，利用离散时间内脉冲发放频率的**频率编码**最为常用，但是会忽略神经元放电时间与所编码信息间的联系[4]。**时序编码**能够利用脉冲发放时间，因而相较于频率编码更为精确，但也更为复杂，并且容易产生较高的推理延迟[5]。

> [4] Adrian E D, Zotterman Y. The impulses produced by sensory nerve-endings: Part ii. the response of a single end-organ [J]. The Journal of physiology, 1926, 61(2): 151.
>
> [5] VanRullen R, Guyonneau R, Thorpe 

---
**Tags:** [[BrainInspired]] [[Chiplet]]
