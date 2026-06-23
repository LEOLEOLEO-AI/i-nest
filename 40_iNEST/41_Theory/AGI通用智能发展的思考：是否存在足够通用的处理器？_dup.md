---
title: AGI通用智能发展的思考：是否存在足够通用的处理器？
tags:
- ai-ml
- artificial-intelligence
- chip
- chiplet
- criticality
- deep-learning
- emergence
- large-language-model
- paper
- survey
---
> 笔记本: 技术学习  
> 创建时间: 2023-06-04  

---

#  AGI通用智能发展的思考：是否存在足够通用的处理器？ 

原创Chaobowx 软硬件融合 **

收录于合集

系统架构5个
人工智能9个
超异构计算28个

欢迎关注软硬件融合公众号：

**编者按**
随着ChatGPT的火爆，AGI（Artificial General Intelligence，通用人工智能）逐渐看到了爆发的曙光。短短一个月的时间，所有的巨头都快速反应，在AGI领域“重金投入，不计代价”。
AGI是基于大模型的通用智能；相对的，之前的各种基于中小模型的、用于特定应用场景的智能可以称之为专用智能。
那么，我们可以回归到一个大家经常讨论的话题：向左（专用）还是向右（通用）？在芯片领域，大家针对特定的场景开发了很多专用的芯片。是否可以类似AGI的发展，开发足够通用的芯片，既能够覆盖几乎所有场景，还能够功能和性能极度强大？
# **1 AGI发展综述**

## **1.1 AGI的概念**

AGI通用人工智能，也称强人工智能（Strong AI），指的是具备与人类同等甚至超越人类的智能，能表现出正常人类所具有的所有智能行为。
ChatGPT是大模型发展量变到质变的结果，ChatGPT具备了一定的AGI能力。随着ChatGPT的成功，AGI已经成为全球竞争的焦点。
与基于大模型发展的AGI对应的，传统的基于中小模型的人工智能，也可以称为弱人工智能。它聚焦某个相对具体的业务方面，采用相对中小参数规模的模型，中小规模的数据集，然后实现相对确定、相对简单的人工智能场景应用。
## **1.2 AGI特征之一：涌现**

“涌现”，并不是一个新概念。凯文·凯利在他的《失控》中就提到了“涌现”，这里的“涌现”，指的是众多个体的集合会涌现出超越个体特征的某些更高级的特征。
在大模型领域，“涌现”指的是，当模型参数突破某个规模时，性能显著提升，并且表现出让人惊艳的、意想不到的能力，比如语言理解能力、生成能力、逻辑推理能力等等。
对外行（比如作者自己）来说，涌现能力，可以简单的用“量变引起质变”来解释：随着模型参数的不断增加，终于突破了某个临界值，从而引起了质的变化，让大模型产生了许多更加强大的、新的能力。

如果想详细了解大模型“涌现”能力的详细分析，可以参阅谷歌的论文《Emergent Abilities of Large Language Models》。
当然，目前，大模型发展还是非常新的领域，对“涌现”能力的看法，也有不同的声音。例如斯坦福大学的研究者对大语言模型“涌现”能力的说法提出了质疑，认为其是人为选择度量方式的结果。详见论文《Are Emergent Abilities of Large Language Models a Mirage?》。
## **1.3 AGI特征之二：多模态**

每一种信息的来源或者形式，都可以称为一种模态。例如，人有触觉、听觉、视觉等；信息的媒介有文字、图像、语音、视频等；各种类型的传感器，如摄像头、雷达、激光雷达等。多模态，顾名思义，即从多个模态表达或感知事物。而多模态机器学习，指的是从多种模态的数据中学习并且提升自身的算法。
传统的中小规模AI模型，基本都是单模态的。比如专门研究语言识别、视频分析、图形识别以及文本分析等单个模态的算法模型。
基于Transformer的chatGPT出现之后，之后的AI大模型基本上都逐渐实现了对多模态的支持：
- 
首先，可以通过文本、图像、语音、视频等多模态的数据学习；
- 
并且，基于其中一个模态学习到的能力，可以应用在另一个模态的推理；
- 
此外，不同模态数据学习到的能力还会融合，形成一些超出单个模态学习能力的新的能力。
多模态的划分是我们人为进行划分的，多种模态的数据里包含的信息，都可以被AGI统一理解，并转换成模型的能力。在中小模型中，我们人为割裂了很多信息，从而限制的AI算法的智能能力（此外，模型的参数规模和模型架构，也对智能能力有很大影响）。
## **1.4 AGI特征之三：通用性**

从2012年深度学习走入我们的视野，用于各类特定应用场景的AI模型就如雨后春笋般的出现。比如车牌识别、人脸识别、语音识别等等，也包括一些综合性的场景，比如自动驾驶、元宇宙场景等。每个场景都有不同的模型，并且同一个场景，还有很多公司开发的各种算法和架构各异的模型。可以说，这一时期的AI模型，是极度碎片化的。
而从GPT开始，让大家看到了通用AI的曙光。最理想的AI模型：可以输入任何形式、任何场景的训练数据，可以学习到几乎“所有”的能力，可以做任何需要做的决策。当然，最关键的，基于大模型的AGI的智能能力远高于传统的用于特定场合的AI中小模型。   
完全通用的AI出现以后，一方面我们可以推而广之，实现AGI+各种场景；另一方面，由于算法逐渐确定，也给了AI加速持续优化的空间，从而可以持续不断的优化AI算力。算力持续提升，反过来又会推动模型向更大规模参数演进升级。
# **2 专用和****通用的关系**


牧本波动（Makimoto's Wave）是一个与摩尔定律类似的电子行业发展规律，它认为集成电路有规律的在“通用”和“专用”之间变化，循环周期大约为10年。也因此，芯片行业的很多人认为，“通用”和“专用”是对等的，是一个天平的两边。设计研发的产品，偏向通用或偏向专用，是基于客户场景需求，对产品实现的权衡。
但从AGI的发展来看，基于大模型的AGI和传统的基于中小模型的专用人工智能相比，并不是对等的两端左右权衡的问题，而是从低级智能升级到高级智能的问题。我们再用这个观点重新来审视一下计算芯片的发展历史：
- 
专用集成电路ASIC是贯穿集成电路发展的一直存在的一种芯片架构形态；
- 
在CPU出现之前，几乎所有的芯片都是ASIC；但在CPU出现之后，CPU迅速的取得了芯片的主导地位；CPU的ISA包含的是加减乘除等最基本的指令，也因此CPU是完全通用的处理器。
- 
GPU最开始的定位是专用的图形处理器；自从GPU改造成了定位并行计算平台的GP-GPU之后，辅以帮助用户开发的CUDA的加持，从而成就了GPU在异构时代的王者地位。
- 
随着系统复杂度的增加，不同客户系统的差异性和客户系统的快速迭代，ASIC架构的芯片，越来越不适合。行业逐渐兴起了DSA的浪潮，DSA可以理解成ASIC向通用可编程能力的一个回调，DSA是具有一定编程能力的ASIC。ASIC面向具体场景和固化的业务逻辑，而DSA则面向一个领域的多种场景，其业务逻辑部分可编程。即便如此，在AI这种对性能极度敏感的场景，相比GPU，AI-DSA都不够成功，本质原因就在于AI场景快速变化，但AI-DSA芯片迭代周期过长。
从长期发展的角度看，专用芯片的发展，是在给通用芯片探路。通用芯片，会从各类专用计算中析取出更加本质的足够通用的计算指令或事务，然后把之融合到通用芯片的设计中去。比如：
- 
CPU完全通用，但性能较弱，所以就通过向量和张量等协处理器的方式，实现硬件加速和性能提升。
- 
CPU的加速能力有限，于是出现了GPU。GPU是通用并行加速平台。GPU仍然不是性能最高的加速方式，也因此，出现了Tensor Core加速的方式。
- 
Tensor Core的方式，仍然没有完全释放计算的性能。于是，完全独立的DSA处理器出现。

智能手机是通用和专用的一个经典案例：在智能手机出现之前，各种各样的手持设备，琳琅满目；智能手机出现之后，这些功能专用的设备，就逐渐消失在历史长河中。
通用和专用，并不是，供设计者权衡的，对等的两个方面；从专用到通用，是低级到高级的过程。短期来看，通用和专用是交替前行；但从更长期的发展来看，专用是暂时的，通用是永恒的。
# **3 通用处理器是否可行？**

CPU是通用的处理器，但随着摩尔定律失效，CPU已经难堪大用。于是，又开始了一轮专用芯片设计的大潮：2017年，图灵奖获得者John Hennessy和David Patterson就提出“体系结构的黄金年代”，认为未来一定时期，是专有处理器DSA发展的重大机会。
但这5-6年的实践证明，以DSA为代表的专用芯片黄金年代的成色不足。反而在AI大模型的加持之下，成就了通用GPU的黄金年代。
当然，GPU也并不完美：GPU的性能即将，如CPU一样，到达上限。目前，支持GPT大模型的GPU集群需要上万颗GPU处理器，一方面整个集群的效率低下，另一方面集群的建设和运行成本都非常的高昂。

是否可以设计更加优化的处理器，既具有通用处理器的特征，尽可能的“放之四海而皆准”，又可以更高效率更高性能？这里我们给一些观点：
- 
我们可以把计算机上运行的系统拆分为若干个工作任务，如一些软件进程或相近软件进程的组合可以看做是一个工作任务；
- 
广泛存在的二八定律：系统中的工作任务，并不是完全随机的，很多工作业务是相对确定的，比如虚拟化、网络、存储、安全、数据库、文件系统，甚至人工智能推理，等等；并且，即使应用层的比较随机的计算任务，仍然会包含大量确定性的计算成分，例如一些应用包含安全、视频图形处理、人工智能等相对确定的计算部分。
- 
我们把处理器（引擎）按照性能效率和灵活性能力，简单的分为三个类型：CPU、GPU和DSA。
- 
类似“塔防游戏”，依据二八定律，把80%的计算任务交给DSA完成，把16%的工作任务交给GPU来完成，CPU负责剩余4%的其他工作。CPU很重要的工作是兜底。
- 
依据性能/灵活性的特征，匹配到最合适的处理器计算引擎，可以在实现足够通用的情况下，实现最极致的性能。
# **4 通用处理器的历史和发展**


如果我们以通用计算为准，计算架构的演进，可以简单的划分为三个阶段，即从同构走向超异构，再持续不断的走向超异构：
- 
第一代通用计算：CPU同构。
- 
第二代通用计算：CPU+GPU异构。
- 
第三代（新一代）通用计算：CPU+GPU+DSAs的超异构。
## **4.1 第一代通用计算：CPU同构**

##     

Intel发明了CPU，这是第一代的通用计算。第一代通用计算，成就了Intel在2000前后持续近30年的霸主地位。
CPU标量计算的性能非常弱，也因此，CPU逐渐引入向量指令集处理的AVX协处理器以及矩阵指令集的AMX协处理器等复杂指令集，不断的优化CPU的性能和计算效率，不断的拓展CPU的生存空间。
## **4.2 第二代通用计算：CPU+GPU异构**


CPU协处理器的做法，本身受CPU原有架构的约束，其性能存在上限。在一些相对较小规模的加速计算场景，勉强可用。但在AI等大规模加速计算场景，因为其性能上限较低并且性能效率不高，不是很合适。因此，需要完全独立的、更加重量的加速处理器。
GPU是通用并行计算平台，是最典型的加速处理器。GPU计算需要有Host CPU来控制和协同，因此具体的实现形态是CPU+GPU的异构计算架构。
NVIDIA发明了GP-GPU，以及提供了CUDA框架，促进了第二代通用计算的广泛应用。随着AI深度学习和大模型的发展，GPU成为最炙手可热的硬件平台，也成就了NVIDIA万亿市值（超过Intel、AMD和高通等芯片巨头的市值总和）。
当然，GPU内部的数以千计的CUDA core，本质上是更高效的CPU小核，因此，其性能效率仍然存在上升的空间。于是，NVIDIA开发了Tensor加速核心来进一步优化张量计算的性能和效率。
## **4.3 第三代（面向未来的）通用计算：CPU+GPU+DSAs超异构**


技术发展，永无止境。第三代通用计算，即多种异构融合的超异构计算，面向未来更大算力需求场景的挑战：
- 
首先，有三个层次的独立处理引擎。即CPU、GPU和DSA。（相应的，第一代CPU只有一个，第二代异构计算有两个。）
- 
多种加速处理引擎，都是和CPU组成CPU+XPU的异构计算架构。
- 
超异构不是简单的多种异构计算的集成，而是多种异构计算系统的，从软件到硬件层次的，深度融合。
- 
超异构计算，要想成功，必须要实现足够好的通用性。如果不考虑通用性，超异构架构里的相比以往更多的计算引擎，会使得架构碎片化问题更加严重。软件人员无所适从，超异构就不会成功。
（正文完）
更多阅读：
- 
[从ChatGPT等大模型的兴起，看未来计算芯片的发展趋势](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247488290&idx=1&sn=ead71d194e0c8ac82a1fc8520f6c5730&chksm=c12ed367f6595a7128353a97f3b7beb2d30a4238f35f726780371f60f80ed673a8b7746da971&scene=21#wechat_redirect)
- 
[从算力网络发展，看未来十年的宏观算力体系](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247488237&idx=1&sn=c157d057bd7ec61161d3e7469517dec3&chksm=c12ed2a8f6595bbef20cfe716e88f2f3d045597a23d3b01713e608e7f711779bbdcd9ddbe654&scene=21#wechat_redirect)
- 
[超异构处理器HPU和系统级芯片SOC的区别在哪里？](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247488203&idx=1&sn=5828f791ecef28a95449568093d62168&chksm=c12ed28ef6595b982633232a03e4eb434123dd6183ca526fe13fe6a5deeb609b35edb68c4bd9&scene=21#wechat_redirect)
- 


[超异构计算时代的操作系统架构初探](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247487967&idx=1&sn=708114e3ce500acf64ffaf2668ed8263&chksm=c12ed19af659588c6b6bf1fe86eea98ad744f60563d6b72918efc5ef70dad2a3f10490716064&scene=21#wechat_redirect)
- 


[异构计算面临的挑战和未来发展趋势](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247487918&idx=1&sn=6d879ad760e25ae06b19feae8691447b&chksm=c12ed1ebf65958fdcffcb97ca386ae9f97030c1f126ae2f4525713831b2829cf17e2b809e01b&scene=21#wechat_redirect)
- 


[汽车芯片技术趋势分析：未来5年，单芯片算力突破20000 TOPS](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247487875&idx=1&sn=6f8339d7c45d4e8d7835add311888c79&chksm=c12ed1c6f65958d0f6dedc0c23e23890b3d80e0241ec089e65fc7dfc1930e86f4dd593d24e9c&scene=21#wechat_redirect)
- 


[Intel Sapphire Rapids CPU，吹响反攻DPU的号角](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247487676&idx=1&sn=04a406987f5b6469764047f821ab6287&chksm=c12ed0f9f65959ef24ee5ad81f7175a44989c33f2f904e3bc0d6e15b4220084d319ed67f539c&scene=21#wechat_redirect)
- 


[为什么要从“软硬件协同”走向“软硬件融合”？](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247487597&idx=1&sn=88a3333b5dc22c1c63238fd722f0c2cd&chksm=c12ed028f659593e32debcb8d6fd92847d11cda76d057d6d85e8b737ab2f0f63e738f1d1893c&scene=21#wechat_redirect)
- 


[未来，所有芯片公司都需要进化成互联网公司](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247487437&idx=1&sn=5a5ac38b22a3dfd600f47f1d6c41602d&chksm=c12ecf88f659469ea10a35f4da7e4b312cc19116241c96da8449249cbe9f7d3a99e7a9e44e2e&scene=21#wechat_redirect)
- 


[从NVIDIA自动驾驶芯片Thor，看大芯片的发展趋势](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247487393&idx=1&sn=5545d1c5dea7d7afd66558e9708fc3dc&chksm=c12ecfe4f65946f237c6b673e81f54e78b9f2ef001a3b8b8a83be4d64d9e90b549add21ae480&scene=21#wechat_redirect)
- 


[“黄金年代”之后，计算机体系结构将何去何从？](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247487273&idx=1&sn=ca48d4ca83e7ac4924e2357b181465b9&chksm=c12ecf6cf659467a9f4901d8b45f7f4312d5462f85dbe9058a7377a16ce2719f13ccc0bf6673&scene=21#wechat_redirect)
- 


[从DPU看大芯片的发展趋势](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247487054&idx=1&sn=6a6a9016077d897b4998e273acf13007&chksm=c12ece0bf659471d524c8aaf39caa8d3c34a4b37516207ebfc3ef7a4589e4d39edbc3285844c&scene=21#wechat_redirect)
- 


[大芯片面临的共同挑战](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247487007&idx=1&sn=03e4a3bea7490f60b74bed4edb0df9db&chksm=c12ece5af659474c23ff8a733411ea164b55e83b8d16325e7dc48f6242252dd4e85d9135b429&scene=21#wechat_redirect)
- 


[超异构 x Chiplet：双剑合璧，实现算力指数级提升](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247486931&idx=1&sn=0bf86b1e7f3f8d71ab1614f2a5b7c45f&chksm=c12ecd96f6594480c3a1dc5771356dd17569d215151cb488b4c5ddeb22575b10091b8f928b4b&scene=21#wechat_redirect)
- 


[异构计算，NVIDIA已经在行动](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247486775&idx=1&sn=cab8e6f6b2f4fbb8891ac613b3e52485&chksm=c12ecd72f6594464d9c86b30feea415f13d6f6b11de75fa9db541f4c901df6b9efa5adce5353&scene=21#wechat_redirect)
- 


[大算力芯片，向左（定制）还是向右（通用）？](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247486727&idx=1&sn=aa30cf0bc28e8a9dceca4fbb1c720856&chksm=c12ecd42f65944549caba4353da71f41212e9776261438833668a28b579fd8d2d2b774e21b26&scene=21#wechat_redirect)
- 


[超异构计算，Intel的一盘大棋](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247486687&idx=1&sn=ad9af9d3d0477538ad36970de2f27383&chksm=c12ecc9af659458ca04efbe981449d5dcd58fee3abdaff02d531f397ba6225b26a0b9de8ee4e&scene=21#wechat_redirect)
- 


[超异构计算：大算力芯片的未来](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247486621&idx=1&sn=f34a3ae259b42ca14b9af2d43a5040fb&chksm=c12eccd8f65945ceb89bdb4de719fd7a17386db0ad5e8bdefe903466eaf6ffa0eae057c05dc4&scene=21#wechat_redirect)
- 


[DPU发展面临的困境和机遇](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247486416&idx=1&sn=fddfc02b776ea1e6704800cdeda07350&chksm=c12ecb95f6594283ce1442ade60e55f43d2df0a20c7fa8d5dbb8c0245a76131f09e7035da597&scene=21#wechat_redirect)
- 


[软硬件融合：超异构算力革命](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247486273&idx=1&sn=2abb06b7d0d68cc95448c015ff37795e&chksm=c12ecb04f659421255e415b3b8fc18c9883f7d8d97e075ffe1a8844a21684abef6ecf4b43ea4&scene=21#wechat_redirect)
- 


[是否存在足够“通用”的处理器，在性能快速提升的同时，还能够“包治百病”？](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247485929&idx=1&sn=196e79c0d5804928f4d562750d47c77b&chksm=c12ec9acf65940baa6a6758dcbc4012d3a2b40e9e1c50f623e4fadc5c4070797384c0f7256d7&scene=21#wechat_redirect)
- 


[Chiplet UCIe协议已定，CPU、GPU、DPU混战开启，未来路在何方？](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247485870&idx=1&sn=b92e1df5594c7a4399e382cc5982ed40&chksm=c12ec9ebf65940fd35fa4aba47ac65947d463f0b0682c10945440dcc1bc21b819cb85bf13e75&scene=21#wechat_redirect)
- 


[预见·第四代算力革命（三）：面向未来十年的新一代计算架构](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247485774&idx=1&sn=e6b3fad493f105f21fd0d8c907e2c2ab&chksm=c12ec90bf659401d59d05073135d58105aacc7d649b28a4414c59ac6bf23cf37ed970f7156f5&scene=21#wechat_redirect)
- 


[“DPU”非DPU](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247485656&idx=1&sn=345571fb94cba06798efb690afa42568&chksm=c12ec89df659418bb3a19246666576d4b4b9a5a19854467153ce74802ead2ff7db20a782f255&scene=21#wechat_redirect)
- 


[硬件定义软件？还是软件定义硬件？](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247485247&idx=1&sn=e4dbce939773432d53bf13b74629367f&chksm=c12ec77af6594e6c871ad13ce8bb06b11e902b0932df948c0b601e50154b66b2c80d62c0e15f&scene=21#wechat_redirect)
- 


[软硬件融合视角的SmartNIC、DPU和IPU定义](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247484885&idx=1&sn=cd48850c16e623b92b00749ecb14f783&chksm=c12ec590f6594c860bd78f67bf9dba86476f6877227450800ebe944a1f5b5f7d793fb2a72ff4&scene=21#wechat_redirect)
详情点击：[携手合作，走进软硬件融合时代](http://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247487640&idx=1&sn=e5f3c48ebe4bb894fb196af37630f330&chksm=c12ed0ddf65959cb2afc9b9296062044c5541b6de03aae89e8cfb1ce6fdb651263b6350b2de4&scene=21#wechat_redirect)

公众号回复“介绍PPT”下载相关幻灯片；
点击阅读原文或访问网址，观看软硬件融合视频：
https://aijishu.com/l/1110000000344055；
扫描二维码或公众号回复“加群”，加入交流群：

---
**Tags:** CST [[Chiplet]]
