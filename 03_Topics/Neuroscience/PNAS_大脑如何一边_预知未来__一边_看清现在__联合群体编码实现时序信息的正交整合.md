---
title: PNAS：大脑如何一边“预知未来”，一边“看清现在”？联合群体编码实现时序信息的正交整合
tags:
- brain
- brain-science
- neuroscience
- paper
---
- **笔记本**: 我的剪贴板
- **时间**: 2026-01-14 23:11

---

原文链接: https://mp.weixin.qq.com/s/b_rC6q25qwxuxc2tKxG50g

PsyBrain 脑心前沿 | 公众号 PSY-Brain_Frontier
一键关注，点亮星标 ⭐️不错过每日前沿资讯

认知神经科学前沿文献分享

基本信息
Title: Conjunctive population coding integrates sensory evidence to guide adaptive behavior发表时间：2025.12.24发表期刊:PNAS影响因子：9.1获取原文：

- 添加小助手: PSY-Brain-Frontier即可获取PDF版本
- 点击页面底部“阅读原文”即可跳转论文原网页

研究背景
在日常生活的复杂环境中，我们的行为往往依赖于对“当下”的精准感知与对“过去”的有效整合。试想你在聆听一段旋律或理解一句话时，大脑不仅需要清晰地接收每一个独立的音符或单词（感觉辨别），还需要将其置于前序的时间脉络中，以预测接下来的走向（时间整合）。这种能力是人类认知灵活性的基石。

然而，对于神经系统而言，这构成了一个巨大的计算挑战：大脑如何在单一的神经群体中，既保留对当前刺激的精确表征，又融合过去的历史信息以形成预测？这就好比在同一块画布上不断叠加新的颜料，如何才能既看到最新的笔触，又不让底色模糊不清，甚至还能让二者交相辉映形成有意义的图像？长期以来，关于大脑如何处理“历史偏差”（Serial Biases）与“当下感知”的争论不休。一方面，我们需要利用先验知识（Prior）来加速反应；另一方面，过度的整合可能导致当前感知的失真或干扰（Interference）。传统的实验室研究往往将试次（Trial）视为相互独立的事件，忽略了这种时间流中的连续整合机制 。因此，在毫秒级的时间尺度上，神经群体究竟采用了何种编码策略来平衡“整合预测”与“感觉辨别”之间的权衡，仍是认知神经科学领域亟待解开的谜题。

研究核心总结
本研究利用高时空分辨率的人类颅内脑电图（iEEG）技术，深入探究了大脑如何在广泛分布的皮层网络中通过神经群体活动整合时序信息。研究者记录了15名癫痫患者在执行听觉目标检测任务时的神经活动，该任务包含随机序列与具有预测性的序列结构。通过分析高频活动（HFA，70-150 Hz）这一反映局部神经群体放电的指标 ，研究揭示了“联合群体编码”（Conjunctive Population Coding）是解决上述计算挑战的关键机制。

Fig. 1. Experimental paradigm, behavioral results, and electrode coverage.

预测性语境通过“模式分离”而非“噪声抑制”增强感觉表征
研究发现，当听觉刺激出现在具有预测性的序列中时，被试的反应速度显著加快，且诱发的神经高频活动受到显著调制。通过解码分析与表征相似性分析（RSA），研究者对比了两种可能的神经增强机制：“噪声抑制”（降低试次间的变异性）与“模式分离”（增加不同刺激间表征距离）。结果明确支持模式分离（Pattern Separation）假说：预测性语境并没有降低神经响应的变异性，而是通过招募更多具有刺激选择性的电极，显著增加了不同刺激在神经状态空间中的多维距离（Multidimensional Distance, MDD）。这意味着，预测信号非但没有模糊感觉输入，反而扩展了表征空间，使得当前刺激的编码更加清晰、易于区分 。

Fig. 2. Build-up of predictive information.

联合编码子空间实现历史与当下的无干扰整合
本研究最核心的发现在于揭示了神经群体如何同时表征“过去”与“现在”。结果显示，神经活动并未将过去和现在的刺激独立存储在不同脑区，而是采用了一种联合编码（Conjunctive Coding）策略。RSA分析表明，神经群体的状态轨迹由“过去刺激”与“当前刺激”的特定组合共同决定，形成了一个整合的时间语境表征。更为精妙的是，为了防止过去的信息干扰对当前刺激的读取，大脑采用了正交读出（Orthogonal Readout）的几何策略。虽然同一个神经群体同时携带了过去和现在的信息，但可以通过两个近乎正交的分类器平面分别读取这两种信息。这种正交的几何结构确保了大脑可以在保留序列顺序（时间语境）的同时，精确识别当前的感官输入，从而在同一神经群体中实现了信息的“多路复用”。

Fig. 3. Neural pattern separation facilitates the readout of behaviorally relevant task states.

研究意义
本研究通过直接的人类神经生理学证据，从群体几何（Population Geometry）的视角阐释了认知灵活性的神经基础。它表明，大脑并非简单地覆盖旧信息，而是通过构建高维的联合表征空间，将先验预测与感官证据“编织”在一起。这种机制既保证了利用历史信息进行自适应预测的优势，又通过正交子空间避免了感官干扰，为理解人类如何在动态环境中实现连续、灵活的认知控制提供了关键的理论框架。

Fig. 4. Conjunctive neural coding integrates past and present stimuli.

Abstract

Cognitive flexibility relies on the continuous accumulation and integration of sensory evidence to guide adaptive behavior. In natural environments, behaviorally relevant information unfolds sequentially over time and is constantly evaluated against prior knowledge, task rules, and current demands. Integration of these inputs poses a computational challenge: How is temporally unfolding, predictive information integrated into a stable representation, while preserving the discriminability and flexibility to map individual stimuli to competing context-specific actions? Using large-scale human intracranial electroencephalography, we assessed how neural population activity integrates behaviorally relevant information across multiple sensory events that sequentially unfold over time and jointly determine the current context. The results uncover that the population geometry supports the emergence of conjunctive coding subspaces that integrate prior information with current sensory evidence and jointly define the temporal context that mediates behavioral benefits. Evidence accumulation diversifies the population responses distributed across the cortex, increasing the representational space that embeds context-dependent stimulus-action mappings. Hence, context-dependent sensory coding might constitute the neural basis underlying adaptive human behavior. In sum, these results demonstrate how neural population activity balances integrating predictive information with preserving stimulus discriminability to enable flexibility, while minimizing interference.
前沿交流 |  欢迎加入认知神经科学前沿交流群！⭐️ [[入群链接](https://mp.weixin.qq.com/s?__biz=MzYyMTE5NTI5OA==&mid=2247484688&idx=3&sn=674dfdbd6497ee923af211ad05a155bc&scene=21#wechat_redirect)]

核心图表、方法细节、统计结果与讨论见原文及其拓展数据。分享人：饭鸽儿审核：PsyBrain 脑心前沿编辑部

## Related Notes

- [[Less is more，大脑“低能耗”并“高效响应”的秘诀：模块化 | NSR]]
- [[Less is more，大脑“低能耗”并“高效响应”的秘诀：模块化 | NSR]]
- [[Milinkovic B (2024)：复杂神经系统涌现动力学结构]]
