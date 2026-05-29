# Chiplet与异构集成技术研究

> 笔记本: 微信  
> 创建时间: 2021-03-07  

---

速读摘要
说是一个庞大的工作，其2019年版本包括了23个章节，也涵盖了异构集成的方方面面内容。本文的下面的重点是讨论通过异构集成追求更高性能(面向HPC和数据中心的高端芯片)，看看这个方向上异构集成技术会怎么发展。从延续摩尔定律这个目标来说，新的集成技术的目标就是实现更高的性能。Model的角度分析异构集成是如何实现"抬高"Roofline(即提升性能上限)这一目标的。简单来说，这个项目的目标就是把光互连推到芯片封装里面。
原文约 4957  字   |  图片 14 张  |  建议阅读 10 分钟  |  [评价反馈](https://static.app.yinxiang.com/embedded-web/clipper/#/Evaluating?d=2021-03-07&nu=dd8a3791-eaab-4f43-8ef8-291296839d76&fr=myyxbj&ud=1bb10ab&v=2&sig=85D9FA9DA4A11733B1A6EBE3A1883359)

 


##  Chiplet与异构集成技术研究 

原创唐杉 StarryHeavensAbove **


收录于话题
基础芯片技术
22个


Chiplet的概念很火，我之前也写过一篇文章，**[从AI Chip到AI Chiplet](http://mp.weixin.qq.com/s?__biz=MzI3MDQ2MjA3OA==&mid=2247484890&idx=1&sn=a9464f059dab39c0f2d77c086ccccd66&chksm=ead1f8cbdda671ddd48789e1636839b930a7466004faa61119c5cfb76bb43f1efa667558f29c&scene=21#wechat_redirect)，**初步的分析它的基本特征，优势，前景和一些挑战。Chiplet的重要性，不仅是给摩尔定律“续命”，也开启了很多新的机会，其前景毋庸置疑。Chiplet虽然是个新词，但其背后更通用的说法：异构集成（Heterogeneous Integration），并不是新概念。从Chiplet到异构集成，涉及内容很多，也非常有意思，值得仔细研究讨论一下。

**Heterogeneous Integration Roadmap**
Chiplet可以看作是异构集成（Heterogeneous Integration）的一个子集。如果大家希望比较完整和系统的了解HI技术，一个比较好的来源是“HIR: Heterogeneous Integration Roadmap”[1]。大家可能都比较熟悉半导体行业著名的一个路线图ITRS（International Technology Roadmap for Semiconductors）。但ITRS对半导体产业的展望工作到2016年就终止了，HIR则是从2016年开始，某种程度上可以说代表了新的时代。

HIR的愿景如下：

而下表则反应了HIR和ITRS的对比，出发点和模式类似。

Source: Heterogeneous Integration Roadmap Working Group
HIR可以说是一个庞大的工作，其2019年版本包括了23个章节，也涵盖了异构集成的方方面面内容。这些内容包括了几个维度，第一个是市场和应用场景维度，包括下面6个主要领域：High Performance Computing and Data Centers; Medical，Health and Wearables; Autonomous Automotive; Mobile; Aerospace and Defense; IoT。显然，不同的领域，异构集成的需求大不相同。早期的发展里，手机是异构集成的一大推动力。为了节省空间，手机里面应用处理器AP和存储器通常会使用Package-on-Package集成，而其它组件也使用了各种各样的集成和封装方式。
而HPC和数据中心芯片，则追求高性能。汽车，航空航天，可穿戴，IoT这些领域也都有各自重点关注的需求和挑战，这里不再赘述。

第二个维度主要是通过如下一些电子系统的基本组成模块来讨论对集成技术的需求，包括：Single Chip and Multi Chip Integration (including substrate); Integrated Photonics; Integrated Power Electronics; MEMS and Sensor integration; 5G and Analog and Mixed Signal。这些是异构集成的基础组件。

第三个维度是底层基础技术，包括Materials and Emerging Research Materials; Emerging Research Device；Test；Supply Chain; Thermal Management; Co-Design; Simulation。

最后是和异构集成关系最紧密的三个综合技术领域：SiP；3D & 2D Interconnections；Wafer-Level Packaging - WLP (fan in and fan out)。

HIR的内容太多，也涉及很多细节的讨论，很难给出一个简化的版本，大家还是自己去浏览一下比较好。它的23个章节由不同专家撰写，完成度不太一样，也有一定的重复，其中应用场景相关需求和挑战写的都比较清楚；关键技术相关的部分，比如，“Single Chip and Multi Chip Integration”，也有很高的参考价值。

本文的下面的重点是讨论通过异构集成追求更高性能（面向HPC和数据中心的高端芯片），看看这个方向上异构集成技术会怎么发展。这里异构集成希望解决的问题包括：**Die size limitation**（工艺和良率的限制，Die的面积很难继续增大）；**The Processor-Memory Performance Gap**（传统的架构挑战）；**Exploiting Accelerators for Emerging Applications**（领域专用架构的更多使用）；**Package IO Limitations for future Ethernet Switches and Routers**（I/O瓶颈对系统扩展性的影响） ；**Integration of dies from diverse nodes and technologies**（集成不同工艺节点的Die的需求，典型的包括Compute，Memory，I/O的集成）。

**HBM集成的实例**
异构集成涉及相当多的内容和概念，为了方便后面的讨论，下面通过目前在高端芯片中已经广泛使用的HBM（High-Bandwidth Memory）集成来说明一些重要基本的概念。

source: WikiChip
这张图来自WikiChip的“Chip-on-Wafer-on-Substrate (CoWoS) - TSMC”条目，不代表最新的技术，这里借用一下来讨论。这是一个芯片剖面图，主要是看看封装里包括哪些部件和连接。最底层是PCB电路板，上面则是芯片（包括封装和内部的各层Die），芯片通过Package Balls焊接到PCB上。进入封装之内，最底层是Package Substrate（封装基板），它一方面保护、固定、支撑芯片，增强导热散热性能，保证芯片不受物理损坏；另一方面实现芯片和下层PCB间的电气和物理连接、功率分配、信号分配，以及沟通芯片内部与外部电路等功能。再上面是Silicon Interposer，这一层实际上也是一个Silicon Die，只是这个Die上只有连线和TSV（Through Silicon Vias），用于实现它上面集成的各种功能Die之间的连接（比如从Compute Die到HBM存储器），以及功能Die和下层的Package Substrate的连接。由于这个Die只有连线，而且线宽和间距是um级的，所以是通过比较老旧工艺实现的。Interposer和Package Substrate间使用的是C4 Cu Bumps，和功能Die的连接使用μBump，图中可以明显看出，μBump的尺寸相对其它层级的Bunp要小很多，密度要大很多。

再往上就是各种功能Die了，这里稍微展开一下HBM部分。

source：Joungho Kim, "Kim’s Law: Vertical Stack-up Trends"
HBM实际上是有多颗DRAM Die在垂直方向堆叠而成，最底层是一个逻辑功能的Die，实现控制和接口功能。这个接口通过上述Interposer中的连线和Compute Die（比如CPU或GPU Die）连接。HBM首先利用了垂直方向的空间，可以更好的利用封装内的空间增加存储容量，更重要的是，它和Comput Die之间的连接封装内利用interposer中的连线实现的，其功耗比访问封装外的DRAM低的多。

上述的HBM集成方案，是一个典型的2.5D集成技术。同时，2.5D集成还有其它几类方案，如下图。其差别主要是Die之间的连接通过什么方式实现。其中Intel推的方案是EMIB，它不需要额外的Silicon Interposer，只是在Package Substrate中对性能要求最高的部分使用高密度连接，因此具有成本的优势。

source: Intel
HBM的成功是异构集成优势的一个很好的实例，即**通过先进的集成和封装技术实现更高的计算和存储密度，计算和存储之间更高的带宽，同时降低能量的消耗**。

下图是目前主流的HBM集成的供应链的情况。

source: System Plus Consulting
如果看目前比较成熟的集成方案，虽然已经展示了异构集成的潜力，但成本也是巨大的。技术的复杂度增加，工艺流程增加（参考[8]），集成模块更多导致的整体良率降低，集成和封测的成本大增，一般也只有追求最高性能的高端芯片能够用的起。此外，标准化和供应链的因素也是影响Chiplet普及的重要障碍。从另一个角度来看，我们对性能要求是无止境的，现有的集成方案需要不断改进甚至做大幅度的革新。

**技术发展**
从延续摩尔定律这个目标来说，新的集成技术的目标就是实现更高的性能。大家知道，Roofline模型是描述一个架构的性能极限的常用模型。下图来自ERI Summit 2020中TSMC的keynote，就是从Roofline Model的角度分析异构集成是如何实现“抬高”Roofline（即提升性能上限）这一目标的。

source: Dr. H.-S. Philip Wong @ ERI Summit 2020
在Roofline模型里，“屋脊”的两根线，水平的代表处理器的峰值算力（这里的Processor peak throughput），可以分解为核的数量，核的频率以及每个时钟周期的操作数数量这几个因素；而斜线的高度由存储带宽决定。不同的Workload，由于处理密度（Operational intensity）不同，在图中处于不同位置，但这个“屋脊”是性能上限。由于摩尔定律放缓，功耗的限制，Die Size的限制，在单个Die上提高Roofline已经非常困难（领域专用架构DSA可能抬高Roofline，但同样受到这些限制）。这里的一个例外是Cerebras搞的WSE，感兴趣的可以参考“[**如何设计一颗40PFLOPS量级的AI芯片？**](http://mp.weixin.qq.com/s?__biz=MzI3MDQ2MjA3OA==&mid=2247484629&idx=1&sn=8297f335784f63b7010880dc0ca07b28&chksm=ead1f9c4dda670d2652c842aa8555f1d32abc74e9da0a91d812233f9c39034fc3cd7694d0570&scene=21#wechat_redirect)”。
很自然的想法就是在一个封装内集成更多的Die，包括更多领域专用处理器，同时让memory和compute的距离更近。这个讲演里，Dr. H.-S. Philip Wong上来第一句话就是，“*my message today is very simple, the future is system integration*”。
长远来看，最终目标是Monolithic 3D（图中红框的部分：N3XT是一个方案），即所有计算和存储（包括新型存储）的Die都在垂直方向按照分层的方式集成，是现有芯片工艺的在垂直方向上更大规模的延申。
Wikipedia的“Three-dimensional integrated circuit”条目中，总结了这类集成技术在诸多方面存在的挑战和限制：Cost，Yield（每增加一个步骤，就会增加缺陷的概率），Heat（集成密度越高，性能越高，散热越困难），Design Complexity（需要越来越复杂的技术和EDA工具），TSV-introduced overhead（不同层间的TSV的占用的空间很大），Testing（很难分层测试，不利于分解问题），Lack of Standards，Heterogeneous integration supply chain（不同部分来自不同厂商），Lack of clearly defined ownership（谁来主导？）。


Monolithic 3D的概念不难理解，应该是一个终极目标；但技术挑战极大，有自己的演进路径，且距离尚远，这里就不再深入。让我们回到之前讨论的HBM集成实例，看看沿着这个基本的集成框架，有哪些改进的机会。为了讨论方便，这里再贴一下第一部分用的图：


source: WikiChip
从这个图中，我们可以看到一些可以继续提升的点。其目标简单来讲就是，**集成更多种类和数量的Die，并尽可能减少它们之间的通信开销。**
****
首先，是**垂直方向发展**。可以在垂直方向堆叠更多的HBM DRAM Die，HBM2E目前已经可以堆叠8颗Die。这里插一句，Samsung在这次ISSCC上提出的在HBM DRAM Die上加入Compute是个有意思的发展。这块的演进基本掌握在Memory厂商手中。其它类型的Die，也可以在垂直方向不断堆叠，即向Monolithic 3D方向发展。
第二个是**Silicon interposer的改进**。这块的可能性还是挺多的，比如增大面积，上面可以放更多或者更大的计算（包括DSA），存储或者IO Die；增加功能，比如加入Active的逻辑，而不是目前只有连线，Intel的Foveros就是这方面的改进；使用更细的连线，增加连线密度（也包括Package Substrate），等等。由于Interposer也是来自foundry，这部分的改进也是依赖foundry的。
第三个要提升的是**Die之间的互连**，这里又涉及几个方面的内容。首先是互连标准和IP，如上图中的HBM标准，有相应的IP供应商；而其它的Die之间，比如上图的Comput和Logic之间（也包括其它组合，如多个Compute Die，Compute和IO Die等等），和HBM不同，这类Die to Die互连目前并没有统一的标准（有一些方案），但有相应的IP供应商。这方面虽然有一些标准化的努力，但由于核心厂商不多，也都很强势，能否形成一个统一的标准还很难说。此外，上图中的μBump的尺寸和密度对互连的性能和功耗也非常重要，相关改进的研究也很多，甚至包括不适用Bump直接“粘贴”两个Die。下图就是Intel提出的封装路线图。可以看出，即使是对μBump这个点的改进，也是一个循序渐进的过程。无线通信和光通信也是未来可能的Die to Die通信技术。整体来讲，Died之间的互连主要是Foundry和IP厂商共同驱动的。

source: Intel @ Hotchips 2020
最后，**如何****降低成本**？上述的技术改进虽然能够获得更高的性能和功耗效率，但大部分都增加了实现的难度和流程的复杂度，意味着更高的成本。因此，如何降低成本可能是最技术普及最大的挑战。

**远景**
到这里，我们讨论的内容都是比较贴近业界现状的。如果要看异构集成的未来，我们不妨来参考DARPA ERI中的相关项目。

source: Dr. H.-S. Philip Wong @ ERI Summit 2020
这个图也是来自[4]，可以说是DARPA ERI项目中和异构集成相关的项目的一个总结。这里将相关的项目分成了几个层次。第一个层次的CHIPS项目我们都比较熟悉了，强调了Chiplet通过模块化和重用，促进不同工艺的集成，降低芯片开发的整体成本。其重点任务在于驱动Chiplet的标准化和相关的重用模式。这个项目中的一个成果是Intel的AIB（Advanced Interface Bus）标准。标准化对于Chiplet的发展固然重要，但如前所述，由于供应链的特点，这种标准化的前景还有待观察。

3DSoC（3 Dimensional Monolithic System on a Chip）项目实际就是要推进前面提到过的Monolithic 3D技术。在2020 ERI Summit上，SkyWater和MIT有个相关的展示（基于碳纳米管），大家可能也看到过新闻。该项目和LUMOS （Lasers for Universal Microscale Optical Systems）及FRANC（Foundations Required for Novel Compute）项目一起放在作为新材料方向（更远期）的探索。T-MUSIC(Technologies for Mixed-mode Ultra Scaled Integrated Circuits)主要是探索在CMOS工艺上支持太赫兹射频的方法，和PIPES项目在一起主要是展示异构集成对于芯片功能多样性的帮助。

这里我比较关注的是PIPES（Photonics in the Package for Extreme Scalability）项目。简单来说，这个项目的目标就是**把光互连推到芯片封装里面**。我们直接看下图这个例子就很容易明白。


source：Intel/Ayar Labs
这个例子来自被Intel收购的Ayar Lab，正好也用到了本文前面讲的2.5D Chiplet的技术。左图是概念图，下面绿色的就是Package Substrate，中间是一个FPGA Die，边上Die是光I/O的Phy（TeraPHY）。FPGA Die和TeraPHY就是通过Intel的EMIB模式连接的（没有额外的Interposer）。右边就是最终的封装外形，可以看到，正是把光I/O放到封装里。下图正好可以体会一下EMBI的Substrate。

source：Intel/Ayar Labs
先看这个项目本身的重要性。电互连的提升空间已经不大了，未来要进一步提升互连性能，光互连是必然选择。但是传统的光模块一般是到达电路板，然后再通过电接口连接到芯片，必然出现瓶颈。这个项目推动的技术如果成功，则可解决这一问题，进而推进基于光互连的系统大规模扩展的问题。从另一个角度看，这个项目的实施，正好也充分利用了异构集成技术的能力。

异构集成的终极目标是集成不同用途，不同工艺（甚至是**完全不同类**的工艺）的组件，如下图所示的“集大成”的例子。而沿另一个方向思考，也许可以把现在的一个Server的能力集成到一个封装之内？

source: Georgia Tech PRC

****
我本来是希望用比较短的篇幅来介绍Chiplet和异构集成涉及的技术，但发现即使篇幅超出了预期仍然很难把所有问题交待清楚。大家要是感兴趣，还是建议延伸阅读后面附上的参考文献。当然，个人能力所限，难免有疏漏错误之处，还请大家批评指正。本文算是抛砖引玉吧，期待看到更多更深入的讨论。


**参考资料**
[1] Heterogeneous Integration Roadmap 2019 Edition
[2] HIR Workshop at ECTC 2019
[3] 2020 Symposia on VLSI Technology and Circuits SC2
[4] ERI Summit 2020: Heterogeneous 3D Microsystems: Design, Fabrication, and Packaging
[5] The Open Domain-Specific Architecture: A Chiplet-Based Open Architecture
[6] www.3dincites.com
[7] https://en.wikipedia.org/wiki/Three-dimensional_integrated_circuit
[8] 胡承維，"CoWoS ＆ Fan-Out Process Flow"


公众号专题：
[**人工智能芯片技术基础**](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI3MDQ2MjA3OA==&action=getalbum&album_id=1374108991751782402&token=825417533&lang=zh_CN#wechat_redirect)
[**人工智能芯片技术进步**](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI3MDQ2MjA3OA==&action=getalbum&album_id=1374097412805165056&token=825417533&lang=zh_CN#wechat_redirect)[**人工智能芯片产业发展**](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI3MDQ2MjA3OA==&action=getalbum&album_id=1374089812021673988#wechat_redirect)[**人工智能芯片初创公司**](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI3MDQ2MjA3OA==&action=getalbum&album_id=1600178502002098179&token=825417533&lang=zh_CN#wechat_redirect)[**人工智能芯片评测对比**](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI3MDQ2MjA3OA==&action=getalbum&album_id=1600208703943688199&token=825417533&lang=zh_CN#wechat_redirect)[**科技巨头的芯片尝试**](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI3MDQ2MjA3OA==&action=getalbum&album_id=1600213438406934529&token=825417533&lang=zh_CN#wechat_redirect)[**从学术会议看人工智能芯片**](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI3MDQ2MjA3OA==&action=getalbum&album_id=1600183908778721281#wechat_redirect)**[基础芯片技术](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI3MDQ2MjA3OA==&action=getalbum&album_id=1678711252069466118#wechat_redirect)**

题图来自网络，版权归原作者所有
本文为个人兴趣之作，仅代表本人观点，与就职单位无关

---
**Tags:** [[SDSoW]] [[Chiplet]]

---
## 相关笔记 (AI 自动关联)
- [[Chiplet技术带来的新“四化”]]
- [[MIT 异构Chiplet集成构建下一代计算的 超级芯片]]
- [[Chiplet：将彻底颠覆这一行业]]
