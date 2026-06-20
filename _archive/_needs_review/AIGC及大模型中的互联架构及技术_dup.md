# AIGC及大模型中的互联架构及技术

> 笔记本: 我的剪贴板  
> 创建时间: 2024-04-28  

---

人工智能生成内容（AIGC）和大模型（LLM）的火爆，引发了算力需求迅猛增长，随着模型参数规模的不断扩张，一次GPT的部署动辄需要数万块GPU，传统的单一架构显然难以胜任。计算方式逐渐发生了从单机到分布，从同构到异构的转变。同时，由于训练大模型的数据量极大，不同计算节点之间、异构xPU间，超高带宽、超低延迟和超高可靠性的互联技术已成为高性能计算的迫切需求。为了满足上述需求，通信技术也在不断地演进和发展，以下将从节点内部、超级节点、网络层面等维度进行分析。 
为方便理解，画了两张导图，仅供参考。 
 
 
 
 
节点及超级节点内的高速互联技术 
**PCIe/CXL** 
***PCIe*** 
节点内部主要涉及CPU-CPU、CPU-GPU、GPU-GPU之间的通信。其中，CPU-CPU通常采用QPI/UPI通信，本文不做过多论述。 
 
传统架构下，PCIe（PCI express）是服务器内部通信的总线标准，经典的通用服务器内，CPU、GPU、硬盘驱动器、SSD、以太网设备等主要基于PCIe协议相互连接。 
 
 
伴随着大数据、AI人工智能、云计算、自动驾驶、AR/VR等应用快速发展，服务器内的高速硬件数据交互需求变得愈发紧迫，迫使PCIe标准在近些年实现了跨越式发展，在PCIe 5.0还未普及，PCIe 7.0都已在制定之中，处理器I/O带宽的需求每三年实现翻番，PCIe也大致按照3年一代甚至更快的速度更新演进，每一代升级几乎能够实现传输速率的翻倍，并有着良好的向后兼容性。 
 
尽管从PCIe 7.0已经开始制定，但是目前PCIe 5.0也仅仅刚刚开始商用。而大规模分布式训练场景下，节点内GPU间的通信如果通过PCIe总线绕经CPU进行，显然已经无法满足要求，GPU卡间通信必须经过CPU绕转甚至跨CPU NUMA，不仅带来通信延迟，还会增加AI算法的开发难度。 
***CXL*** 
由于存储成本不断增加、数据爆炸式增长、计算和带宽开始失衡，PCIe日趋乏力，为此，2019年，英特尔提出一种开放性互联协议--Compute Express Link（CXL），CXL是建立在PCIe物理层之上的协议，可以实现设备之间的缓存和内存一致性。利用广泛存在的PCIe接口，CXL允许内存在各种硬件上共享：CPU、NIC和DPU、GPU和其它加速器、SSD和内存设备，从而满足高性能异构计算的要求。 
 
CXL 3.0是2022年8月份发布的新标准，CXL3.0建立在PCIe 6.0之上，并且其将一些复杂的标准设计简单化，确保了易用性，通过“内存池化”等方式优化内存调用，进而提升系统整体性能，但通信带宽相比PCIe 6.0无变化。 
 
另外，可用性也是CXL面临的主要问题，主流的GPU中，英伟达的GPU不支持CXL， AMD产品中也只有MI300A理论上可以支持CXL，但并有详细的描述。 
 
**NVLink、NVSwitch和NVLink-network Switch** 
 
***NVLink*** 
 
算力的提升不仅依靠单张GPU卡的性能提升，往往还需要多GPU卡组合。在多GPU系统内部，GPU间通信的带宽通常在数百GB/s以上，PCIe总线的数据传输速率容易成为瓶颈，且PCIe链路接口的串并转换会产生较大延时，影响GPU并行计算的效率和性能。GPU发出的信号需要先传递到PCIe Switch，PCIe Switch中涉及到数据的处理，CPU会对数据进行分发调度，这些都会引入额外的网络延迟，限制了系统性能。 
 
在此背景下，英伟达在PCIe互联体系之外，重新构建了一套自己的NVLink互联体系，NVLink是一种高速的、直接的GPU到GPU的互联技术；而NVSwitch是将多条NVLink整合，在单个节点内以NVLink的速度实现多对多的GPU通信的芯片，类似PCIe技术和PCIe switch的关系，与传统的PCIe解决方案相比，NVLink能为多GPU系统通信提供更快速的替代方案，同时，因为NVIink数倍于以太网和IB网络的带宽优势，NVIink技术也在向网络层面的多节点互联进发，当然现在主要是应用于SuperPod内部节点间的互联----NVLink-network Switch，但是不排除未来进一步向网络层面进军。 
截止目前，NVLink已经演进到了第五代。 
 
 
 
第五代NVLink的每个GPU上有18个NVLink，不过单Link双向带宽从H100的第四 代NVLink的50GB/s升级到100GB/s。所以B100和B200的GPU-to-GPU带宽上限为1.8TB/s（注意是大B，远非PCIe所能比拟的）。 
 
***NVSWitch和NVLink-network Switch*****
** 
NVSwitch的演进如下： 
 
 
这里涉及到三个概念，NVLink、NVSwitch以及NVLink-network Switch。其中： 
 
- 
NVLink：为了应对PCIe选代速度缓慢导致GPU I/O带宽成为整个算力系统的瓶颈，NVLink应运而生，NVLink用于连接GPU之间以及GPU与CPU之间，其允许GPU芯片间以点对点的方式通信，可以突破传统PCIe互联带宽限制，实现更高带宽、更低延迟的数据互连。 

- 
NVSwitch：NVSwitch芯片是一种类似交换机ASIC的物理芯片，通过NVLink接口可以将多个GPU高速互联到一起，实现所有GPU在一个具有全带宽连接的集群中all-to-all互联，从而提升服务器内部多个GPU之间的通讯效率和带宽。NVLink和NVSwitch的结合使NVIDIA得以高效地将AI性能扩展到多个GPU。  
 
NVSwitch在A100中的应用 
- 
NVLink-network Switch：一般情况下，NVSwitch是用于单机服务器内部的GPU间通信，可以理解为把NVSwitch芯片基础到服务器的主板上，从而完成单机内部的GPU间的通信；而NVLink-network Switch则是将NVLink扩展到支持多机（SuperPod）的NVLink Network，例如基于H100或GH200 NVL32搭建的256 GPU的SuperPod，或是基于B100或GB200 NVL72搭建的576 GPU的SuperPod。此情况下，NVLink-network Switch是以交换机板卡或实体交换机的形态存在，但核心的交换芯片是基于NVSwitch。  
**基于H100搭建256 GPU的SuperPod****
** 
在DGX A100情况下，每个节点上8张GPU通过NVLink和NVSwitch互联，机间（不同服务器）直接用200Gbps IB HDR网络互联（注：机间网络可以用IB网络，也可以用RoCE网络）。而在DGX H100的情况下，英伟达把机内的NVLink扩展到机间，增加了NVLink-network Switch，由NVSwitch负责机内的交换，NVLink-network Switch则是负责机间交换的交换机，基于NVSwitch和NVLink-network Switch可以搭建256个H100 GPU组成的SuperPod（即一个超级计算系统 ），256个GPU卡Reduce带宽仍然可以打到450 GB/s，和单机内部8个GPU卡的Reduce带宽完全一致。 
 
 
但是DGX H100的SuperPod也存在一定的问题，跨DGX H100节点的连接只有72个NVLink连接，SuperPod系统里并不是无收敛的网络。 
 
如下图，在DGX H100系统里，四个NVSwitch留出了72个NVLink连接用于通过NVLink-network Switch连接到其他DGX H100系统，72个NVLink连接的总双向带宽是3.6TB/s，而8个H100的总双向带宽是7.2TB/s，因此，在SuperPod系统里在NVSwitch处存在收敛。 
 
 
 
基于H100搭建256 GPU的SuperPod 
 
**基于GH200和GH200 NVL32搭建256 GPU的SuperPod****
** 
2023年，英伟达宣布生成式AI引擎DGX GH200投入量产，GH200是H200 GPU（H200与H100主要是内存大小和带宽性能方面的区别）与Grace CPU的结合体，一个Grace CPU对应一个H200 GPU，GH200除了GPU之间采用NVLink4.0连接以外，GPU和CPU之间也采用NVLink4.0连接。 
 
 
GH200通过NVLink 4.0的900GB/s超大网络带宽能力来提升算力，服务器内部可能采用铜线方案，但服务器之间可能采用光纤连接。对于单个256 GH200芯片的集群，计算侧1个GH200对应9个800Gbps（每个800Gbps对应100GB/s，2条NVLink 4.0链路）光模块。 
GH200 SuperPod与DGX H100 SuperPod的区别在于在单节点内部和节点之间互联时都是用NVLink-network Switch互联。DGX GH200采用二级Fat-tree结构，由8个GH200和3个一级NVLink-network Switch（每个NVSwitch Tray包含2个NVSwitch芯片，有128个Port）组成单机，32个单机经由36个二级NVLink-network Switch全互联，形成了256个GH200的SuperPod（注意是36个二级NVLink-network Switch，这样才能保证无收敛）。 
 
 
基于GH200搭建256 GPU的SuperPod 
GH200 NVL32为机架级集群，单个GH200 NVL32拥有32个GH200 GPU和9个NVSwitch Tray（18个NVSwitch3.0芯片），如果组成256个GPU的GH200 NVL32超级节点，则需要再配置一级机间的36个NVLink-network Switch即可。 
 
**基于GB200 NVL72**搭建576 GPU的SuperPod
 
和GH200不同，一个GB200由1个Grace CPU和2个Blackwell GPU组成（注：单个GPU算力不完全等价B200）。GB200 Compute Tray是基于英伟达MGX设计的，一个Compute Tray包含2个GB200，也就是2个Grace CPU、4个GPU。 
 
一个GB200 NVL72节点包含18个GB200 Compute Tray，即36个Grace CPU，72个GPU，此外还包含9个NVLink-network Switch Tray（每个Blackwell GPU有18个NVLink，而每个第4代NVLink-network Switch Tray包含144个NVLink Port，所以需要72*18/144=9个NVLink-network Switch Tray实现全互联）。 
 
 
GB200 NVL72内部拓扑架构 
在英伟达的官方宣传中，8个GB200 NVL72组成一个SuperPod，从而组成一个由576个GPU组成的超级节点。但是，我们通过分析可以看出GB200 NVL72机柜中的9个NVLink-network Switch Tray已经全部用于连接72个GB200了，已经没有额外的NVLink接口用于扩展构成更大规模的两层交换集群了，576个GPU的SuperPod从英伟达官方的图片来看，更多的是通过Scale-Out RDMA网络互联的，而并不是通过Scale-Up的NVLink网络互联的。如果需要通过NVLink互联来支持576个GPU的SuperPod，则需要每72个GB200配置18个NVSwitch，这样单机柜就放不下了。 
 
另外，英伟达官方说NVL72有单机柜版本，也有双机柜的版本，并且双机柜每个Compute Tray只有一个GB200子系统，这样有可能是通过双机柜的版本来实现通过NVLink互联来支持576个GPU的SuperPod，这样这个双机柜版本的每个双机柜有72个GB200和18个NVLink-network Switch Tray，从而可以满足两层集群的部署需要。如下图所示： 
 
 
基于GB200搭建576 GPU的SuperPod 
和上一代256个H200全互联类似结构类似，只是第一级及第二级所有的设备台数有所不同，需要两级NVLink-network Switch互联： 
 
第一级的一半Port连接576个Blackwell GPU，所以需要576*18/(144/2) =144个NVLink-network Switch，每个NVL72有18个NVLink-network Switch Tray。第二级Port全部与第一级的NVLink-network Switch Port连接，所以需要144*72/144=72 个NVSwitch。 
 
注：英伟达超大规模与HPC业务总经理Ian Buck提到：NVLink Switch 3中256个GPU的理论上限只适用于研究，对实际生产无甚影响；同样的，NVLink Switch 4中576个GPU的理论上限同样只适用于研究，实际生产不可能触及，实际生产中更多的是用NVL32/NVL72来进行部署，通过IB或RoCE进行更大规模的集群扩展。 
 
**HCCS****
** 
华为在昇腾Ascend 910B中也定义了类似英伟达NVLink的高速通信接口，即HCCS，HCCS采用对等拓扑（暂时没有对应NVSwitch芯片之类的东西），HCCS单链路的最大带宽是56GB/s。 
 
 
**Infinity Fabric** 
Infinity Fabric实际是由传输数据的Infinity Scalable Data Fabric(SDF)和负责控制的Infinity Scalable Control Fabric(SCF)两个系统组成。Infinity Fabric连接了on-die和off-die以及多路CPU间的通信，但AMD没有把Infinity Fabric用的节点间的通信中。最新的AMD Instinct MI300X GPU采用5nm制程，支持客户将8个GPU整合为一个性能主导型节点，并且具有全互联式点对点环形设计，单一平台内的HBM3显存总计可达到1.5 TB——提供足以应对各类AI或HPC工作负载部署的性能密集型解决方案，使用了第4代Infinity Fabric高速总线互联，从而实现结构的简化以及编程的便利性，Infinity Fabric总线带宽达到896GB/s（与英伟达H100的900GB/s带宽相当）。 
 
 
除了前面提到的英伟达NVLink、华为HCCS、AMD Infinity Fabric以外，其他的AI芯片厂家也有定义自己的片间高速互联技术，如寒武纪MLU-LINK、燧原GCU-LARE、壁仞B-LINK等，这里不再一一论述。 
 
网络层面 
网络层面，在AIGC/LLM/超算等领域，需要几百个上千个GPU连在一起的集群计算已俨然成为AI训练的标配。面对这样规模庞大的数据交互，传统的TCP/IP协议逐渐被RDMA（远程直接内存访问）技术取代。RDMA技术有四种实现：InfiniBand、RoCEv1、RoCEv2和iWARP。业界通用的网络解决方案在向InfiniBand和RoCEv2集中。 
- 
IB网络：InfiniBand（IB）网络起源于超算，其设计旨在为超算提供低延迟、高吞吐量的数据传输解决方案，同时，IB也成为大规模AI训练集群的一种很好的选择，但是InfiniBand成本和封闭性，也导致大家在选择的时候有这样或那样的顾虑。 

- 
RoCE网络：基于以太网RoCE（RDMA over Converged Ethernet）网络协议，可以利用现有的以太网基础设施，构建与IB网络性能接近RDMA网络，但是RoCE网络也面临诸如：RoCE参数配置的复杂、交换机时延高于IB交换机、提供端到端的解决方案困难（交换机、网卡、上层应用之间的配合）等问题。 

- 
UCE：谈到下一代高速以太网，就不得不提到超以太网联盟（UCE），一个由英特尔、AMD、HPE、Arista、Broadcom、思科、Meta和微软为打破英伟达垄断而共同创始的组织。该组织认为，通过调整以太网的架构，可以让以下一代高速太网的性能像InfiniBand网络一样好，并更具成本与开放性优势，从而让更多的企业加入进来，但是，直到目前UCE的规范也还在制定中，预计2024年第三季度发布v1.0规范，从规范到应用还有很长的路要走，且效果也需要实际应用的检验。  
关于网络层面的相关技术内容，我们将在后面的文章中做进一步分析。  
声明 | 本公众号相关文章仅供交流学习，主要为本人学习笔记和总结，部分内容节选在其它文章或由其它文章归纳所得，版权归原作者或原出处所有，本公众号致力于保护原作者版权，若来源标注错误或侵犯到您的权益，烦请及时联系进行处理。

---
**Tags:** #NaaS
