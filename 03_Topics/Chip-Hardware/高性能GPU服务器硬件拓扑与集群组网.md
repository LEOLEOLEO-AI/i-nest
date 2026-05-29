# 高性能GPU服务器硬件拓扑与集群组网

> 笔记本: 技术学习  
> 创建时间: 2024-04-16  

---

[
                智能计算芯世界              ](#)
              
            
            
              *2024-04-04 08:19*
              *四川*
                          
          

          
          
          
            
              
              
            
              
              
                
              
            
          

          
          

          
                                        

          
                    

          
                              
                                        
                    
                    
          
          
          
          
          
                                                  


**01****、****术语与基础**

大模型训练一般都是用单机 8 卡 GPU 主机组成集群，机型包括 8*{A100,A800,H100,H800} 。下面一台典型 8*A100 GPU 的主机内硬件拓扑：


| 典型 8 卡 A100 主机硬件拓扑

本节将基于这张图来介绍一些概念和术语，有基础的可直接跳过。

关于CPU、服务器和存储详细技术，请参考“[下载提醒：服务器基础知识全解(终极版)](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650741318&idx=1&sn=109db31f0a49f20170ec5744b9c7a67e&chksm=83e8dc27b49f5531df8627770d66f835cc62954228702fde80e0f1c82c02cf9175bf83efbd2d&scene=21#wechat_redirect)”，“[2023年服务器计算机CPU行业报告](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650745237&idx=1&sn=eb307f474a6df8eaef1fd3dbf9f5d99d&chksm=83e8eff4b49f66e2101bac70d6046e388f36af596c39e679630181934cd8acb98f9663e42848&scene=21#wechat_redirect)”、“[2023年机架式服务器行业洞察](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650744924&idx=1&sn=08116f9b46b9a83fef7a3937c258e901&chksm=83e8ee3db49f672b51a4137fc74d812b30631eb548871fb2592f20cea3b949862d50dd9fc85a&scene=21#wechat_redirect)”、“[2023~2025服务器CPU路线图](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650744183&idx=1&sn=746c077657af91dbfdd746c42b4847a7&chksm=83e8e316b49f6a00d6034a396157decd73ce0e9eac94587040a98506484214884ef2d0ddd58f&scene=21#wechat_redirect)”、“[2023服务器产业链及市场竞争格局](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650741387&idx=1&sn=55a02afd0d17077589e6c1a08715db10&chksm=83e8dceab49f55fc26e4a5517aad3dd948b201276d25d50ba7d22c44bb781b510d2faf5b3eed&scene=21#wechat_redirect)”、“[存储系统关键技术全解（终极版）](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650744809&idx=1&sn=a4cdc160176f3730fc812eb0a98836b8&chksm=83e8e188b49f689e141d705b9e63f6dc1861027c21897c14183b75cf751b6093c709d3e676c2&scene=21#wechat_redirect)”、“[**更新下载：存储系统基础知识全解（终极版）**](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650743814&idx=1&sn=8a38067f2b13ad7ffcd0a124964ab67f&chksm=83e8e267b49f6b71d6cbb693083133199fce398a5689f58011fbe023ea878279ae4f8a0a1b00&scene=21#wechat_redirect)”、“[存储芯片技术基础知识介绍（2023）](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650744012&idx=1&sn=8d797a8085babdb6e7c5b5948bc745c7&chksm=83e8e2adb49f6bbb83b7148e1b40cd222907e4ffba26e4d9e6e4bd6506e7749e28a3324b6408&scene=21#wechat_redirect)”等等。


** PCIe 交换芯片**

CPU、内存、存储（NVME）、GPU、网卡等支持 PICe 的设备，都可以连接到 PCIe 总线或专门的 PCIe 交换芯片，实现互联互通。

PCIe 目前有 5 代产品，最新的是 Gen5。


**NVLink**

**＞定义**
****
Wikipedia 上 NVLink 上的定义：

*NVLink is a wire-based serial multi-lane near-range communications link developed by Nvidia. Unlike PCI Express, a device can consist of multiple NVLinks, and devices use mesh networking to communicate instead of a central hub. The protocol was first announced in March 2014 and uses a proprietary high-speed signaling interconnect (NVHS).*

简单总结：同主机内不同 GPU 之间的一种高速互联方式：

- 
是一种短距离通信链路，保证包的成功传输，更高性能，替代 PCIe，
- 
支持多 lane，link 带宽随 lane 数量线性增长，
- 
同一台 node 内的 GPU 通过 NVLink 以 full-mesh 方式（类似 spine-leaf）互联，
- 
NVIDIA 专利技术。

**＞演进：1/2/3/4 代**

主要区别是单条 NVLink 链路的 lane 数量、每个 lane 的带宽（图中给的都是双向带宽）等：


| NVLink 演进。Image from: HotChips 2022 [1]

例如：
- 
A100 是 2 lanes/NVSwitch * 6 NVSwitch * 50GB/s/lane= 600GB/s 双向带宽（单向 300GB/s）。注意：这是一个 GPU 到所有 NVSwitch 的总带宽；
- 
A800 被阉割了 4 条 lane，所以是 8 lane * 50GB/s/lane = 400GB/s 双向带宽（单向 200GB/s）。

**＞监控**
****
基于 DCGM 可以采集到实时 NVLink 带宽：


| Metrics from dcgm-exporter [5]


**NVSwitch**

还是参考下图：


| 典型 8 卡 A100 主机硬件拓扑

NVSwitch 是 NVIDIA 的一款交换芯片，封装在 GPU module 上，并不是主机外的独立交换机。

下面是真机图，浪潮的机器，图中 8 个盒子就是 8 片 A100，右边的 6 块超厚散热片下面就是 NVSwitch 芯片：


Inspur NF5488A5 NVIDIA HGX A100 8 GPU Assembly Side View. Image source: [2]


**NVLink Switch**

NVSwitch 听名字像是交换机，但实际上是 GPU module 上的交换芯片，用来连接同一台主机内的 GPU。

2022 年，NVIDIA 把这块芯片拿出来真的做成了交换机，叫 NVLink Switch [3]， 用来跨主机连接 GPU 设备。

这俩名字很容易让人混淆。


**HBM (High Bandwidth Memory)**


**＞由来**

传统上，GPU 显存和普通内存（DDR）一样插在主板上，通过 PCIe 连接到处理器（CPU、GPU）， 因此速度瓶颈在 PCIe，Gen4 是 64GB/s，Gen5 是 128GB/s。

因此，一些 GPU 厂商（不是只有 NVIDIA 一家这么做）将将多个 DDR 芯片堆叠之后与 GPU 封装到一起 （后文讲到 H100 时有图），这样每片 GPU 和它自己的显存交互时，就不用再去 PCIe 交换芯片绕一圈，速度最高可以提升一个量级。这种“高带宽内存”（High Bandwidth Memory）缩写就是 HBM。

HBM 的市场目前被 SK 海力士和三星等韩国公司垄断。

**＞演进：HBM 1/2/2e/3/3e**

From wikipedia HBM，


| 使用了 HBM 的近几代高端 NVIDIA GPU 显存带宽（双向），纵坐标是 TB/s。Image source: [3]

- 
AMD MI300X 采用 192GB HBM3 方案，带宽 5.2TB/s；
- 
HBM3e 是 HBM3 的增强版，速度从 6.4GT/s 到 8GT/s。


**带宽单位**

大规模 GPU 训练的性能与数据传输速度有直接关系。这里面涉及到很多链路，比如 PCIe 带宽、内存带宽、NVLink 带宽、HBM 带宽、网络带宽等等。

- 
网络习惯用 bits/second (b/s) 表示之外，并且一般说的都是单向（TX/RX）；
- 
其他模块带宽基本用 byte/sedond (B/s) 或 transactions/second (T/s) 表示，并且一般都是双向总带宽。

比较带宽时注意区分和转换。


**02、****典型**** 8*A100/8*A800** **主机**


**主机内拓扑：****2-2-4-6-8-8**


- 
2 片 CPU（及两边的内存，NUMA）
- 
2 张存储网卡（访问分布式存储，带内管理等）
- 
4 个 PCIe Gen4 Switch 芯片
- 
6 个 NVSwitch 芯片
- 
8 个 GPU
- 
8 个 GPU 专属网卡


| 典型 8 卡 A100 主机硬件拓扑

下面这个图画的更专业，需要更多细节的可参考：


NVIDIA DGX A100 主机（官方 8 卡机器）硬件拓扑。Image source: [4]

**＞存储网卡**

通过 PCIe 直连 CPU。用途：
- 
从分布式存储读写数据，例如读训练数据、写 checkpoint 等；
- 
正常的 node 管理，ssh，监控采集等等。

官方推荐用 BF3 DPU。但其实只要带宽达标，用什么都行。组网经济点的话用 RoCE，追求最好的性能用 IB。

**NVSwitch fabric：intra-node full-mesh**
****
8 个 GPU 通过 6 个 NVSwitch 芯片 full-mesh 连接，这个 full-mesh 也叫 NVSwitch fabric；full-mesh 里面的每根线的带宽是 n * bw-per-nvlink-lane：

- 
A100 用的 NVLink3，50GB/s/lane，所以 full-mesh 里的每条线就是 12*50GB/s=600GB/s，注意这个是双向带宽，单向只有 300GB/s。
- 
A800 是阉割版，12 lane 变成 8 lane，所以每条线 8*50GB/s=400GB/s，单向 200GB/s。

**用 nvidia-smi topo 查看拓扑**

下面是一台 8*A800 机器上 nvidia-smi 显示的实际拓扑（网卡两两做了 bond，NIC 0~3 都是 bond）：


- 
GPU 之间（左上角区域）：都是 NV8，表示 8 条 NVLink 连接；
- 
NIC 之间：
在同一片 CPU 上：NODE，表示不需要跨 NUMA，但需要跨 PCIe 交换芯片；
不在同一片 CPU 上：SYS，表示需要跨 NUMA；

- 
GPU 和 NIC 之间：
在同一片 CPU 上，且在同一个 PCIe Switch 芯片下面：NODE，表示只需要跨 PCIe 交换芯片；

在同一片 CPU 上，且不在同一个 PCIe Switch 芯片下面：NODE，表示需要跨 PCIe 交换芯片和 PCIe Host Bridge；

不在同一片 CPU 上：SYS，表示需要跨 NUMA、PCIe 交换芯片，距离最远；


**GPU 训练集群组网：IDC GPU fabirc**


GPU node 互联架构：


****
**＞计算网络**

GPU 网卡直连到置顶交换机（leaf），leaf 通过 full-mesh 连接到 spine，形成跨主机 GPU 计算网络。

- 
这个网络的目的是 GPU 与其他 node 的 GPU 交换数据；
- 
每个 GPU 和自己的网卡之间通过 PCIe 交换芯片连接：GPU <--> PCIe Switch <--> NIC。

**＞存储网络**

直连 CPU 的两张网卡，连接到另一张网络里，主要作用是读写数据，以及 SSH 管理等等。

**RoCE vs. InfiniBand**

不管是计算网络还是存储网络，都需要 RDMA 才能实现 AI 所需的高性能。RDMA 目前有两种选择：
- 
RoCEv2：公有云卖的 8 卡 GPU 主机基本都是这种网络，比如 CX6 8*100Gbps 配置；在性能达标的前提下，（相对）便宜；
- 
InfiniBand (IB)：同等网卡带宽下，性能比 RoCEv2 好 20% 以上，但是价格贵一倍。


**数据链路带宽瓶颈分析**


| 单机 8 卡 A100 GPU 主机带宽瓶颈分析

几个关键链路带宽都标在图上了：
- 
同主机 GPU 之间：走 NVLink，双向 600GB/s，单向 300GB/s；
- 
同主机 GPU 和自己的网卡之间：走 PICe Gen4 Switch 芯片，双向 64GB/s，单向 32GB/s；
- 
跨主机 GPU 之间：需要通过网卡收发数据，这个就看网卡带宽了，目前国内 A100/A800 机型配套的主流带宽是（单向） 100Gbps=12.5GB/s。所以跨机通信相比主机内通信性能要下降很多。
- 
200Gbps==25GB/s：已经接近 PCIe Gen4 的单向带宽；
- 
400Gbps==50GB/s：已经超过 PCIe Gen4 的单向带宽。

所以在这种机型里用 400Gbps 网卡作用不大，400Gbps 需要 PCIe Gen5 性能才能发挥出来。


**03、****典型 8*H100/8*H800 主机**
****
GPU Board Form Factor 分为两种类型：
- 
PCIe Gen5
- 
SXM5：性能更高一些


**H100 芯片 layout**

下面是一片 H100 GPU 芯片的内部结构：


单片 H100 GPU 内部逻辑布局。Image source: [3]

- 
4nm 工艺；
- 
最下面一排是 18 根 Gen4 NVLink；双向总带宽 18 lanes * 25GB/s/lane = 900GB/s；
- 
中间蓝色的是 L2 cache；
- 
左右两侧是 HBM 芯片，即显存。


**主机内硬件拓扑**

跟 A100 8 卡机结构大致类似，区别：

NVSwitch 芯片从 6 个减少到了 4 个；真机图如下：


与 CPU 的互联从 PCIe Gen4 x16 升级到 PCIe Gen5 x16，双向带宽 128GB/s；


**组  网**

与 A100 也类似，只是标配改成了 400Gbps 的 CX7 网卡， 否则网络带宽与 PCIe Switch 和 NVLink/NVSwitch 之间的差距更大了。


**04、****典型 4*L40S/8*L40S 主机**
****
L40S 是今年（2023）即将上市的新一代“性价比款”多功能 GPU，对标 A100。除了不适合训练基座大模型之外（后面会看到为什么），官方的宣传里它几乎什么都能干。 价格的话，目前第三方服务器厂商给到的口头报价都是 A100 的 8 折左右。


**L40S vs A100 配置及特点对比**

L40S 最大的特点之一是 time-to-market 时间短，也就是从订货到拿到货周期比 A100/A800/H800 快很多。这里面技术和非技术原因都有，比如：

- 
比如 FP64 和 NVLink 都干掉了；
- 
使用 GDDR6 显存，不依赖 HBM 产能（及先进封装）。

价格便宜也有几方面原因，后面会详细介绍：

- 
大头可能来自 GPU 本身价格降低：因为去掉了一些模块和功能，或者用便宜的产品替代；
- 
整机成本也有节省：例如去掉了一层 PCIe Gen4 Swtich；不过相比于 4x/8x GPU，整机的其他部分都可以说送的了。


**L40S 与 A100 性能对比**

下面是一个官方标称性能对比：


具体场景的性能对比网上也有很多官方资料，这里就不列举了。

- 
性能 1.2x ~ 2x（看具体场景）；
- 
功耗：两台 L40S 和单台 A100 差不多。

需要注意，L40S 主机官方推荐的是单机 4 卡而不是 8 卡（后面会介绍为什么）， 所以对比一般是用 两台 4*L40S vs 单台 8*A100。另外，很多场景的性能提升有个 大前提：网络需要是 200Gbps RoCE 或 IB 网络，接下来介绍为什么。


** L40S 攒机**

**＞推荐架构：****2-2-4**
****
相比于 A100 的 2-2-4-6-8-8 架构， 官方推荐的 L40S GPU 主机是 2-2-4 架构，一台机器物理拓扑如下：


| 推荐单机 4 卡 L40S GPU 主机拓扑

最明显的变化是去掉了 CPU 和 GPU 之间的 PCIe Switch 芯片， 网卡和 GPU 都是直连 CPU 上自带的 PCIe Gen4 x16（64GB/s）：

- 
2 片 CPU（NUMA）
- 
2 张双口 CX7 网卡（每张网卡 2*200Gbps）
- 
4 片 L40S GPU
- 
另外，存储网卡只配 1 张（双口），直连在任意一片 CPU 上

这样每片 GPU 平均 200Gbps 网络带宽。

**＞不推荐架构：****2-2-8**


单机 8 卡 L40S GPU 主机拓扑，来自 NVIDIA L40S 官方推介材料

如图，跟单机 4 卡相比，单机 8 卡需要引入两片 PCIe Gen5 Switch 芯片：
- 
说是现在PCIe Gen5 Switch 单片价格 1w 刀（不知真假），一台机器需要 2 片；价格不划算；
- 
PCIe switch 只有一家在生产，产能受限，周期很长；
- 
平摊到每片 GPU 的网络带宽减半。


**组网**

官方建议 4 卡机型，搭配 200Gbps RoCE/IB 组网。


**数据链路带宽瓶颈分析**


|  单机 4 卡 L40S GPU 主机带宽瓶颈分析

以同 CPU 下面的两种 L40S 为例，这里面有两条链路可选：

1）直接通过 CPU 处理：GPU0 <--PCIe--> CPU <--PCIe--> GPU1
- 
PCIe Gen4 x16 双向 64GB/s，单向 32GB/s；
- 
CPU 处理瓶颈？TODO

2）完全绕过 CPU 处理，通过网卡去外面绕一圈再回来：GPU0 <--PCIe--> NIC <-- RoCe/IB Switch --> NIC <--PCIe--> GPU1
- 
PCIe Gen4 x16 双向 64GB/s，单向 32GB/s；
- 
平均每个 GPU 一个单向 200Gbps 网口，单向折算 25GB/s；
- 
需要 TCCL 支持，官方说新版本 TCCL 正在针对 L40S 适配，默认行为就是去外面绕一圈回来；

第二种方式看着长了很多，但官方说其实比方式一还要快很多（这里还每太搞懂，CPU 那里是怎么处理的？）—— 前提是网卡和交换机配到位：200Gbps RoCE/IB 网络。在这种网络架构下（网络带宽充足）。

- 
任何两片 GPU 的通信带宽和延迟都是一样的，是否在一台机器内或一片 CPU 下面并不重要，集群可以横向扩展（scaling up，compared with scaling in）；
- 
GPU 机器成本降低；但其实对于那些对网络带宽要求没那么高的业务来说，是把 NVLINK 的成本转嫁给了网络，这时候必须要组建 200Gbps 网络，否则发挥不出 L40S 多卡训练的性能。

如果是方式二，同主机内 GPU 卡间的带宽瓶颈在网卡速度。即使网络是推荐的 2*CX7 配置：
- 
L40S：200Gbps（网卡单向线速）
- 
A100：300GB/s（NVLINK3 单向） == 12x200Gbps
- 
A800：200GB/s（NVLINK3 单向） == 8x200Gbps

可以看到，L40S 卡间带宽还是比 A100 NVLINK 慢了 12 倍， 比 A800 NVLink 慢了 8 倍，所以不适合数据密集交互的基础大模型训练。


**测试注意事项**

如上，即便只测试单机 4 卡 L40S 机器，也需要搭配 200Gbps 交换机，否则卡间性能发挥不出来。

*参考资料*
*NVLink-Network Switch - NVIDIA’s Switch Chip for High Communication-Bandwidth SuperPODs, Hot Chips 2022*
*ChatGPT Hardware a Look at 8x NVIDIA A100 Powering the Tool, 2023*
*NVIDIA Hopper Architecture In-Depth, nvidia.com, 2022*
*DGX A100 review: Throughput and Hardware Summary, 2020*
*Understanding NVIDIA GPU Performance: Utilization vs. Saturation, 2023*
相关阅读：
- 
[Arm架构升级，v9与v8版本有何差异？](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650738550&idx=1&sn=cf73968d18217e41c346a7ece631b3bc&chksm=83e8c917b49f40015f35a2747e62955b436314c17994647a4dc051f0f8153fadb9c1873850e5&scene=21#wechat_redirect)
- 
[从X86到ARM，跨越CPU架构鸿沟](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650745252&idx=1&sn=7b6bf25a5a5bfe2fc705f89f44060699&chksm=83e8efc5b49f66d3d8e91018d473844378216ce70bfa2b1825d0ace4be904b8245037d040d77&scene=21#wechat_redirect)
- 
[ARM vs x86云数据库性能深度测评与对比](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650746193&idx=1&sn=984ea1bc0d5fc7f2ac1923a0275e05a5&chksm=83e8eb30b49f62262719ab5d4df7e2704644fa823324ce7193340276bb27f408207dcee5d3f1&scene=21#wechat_redirect)
- 
[从Arm v8到v9，服务器发展之路](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650745268&idx=1&sn=76c3f16bd65ef7aaddaededee336503b&chksm=83e8efd5b49f66c337c12b8bf0e191e0ed105900cfe56884a59de517f4a90b997673a3aa4e0f&scene=21#wechat_redirect)
- 
[ARM与x86：有何区别？](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650744890&idx=1&sn=16a070431e1b54ea72b58d2e9f99d90e&chksm=83e8ee5bb49f674db5f6a0c1ad2817c0c94ab7b844355a5af2c30f5abd634e14636864df6e56&scene=21#wechat_redirect)
- 
[Arm增长突出，中国服务器市场占比达16%](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650742882&idx=1&sn=7f6aa73f59dd8a09c8bb775a9f82fcd1&chksm=83e8e603b49f6f15e1026ec2a1ea8a92c56aa83896b5ddb22153a3a777b19616e7391df92466&scene=21#wechat_redirect)
- 
[分布式软件：X86/ARM CPU混合部署](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650740044&idx=1&sn=12fd329afa89faf3465f1564c53deae2&chksm=83e8d32db49f5a3b683947b22f002f8293a4e6746163b0aa683d74421395ccf8346fa81c34c4&scene=21#wechat_redirect)
- 
[Arm竞争加剧，全球众多巨头涌入](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650739873&idx=1&sn=3a8245b54e335e36cbe36267e06b8dde&chksm=83e8d2c0b49f5bd615d14488aafb30349bbca0fa19c15ff8caabe5be407856986b3024badd77&scene=21#wechat_redirect)
- 
[ARM处理器架构和天梯图解析](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650739689&idx=2&sn=4193845c0742a3bb4ea9ec9fe209e3cc&chksm=83e8d588b49f5c9e87db5b359d024e0ca1f3277db58a7248eac10cde4188fae782d86c683009&scene=21#wechat_redirect)
- 
[信创始于芯：Arm64体系结构编程与实践](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650739584&idx=1&sn=934483d9011f7a43a16a4551076c53a7&chksm=83e8d5e1b49f5cf73a3e5818a63635fdd776c375aad74af7a665ffd1cbb6e1adb3f503e6c337&scene=21#wechat_redirect)
- 
[ARM v8处理器概述、架构、及技术介绍](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650738653&idx=1&sn=dd7265ce3fe259dd52c715b41cfbe99e&chksm=83e8c9bcb49f40aac470a0b08e029627eac9380be9406aad2cf54bcff013c9651b26c742bd4d&scene=21#wechat_redirect)
- 
[飞腾系和鲲鹏系：国产Arm架构CPU服务器正在崛起](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650738520&idx=1&sn=ad8788ebcdcda9349a6526273f1cbbb3&chksm=83e8c939b49f402fa431ba2bf9a96272cd8565d81684f230096005f2067e8f552e24de2d5b25&scene=21#wechat_redirect)
- 
[Fujitsu A64FX：继承SPARC64架构的Arm超级处理器](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650736886&idx=1&sn=b03c2219c0c36f62e2eb1473ab3e857c&chksm=83e8ce97b49f47812898bcc949a182095b983fc0ca8fcb7a0275eb6b25d10f1025c5aab5e2ea&scene=21#wechat_redirect)
- 
[收藏：从全球超算战略看ARM指令架构在HPC领域的发展](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650736880&idx=1&sn=d504e7c6d365d2ac6e8bee43e942a8da&chksm=83e8ce91b49f47871be00311f65092c0e455fb55087dc8d69b3846a8f496fb5877488959e044&scene=21#wechat_redirect)
- 
[众多科技巨头涌入ARM，国内研发进展及玩家详解](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650735166&idx=1&sn=3e5e33787ac2a01e8cb6adbaca790397&chksm=83e8c45fb49f4d498f05514d8c1d199303be246ded7e36036025b7707add58c246f52c4d64b5&scene=21#wechat_redirect)
- 
[亚马逊最新Arm服务器芯片详解](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650732900&idx=1&sn=4fc485f5c67e03624c546c3e34211697&chksm=83e93f05b49eb6137db05be3485ce7de54c53ec26a6218807f594cd9bc10bb6ab69684c02194&scene=21#wechat_redirect)
- 
[计算芯片变革：ARM取代x86成为趋势](http://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650731153&idx=1&sn=14fe9dd5f36753bdecc7ff28193ebe5e&chksm=83e934f0b49ebde6e767277548de1b490731494d864e07f16717192853c0b015a667af32c933&scene=21#wechat_redirect)
- 
[国内外AI芯片、算力综合对比](http://mp.weixin.qq.com/s?__biz=MzUzMzY1NTkwOQ==&mid=2247509458&idx=1&sn=48a7c63eda411253f0f0682a8d6a0b6f&chksm=faa25dd8cdd5d4ceaa1a068e2cc74549f6fbb9c44ab99e40c58d5292ff63545719af497e3914&scene=21#wechat_redirect)
- 
[华为算力编年史（2023）](http://mp.weixin.qq.com/s?__biz=MzUzMzY1NTkwOQ==&mid=2247509448&idx=1&sn=fda4e35dea46150f4a8257718e390c1a&chksm=faa25dc2cdd5d4d430a557b5f46fe2b95dd175354ab640998959d8dea37922403f59fdbdf828&scene=21#wechat_redirect)
- 
[AI算力研究框架（2023）](http://mp.weixin.qq.com/s?__biz=MzUzMzY1NTkwOQ==&mid=2247509385&idx=1&sn=22ed54b57074757a11538bbe112dc29e&chksm=faa25d83cdd5d495464596116ab37230a5aa1c8d387577037b4254d38e3cce31eb305d2bbc8b&scene=21#wechat_redirect)
- 
[大模型训练，英伟达Turing、Ampere和Hopper算力分析](http://mp.weixin.qq.com/s?__biz=MzUzMzY1NTkwOQ==&mid=2247508159&idx=1&sn=22d1f54197c3f7239a75a514d5f2d6a7&chksm=faa258b5cdd5d1a342ec69a1f7a651241b7bd0ccd7e177bc2e30ef988ec38d2cdc479edb93be&scene=21#wechat_redirect)
- 
[AI大语言模型原理、演进及算力测算](http://mp.weixin.qq.com/s?__biz=MzUzMzY1NTkwOQ==&mid=2247508158&idx=1&sn=560b50436efd9a197b0ff7ce78c64b8f&chksm=faa258b4cdd5d1a2b48bdd5044446f5b599ad1ac0fed6240d3d213b4ca0555db676210a4515d&scene=21#wechat_redirect)
- 
[大算力模型，HBM、Chiplet和CPO等技术打破技术瓶颈](http://mp.weixin.qq.com/s?__biz=MzUzMzY1NTkwOQ==&mid=2247507557&idx=1&sn=b4b69bea6ab5b1379484e0416b682f21&chksm=faa2266fcdd5af79d60e95fc699ad1728fd975d2c39f1318bc78e6a823e972fc76d9522d8c62&scene=21#wechat_redirect)
- 
[走进芯时代：AI算力GPU行业深度报告](http://mp.weixin.qq.com/s?__biz=MzUzMzY1NTkwOQ==&mid=2247507158&idx=1&sn=9f4a370567cb973c021ccc56d61e1406&chksm=faa224dccdd5adca29edbe3ee98e3544db7a827685f9ffc0c5000a6e0e4bcc7291a27e547d0e&scene=21#wechat_redirect)
本号资料全部上传至知识星球，更多内容请登录[**智能计算芯知识（知识星球）**](https://mp.weixin.qq.com/s?__biz=MzUzMzY1NTkwOQ==&mid=2247517832&idx=1&sn=24233b983da3cf1a0d2d56e137e1bcba&chksm=fb9bea542615c911d486203a93d14f80e88eeb7e7b28130b0b82740d4b024084e9b10929afd5&scene=132&exptype=timeline_recommend_article_extendread_samebiz&show_related_article=1&subscene=21&scene=132)星球下载全部资料。


**免责申明：**本号聚焦相关技术分享，内容观点不代表本号立场，**可追溯内容均注明来源**，发布文章若存在版权等问题，请留言联系删除，谢谢。

**温馨提示：**
请搜索“**AI_Architect**”或“**扫码**”关注公众号实时掌握深度技术分享，点击“**阅读原文**”获取更多**原创****技术**干货。

---
**Tags:** [[Chiplet]]

---
## 相关笔记 (AI 自动关联)
- [[AI服务器主流互联技术汇总！]]
