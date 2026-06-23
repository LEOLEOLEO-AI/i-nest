---
title: "DeepSeek：爆火全球的中国AI大模型及其背后的技术与影响"
source: "https://mp.weixin.qq.com/s/KwfY6xpKSx5Zpu4L8MR4jw"
created: 2025-02-03
note_id: "1866762694674230760"
tags:
  - "AI链接笔记"
  - "AI大模型"
  - "技术架构"
  - "get-笔记"
  - "学术论文"
---

# DeepSeek：爆火全球的中国AI大模型及其背后的技术与影响

## 摘要

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Ff160a8c53eb76ff65c63cb2bc7842fb1.jpeg?Expires=1780073841&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9

## 正文

过去两周，DeepSeek已经成为了全球的热点。尤其是在西方世界，这个来自于中国的生成式人工智能系统引发了广泛讨论。

在发布的前18天内，DeepSeek便实现了惊人的1600万次下载，这一数字几乎是竞争对手OpenAI的ChatGPT在同期下载量的两倍，充分展示了其强大的市场吸引力和用户基础。

据市场分析公司Appfigures的权威数据，DeepSeek的应用程序于1月26日首次登顶苹果App Store，并自此持续保持其全球领先的霸主地位。数据统计显示，自今年初发布以来，迅速攀升至140个国家的苹果App Store下载排行榜首位，并在美国的Android Play Store中同样占据榜首位置。

作为一个中国的AI大模型，DeepSeek能够获得这个关注度，除了其出色的性能表现以外，其低训练成本也是其吸引全球目光的关键。在今天的文章中，我们来看一下藏在DeepSeek背后的芯片和系统。

**DeepSeek的架构自述**

早在2024年8月，8 月，DeepSeek团队发表了一篇论文，描述了它创建的一种新型负载均衡器，用于将其混合专家 (MoE：mixture of experts) 基础模型的元素相互连接。

DeepSeek在文章中表示，对于混合专家 (MoE) 模型，专家负载（ expert load）不均衡将导致路由崩溃（routing collapse）或计算开销（ computational overhead）增加。现有方法通常采用辅助损失（ auxiliary loss ）来促进负载平衡，但较大的辅助损失会在训练中引入不可忽略的干扰梯度（interference gradients），从而损害模型性能。

为了在训练过程中控制负载平衡但不产生不良梯度（undesired gradients ），DeepSeek团队提出了无损平衡（Loss-Free Balancing），其特点是无辅助损失的（auxiliary-loss-free）负载平衡策略。

具体而言，在进行 top-K 路由决策（routing decision）之前，无损平衡将首先对每个专家的路由分数（routing scores）应用专家偏见（expert-wise bias ）。通过根据每个专家的近期负载动态更新其偏见，无损平衡可以始终保持专家负载的均衡分布。

此外，由于无损平衡不会产生任何干扰梯度，它还提升了从 MoE 训练中获得的模型性能的上限。DeepSeek团队还在多达 3B 个参数、在多达 200B 个 token 上训练的 MoE 模型上验证了无损平衡的性能。实验结果表明，与传统的辅助丢包控制负载均衡策略相比，无损平衡策略既实现了更好的性能，也实现了更好的负载均衡。

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fb42200304ced6397842c3c6f8f34e4ad.png?Expires=1780073851&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=wCJgChDsCFonXeQnxg4mYflD%2FOY%3D)

_图 1：无损平衡根据每个训练步骤中的“偏见门控分数”（biased gating score）选择专家，并在每个训练步骤之后更新此专家偏见。_

在2024年年底发布的报告《DeepSeek-V3 Technical Report》中，DeepSeek团队对其DeepSeek-V3模型的技术架构进行了深入解读，这为我们了解这家公司的技术有了更多参考。

他们在报告中直言，出于前瞻性的考虑，公司始终追求模型性能强、成本低。因此，在架构方面，DeepSeek-V3 仍然采用多头潜在注意力（MLA：Multi-head Latent Attention）  进行高效推理和 DeepSeekMoE 以实现经济高效的训练。而为了实现高效训练，DeepSeek团队的解决方案支持 FP8 混合精度训练，并对训练框架进行了全面优化。在他们看来，低精度训练已成为高效训练的一种有前途的解决方案，其发展与硬件能力的进步密切相关。

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fcb83e984d115e97df037cbdc563056b4.png?Expires=1780073851&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=fa3MAWI6UGQVwF%2BvhHWGFG1Lqck%3D)

_图2：采用 FP8 数据格式的整体混合精度框架。为了清楚起见，仅说明了线性算子。_

通过对FP8计算和存储的支持，DeepSeek团队实现了加速训练和减少GPU内存使用。在训练框架方面，他们设计了DualPipe算法来实现高效的流水线并行，该算法具有更少的流水线气泡，并通过计算-通信重叠（overlap）隐藏了训练过程中的大部分通信。

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2F78ef7d139cdd355e4544fdeff80d500e.png?Expires=1780073851&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=NYtBVqaETsjJqj1BgASC2UJShx0%3D)

_图 3：DeepSeek-V3 基本架构图。继 DeepSeek-V2 之后，该公司采用 MLA 和 DeepSeekMoE 进行高效推理和经济训练。_

DeepSeek团队表示，这种重叠确保了随着模型的进一步扩大，只要保持恒定的计算与通信比率，公司仍然可以跨节点使用细粒度的专家（fine-grained experts），同时实现接近于零的全对全通信开销（all-to-all communication overhead）。

此外，DeepSeek团队还开发了高效的跨节点全对全通信内核，以充分利用InfiniBand（IB）和NVLink带宽。公司还对内存占用进行了精心优化，使得无需使用昂贵的张量并行即可训练DeepSeek-V3。

在将这些努力结合起来，DeepSeek团队实现了很高的训练效率。

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Faa69385097e96ab5c158746e40892baf.png?Expires=1780073851&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=VOgCTga6FZGkZuzqVHVGgfB07aM%3D)

_表 1：DeepSeek-V3 的训练成本，假设 H800 的租赁价格为每 GPU 小时 2 美元。_

根据DeepSeek团队在论文中强调，通过优化算法、框架和硬件的协同设计实现的。在预训练阶段，每万亿个 token 上训练 DeepSeek-V3 只需要 180K H800 GPU 小时，也就是说，在其拥有 2048 个 H800 GPU 的集群上只需要 3.7 天。因此，公司的预训练阶段在不到两个月的时间内完成，花费了 2664K GPU 小时。加上上下文长度扩展的 119K GPU 小时和后训练的 5K GPU 小时，DeepSeek-V3 完整训练仅花费 278.8 万 GPU 小时。

假设 H800 GPU 的租赁价格为每小时 2 美元，则代表着其总训练成本仅为 557.6 万美元DeepSeek团队还特意强调，上述成本仅包括 DeepSeek-V3 的官方训练，不包括与架构、算法或数据的先前研究和消融实验相关的成本。作为对比，OpenAI 老板 Sam Altman 表示，训练 GPT-4 需要超过 1 亿美元。

在1 月 20 日，DeepSeek 推出了 DeepSeek-R1 模型，该模型增加了两个强化学习阶段和两个监督微调阶段，以增强模型的推理能力。DeepSeek AI 对 R1 模型的收费比基础 V3 模型高出 6.5 倍。随后，DeepSeek发布了Janus-Pro，这是其多模态模型 Janus 的更新版本。新模型改进了训练策略、数据扩展和模型大小，增强了多模态理解和文本到图像的生成。

至此，DeepSeek火爆全球。

**躲在DeepSeek背后的芯片**

在DeepSeek横空出世之后，一些围绕着其系统和技术研究框架的讨论，也遍布全网，具体到硬件方面。因为其极低的成本，这引致了整个AI芯片市场的震荡，早几天英伟达的大跌，正是这个担忧的最直接的反映。

如上所述，DeepSeek 表示，用于训练 V3 模型的集群只有 256 个服务器节点，每个节点有 8 个 H800 GPU 加速器，总共有 2,048 个 GPU。据nextplatform的分析师推测，这些GPU卡是 英伟达H800 卡的 H800 SXM5 版本，其 FP64 浮点性能上限为 1 万亿次浮点运算，其他方面与世界上大多数公司可以购买的 80 GB 版本的 H100 卡相同。

其中，节点内的八个 GPU 与 NVSwitch 互连，以在这些 GPU 内存之间创建共享内存域，并且节点具有多个 InfiniBand 卡（可能每个 GPU 一个）以创建到集群中其他节点的高带宽链接。

具体到H800，这是当初英伟达因应美国的出口限制需求推出的GPU。当时的美国GPU出口禁令规定主要限制了算力和带宽两个方面。其中，算力上限为4800 TOPS，带宽上限为600 GB/s。A800和H800的算力与原版相当，但带宽有所降低。

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fffc4f363dbd66c1214364553d98e0622.png?Expires=1780073851&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vLA7%2BHPRa4o5duzDbGGDXo9Mz8c%3D)

_图4：H800的细节_

如上所述，DeepSeek在训练中使用的是H800 SXM版本。据了解，所谓SXM 架构，是一种高带宽插座式解决方案，用于将 NVIDIA Tensor Core 加速器连接到其专有的 DGX 和 HGX 系统。对于每一代 NVIDIA Tensor Core GPU，DGX 系统 HGX 板都配有 SXM 插座类型，为其匹配的 GPU 子卡实现了高带宽、电力输送等功能。

资料显示，专门的 HGX 系统板通过 NVLink 将 8 个 GPU 互连起来，实现了 GPU 之间的高带宽。NVLink 的功能使 GPU 之间的数据流动速度极快，使它们能够像单个 GPU 野兽一样运行，无需通过 PCIe 或需要与 CPU 通信来交换数据。NVIDIA DGX H800 连接了 8 个 SXM5 H800，通过 4 个 NVLink 交换芯片，每个 GPU的带宽为 400 GB/s，总双向带宽超过 3.2 TB/s。每个 H800 SXM GPU 也通过 PCI Express 连接到 CPU，因此 8 个 GPU 中的任何一个计算的数据都可以转发回 CPU。

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fc523e1195781d9719efa76f8c8866ae3.png?Expires=1780073851&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=XVK3HP0nrNqO2xJk2eyuH7AhXoI%3D)

_图5：基本的SGX/HGX to CPU框架图_

过去几年里，大型企业对英伟达DGX热度大增，这是因为SXM GPU 更适合规模化部署。如上所说，八 个 H800 GPU 通过 NVLink 和 NVSwitch 互连技术完全互连。而在 DGX 和 HGX 中，8 个 SXM GPU 的连接方式与 PCIe 不同；每个 GPU 与 4 个 NVLink Switch 芯片相连，基本上使所有的 GPU 作为一个大 GPU 运行。这种可扩展性可以通过英伟达 NVLink Switch 系统进一步扩展，以部署和连接 256 个 DGX H800，创建一个 GPU 加速的 AI 工厂。

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fed97655aaf4396ec9d66fed5a02045ca.png?Expires=1780073851&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=gf1THZdM71qCierc5H5%2BQ9lBhHU%3D)

图6：基本的8 PCIe GPU to CPU框架图

**外国分析师眼里的DeepSeeK**

基于这些GPU和系统，搞出这个成就，西方不少分析人士一面倒抨击Deepseek团队，但nextplatform的分析师表示，如果你仔细阅读这篇 53 页的论文，就会发现 DeepSeek 已经采取了各种巧妙的优化和方法来制作 V3 模型，他们也确实相信，这确实减少了效率低下的问题，并提高了 DeepSeek 在硬件上的训练和推理性能。

他们认为， DeepSeek团队训练 V3 基础模型所采用方法的关键创新是使用 Hopper GPU 上的 132 个流式多处理器 (SM) 中的 20 个，作为数据的通信加速器和调度器，因为训练运行会仔细检查token并从参数深度集生成模型的权重，因此数据会在集群中传递。据nextplatform推测，正如 V3 论文所述，这种“计算和通信之间的重叠可以隐藏计算过程中的通信延迟”，使用 SM 在不在同一节点的 GPU 之间创建实际上是 L3 缓存控制器和数据聚合器的东西。

按照nextplatform对其论文的分享，DeepSeek 创建了自己的 GPU 虚拟 DPU，用于执行与 GPU 集群中的全对全通信相关的各种类似 SHARP 的处理。

如上文所述，DeepSeek团队设计了 DualPipe 算法以实现高效的流水线并行。对此，nextplatform指出，如果 DeepSeek 可以将这 2,048 个 GPU 上的计算效率提高到接近 100%，那么集群将开始认为它有 8,192 个 GPU（当然缺少一些 SM）运行效率不高，因为它们没有 DualPipe。作为对比，OpenAI 的 GPT-4 基础模型是在 8,000 个 Nvidia 的“Ampere”A100 GPU 上训练的，相当于 4,000 个 H100（差不多）。

此外，包括辅助无损负载平衡、 FP8 低精度处理、将张量核心中中间结果的高精度矩阵数学运算提升到 CUDA 核心上的矢量单元以保持更高精度的表象、在反向传播期间重新计算所有 RMSNorm 操作和重新计算所有 MLA 向上投影等也都是DeepSeek的创新点之一。

知名半导体分析机构SemiAnalysis的Dylan Patel虽然对DeepSeek团队所披露的成本有质疑。但他们也承认DeepSeek有过人之处。

SemiAnalysis表示，DeepSeek-R1 能够取得与 OpenAI-o1 相当的成果，而 o1 在 9 月份才发布。DeepSeek 为何能如此迅速地赶上？这主要是因为推理已经成为了是一种新的范式，与以前相比，现在推理的迭代速度更快，计算量更小，却能获得有意义的收益。作为对比，以前的模式依赖于预训练，而预训练的成本越来越高，也很难实现稳健的收益。

他们指出，新范式侧重于通过合成数据生成和现有模型后训练中的 RL 来实现推理能力，从而以更低的价格获得更快的收益。较低的准入门槛加上简单的优化，意味着 DeepSeek 能够比以往更快地复制 o1 方法。

“R1 是一个非常优秀的模型，我们对此并无异议，而且这么快就赶上了推理边缘，客观上令人印象深刻。”SemiAnalysis强调。他们总结说：

一方面，DeepSeek V3 以前所未有的规模采用了多token预测（MTP：Multi-Token Prediction）技术，这些附加的注意力模块（attention modules）可以预测下几个token，而不是单个token。这提高了模型在训练过程中的性能，并可在推理过程中舍弃。这是一个算法创新的例子，它以较低的计算量提高了性能。还有一些额外的考虑因素，比如在训练中提高 FP8 的准确性；

另一方面，DeepSeek v3 也是专家模型（experts model,）的混合体，它是由许多专门从事不同领域的其他小型模型组成的大型模型。混合专家模型面临的一个难题是，如何确定将哪个token交给哪个子模型或 "专家"。DeepSeek 实施了一个 "门控网络"（gating network），以不影响模型性能的平衡方式将token路由到合适的专家。这意味着路由选择非常高效，相对于模型的整体规模，每个token在训练过程中只需改变少量参数。这不仅提高了训练效率，还降低了推理成本；

再者，就 R1 而言，有了强大的基础模型（v3），它将受益匪浅。部分原因在于强化学习（RL）。

强化学习有两个重点：格式化（确保提供连贯的输出）以及有用性和无害性（确保模型有

用）。在合成数据集上对模型进行微调时，推理能力出现了；

SemiAnalysis重申，MLA 是 DeepSeek 大幅降低推理成本的关键创新技术。原因在于，与标准注意力（standard attention）相比，MLA将每次查询所需的KV缓存量减少了约93.3%。KV 缓存是转换器模型中的一种内存机制，用于存储代表对话上下文的数据，从而减少不必要的计算。

**对英伟达芯片的潜在影响**

在文章开头我们就提到，DeepSeek爆火以后，英伟达用暴跌来回应。因为如果美国大型科技公司开始向 DeepSeek 学习，选择更便宜的人工智能解决方案，这可能会给 Nvidia 带来压力。

随后，Nvidia 对 DeepSeek 的进展给予了积极评价。该公司在一份声明中表示，DeepSeek 的进展很好地展示了 AI 模型的新操作方式。该公司表示，向用户提供此类 AI 模型需要大量 Nvidia 芯片。

但著名投资人、方舟投资CEO“木头姐”凯西·伍德在采访中表示，DeepSeek证明了在AI领域成功并不需要那么多钱，并且加速了成本崩溃。

Counterpoint Research 人工智能首席分析师孙伟也表示，Nvidia 的抛售反映了人们对人工智能发展的看法转变。她进一步指出：“DeepSeek 的成功挑战了人们认为更大的模型和更强大的计算能力能够带来更好性能的信念，对 Nvidia 由 GPU 驱动的增长战略构成了威胁。”

SemiAnalysis强调，算法改进的速度太快了，这对 Nvidia 和 GPU 来说也是不利的。

美媒《财富》更是预警道，DeepSeek 正在威胁英伟达的 AI 主导地位。

如前文所说，DeepSeek 已采用性能更低、价格更便宜的芯片打造了其最新型号，这也给 Nvidia 带来了压力，一些人担心其他大型科技公司可能会减少对 Nvidia 更先进产品的需求。

AvaTrade 首席市场分析师凯特·利曼 (Kate Leaman) 向《财富》杂志表示：“投资者担心 DeepSeek 与性能较弱的 AI 芯片配合使用的能力可能会损害英伟达在 AI 硬件领域的主导地位，尤其是考虑到其估值严重依赖于 AI 需求。”

值得一提的是，根据tomshardware的报道，DeepSeek 的 AI 突破绕过了英伟达的CUDA不成盒，而是使用了类似汇编的 PTX 编程，这从某种程度上加大了大家对英伟达的担忧。

据介绍，Nvidia 的 PTX（Parallel Thread Execution：并行线程执行）是 Nvidia 为其 GPU 设计的中间指令集架构。PTX 位于高级 GPU 编程语言（如 CUDA C/C++ 或其他语言前端）和低级机器代码（流式汇编或 SASS）之间。PTX 是一种接近金属的 ISA，它将 GPU 公开为数据并行计算设备，因此允许细粒度优化，例如寄存器分配和线程/warp 级别调整，这是 CUDA C/C++ 和其他语言无法实现的。一旦 PTX 进入 SASS，它就会针对特定一代的 Nvidia GPU 进行优化。

在训练 V3 模型时，DeepSeek 重新配置了 Nvidia 的 H800 GPU：在 132 个流式多处理器中，它分配了 20 个用于服务器到服务器通信，可能用于压缩和解压缩数据，以克服处理器的连接限制并加快交易速度。为了最大限度地提高性能，DeepSeek 还实施了高级管道算法，可能是通过进行超精细的线程/warp 级别调整来实现的。

报道指出，这些修改远远超出了标准 CUDA 级开发的范围，但维护起来却非常困难。

不过，晨星策略师布莱恩·科莱洛 (Brian Colello) 直言，DeepSeek 的进入无疑给整个人工智能生态系统增加了不确定性，但这并没有改变这一运动背后的压倒性势头。他在一份报告中写道：“我们认为人工智能 GPU 的需求仍然超过供应。因此，尽管更轻薄的机型可能能够以相同数量的芯片实现更大的发展，但我们仍然认为科技公司将继续购买所有他们能买到的 GPU，作为这场人工智能‘淘金热’的一部分。”

英特尔前首席执行官帕特·基辛格 (Pat Gelsinger) 等行业资深人士也认为，像人工智能这样的应用程序可以利用它们能够访问的所有计算能力。至于 DeepSeek 的突破，基辛格认为这是一种将人工智能添加到大众市场中大量廉价设备中的方法。

SemiAnalysis在其报告中透露，自DeepSeek V3 和 R1 发布以来，H100 的 AWS GPU 价格在许多地区都有所上涨。类似的 H200 也更难找到。“V3 推出后，H100 的价格暴涨，因为 GPU 的货币化率开始大大提高。以更低的价格获得更多的智能意味着更多的需求。这与前几个月低迷的 H100 现货价格相比发生了重大转变。”SemiAnalysis说，

所以，大家认为，DeepSeek将如何发展？英伟达芯片，还能继续独霸天下吗？

**参考链接**

https://arxiv.org/html/2408.15664v1

https://arxiv.org/html/2412.19437v1

https://www.nextplatform.com/2025/01/27/how-did-deepseek-train-its-ai-model-on-a-lot-less-and-crippled-hardware/

https://www.lthpc.com/cms/jishufenxiang/71.html

https://semianalysis.com/2025/01/31/deepseek-debates/

https://finance.yahoo.com/news/chinese-ai-startup-deepseek-threatening-153810959.html

https://www.tomshardware.com/tech-industry/artificial-intelligence/deepseeks-ai-breakthrough-bypasses-industry-standard-cuda-uses-assembly-like-ptx-programming-instead

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 12:57*

## Related Notes

- [[AutoResearchClaw：全自动端到端AI科研智能体深度解析]]
- [[DeepSeek：引领全球AI创新的新力量]]
- [[智能荧光粉的神经形态行为实现全光物理储层计算]]
