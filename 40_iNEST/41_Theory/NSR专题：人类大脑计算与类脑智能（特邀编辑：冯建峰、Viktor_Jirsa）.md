# NSR专题：人类大脑计算与类脑智能（特邀编辑：冯建峰、Viktor Jirsa）

> 笔记本: 我的剪贴板  
> 创建时间: 2024-06-23  

---

本文转载自公众号“中国科学杂志社”
 

  

 

 
《国家科学评论》（National Science Review，NSR）今年第5期出版了“人类大脑计算与类脑智能”专题（Special Topic: Human Brain Computing and Brain-inspired Intellegence），专题特邀编辑为复旦大学冯建峰教授和法国艾克斯-马赛大学Viktor Jirsa教授。本专题共收录10篇文章，包含1篇Editorial、3篇Perspective、3篇Research Article、2篇Review和1篇Interview，展示了该领域的发展现状及其未来方向。  

   
 

 

  

 
**ISTBI**  

  
 


 

**/ ****编者按 /** 
 

 
 

**人类大脑计算与类脑智能**
冯建峰（复旦大学）、Viktor Jirsa（法国艾克斯-马赛大学）、卢文联（复旦大学）
人类大脑中，结构、功能以及神经动力学之间的关系复杂，且涉及到多个学科的各个方面。对这些关系的理解是脑科学研究的一个基本目标，并可能是通往下一代人工智能的道路。**本期NSR“人类大脑计算与类脑智能”专题涉及了该领域中的几个重大挑战性问题。**
首先，鉴于人脑的神经元规模、神经形态细节和连接拓扑结构的复杂性，**建立人脑的计算神经网络模型**是极其困难的。人类大脑是一个极其复杂的器官，拥有860亿个神经元和100万亿个突触，这让所有人造智能的尝试——比如大语言模型——都相形见绌。对大脑的不同尺度、不同规模进行详尽细致的结构与连接的建模，在数学上是一项不可能完成的任务。由此产生的一个问题是：多尺度结构在多大程度是实现大脑功能的必要条件？因此，绘制全连接组（包括所有神经连接的综合图谱）是当前研究的优先事项，而破译每个大脑区域的功能更是重大挑战。
在介观尺度上，Maass在Perspective文章中提出并讨论了皮层微电路（cortical microcircuits, CMs）的基本原理，这些原理可以帮助我们理解皮层计算，并可能启发产生某种本质上更像大脑和更节能的计算框架。在微观尺度上，Senden等人对混合整合大脑模型（hybrid integrative brain models）进行了综述。这类模型以模块化的方式整合了大脑、身体和环境之间复杂的相互作用，并包含通过丘脑等枢纽结构来调节的类似注意力机制等的整体性过程。为了进一步分析这种相互作用，Vohryzek等人从基于体素的结构矩阵的归一化拉普拉斯算子的本征函数出发，提出了用于fMRI的时空谐波分解（Harmonic Decomposition of Spacetime, HADES）框架。由此，作者发现致幻剂作用下存在明确的谐波模式和功能性的谐波变化。
其次，神经形态计算采用建设性的“构建用以理解”（build to understand）方法来表达大脑的结构-功能二分性，旨在设计和实现人类大脑结构和功能启发的计算系统。当然，要复制出类似于人类大脑规模和实时计算能力的复杂神经网络，需要开发能够精确模仿并行和分布式神经信息处理机制的硬件，这些硬件还应当具有与大脑相当的能量效率。因此，设计和制造神经形态芯片是实现具有人类大脑规模和复杂性的神经网络的必由之路。
本专题报道并发布的最新版达尔文3（Darwin3），是一种神经形态专用指令集和高密度连接存储技术。它将单位芯片负载神经元数量提升至超过200万，还具有强大的不同模型支持能力和可编程性的学习能力。近期神经形态计算系统的研究焦点主要集中在脑科学方向。但此类系统也正在将其范围扩展到具有工程应用的通用人工智能（AGI）领域。该方向的一个值得注意的案例是混合神经网络（Hybrid Neural Network, HNN），它集成了面向计算机科学的人工神经网络和面向神经科学的脉冲神经网络。新一代神经形态系统的主要特征就是支持HNN。例如，第二代Spinnaker（Spinnaker2）与其第一代相比在功能密度和能量效率方面都有超过一个数量级的改进，并支持HNN，引领了节能型先进人工智能的发展。甚至于，事件驱动的稀疏大语言模型也即将浮出水面。
第三，**人类大脑计算模型的临床应用**也是脑科学的前沿问题，亟需要开发新的科学有效的方法。数字孪生脑（digital twin brain, DTB）的概念和技术被用于描述生物脑结构、计算过程和智能功能的数字化表示。这将为数字化测试各种认知行为和医学方法提供平台，而这些测试常常是无法在真实的生物体上进行的。然而，临床应用要求需要个体化的数字化表示。为此，虚拟孪生脑（Virtual Brain Twin, VBT）提出了一种个性化的全脑网络模型，该模型是通过个体的大脑成像数据构建的。王慧芳等人的专题文章提出，该模型给出描述五种大脑疾病相关参数的空间掩码，并基于生理学和病理生理学假设证明了其临床应用潜力。冯建峰课题组的专题封面文章提出的数字孪生脑平台，构建脉冲神经元网络，达到了全脑规模，拥有多达200亿个神经元，并包含大脑结构数据作为结构。数字孪生脑的特色是以逆向工程方法提供了数据同化的范式。作者通过此方法发现，在神经元网络规模和结构上越接近真实大脑，模型与真实大脑之间的相似性就越大——无论在静息状态还是任务态，都是如此。这在一定程度上（首次）揭示了在计算模型与人类大脑在规模和结构细节的相似性，是探索有生物学意义的类脑智能的必要条件。
**综上所述，模型、数据和算力，**是探索大脑计算基本原理的必要因素。例如，自由能原理依托大脑计算的贝叶斯假设，而该假设需要通过这些领域中的诸多机制的结合才能实现。大脑计算的贝叶斯机制为理解真实智能提供了一条独特的路线图，指向了类脑智能发展的重要方向。 
 
 

 

    

 
**专题篇目**
 

   

 

   
 

 

**GUEST EDITORIAL**  
 

**Human brain computing and brain-inspired intelligence**
**人类大脑计算与类脑智能**
作者：冯建峰（复旦大学）、Viktor Jirsa（法国艾克斯-马赛大学）、卢文联（复旦大学） 
 

 
   

 
   

 
  
 

https://doi.org/10.1093/nsr/nwae144 
 

 

**PERSPECTIVE**  
 

**Digital neuromorphic technology—current and future prospects**
**数字式类脑技术—现状与前景**
通讯作者：Steve Furber（英国曼彻斯特大学） 
 
 
 

https://doi.org/10.1093/nsr/nwad283
数字式类脑技术可以为模拟式类脑技术提供有效的补充，它的显著的优势是能兼容最先进的芯片制造技术。本文介绍了数字式类脑技术的现状和前景。当前主要数字式类脑平台包括Intel公司的Loihi、曼彻斯特大学的SpiNNaker和清华大学的天机。相应的软件平台（PyNN）可用来描述触发式神经网络。 
 

**How can neuromorphic hardware attain brain-like functional capabilities?**
**神经形态硬件如何实现类脑功能？**
通讯作者：Wolfgang Maass（奥地利格拉茨技术大学） 
 
 
 

https://doi.org/10.1093/nsr/nwad301
为什么大多数脉冲神经网络模型的“生物性”都不强？如何使神经形态硬件获得类脑功能？本文中，作者提出了将皮层微电路制成神经形态硬件的4个设计原则，为下一代神经形态硬件设计提供思路。 
 

**Modular-integrative modeling: A new framework for building brain models that blend biological realism and functional performance**
**模块化综合建模：一种融合了生物学事实与功能性表现的构建大脑模型的新框架**
通讯作者：Mario Senden（荷兰马斯特里赫特大学） 
 
 
 

https://doi.org/10.1093/nsr/nwad318
本文提出了模块化综合建模方法，这一神经科学领域的新框架可以将生物学事实与功能性表现相结合，以构建大脑模型，其所提供的整体图景可以展示大脑功能与身体和环境的相互作用。 
 

 

**RESEARCH ARTICLE**  
 

**Imitating and exploring human brain's resting and task-performing states via resembling brain computing: scaling and architecture**
**类脑计算模拟和探索人类大脑的静息和任务状态：尺度与结构**
通讯作者：冯建峰（复旦大学） 
 
 
 

https://doi.org/10.109‍3/nsr/nwae080
数字孪生脑是国际上首个基于数据同化方法开发的具备860亿神经元规模、百万亿突触的全人脑尺度大脑模拟平台，开展数字化的大脑认知与医学应用研究，探索全脑结构与脑功能的关系，为下一步真正意义上跨越大脑模型和类脑智能鸿沟提供重要研究手段。本文研究发现，数字孪生脑在50亿神经元规模的大模型上，会逐渐展现出类似在人脑中观测到的临界现象与相似的认知功能。
[【中文报道】复旦冯建峰组NSR｜全脑规模数字孪生脑平台，探索脑结构与脑功能的关系](https://mp.weixin.qq.com/s?__biz=MzA3MzQ5MzQyNA==&mid=2656842715&idx=1&sn=a8bffebb872666cf7b2eac391a042852&scene=21#wechat_redirect) 
 

**Darwin3: a large-scale neuromorphic chip with a novel ISA and on-chip learning**
**达尔文3：支持新颖指令集架构和片上学习的大规模神经拟态类脑芯片**
通讯作者：潘纲（浙江大学） 
 
 
 

https://doi.org/10.1093/nsr/nwae102‍
本文展示了一款支持新颖类脑专用指令集的大规模类脑计算芯片——达尔文3。能够支持200万以上神经元和1亿以上神经突触，具备灵活的片上学习和芯片级扩展能力，通过专用指令编程能够高效实现不同类型的神经元和突触，运行多种脉冲神经网络模型，对探索新型的人工智能算力基座具有重要的意义。实验结果表明，达尔文3与国内外其它类脑芯片相比在神经元规模、突触存储密度、推理学习任务的效率与准确性等方面都具有优势。
[【中文报道】大规模类脑芯片“达尔文3”：支持专用指令集与在线学习 | NSR](https://mp.weixin.qq.com/s?__biz=MzA3MzQ5MzQyNA==&mid=2656842075&idx=1&sn=ad57442b62be27345fa2ab978b7674b6&scene=21#wechat_redirect) 
 

**The flattening of spacetime hierarchy of the DMT brain state is characterised by harmonic decomposition of spacetime (HADES) framework**
**DMT大脑状态时空层次的扁平化以时空谐波分解（HADES）框架为特征**
通讯作者：Jakub Vohryzek（英国牛津大学） 
 
 
 

https://doi.org/10.1093/nsr/nwae124
本研究设计了全新的时空谐波分解（HADES）框架，该框架可以描述大脑各区域中谐波模式随时间的变化。利用HADES，作者对健康人大脑在5-羟色胺能迷幻剂N，N-二甲基色胺（DMT）作用下的时空层级变化进行了精准的动态描述。 
 

 

**REVIEW**  
 

**Advancing brain-inspired computing with Hybrid Neural networks**
**以混合神经网络推进类脑计算**
通讯作者：赵蓉（清华大学） 
 
 
 

https://doi.org/10.1093/nsr/nwae066‍
“混合神经网络”（HNN）融合人工神经网络（ANN）和脉冲神经网络（SNN），将为人工智能注入新的活力。本文对其起源、架构和支持系统等进行全面综述，并提出未来研究方向。
[【中文报道】清华大学团队NSR综述：混合神经网络（ANN+SNN→HNN）推动类脑计算](https://mp.weixin.qq.com/s?__biz=MzIzNzE2NDQ1MA==&mid=2650761192&idx=1&sn=968e863641ea867309bde84ff5680993&scene=21#wechat_redirect) 
 

**Virtual brain twins: from basic neuroscience to clinical use**
**虚拟孪生大脑：从基础神经科学到临床应用**
通讯作者：王慧芳、Viktor K Jirsa（法国艾克斯-马赛大学） 
 

 
   

 
  
 

https://doi.org/10.1093/nsr/nwae079
虚拟孪生大脑以个人大脑成像数据为基础，构建出能准确反映个体大脑状态的个性化、生成式、适应性数学模型，在科学研究和临床诊疗中具有重要应用前景。这篇综述对其在各种脑部疾病中的应用进行详细介绍。 
 

 

**INTERVIEW**  
 

**Bayesian brain computing and the free-energy principle: an interview with Karl Friston**
**贝叶斯大脑计算与自由能原理——专访Karl Friston**
通讯作者：卢文联（复旦大学） 
 
 
 

https://doi.org/10.1093/nsr/nwae025 
 

NSR专访理论神经科学家、脑成像领域权威专家Karl Friston。Friston提出的自由能原理以及与之相关的贝叶斯大脑假说，为理解和发展类脑计算、类脑智能提供了一条独特的途径。
[【访谈中文版】贝叶斯脑计算与自由能原理：Karl Friston访谈 | NSR](https://mp.weixin.qq.com/s?__biz=MzA3MzQ5MzQyNA==&mid=2656841603&idx=1&sn=d71c862f7065db419f5b0cd75d7c61ea&scene=21#wechat_redirect) 
 
 
 
 

 

 

 

**ISTBI** 
 
   

 

 

**ISTBI**   

 

  
 

 
**扫描二维码****关注我们** 
复旦大学 
类脑智能科学与技术研究院

---
**Tags:** #BrainInspired
