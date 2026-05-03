---
title: "Simplex Micro：突破冯·诺依曼架构的确定性计算革命"
source: "https://mp.weixin.qq.com/s/3HfqiW5NOqWQz6M8hV_InQ"
created: 2025-09-09
note_id: "1886988375349718280"
tags:
  - "AI链接笔记"
  - "预测执行"
  - "时间资源矩阵"
  - "统一计算架构"
  - "get-笔记"
  - "科技资讯"
---

# Simplex Micro：突破冯·诺依曼架构的确定性计算革命

## 摘要

🔄 **传统计算架构的瓶颈**   - 半个世纪以来，计算基础依赖冯·诺依曼/哈佛模型，CPU、GPU等均为其变体   - 现有方案（VLIW、数据流芯片、GPU）为单点优化，无法全面替代传统架构   - 传统架构痛点：GPU功耗高且内存瓶颈突出，CPU并行性不足，多芯片方案存在延迟与同步问题   

## 正文

公众号记得加星标⭐️，第一时间看推送不会错过。

来源：内容编译自semiwiki。

半个多世纪以来，计算的基础一直建立在单一架构之上：冯·诺依曼模型或哈佛模型。几乎所有现代芯片——CPU、GPU，甚至许多专用加速器——都依赖于这种设计的某种变体。随着时间的推移，业界不断提升复杂性和专业化程度，以满足新的需求。超长指令字
(VLIW) 架构、数据流芯片和 GPU 最初都是作为针对特定瓶颈的单点解决方案而引入的，但都未能提供全面的替代方案。直到现在。

Simplex Micro
开发出的技术可能是半个多世纪以来对传统范式最重大的突破——在单一确定性流水线中实现统一的标量、矢量和矩阵计算。其核心是一个革命性的概念：预测执行。与猜测下一步会发生什么的动态执行不同，预测执行以周期级精度静态地调度每个操作，将处理器转变为具有已知执行时间线的确定性机器。这使得单芯片架构无需单独的加速器即可同时处理通用任务和高吞吐量
AI 工作负载。

确定性执行消除了动态执行的低效性和漏洞。预测性执行无需动态调度指令并回滚错误路径，而是确保每条指令都在正确的时间以正确的资源发出。它不仅更高效，而且可预测、可扩展，并且本质上更安全。

突破在于 Simplex
所谓的“时间资源矩阵”：这是一种新颖的专利调度机制，可以跨时间分配计算、内存和控制资源。每条指令都有指定的时隙和访问窗口，确保零重叠并消除流水线停顿。可以将其想象成火车时刻表——只不过火车是在同步计算结构中移动的标量、矢量和矩阵运算。

这项创新允许单个处理器同时充当 CPU 和加速器，无需切换开销，无需内存层次结构不匹配，也无需在异构单元之间进行昂贵的数据传输。它是一种通用架构，性能堪比专用
AI 引擎，在许多情况下甚至超越了它们。

这种统一是通过一系列已获专利的创新技术实现的，这些创新技术已被证明与现有技术并无直接关联。时间资源矩阵提供了基础的执行调度，而其他突破则将其扩展到新的领域：幻影寄存器允许系统超越物理寄存器文件的限制来流水线化指令；矢量数据缓冲器和扩展矢量寄存器集则支持无缝扩展AI操作的并行计算。指令重放缓冲器确保即使是可变延迟的内存或分支事件也能得到可预测的解析，而无需进行动态执行猜测。

这些发明共同构成了计算引擎的基石，它拥有与 CPU 类似的灵活性，但又能提供加速器般的持续吞吐量，无需两块独立的芯片。无论是矩阵密集型的 AI
推理，还是控制密集型的实时决策，同一个处理器都能高效、同步地处理，无需架构切换。这不仅代表着通用计算的一次演进，更是一次真正的重塑。

随着人工智能工作负载规模和复杂性的不断增长，传统架构不堪重负。GPU 需要巨大的功耗预算，并且仍然面临内存瓶颈。CPU
缺乏现代推理和训练任务所需的并行性。同时，多芯片解决方案也面临延迟、同步和软件碎片化等问题。

借助预测执行，Simplex 提供了一个统一的、时间驱动的机器，该机器已在 RISC-V 矢量处理器中实现，并已准备好集成到下一代 AI
基础架构中。这并非一个理论概念——它实际上是一个基于仿真结果的 RTL 级执行器，可以运行生产代码。

对于芯片架构师而言，这意味着更简单的系统设计，更小的硅片占用空间。对于软件开发人员而言，这意味着可以编写统一、可预测的目标，并具有一致的时序行为——这对于安全关键型和性能敏感型应用来说都是理想的选择。

这不仅仅是性能的提升，更是对架构优雅的回归，一颗芯片即可胜任多种任务，且性能丝毫不受影响。通过消除动态执行，并将执行置于确定性时间窗口内，Simplex
打造了一个可根据未来 AI、边缘计算和云应用需求进行扩展的平台。

随着我们迈入人工智能驱动应用的新时代，对可扩展、统一且确定性计算的需求空前高涨。预测执行奠定了基础，我们诚邀研究和工程界在此基础上继续发展。

参考链接

https://semiwiki.com/ip/361169-beyond-von-neumann-toward-a-unified-deterministic-architecture/

\*免责声明：本文由作者原创。文章内容系作者个人观点，半导体行业观察转载仅为了传达一种不同的观点，不代表半导体行业观察对该观点赞同或支持，如果有任何异议，欢迎联系半导体行业观察。

***END***

**今天是《半导体行业观察》为您分享的第4149期内容，欢迎关注。**

**推荐阅读**

★[一颗改变了世界的芯片](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247732748&idx=1&sn=2ba19055f90ac8ab5512098d039ef391&chksm=ce6e4cfbf919c5eddc8b3af5a147990afc3c7227f59c332d15ed5f8b8a100a4dcb97f59d05d1&scene=21#wechat_redirect)

★[美国商务部长：华为的芯片没那么先进](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247735441&idx=6&sn=786b62b5f4edbac37b66f91ff36d0f49&chksm=ce6e5a66f919d37052778a97f49442c77529699f08f3dcf599c99347dcf35da064528aab5222&scene=21#wechat_redirect)

★[“ASML新光刻机，太贵了！”](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247738477&idx=1&sn=636a6387c4e83b7e47e6377aba07f8d4&chksm=ce6e269af919af8cc2bfddf1dff60566bfd0169eb1c31d97413c6f97abe8d307cda0b58cc795&scene=21#wechat_redirect)

★[悄然崛起的英伟达新对手](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247741738&idx=1&sn=860c31832b6c6e03b152300b991be5f9&scene=21#wechat_redirect)

★[芯片暴跌，全怪特朗普](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247746259&idx=1&sn=f9a5a82f84e598d0f2d8b8d2cb1d371e&chksm=ce6e0024f919893285b3069f01821e6bd47cb772c890cacf88874707e1576ecc3d7673290afb&scene=21#wechat_redirect)

★[替代EUV光刻，新方案公布！](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247732748&idx=1&sn=2ba19055f90ac8ab5512098d039ef391&scene=21#wechat_redirect)

★[半导体设备巨头，工资暴涨40%](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247723271&idx=7&sn=1e4f5124fa7d3f029e4c212823633e1e&scene=21#wechat_redirect)

★[外媒：美国将提议禁止中国制造的汽车软件和硬件](https://mp.weixin.qq.com/s?__biz=Mzg2NDgzNTQ4MA==&mid=2247756729&idx=8&sn=7763455e2146a96c6c5945c7092c9c90&scene=21#wechat_redirect)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff7a8f1fb68b0124ac9bfba335b700b01?Expires=1780067394&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=cJ9a6AZ8mzyUNd9PlL6K5T%2Fxmvw%3D)

加星标⭐️第一时间看推送，小号防走丢

求点赞

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5b10506cd8d868c4b29a421d44d425b4?Expires=1780067394&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=FZMkLzeEu22bPjDAiDPM4CXvu50%3D)

求分享

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3dce8a8a52ab940486a4ef8ad59da555?Expires=1780067394&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=lQo%2FouCW1fXtcyK6MoGYONaQz00%3D)

求推荐

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb9435339555bddfa8906c222e99bf93f?Expires=1780067394&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=xKV%2FICeY9m2NbTQGTQHxWLanfoE%3D)

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 11:09*