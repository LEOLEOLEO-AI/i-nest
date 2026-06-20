---
title: "层次化推理模型（HRM）：突破LLM推理瓶颈的脑启发式架构"
source: "https://mp.weixin.qq.com/s/4uH2RhfJTTs8CBZVuogDxA"
created: 2025-09-05
note_id: "1886624937364589768"
tags:
  - "AI链接笔记"
  - "层次化推理模型"
  - "隐推理范式"
  - "认知科学AI"
  - "get-笔记"
  - "AI研究"
---

# 层次化推理模型（HRM）：突破LLM推理瓶颈的脑启发式架构

## 摘要

🧠 **LLM推理范式的局限性**   当前大型语言模型（LLMs）依赖思维链（CoT）技术，但存在三大核心挑战：   - **任务规划脆弱性**：依赖人工定义或原生推理泛化能力，缺乏灵活的内部结构自适应与回溯机制   - **数据需求高昂**：需大量结构化标注数据，面临高质量数据源稀缺与强化学习奖

## 正文

“推理·Reasonning”作为当前人工智能的下一个核心挑战，它要求模型能够设计并执行复杂的、跨多搜索路径的、多阶段多步骤、目标导向的行动&决策序列。当前的大型语言模型（LLMs）依赖于“思维链”（Chain-of-Thought, CoT）等技术，通过将复杂任务分解为简单的中间步骤，并逐步生成文本输出，即通过自回归（AR）CoT指令微调或强化学习奖励建模机制将推理过程外化为token级别的语言表达，然而，这种方法也许存在着一些显著的局限性。

记得在两年前，当业界基于当时的LLMs提出其能否像人类那样进行系统Ⅱ·慢思考step by step reasonning或模拟人类chain of thought假设时，自己也在持续尝试思考LLMs这种生成式自回归（AR）next token predict建模方式和其模型本身的Transformer网络结构对于“慢思考”推理范式的天然适配性问题，甚至也尝试过很多思想实验试图将Transformer+AR范式与人类各种认知推理范式统一起来。

如在去年的这个时候，临时思考并记录下的上、下两篇图文笔记中：[Thinking·快与慢的统一认知框架探索 上篇](https://mp.weixin.qq.com/s?__biz=MzkxOTY2MjE3Nw==&mid=2247484575&idx=1&sn=e082c589bbb3c5c01293cc05d4febc41&scene=21#wechat_redirect) 描述了这样几段不太成熟的假设陈述：

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd3266173efc27fde3adbe8823e9ecb85?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=VYXTOXOKVPkafsZ59g5WDixaQXE%3D)

“针对于systemⅡ的COT或TOT等思维链端到端的尝试性窥见.其模型的两端，输入侧与生成侧均是基于离散的语言符号在开放性tokenize空间中编织merge在一起的，直觉上与当前LLM·system1的自回归next token predict在推理本上质是等价的，稍有一点的差别也许是序列化token的生成所表征的这种长链模式其复杂度会更抽象，且在经过合理且理想化的学习与训练框架之后，不论体现在显性的内容生成的过程+结果上还是将其中的过程隐含在模型网络神经元的信号激活与传递中，其中均蕴含着复杂而多样的长链过程模式(long patterns)。”

“...但是需要注意的是：虽然e2e下的system Ⅱ模型中间隐层中神经元激活信号传递路径中的信息变换过程中（本质上是数学变换）也许仍是黑盒不可解释的，但近似于真实世界中的形式化显性模式历经中间过程到最终结果所蕴含的因果链理论上是能够近似拟合的(取决于学习目标与优化策略)，即被其中模型参数中间隐层与输出层各激活状态及传导带来的信息复杂变换所拟合（如MLP或KAN的B样条曲线spline）。”

“另外，对于E2E的systemⅡ的推理模型网络结构的选择与设计，也许需要依据直觉或加入先验经验（类似transformer那种类人注意力机制的理性洞察）对模型网络结构进行重整与设计，transformer/Manba/TTT也好，MOE/Dence也罢，或者深入到muti-head层，甚至对生成式自回归·AR的next token prediction下联合条件概率预测与Diffusion下的token扩散思想进行底层结构的改良统一，以促使关键表征或表征组合被模型有效捕捉到并有效传递遍布到多层更深或更宽广的神经网络上，直觉上分析数学与拓扑学更深刻的理论支撑或两者结合，也许能够在未来帮助我们对神经网络结构的更进一步的探索理解与创新设计带来非常大的帮助。”

在这两年间，起始于Ilya的那篇《Let's Verify Step by Step》，OpenAI o1→o3的“鼓噪”，DeepSeek r1的横空出世；在经历了全球各大小厂和实验室对各种类CoT指令数据的筹备、各精调方法的运用、强化学习·RL思想PT融入、奖励机制及优化策略的持续探索与优化、推理时扩展（test-time scaling）思想从探索到应用等阶段后，当前LLMs在复杂推理与规划任务、跨多重形式化符号推理模式（代码编程&定理证明..）、Agentic工具调用（Tool Use）等诸多场景上均取得一定的里程碑进展。

但我想对于长期涉足人工智能、大模型领域的研究者或持续关注这一领域进展的人们来说，模型在复杂推理任务所呈现出的技术涌现在感性上与三年前ChatGPT刚刚发布时AIGC技术涌现带来的爆发或冲击则要平和的多，究其原因两者间也许在模型泛化能力直接为人们带来的应用价值与使用体验上，前者确实与后者存在着一定差距，也许人们曾经历于ChatGPT时刻后其自身神经兴奋阈值被拉高，也许人们进一步改变了对LLMs的期待及严谨审视的态度，也许从技术维度上，生成式自回归（AR）的这种语言建模与强化学习（RL）思想的融合虽然经历了短暂的“DeepSeek Aha时刻”后，但在底层技术原理与内涵上仍未取得或者被人们意识到到像当初生成式自回归（AR）下next token predict语言编码建模所带来的这种范式变革、突破与价值。

同时，正如上述所说，当前的大型语言模型（LLMs）所依赖于“思维链”（Chain-of-Thought, CoT）等技术，通过将复杂任务分解为简单的中间步骤，并逐步生成文本输出的这种方法也许亦存在着一些显著的局限性，如：

复杂任务规划与分解表现出一定的脆弱性：CoT依赖于人工定义或LLMs原生一过性推理泛化能力的任务规划与分解，一旦某个步骤出错或顺序不当，整个推理过程可能会失败，同时由于当前DNN Model不管依赖于流行的Transformer架构还是RNN等架构，由于其模型结构本身及建模过程方式的限制，使得其无法进行有效的思维回溯或依据不同任务和环境进行更为灵活的内部结构自适应。

模型多阶段训练过程中对数据层面的需求挑战：CoT推理需要大量的训练数据来促进模型学习中间推理步骤以实现对这种长链推理泛化Pattern概率分布的拟合，导致模型一定程度在多阶段、跨训练模式成本上的高昂，包括高度结构化及专业性的人类精细化标注成本、稀缺的高质量数据源采集加工→数据合成工程、强化学习过程中对数据采样分布、控制及联动奖励机制的探索与策略优化设计等。

训练&推理计算复杂度及响应延迟挑战：不管是在训练or推理阶段，由于LLMs自身生成式自回归（AR）的next token prediction建模的特点，均需或显性或隐性的生成→表征→压缩大量的中间步骤，使得CoT模型的推理速度较慢，难以满足某些场景下实时性要求。

此外，从计算理论的角度来看，标准的Transformer架构由于其固定的深度以及在训练过程中自回归联合概率优化方法下，在需要解决某些多项式时间复杂度问题时，自然的也会受到来自训练数据样本、梯度优化的诸多挑战，这亦限制了其在复杂推理任务中的表现。

为了解决并尝试推动对上述这些问题采用其它可探索路径，来自Sapient Intelligence公司的研究者们从人类大脑的层次化和多时间尺度处理机制中汲取灵感，提出了层次化推理模型·Hierarchical Reasoning Model, HRM，下面也大家带来对这篇论文所开创的层次化推理范式带来简单解读：

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F68808d1ffad01223a667be3065e77223?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=TCiHQxDlQJnds0489PaBVD8CxVk%3D)

可以说，论文整体上立足于从探索模型“潜在推理·latent reasoning”模式出发，以语言是人类交流的工具，而非思维本身的载体为基础（去年解读并记录成笔记的一篇来自Nature的论文亦可作为大家参考：[来自MIT：大脑认知与语言符号形式化推理的观点](https://mp.weixin.qq.com/s?__biz=MzkxOTY2MjE3Nw==&mid=2247485245&idx=1&sn=9f9c85b78e2691d74e0fd964daa94470&scene=21#wechat_redirect)），得出大脑在潜在空间中以惊人的效率维持着长而连贯的推理链条，而无需不断将其翻译回语言的猜想框架。

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F99c14a33d2a8262020409052a4ffd1c2?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=yTFMHRoB%2FZ0R9QUqpaV5KwvVOUk%3D)

基于上述框架思想，论文亦提到现有LLMs的latent reasoning能力仍从根本上受限于模型的有效计算深度，受到模型结构因简单地堆叠造成梯度消失问题而带来诸多挑战，亦严重影响了训练的稳定性与有效性，如循环架构作为处理序列任务的自然替代方案，常出现过早收敛的问题，导致后续计算步骤失效，且依赖于在生物学上不现实、计算成本高且内存消耗大的“时间反向传播·Backpropagation Through Time, BPTT”。

同时，论文捕捉到人类大脑为实现当前人工模型所缺乏的有效计算深度提供了极具启发性的蓝图，如：大脑在不同时间尺度运行的皮层区域之间以分层方式组织计算，从而实现深度的多阶段推理；人类在进行system Ⅱ·慢思考时通过循环反馈回路不断优化内部表征，使得缓慢的高层区域能够指导快速的低层回路执行任务，在保持全局一致性的同时实现分层处理...值得注意的是，大脑在实现这种深度的同时，也许也通过巧妙的方法避免了传统循环网络因时间反向传播而产生的高昂信用分配成本，论文后续也针对环节进行了探索与数学推导。

因此，论文受人脑中分层和多时间尺度处理等的启发，提出了分层推理模型（HRM），作为一种新颖的递归架构，其能够在保持训练稳定性和效率的同时实现显著的计算深度。HRM通过两个相互依赖的递归模块在单次前向传递中执行顺序推理任务，而无需对中间过程进行显式监督：高层模块（H-module）和低层模块（L-module），一个负责缓慢、抽象规划的高级模块，以及一个处理快速、详细计算的低级模块，同时保持训练的稳定性和效率。同时，提出了一种单步梯度近似方法来训练HRM，以提高训练效率，消除对BPTT的需求，使其具有良好的可扩展性，并更符合生物学机制。

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F6dd1ff4f50c3b114c861d668edf75d84?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=IQukFR5kXfegmFxJ%2Bc%2BblqPqKpY%3D)

在模型核心架构设计与技术细节上，HRM包括四个可学习的组件：输入网络∫I、低层递归模块 ∫L、高层递归模块∫H和输出网络∫O；模型的动态过程分为N个高层周期，每个周期包含T个低层时间步。具体来说，HRM的工作流程如下：

1\. 输入投影：输入向量 x 通过输入网络 ∫I 被投影到一个工作表示 x tilde。

2\. 低层模块更新：在每个时间步 i，低层模块 ∫L 根据自身的前一状态、高层模块的当前状态（在当前周期内保持不变）以及输入表示来更新其状态：

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1841a0a5e6719a80b54ac720cb3e203e?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=63HKopAAudt5zaYz0mce2KmIuwU%3D)

3\. 高层模块更新：高层模块 ∫H 每 T 个时间步更新一次，使用低层模块在当前周期结束时的最终状态：

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F566b4a4ddb7ea034753c812a1edd4cb7?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=LrrY14QqXoL3ll76UGpz5uin%2Ba0%3D)

4\. 输出预测：在 N 个完整周期后，从高层模块的隐藏状态中提取预测结果 y hat：  

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ffb95585b85483abb655405aeaa35806d?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=kfW38r5ojUMuLW1E1k4HsKaoESQ%3D)

在模型整体训练范式以及对应所采用的一些关键机制上，包含了“层次化收敛”、“单步梯度近似”、“深度监督”、自适应计算时间等创新方法：

层次化收敛

（Hierarchical Convergence）

  

为了避免传统递归模型中常见的快速收敛问题，HRM通过慢速更新的高层模块和快速更新的低层模块之间的协作，实现更深层次的计算。低层模块在每个周期内多次更新，达到局部平衡后，高层模块才进行更新，从而实现更深层次的计算。

如论文中具体描述：在每个周期中，低层模块（L模块 - 一个循环神经网络RNN）会稳定地收敛到一个局部平衡状态。然而，该平衡状态依赖于该周期中高层模块提供的高层状态 。在完成T个时间步后，高层模块（H模块）整合此次子计算的结果（即低层模块的最终状态zL），并执行自身的状态更新。这一zH的更新为低层模块建立了一个全新的上下文环境，实质上“重启”了其计算路径，从而开启向另一个局部平衡状态的新一轮收敛阶段。

这一过程使得HRM能够执行一系列不同但稳定的嵌套式计算：高层模块指导整体问题求解策略，而低层模块则执行每一步所需的密集搜索或精细优化。尽管一个标准RNN可能在T次迭代内接近收敛，但分层收敛机制的有效计算深度达到了N×T步。正如论文中图3的实验结果所示，该机制使HRM能够在多个时间步中保持较高的计算活跃度（前向残差），而标准RNN的活跃度则迅速衰减；同时仍能实现稳定的收敛。这使得HRM在任意计算深度下均表现出更优的性能，原论文图2所示。  

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb8b358104fde7deed9f5ff238a0c44b1?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=AFF%2F1aJyAvzw3AtGbJjm23l3a2k%3D)

单步梯度近似

（One-step Gradient Approximation）

  
为了避免传统递归模型中反向传播通过时间（BPTT）的高内存需求，HRM采用单步梯度近似方法，仅使用模块的最终状态进行反向传播，大大降低了内存需求。

如论文中所提及，循环模型通常使用时间反向传播（BPTT）来计算梯度。然而，BPTT需要存储前向传播过程中的所有隐藏状态，并在反向传播时将它们与梯度结合，这需要O(T)的内存（T 为时间步数）。这种巨大的内存开销迫使使用更小的批量大小，导致GPU利用率低下，尤其对于大规模网络而言更为严重。此外，由于在时间上保留完整历史轨迹在生物学上是不可行的，因此人类大脑很可能并非是以类BPTT方式来进行反向梯度优化并完成学习训练的。

试想，如果一个循环神经网络收敛到一个固定点，自然的可通过在该平衡点进行单步反向传播，从而避免展开其状态序列，基于这一发现，论文提出一种梯度单步近似方法·One-step Gradient Approximation，仅使用每个模块最后状态的梯度，无需进行时间上的展开，通过PyTorch等自动微分框架实现。

这种梯度单步近似，即One-step Gradient Approximation在理论上基于深度平衡模型(Deep Equilibrium Models，DEQ)数学思想，模型利用隐函数定理(Implicit Function Theorem，IFT)来绕过传统的Backpropagation Through Time，BPTT，具体的可参考论文中所列的推导步骤：

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fcfd56cc843465d9969bf52b3ea180f50?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=MmDd6s5DsZHJinBQvCrdrCWUvxg%3D)

深度监督（Deep Supervision）

  
受大脑中周期性神经振荡调节学习发生时间的原理启发，论文中的HRM加入了深度监督机制，在给定的一个数据样本(x，y)，运行多次HRM模型的前向传递，每一次称之为一个片段，设M表示在终止之前执行的总片段数，则：

对于每个片段m ∈ {1, ..., M}，设zm = (zmN TH, zmN TL) 表示片段m结束时的隐藏状态，包括高级和低级状态组件。

在每个片段m中，应用深度监督步骤计算损失及更新参数的步骤如下:  

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1da0ca3f4d19a7fde796431cec89ae7f?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=m9WVjMGEXtnsqiWV0isxRWtbzhk%3D)

这一过程的关键在于，在将隐藏状态zm用作下一个片段的输入状态之前，它已被从计算图中“分离”(detached)。因此，第m+1个片段的梯度不会反向传播至第m个片段，从而有效地实现了对递归式深度监督过程梯度的单步近似，同时该方法亦为高层模块提供了更频繁的反馈，并作为一种正则化机制，在经验表现和深度平衡模型的稳定性方面，优于更复杂的基于雅可比矩阵的正则化技术，下图展示了深度监督训练的伪代码：

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb0ad72ac1d91ba1ea10e7308b6cc89a4?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=pdoOH5Ze2tIjGSeRLK1FZQISx0Y%3D)

这样通过在每个推理阶段对模型进行监督学习，提供更频繁的反馈，并增强模型的稳定性和性能。

另外，本篇论文中的“深度推理”思想与之前分享的几篇关于“Latent Space Reasoning”的论文均有相似之处，如大家感兴趣，可以回顾一下:)

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3447cdbf377be57fab031b2a049fdfbf?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=c62LAB4wZvhPno7dzc912hLIX6w%3D)

[来自Meta田渊栋团队：继Coconut之后CoCoMix带来的隐推理范式进阶](https://mp.weixin.qq.com/s?__biz=MzkxOTY2MjE3Nw==&mid=2247486754&idx=1&sn=478a43b1101a3e5b70e2b5a4d46458c8&scene=21#wechat_redirect)

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3e878fee6cee0d0eaf8ea3f212cab781?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=aK%2B%2F822naR1t4TR0Ak%2BAbLd5%2BJU%3D)

[来自对Meta FAIR田渊栋：符号和神经网络推理融合与统一的思考](https://mp.weixin.qq.com/s?__biz=MzkxOTY2MjE3Nw==&mid=2247485611&idx=1&sn=18e26301e13d454cfe6da26951b4d389&scene=21#wechat_redirect)

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe47f80bc015b74ea88bcac21f3d75468?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=AtSOyhPUlvA3MItZyayMf87rI7M%3D)

还有像“谷歌DeepMind提出的苏格拉底式自主递归增强学习”：[谷歌DeepMind提出苏格拉底式自主递归增强学习](https://mp.weixin.qq.com/s?__biz=MzkxOTY2MjE3Nw==&mid=2247485868&idx=1&sn=b6ac7004e8298c9151dde11463b64f45&scene=21#wechat_redirect)  

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5fc6a621bad9f73aa4a1e62140eeab73?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=PyU5TvPd8jKBfrfp7o%2BsZa35s6I%3D)

以及马里兰大学的一篇论文《Scaling up Test-Time Compute with Latent Reasoning:A Recurrent Depth Approach》提出的语言模型在模型隐状态空间中通过迭代循环块来完成深度推理（泛化组合的持续封装与映射）工作：[后DS-R1下，显性推理·Existent‌ Reasoning → 隐性推理·Latent Reasoning的演进](https://mp.weixin.qq.com/s?__biz=MzkxOTY2MjE3Nw==&mid=2247486618&idx=1&sn=654e67abd474bb4795fe6cca1fc2b511&scene=21#wechat_redirect)  

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F54bb13bd9723acc06f3fed79d4e7896f?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=aWzNcTCgwTUINq31mh1l6z4xdx8%3D)

清华的Test-Time RL工作：[从清华的Test-Time RL到Socratic Learning：尝试探索RL自监督框架下模型推理范式演进的机制与内涵](https://mp.weixin.qq.com/s?__biz=MzkxOTY2MjE3Nw==&mid=2247487033&idx=1&sn=3fe40d113632248a56c65c3ef614b5c9&scene=21#wechat_redirect)

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff6821024ba4fadec9abeb2fdff46584e?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=uf7aHpCALUSi1OP1Ockoe3MjLWU%3D)

自适应计算时间

（Adaptive Computation Time, ACT）

  
自“Test-Time Compute Scaling”提出后，业界即涌现出多种test-time范式，本篇论文自然也必不可少的提出了自适应计算时间（Adaptive Computation Time, ACT）机制，以能够实现模型自主的完成在System Ⅰ·快思考与System Ⅱ·慢思考的自由动态切换，即 根据任务的复杂性动态调整计算步骤，类似于人类在面对复杂问题时的“深思熟虑”和简单问题时的“快速反应”。

论文指出，经前人神经科学研究表明，上述两种认知模式于人类大脑中共享重叠着部分神经回路，特别是在前额叶皮层和默认模式网络等区域。这表明大脑会根据任务复杂性和潜在收益，动态调节这些回路的“运行时间”。

受此机制启发，论文中在HRM中引入了一种自适应停机策略，实现“快与慢的思考”。该机制利用深度监督，并结合Q-Learning，自适应地决定推理片段的数量。一个Q-head网络利用高层模块的最终状态，预测“停止”(halt)和“继续”(continue)两种动作的Q值，进一步具体的算法设计及推导大家可参加下图或原论文，这里不在赘述：

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fdc1ea5a31ad7fd057d4a9423013975bc?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=QEEbChZWo%2B9A2LUrUjLDhmoagI4%3D)

同时，论文亦指出了当下Test/Inference-time scaling在面对不同复杂程度、类型的任务上仍具备更多人类无法理解或洞察的角落，如在数独和ARC-AGI等不同挑战任务上，看似同类型、同等复杂的任务会对Test/Inference-time有着差异性的诉求，我想这也为类似于ACT这种方法带来更多研究潜力与可探索空间 ，同时我认为这也将是未来计算复杂性理论的重点研究领域之一。

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F63b5ceca5d3c656007ed8b286c23de40?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=KQQegU4RZhdLx5RYoSkx5w89cuI%3D)

论文中的图5展示了两种HRM变体之间的性能对比：一种采用了ACT机制，另一种则使用与ACT的Mmax参数相当的固定计算步数。结果表明，ACT能够根据任务复杂度自适应地调整其计算资源，在对性能影响极小的情况下实现了显著的计算节省。

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F712876e930f6246353b9a490b6d99b09?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=XcnQS8PyV%2B2xw45BJJyTdLUv2fE%3D)

在此处，论文也提到了所采用的Q-Learning算法所面临的稳定性挑战，ACT通过模型本身及其训练过程的内在属性实现了稳定性，采用RMSNorm（一种层归一化变体）和AdamW优化器的Post-Norm架构一定程度上解决了上述挑战。

在最终的实验结果与性能分析上，HRM在多个复杂推理任务上表现出色，包括ARC-AGI挑战（抽象和推理能力测试）、Sudoku-Extreme（复杂数独）和Maze-Hard（复杂迷宫路径寻找）。在这些任务中，HRM仅使用1000个训练样本，就超越了现有的基于CoT的大型模型。

如ARC-AGI挑战任务中，HRM在ARC-AGI-1任务中达到了40.3%的准确率，显著高于现有的CoT模型（如o3-mini-high的34.5%和Claude 3.7 8K的21.2%）。在ARC-AGI-2任务中，HRM也表现出色，尽管具体数值未在摘要中提及。

在Sudoku-Extreme复杂数独任务中，HRM达到了74.5%的准确率，而基于CoT的模型准确率为0%。这表明HRM在处理需要深度搜索和回溯的任务时具有显著优势。

在Maze-Hard 30x30迷宫路径寻找任务中，HRM也表现出色，准确率接近完美，而CoT模型的准确率为0%。

此外，HRM在推理时亦可以任务自适应的通过增加计算步数来提升性能，而无需额外训练或架构修改，显示出良好的可扩展性。

更进一步的模型与神经科学对应解释机制对中间步骤可视化方面，通过分析HRM在不同任务中的中间步骤，发现模型能够根据任务类型采用不同的推理策略。例如，在迷宫任务中，HRM会同时探索多条路径，逐步淘汰无效路径，并逐步优化解决方案；在数独任务中，HRM采用深度优先搜索策略，当遇到死胡同时会回溯。

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0902155a0214b9760ec33361396fc580?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=4hZjmJP9GOGmQwg4%2BAeTLp%2BF5C4%3D)

与大脑的对应关系：HRM的层次化结构和多时间尺度处理机制与大脑的神经活动有相似之处。例如，HRM的高维表示（高PR值）和低维表示（低PR值）之间的分离，类似于大脑中高级皮层区域和低级感觉区域的功能分工。这种层次化组织可能是HRM在复杂任务上表现出色的关键原因之一。

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3a98cfc4500d4f2cf3e804f5b5b1c99f?Expires=1780067727&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=NcYTXTWlBGbh0XrzDaJqI0Hxz%2F4%3D)

最后结合论文做一些未来展望与观点总结

1\. 隐推理范式（Latent Reasoning）的潜力  
HRM的成功表明，隐推理范式（即模型在内部隐藏状态空间中进行推理，而不是依赖于显式的语言步骤）可能是实现复杂任务推理的关键。与传统的CoT方法相比，隐推理范式具有以下优势：

更高的推理效率：隐推理不需要生成大量的中间步骤，因此可以显著减少计算成本和响应时间。

更强的泛化能力：隐推理不依赖于特定的语言模式，因此在面对新的、未见过的任务时，模型能够更好地泛化。

更接近人类的推理方式：人类的大脑在进行推理时，通常不会将每一步都转化为语言形式，而是通过内部的神经网络进行高效的推理。隐推理范式更接近这种自然的推理方式。

2\. 隐推理范式下的未来模型设计

多模态隐推理：未来可以探索将HRM的隐推理机制扩展到多模态任务中，例如结合视觉和语言信息进行推理。例如，在视觉问答（VQA）任务中，模型可以通过隐推理来理解图像内容和问题之间的关系，从而生成更准确的答案。

动态架构调整：HRM的自适应计算时间机制为动态调整模型架构提供了思路。未来可以设计更灵活的模型架构，根据任务的复杂性动态调整模块的连接方式或计算资源分配。例如，对于简单的任务，模型可以减少计算步骤；对于复杂的任务，模型可以增加计算步骤或引入更多的模块。

与神经科学的深度融合：HRM的设计灵感来源于大脑的神经机制，未来可以进一步加强神经科学与人工智能之间的交叉研究。例如，通过模拟大脑的神经活动模式来设计更高效的推理算法，或者利用人工智能技术来研究大脑的神经机制。这种跨学科的研究可能会带来更多的创新和突破。

3\. 隐推理范式下的挑战与应对策略  
  
模型可解释性：隐推理范式的一个潜在挑战是模型的可解释性。由于推理过程隐藏在模型的内部状态中，很难直接观察和理解模型是如何进行推理的。为了解决这个问题，可以开发新的可视化技术和解释方法，例如通过分析模型的中间状态和梯度信息来揭示推理过程。

训练难度：隐推理模型的训练可能比传统的CoT模型更具挑战性，因为它们需要学习更复杂的内部表示和推理机制。为了解决这个问题，可以探索新的训练方法和正则化技术，例如通过引入对抗训练或元学习来提高模型的稳定性和泛化能力。

数据需求：尽管HRM在小样本学习任务中表现出色，但在大规模数据集上训练隐推理模型可能需要更多的数据和计算资源。为了解决这个问题，可以探索数据增强技术和迁移学习方法，以减少对大规模标注数据的依赖。

本篇论文中的HRM作为一种新型的层次化推理模型，通过其独特的架构和机制，在复杂推理任务上取得了显著的性能提升。它不仅为解决当前人工智能中的推理挑战提供了新的思路，还为未来的研究方向提供了有价值的启示。尽管HRM作为一种全新的范式，还无法像基于Transformer和AR下的LLMs那样健壮和成熟，也许也还还存在诸多的不足和局限，但相信通过进一步探索其在不同领域的应用和与其他技术的结合，有望推动人工智能向更高效、更智能的方向发展，如隐推理范式也许会成为人工智能推理领域的一个重要发展方向，为实现更接近人类水平的推理能力提供新的可能性。

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 11:15*

## Related Notes

- [[AgentEvolver vs AlphaEvolve：AI自我进化的两条核心路线对比 🧠]]
- [[AI编码代理的质的飞跃：v3.3透明化与v3.4连续性技术解析]]
- [[DARPA人工智能与自主系统项目深度研究报告：以“第三波AI”为核心的军事智能革命]]
