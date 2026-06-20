---
title: UCIe 3.0来了：Chiplet互连速度翻倍
tags:
- chip
- chip-hardware
- chiplet
- semiconductor
- topology
- wafer
---
> 笔记本: 我的剪贴板  
> 创建时间: 2025-08-15  

---

原文链接: [https://mp.weixin.qq.com/s/NOq88ELQfwwB3x5xQrSklg](https://mp.weixin.qq.com/s/NOq88ELQfwwB3x5xQrSklg)


公众号记得加星标⭐️，第一时间看推送不会错过。

来源：内容来自nextplatform


随着云计算、高性能计算（HPC）以及如今的人工智能（AI）推动企业计算不断发展，再加上半导体设计与制造相关的技术挑战和成本持续增加，对Chiplet（小芯片）架构的需求也在不断上升。
过去几年，英特尔、AMD等系统级芯片（SoC）制造商一直在不断增强其Chiplet能力，将更小、可复用的小芯片以模块化架构组合在一起，以提升效率、灵活性和定制化能力。不过，这些基于Chiplet的半导体目前仍依赖各自厂商的专有互连技术来实现连接。
Universal Chiplet Interconnect Express（UCIe）联盟于2022年成立，由英特尔、AMD、高通、台积电（TSMC）等半导体公司，以及Google Cloud、Meta、微软等超大规模云厂商共同推动。该联盟的目标是制定一套标准化的互连规范，使不同厂商、不同晶圆厂生产、不同功能的小芯片能够在单一封装中协同工作，从而实现更高的灵活性、效率和定制化。当年，UCIe 1.0规范便同步发布。


本周，UCIe联盟（现已拥有140多名成员）推出了开放式Chiplet标准的3.0版本，在功耗效率与管理方面做了多项增强，并保持向后兼容。但最引人关注的是性能提升——新规范支持48 GT/s和64 GT/s的数据速率，是一年前发布的UCIe 2.0（32 GT/s带宽）的两倍。
这种性能提升，旨在满足联盟所称的“对高带宽永无止境的需求”，特别是在AI、HPC和数据分析等快速扩张的领域中，这些领域的封装可用互连边界长度（即芯片间连接的物理边缘长度）十分有限。


数据速率的翻倍适用于UCIe-S（2D标准封装）和UCIe-A（2.5D先进封装）设计。诸如AI等应用需要在有限的互连边界长度内获得越来越高的吞吐量。
“在很多应用中，我们都受到封装互连边界的限制，这在AI和HPC领域尤为突出，但其他领域也紧随其后。”


英特尔资深院士、UCIe联盟主席Debendra Das Sharma在接受The Next Platform采访时表示，“你需要更高的线性带宽密度。换句话说，你必须在给定的互连边界长度上提供更多带宽，因为芯片尺寸不会仅仅为了带宽需求而改变——它可能因其他原因改变，但不会为了芯片间带宽而变。这就是我们把数据速率从32 Gb/s提升到48 Gb/s甚至64 Gb/s的原因。”


Das Sharmas 表示，3D设计方面并没有变化。
“它仍然是非常低的频率，因为在较低凸点密度下，我们已经拥有非常高的带宽——每平方毫米数百TB/s，甚至多到用不完，因此在3D侧不需要提升，这样可以非常节能。而在2D和2.5D封装中，则确实需要在固定的互连边界长度内提供更高带宽。”
提升数据速率的关键是保持3.0版本与之前版本的向后兼容。
联盟在白皮书中写道：“这是至关重要的，因为它确保了现有系统和基础设施能够无缝集成新标准。该规范保留了现有的边带、有效信号、时钟跟踪、数据、训练和信令协议，为系统设计人员和开发人员提供平滑的过渡，并确保与前几代规范设计的小芯片互操作。”


随着标准适用范围的扩大，这一点也尤为重要。虽然UCIe在数据中心、HPC和AI系统中的应用已广为人知，但它将具有普遍性。
Das Sharma说：“如今，一切都是Chiplet架构，这无关领域。你看看手持设备或PC，它们都是由Chiplet构建的。UCIe跨越所有领域，汽车也是一个重要应用。我们认为它就像PCIe（今年6月也迎来了速度升级）一样，只不过PCIe是板级互连，而UCIe可以从手持设备一直用到数据中心。比如UCIe-A更适合高端小芯片，比如AI应用；而手持设备没有这种带宽需求，所以我们有2D封装。这是一个我们想要覆盖的完整计算连续体。”
这个连续体还包括数字信号处理器（DSP）以及无线基础设施、雷达系统等应用。
“当然，我们希望进入AI、HPC和数据中心这些领域，但我们的目标也包括其他市场。这就是我们的定位——那只是我们的一部分‘赛道’。”
UCIe 3.0还带来了其他改进，包括：
运行时重新校准（runtime recalibration）：可重用初始化状态，在运行过程中实现低功耗的链路调优；
更灵活的SIP（Session Initiation Protocol）拓扑：通过扩展边带通道（最长可达100毫米）实现；
连续传输协议支持：通过Raw Mode映射实现不中断的数据流，适用于SoC与DSP小芯片互连等新型应用。


参考链接


https://www.nextplatform.com/2025/08/08/uci-express-cranks-up-chiplet-interconnect-speeds/


*免责声明：本文由作者原创。文章内容系作者个人观点，半导体行业观察转载仅为了传达一种不同的观点，不代表半导体行业观察对该观点赞同或支持，如果有任何异议，欢迎联系半导体行业观察。


***END***

**今天是《半导体行业观察》为您分享的第4120期内容，欢迎关注。**


**推荐阅读**

★[一颗改变了世界的芯片](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247732748&idx=1&sn=2ba19055f90ac8ab5512098d039ef391&chksm=ce6e4cfbf919c5eddc8b3af5a147990afc3c7227f59c332d15ed5f8b8a100a4dcb97f59d05d1&scene=21#wechat_redirect)
★[美国商务部长：华为的芯片没那么先进](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247735441&idx=6&sn=786b62b5f4edbac37b66f91ff36d0f49&chksm=ce6e5a66f919d37052778a97f49442c77529699f08f3dcf599c99347dcf35da064528aab5222&scene=21#wechat_redirect)
★[“ASML新光刻机，太贵了！”](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247738477&idx=1&sn=636a6387c4e83b7e47e6377aba07f8d4&chksm=ce6e269af919af8cc2bfddf1dff60566bfd0169eb1c31d97413c6f97abe8d307cda0b58cc795&scene=21#wechat_redirect)
★[悄然崛起的英伟达新对手](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247741738&idx=1&sn=860c31832b6c6e03b152300b991be5f9&scene=21#wechat_redirect)
★[芯片暴跌，全怪特朗普](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247746259&idx=1&sn=f9a5a82f84e598d0f2d8b8d2cb1d371e&chksm=ce6e0024f919893285b3069f01821e6bd47cb772c890cacf88874707e1576ecc3d7673290afb&scene=21#wechat_redirect)
★[替代EUV光刻，新方案公布！](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247732748&idx=1&sn=2ba19055f90ac8ab5512098d039ef391&scene=21#wechat_redirect)
★[半导体设备巨头，工资暴涨40%](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247723271&idx=7&sn=1e4f5124fa7d3f029e4c212823633e1e&scene=21#wechat_redirect)
★[外媒：美国将提议禁止中国制造的汽车软件和硬件](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247756729&idx=8&sn=7763455e2146a96c6c5945c7092c9c90&scene=21#wechat_redirect)


加星标⭐️第一时间看推送，小号防走丢


求点赞


求分享


求推荐

---
**Tags:** [[Chiplet]]

---
## 相关笔记 (AI 自动关联)
- [[UCIe生态正在完善，Chiplet腾飞指日可待]]
- [[Chiplet电话会议纪要]]
- [[打破Chiplet的最后一道屏障：全新互联标准UCIe宣告成立]]
