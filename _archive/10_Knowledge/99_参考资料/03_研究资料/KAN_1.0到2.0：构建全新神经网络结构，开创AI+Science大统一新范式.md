# KAN 1.0到2.0：构建全新神经网络结构，开创AI+Science大统一新范式

> 笔记本: 我的剪贴板  
> 创建时间: 2024-09-20  

---

原文链接: [https://mp.weixin.qq.com/s/lS5yOCOynUl0BUbEtPK6VQ](https://mp.weixin.qq.com/s/lS5yOCOynUl0BUbEtPK6VQ)


**导语**


**今年4月，Max Tegmark 团队发布了一种崭新的深度学习网络结构 Kolmogorov-Arnold Network（简称KAN） 后迅速引起轰动，论文一作刘子鸣在集智俱乐部 AI+Science 读书会中详细介绍了团队的最新工作（参看：[KAN一作刘子鸣直播总结：KAN的能力边界和待解决的问题](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247690790&idx=1&sn=518f551f3b0c0c2cf50702204d416838&chksm=e898b0abdfef39bd95ff7594ba90364525db67da1834508dfd4ba6ea974cfd519c418b497b3a&scene=21#wechat_redirect)）。随后8月再次发布 KAN 的拓展工作 [KAN 2.0](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247697246&idx=2&sn=1a9aa1b5a7a2e3b344252b02702705ca&chksm=e89899d3dfef10c59eb66c6ef9147cc8ec3030b81152ae14c8fc2a98b1412c18f9e111a8fe62&scene=21#wechat_redirect)，呈现的不仅是一个优化升级的网络架构，更是一种 AI+Science 研究范式，这一范式使得 AI+Science 研究更具有交互性和可解释性，希望能够支持“好奇心驱动的科学”的发展。知名科普杂志 *Quanta Magazine* 近日撰文回顾梳理了 KAN 这一系列工作的研究历程，本文是对该文章的翻译。**

**


研究领域：AI+Science，深度学习，神经网络，AI可解释性**
**


**


Steve Nadis**| 作者**
龚铭康**| 译者**
“神经网络目前是人工智能中最强大的工具。当它们应用于更大的数据集时，没有什么可与之抗衡。”前沿理论物理研究所（Perimeter Institute for Theoretical Physics）研究员 Sebastian Wetzel 说道。

然而，长期以来神经网络存在一个缺点：被称为**多层感知器**（multilayer perceptron，MLP）的基本构建块是许多成功的神经网络的基础，但人类目前无法理解基于这些MLP的网络如何得出结果，或者是否有某种潜在的原理来解释这些结果。神经网络执行的惊人壮举被隐藏在“黑箱”背后，就像魔术师的表演一样。AI研究人员长期以来一直在思考，是否可能有一种不同类型的网络以更透明的方式提供同样可靠的结果。

2024年4月的一项研究提出了一种替代的神经网络设计，称为 **Kolmogorov-Arnold 网络**（Kolmogorov-Arnold network，KAN），它更透明，并且在某些问题类别中几乎可以完成常规神经网络的所有工作。它基于20世纪中叶的一个数学概念，已被重新发现并重新配置，以用于深度学习时代的应用。

尽管这一创新仅仅问世了几个月，这种新的设计已经在研究和编程社区中引起了广泛兴趣。“KANs更易于解释，可能特别适用于科学应用，在这些应用中它们可以从数据中提取科学规则。”约翰·霍普金斯大学的计算机科学家Alan Yuille说道，“它们是广泛应用的MLP的一个令人兴奋的新替代品。”研究人员已经开始学习如何最大限度地利用他们的新能力。


论文题目：KAN: Kolmogorov-Arnold Networks
论文地址：https://arxiv.org/abs/2404.19756
相关推文：《[KAN一作刘子鸣直播总结：KAN的能力边界和待解决的问题](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247690790&idx=1&sn=518f551f3b0c0c2cf50702204d416838&chksm=e898b0abdfef39bd95ff7594ba90364525db67da1834508dfd4ba6ea974cfd519c418b497b3a&scene=21#wechat_redirect)》

>> 在[AI+Science读书会](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247659349&idx=1&sn=5e0bcad718d122a04e1b34a8bf94f906&chksm=e89935d8dfeebcceb72a61c9c7602a6042eefad7bf106147d81c3110e04c6f61fbde5214aec9&scene=21#wechat_redirect)中，刘子鸣详细介绍了Max Tegmark团队的这项最新工作 。欢迎感兴趣的朋友扫码观看视频回放：


### 


**KAN：拟合“不可能”**


一个典型的神经网络这样工作：多层人工神经元（节点）通过人工突触（或边）相互连接。信息通过每一层进行处理并传递到下一层，直到最终输出。边被赋予不同的权重，权重较大的边比其他边具有更大的影响。在训练期间，这些权重不断调整，使网络的输出越来越接近正确答案。

神经网络的一个常见目标是找到让某些数据点最好地连接的数学函数或曲线。网络越接近该函数，其预测就越好，结果也就越准确。如果你的神经网络模拟某个物理过程，输出函数理想情况下将代表一个描述该物理过程的方程——相当于物理定律。

对于MLP，有一个数学定理告诉我们网络能多接近最优函数。它的一个结论是，MLP无法完美地表示该函数。但在适当的情况下，KAN可以做到。

KAN在函数拟合（连接网络输出的点）方式上与MLP有根本不同。**KAN不依赖具有数值权重的边，而是使用函数。这些边缘函数是非线性的，可以表示更复杂的曲线。**它们也是可学习的，因此可以比MLP的简单数值权重进行更灵敏的调整。

然而，在过去35年里，KAN一直被认为是不切实际的。1989年，由麻省理工学院的物理学家转计算神经科学家 Tomaso Poggio 参与撰写的一篇论文明确指出，KAN核心的数学思想“在网络学习的背景下是无关紧要的”。Poggio的一个顾虑可以追溯到 KAN 的核心数学概念。1957年，数学家 Andrey Kolmogorov 和 Vladimir Arnold 分别在论文中表明，如果你有一个使用多个变量的数学函数，可以将其转换为多个每个只包含一个变量的函数的组合。


Kolmogorov 关于该定理的论文：https://cs.uwaterloo.ca/~y328yu/classics/Kolmogorov57.pdf
Arnold 关于同一主题的论文：https://link.springer.com/chapter/10.1007/978-3-642-01742-1_2

然而，有一个重要的限制。定理生成的单变量函数可能不是“平滑的”，而是可能会有像V字形顶点一样尖锐的边缘。这对于任何试图使用该定理来重建多变量函数的网络来说都是一个问题。这些较简单的单变量部分需要是平滑的，以便在训练过程中能够正确地弯曲，从而匹配目标值。


Andrey Kolmogorov(左图)和Vladimir Arnold在1957年证明了可以将一个复杂的数学函数重写为简单函数的组合。
所以KANs看起来前景暗淡——直到今年一月某个寒冷的日子，麻省理工学院的物理学研究生刘子鸣决定重新审视这个主题。他和他的导师、麻省理工学院的物理学家Max Tegmark一直在研究如何让神经网络在科学应用中更易理解——希望能够窥探黑箱内部——但进展并不顺利。出于无奈，刘子鸣决定研究 Kolmogorov-Arnold 定理。“为什么不试试，看看它是如何工作的，即使过去人们没有给予它太多的关注？”


刘子鸣利用Kolmogorov-Arnold定理构建了一种新的神经网络。

Tegmark 熟悉 Poggio 的论文，认为这一尝试会再次陷入死胡同。但刘子鸣并未气馁，而 Tegmark 也很快改变了想法。他们认识到，即使定理生成的单值函数不平滑，网络仍然可以用平滑函数来逼近它们。他们进一步理解到，科学中我们遇到的大多数函数都是平滑的，这使得完美（而非近似）的表示或许是可实现的。

刘子鸣不想在没有尝试的情况下放弃这个想法，因为他知道自 Poggio 的论文问世35年来，软件和硬件已经取得了巨大进步。从计算角度来看，2024年许多事情是1989年无法想象的。

刘子鸣围绕这个想法工作了大约一周，在此期间他开发了一些原型 KAN 系统，所有这些系统都只有两层——这是最简单的网络，也是几十年来研究人员专注的类型。两层的 KAN 似乎是显而易见的选择，因为 Kolmogorov-Arnold 定理本质上为这种结构提供了蓝图。该定理特别将多变量函数分解为不同的内部函数和外部函数集。（这些函数代替MLP中权重的边的激活函数。）这种安排自然适合于具有内层和外层神经元的KAN结构——这是简单神经网络的常见安排。

但令刘子鸣沮丧的是，他的原型都没有如设想的在科学相关的任务中表现出色。Tegmark随后提出了一个关键建议：为什么不试试两层以上的KAN，它或许能够处理更复杂的任务？


刘子鸣的导师 Max Tegmark 提出了使Kolmogorov-Arnold网络成功运行的关键建议：为什么不建立一个两层以上的KAN ?

这个跳出框架的想法是他们所需要的突破。刘子鸣的新型网络架构开始展现出潜力，因此两人很快联系了麻省理工学院、加州理工学院和东北大学的同事。他们希望团队中有数学家，以及他们计划使用KAN分析的领域中的专家。

在四月份的论文中，该团队展示了三层KAN确实是可行的，并提供了一个三层KAN可以精确表示某个函数的例子（而两层KAN无法做到）。他们并没有止步于此。团队此后进行了最多六层的实验，随着每一层的增加，网络能够对齐更复杂的输出函数。“我们发现可以基本上随意堆叠层数。”论文的合著者之一Yixuan Wang说道。

### 


**来自数学和凝聚态物理的实验验证**


研究人员还将他们的网络应用于两个现实世界的问题。第一个问题涉及一个称为**纽结理论**（knot theory）的数学分支。2021年，DeepMind 的一个团队宣布他们构建了一个MLP，能够在输入足够多纽结的其他属性后，预测给定纽结的某一拓扑属性。三年后，新的 KAN 重复了这一壮举。然后它更进一步展示了预测的属性如何与所有其他属性相关联——刘子鸣表示，这是“MLP完全无法做到的”。

第二个问题涉及凝聚态物理学中称为**安德森局域化**（Anderson localization）的现象。目标是预测发生特定相变的边界，然后确定描述该过程的数学公式。没有任何MLP能够做到这一点，而KAN做到了。

但KAN相比于其他形式的神经网络的最大优势，及其最近进展的主要动机，在于其可解释性，Tegmark解释说。在这两个例子中，KAN不仅给出了答案，还提供了解释。“什么叫可解释性？”他问道。“如果你给我一些数据，我会给你一个可以写在T恤上的公式。”
约翰霍普金斯大学的物理学家Brice Ménard说，KAN的这种能力尽管目前还有限，但表明这些网络理论上可能会教给我们一些关于世界的新知识。“如果问题实际上可以由一个简单的方程来描述，KAN网络非常擅长找到它，”他说。但他警告说，KAN最适合的领域可能仅限于物理学中的问题——这些问题的方程通常只有很少的变量。

刘子鸣和Tegmark同意这一点，但并不认为这是一个缺点。“几乎所有著名的科学公式——比如 E=mc² ——都可以用一两个变量的函数来表示。”Tegmark说，“我们所做的大多数计算都依赖于一个或两个变量。KAN 利用了这一事实，并寻找这种形式的解决方案。”
### 


**KAN 2.0：推动好奇心驱动的科学**


刘子鸣和 Tegmark 的 KAN 论文迅速引起轰动，在大约三个月内获得了75次引用。不久之后，其他研究小组也开始开发自己的KAN。清华大学的王一政和其他人撰写的一篇论文在六月上线，显示他们的** Kolmogorov-Arnold 启发的神经网络**（Kolmogorov-Arnold-informed neural network，KINN）“在求解偏微分方程（PDEs）方面显著优于MLP”。


论文题目：Kolmogorov Arnold Informed neural network: A physics-informed deep learning framework for solving forward and inverse problems based on Kolmogorov Arnold Networks
论文地址：https://arxiv.org/abs/2406.11045
新加坡国立大学研究人员在七月发布的一篇论文得出的结论更为复杂。他们发现：**KAN****在与可解释性相关的任务中表现优于MLP，但MLP在计算机视觉和音频处理方面表现更好。两者在自然语言处理和其他机器学习任务上大致相等。**对于刘子鸣来说，这些结果并不令人惊讶，因为最初KAN团队的重点一直是“与科学相关的任务”，在这些任务中可解释性是首要优先事项。


论文题目：KAN or MLP: A Fairer Comparison
论文地址：https://arxiv.org/abs/2407.16674

与此同时，刘子鸣正在努力使 KAN 更实用，更易于使用。在八月份，他和合作者发布了一篇新论文，称为“KAN 2.0”，他将其描述为“更像是一本用户手册，而不是传统的论文”。刘子鸣表示，这个版本更易于用户使用，并提供了原始模型中缺乏的乘法工具等功能。


论文题目：KAN 2.0: Kolmogorov-Arnold Networks Meet Science
论文地址：https://arxiv.org/abs/2408.10205
相关推文：[KAN 2.0 震撼发布：构建AI+Science大统一的新范式](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247697246&idx=2&sn=1a9aa1b5a7a2e3b344252b02702705ca&chksm=e89899d3dfef10c59eb66c6ef9147cc8ec3030b81152ae14c8fc2a98b1412c18f9e111a8fe62&scene=21#wechat_redirect)

他和他的合著者认为，这种类型的网络不仅仅是达到目的的一种手段。KANs 促进了该团队所称的“**好奇心驱动的科学**”，这与长期以来主导机器学习的“**应用驱动科学**”相辅相成。例如，在观察天体运动时，应用驱动的研究人员专注于预测它们的未来状态，而好奇心驱动的研究人员则希望揭示运动背后的物理学原理。刘子鸣希望，通过KANs，研究人员可以从神经网络中获得更多，不仅仅是帮助解决棘手的计算问题。他们可以专注于纯粹为了理解而去研究。


本文翻译自 Quanta Magazine，原文链接：
https://www.quantamagazine.org/novel-architecture-makes-neural-networks-more-understandable-20240911/


**AI+Science 读书会**
AI+Science 是近年兴起的将人工智能和科学相结合的一种趋势。一方面是 AI for Science，机器学习和其他 AI 技术可以用来解决科学研究中的问题，从预测天气和蛋白质结构，到模拟星系碰撞、设计优化核聚变反应堆，甚至像科学家一样进行科学发现，被称为科学发现的“第五范式”。另一方面是 Science for AI，科学尤其是物理学中的规律和思想启发机器学习理论，为人工智能的发展提供全新的视角和方法。
集智俱乐部联合斯坦福大学计算机科学系博士后研究员吴泰霖（Jure Leskovec 教授指导）、哈佛量子计划研究员扈鸿业、麻省理工学院物理系博士生刘子鸣（Max Tegmark 教授指导），共同发起以[“AI+Science](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247659349&idx=1&sn=5e0bcad718d122a04e1b34a8bf94f906&chksm=e89935d8dfeebcceb72a61c9c7602a6042eefad7bf106147d81c3110e04c6f61fbde5214aec9&scene=21#wechat_redirect)”为主题的读书会，探讨该领域的重要问题，共学共研相关文献。读书会已完结，现在报名可加入社群并解锁回放视频权限。

详情请见：
[人工智能和科学发现相互赋能的新范式：AI+Science 读书会启动](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247659349&idx=1&sn=5e0bcad718d122a04e1b34a8bf94f906&chksm=e89935d8dfeebcceb72a61c9c7602a6042eefad7bf106147d81c3110e04c6f61fbde5214aec9&scene=21#wechat_redirect)
**推荐阅读**
**1. ****[KAN一作刘子鸣直播总结：KAN的能力边界和待解决的问题](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247690790&idx=1&sn=518f551f3b0c0c2cf50702204d416838&chksm=e898b0abdfef39bd95ff7594ba90364525db67da1834508dfd4ba6ea974cfd519c418b497b3a&scene=21#wechat_redirect)**
**2. ****[KAN 2.0 震撼发布：构建AI+Science大统一的新范式](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247697246&idx=2&sn=1a9aa1b5a7a2e3b344252b02702705ca&chksm=e89899d3dfef10c59eb66c6ef9147cc8ec3030b81152ae14c8fc2a98b1412c18f9e111a8fe62&scene=21#wechat_redirect)**
**3. ****[无心插柳：苏联数学家柯尔莫哥洛夫与神经网络的新生](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247690447&idx=4&sn=112085b5d8dc9a105bd1821f8ee5da3b&chksm=e898b242dfef3b54eeb13a35812a2c9ada58dc29f3d4d2dddfc4b912e83378106c6b3e8c327b&scene=21#wechat_redirect)**
**4. ****[张江：第三代人工智能技术基础——从可微分编程到因果推理 | 集智学园全新课程](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247667315&idx=1&sn=fca3a09806e753fa83d3fd6eb8ccf9d8&chksm=e89914fedfee9de82ae7107592b173d2a1c35141fab0006d3eac2dcb2dd1e74aa78a86e09a93&scene=21#wechat_redirect)**
**5.****[龙年大运起，学习正当时！解锁集智全站内容，开启新年学习计划](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247684525&idx=1&sn=bee7098c0fdf998e7efd72def2442287&chksm=e8994b20dfeec2360074b521111d22ada050fec084bd381175d2ffd708e31b3f94482be0daee&scene=21#wechat_redirect)******
**6. **[**加入集智，一起复杂！**](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247667297&idx=2&sn=988b7314df45d949e69e81257801fff2&chksm=e89914ecdfee9dfac76f9245fb1fd0e5b25d567e20790fbdab671234588ad0e88e1acf205711&scene=21#wechat_redirect)
**点击“阅读原文”，报名读书会**

---
**Tags:** [[CST]] [[Chiplet]]
