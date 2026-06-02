---
title: "UB-Mesh：革新大规模语言模型训练的数据中心网络架构"
source: "https://mp.weixin.qq.com/s/Syo00m2VSlnnd47QEzViCg"
created: 2025-04-16
note_id: "1873439913899287168"
tags:
  - "AI链接笔记"
  - "UB - Mesh"
  - "大规模语言模型训练"
  - "数据中心网络架构"
  - "get-笔记"
  - "AI研究"
---

# UB-Mesh：革新大规模语言模型训练的数据中心网络架构

## 摘要

📈 **LLM训练挑战与需求** - 大规模语言模型（LLM）不断扩大规模，对计算能力和带宽需求剧增，给底层训练系统和基础设施带来巨大挑战。 - 下一代AI数据中心需满足大规模、高带宽、成本效益和高可用性四大要求。例如，Llama - 3预训练用1.6万个GPU需54天，领先公司已部署10万GPU的

## 正文

*   标题：UB-Mesh: a Hierarchically Localized nD-FullMesh Datacenter Network Architecture
    
*   作者：Heng Liao, Bingyang Liu, Xianping Chen, Zhigang Guo, Chuanning Cheng, Jianbing Wang, Xiangyu Chen, Peng Dong, Rui Meng, Wenjie Liu, Zhe Zhou, Ziyang Zhang, Yuhang Gai, Cunle Qian, Yi Xiong, Zhongwu Cheng, Jing Xia, Yuli Ma, Xi Chen, Wenhua Du, Shizhong Xiao, Chungang Li, Yong Qin, Liudong Xiong, Zhou Yu, Lv Chen, Lei Chen, Buyun Wang, Pei Wu, Junen Gao, Xiaochu Li, Jian He, Shizhuan Yan, Bill McColl
    
*   链接：https://arxiv.org/abs/2503.20377v1
    
*   时间：26 Mar 2025
    

摘要

随着大规模语言模型（LLM）的规模持续扩大，其所需的计算能力和带宽需求也在不断提升。为应对这一挑战，我们提出了UB-Mesh，一种新颖的AI数据中心网络架构，旨在提升可扩展性、性能、成本效益以及可用性。与传统数据中心提供对称的节点间带宽不同，UB-Mesh采用了一种分层局部化的n维全互连（nD-FullMesh）网络拓扑结构。该设计充分利用了LLM训练中的数据局部性，优先采用短距离直接互连，以最小化数据移动距离并减少交换机的使用。

尽管UB-Mesh的n维全互连拓扑在理论上具有多项优势，但其具体的架构设计、物理实现以及网络系统优化带来了新的挑战。为实现UB-Mesh的实际构建，我们首先设计了基于4维全互连拓扑的UB-Mesh-Pod架构。UB-Mesh-Pod通过一系列硬件组件实现，这些组件构成了基础构建模块，包括专门设计的NPU、CPU、低基数交换机（LRS）、高基数交换机（HRS）、网卡（NIC）等。这些组件通过一种新颖的统一总线（Unified Bus, UB）技术实现互连，该技术支持灵活的IO带宽分配和硬件资源池化。在网络系统优化方面，我们提出了名为全路径路由（All-Path-Routing, APR）的先进路由机制，以高效管理数据流量。这些优化措施结合拓扑感知的性能增强和诸如64+1备份设计的稳健可靠性机制，使得UB-Mesh相比传统的Clos架构实现了2.04倍的成本效益提升、7.2%的网络可用性提升，并在多种LLM训练任务中实现了95%以上的线性扩展能力。

1 引言

新兴的大规模语言模型（LLM）\[1, 4, 6, 8, 10, 18, 22, 26, 27, 31, 32\]正在改变AI产业和人类社会。根据规模定律（Scaling Laws）\[5, 13\]，LLM通过增加模型参数和训练数据量持续提升其理解、生成和推理能力。然而，这一趋势对底层训练系统和基础设施提出了日益严峻的挑战，迫使下一代AI数据中心满足以下要求：

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F598b65371f542b5dd1bca0fd1f0bba70?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=WzCOa8dBd1T%2F3Yn%2BVmurczUZle0%3D)

图1：传统Clos数据中心架构与UB-Mesh的比较

R1：大规模。随着模型规模和训练数据量的增加，需要越来越多的NPU（神经网络处理单元）或GPU在合理的时间内完成训练。例如，Llama-3的预训练使用1.6万个GPU需要54天\[8\]。领先公司最近的公告显示，已成功部署了拥有10万GPU的AI训练系统\[30\]。可扩展的基础设施对于支持LLM技术的持续发展至关重要。

R2：高带宽。在LLM训练系统中，AI计算节点（NPU/GPU）需要的互连带宽超过每节点3.2 Tbps\[12, 17\]，大约是当代数据中心中典型CPU节点互连带宽的10倍。因此，最先进的AI训练系统的总带宽比当前基于CPU的基础设施即服务（IaaS）系统高出10到100倍。

R3：成本效益。构建大规模AI数据中心需要巨额硬件投资，资本支出（CapEx）往往达到数十亿美元。为实现所需的10到100倍总互连带宽增长，若使用传统的对称Clos数据中心网络架构（见图1-(a)），互连成本也将增加10到100倍。优化网络基础设施为提升成本效益提供了重要机会。此外，降低运营成本（OpEx），包括能耗和维护费用，对于确保整体成本效益同样至关重要。

R4：高可用性。拥有10万计算节点和约100万个光模块的大型LLM训练集群面临显著的可用性挑战。当前统计数据显示，即使每条链路的平均故障间隔时间（MTBF）为5年，整个10万GPU的AI集群的原始MTBF仍下降至不到30分钟\[24\]。为此，网络架构设计不仅需提升硬件可靠性，还需融入容错机制，以应对互连、计算资源、控制系统和存储的故障。

同时实现这些目标极具挑战性，需要向先进的下一代数据中心网络架构设计转变。我们认为，设计下一代AI数据中心应以以下三个原则为核心：

P1：流量模式驱动的网络拓扑。与传统数据中心工作负载通常产生均匀且随机的流量不同，大规模语言模型（LLM）的训练流量具有确定性并表现出强烈的数据局部性。例如，张量并行（Tensor Parallelism）\[25\]操作所需的集合通信通常占总数据流量的50%以上，且通常发生在8-64个相邻NPU的集群内。相比之下，数据并行（Data Parallelism）产生的集合通信占总流量的不到2%，但通常需要长距离传输。因此，层次化、局部化的网络架构对于适配这些流量模式至关重要。

P2：拓扑感知的计算与通信。在分层局部化的数据中心网络中，有效运行LLM训练是另一重大挑战。如果训练任务未在计算资源上优化分布，或网络系统未得到充分优化，AI集群可能因流量拥塞或带宽利用不足而性能低下。为解决这一问题，并行策略选择、路由、集合通信、负载均衡等因素必须与网络拓扑精确对齐。

P3：容错自愈系统。LLM训练系统必须具备自愈能力以确保鲁棒性。链路故障时，路由系统应自动切换至备用路径；同样，若NPU发生故障，应有机制无缝激活备用NPU，以维持系统完整性和LLM训练的连续性。

为满足要求R1-R4并遵循原则P1-P3，我们提出了创新的UB-Mesh架构。如图1-(b)所示，UB-Mesh采用n维全互连（nD-FullMesh）网络拓扑，通过递归构建全互连拓扑——从板上相邻NPU间的1维连接开始，扩展到机架内相邻1维网格间的2维连接，再通过互连更广范围的相邻高维网格扩展至3维及以上。这种分层局部化的网络架构最小化传输跳数并优化每跳距离，优先采用直接互连而非间接长距离交换，从而减少对交换机和光模块的依赖，满足R1和R3。此外，它根据LLM训练的传输需求实现层次化带宽分配，为短距离通信提供高带宽，为长距离通信提供较低带宽，满足R2和R3并遵循P1。

遵循P2，我们深入研究了先进的网络和系统优化机制以增强UB-Mesh架构。具体而言，我们引入了全路径路由（All-Path Routing, APR）技术，以充分利用直接连接链路的带宽。APR结合源路由、结构化寻址与线性表查找以及无死锁流量控制机制，实现自适应路由、最小化转发开销并避免死锁。此外，我们加入了拓扑感知的快速故障恢复机制以提升可靠性。为进一步优化性能，我们提出了拓扑感知的集合通信和并行优化，以提升训练期间的带宽利用率。

为满足R4并遵循P3，UB-Mesh采用64+1高可用性设计：每个机架包含一个额外的备用NPU。当系统中NPU发生意外故障时，备用NPU被激活以恢复功能，确保LLM训练任务不间断继续。此外，路由系统通过一种新颖的直接通知技术在链路故障时实现快速恢复。

我们精心设计了UB-Mesh的硬件和系统堆栈，综合考虑了各种工程约束和权衡。具体实现中，UB-Mesh-Pod采用4维全互连拓扑，使UB-Mesh可无缝扩展至8000个NPU，形成支持下一代AI数据中心构建的高带宽域。为此，我们开发了一系列硬件组件作为基础构建模块，包括NPU、CPU、低基数交换机（LRS）、高基数交换机（HRS）、网卡（NIC）等。

与采用多种互连技术（如PCIe、NVLINK、IB和RoCE）的基线系统不同，UB-Mesh使用新颖的统一总线（Unified Bus, UB）技术实现所有组件互连。这种统一方法提升了IO资源分配的灵活性，其点对点通信能力支持高效的硬件资源池化，UB还为无缝跨层优化提供了机会。

全面评估表明，与非超订阅的Clos网络相比，UB-Mesh将高基数交换机使用量减少98%，光模块使用量减少93%，实现系统级成本效益提升2.04倍。在多个LLM训练任务中的实验还显示，与成本高昂的Clos网络相比，UB-Mesh的性能降幅仅在7%以内。这种低成本与高性能的结合不仅满足当前LLM训练需求，还使其能够有效应对未来的可扩展性挑战。

2 背景与动机

2.1 LLM训练中的“通信墙”

大规模语言模型（LLM）训练是有史以来规模最大、计算和通信需求最为密集的并行计算应用\[11, 18, 20–22, 25, 27, 32\]。遵循所谓的规模定律（Scaling Laws）\[3, 5, 13\]，LLM通过增加模型参数和训练数据量来提升性能。因此，LLM需要越来越多的AI加速器以在合理的时间内完成训练。例如，开源的Llama-3.1模型在1.6万个GPU上进行训练\[8\]，而下一代LLM模型已使用10万GPU进行训练\[24, 29\]。

标准的训练过程包括重复的训练迭代，每个迭代包含前向传播以计算损失、反向传播以确定梯度，以及优化器步骤以调整模型参数。为充分利用分布式计算能力，LLM训练通过多种并行策略将数据、模型和激活值分割到数万个NPU上。在每个迭代中，NPU之间频繁交换数据以分发输入数据、同步激活值和梯度等。随着训练系统规模的扩大，数据移动成为系统中成本最高的部分\[9, 19\]。若缺乏强大的NPU间通信能力，训练过程很容易受限于“通信墙”（Communication Wall）。

2.2 LLM训练中数据流量的局部性

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F027adfcf394ac1766cae29840aedced9?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ZSNICV1B4zMbbvnGjo0dje2ycQg%3D)

图2：LLM训练中的并行性

如图2所示，LLM训练通常涉及多种并行技术，以下逐一介绍：

张量并行（Tensor Parallelism, TP）：TP以行或列的方式分割模型层，并将子层放置在多个NPU上并行计算\[25\]。其主要涉及AllReduce操作以合并分布式的部分结果。

序列并行（Sequence Parallelism, SP）：SP（在某些论文中也称为上下文并行）通常用于将序列分割到多个NPU以实现并行处理。SP依赖RingAttention\[15\]技术，并可采用AllGather操作收集不同NPU的部分结果。

专家并行（Expert Parallelism, EP）：对于采用专家混合（Mix-of-Experts, MoE）技术的LLM模型，密集MLP层被MoE层替代，每个MoE层包含若干“专家”。执行时专家被稀疏激活。EP将专家分布在不同NPU上，输入标记通过All2All通信动态发送至目标专家。

流水线并行（Pipeline Parallelism, PP）：与TP分割每个模型层不同，PP将层分布到多个设备上，并以流水线方式执行前向和反向传播。PP涉及低开销的P2P通信以传输层间激活值，但需要高效的调度算法\[11, 16\]以最小化流水线中的空泡。

数据并行（Data Parallelism, DP）：DP在多个NPU上复制模型和优化器状态，每个副本并行处理一部分输入批次。训练过程中需通过AllReduce操作同步梯度。

表1：LLM训练中数据流量的分析

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3f21c89250499be3ef26ef6ed6e42ef6?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=adwn29th3mP6ViDyPWWwz%2Bsp5uA%3D)

这些并行技术共同将训练任务分布到数千个NPU上。需要注意的是，并非所有并行技术产生的数据流量均等。根据我们基于内部MoE-2T模型的分析（如表1详述），通信强度呈层次化并表现出强烈的局部性。具体而言，TP和SP约占总流量的97%，而其余并行技术通常产生不到2%的流量。其他模型架构可能表现出略有不同的数据流量分布，但同样具有较强的局部性\[28\]。因此，架构设计应优先采用层次化的网络带宽分配方式。

2.3 数据中心网络架构

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3136c2b8dd3f7e1144e85e7c0287af87?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=paW4tFRRIC8NtTKqVMhjlAdYZD4%3D)

图3：传统数据中心网络架构

设计大规模LLM训练集群涉及一个关键问题：如何将众多NPU资源组织成一个协调的分布式系统？这需要确定合适的数据中心网络架构。传统数据中心和超算系统探索了多种拓扑结构，但这些拓扑未必适用于大规模LLM训练。图3展示了一些常见拓扑：

Clos：传统数据中心通常采用Clos架构，通过两到三层交换机对称连接NPU/CPU，提供高性能并适应多种流量模式。然而，其高成本是一个缺点，主要源于对高性能交换机和光模块的广泛使用。

3D Torus：与依赖交换机互连的Clos不同，3D Torus直接连接相邻NPU。虽然降低了成本，但3D Torus的NPU间带宽较低，且难以适应复杂的通信模式，例如MoE模型中常见的All-to-All通信\[20\]。

Dragon-Fly：Dragon-Fly拓扑\[14\]将交换机组织为互连组，每组内交换机彼此直接相连，组间通过长距离电缆连接，数据包通过间接路由传输。该架构在传统数据中心和高性能计算（HPC）环境中降低了维度。Dragon-Fly比Clos成本更低，但因需满足完整的NPU-交换机带宽需求仍较昂贵，且其架构在LLM训练流量（特别是P2P和AllReduce场景）中表现不佳。

Fugaku Tofu：Fugaku Tofu\[2\]提出了一种独特的6D Torus拓扑用于HPC应用。然而，与3D Torus类似，其NPU间带宽较低，且难以适应复杂的通信模式。

综上所述，如何为大规模LLM训练设计一个高性能且成本效益高的数据中心网络架构仍是一个开放性问题。

3 UB-Mesh架构

为满足第1节中提出的要求R1-R4并遵循原则P1-P3，我们提出了UB-Mesh架构。UB-Mesh采用了一种新颖的n维全互连（nD-FullMesh）拓扑结构，最大限度地利用直接电线互连，从而减少对昂贵高带宽交换机和光模块的需求。接下来，我们将介绍一系列专为构建UB-Mesh设计的硬件模块。最后，我们将详细讨论UB-Mesh-Pod的架构设计，即UB-Mesh的具体4维全互连实现，同时充分考虑了若干工程约束和权衡。

3.1 nD-FullMesh拓扑

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9852ffa3fe62ec8228e8c6f482b35f23?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=He0P9E4ymcyXkggaRr7Cs154zkg%3D)

图4：UB-Mesh的n维全互连拓扑及可能的物理映射

如图4所示，UB-Mesh引入了一种新颖的n维全互连拓扑，强调跨所有网络层级的直接互连。该拓扑从相邻节点形成1维全互连开始，其中同一层级的每个节点与该层内其他所有节点相连。基于这一概念，相邻1维全互连的节点之间再进行直接互连，形成2维全互连。这一过程递归进行，相邻的2维全互连形成3维全互连，依此类推，最终根据需要扩展至n维全互连。这种灵活的虚拟拓扑可以无缝映射到各种物理NPU组织形式：单板上的1维全互连、机架内的2维全互连、机架行间的3维全互连、楼层机架组内的4维全互连，甚至跨越整栋建筑的5维全互连及更高维度。

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb1f4490b8754e7453467144fb8e35d04?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=y5sSf7TPskJyKH33C75ng%2BUpJhY%3D)

图5：高维拓扑与灵活的带宽分配

这种分层局部化的拓扑在构建下一代LLM训练数据中心时具有多项优势。首先，由于nD-FullMesh在每个网络维度上形成紧密耦合的直接连接域，并可提供逐层超订阅的带宽，它充分利用了LLM训练固有的数据局部性和从密集到稀疏的流量模式（见第2.2节）。此外，我们可以灵活调整每个维度的每节点带宽分配，以满足未来LLM训练任务的具体需求。例如，如图5-(a)所示，假设存在6维全互连拓扑，我们可以通过在NPU的IO模块中分配不同数量的互连链路来调整𝑋𝑌𝑍和𝛼𝛽𝛾维度的带宽，如图5-(b)所示。

其次，与需要大量交换的Clos架构不同，这种直接连接的拓扑在减少传输距离方面具有巨大潜力。结合数据放置和集合通信优化（见第5.2节），大多数传输（通常涉及TP或SP，如表1所示）可在0-2跳内完成，大幅降低数据移动开销。

表2：不同类型链路的使用估算

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F185dc5dabe73d04684a0bc40fa93fefb?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=kO%2B7WW96EO9G94Vkt3Fl7gwzCRg%3D)

第三，与Clos等其他流行拓扑相比，nD-FullMesh拓扑减轻了对高带宽交换机和长距离光互连的依赖。相反，它最大限度地利用短距离直接互连。例如，根据表2的估算，短距离无源电线占据了总电缆消耗的86.7%。这一设计显著降低了交换机和光模块的成本，同时提升了系统可靠性，因为电线和连接器比光模块更稳定。

最后，与不适合复杂集合通信操作（如All-to-All）的3D-Torus拓扑不同，全互连拓扑能够高效支持这些操作，具体将在第5节中讨论。

3.2 UB-Mesh的构建模块

所提出的nD-FullMesh拓扑在理论上具有多项优势，但其实践实现和系统性能的提升带来了新的挑战，需要全面考虑各种工程约束和权衡。为此，我们设计并制造了一系列硬件模块，作为UB-Mesh的基础构建块。这些模块通过一种名为统一总线（Unified Bus, UB）的新型互连机制实现连接。具体细节如下：

3.2.1 硬件模块

表3：UB-Mesh的主要构建模块

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb7149767077b5b37e53c66cbd57c3639?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=owU%2BYtgjKxTYlmxcF9ObWozkQ3g%3D)

表3列举了UB-Mesh的主要组件。其核心是作为AI计算单元的NPU。NPU配备两个UB IO控制器，总计提供x72条UB通道。负责执行主机程序的CPU也配备一个UB IO控制器，提供x32的UB IO。

尽管UB-Mesh优先采用直接互连，但交换能力对于满足特定需求仍不可或缺。例如，在图5中聚合𝑍和𝛼𝛽𝛾维度的NPU IO有助于实现高效的机架间互连。此外，我们期望CPU-NPU比例及其绑定关系能够灵活调整，以实现NPU和内存资源的高效池化，这可以通过交换实现。

为在UB-Mesh-Pod内提供成本效益高的交换能力，我们开发了轻量级低基数交换机（LRS）。其制造成本低，可高效聚合机架间IO带宽并支持CPU-NPU通信。

尽管UB-Mesh仅使用低基数交换机即可实现，但实际网络约束通常将其规模限制在一定范围内（UB-Mesh-Pod）。因此，UB-Mesh还包括高基数交换机（HRS），提供x512的UB IO容量以支持Pod级交换。UB-Mesh的详细架构设计和考虑将在第3.3节中介绍。

3.2.2 统一总线（UB）互连

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F6a67bd67642fa5054086b32f98ee6c3b?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=yXlmqNJRFrwnT7kYGVvEdHpHrxI%3D)

图6：统一总线互连与传统混合互连的对比

连接这些异构硬件模块需要特定的互连技术。如图6-(a)所示，传统的基于GPU的LLM系统通常采用多种互连方式，而UB-Mesh通过统一总线（UB）技术实现所有组件的互连，其优势包括：  

*   灵活的IO资源分配：UB互连与特定用例解耦，支持芯片内不同类型IO的灵活资源分配，如图5所示。NPU间带宽和CPU-NPU带宽也可根据具体需求灵活调整，因为它们使用相同的UB链路。
    
*   硬件资源池化：UB的点对点通信能力支持包括DDR DRAM、CPU、NPU和NIC在内的高效硬件资源池化。例如，在图6-(b)中，CPU和NPU通过UB互连实现池化，以提升资源利用率。
    
*   系统优化收益：统一互连消除了协议转换的需要，大幅降低开销并简化驱动程序、通信库和框架的设计与优化。
    

3.3 架构概览

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9ccd8426bdddfbb063a241df79e262df?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ZQL2sZICdj%2F9IKmoZ7KltO1TwwU%3D)

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F6bc8b23ccd2d86479e9a4d70e11f049b?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=BefUV96%2BDhCHWTxRKLVHdvWmHI8%3D)

图7：UB-Mesh的架构设计

通过组合表3中列出的硬件构建模块并通过统一总线（Unified Bus, UB）进行互连，我们提出了UB-Mesh的整体架构设计。如图7-(a)所示，我们按照所提出的nD-FullMesh拓扑实现了一个UB-Mesh-Pod。具体而言，在该架构中，我们在每个机架内创建了一个2D全互连拓扑，并将其扩展到机架之外的另一个2D全互连拓扑，从而形成一个4D全互连拓扑。我们选择不在这一代产品中将UB-Mesh扩展至5D全互连或更高维度，以在成本效益和灵活性之间实现工程平衡，在4D全互连之外仍采用Clos拓扑。以下为详细介绍：

3.3.1 在机架内实现2D全互连

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F2e97ff9f7d3918cc0591ea613a3eb292?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ULo78ng3rHvphq98dfUhehfT92c%3D)

图8：UB-Mesh机架的硬件实现

如图7-(b)所示，每个机架配置为2D全互连拓扑，集成了多个组件以确保高效通信和资源利用。机架的核心由八个NPU板组成，每个板包含八个NPU，如图8-(a)所示。这64个NPU在机架内互连，形成一个2D全互连网络，确保高NPU间带宽。需要注意的是，由于UB IO控制器也具备路由能力，每个NPU在此架构中既充当计算单元又充当路由器，支持间接路由。

除NPU外，机架还包括专用CPU板，如图8-(c)所示。与传统设置中CPU和NPU位于同一板不同，此处它们是分离的。CPU通过交换机连接到NPU，支持灵活的CPU/NPU比例调整，并实现CPU/NPU/DDR资源池化以提升资源利用率。

机架配备多个背板交换机，管理机架内和机架间的连接。这些交换机采用低基数设计（称为LRS），以降低成本，同时确保设备间的无阻塞通信。总体而言，这些背板交换机输出四个UB x256 IO。

3.3.2 64+1高可用性设计

正如第1节所述，在大规模AI数据中心中确保系统可用性是一个关键挑战。系统中单个NPU可能会发生意外故障。虽然软件系统可以检测这些故障并使用剩余健康NPU重启训练，但由于计算能力和系统带宽的减少，系统性能将受到显著影响。

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd0a58b54f52ae1b3d847d0295d72ef26?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=QWhSaBD%2F6YL4mbJrNShmx%2FhmGWc%3D)

图9：通过启用备用NPU实现容错

为提升系统可用性，我们引入了特殊的64+1设计：如图7-(b)和图8-(b)所示，系统包含64个常规NPU以及一个额外的备用NPU。该备用NPU通过LRS与64个常规NPU相连。当任何NPU发生故障时，备用NPU将被策略性地启用。如图9所示，当NPU-3发生故障时，管理系统激活备用NPU（图中节点B）以替换NPU-3。与NPU-3相关的原始直接连接链路将被重定向。例如，路径5-3被重定向为路径5-LRS-B。尽管此策略将原始直接连接变为单跳路由，略微增加了传输延迟，但相比简单屏蔽NPU-3并在剩余七个NPU上运行任务，其效果要优越得多。在机架内带宽为主要关注点的LLM训练场景中，增加的延迟对整体训练性能影响微乎其微。

3.3.3 在UB-Mesh-Pod中扩展至4D全互连

在机架内，我们将64个NPU组织为2D全互连拓扑。在机架之外，我们实现另一个2D全互连来组织机架，形成名为UB-Mesh-Pod的4D全互连架构。

如图7-(a)和(c)所示，一行中四个相邻机架被组织为紧密耦合的1D全互连，机架通过每个机架中的LRS端口直接互连。在每个机架列中，机架也直接相连，形成一个16机架的2D全互连拓扑。此配置中的每条链路代表一个UB x128 IO，如图8-(d)所示。我们沿两个维度连接四个相邻机架以构建机架间全互连，这是考虑到有源电线的覆盖范围得出的最佳点。由于每个机架有64个NPU，每个Pod有16个机架，一个4D全互连的UB-Mesh-Pod总共包含1024个NPU。

3.3.4 UB-Mesh-SuperPod及更高规模

基于1000规模的UB-Mesh-Pod，我们进一步构建了UB-Mesh-SuperPod，可容纳多个UB-Mesh-Pod。考虑到当前云场景中小规模或中规模LLM训练负载可能不会消耗整个SuperPod，我们选择在Pod级互连中采用对称的Clos拓扑，而非继续使用全互连设计。这种设计允许云管理者根据用户需求灵活划分SuperPod，并保证每个划分域内的全带宽。如图7-(c)所示，我们使用高基数Pod交换机（HRS）连接SuperPod中的每个机架，可扩展至8000个NPU。

最后，SuperPod中的机架还通过UB交换机（方案(a)）或位于CPU板上的NIC（方案(b)）连接到大规模数据中心网络（DCN）。DCN域通常支持大规模数据并行训练。DCN交换机采用Clos拓扑组织。DCN域可扩展至10万NPU或更多。

4 实现架构

在UB-Mesh-SuperPod中，4D全互连与Clos混合拓扑迫切需要高效的混合路由支持：除了通过LRS和HRS进行的基于交换机的路由外，NPU本身通过UB控制器也具备路由能力。UB-Mesh中大量路由器和层次化拓扑为路由系统引入了新的复杂性。我们认为，路由系统必须满足以下五个关键要求：  

*   支持混合拓扑：路由系统必须满足UB-Mesh的4D全互连与Clos混合拓扑所带来的需求。
    
*   高效转发：由于每个NPU同时也是路由器，且整个系统包含大量NPU，为节省NPU硬件资源，路由系统必须高效处理路由表查询和转发操作。
    
*   支持非最短路径：在nD全互连拓扑中，两个端点之间存在多个路径，距离各异。系统应支持使用非最短路径，以最大化网络带宽利用率。
    
*   快速故障恢复：为确保可靠性和可用性，路由系统必须快速从故障中恢复，减少对训练过程的影响。
    
*   无死锁：最后，整个网络系统必须在无死锁风险下运行，确保数据流畅通无阻。
    

表4：路由系统比较

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff63646102a430b006e48e51df6ba327f?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ZwF%2BSiqyO8kFC%2FkJjsmHu1pQYk4%3D)

然而，表4中列出的现有路由技术，如Clos、Torus和DragonFly拓扑上使用的长前缀匹配（LPM）、基于主机的路由和维度顺序路由（DOR），均无法完全满足我们的需求。因此，我们提出了全路径路由（All-Path-Routing, APR）技术和基于直接通知的快速故障恢复技术，以满足上述要求。

4.1 全路径路由（APR）

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F782a1b51cb3f9f77bd712a58be9bb351?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=9%2BjSis1luQXokwIcdDp9Bigo8ZI%3D)

图10：最短路径路由与全路径路由

UB-Mesh的全互连网络架构为任意两个NPU之间提供了多条路径。传统的路由策略，如最短路径优先（SPF）路由（见图10-(a)），往往无法充分利用网络带宽，且易受链路故障影响。为提升网络效率和鲁棒性，我们在UB-Mesh中提出了全路径路由（APR）机制。

如图10-(b)所示，APR利用源节点与目标节点之间的所有可用路径。这种灵活性允许动态切换路径，以应对故障或拥塞，从而提升网络鲁棒性。为高效实现这一目标，APR依赖以下三种底层机制：(1) 源路由（SR）机制实现自适应路由；(2) 结构化寻址与线性表查询技术，减少路由表查询和转发开销；(3) 拓扑感知无死锁流量控制，避免死锁。

4.1.1 源路由

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F8ea429101b7fd3c23ea248478a189b9b?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Ic%2FM8RzJcInx5uMhQ8Tw6JXGxAM%3D)

图11：源路由头部格式

为充分利用APR提供的路径，一种实用方法是采用源路由（SR）机制。如图11所示，在原始数据包头部添加一个8字节的SR头部，包含转发指令。每个路由器使用一个4位指针（ptr）指示12位位图字段中的位偏移。第𝑖位的值指定第𝑖跳的转发方式（即，位值为1表示该跳采用SR转发，0表示传统转发）。在SR转发的情况下，位图字段还用于定位六个指令字段之一，指示如何转发该数据包。SR信息高度压缩，因此开销较低。

4.1.2 结构化寻址与线性表查询

为减少每个NPU的UB IO控制器中的路由表查询和转发开销，APR路由系统利用UB-Mesh拓扑的结构，采用结构化寻址和线性表查询机制。具体而言，地址空间根据网络元素的物理位置（如Pod、机架和板）划分为多个段。由于同一段内的NPU共享相同前缀，仅需存储短段地址，NPU可通过相对于段地址的线性偏移进行寻址。此设计显著减少表空间，加速路由表生成和分发，提升收敛速度，并支持快速响应状态变化，例如故障恢复操作。

4.1.3 拓扑感知无死锁流量控制

鉴于UB-Mesh的nD全互连拓扑包含复杂的环结构，且APR机制支持多跳路由，在有限的虚拟通道（VL）资源下实现无死锁流量控制具有挑战性。为应对这一挑战，我们提出了TFC（拓扑感知无死锁流量控制）算法。该算法在仅使用2个VL资源的情况下，最小化VL资源使用，同时实现无死锁的全路径路由。

TFC算法通过通道依赖图（CDG）建模死锁，并将UB-Mesh拓扑划分为子图。在每个子图内，拓扑导向规则和VL约束被统一为单一集合。算法应用N维跨维度断环原则，将集合分解为单VL无环子集，随后采用同维度断环原则计算幂集元素的排列和笛卡尔积，生成所有路径组合和VL映射，确保无死锁运行。由于篇幅限制，详细说明在此省略。

4.2 基于直接通知的快速故障恢复

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd80510057cee1cd55c9c7276ee2656c6?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=GxjtDwUHvj0XbGXp0hrBNxHH9G4%3D)

图12：从逐跳通知到直接通知

当网络中发生链路故障时，传统路由系统通常采用逐跳通知方式。如图12左侧所示，当链路1-3发生故障时，该信息由节点1和3逐跳传播，通常耗时较长。在UB-Mesh中，由于每个节点具有确定的通信目标集，我们可以通过直接通知受影响的节点加速路由收敛。如图12右侧所示，当链路1-3发生故障时，根据预计算的路由关系，该信息直接发送至节点6。通过这种拓扑感知的直接通知方式，可大幅减少控制平面的开销。

5 性能最大化

尽管UB-Mesh的硬件架构设计与LLM训练的流量模式相匹配，但在这种层次化的AI集群上运行工作负载时，如果训练任务未能在计算资源上有效分布，可能会导致低利用率。此外，集合通信的性能对整体训练效率至关重要。为确保LLM训练期间的系统性能最优，我们引入了若干拓扑感知优化策略，以进一步提升系统性能。

5.1 拓扑感知集合通信

为优化UB-Mesh上的集合通信并充分利用层次化直接互连的带宽，我们提出了利用UB-Mesh全路径路由能力（见第4.1节）的拓扑感知集合通信算法。我们以All-Reduce和All-to-All为例阐述我们的概念：

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4fdb2e8f7d2538017ad060b9d8a2a2d7?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=CgVlh1NRvtZ%2BgaJXl1Jzbqxkvwc%3D)

图13：AllReduce的多环算法

All-Reduce：我们提出了一个多环（Multi-Ring）算法，以在UB-Mesh上高效实现All-Reduce。我们首先通过统一的抽象模型对网络拓扑进行建模，考虑节点数量、节点间连接、链路带宽和延迟等因素。接下来，我们将集合通信与路径映射相结合，采用逻辑多环算法，确保路径独占使用，避免流量冲突。如图13-(a)所示，原始路径表示默认映射。未包含在这些路径中的空闲链路通过APR机制被利用，以提升带宽。最后，如图13-(b)所示，我们优化了多路径上的流量分区，以缓解瓶颈并通过APR最大化借用带宽的收益。

All-to-All：在All-to-All通信场景中，我们考虑了两种代表性用例：

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7cebebe9fbeb5657753f32bd6d110598?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=L4PRiiudeSxY8f6SzGt435BqBKY%3D)

图14：多路径与层次化All-to-All

(1) 通用All-to-All：如图14-(a)所示，当UB-Mesh中的源节点（为简化起见，图中展示2D网格，提出的技术可扩展至更高维度）向不同目标节点发送不同数据时，我们采用多路径All2All优化。具体而言，每个元素（向量或张量）被分为两个分区，分别沿X-FullMesh和Y-FullMesh互连同时传输，并最多使用一跳转发到达目标。这种策略保证了UB-Mesh nD全互连架构中的高带宽利用率。

(2) 广播+归约（Broadcast + Reduce）：对于涉及标记分发和专家数据收集的All-to-All操作\[7\]，其语义等价于多个广播和归约操作的重叠。如图14-(b)和(c)所示，我们可采用层次化广播/归约以节省带宽使用，充分利用UB-Mesh的层次拓扑。

5.2 拓扑感知并行化

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc3bc42086a7ae9248dec4189c73bd86e?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=%2FxDB49wPJ8scNngu7CFxw6uvfko%3D)

图15：拓扑感知并行化

给定训练任务和系统，我们确定最优并行策略，以充分利用UB-Mesh的高带宽局部互连。我们采用拓扑感知并行化机制优化LLM训练的模型和数据分割。如图15所示，我们的方法包括：

步骤①：生成可行的并行配置并将其映射到UB-Mesh架构上。

步骤②：利用拓扑感知通信成本模型评估通信成本。

步骤③：迭代最小化通信开销以找到最优配置。

该机制有两个重要要求：(1) 构建适当的搜索空间以平衡效率和性能；(2) 确保成本模型尽可能准确。对于要求(1)，我们使用基于优先级的启发式方法剪枝搜索空间：涉及高通信量的TP和SP（或CP）优先分配到高带宽域，而用于梯度更新的PP和DP优先级最低。对于需要EP的MoE模型，我们强制SP\*DP为EP的整数倍。对于要求(2)，我们在UB-Mesh拓扑上准确建模APR和拓扑感知集合通信的行为，并使用内部高精度仿真基础设施校准模型。

6 评估

在本节中，我们探索了UB-Mesh的架构设计空间，并分析其相较于基线Clos架构的优势。为便于更详细的比较，我们将分析分为两个层级：机架内架构比较和机架间架构比较。

6.1 实验设置

表5：基准模型

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F11ce384777a073c7dbda9518bc7a58f0?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=5Igh%2Fh0J1eRc%2FuCkhRnNV48STRE%3D)

表5列出了基准工作负载：Llama-70B和GPT3-175B为密集模型，而GPT4-2T为采用MoE技术的稀疏模型\[20\]。需要注意的是，GPT4的架构尚未正式发布，我们采用了推测参数\[23\]。为评估系统在更大模型上的性能，我们还包括了Dense-1T和MoE-10T模型。为探索UB-Mesh的架构，我们构建了一个内部仿真基础设施，并与真实PoC硬件对齐，以评估集群规模的LLM训练性能。

6.2 机架内架构探索

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F61aeffce7d1c2cac61015f2b629dff1d?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=R5t8qsuvW7rZpBLEiE%2B1miZjS2I%3D)

图16：基线机架内架构

我们比较了不同的机架内网络架构，如图16所示：

(a) 2D-FM：UB-Mesh的架构。64个NPU通过电线直接互连，形成2D全互连网络拓扑（X-Fullmesh + Y-Fullmesh）。该设计成本低，采用48个LRS（见表3）聚合机架间带宽并实现CPU-NPU互连（为简化起见，图中省略了CPU）。

(b) 1D-FM-A：此替代架构保留1D X-Fullmesh，即每个板上的8个NPU仍直接互连。然而，跨板通信通过36个LRS实现。每个NPU有一个UB x16 IO连接到LRS，另一个UB x16 IO连接到四个高基数交换机（HRS）用于机架间通信。

(c) 1D-FM-B：此架构进一步用HRS替换LRS。每个背板中的四个LRS用于NPU到CPU通信。跨板NPU通信通过四个背板中的八个交换机实现。这些交换机还连接到机架间网络，为每个NPU提供UB x32 IO用于机架间通信。

(d) Clos：此架构不使用NPU间直接连接，而是将64个NPU的所有端口连接到72个LRS，形成对称的Clos拓扑。该架构提供最高灵活性，但需要大量交换资源。

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5679d6a72021c3c7a7ed700320fbc79d?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=waVyG1RGct0FHsGyVzRtsLxxKmo%3D)

图17：不同机架内拓扑的性能

性能比较：在图17中，我们固定机架间架构（2D-FM，见第6.3节），并比较不同机架内架构的训练吞吐量，相对于Clos基线。SuperPod规模为8000（128个机架），评估的序列长度范围为8000至1000万。我们计算了不同序列长度的平均性能。

如图17-(a)所示，与Clos架构相比，2D-FM架构实现了93.2%至95.9%的训练性能。1D-FM-A架构显示出较低的性能下降，对于Llama2-70B相比2D-FM提升了2.44%的性能。对于其他参数更多的模型，提升幅度小于1.6%。1D-FM-B架构由于更高的机架间带宽，相比2D-FM显示出略高的性能提升，超过3%，但提升幅度仍较小。

图17-(b)探索了不同序列长度下的性能，相对于Clos架构的基线场景（所有模型平均值）。对于8000至3.2万的序列长度，2D-FM架构实现了95.5%的性能，略低于1D-FM-A（98.1%）和1D-FM-B（99.2%）。对于6.4万至1000万的序列长度，2D-FM架构相比Clos架构实现了95.0%的性能。

可以看出，与Clos相比，2D-FM架构以远低于硬件成本提供了相似的训练性能（性能差距在7%以内），这将在第6.4节中进行评估。

6.3 机架间架构探索

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F326f708a36b9327b94664dbff7fe40e7?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Zg8ELZ2CqLNAJzWGZDSQ0%2FRZNrs%3D)

图18：机架间网络架构

在机架内2D-FM之外，UB-Mesh在UB-Mesh Pod内采用另一个2D-FM，形成4D-FM网络架构。如图18所示，我们比较了UB-Mesh的2D全互连机架间架构与基线Clos架构：

(a) 2D-FM：16个机架在水平和垂直方向直接互连，形成2D全互连直接连接。所有机架连接到HRS交换机，支持跨Pod互连。在UB-Mesh-Pod中，可支持三种路由策略：  

*   最短路径（Shortest）：基线路由策略，仅选择2D网格上的最短路径用于P2P通信。
    
*   绕行（Detour）：根据全路径路由机制，还使用其他路径以最大化带宽。
    
*   借用（Borrow）：由于所有机架也连接到交换机，我们允许机架“借用”交换机的带宽。
    

(b) Clos：所有机架连接到HRS交换机，无直接连接。此架构比2D-FM消耗更多交换机，但提供最高的All-to-All带宽和灵活性。

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F407ee2c9b10f6f968acf2bfa34896705?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=LCLw2sPl7n17WvqRzVMjHfD%2FcxU%3D)

图19：不同机架间互连的端到端性能比较

性能比较：如图19所示，我们比较了2D-FM（包括不同路由策略）和Clos架构的性能。可以看出，与理想的Clos架构相比，2D-FM与Clos之间的性能差距微乎其微，尤其是应用Detour和Borrow策略时。GPT3-175B对机架间通信性能不敏感，而在GPT4-2T上，采用最短路径路由的朴素2D-FM训练性能下降0.73%。采用Detour和Borrow路由策略后，性能差距缩小至仅0.46%。总体而言，2D-FM机架间互连表现出与昂贵的Clos架构几乎相同的性能。

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7da72d61cf957a798a08b725076c337f?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=gI3HuXZMWgLPBRo163iOmahC6Io%3D)

图20：机架间带宽探索

机架间带宽探索：图20-(b)比较了8000 SuperPod在不同机架间带宽条件下的吞吐性能。评估的机架间带宽为每NPU的x4、x8、x16和x32 UB IO。对于8000至3.2万的序列长度，最优机架间带宽为UB x16；而对于6.4万至1000万的序列长度，最优机架间带宽为UB x32。从UB x8增加到UB x16在8000-3.2万序列长度范围内的性能增益仅为0.44%，但从UB x16增加到UB x32在6.4万-1000万序列长度范围内的性能增益更为显著，达1.85%。在6.4万至1000万序列长度的场景中，部分TP（张量并行）和SP（序列并行）流量不可避免地穿越机架间链路。更高的机架间带宽显著减少了TP和SP的通信时间，在这些场景中带来更明显的性能提升。这些数据强调了将机架间带宽与不同模型场景的特定序列长度需求相匹配的重要性，特别是在减少大规模模型的TP和SP通信延迟方面。

UB-Mesh默认分配每NPU UB x16 IO用于机架间通信，以在成本和性能之间实现平衡。我们还可调整机架内/机架间带宽比例，以匹配特定LLM训练工作负载的需求。

6.4 成本效益比较

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd4967428a06b620002c45b5f6ad7c966?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=zOqqUthWdn0BQT%2BoE8ZH4JHj%2B0k%3D)

图21：CapEx比较

系统成本通常以总拥有成本（TCO）衡量，即TCO = CapEx + OpEx。考虑到相对于基线的训练性能，我们定义系统的成本效益如下：

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5cbfd35b3e05fe7e0f28d0cc90259398?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=YMUTLQ5Tz8iork6lee%2FpbzmogCg%3D)

我们使用内部数据估算CapEx成本，包括NPU、CPU、LRS、HRS、电缆和其他模块的成本，并比较不同架构。如图21所示，UB-Mesh的4D-FM+Clos架构相较于2D-FM+x16（表示每NPU UB x16 IO）Clos、1D-FM+x16 Clos和x64T Clos架构分别实现了1.18倍、1.26倍、1.65倍和2.46倍的CapEx降低。与基线Clos架构相比，UB-Mesh成功将系统中网络基础设施成本占比从67%降低至20%，这得益于节省了高性能交换机和长距离光缆/模块。根据我们的评估，与基线Clos架构相比，98%的高基数交换机和93%的光模块得以节省。

OpEx降低主要包括系统生命周期内的电费和维护成本。UB-Mesh相较于Clos减少了约35%的OpEx，这得益于其大幅减少了交换机和光模块的使用。根据我们云部门的AI系统估算，OpEx约占TCO的30%。最终，根据公式(1)，UB-Mesh实现了2.04倍更高的成本效益。

6.5 线性度评估

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F288fac946be48d262eb4604738dffd5e?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=5DC0YWzX7avRZvgBqqiRsNwp6Vc%3D)

图22：序列长度256K时的线性度分析

AI集群的线性度指的是集群性能随NPU数量增加的线性扩展程度。具体而言，我们通过以下公式测量线性度：

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ffd06def9bee69898fa1a0986eaaa1162?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Omxl7jB%2B7nUelASU3daoVk6ss7U%3D)

图22评估了UB-Mesh在不同集群规模下的线性度。基准规模（即图中的1×规模）因任务而异。具体而言，Llama2-70B使用128个NPU，GPT3-175B的基准规模为512，Dense-1T和GPT4-2T使用1000个NPU。

可以看出，UB-Mesh在所有任务的1×至32×规模下线性度超过100%，这是因为规模提升提供了更多高带宽域，并释放了搜索更优并行策略以提升MFU（模型浮点利用率）的潜力。GPT4-2T和Dense-1T模型在64×规模（涉及6.4万个NPU）下线性度有所下降，但仍高于95%。

6.6 网络可靠性分析

AI训练过程对硬件故障敏感。经典的基于时间的指标用于评估系统可靠性：

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F6c58e0eac9b906f3cccbec2114a8a194?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=GXQ6fTT5w0b13YeakK7XJAAE1t8%3D)

其中，MTBF表示平均故障间隔时间，MTTR表示平均修复时间。

表6：MTBF估算

![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd7f01650e7ee7f1c958b8a6aaafc4e5b?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=fc0%2BwJqTITfaZzrHWijvBfC0hIk%3D)

如表6估算，优先使用直接连接的电线（E-Cables）而非光纤和交换机，大幅降低了网络模块的年化故障率（AFR）。

然后，我们计算两种架构的MTBF![](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd8c073404d17c11e4f05271bf0b1b3a6?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=6C0mvznFaPzhnHW4unm%2F7lH2gnU%3D)：基线Clos在8000个NPU集群中为13.8小时，而UB-Mesh达到98.5小时，提升了7.14倍。最终，根据公式(3)（我们根据现有统计数据假设MTTR为75分钟），UB-Mesh的可用性为98.8%，显著优于Clos的91.6%（提升7.2%）。

为进一步提升可用性，我们还精心设计了内部网络监控工具，可在10分钟内快速识别和定位网络故障，并在3分钟内触发任务迁移，大幅减少MTTR。通过这种MTTR优化，根据我们的评估，UB-Mesh的可用性可进一步提升至99.78%。

总结：与基线Clos架构相比，UB-Mesh以微小的性能下降（7%以内）为代价实现了2.04倍更高的成本效益。由于大幅减少了交换机和光模块的使用，UB-Mesh将网络可用性提升了7.2%。UB-Mesh还在多个LLM训练任务上实现了95%以上的线性度。

7 讨论

集合通信协处理器

值得一提的是，在UB IO控制器中还配备了一个特殊的协处理器，称为集合通信单元（Collective Communication Unit, CCU），用于卸载集合通信任务。具体而言，CCU执行指令，主动从HBM读取或写入数据，启动NPU间传输，并利用片上SRAM缓冲区执行在线数据归约操作。这种设计消除了从应用程序内存缓冲区到通信缓冲区的冗余数据拷贝，有效缓解了HBM带宽的消耗，并通过基于检查位的细粒度同步机制维持确定的归约顺序。CCU还能与计算核心无缝协作，实现高效的计算与通信重叠。

支持大规模专家模型

除了密集模型和常规MoE模型外，我们注意到人们正在积极探索包含大规模专家的MoE模型\[6, 7\]。这种设计通常需要大规模、细粒度的All-to-All通信。UB-Mesh通过多路径和层次化的All-to-All优化（见第5.1节）以及基于UB的Load/Store数据传输，能够高效支持此类大规模专家模型。CCU还能有效卸载All-to-All操作，节省宝贵的计算核心使用，这与\[7\]中的预期一致。

8 结论

本文提出了UB-Mesh，一种为下一代大规模语言模型（LLM）训练设计的新型数据中心网络架构。UB-Mesh采用n维全互连（nD-FullMesh）网络拓扑，减少了交换机和光模块的使用，同时适配LLM工作负载的分层局部化流量模式。我们深入考虑了架构设计、物理实现和网络系统优化，并提出了多项技术以应对各种挑战。与传统的Clos网络相比，UB-Mesh在提供相似LLM训练性能的同时，实现了2.04倍的系统级成本效益提升和7.2%的可用性提升。此外，UB-Mesh在多项LLM训练任务上实现了95%以上的线性扩展能力。

\---【本文完】\---

近期受欢迎的文章：

更多交流，可加本人微信

（请附中文姓名/公司/关注领域）

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F8f7a791c63e984d6f49b8ef8d1cece47?Expires=1780072175&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=e9bKMU7anfaEiOTtOr3PrKnEj4A%3D)

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 12:29*

## Related Notes

- [[AgentEvolver vs AlphaEvolve：AI自我进化的两条核心路线对比 🧠]]
- [[AI编码代理的质的飞跃：v3.3透明化与v3.4连续性技术解析]]
- [[DARPA人工智能与自主系统项目深度研究报告：以“第三波AI”为核心的军事智能革命]]
