# Nature子刊进展：结合神经科学和计算机科学构建通用类脑计算

> 笔记本: 我的剪贴板  
> 创建时间: 2025-01-29  

---

原文链接: [https://mp.weixin.qq.com/s/jD2DepGhuEyaGEAcpLOQeQ](https://mp.weixin.qq.com/s/jD2DepGhuEyaGEAcpLOQeQ)


**
关键词：类脑计算，神经形态计算，通用脑启发计算，神经仿真，忆阻器，高性能计算**
****

**


论文题目：The development of general-purpose brain-inspired computing
论文地址：https://www.nature.com/articles/s41928-024-01277-y
期刊名称：*Nature Electronics*
近年来，随着类脑计算的发展，神经形态计算逐渐成为人工智能领域的重要研究方向。然而，传统的脑启发计算系统主要针对特定任务进行优化，例如图像处理或信号识别，这种专用性使其在面对多样化任务时表现有限。近期发表在*Nature Electronics*的一篇观点性文章，提出了通用脑启发计算**（General-Purpose Brain-Inspired Computing, GPBIC）的概念，旨在融合神经科学与计算科学的优势，构建一个能够应对多种任务需求的通用计算平台。
通用脑启发计算的核心目标是结合现代计算的精确性与控制流能力，以及脑启发计算中的数据流优势，构建兼具灵活性与高效性的计算模型。这种模型需要解决三大核心挑战：功能的多样性、负载的多样性以及性能的多样性。为了应对这些挑战，研究从硬件、软件到应用层面提出了系统化的解决方案。
在**硬件层面**，文章提出，利用如忆阻器和光学存储器的后CMOS技术，设计高效的神经形态芯片。这些新兴技术能够更好地模拟生物神经元的动态特性，提高能量效率的同时，还支持动态拓扑结构的灵活性。此外，结合传统的通用处理器，如CPU或FPGA，提出异构架构设计，以实现不同任务的协同处理，不仅提升了硬件的扩展性，还显著增强系统对复杂任务的适应能力。
在**软件层面**的创新则集中在系统框架的通用性上。文章提出了一种“神经形态自动机”的模型，这种模型能够同时支持空间计算、时间计算和多精度计算的任务需求。通过构建通用的编程框架和灵活的运行时环境，该模型能够在硬件与算法之间建立高效的通信桥梁，实现任务需求与硬件性能的深度适配。此外，开发领域无关的编译工具链，用户可以更加高效地开发和部署多样化的应用。
在**应用层面**，文章探讨了通用脑启发计算在模式泛化上的潜力。从脉冲神经网络和人工神经网络的优化开始，一步步扩展到高性能计算、图处理和多智能体模拟等在内的复杂任务场景。这些任务的共同特点是需要强大的并行计算能力和高效的数据流处理，而脑启发计算的低精度容错性和时间空间并行特性为这些需求提供了天然的支持。
实验结果表明，通用脑启发计算在硬件性能和任务适应性方面均表现出显著优势。通过引入忆阻器技术，研究团队在矩阵乘法任务上实现了能量效率的显著提升。此外，通过时空编码和丰富的连接模式，提出了时间-空间弹性（TST Elasticity）这一框架，使得系统能够动态调整计算资源和任务调度，从而满足不同场景下的任务需求。
这项研究的意义不仅在于提出了全新的通用计算框架，还为人工智能和脑科学的交叉研究提供了新的视角。通用脑启发计算的实现，不仅可能为下一代智能系统提供技术支撑，还可能推动人类对大脑信息处理机制的进一步理解。未来，随着硬件抽象层的完善和软件生态的进一步优化，通用脑启发计算有望在人工智能、类脑计算和高性能计算领域释放更大的潜力。

图 1. 脑启发计算的指导范式和应用。

图2. 脑启发计算的硬件和软件进展。

图3. 大规模脑启发计算系统。

图4. 融合大脑和计算机的关键特征。


**NeuroAI读书会**


详情请见：
**[NeuroAI 读书会启动：探索神经科学与人工智能的前沿交叉领域](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247645814&idx=1&sn=cdb37d5aa7a4b2827c39d7d9e476d625&chksm=e899e0fbdfee69edf3e7c9be3479303189d39c3b1fae33370176ba1767133bba6eadf32b77db&scene=21#wechat_redirect)******

**推荐阅读**
**1. ****[人类智能如何从大脑中涌现？大脑精细模拟重塑 NeuroAI 范式](https://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247707053&idx=1&sn=411556b792c735420711efd48aa0048d&scene=21#wechat_redirect)****
2. ****[类脑计算模型登Nature子刊：受大脑启发的人工树突网络，实现高能效AI](https://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247694452&idx=3&sn=b696207237e8a201282bb55e101aeb9b&scene=21#wechat_redirect)****
3. ****[从复杂神经动力学到智能涌现：基于神经复杂性的类脑人工智能](https://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247688654&idx=1&sn=3854aa0e6287e373c00e05649f406a3f&scene=21#wechat_redirect)****
4. ****[张江：第三代人工智能技术基础——从可微分编程到因果推理 | 集智学园全新课程](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247667315&idx=1&sn=fca3a09806e753fa83d3fd6eb8ccf9d8&chksm=e89914fedfee9de82ae7107592b173d2a1c35141fab0006d3eac2dcb2dd1e74aa78a86e09a93&scene=21#wechat_redirect)**
**5. ****[龙年大运起，学习正当时！解锁集智全站内容，开启新年学习计划](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247684525&idx=1&sn=bee7098c0fdf998e7efd72def2442287&chksm=e8994b20dfeec2360074b521111d22ada050fec084bd381175d2ffd708e31b3f94482be0daee&scene=21#wechat_redirect)**
**6. **[**加入集智，一起复杂！**](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247667297&idx=2&sn=988b7314df45d949e69e81257801fff2&chksm=e89914ecdfee9dfac76f9245fb1fd0e5b25d567e20790fbdab671234588ad0e88e1acf205711&scene=21#wechat_redirect)
点击“阅读原文”，报名读书会

---
**Tags:** #BrainInspired #CST #Chiplet
