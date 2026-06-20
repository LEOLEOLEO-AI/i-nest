---
title: 涌现的计算框架
tags:
- attention-mechanism
- chiplet
- concepts-theory
- dynamics
- embodied-ai
- emergence
- fundamentals
- large-language-model
- neural-networks
- neuroscience
---
> 笔记本: 我的剪贴板  
> 创建时间: 2024-06-14  

---

**年**初在[**大模型能使人类自由**](https://mp.weixin.qq.com/s?__biz=MzI2MjU4MDYwOA==&mid=2247486859&idx=1&sn=3b7220c79dc82d09ca20ffefdce8916e&scene=21#wechat_redirect)一文中，笔者开篇即强调：[**重整化与涌现是自然界的普遍规律**](https://mp.weixin.qq.com/s?__biz=MzI2MjU4MDYwOA==&mid=2247484728&idx=1&sn=be348a95917c99e9e1fbd3ea7411bf11&scene=21#wechat_redirect)。  
   
涌现是复杂系统中的集体现象或行为，这些现象或行为不存在于它们的各个部分中。  
   
陶哲轩也在致力于[**从复杂性中探索普适规律**](https://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247677712&idx=1&sn=7fa18001c7c31f09d5020aff87a9eb8d&scene=21#wechat_redirect)，“一个大型复杂系统的宏观行为几乎完全与其微观构造无关”，这让他着迷。  
  
“**一切问题都可以转化成数学问题**。” -- 笛卡尔。  
   
“长期以来，哲学家们一直在争论涌现，不停兜圈子”，英国萨塞克斯大学（University of Sussex）的神经科学家 Anil Seth说。  
   
Seth和著名复杂系统科学家Fernando Rosas等学者一起，提出了一个理解涌现如何产生的计算框架--《层次涌现的计算方法》【文献1】。  
   
现在，**涌现有了属于自己的数学框架**！！！  
   
   
   
学者们认为：理解复杂系统的功能结构，对于揭示其内部工作机制，并开发有效的预测和控制方法至关重要。笔者十分赞同，[**大模型的数学物理原理**](https://mp.weixin.qq.com/s?__biz=MzI2MjU4MDYwOA==&mid=2247487444&idx=1&sn=2c63902fca7ce7051c12af169c296e37&scene=21#wechat_redirect)，知其然还探究其所以然，并不只是兴趣使然。  
     
  
基于宏观过程如何表达自包含的信息、介入和计算属性的数学形式化方法，该框架揭示了一系列嵌套的自包含过程的层次结构，决定了在哪个层次上进行何种计算，从而勾画出复杂系统的功能结构。  
   
这种方法在统计力学和计算神经科学的典型模型中得以印证。该框架能帮助更深入地理解复杂系统的多层次结构，揭示可行的高效模拟、预测和控制的具体方式。  
   
笔者一句话概括该框架的内核：重整化作用于马尔可夫链，Markov Chain + Renormalization。  
   
首先，学者分别对微观过程与宏观过程做了马尔可夫链简化，并引入“ϵ机”描述宏观微观过程的状态迁移。  
   
   
   
接着，通过理论建模和推导，将现实空间（Real space）层间变换或态射 f，等价映射到，计算空间(Mechanism space) 因果态（Causal states）或隐藏态（Hidden states）之间的态射。  
   
   
   
从重整化理论的角度来看，微观和宏观过程的ε机可被视为一个“理论”或模型，作为对每个层次上观察到的统计模式的最好解释。  
   
下图表明，若计算上的封闭性成立，解释宏观层次的理论可以通过将解释较低层次的理论（或ε机器）做粗粒化来获得。    
  
   
也就是，计算上封闭的宏观层次完全可以用简化的、粗粒度版本的理论来描述，而不需要依赖完整的微观理论，即使这并不适用于任意宏观过程。  
   
   
   
粗粒化是有条件的，学者们的关键发现是，**可积性定义了微观过程涌现宏观过程的充分必要条件**：如果微观过程的因果状态具有很强的可积性，那么该微观过程就具有因果封闭的层次，而这为涌现敞开了大门。  
   
结合利用已经开发的用于经验上发现马尔可夫链可积分区的丰富成果，此框架方法易用于增强数据驱动的涌现粗粒化发现——技巧是在“真实空间”之外的因果状态空间上应用这些方法。  
   
笔者引申一下，Lumpability 可积性，粗粒化可以保持Markov性质。保持的一定需要是Markov性质吗？是否从能量的角度可以更广义？能量分布的可积性，信息熵分布的可积性，同样可导致粗粒度层次的封闭（closure）性质？  
   
封闭性质或闭包（closure）抽象了"同层次行为和特性不取决于细颗粒度层次的特性和行为"，也即**因果关系可以在较高层次上独立于较低层次的细节发挥作用**。  
   
正如，人体会在半年内更新掉身体98%组织的细胞。每半年后你都会拥有一个全新的身体，你已经不是你，但你还是你。在宏观层次上，你只是一个米田嵌入，尽管是动态的。  
     
  
   
   
统计力学中的经典扩散模型 Ehrenfest diffusion model, Ising 二元自旋模型，元胞自动机，随机游走网络和循环神经网络都可以验证这个计算框架。  
   
笔者[**Spin-Transformer数据雕刻自旋玻璃**](https://mp.weixin.qq.com/s?__biz=MzI2MjU4MDYwOA==&mid=2247486762&idx=1&sn=620c79d86f04f1b363d6b4e5bf5de0b5&scene=21#wechat_redirect)文中讲的Spin-Transformer可以作为这个框架的推演范例。而且在能量守恒的前提下，假定了可积性。  
   
统计力学中的经典扩散模型 Ehrenfest diffusion model：   
   
  
   
   
Ising 二元自旋模型：  
   
   
   
这里还要进一步区分两种类型的涌现：    
  
  
1.针对时序（time series）, 此涌现计算框架可以相当自然地，对应到重整化中的微观到介观到宏观不同层次的可积性，引发的宏观粗粒度层次的封闭特征与行为；  
  
2.针对语义（语言token）， 文本意义下，语义不同尺度的attention的叠加是否也是一种可积性？持续训练获取米田嵌入，构建范畴，非同质随机图连通性引发的涌现。   
  
当封闭特性Closure对应有意义的（人类可认知的）态射时，两种涌现等价？神经网络隐藏层部分晶格 (sub lattice)对应粗粒度化层的因果或信息闭包?  
   
   
   
此涌现计算框架，非常符合[**大模型的数理原理**](https://mp.weixin.qq.com/s?__biz=MzI2MjU4MDYwOA==&mid=2247487444&idx=1&sn=2c63902fca7ce7051c12af169c296e37&scene=21#wechat_redirect)的处理模式：  
   
1. 用于语言时，语义或信息熵的可积性，促成不同尺度层次的closure ( 词元token - 短语phrase- 段落paragraph - 文章article )，对应范畴视角下的米田嵌入各种关系的非同质随机图的从节点、碎片、局部、到整体的网络的语义联通性。  
   
2. 用于多媒体时序数据时，例如 SSM or Sora 等各种GPT , 时序序列的可积性，做粗粒度化，归一化能量分布或者信息熵分布，对应不同颗粒度的观测、模式提取或压缩，同样具备涌现的潜质。只不过[**压死骆驼需要提供最后一根稻草**](https://mp.weixin.qq.com/s?__biz=MzI2MjU4MDYwOA==&mid=2247487508&idx=1&sn=86ab38d12b0dc848055c2aec38533e6f&scene=21#wechat_redirect)。  
     
  
这个涌现计算框架，可积性基础上的粗粒度化，对语义和时序的粗粒度层次的涌现，就是笔者一直致力的，[**重整化驱动大模型的涌现**](https://mp.weixin.qq.com/s?__biz=MzI2MjU4MDYwOA==&mid=2247484547&idx=1&sn=65f4168165b6d852106c91a10caade58&scene=21#wechat_redirect)的过程：1重整化提取出范畴，2持续重整化驱动范畴相变，3跨范畴采样做变分推理。  
   
该涌现框架的理论推导、多个典型复杂范式模型的验证反映了其普适性。迄今为止，人们观测到的大模型的各种行为也都可以用笔者整理的数理框架加以合理解释，这同样印证了重整化与涌现的普适性。   
   
   
   
《生命的出现是预期的相变吗？》【文献2】，提出一种新的生命定义：**生命是康德式的整体（Kantian Whole）**，整体为部分而存在，部分为整体而存在，并通过整体而存在。  
   
生命实现了催化闭合（Catalytic Closure）、约束闭合（Constraint Closure）和空间闭合（Spatial Closure），这些closure确保了即使98%细胞更替，宏观层次上你还是你。  
   
能量守恒，信息守恒支撑了可积性，粗粒化细胞组装涌现为器官，与集体自催化集和邻近可能性的相互作用，表明**生命是宇宙演化中可预见的相变**。  
   
[**大模型能使人类自由**](https://mp.weixin.qq.com/s?__biz=MzI2MjU4MDYwOA==&mid=2247486859&idx=1&sn=3b7220c79dc82d09ca20ffefdce8916e&scene=21#wechat_redirect)，以重整化普适规律为核心的大模型，遵循能量守恒，信息守恒，融汇了人类知识和推理，已然涌现出神奇的能力，纵然不乏幻觉。具身能使她们实现空间闭合吗？！  
   
   
文献1：Software in the natural world: A computational approach to hierarchical emergence https://arxiv.org/abs/2402.09090  
     
  
文献2：Is the Emergence of Life an Expected Phase Transition in the Evolving Universe https://arxiv.org/abs/2401.09514

---
**Tags:** CST [[Chiplet]]

---
## 相关笔记 (AI 自动关联)
- [[涌现的计算方法：从计算力学到层级涌现]]
- [[什么是涌现？]]
- [[涌现动力学如何用来分析复杂系统？___新课上线]]
