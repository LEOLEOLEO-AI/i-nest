# 细看hotchip2025 之 AI数据中心互联以及Parallelism范式发展

> 笔记本: 我的剪贴板  
> 创建时间: 2025-09-22  

---

原文链接: [https://mp.weixin.qq.com/s/51nqFOs6cdHWELg9lwW0sQ](https://mp.weixin.qq.com/s/51nqFOs6cdHWELg9lwW0sQ)


目录
1. AI数据中心的互联（interconnect)
    1.1  AI interconnects分层架构
        1.1.1 scale-up interconnect
        1.1.2 scale-out(backend) network
        1.1.3 front-end network and backend network
        1.1.4 Data Center Interconnect (DCI) 
    1.2 各种interconnect的物理介质
2. AI模型的Building Blocks以及各种Parallelism范式的提出
    2.1 AlexNet(2012) | The begining
    2.2 ResNet50(2015) |  Data Parallelism
    2.3 BERT(2018) |  Data Parallelism
    2.4 GPipe(2018) | Pipeline Parallelism
    2.5 Megatron LM (2019)  | Tensor Parallelism
        2.5.1 通过Megatron训练利用 DP+PP+TP 训练大模型的划分
        2.5.2 通过Megatron训练利用 DP+PP+TP 训练大模型的实例（MI300X）
    2.6 GShared (2020) - Experts Parallelism
本文部分内容参考自：hotchip2025《How AI Workloads Shape Hardware Architecture》
## 1.1  AI interconnects分层架构

下面这张图是对各种interconnect做了一个分类，好吧，图有点粗糙。主要分为scale-up/scale-out/front-side network，实际上如果跨多个data center，那么也会存在跨data center的interconnect。

下面我们基于参考文章[1]，对各种interconnect的划分及其定义进行细化。在该文章中，提出了interconnects分层架构，通过这个架构，可以清晰的理解interconnect的层次结构。
如下图所示，定义AI data centers的分层架构。

### 1.1.1 scale-up interconnect

scale-up指的是直接连接在GPU上的链路，例如NVLink，UALink，UB-network等。通过scale-up链路，所有互联的的XPUs在一个Scale-up域，例如在nvlink中，如果2个GPU在一个scale-up域，那么通过nvml获得nvlink 的cliqueue id是一样的。在同一个scale-up域中，其中一个XPUs可以在一个UVA空间中访问其他所有的XPUs。在下图中描述，scale-up 使用铜缆，但实际上在华为的Matrix346 scale-up网络使用的是UB-network。

一般一个tray的GPU数量少于10个XPU，例如NVL72一个tray包括了4个GPU；一个rack的XPU数量少于100个XPU，例如NVL72一个rack包括了72个GPU；一个row包括的XPU数量多于100XPU，例如Matrix386是一个row，包括了386个XPU。下图中Passive copper traces指的是通过背板铜缆链接的方式。

### 1.1.2 scale-out(backend) network

Scale out是指经过链接到NIC上的网络，能够支撑由上万（10万）颗XPUs组成的集群。scale-out也被称为backend网络。Scale out 网络通常采用标准的网络协议，比如 InfiniBand 或以太网，其设计目标是支持数据中心内部更大范围的通信。它往往由多层交换机构成：第一层交换机直接连接计算节点，而第二层、第三层交换机则用来实现更大范围的互联。

### 1.1.3 front-end network and backend network

back-end网络也称为scale-out网络，主要用于GPU节点间高速通信、分布式训练。front-end网络主要用于用户访问、数据进出、管理调度等。如下图对比了scale-out网络和front-end网络的范围。

### 1.1.4 Data Center Interconnect (DCI)

在 scale-out 网络之外，数据中心运营商会使用 高速光纤链路 来连接不同的数据中心站点，提供高带宽的数据传输。这类 长距离链路 可以跨越很长的距离，在许多方面与互联网的骨干网链路类似。这部分网络被称为数据中心互连（Data Center Interconnect, DCI）。跨数据中心的光纤资源通常更为有限，因此运营商必须尽可能提升每根光纤的传输容量。

## 1.2 各种interconnect的物理介质

在下表中罗列了各种互联的物理介质。对于短距离的链路，一般会选用铜介质（背板，或者线缆）作为第一优先级的传输方式。因为铜缆的经济性更好且耗能低。但由于物理特性的限制，铜介质在传输上有距离的限制，而且随着数据传输速率的增大，影响也会增大。虽然可以通过switch，延长通信的范围，但是会带来很大的开销（例如：延迟增大，功耗增大，服务器负责性增大），可能需要综合权衡。一般在较长距离传输选用光传输，例如scale-up网络，front-end网络。随着AI 数据中心越来越大，未来将会是光的世界。

# 2. AI模型的Building Blocks以及各种Parallelism范式的提出


## 2.1 AlexNet(2012) | The begining

AlexNet是Hinton等提出的。在训练AlexNet的时候，由于一张GTX580放不下完整的模型，所以他们使用了2张GTX580进行了训练，耗时5～6天。如下图所示，模型上下划分为2部分，分别放在2个GPU上，在某些层需要2卡进行通信交换数据。这里虽然没有明确提出Parallelism范式，但实际上已经有模型并行的思想在里面。

## 2.2 ResNet50(2015) |  Data Parallelism

ResNet (Residual Network) 是Kaiming He(google)等提出的。ResNet50是ResNet系列模型中的一个，50表示的层数是50层。在论文中，他们并没有说明训练的规模。但是从开源文档中，我们可以看到，他们使用了8个挂在PCIe上的GPU，通过数据并行的方式进行训练。 (we use a mini-batch of 256 images on 8 GPUs, that is, 32 images per GPU)

在Data Parallelism下，每张卡都有一份模型的拷贝，将训练数据划分到每张卡上，每张卡使用1/n份数据进行训练。在梯度更新的时候需要做一个alreduce的操作，获得所有梯度的更新。

## 2.3 BERT(2018) |  Data Parallelism

Jacob Devlin(google)等人提出BERT模型。他们使用了 Google TPU进行了训练，通过Data Parallelism的方式将数据划分到不同的TPU上。对于BERT_base模型，在16个 Google TPU上进行了pre_train，训练了4天；对于BERT_large模型，在64个TPU上进行了训练，同样训练了4天。

下图显示了TPUv2的物理结构，一个board包含了4个soc。

## 2.4 GPipe(2018) | Pipeline Parallelism

GPipe是由Yanping Huang（Google）等人提出。提供了一种pipeline parallelism的机制，如下图所示，将模型按照执行顺序划分为F0→F1→F2→F3 共4个stage，F_i的执行依赖于F_i-1的执行，F_i-1计算完后，会将本地的结果发送到负责F_i的机器，F_i接收到了数据后开始计算。如（b）中所示显示了网络计算的依赖关系。在(c)中，通过将mim-batch划分为更小的micro-batches，使得不同的加速器在同一时刻处理不同的micro-batch，如此可以将整个流程pipeline起来。只在相邻stage传递 activations 和 gradients，点对点通信，通信模式简单。

下图描述了4个Node pipeline的训练模型的场景，划分为16个pipeline stage。理论上流水线并行能接近线性加速（N 倍），但因为气泡、通信和同步开销，实际只能达到 0.x × N 倍的性能提升。

## 2.5 Megatron LM (2019)  | Tensor Parallelism

Megatron LM是由Mohammad等人（NVIDIA）提出。下面举了一个MLP（multi-layer perceptron)层的例子，说明Tensor Parallelism的执行流程。在(a)中，将A矩阵划分为 [A1, A2], 将B矩阵划分为[B1, B2]，表示将A和B划分到2个GPU上，然后通过2卡allreduce的操作，获得最终的结果f。如果模型参数较大，这里矩阵A和矩阵B也可以划分到更多的GPU上处理。

### 2.5.1 通过Megatron训练 - 利用 DP+PP+TP 训练大模型的划分

现在已经讲解了DP，PP，TP各种并行模式，下表对比了各种并行方式及其使用场景依赖等。

下面，我们利用DP+PP+TP来训练一个530B的模型。一个完整的模型占了280张GPU，8-way TP并行（1个node），跨35个node的PP并行。如果DP使用 8-way, 10-way, 12-way，分别占用了2240张GPU，2800张GPU，3360张GPU。

### 2.5.2 通过Megatron训练 - 利用 DP+PP+TP 训练大模型的实例（MI300X）

下图是一个MI300X系统，一个chasis有8张GPU，用于PP并行。一个rack有4个chassis，如果要实现35个node的PP，需要跨多个rack。

下图描述了一个完整的模型。使用了PP+TP，8-way TP使用一个chassis，PP使用了35个node，占用了9个rack。rack内的网络通过TOR（top of rack)交换机连接。rack与rack之间第二层交换机连接。如果使用12-way DP，需要复制12份的模型，每个完整的模型占用下图的一份硬件资源。共需要108个rack，3360个GPUs。


## 2.6 GShared (2020) - Experts Parallelism

GShared是由Dmitry Lepikhin（Google）等人提出。如下图所示，他们提出了一种EP的并行机制，FFN（表示不同的export）分布在不同的device上，通过alltoall combine dispatch获得不同FFN的信息。他们在2048块TPU v3上用4天的时间训练了一个超过600B大小的大模型。

如下图所示，相比normal transformer，MOE transformer由于在某个时刻，只有部分的GPU进行工作，耗能会更少一些。

参考：
[1] https://www.marvell.com/blogs/the-evolution-of-ai-interconnects.html
[2] https://www.aflhyperscale.com/wp-content/uploads/2024/12/AI-Data-Centers-Scaling-Up-and-Scaling-Out-White-Paper.pdf
[3] https://arxiv.org/pdf/1512.03385
[4] https://github.com/KaimingHe/deep-residual-networks
[5] https://arxiv.org/pdf/1810.04805
[6] https://arxiv.org/pdf/1811.06965
[7] https://arxiv.org/pdf/2006.16668


END


更多交流，可加本人微信
（请附中文姓名/公司/关注领域）

---
**Tags:** [[NaaS]]
