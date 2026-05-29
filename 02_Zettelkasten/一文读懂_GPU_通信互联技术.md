# 一文读懂 GPU 通信互联技术

> 笔记本: 我的剪贴板  
> 创建时间: 2024-03-05  

---

在之前的文章中，我们详细介绍过**PCIe****、****RDMA****、****NVlink****、****CXL**等互联技术。今天我们就通过这篇文章来详细的介绍下GPU通信互联技术。  
**为什么需要GPU互联技术？**  
我们都知道，在GPU未出现前，CPU一直是计算机中的绝对核心，甚至连存储、内存、网络等子系统的能力都是CPU说了算。  
比如，一个CPU能够支持多大的内存，CPU都是有严格要求的。甚至同样一颗CPU，只是支持不同的内存，都能卖两个价格。  
**这也导致了Intel的"独断专行"，其它人想对CPU做点"手脚"那是被限制的死死的**，可以说Intel真正做到了"此路是我开，此树是我栽，要想此路过，留下买路财"，这直接导致了Intel在产品创新方面一直"挤牙膏"。  
但人算不如天算，没想到大数据分析、AI、视觉渲染、基因分析以及EDR仿真等需求的突然爆发，给了NVIDIA的GPU带了巨大增长空间。  
   
GPU的快速增长超出了所有人的预料，它几乎彻底颠覆了CPU在计算机系统中的地位，**而传统的根据CPU为核心设计的互联通信方式在GPU高速增长的情况下开始慢慢成为了阻碍，原有的通信技术已经成为效率阻碍。**  
比如，传统方式如果想把数据从存储系统转运到GPU显存中，由于历史原因此过程受CPU管理。随着计算负载从较慢的CPU转移到较快的GPU后，I/O逐渐成为系统的性能瓶颈。  
面对这种情况，那么GPU就要在原有的计算机里"开路"了。  
为了更好地让大家理解GPU互联技术，本文按照GPU的使用模式分为两种方式来讲解，分为**单机多卡GPU互联技术**和**多机多卡GPU通信技术****。**  
不多说了，我们马上开始。  
**单机多卡GPU通信技术**  
谈到GPU"开路"的通信技术，我们就不得不聊到GPUDirect这项技术。  
**1、GPUDirect**  
GPUDirect是NVIDIA开发的一项技术，可实现GPU与其他设备（例如网络接口卡 (NIC) 和存储设备）之间的直接通信和数据传输，而不涉及CPU。  
使用GPUDirect，网络适配器和存储驱动器可以直接读写GPU内存，减少不必要的内存消耗，减少CPU开销并降低延迟，从而显著提高性能。  
  
发展到今天，**GPUDirect技术发展经历了四个阶段：**  
2010 年，GPU支持与网卡，存储等设备共享内存，即GPUDirect Shared Memory；  
2011 年，NVIDIA推出GPUDirect P2P（Peer-to-Peer），支持同一PCIe 总线上的GPU之间的内存访问 ；  
2012 年底，GPU Direct RDMA 完美地解决了计算集群节点间GPU卡PCIe 总线的通信问题。该技术将在多机的GPU通信中详细说明。  
如今，GPUDirect 技术已经逐渐完善，形成了包括**GPUDirect Storage、GPUDirect RDMA、GPUDirect P2P 和 GPUDirect Video四组重要技术的组合。**  
***1）GPUDirect Storage***  
对AI和HPC应用而言，随着数据规模的不断扩大，数据加载时间对系统性能影响越发显著。随着GPU计算速度的快速提升，系统I/O（数据从存储读取到GPU显存）已经成为系统瓶颈。  
   
GPUDirect Storage提供本地存储（NVMe）/远程存储（NVMe over Fabric）与GPU显存的直接通路，它可以减少不必要的系统内存拷贝（通过bounce buffer）。它可应用网卡NIC和存储系统附近的DMA引擎，直接向GPU显存写入/读取数据。  
   
***2）GPUDirect RDMA***  
RDMA (Remote direct memory access)技术可使外围PCIe设备直接访问GPU显存。GPUDirect RDMA被设计用来支持GPU间快速跨机通信。它能减轻CPU负载，同时也能减少不必要的通过系统内存进行的数据拷贝。  
  
GPUDirect RDMA在CUDA Toolkit中提供支持。您可联系网络供应商下载相关驱动，来使用RDMA功能。它对Tesla and Quadro GPU都是可用的。  
***3）GPUDirect for Video***  
GPUDirect for Video提供一个服务于frame-based的通过优化的流水线功能。设备包括：frame grabbers、video switchers、HD-SDI capture、CameraLink device，它可以把视频帧高效地向GPU显存中写入/读出。  
  
过去处理视频的第三方硬件与GPU交互时，会引入不必要的延迟，如图6左边所示。有了GPUDirect for Video技术，I/O设备和GPU可达到很好的同步（两个设备driver间拷贝数据），同时能减少CPU的负载。GPUDirect for Video由第三方公司的SDK提供，开发者对视频流进/出GPU（通过OpenGL， DirectX or CUDA在子帧的传输过程 ）有充分的控制能力[7]。  
***4）GPUDirect P2P***  
GPUDirect P2P支持GPU之间通过memory fabric（PCIe或NVLink）直接进行数据拷贝。CUDA driver原生支持P2P技术，开发者可使用最新的CUDA Toolkit和driver来实现GPU间直接通信[6]（一般用于机内通信）。  
**2、NVLink**  
介绍完GPU Direct技术后，我们来看一下另一项机内互联技术NVlink。  
当训练数据不断增长时，PCIe 的带宽满足不了需求，会逐渐成为系统瓶颈。为提升多 GPU 之间的通信性能，充分发挥 GPU 的计算性能，**NVIDIA 于 2016 年发布了全新架构的 NVLink。**这项技术不仅仅是SLI技术的升级，而且是对GPU如何互联的根本性重新思考。  
   
NVLink 是一种高速、高带宽的互连技术，用于连接多个 GPU 之间或连接 GPU 与其他设备（如CPU、内存等）之间的通信。**NVLink 提供了直接的点对点连接，具有比传统的 PCIe 总线更高的传输速度和更低的延迟。**  
NVLink代表了多GPU互联技术的逻辑演变，不仅在速度方面，而且在架构设计方面。NVLink的结构由可以双向传输数据的高速数据通道组成。与传统的基于总线的系统不同，NVLink采用点对点连接，有效减少瓶颈并提高数据吞吐量。最新的迭代提供高达900GB/s的带宽，比SLI的功能有了显著增强。  
NVLink与众不同的关键功能之一是它支持网状拓扑的能力。与旧技术的菊花链或中心辐射型拓扑相比，网格设置允许GPU之间实现更通用且数量更多的连接。这在数据中心和高性能计算应用程序中特别有用，在这些应用程序中，复杂的数据路由是常态。  
统一内存是NVLink的另一个特点。这允许GPU共享公共内存池，从而实现更高效的数据共享并减少在GPU之间复制数据的需要。这对于机器学习和大数据分析等应用程序来说是一个巨大的推动，在这些应用程序中，大型数据集通常超过单个GPU的内存容量。  
**NVLink还改善了延迟，这是任何高性能计算设置中的一个关键因素。**较低的延迟可确保GPU之间更快的数据传输和同步，从而实现更高效的并行计算。这是通过NVLink的直接内存访问 (DMA) 功能实现的，允许GPU直接读写彼此的内存，而不需要CPU的参与。  
NVLink技术无法使单服务器中8个GPU达到全连接，为解决该问题，NVIDIA 在2018年发布了NVSwitch，实现了NVLink的全连接。NVIDIA NVSwitch 是首款节点交换架构，可支持单个服务器节点中 16个全互联的GPU，并可使全部8个GPU对分别达到 300GB/s 的速度同时进行通信。  
**3、NVSwitch**  
单服务器中8个GPU卡可以依靠NVLink实现全连接。超过8个之后，就要依靠NVSwitch来实现了。  
   
NVIDIA NVSwitch将多个NVLink加以整合，在单个节点（如 NVIDIA HGX A100）内以NVLink的较高速度实现多对多的GPU通信，从而进一步提高互联性能。NVLink和NVSwitch 的结合使NVIDIA得以高效地将AI性能扩展到多个GPU，每个GPU都有12个连接NVSwitch 的NVLink链路，可实现高速的多对多通信  
   
  
**多机之间GPU卡通信技术**  
随着大数据分析、科技计算、AI 计算等应用对算力需求巨大，单机形态已经不能满足用户需求，  
多机多卡的计算是一个常态，多机间的通信是影响分布式训练的一个重要指标。在这里我们谈谈多机之间GPU卡的通信技术，**主要有RDMA、GPUDirect RDMA和IP over InfiniBand等技术。**  
**1、RDMA**  
在在传统的 TCP/IP 网络通信中，数据发送方需要将数据进行多次内存拷贝，并经过一系列的网络协议的数据包处理工作；数据接收方在应用程序中处理数据前，也需要经过多次内存拷贝和一系列的网络协议的数据包处理工作。经过这一系列的内存拷贝、数据包处理以及网络传输延时等，服务器间的通信时延往往在毫秒级别，不能够满足多机多卡场景对于网络通信的需求。  
   
RDMA（Remote Direct Memory Access）是一种绕过远程主机而访问其内存中数据的技术，解决网络传输中数据处理延迟而产生的一种远端内存直接访问技术。  
目前 **RDMA 有三种不同的技术实现方式：**  
**InfiniBand（IB）**：IB是一种高性能互联技术，它提供了原生的RDMA支持。IB网络使用专用的IB适配器和交换机，通过RDMA操作实现节点之间的高速直接内存访问和数据传输。  
**RoCE（RDMA over Converged Ethernet**）：RoCE是在以太网上实现 RDMA 的技术。它使用标准的以太网作为底层传输介质，并通过使用RoCE 适配器和适当的协议栈来实现RDMA功能。  
**iWARP：**iWARP是基于TCP/IP协议栈的RDMA实现。它使用普通的以太网适配器和标准的网络交换机，并通过在TCP/IP协议栈中实现RDMA功能来提供高性能的远程内存访问和数据传输。  
   
**使用RDMA的优势如下：**  
**零拷贝(Zero-copy) **- 应用程序能够直接执行数据传输，在不涉及到网络软件栈的情况下。数据能够被直接发送到缓冲区或者能够直接从缓冲区里接收，而不需要被复制到网络层。  
**内核旁路(Kernel bypass)** - 应用程序可以直接在用户态执行数据传输，不需要在内核态与用户态之间做上下文切换。  
**不需要CPU干预(No CPU involvement)** - 应用程序可以访问远程主机内存而不消耗远程主机中的任何CPU。远程主机内存能够被读取而不需要远程主机上的进程（或CPU)参与。远程主机的CPU的缓存(cache)不会被访问的内存内容所填充。  
简单来说，**RDMA更像一个去掉中间商的技术，让数据能够快速获取。不再在操作系统、CPU等环节浪费时间。**  
**2、GPUDirect RDMA**  
GPUDirect RDMA 结合了GPU加速计算和 RDMA（Remote Direct Memory Access）技术，实现了在GPU和RDMA网络设备之间直接进行数据传输和通信的能力。它允许GPU直接访问RDMA网络设备中的数据，无需通过主机内存或CPU的中介。  
   
GPUDirect RDMA通过绕过主机内存和CPU，**直接在GPU和RDMA网络设备之间进行数据传输，显著降低传输延迟，加快数据交换速度，并可以减轻 CPU负载，释放CPU的计算能力。**另外，GPUDirect RDMA 技术允许GPU 直接访问RDMA网络设备中的数据，避免了数据在主机内存中的复制，提高了数据传输的带宽利用率  
**3、IPOIB（IP over InfiniBand）**  
IPOIB是一种在 InfiniBand 网络上运行IP协议的技术。它将标准的IP协议栈与 IB 互连技术相结合，使得在IB网络上的节点能够使用IP协议进行通信和数据传输。  
IPOIB 提供了基于RDMA之上的IP网络模拟层，允许应用无修改的运行在 IB 网络上。但是，IPoIB仍然经过内核层（IP Stack），会产生大量系统调用，并且涉及CPU中断，因此IPoIB性能比RDMA通信方式性能要低，大多数应用都会采用RDMA方式获取高带宽低延时的收益，少数的关键应用会采用IPoIB 方式通信。  
   
在大规模计算中，单机多卡场景下使用GPUDiect、NVLink技术，分布式场景下使用 GPUDirect RDMA技术，可以大大缩短通信时间，提升整体性能。  
**NVIDIA 数据中心明星产品**  
**1、Magnum IO**  
NVIDIA Magnum IO是数据中心IO的并行化、智能化架构，它是IO的加速平台。该架构最大限度地提升存储、网络、多节点和多GPU通讯性能，为大型语言模型、推荐系统、成像、仿真和科学研究等全球重要的应用优化实现加速。  
   
它可以最大化很多重要应用的存储、网络、多节点和多GPU通信性能。利用存储IO、网络IO、在网计算和IO管理简化和加速数据移动、访问、多GPU和多节点管理。Magnum IO支持NVIDIA CUDA-X库，同时能利用一系列NVIDIA GPU和NVIDIA网络硬件拓扑实现高吞吐和低延迟。  
**2、DGX**  
DGX是一个完整的超级计算机，它是一套完整的人工智能解决方案，包括硬件设备、软件工具和优化，具有很高的集成度和易用性，适用于企业和研究机构。DGX的系列产品有：DGX-1、DGX-2、DGX A100、DGX H100、DGX GH200、DGX SuperPod、DGX BasePod。  
**3、HGX**  
HGX是一个计算模组，整合了NVIDIA GPU 、 NVLink 、 NVIDIA 网络以及全面优化的 AI 和高性能计算 (HPC) 软件堆栈的全部功能，可提供最高的应用性能并加快获得见解的速度。  
虽然在系统完备性上不如DGX，但它可进行灵活的配置调整，适用于云服务提供商和大型数据中心。HGX的系列产品有：HGX A100、HGX H100、HGX H200。  
**总结**  
本文主要介绍了GPU间通信技术，包括单机多卡间的GPUDirect 和NVLink 技术，多机多卡间的RDMA、IPOIB以及GPUDirect RDMA 技术。在大规模计算中，单机场景下使用NVLink技术，分布式场景下使用GPUDirect RDMA技术，可以极大地缩短通信时间，提升整体性能。  
  
【投稿】：[**SDNLAB原创文章奖励计划**](http://mp.weixin.qq.com/s?__biz=MzAxMDA1NjMwMQ==&mid=2651792740&idx=1&sn=ce83f53a30f3a70bf878955af80bfb4e&chksm=80ada266b7da2b701d7beb0eb3cdfe1d26a3d8e37b09ceacecdc600c166ff2bf7a1f1321b318&scene=21#wechat_redirect)

---
**Tags:** [[Chiplet]] SDI
