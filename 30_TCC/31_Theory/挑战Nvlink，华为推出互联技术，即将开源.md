# 挑战Nvlink，华为推出互联技术，即将开源

> 笔记本: 我的剪贴板  
> 创建时间: 2025-08-28  

---

原文链接: [https://mp.weixin.qq.com/s/Y--1MDh2awMS-Hp-BdymYA](https://mp.weixin.qq.com/s/Y--1MDh2awMS-Hp-BdymYA)


公众号记得加星标⭐️，第一时间看推送不会错过。


来源：内容编译自tomshardware。


利用其Hot Chips 2025大会的演讲契机，华为推出了UB-Mesh技术，该技术旨在通过单一协议统一AI数据中心内外部节点的所有互连。该公司还表示，将在下个月的活动中宣布向所有用户免费开放该协议。
该技术旨在用单一协议取代PCIe、CXL、NVLink和TCP/IP协议，以降低延迟、控制成本并提高千兆级数据中心的可靠性。为了推动这一举措，华为计划开源该规范。但它会获得广泛关注吗？
华为处理器部门海思半导体首席科学家廖恒（音译）表示：“下个月我们将召开一次会议，宣布UB-Mesh协议将像免费许可证一样向所有人开放。” “这是一项非常新的技术；我们看到不同阵营正在竞相推进标准化工作。根据我们在实际系统部署方面的成功程度以及合作伙伴和客户的需求，我们可以讨论将其转化为某种标准。”
虽然用于训练和推理的 AI 数据中心应该像一个大型并行处理器一样运行，但它们由独立的机架、服务器、CPU、GPU、内存、SSD、NIC、交换机和其他组件组成，这些组件使用不同的总线和协议相互连接，例如 UPI、PCIe、CXL、RoCE、NVLink、UALink、TCP/IP 以及即将推出的超级以太网等等。协议转换需要耗电，会增加延迟和成本，并引入潜在的故障点，所有这些因素在拥有数百万个处理器的千兆瓦级数据中心中都可能造成灾难性的后果。


华为无需费力处理大量的链路和协议，而是提出了一个名为 UB-Mesh 的统一框架，使任何端口都能在无需转换的情况下与其他端口通信。这种简化的设计减少了转换延迟，简化了设计，并且在需要时仍保留了通过以太网运行的空间，从而将整个数据中心转变为一个通过 UB-Mesh 连接的连贯超级节点。


华为将 SuperNode 定义为数据中心规模的 AI 架构，将多达 1,000,000 个处理器（无论是 CPU、GPU 还是 NPU）、池化内存、SSD、NIC 和交换机统一到一个系统中，每芯片带宽从 100 Gbps 提升到 10 Tbps（1.25 TB/s，甚至超出 PCIe 8.0 所能提供的带宽），跳跃延迟从微秒级降低到 ~150 ns，整体设计从异步 DMA 转向同步加载/存储语义。
这种结构旨在降低延迟，允许所有高速 SERDES 连接灵活重用，甚至支持通过以太网操作以实现向后兼容。


然而，华为承认，在整个数据中心推广这一概念会带来新的挑战，尤其是从铜缆（仍在机架内部连接）过渡到可插拔光纤链路。长距离传输不可避免地需要使用光纤，但其错误率远高于电气连接。为了解决这个问题，华为提出了链路级重试机制、光模块内的备份通道以及将控制器连接到多个模块的交叉设计。这些措施旨在确保即使单个链路或模块发生故障也能持续运行，尽管这显然会增加成本。


UB-Mesh 的网络拓扑结构是混合的。在顶层，CLOS 结构将整个大厅的机架连接在一起。在其下层，多维网格将连接每个机架内的数十个节点。这种混合模型旨在避免传统设计在系统扩展到数万或数十万个节点时产生的高昂成本。


此外，可靠性必须超越单个链路的范畴。华为概述了一种系统模型，当另一个机架发生故障时，热备用机架会自动接管。然后，故障机架会被修复并轮换回来，以保持可用性。华为表示，这种设计将平均故障间隔时间延长了几个数量级，这对于百万芯片系统来说是一个必要的改进。
从成本角度来看，根据华为的数据，差异显而易见。传统互连的成本往往会随着节点数量的增加而线性增长，这意味着它们最终可能会超过AI加速器（例如Nvidia的H100或B200）本身的价格。相比之下，UB-Mesh的扩展速度呈亚线性，容量增加时成本不会相应增加。华为甚至提出了一个结合CLOS和二维网格单元的8192节点实用系统，作为可行性的证明。


借助 UB-Mesh 和 SuperNode，华为正在提供一套系统级架构，旨在支持国内外的大规模 AI 集群。如果这些技术能够成功落地，华为将减少（或者更确切地说，彻底摆脱）其下一代数据中心对 PCIe、NVLink、UALink 甚至 TCP/IP 等西方标准的依赖。华为并非在 CPU、GPU 甚至机架级解决方案上与 AMD、英特尔和英伟达竞争，而是致力于打造一套数据中心级的解决方案。
但问题是，除了华为之外，还有其他公司会采用这项举措吗？因为该公司的客户是否有兴趣从单一供应商那里获得数据中心基础设施仍有待观察。为此，华为正在开放 UB-Mesh 链路协议，供全球评估。如果华为自身部署成功，并且第三方有足够的兴趣，那么它可以将 UB-Mesh 打造成标准，甚至可能将超级节点架构本身标准化。
然而，业界是否感兴趣还有待观察。Nvidia 依靠其机架内部的 NVLink 连接以及整个数据中心的以太网或 InfiniBand 连接。AMD、博通和英特尔等其他公司正在推动 UALink 用于机舱间通信，以及超级以太网用于数据中心范围的连接。这两种技术都已标准化，并得到了众多公司的支持，从而实现了灵活性并降低了成本。


**参考链接**


https://www.tomshardware.com/tech-industry/artificial-intelligence/huawei-to-open-source-its-ub-mesh-data-center-scale-interconnect-soon-details-technical-aspects-one-interconnect-to-rule-them-all-is-designed-to-replace-everything-from-pcie-to-tcp-ip
*免责声明：本文由作者原创。文章内容系作者个人观点，半导体行业观察转载仅为了传达一种不同的观点，不代表半导体行业观察对该观点赞同或支持，如果有任何异议，欢迎联系半导体行业观察。


***END***

**今天是《半导体行业观察》为您分享的第4139期内容，欢迎关注。**


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
**Tags:** #Chiplet
