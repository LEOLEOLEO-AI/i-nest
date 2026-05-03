---
title: "谷歌Ironwood TPU与Axion CPU技术解析及行业影响"
source: "https://mp.weixin.qq.com/s/7QpUwOWyNp7j5AJMId90Sw"
created: 2025-11-07
note_id: "1892478181072592200"
tags:
  - "AI链接笔记"
  - "谷歌Ironwood TPU"
  - "Axion CPU"
  - "集成电路发展论坛"
  - "get-笔记"
  - "科技资讯"
---

# 谷歌Ironwood TPU与Axion CPU技术解析及行业影响

## 摘要

### 一、2025集成电路发展论坛信息  📅 **展会基本信息** - 名称：2025集成电路发展论坛（成渝）暨三十一届集成电路设计业展览会（ICCAD-Expo 2025） - 日期：2025年11月20-21日 - 地点：成都中国西部国际博览城 - 规模：展览面积20000㎡，参展商300+，

## 正文

公众号记得加星标⭐️，第一时间看推送不会错过。

[![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5b17f8d0d0d703cf2c197b28f57c5253?Expires=1780064561&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=XYabyVlv2Gr1BOPYy57bZJSh5yU%3D)](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247800430&idx=3&sn=3021338ba0a1372c7fadc4a7f71737c4&scene=21#wechat_redirect)

来源：内容来自theregister。

小心了，Jensen！谷歌凭借其 TPU 一次又一次地证明，重要的不是加速器的大小，而是它们在生产环境中扩展的效率。

如今，随着最新一代 Ironwood 加速器计划在未来几周内全面上市，Chocolate Factory 不仅拥有规模优势，而且还配备了强大的张量处理单元
(TPU)，足以与 Nvidia 的 Blackwell巨兽一较高下。

谷歌的 TPU v7 加速器于 4 月份首次发布，同时还与 El Capitan 超级计算机进行了滑稽的糟糕比较——不，Ironwood TPU Pod
的速度并不是美国能源部最大的钢铁机器的 24 倍——与前几代相比，谷歌的 TPU v7 加速器在性能上有了重大飞跃。

从历史上看，谷歌的 TPU 在原始 FLOPS、内存容量和带宽方面一直远逊于英伟达以及最近的 AMD 等公司的当代 GPU，谷歌只是通过增加 TPU
的数量来弥补这一不足。

谷歌以 Pod（大型、可扩展的计算域）的形式提供其 TPU，每个 Pod 包含数百甚至数千个芯片。如果需要额外的计算能力，用户可以扩展到多个 Pod。

在将浮点运算性能标准化到相同精度后，谷歌的 TPU v7 加速器提供的性能与英伟达 Blackwell GPU 的性能非常接近。

每个 Ironwood TPU 都拥有 4.6 petaFLOPS 的密集 FP8 性能，略高于 Nvidia 的 B200 的 4.5
petaFLOPS，略低于 GPU 巨头 Nvidia 更强大、更耗电的 GB200 和 GB300 加速器的 5 petaFLOPS。

该计算平台配备了 192 GB 的 HBM3e 内存，提供 7.4 TB/s 的带宽，这使其与英伟达的 B200（192GB HBM 和 8TB/s
内存带宽）处于同一水平。

对于芯片间通信，每个 TPU 具有四个 ICI 链路，可提供9.6 Tbps 的总双向带宽，而 B200 和 B300 的带宽为 14.4 Tbps (1.8
TB/s)。

简而言之，Ironwood 是谷歌迄今为止功能最强大的 TPU，其性能是 TPU v5p 的 10 倍，是去年发布的 TPU v6e“Trillium”加速器的
4 倍，并且大致与英伟达和 AMD 的最新芯片的性能相当。

**性能与规模相匹配**

但正如我们之前提到的，谷歌真正的诀窍在于能够将TPU扩展到真正庞大的计算域。英伟达的NVL72机架式系统利用其专有的NVLink互连技术，将72个最新的Blackwell加速器连接成一个单一的计算域。AMD明年也将在其Helios机架式系统和MI450系列中实现类似的功能。

相比之下，Ironwood 的规模就显得庞大了。

Ironwood不仅仅是对谷歌第六代 TPU 的渐进式改进。根据该公司公布的技术规格，与上一代产品相比，Ironwood
在训练和推理工作负载方面的性能提升超过四倍——谷歌将这一提升归功于系统级协同设计方法，而不仅仅是增加晶体管数量。

该架构最引人注目的特点是其规模。单个 Ironwood“模块”（由紧密集成的 TPU 芯片组成，作为一个超级计算机运行）可以通过谷歌专有的芯片间互连网络连接多达
9216 个独立芯片，传输速度高达每秒 9.6 太比特。为了更直观地理解这个带宽，它大致相当于在不到两秒的时间内下载整个美国国会图书馆。

这种庞大的互连架构使9216颗芯片能够共享1.77PB的高带宽内存——其速度足以跟上芯片的处理速度。这相当于约4万部高清蓝光电影的工作内存，可供数千个处理器同时即时访问。谷歌在技术文档中指出：“作为参考，这意味着Ironwood
Pods的FP8 ExaFLOPS性能是其最接近的竞争对手的118倍。”

该系统采用光路交换技术，构成一个“动态可重构架构”。当个别组件发生故障或需要维护时（在这种规模下，这种情况不可避免），OCS
技术会在几毫秒内自动将数据流量绕过中断点，从而使工作负载能够继续运行，而不会对用户造成任何可见的干扰。

这种对可靠性的重视体现了从前五代TPU部署中汲取的经验教训。谷歌报告称，自2020年以来，其液冷系统的整体正常运行时间一直保持在约99.999%的可用性水平——相当于每年停机时间不到6分钟。

需要明确的是，包含数十万个英伟达GPU的计算集群确实存在，而且实际上已经很常见。不同之处在于，在Blackwell架构之前，这些集群都是使用八路GPU单元构建的，并以大规模横向扩展的方式排列。英伟达的NVL72将计算单元的性能提升了九倍，但仍然远不及谷歌的TPU
POD。

谷歌扩展计算架构的方法与英伟达截然不同。这家GPU巨头为其机架级平台选择了一种大型、相对扁平的交换机拓扑结构，而谷歌则采用了一种3D环面拓扑结构，其中每个芯片都以三维网格的形式与其他芯片连接。

这种拓扑结构无需使用高性能数据包交换机，而高性能数据包交换机价格昂贵、耗电量大，并且在高负载下可能会引入不必要的延迟。

虽然环面拓扑可以消除交换机延迟，但网状拓扑意味着任何一个芯片与其他芯片通信可能需要更多跳数。随着环面规模的扩大，芯片间延迟的可能性也会增加。通过使用交换机，英伟达和AMD能够确保其GPU与下一个芯片之间的距离最多不超过两跳。

据我们了解，哪种方案更优取决于工作负载。某些工作负载可能受益于大型多跳拓扑结构，例如谷歌 TPU pod 中使用的 2D 和 3D
环面，而另一些工作负载则可能在英伟达和 AMD 机架式设计所提供的较小规模的交换式计算域上表现更佳。

因此，谷歌采用了一种不同的交换技术，使其能够将 TPU 模块切割成各种形状和尺寸，以便更好地适应其自身内部和客户的工作负载。

与你可能熟悉的包交换机不同，谷歌采用的是光路交换机（OCS）。这种交换机更像是20世纪的电话交换机。OCS设备使用多种方法（例如MEMS器件）将一个TPU连接到另一个TPU。由于这种连接通常是通过物理方式将一个端口连接到另一个端口来实现的，因此几乎不会引入延迟。

此外，OCS 还有助于提高容错能力，因为如果 TPU 发生故障，OCS 设备可以将其从网络中移除，并用正常工作的部件替换它。

**谷歌终于部署了自主设计的处理器**

尽管像谷歌Ironwood这样的AI加速器在人工智能时代的计算领域往往抢尽风头，但CPU对于应用程序逻辑、服务托管以及运行某些AI工作负载（例如数据采集）仍然至关重要。因此，除了第七代TPU之外，谷歌还在部署其首款基于Armv9架构的通用处理器，名为Axion。

谷歌尚未公布其 Axion CPU 的完整芯片规格：目前尚不清楚每个芯片的核心数量（除了 C4A Metal 实例最多可支持 96 个虚拟 CPU 和 768
GB DDR5 内存之外），也未公开时钟频率和工艺节点等信息。我们已知的是，Axion 基于 Arm Neoverse v2 平台构建，旨在提供比现代 x86
CPU 提升高达 50% 的性能和高达 60% 的能效，以及比目前云端速度最快的通用 Arm 架构实例高出 30% 的性能。有报道称，该 CPU 每个核心配备
2 MB 私有 L2 缓存，80 MB L3 缓存，支持 DDR5-5600 MT/s 内存，并支持统一内存访问 (UMA)。

Axion战略体现了一种日益增强的信念，即未来的计算基础设施既需要专用AI加速器，也需要高效的通用处理器。TPU负责运行AI模型这一计算密集型任务，而Axion级处理器则负责管理数据摄取、预处理、应用逻辑、API服务以及现代AI应用堆栈中的无数其他任务。

早期客户反馈表明，这种方法能够带来可衡量的经济效益。Vimeo 在初步的 N4A 测试中报告称，与同类 x86 虚拟机相比，其核心转码工作负载的性能提升了
30%。ZoomInfo 的首席基础设施架构师 Sergei Koren 表示，该公司在 Java 服务上运行的数据处理管道的性价比提升了 60%。

**软件工具可以将芯片性能转化为生产力**

如果开发者无法轻松利用硬件性能，那么硬件性能就毫无意义。谷歌强调，Ironwood和Axion都集成到了其所谓的AI
超级计算机中——“这是一个集成了计算、网络、存储和软件的超级计算系统，旨在提高系统级性能和效率。”

根据 IDC 2025 年 10 月发布的《商业价值快照》研究，人工智能超级计算机客户平均实现了 353% 的三年投资回报率、降低了 28% 的 IT
成本，并提高了 55% 的 IT 团队效率。

谷歌公布了多项旨在最大限度提高 Ironwood 利用率的软件增强功能。谷歌 Kubernetes Engine现在为 TPU
集群提供高级维护和拓扑感知功能，从而实现智能调度和高弹性部署。该公司开源的 MaxText 框架现在支持包括监督式微调和生成式强化策略优化在内的高级训练技术。

对于生产环境部署而言，谷歌推理网关最重要的优势或许在于它能够智能地在模型服务器之间进行请求负载均衡，从而优化关键指标。据谷歌称，通过前缀缓存感知路由等技术，它可以将首次令牌延迟降低
96%，并将服务成本降低高达 30%。

推理网关会监控关键指标，包括键值缓存命中率、GPU 或 TPU 利用率以及请求队列长度，然后将传入的请求路由到最佳副本。对于多个请求可能共享上下文的对话式 AI
应用，将具有共享前缀的请求路由到同一服务器实例可以显著减少冗余计算。

**战胜竞争对手**

自 2021 年 TPU v4 发布以来，谷歌就一直在其 TPU pod 中使用2D 和 3D 环面以及 OCS
设备。谷歌在生产环境中运行大规模计算架构方面也经验丰富。

其 TPU v4 支持最大 4096 个芯片的 POD，而 TPU v5p 则将其提升了一倍多，达到 8960 个芯片。因此，对于谷歌来说，Ironwood 将
TPU POD 的数量提升到 9216 个应该不成问题。

这些海量计算资源的出现无疑引起了各大模型构建者的关注，其中包括那些与谷歌Gemini模型直接竞争的公司。Anthropic是谷歌最大的客户之一，该公司已宣布计划利用多达一百万个TPU来训练和运行其下一代Claude模型。

考虑到模型开发商 Anthropic 还在Project Rainier下将其工作负载部署到亚马逊数十万台 Trainium 2
加速器上，而这些加速器在其计算结构中也采用了 2D 和 3D 环面网格拓扑结构，因此 Anthropic 采用 Google 的 TPU 技术也就不足为奇了。

尽管英伟达首席执行官黄仁勋可能会淡化人工智能ASIC对其GPU帝国的威胁，但很难忽视这样一个事实：谷歌、亚马逊等公司的芯片在硬件能力和网络可扩展性方面正在迅速赶上，而软件往往最终成为决定性因素。

或许这就是为什么分析师们每个季度都会不断提出这个问题的原因。

\*免责声明：本文由作者原创。文章内容系作者个人观点，半导体行业观察转载仅为了传达一种不同的观点，不代表半导体行业观察对该观点赞同或支持，如果有任何异议，欢迎联系半导体行业观察。

***END***

**今天是《半导体行业观察》为您分享的第4219期内容，欢迎关注。**

**推荐阅读**

★[一颗改变了世界的芯片](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247732748&idx=1&sn=2ba19055f90ac8ab5512098d039ef391&chksm=ce6e4cfbf919c5eddc8b3af5a147990afc3c7227f59c332d15ed5f8b8a100a4dcb97f59d05d1&scene=21#wechat_redirect)

★[美国商务部长：华为的芯片没那么先进](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247735441&idx=6&sn=786b62b5f4edbac37b66f91ff36d0f49&chksm=ce6e5a66f919d37052778a97f49442c77529699f08f3dcf599c99347dcf35da064528aab5222&scene=21#wechat_redirect)

★[“ASML新光刻机，太贵了！”](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247738477&idx=1&sn=636a6387c4e83b7e47e6377aba07f8d4&chksm=ce6e269af919af8cc2bfddf1dff60566bfd0169eb1c31d97413c6f97abe8d307cda0b58cc795&scene=21#wechat_redirect)

★[悄然崛起的英伟达新对手](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247741738&idx=1&sn=860c31832b6c6e03b152300b991be5f9&scene=21#wechat_redirect)

★[芯片暴跌，全怪特朗普](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247746259&idx=1&sn=f9a5a82f84e598d0f2d8b8d2cb1d371e&chksm=ce6e0024f919893285b3069f01821e6bd47cb772c890cacf88874707e1576ecc3d7673290afb&scene=21#wechat_redirect)

★[替代EUV光刻，新方案公布！](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247732748&idx=1&sn=2ba19055f90ac8ab5512098d039ef391&scene=21#wechat_redirect)

★[半导体设备巨头，工资暴涨40%](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247723271&idx=7&sn=1e4f5124fa7d3f029e4c212823633e1e&scene=21#wechat_redirect)

★[外媒：美国将提议禁止中国制造的汽车软件和硬件](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247756729&idx=8&sn=7763455e2146a96c6c5945c7092c9c90&scene=21#wechat_redirect)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff7a8f1fb68b0124ac9bfba335b700b01?Expires=1780064561&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=xL6%2BniR%2BD0%2BQSkKWe9qgfaRZNRk%3D)

加星标⭐️第一时间看推送，小号防走丢

求点赞

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5b10506cd8d868c4b29a421d44d425b4?Expires=1780064561&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=RPhhU0xLKzaTLSVRLv8NPQrTJ2A%3D)

求分享

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3dce8a8a52ab940486a4ef8ad59da555?Expires=1780064561&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Kh9Z%2FvnaGmgNopvh7wzse1uSaDM%3D)

求推荐

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb9435339555bddfa8906c222e99bf93f?Expires=1780064561&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=tvqURhvM7SesM9Ct6ZaHXfUlvgg%3D)

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 10:22*