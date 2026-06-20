---
title: Nature重磅 | 揭秘大脑中的共享神经子空间与几何缩放
tags:
- brain
- brain-science
- neuroscience
- paper
---
- **笔记本**: 我的剪贴板
- **时间**: 2026-01-13 09:54

---

原文链接: https://mp.weixin.qq.com/s/S3ALrTJvMRt5Hzn228wdOQ

PsyBrain 脑心前沿 | 公众号 PSY-Brain_Frontier
一键关注，点亮星标 ⭐️不错过每日前沿资讯

认知神经科学前沿文献分享

基本信息
Title: Building compositional tasks with shared neural subspaces发表时间：2025.11.26发表期刊:Nature影响因子：48.5获取原文：

- 添加小助手: PSY-Brain-Frontier即可获取PDF版本
- 点击页面底部“阅读原文”即可跳转论文原网页

研究背景
认知系统如何灵活适应环境变化并学习新任务？人类和非人灵长类动物能够将简单的行为和认知模块进行重新利用和灵活组合 ，这种能力被称为任务组合性（Task Compositionality）。试想，我们在学会辨别水果颜色“是否成熟”这一基本技能后，可以将它用于采摘、烹饪、食用等多种任务中。组合性正是实现通用智能的关键 。   

然而，大脑在神经环路层面如何将这些基本模块像“乐高积木”一样灵活地“搭建”和“拆解”，并实现对感觉、认知和运动表征的灵活“动态路径选择/动态路由”（Dynamic Routing），一直是认知神经科学的核心挑战 。神经系统必须解决一个关键问题：如何确保在执行新任务时，只激活并连接当前任务所需的神经资源（例如，颜色信息），同时抑制那些不相关的旧信息（例如，形状信息或错误的运动路径），避免“内部短路”？   本研究正是为了揭示这一动态调控的神经基础。研究团队通过设计三个具有精妙组合关系的视觉分类任务（S1, C1, C2），精准测试了任务组合性在神经层面的实现 。其中，任务C1被视为组合任务，它结合了C2的颜色感知子任务与S1的轴1运动响应子任务 。更重要的是，实验范式要求猕猴在任务切换时，必须通过迭代更新内部任务信念来推断当前规则（即任务推断），从而提供了观察神经资源动态调控的理想窗口 。

Fig. 1 | The monkeys performed three compositional tasks.

研究核心总结
本研究的核心发现是，大脑通过维护和调用共享神经活动子空间来高效支持任务组合性，而外侧前额叶皮层（LPFC）是实现这一灵活机制的关键枢纽。

Fig. 2 | Colour category and response representations were shared across tasks. 

一、共享表征与动态转换

- 子空间泛化性： LPFC是共享表征的主要枢纽，其神经活动表现出强大的跨任务泛化能力，证实了存在与具体任务解耦的共享感觉子空间（编码颜色类别）和共享运动子空间（编码轴1/轴2响应方向）。通过线性分类器验证，训练用于C2的颜色分类器可成功解码C1任务中的颜色信息；运动表征则在所有记录区域（包括LPFC, FEF, PAR, aIT）中都表现出广泛的共享性 。   
- 顺序组合与计算路由： 任务的执行体现为这些子空间的顺序参与和任务依赖的转换 。在LPFC中，神经活动首先在共享颜色子空间中编码刺激类别，随后被选择性地路由至任务相关的共享运动子空间（如C1任务中路由至轴1）。跨时序相关性分析进一步证实，共享感觉表征的编码强度能够预测未来相关运动响应轴的编码，而非无关轴，清晰地展示了从感知信息到任务特定运动输出的动态转换过程 。   

Fig. 3 | Shared representations were transformed into shared motor representations during the task.

二、任务信念与几何门控

- 信念驱动的动态门控： 子空间的灵活调用并非自动，而是由内部任务信念驱动和调控 。LPFC中任务信念编码的增强，正相关地预测了共享颜色子空间的参与度 。   
- 增益调控与干扰抑制： 任务信念通过实施一种几何缩放机制，即增益调控，来实现对表征的动态控制 。任务相关特征（如颜色）的神经表征被放大，而任务无关特征（如形状）的表征则被衰减和延迟。这种几何调整策略由压缩指数（Compression Index, CPI）量化，并与任务信念高度相关，是解决多任务干扰和支持持续学习的关键策略 。值得注意的是，对无关运动轴的抑制是快速的（3-6个试次内），而对无关感觉特征的衰减则是渐进的，反映了不同层级规则的推断速度差异 。

Fig. 4 | Shared subspaces are dynamically engaged during task discovery.
综上所述，本研究在神经群体层面为任务组合性的实现提供了结构性证据。外侧前额叶皮层（LPFC）通过维护共享神经子空间作为可重用的计算组件 。这种灵活的组合，本质上依赖于高维度的内部任务信念作为核心的控制信号 。该信念不仅驱动了从感觉表征到运动表征的动态计算路由，实现任务相关的时序转换 ，还通过几何门控机制，精确地放大任务相关信息并抑制干扰信息 。这一发现揭示了大脑如何在保障跨任务泛化性的同时，通过精细的表征几何学调整来有效解决持续学习中的干扰和冲突问题 。

Fig. 5 | Irrelevant sensory and motor representations were suppressed during flexible behaviour.

Abstract

Cognition is highly flexible—we perform many different tasks and continually adapt our behaviour to changing demands. Artificial neural networks trained to perform multiple tasks will reuse representations and computational components across tasks. By composing tasks from these subcomponents, an agent can flexibly switch between tasks and rapidly learn new tasks. Yet, whether such compositionality is found in the brain is unclear. Here we show the same subspaces of neural activity represent task-relevant information across multiple tasks, with each task flexibly engaging these subspaces in a task-specific manner. We trained monkeys to switch between three compositionally related tasks. In neural recordings, we found that task-relevant information about stimulus features and motor actions were represented in subspaces of neural activity that were shared across tasks. When monkeys performed a task, neural representations in the relevant shared sensory subspace were transformed to the relevant shared motor subspace. Monkeys adapted to changes in the task by iteratively updating their internal belief about the current task and then, based on this belief, flexibly engaging the shared sensory and motor subspaces relevant to the task. In summary, our findings suggest that the brain can flexibly perform multiple tasks by compositionally combining task-relevant neural representations.

请打分
这篇刚刚登上 Nature 的研究，是否实至名归？我们邀请您作为“云审稿人”，一同品鉴。精读全文后，欢迎在匿名投票中打分，并在评论区分享您的深度见解。
前沿交流 |  欢迎加入认知神经科学前沿交流群！⭐️ [[入群链接](https://mp.weixin.qq.com/s?__biz=MzYyMTE5NTI5OA==&mid=2247484688&idx=3&sn=674dfdbd6497ee923af211ad05a155bc&scene=21#wechat_redirect)]

核心图表、方法细节、统计结果与讨论见原文及其拓展数据。分享人：饭哥审核：PsyBrain 脑心前沿编辑部

## Related Notes

- [[Less is more，大脑“低能耗”并“高效响应”的秘诀：模块化 | NSR]]
- [[Less is more，大脑“低能耗”并“高效响应”的秘诀：模块化 | NSR]]
- [[Milinkovic B (2024)：复杂神经系统涌现动力学结构]]
