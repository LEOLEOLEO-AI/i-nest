# 神经可塑性与忆阻器：大脑与硅基模拟的对比研究

- **类型**: link
- **时间**: 2025-10-09 11:46:33
- **标签**: AI链接笔记, 神经可塑性, 忆阻器, 类脑计算
- **来源**: https://mp.weixin.qq.com/s/aJm_Okms_AuqntFSFOwKHA

## 内容

🧠 **神经可塑性核心概念**  
- **通俗定义**：记忆/技能使用频率越高，神经元连接能力越强（宏观表现为熟练，微观为神经连接强化）  
- **专业定义**（Christopher Shaw & Jill McEachern）：神经系统结构和功能的适应性改变能力，分为两类：  
  1. **结构性神经可塑性**：大脑改变神经元连接的能力，伴随新神经元生成与整合，通过MRI/CT等成像技术研究  
  2. **功能性神经可塑性**：神经元功能特性的适应性改变，包括：  
     - 活动依赖性可塑性（如突触可塑性，用于记忆形成）  
     - 反应性可塑性（神经元损伤后功能代偿，如脑区功能转移）  

🔬 **神经可塑性研究焦点**  
- 结构性神经可塑性是当前神经科学领域研究热点，关注内部/外部刺激对大脑解剖结构比例或强度的影响  

💡 **硅基芯片与大脑的核心差异**  
| **维度**       | **传统硅基芯片（二极管）** | **大脑神经元**               |  
|----------------|--------------------------|-----------------------------|  
| **信号模式**   | 二进制（0/1，通断控制）   | 多状态调节（神经递质释放量、兴奋/抑制类型） |  
| **可塑性基础** | 固定电路连接             | 动态突触连接强度变化         |  

🔍 **忆阻器：类脑计算的关键器件**  
- **定义**：可记忆先前通过电荷量的被动元器件，电阻值可动态调节  
- **优势**：相比二极管增加量化调节能力，更接近神经突触的连续状态  
- **局限**（与神经突触对比）：  
  1. 仅能模拟伪随机（算法控制），无法实现神经递质释放的真随机  
  2. 电阻值非负，无法同时模拟兴奋（正调节）与抑制（负调节）神经递质  
  3. 硬件连接固定，无法像神经元一样通过学习长出新突触  

📚 **研究案例与数据**  
- **忆阻器电路研究**：  
  - 4K-memristor analog-grade passive crossbar circuit（H. Nili & D. B. Strukov, 2021）  
  - 晶圆级忆阻器被动交叉阵列电路（Sanghyeon Choi et al., 2025），实现脑尺度神经形态计算潜力  
- **核心洞察**：人类技术发展呈现“规则随机化”（算法模拟真随机）与“随机规则化”（学习过程）的双向趋势

## 原文

首先解释一下什么是神经可塑性，通俗来讲：就是你对于种记忆、某项技能用的越多，宏观上表示为越熟练；微观上表示为，神经元的连接能力更强。  
  
用更专业一点的分类：Christopher Shaw和Jill McEachern（eds）在“走向神经可塑性的理论”中指出，在神经可塑性的研究中，没有包罗万象的理论包容不同的框架和系统。但是，研究人员通常将神经可塑性描述为“与神经系统的结构和功能相关的适应性改变的能力”。相应地，经常讨论两种类型的神经可塑性：结构性神经可塑性和功能性神经可塑性。  
  
结构性神经可塑性  
  
结构可塑性通常被理解为大脑改变其神经元连接的能力。基于这种类型的神经可塑性，在整个生命周期中不断产生新的神经元并将其整合到中枢神经系统中。如今，研究人员使用多种截面成像方法（如（MRI），（CT））来研究人脑的结构变化。这种类型的神经可塑性经常研究各种内部或外部刺激对大脑解剖结构的影响。脑中比例或强度的变化被认为是结构性神经可塑性的例子。当前在学术界的神经科学领域中，对结构神经可塑性的研究较多。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F8a71218e982d8aeae3f573db718accb4?Expires=1776346118&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=t13PZfLtM%2FfxTvCXVdRqiVGsp%2B0%3D)

功能性神经可塑性  
  
功能可塑性是指大脑改变和适应神经元功能特性的能力。可以响应于先前的活动（依赖于活动的可塑性）以获取记忆，或者响应于神经元的故障或损伤（反应性可塑性）以补偿病理事件而发生变化。在后者的情况下，根据需要恢复行为或生理过程，从大脑的一部分功能转移到大脑的另一部分。关于活动依赖性可塑性的生理形式，那些涉及突触的形式称为突出可塑性。  
  
我们说完神经的可塑性调节，接下来说一下硅基芯片模拟神经网络，硅基芯片的基本构成原件是二极管，功能即通过和停止，也就是我们编码中的0和1。那么问题来了：而构成大脑的基本原件的神经元神经释放神经递质，不只是释放和不释放0和1两种状态，还有每次释放多少，释放抑制还是兴奋神经递质等量化调节，即神经具有可塑性。  
  
下面引出一个电子元器件忆阻器：忆阻器（memristor）又名记忆电阻（memory resistor 的混成词），是一种被动元器件。如同电阻器，忆阻器能产生并维持一股安全的电流通过某个设备。但是与电阻器不同的地方在于，忆阻器可以在关掉电源后，仍能“记忆”先前通过的电荷量。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9e845d73be48915992cbad82ed96995d?Expires=1776346118&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=30md1RmQhabY25IGqciFVCey46I%3D)

个人想法：忆阻器作为基本元器件构成的矩阵网络芯片，相比较传统的二极管为基础的芯片更接近大脑神经突突触，不仅仅是定性调节，还有定量调节。  
  
不过类比于真正的神经突触，忆阻器还有以下几点达不到：  
  
1.忆阻器相比较二极管而言仅仅是多了一部分量化，但是和囊泡随机释放的神经递质比，做不到真随机，而是在算法下的一种伪随机。  
  
2.忆阻器电阻大小从0—某值，不能成为负值，不能同时模拟神经元突触的兴奋和抑制。  
  
3.对于新知识的学习，无法像神经元一样长出新的连接突触，软件无法重塑硬件。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ffa9a0d41369f9c15cfe7e441bdb9b323?Expires=1776346118&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=3tUb%2BJlany5Gak2Zdqc2MwQQKdo%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F59bc106065a82da72225f6d984c09a3d?Expires=1776346118&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=qOkl1fFnI62wOyc9MRNFTfhdy9o%3D)

个人认为，人类正在干两件事：规则随机化（利用各种算法模拟真随机），随机规则化（人的学习）

参考文献：

1.https://zh.wikipedia.org/wiki/神经可塑性

2.https://zh.wikipedia.org/wiki/忆阻器

3.4K-memristor analog-grade passive crossbar circuit，H. Nili & D. B. Strukov

Nature Communications volume 12, Article number: 5198 (2021)

4.Wafer-scale fabrication of memristive passive crossbar circuits for brain-scale neuromorphic computingSanghyeon Choi, Sai Su，NatCommunications volume 16, Article number: 8757 (2025)

---
**Tags:** #SDSoW #Chiplet
