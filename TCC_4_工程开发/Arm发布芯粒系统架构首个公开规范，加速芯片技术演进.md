---
title: Arm发布芯粒系统架构首个公开规范，加速芯片技术演进
tags:
- chip
- chiplet
- large-language-model
- project
- wafer
---
> 笔记本: 我的剪贴板  
> 创建时间: 2025-01-24  

---

原文链接: [https://mp.weixin.qq.com/s/3nrskibHboyA3SjWQjrtvw](https://mp.weixin.qq.com/s/3nrskibHboyA3SjWQjrtvw)


Arm宣布其芯粒系统架构 (CSA) 正式推出首个公开规范，进一步推动芯粒技术的标准化，并减少行业的碎片化。目前，已有超过60家行业领先企业，如ADTechnology、Alphawave Semi、AMI、楷登电子、云豹智能、Kalray、Rebellions、西门子和新思科技等，积极参与了 CSA 的相关工作，助力不同领域的芯片战略制定并遵循统一的标准。
Arm 基础设施事业部副总裁 Eddie Ramirez 表示：“人工智能 (AI)具备引领新一轮工业革命的巨大潜力，其市场渗透的深度与广度均达到了前所未有的水平。为了实现这一宏伟目标，我们必须能够应对不同市场中广泛且多样化的AI工作负载。这伴随而来的是对计算的广泛要求，也就意味着我们需要提供远不止一种的计算解决方案，且每种方案都要针对特定市场的需求进行优化。随着行业对定制芯片需求的不断攀升，加之芯片生产的成本与复杂性日益增加，芯粒 (Chiplet) 正逐渐成为业界广泛采用的解决方案。”
通过标准化和生态协作推进芯粒生态系统发展
通过复用专用的芯粒来开发多种定制化系统级芯片 (SoC)，与传统单片芯片相比，能够实现更高性能、更低功耗的系统设计，整体设计成本更低。然而，若缺乏行业统一的标准和框架，不同芯片组之间的差异可能会引发兼容性问题，进而阻碍创新的步伐。为解决这一碎片化问题，[Arm 于去年推出了 CSA](https://mp.weixin.qq.com/s?__biz=MjM5MzAyMzkwOA==&mid=2247492326&idx=2&sn=37fa32c7c7dce6203d86edba1d6c9aec&scene=21#wechat_redirect)。CSA提供了一套与生态系统共同开发的系统切分和芯粒互联的标准，使行业在构建芯粒的基础选择上达成一致。通过CSA，新的芯粒设计能够在符合标准的系统中无缝适配和复用，这不仅加速了基于芯粒的系统创新，还有效降低了碎片化的风险。
CSA 首个公开规范进一步加速芯片技术的演进
这些创新科技公司对 CSA 的广泛参与，构成了基于 Arm 技术的芯粒生态系统的基石。该生态系统致力于革新系统设计，使 SoC 更具灵活性、可访问性和成本效益，同时能显著降低碎片化风险。随着公开规范的发布，设计人员能够对如何定义和连接芯粒以构建可组合的SoC达成一致理解，这些SoC凭借高度的灵活性，能够满足AI工作负载的多样性需求，并确保最终芯片产品精准契合特定市场的需求。
参与 CSA 的多家合作伙伴也在 Arm 全面设计 (Arm Total Design) 生态项目中积极构建解决方案。Arm全面设计是一个致力于无缝交付由Arm Neoverse计算子系统 (CSS)驱动的定制芯片的生态系统。迄今为止，Arm全面设计已在部署基于芯粒的CSS 解决方案方面取得显著的成就，这些解决方案能够支持针对特定市场的战略实施，包括：
为多样化市场定制AI工作负载：Alphawave Semi 的客户对用于 AI工作负载的高性能芯片有着迫切需求，涵盖网络、边缘计算、存储和安全等领域。为了响应这些需求，Alphawave Semi 将基于Arm Neoverse CSS的芯粒与专有I/O晶粒 (die) 相结合，利用AMBA® CHI C2C技术，将针对不同市场需求定制的加速器互相连接。这些针对特定市场的定制化芯片基于一个标准化基础，能够有效分摊计算晶粒的成本，同时保持构建多种系统的灵活性。
革新大规模AI训练和推理工作负载：ADTechnology、三星晶圆代工厂、Rebellions和Arm[联合打造](https://mp.weixin.qq.com/s?__biz=MjM5MzAyMzkwOA==&mid=2247494616&idx=1&sn=774e5d824e3e79a2a780a1cf6ebfd3f9&scene=21#wechat_redirect)[了 AI CPU ](https://mp.weixin.qq.com/s?__biz=MjM5MzAyMzkwOA==&mid=2247494616&idx=1&sn=774e5d824e3e79a2a780a1cf6ebfd3f9&scene=21#wechat_redirect)[芯粒平台](https://mp.weixin.qq.com/s?__biz=MjM5MzAyMzkwOA==&mid=2247494616&idx=1&sn=774e5d824e3e79a2a780a1cf6ebfd3f9&scene=21#wechat_redirect)，用于数据中心大规模AI 工作负载的训练和推理，预计可为生成式 AI 工作负载（Llama3.1 405B 参数 LLMs）带来 2-3 倍的能效优势。该多供应商芯粒平台集成了Rebellions的REBEL AI加速器、使用AMBA CHI C2C互连技术的一致性NPU及 ADTechnology基于Neoverse CSS V3的计算芯粒，并采用三星晶圆代工厂的 2nm 全环绕栅极 (GAA) 制程工艺进行制造。这项成果得益于 CSA 的标准化工作进展。       

芯粒为不断增长的 AI 工作负载所需的定制芯片发挥关键作用
CSA 在基础设施、汽车及消费电子等多个市场领域，为 AI 技术驱动的多样化工作负载提供了高效的解决方案，并树立了多个成功案例。凭借 Arm 计算平台的卓越灵活性、AMBA CHI C2C 等标准所实现的无缝通信技术，以及CSA所引领的集成创新趋势，基于 Arm 技术的芯粒生态系统能够巧妙应对各市场中不断增长的 AI 需求。随着 CSA 生态系统的持续壮大，以及行业在标准化与协作方面的不断深化，Arm 将携手合作伙伴显著减少碎片化现象，并加速定制芯片解决方案的开发与部署。

---
**Tags:** [[Chiplet]]
