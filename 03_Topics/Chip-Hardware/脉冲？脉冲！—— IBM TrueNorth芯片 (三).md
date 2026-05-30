---
title: 脉冲？脉冲！—— IBM TrueNorth芯片 (三)
tags:
- brain
- chip
- chip-hardware
- dynamics
- large-language-model
- neural-networks
- neuron
- neuroscience
- plasticity
- project
---
> 笔记本: 我的剪贴板  
> 创建时间: 2024-05-28  

---

**引言** 在IBM TrueNorth芯片（一）中我们介绍了美国国防部研究机构DARPA的“类脑自适应可塑性可扩展电子系统”项目，也就是IBM TrueNorth芯片的背景，大脑启发、模拟大脑的概念，IBM TrueNorth芯片的设计原则。在IBM TrueNorth芯片（二）中我们介绍了冯·诺依曼架构，非冯·诺依曼架构，芯片极简史，戈登·摩尔和卡弗·米德的革命情谊，摩尔定律和类脑计算的渊源。  在本篇文章中，我们将继续非冯·诺依曼架构这一章节，介绍神经网络的芯片实现，再深入介绍生物神经元、以及TrueNorth中的神经元模型。  **笔者将详细探讨类脑计算与脉冲神经网络的核心，让人又爱又恨的脉冲，到底是什么样的存在。**  **借用哈姆雷特的经典独白：** **To Spike, or Not Spike? ** **That is the question!**  **神经网络在TrueNorth芯片中的实现**
 
在类脑芯片中，存储单元和计算单元位于同一位置。神经元是计算单元，神经元计算过程中需要用到突触权重 (weight)和膜电位 (membrane potential)这些数据。我们可以通过决定神经元和神经元的连接来对芯片进行编程，因此我们不需要写指令到内存中，而是编程神经元之间的连接和参数。 
 
TrueNorth计算核架构 
上图说明了TrueNorth的核心逻辑。灰色箭头左边的子图是一个两层神经网络，在这个子图中，左边的第一层是突触前神经元，以白色半圆半矩形的图案 (与门符号的形状)表示；右边的第二层是突触后神经元，以灰色的三角形表示，这些黑线代表突触连接。这其实就是人工神经网络中全连接层。
 
灰色箭头右边的子图展示了这个全连接层在芯片中的逻辑实现。输入的脉冲信号被收集在缓冲器 (Buffer)中：每1毫秒一次的全局时钟决定了在芯片中脉冲是定期计算的 (可以想象全局时钟每1毫秒为一个周期滴答一次，计算一次结果并更新)，所以我们需要存储这些脉冲，存储到时钟滴答声传过来进行计算，因此，我们需要本地存储。 
哪个脉冲被送到哪个神经元是由具体神经元中的连接决定，这个连接可以通过交叉阵列 (crossbar)来实现：交叉阵列上的一个点代表相应的突触后神经元树突(垂直线)和突触前神经元轴突末端 (水平线)之间的连接。这个连接点是突触，连接“强度”就是突触权重。 
在图中还有一些额外的模块，如伪随机数生成器 (Pseudo Random Number Generator, PRNG)，用于更复杂的功能，如随机脉冲整合 (stochastic spike integration)、随机泄漏 (stochastic leakage)、随机阈值 (stochastic thresholds)等。 
当时钟滴答声到达时，神经元开始处理接收到的脉冲，如果他们达到了脉冲阈值，它们将生成脉冲并将这些脉冲发送给相应的神经元。 
Truenorth芯片内部由以二维网状(2D Mesh)的拓扑结构连接的计算核组成。在更上一个层次，Truenorth芯片也同样可以二维网状结构连接，这种连接称为片上网络 (Network-on-Chip, NoC)。基于这种架构，神经元既可以有局部连接 (即脉冲在芯片内的计算核中进行发送和接收)，也可以有全局连接 (通过片上网络将脉冲发送到外部芯片的计算核)。
 
  
TrueNorth芯片互联 
**现在我们已经知道TrueNorth芯片如何实现神经网络。我们还需要深入一层了解，它的神经元是怎么实现的？要回答这个问题，我们得先知道，什么是生物中定义的神经元？** **生物神经元**
 **** 
神经元 (neuron)由不同部分组成，如图所示。树突 (dendrite)从细胞体(cell body, soma)分支出来，细胞体中延伸出一个长的通讯通道称为轴突 (axon)，它一直延伸到突触前的末端 (pre-synaptic terminal)，这个末端可以有多个分支。
 
 
树突(dendrite)的功能是接收其他神经元的信息。一些树突有小突起称为棘突 (dendritic spine)，这对于与其他神经元的通信非常重要。
 
 
细胞体 (cell body, soma)是神经元进行计算的地方，其中包含细胞核 (nucleus)，膜电位 (membrane potential)在这里通过与环境和其他神经元进行离子交换来累积。
 
 
轴突 (axon)是神经元的通讯通道。它通过轴突丘 (axon hillock)附着于神经元。
 
 
沿着这个神经元的轴突末端一路往前，到达突触前末端 (presynaptic terminal)，可以看到与很多其他神经元形成了连结点，这些连接点称为突触 (synapse)。也就是说，突触前细胞 (presynaptic cell)的末端与突触后细胞 (postsynaptic cell)通过突触连接。 
当动作电位 (action potential)到达突触前末端时，神经元会将神经递质 (neurotransmitter)释放到突触中。神经递质作用于突触后细胞。因此，神经元通信需要一个电信号（动作电位）和一个化学信号（神经递质）。普遍情况下，突触前末端与树突通信，但末端也可以与细胞体甚至轴突通信。神经元还可以与非神经元细胞如肌肉细胞或腺体形成突触。  
轴突可以传递动作电位，这就是脉冲 (spike)。脉冲传递到轴突末梢，导致神经元释放化学神经递质继而与其他细胞通信。 
 
**我们要模拟神经元，要模拟脉冲，以实现脉冲神经网络。那我们还需要更深入地了解，什么是脉冲？** 
**脉冲的产生** 
动作电位在人的细胞中非常重要。在非神经元中，它主要的功能是激活细胞内过程。例如，在肌肉细胞中，动作电位是导致收缩的一系列事件中的第一步。在胰岛β细胞中，它们触发胰岛素的释放。在神经元中，动作电位在细胞通讯中发挥核心作用，我们也将其称之为“脉冲”——Spike。 
 
像所有动物细胞一样，每个神经元的细胞体都被细胞质膜 (Membrane)包围。质膜是双层脂质分子，是一种强大的绝缘体，其中嵌入了多种类型的蛋白质结构，许多具有电活性，其中包括允许带电离子流过膜的离子通道 (ion channel)，有些离子通道是电压门控 (voltage-gated)的，可以通过改变细胞膜内外侧的电压差使得它在开路和闭路状态之间切换。离子物质包括钠 (Na+)、钾 (K+)、氯化物 (Cl−)和钙 (Ca2+)等。细胞膜的内外的电压差也称为膜电位 (Membrane potential)。 
知名结构生物学家颜宁教授的其中一个研究方向就是电压门控离子通道的结构与工作机理，Google Scholar上显示她最新的一篇文章就是“Structural biology of voltage-gated calcium channels”。 
颜宁教授的另一个重点研究领域是葡萄糖转运蛋白 (Glucose transporters)，它们负责运输葡萄糖，为细胞提供能量来源，这种蛋白和离子通道，以及离子转运蛋白 (Ion Transporters)等都是关键膜蛋白，承担着不同功能，可以从怎么和细胞膜结合、运输的物质以及是否消耗能量等来区分。按和细胞膜的结合方式，离子通道属于整合膜蛋白。 
** **  
整合膜蛋白，外在膜蛋白、和脂锚定蛋白**** 
** ** 
KcsA钾离子通道的结构，两个灰色平面表示脂质双层的烃边界**** 
   
(a) 钠 (Na+) 离子。(b) 钾 (K+) 离子。(c) 钠通道。(d) 钾通道。(e) 钠钾泵。 
上图说明了一个脉冲的全过程： 
在 (1)静息状态 (Resting state)时，神经元内部带净负电荷。 
一旦接受到刺激 (Stimulus)，比如突触前神经元传过来的信号，神经元的 (2)去极化 (Depolarization)就会激活钠通道，使钠离子 (Na+)穿过细胞膜进入细胞，从而在神经元中产生相对于细胞外的净正电荷。 
如果电压差没有累积到超过阈值电压 (Threshold)，就不会产生动作电位 (Action potential)，这种情况叫 (Failed initiations)。当超过阈值电压时，就会引发动作电位，膜电位快速上升，然后又快速下降。 
达到动作电位峰值后，神经元开始 (3)复极化 (Repolarization)，其中钠通道关闭，钾通道打开，使钾离子 (K+)穿过膜进入细胞外液，使膜电位恢复为负值。 
最后，有一个 (4)不应期 (Refractory period)，在此期间，这些离子通道失活，钠、钾离子在膜上恢复到它们的静息状态的分布。 
下图是更加清楚的膜电位在一个脉冲期间的变化过程。 
   
脉冲  
  **模拟神经元 —— 一个科学，还是工程问题？**   好的，让我们盯着上面这条红色的曲线默看一分钟，因为，类脑计算的核心问题都与这条曲线相关，引用笔者在之前文章中写的内容： 
 
“Engineering，工程学，本质就是从复杂混沌的自然现象中抽象出一些简单的规律和模式，这些规律和模式可以应用到我们的创造之中，足以解决一些实际的问题。”
 周芃，公众号：开源类脑[迷人又恼人的大脑，人类对大脑的致敬之 —— IBM TrueNorth芯片 (一)](https://mp.weixin.qq.com/s?__biz=MzU3MDkyOTUxOA==&mid=2247483827&idx=1&sn=ac6159851af1fa39bcd4dbf32759e050&chksm=fce6b9b2cb9130a45494273e27857b56b6b92f7087cc9863e8419be5bd8039bbfa192c51f242&token=1016154600&lang=zh_CN#rd)  
我们提出两个核心问题： 
**一、我们从这条曲线里可以抽象出什么模式？** 
**二、在硬件和软件上分别如何复现这个模式？** 
读者朋友们，当你们思考这两个问题，其实就碰触到了类脑计算的核心。  如果读者朋友们看了笔者写的这篇文章：  
 周芃，公众号：开源类脑[史上最全类脑软件总结。大脑仿真也好奇：什么时候大模型可以趋近人脑的数量级？](http://mp.weixin.qq.com/s?__biz=MzU3MDkyOTUxOA==&mid=2247483711&idx=1&sn=964a4b87c98946395066cd99739f0ba1&chksm=fce6b93ecb913028b7c5eb221e9de92e7fe6a900a44a524ebb355586a9c8e7cf8fb44ac12853#rd)  
恭喜你，你至少对软件层面的模拟有了一个大致的概念。 
软件上，我们手上现在有开源的类脑软件，这是好消息。 
软件最终还是依赖硬件运行，在硬件上，我们现在也有很多类脑芯片。 
类脑芯片最终还是需要我们设计。 
所以，我们仍然要回到问题的最初，第一性原理，回到上述这两个问题。 
第一个问题可以仅在数学层面上回答这个问题，请大家思考，什么方程可以模拟这个曲线？我们可以模拟到哪个地步？想象我们是20世纪的神经科学家，我们在鱿鱼的神经元中发现它有一个巨大的轴突，可以把电极插入轴突腔内，记录电位。 
  
鱿鱼 
  
鱿鱼中电极的记录 
我们记录到了这个脉冲！ 
想象我们是计算神经学家，我们开始思考如何模拟这个曲线。我们先将细胞膜做一个简单的电路模拟。 
  
四种基本电子元件及其相互关系 
四种基本电子元件包括：1. 电阻 (Resistor)，2. 电容 (Capacitor)，3. 电导 (Inductor)，4. 忆阻器 (Memristor)。 
请问读者朋友们，在电路的四种基本元件中，可以用什么来模拟细胞膜？ 
细胞膜是绝缘体，并且可以累积电势，这不就是电容嘛！ 
请问读者朋友们，在四种基本电子元件中，可以用什么来模拟对膜电位影响最大的钠、钾离子通道？ 
钠、钾离子通道可以导通，这不就是电阻嘛！不仅如此，它可以导通、关闭，本质上是一种阻值可以变化的电阻，这不就是忆阻器嘛！ 
除了钠、钾离子通道之外，我们还需要考虑细胞膜对离子的自然渗透性，以及一些其他复杂的调控机制，它可以用一个总的泄漏电阻表示。 
所以，我们可以得到神经元的电路模型： 
  
# Hodgkin–Huxley (HH) 神经元电路模型
 
根据以上神经元电路模型图，得到通过细胞膜 (Cm)的电流表达式为： 
 
其中 I 为单位面积总膜电流，Cm为单位面积膜电容，gK和gNa分别为单位面积的钾和钠电导，VK 和VNa分别为钾和钠离子通道的反转电位，g和V分别为各通道单位面积的漏电导和漏电反转电位。其中依赖时间的参数是 Vm、gNa 和 gK。gNa 和 gK两个电导还取决于膜电压 (Vm)。 
这个方程可以抽象出细胞膜电位的模式，但是，我们还没有具体模拟钠、钾离子通道的电导，也就是gNa 和 gK。
 
 
经过了一系列实验，不断改变细胞外钠和钾浓度，最终
 Alan Hodgkin和
 Andrew Huxley
 得到了神经元
 的完整模型，包括四个常微分方程： 
 
其中 I 是单位面积总膜电流， 
𝛼 和
 

 

 𝛽  是各离子通道的速率常数，这些常数依赖于电压但不依赖于时间。 

 

 

 

 𝑔 是各   
 离子通道电导的最大值。
 n
 , 
 m
 , 
 h是介于0和1之间的无量纲参数，分别与钾离子通道激活、钠离子通道激活和钠离子通道失活相关。 
给HH神经元下图三的电流输入时，m, n, h的变化如下图二所示，产生的膜电位如下图一所示。 
  
HH神经元仿真 
**HH模型不需要额外膜电位是否超过阈值的判断，这四个常微分方程互相耦合，形成了神经元奇妙的动力学特性！** 

 Alan Hodgkin和
 Andrew Huxley获得了1963 年诺贝尔生理学或医学奖，就是因为发现了离子机制参与了神经元细胞膜相关的刺激和抑制功能。 
  
1963诺贝尔生理学或医学奖 
**HH模型就是**
 **Alan Hodgkin和**
 **Andrew Huxley从"Spike"中抽象出来的模式！** 

 这四个微分方程比较复杂，我们能不能再进一步简化？在电路模型中，这几个离子通道都是电阻，我们可以用一个最简化的泄漏通道来表示，于是在电路模型中，只有电阻、静息（反转）电压源、电容，已经非常简单，如下图所示。 
  
LIF神经元电路模型 
由于没有相互耦合的机制，我们需要一个额外的阈值判断机制，当膜电位高于一定程度，则产生脉冲，膜电位重置，把这部分机制也加上的神经元电路模型如下图： 
  
LIF神经元完整电路模型 
这就是现在脉冲神经网络领域最常用的Leaky Integrate-and-Fire (LIF)，漏积分点火模型，TrueNorth内部的神经元模型就采用的LIF模型。表达式为：  
 
我们需要设定如下常数：阈值电压Vth，重置电压Vreset，静息电压Vrest。需要额外判断Vm(t)和Vth的大小，当Vm(t)大于Vth时，输出Spike，S(t)=1，Vm(t)=Vreset，膜电位重置，静息电位由图中与电阻串联的电压源Vrest提供。 
更细节的解释，在笔者参与研发的开源类脑软件snnTorch，Rockpool中都有详细推导，请读者搜寻查阅。 
**这个模型复现了"Spike"中的三个核心模式：** 
**1. Leaky**，“leaky”机制的是动力学特性的体现，是上图电路中的电阻。它使得膜电位只要没达到阈值，都会不断“泄漏”电压，指数地衰退到电压源提供的静息电压值。如果没有这个特性，一小时之前的输入和当下的输入对于膜电位都有同样的影响，这显然不合理。 
**2. Integrate**，“integrate”机制是膜电位储存电压能力的体现，是上图电路中的电容。它使得神经元可以积累膜电位，如果没有这个特性，膜电位无法累积，神经元无法产生脉冲。 
**3. Spike**，“Spike”机制是神经元动作电位的体现，是上图电路中的开关，以及完整机制中Vm和Vth的比较过程。它使得神经元产生脉冲，而脉冲产生被简化成了一个狄拉克δ函数 (Dirac Delta Function)。 
   
   
  
上：狄拉克δ函数，下：脉冲产生函数 
Leaky Integrate-and-Fire模型既保留了Spike的核心模式，尤其是它的动力学特性，又极大地简化了微分方程的复杂度。 
神经元的模型还有一系列变种，比如，阈值是不是可以不是常数，而是adaptive，有其动力学特性，使得它经常发出Spike后一定程度受到抑制？比如，能不能在公式中，加入一些非线性的，指数或者二次方依赖Vm(t)的项？比如，Rm是不是可以不是常数，依赖于Vm(t)，或者输入？等等。这些思考和探索也非常好玩有趣，是计算神经科学 (Computational neuroscience)主要的研究领域。 
笔者再抛出： 
**模拟神经元 —— 一个科学，还是工程问题？** 
读者朋友们是不是有自己的答案了？ 
**时间？时间！** 
在脉冲神经网络 (Spiking neural network, SNN)领域，**我们将微分方程离散化，将dt转化成∆t，**于是我们就可以用简单的计算来近似神经元的复杂方程，可以运用计算机软件进行模拟，包括人工智能领域的框架如Pytorch进行加速。 
笔者不断提到“动力学特性”，读者朋友也一定注意到，神经元方程由电路模型推导而来，是微分方程的形式，这也直接决定了脉冲神经网络具有“时间”的核心特性。 
宇宙有时间尺度，人类在时间尺度中生活。 
  
宇宙大爆炸至今 
**所有的计算都不是凭空产生。** 
笔者在上文提到，“第一个问题可以仅在数学层面上回答”，这是第一步。 
**更进一步，****其实“计算”并不是一个束之高阁、高高在上、触摸不到的数学问题，它是一个物理过程。** 
**也就是说，所有的运算、逻辑，2+2，2-2，2*2，2/2，2^2，log 2，dy/dx，积分，与或非逻辑， 都在时间以及空间上耗费真实存在的物理资源进行计算。** 
我们大家能接触得到的计算机，基本都是General Purpose Computer。其中，CPU (Central Processing Unit)可以解码各种不同的指令，然后通过下图中的计算层级，一层一层的分配下去，用底层的通用的模拟电路、逻辑电路完成运算。 
  
计算机的不同层级。来源：Onur Mutlu, “Digital Design and Computer Architecture"。 
聪明的读者们一定可以想到，这么通用的CPU可以在每个任务上都表现的不错，但一定没办法在专用的任务上赢过专门为这个任务设计的芯片。这种芯片，就叫专用集成电路 (Application-Specific Integrated Circuit, ASIC)。 
所以，TrueNorth设计的七个原则中，最后一个是软件和硬件之间的一对一对应 (Hardware–Software One-to-One Equivalence)。这也是为什么，我们现在需要设计各种的芯片，比如层出不穷的人工智能AI芯片，而不是全部都依赖CPU/GPU。当然，通用和专用是两级，这中间具体的选择也是综合的平衡和取舍。 
**预告** 
那么，具体到神经元的模拟上，如果我们要设计一款专用的芯片，我们手上现在有一堆半导体，又需要用什么电路？模拟什么样的神经元？什么样的工作原理？多大程度上需要和这条曲线贴合？在下篇文章中，我们将继续就以下两个问题，尤其在硬件层面上，展开我们开源类脑的旅程： 
**一、我们从这条曲线里可以抽象出什么模式？** 
**二、在硬件和软件上分别如何复现这个模式？** 
  
参考资料 
*1. Wikipedia of Hodgkin–Huxley model, neuron, action potential, cell membrane, membrane transport, membrane proteinm, ion channel, *
 *Glucose transporter，**Biological neuron model，big bang, memristor, etc.*  
*2. Gerstner, W., Kistler, W. M., Naud, R., & Paninski, L. (2014). Neuronal dynamics: From single neurons to networks and models of cognition. Cambridge University Press.*  
*3. Merolla, P. A., Arthur, J. V., Alvarez-Icaza, R., Cassidy, A. S., Sawada, J., Akopyan, F., ... & Modha, D. S. (2014). A million spiking-neuron integrated circuit with a scalable co****mmunication network and interface. Science, 345(6197), 668-673.*  
*4. Akopyan, F., Sawada, J., Cassidy, A., Alvarez-Icaza, R., Arthur, J., Merolla, P., ... & Modha, D. S. (2015). Truenorth: Design and tool flow of a 65 mw 1 million neuron programmable neurosynaptic chip. IEEE transactions on computer-aided design of integrated circuits and systems, 34(10), 1537-1557.*  
*5. Maass, Wolfgang. "To spike or not to spike: that is the question." Proceedings of the IEEE 103.12 (2015): 2219-2224*  
*6. Fang, X., Liu, D., Duan, S., & Wang, L. (2022). Memristive lif spiking neuron model and its application in morse code. Frontiers in Neuroscience, 16, 853010.*  
*7. Chen, J., Qiu, X., Ding, C., & Wu, Y. (2022). SAR image classification based on spiking neural network through spike-time dependent plasticity and gradient descent. ISPRS Journal of Photogrammetry and Remote Sensing, 188, 109-124.*  
*8. Onur Mutlu, “Digital Design and Computer Architecture".*  
*9. open-neuromorphic.org*  
*10. https://www.creative-biolabs.com/blog/index.php/membrane-protein-overview/*  
*11. https://neuronaldynamics-exercises.readthedocs.io/en/latest/index.html*  
*12. https://snntorch.readthedocs.io/en/latest/*

---
**Tags:** [[BrainInspired]]
