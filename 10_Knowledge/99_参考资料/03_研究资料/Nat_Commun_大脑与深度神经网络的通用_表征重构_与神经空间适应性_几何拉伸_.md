# Nat Commun：大脑与深度神经网络的通用“表征重构”与神经空间适应性“几何拉伸”

- **笔记本**: 我的剪贴板
- **时间**: 2025-12-18 18:19

---

原文链接: https://mp.weixin.qq.com/s/yTDXSheg8iCOJrJLcP44sA

PsyBrain 脑心前沿 | 公众号 PSY-Brain_Frontier
一键关注，点亮星标 ⭐️不错过每日前沿资讯

认知神经科学前沿文献分享

基本信息
Title: Adaptive stretching of representations across brain regions and deep learning model layers发表时间：2025.11.21发表期刊:Nature Communications影响因子：15.7获取原文：

- 添加小助手: PSY-Brain-Frontier即可获取PDF版本
- 点击页面底部“阅读原文”即可跳转论文原网页

研究背景
想象一下，当你在一堆杂乱的桌面上寻找你的车钥匙时，你的大脑发生了什么？为了找到那个特定的目标，你会自动忽略掉那些柔软的、毛绒绒的物体，而对金属光泽、特定形状的物体变得格外敏感。这就是心理学中经典的“选择性注意”现象。

长久以来，神经科学家们都知道前额叶皮层（PFC）在这一过程中扮演着“指挥官”的角色，它通过自上而下的信号调节视觉系统，以增强任务相关信息的处理。然而，一个更深层且充满争议的问题是：这种调节究竟在多大程度上改变了大脑的内部表征？大脑是为了当前任务彻底“重构”了自己，还是仅仅是在高层区域做了加权？有一种理论认为，注意力的本质是“表征延伸（Representational Stretching）”，即沿着任务相关的维度（比如“金属光泽”），神经表征的距离被拉长了，而无关维度的差异被压缩了。如果这一假设成立，那么这种延伸是仅限于负责决策的高级脑区，还是会波及到像V4（负责颜色）和MT（负责运动）这样的感觉皮层？更为有趣的是，这种复杂的认知控制机制是生物脑独有的进化产物，还是任何智能系统（包括人工智能）在优化任务表现时都会涌现出的必然策略？为了回答这些问题，研究人员结合了猕猴的多脑区电生理记录与深度学习模型（CNN-LSTM），展开了一场跨越生物与人工神经网络的深度探索。

研究核心总结
本研究通过记录猕猴在执行多属性决策任务时的多脑区神经活动，并结合深度神经网络模型，揭示了大脑在任务导向下的适应性表征重构机制。

Fig. 1 | Overview of the behavioral task and CNN-LSTM modeling.

核心发现一：全脑范围的适应性“维度延伸”
研究采用表征相似性分析（Representational Similarity Analysis, RSA），构建了包含前额叶（PFC）、额叶眼动区（FEF）、外侧顶内沟（LIP）、下颞叶（IT）以及视觉皮层（V4, MT）的表征差异矩阵（RDM）。结果显示，“维度延伸”现象在所有记录脑区中均被观察到。具体而言，当任务要求关注“运动”维度时，那些在运动方向上不同、但在颜色上相同的刺激，其神经表征的差异性显著增大；反之亦然。这意味着，大脑不仅是在决策端进行筛选，而是通过广泛的神经重构，主动拉大了任务相关特征在神经空间中的距离，从而优化分类边界。

Fig. 2 | Spike timing measures best capture the experimenter intended coordinates.

核心发现二：脉冲时序编码的关键作用
与传统的发放率编码（Rate Coding）相比，研究发现包含时间信息的编码指标，特别是脉冲间隔（Inter-Spike Interval, ISI），能更精准地捕捉这种维度延伸效应。数据表明，ISI指标构建的RDM与实验设定的物理刺激空间具有最高的相似度，且在捕捉任务调制的动态变化上显著优于单纯的脉冲计数。这暗示了神经元发放的精细时序结构（Spike Timing）承载着决策所需的关键信息，而非仅仅是发放频率的改变。

Fig. 3 | Dimensional stretching occurs in both neural data and model representations. 

核心发现三：人工神经网络的自发涌现与生物限制
研究者构建了一个模拟灵长类视觉系统的深度学习模型（CNN前端+堆叠LSTM后端），并在相同的视觉输入和任务下进行训练（无显式注意模块，仅通过试错学习最小化误差）。令人惊讶的是，模型不仅在行为表现上达到了高水平，其内部表征也自发涌现出了与生物脑高度相似的“维度延伸”策略。这表明，这种注意机制可能并非需要预设的专用模块，而是智能系统为了最大化任务表现而采取的一种通用统计学习策略。不过，差异在于模型的灵活性远超生物脑：模型的各层均能根据任务完全重构；而生物脑中的V4和MT区虽然也表现出延伸，但仍保留了较强的模态特异性（Modality-bound），即V4始终更偏向颜色处理，MT更偏向运动处理，显示了生物进化的解剖约束。

Fig. 4 | Task-relevant attention allocation as estimated by the cognitive model.
这项研究有力地证明了大脑是一个高度动态的统计学习引擎。为了适应当前任务，它会跨越层级地“拉伸”其神经表征，利用脉冲时序编码来放大相关维度的差异。这种机制在生物脑和人工神经网络中的殊途同归，为我们理解认知的计算本质提供了极其重要的视角。

Fig. 5 | Alignment between brain region and LSTM layers. 

Abstract

Prefrontal cortex (PFC) is known to modulate the visual system to favor goal-relevant information by accentuating task-relevant stimulus dimensions. Does the brain broadly re-configures itself to optimize performance by stretching visual representations along task-relevant dimensions? We considered a task that required monkeys to selectively attend on a trial-by-trial basis to one of two dimensions (color or motion direction) to make a decision. Although effects were most prominent in frontal areas, representations stretched along task-relevant dimensions in all sites considered: V4, MT, lateral PFC, frontal eye fields (FEF), lateral intraparietal cortex (LIP), and inferotemporal cortex (IT). Spike timing was crucial to this code. A deep learning model was trained on the same visual input and rewards as the monkeys. Despite lacking an explicit selective attention or other control mechanism, by minimizing error during learning, the model’s representations stretched along task-relevant dimensions, indicating that stretching is an adaptive strategy.  

请打分
这篇刚刚登上 Nature Communications 的研究，是否实至名归？我们邀请您作为“云审稿人”，一同品鉴。精读全文后，欢迎在匿名投票中打分，并在评论区分享您的深度见解。
前沿交流 |  欢迎加入认知神经科学前沿交流群！⭐️ [[入群链接](https://mp.weixin.qq.com/s?__biz=MzYyMTE5NTI5OA==&mid=2247484688&idx=3&sn=674dfdbd6497ee923af211ad05a155bc&scene=21#wechat_redirect)]

核心图表、方法细节、统计结果与讨论见原文及其拓展数据。分享人：饭哥审核：PsyBrain 脑心前沿编辑部

---
**Tags:** [[CST]]
