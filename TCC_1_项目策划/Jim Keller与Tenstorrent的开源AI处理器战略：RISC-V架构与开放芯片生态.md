---
title: "Jim Keller与Tenstorrent的开源AI处理器战略：RISC-V架构与开放芯片生态"
source: "https://mp.weixin.qq.com/s/heHRkzcWLllTBxTn1vnfRA"
created: 2025-09-14
note_id: "1887413063863406368"
tags:
  - "AI链接笔记"
  - "Jim Keller"
  - "RISC-V AI处理器"
  - "开放芯片架构"
  - "get-笔记"
  - "AI研究"
---

# Jim Keller与Tenstorrent的开源AI处理器战略：RISC-V架构与开放芯片生态

## 摘要

### 🔹 核心人物与使命 - **Jim Keller**：芯片行业传奇人物，曾任职英特尔、AMD、特斯拉硬件部门高管，现领导Tenstorrent推动开源AI处理器创新 - **使命**：解决AI硬件"昂贵且封闭"的痛点，通过开源架构和模块化设计，让高性能AI计算更普及、可扩展  ### 🔹 O

## 正文

公众号记得加星标⭐️，第一时间看推送不会错过。

来源：内容来自technews。

曾经在英特尔、AMD、特斯拉等公司硬件部门任职高阶主管Jim Keller 成功领导了多个成功芯片开发计划，被大家称之为「芯片大神」
的传奇人物，在日前的一场演讲中开场就表示，公司将藉由开放原始码的RISC-V 架构提出全新的AI 处理器，利用普通的DRAM
和以太网来构建高性能AI，让任何人都能建造和扩展它，将AI 应用更快速的普及。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F8373ee091b492548ff1f1519c0e3cef9?Expires=1780067042&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=kHHmZXDNDgGcDwqaznUrU3B1LBI%3D)

Jim Keller 表示，Tenstorrent 正在建造一座特殊的电脑工厂，目标是生产所有现代高阶AI
电脑和高性能处理器所需的零组件。一直以来，Tenstorrent 一直致力于打造高阶AI 电脑和具备大量IP
与技术的高速CPU，如今产品已经开始出货，包括可扩展的Galaxy box 伺服器，以及为了回应客户抱怨噪音而设计的水冷quiet box
等。此外，我们还推出了PCI Express卡，并刚开始向客户提供Eson TPU 作为IP。令人兴奋的是，还已经将AI
处理器出货给多家客户，其中包含LG，他们将AI 处理器整合到电视芯片中。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd4dff0fc7a6de158ad27607ce31a3c1b?Expires=1780067042&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=1yf9wyYxW7rOojSYzs%2FTw3GObF0%3D)

于这些Tenstorrent 的成果，Jim Keller 强调自己是个任务导向的人，虽然长远来看也希望公司能够赚钱。但更重要的是要有一个使命，就是当今AI
世界正在彻底改变一切，随处都可见对「千兆瓦」、「兆位元组」
产品的需求。但这一切都变得越来越大、越来越昂贵，而且很多技术是专有的。尽管有些模型是开源的，但大部分仍然是封闭的。因此，我的使命是创造更便宜、更快、更开放的新型架构。

为此，Tenstorrent 制定了一项宏伟计划，就是正在打造基于开源架构的RISC-V CPU。而这款正在开发的开放式AI
处理器，其来自于一个无意的开源事件，就是一位网路上的年轻人透过逆向工程公布了我们处理器的所有细节，并发布了规格。这个看来恼人的事件，却反而促使我们认为这是一个好主意。因为，如果有人想从头开始构建自己的AI
电脑，网路上很快就会有完整的规格和参考模型。

基于此，我们还承诺将建立一个完全开放原始码的软件堆叠，从模型、编译器、快速操作器、运行时环境的低层指令集等，都将是全部都是开放的。这代表着，如果你购买我们的硬件，你可以清楚地看到所有内部运作。目标就是是利用普通的DRAM
和以太网来构建高性能AI，让任何人都能建造和扩展它。

Jim Kelle 强调，在硬件方面，Black Hole 是我们采用台积电6 奈米制程的芯片，它包含140个张量处理器和RISC-V
处理器，并且支援GDDR6 DRAM
和片上SRAM。我们选择不使用HBM，因为它过于昂贵且封装复杂。我们的策略是制造更多、更小、更便宜的芯片。例如，一块板上有八个Black Hole
芯片，四块板组成一个盒子，总共有32 个芯片，提供1TB 的DRAM 和16TB 的频宽。每个芯片都有以太网接口，所有连接都具备冗余，确保系统的可靠性。

就目前的情况来说，AI 训练的挑战在于尽管可以编写模型，但要使其快速运行却是一个复杂的HPC问题。因此，Tenstorrent 的训练电脑拥有2,000
个Black Hole 芯片，相当于超过一百万个RISC-V 处理器协同运作，这需要巨大的协作和优化。至于，实现低成本的AI 训练方面，目前许多大型AI
模型（如OpenAI 和XAI 的模型） 可能是开源的，但对于我们这些需要自己训练模型的人来说，能够以低成本进行训练至关重要。我们的训练电脑由九个Galaxy
box
组成一个单元，所有连接都具备冗余，即使有线缆故障也能正常运行。多个这样的单元可以进一步组成更大的训练集群，提供从上到下的一致视角，这让管理数百个Galaxy
box 成为可能。

Jim Kelle 强调指出，建造一个芯片成本高昂，我们的Black Hole 芯片耗资约8,000
万美元。每次升级AI，我们都需要再花费数千万美元来打造新芯片。因此，我们的下一代解决方案是采用小芯片（chiplets）。我们将CPU、记忆体控制器和AI
等组件设计成模组化的积木。尽管现有多个小芯片互连标准，目标是确保我们的芯片家族能协同工作，并与UCIe 标准兼容。

Tenstorrent
正在努力实现芯片的独立迭代和组合成完整解决方案，将提供采用这些小芯片的解决方案，同时也将这些小芯片开放给希望自行开发解决方案的客户。为此，我们发起了开放小芯片架构（Open
Chiplet Architecture） 计划，这不仅仅是芯片间的互连标准，还包括测试、重置、系统加密等所有组件。我们将贡献所有相关IP
给这个联盟，甚至计划推出一种空芯片（empty chip） 一个包含所有必要IP 系统的芯片裸晶，让客户可以轻松地将自己的IP 整合进去并快速推向市场。

最后，Jim Kelle
表示，过去许多人会问我们到底卖什么？答案是我们销售我们所做的一切。无论是IP、芯片还是系统，我们都会销售。我们甚至还提供云端服务，让新创公司可以在我们的机器上托管他们的应用。最终，我希望让下一代电脑设计变得更加有趣。这使得人们觉得电脑设计越来越昂贵、越来越困难的情况消失。透过小芯片技术、更好的IP、更优化的验证以及开源的AI
驱动方法，电脑设计将会变得更好、更易于实现。我希望能凝聚大家的力量，共同创造一个充满无限可能的未来。

\*免责声明：本文由作者原创。文章内容系作者个人观点，半导体行业观察转载仅为了传达一种不同的观点，不代表半导体行业观察对该观点赞同或支持，如果有任何异议，欢迎联系半导体行业观察。

***END***

**今天是《半导体行业观察》为您分享的第4153期内容，欢迎关注。**

**推荐阅读**

★[一颗改变了世界的芯片](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247732748&idx=1&sn=2ba19055f90ac8ab5512098d039ef391&chksm=ce6e4cfbf919c5eddc8b3af5a147990afc3c7227f59c332d15ed5f8b8a100a4dcb97f59d05d1&scene=21#wechat_redirect)

★[美国商务部长：华为的芯片没那么先进](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247735441&idx=6&sn=786b62b5f4edbac37b66f91ff36d0f49&chksm=ce6e5a66f919d37052778a97f49442c77529699f08f3dcf599c99347dcf35da064528aab5222&scene=21#wechat_redirect)

★[“ASML新光刻机，太贵了！”](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247738477&idx=1&sn=636a6387c4e83b7e47e6377aba07f8d4&chksm=ce6e269af919af8cc2bfddf1dff60566bfd0169eb1c31d97413c6f97abe8d307cda0b58cc795&scene=21#wechat_redirect)

★[悄然崛起的英伟达新对手](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247741738&idx=1&sn=860c31832b6c6e03b152300b991be5f9&scene=21#wechat_redirect)

★[芯片暴跌，全怪特朗普](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247746259&idx=1&sn=f9a5a82f84e598d0f2d8b8d2cb1d371e&chksm=ce6e0024f919893285b3069f01821e6bd47cb772c890cacf88874707e1576ecc3d7673290afb&scene=21#wechat_redirect)

★[替代EUV光刻，新方案公布！](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247732748&idx=1&sn=2ba19055f90ac8ab5512098d039ef391&scene=21#wechat_redirect)

★[半导体设备巨头，工资暴涨40%](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247723271&idx=7&sn=1e4f5124fa7d3f029e4c212823633e1e&scene=21#wechat_redirect)

★[外媒：美国将提议禁止中国制造的汽车软件和硬件](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247756729&idx=8&sn=7763455e2146a96c6c5945c7092c9c90&scene=21#wechat_redirect)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff7a8f1fb68b0124ac9bfba335b700b01?Expires=1780067042&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=nwuUOlpcDEKQC5cFWjavp97jMO8%3D)

加星标⭐️第一时间看推送，小号防走丢

求点赞

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5b10506cd8d868c4b29a421d44d425b4?Expires=1780067042&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ea6RdcetGf65kmbDKdXE4ZFvM8s%3D)

求分享

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3dce8a8a52ab940486a4ef8ad59da555?Expires=1780067042&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=J3WV8%2B7xPZY3786q86YYyY2KW6A%3D)

求推荐

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb9435339555bddfa8906c222e99bf93f?Expires=1780067042&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=H3RnEGBOXEQRcxq7UfnUy6CBOH4%3D)

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 11:04*