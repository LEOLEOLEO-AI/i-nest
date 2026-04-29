---
title: "第39届ACM SIGCOMM大会RDMA技术前沿与创新实践"
source: "https://mp.weixin.qq.com/s/2wKkKu8UaKT_9BwvAJu5WQ"
created: 2025-09-19
note_id: "1887885660590371312"
tags:
  - "AI链接笔记"
  - "ACM SIGCOMM 2025"
  - "RDMA网络"
  - "数据中心网络"
  - "get-笔记"
  - "学术论文"
---

# 第39届ACM SIGCOMM大会RDMA技术前沿与创新实践

## 摘要

📊 **大会核心数据** - 投稿量：463篇，录用75篇，接收率仅16.2% - 地域亮点：亚洲唯一Best Student Paper Award由华为与香港科技大学合作团队获得  🔍 **RDMA技术发展洞察** - 当前主流：IB和RoCEv2为高性能数据中心主流RDMA技术 - 现存痛点：

## 正文

第39届ACM SIGCOMM大会近日在葡萄牙落下帷幕，来自世界各地的技术大牛分享了计算机网络领域最前沿的技术，为本领域的从业者贡献了一场顶级的技术盛宴。本届 SIGCOMM 投稿共 463 篇，录用 75 篇，接收率仅 16.2%。

本届SIGCOMM中关于RDMA网络的讨论有许多值得关注的内容。

当前，以IB和RoCEv2为主的RDMA网络已成为高性能数据中心的主流。但RoCE在超大规模部署中暴露出的线头阻塞、多路径乱序、ECMP负载均衡等痛点正催生新一代技术变革。

新成立的UEC联盟旨在构建开放、高性能的以太网通信体系，其标准制定虽处早期，但已明确通过原生支持多路径数据包喷洒和增强拥塞控制等方式来超越传统以太网的局限性，预示着RDMA技术正从依赖特定无损网络向更开放、健壮、可大规模扩展的方向演进。

[超级以太网联盟UEC 1.0
规范终于发布！](https://mp.weixin.qq.com/s?__biz=MzI5NzQxNDcxNw==&mid=2247485093&idx=1&sn=4f7fb2505a6122d76b654f0d700d431d&scene=21#wechat_redirect)

[超级以太网调研报告（附下载）](https://mp.weixin.qq.com/s?__biz=MzI5NzQxNDcxNw==&mid=2247484258&idx=1&sn=401acdb6eb07046a32a29207e011bc46&scene=21#wechat_redirect)

挑选了本届SIGCOMM中三篇RDMA相关的论文：

Revisiting RDMA Reliability for Lossy Fabrics

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc4923d4d5d192ce687367a8119026f2d?Expires=1780067024&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=TFEzEFmb433c5E3L%2FaYKJoTrCE0%3D)

第一篇来自华为与香港科技大学iSING Lab 合作的新型RDMA传输架构DCP，获本届大会 Best Student Paper Award，成为亚洲地域唯一的获奖论文。该论文提出的数控分离传输架构DCP，解决大规模AI集群网络可扩展性难题，帮助构建大规模、高性能、高可靠的网络底座，充分释放AI算力。

摘要：由于无损RDMA网络的操作复杂性和有限的部署规模，业界一直在探索在有损网络上实现高效的RDMA通信。最先进的（SOTA）有损RDMA解决方案在RDMA网卡中采用了简化的选择性重传机制，以提高丢包恢复效率。然而，这些解决方案仍面临性能挑战，例如不可避免的等价多路径（ECMP）哈希冲突和过多的重传超时（RTO）。

在本文中，我们重新探讨RDMA的可靠性，目标是不依赖优先级流控制（PFC）、数据包级负载均衡兼容、摆脱重传超时，并且便于硬件卸载。为此，我们提出了DCP，一种协同设计交换机和网卡的传输架构，它能完全满足设计目标，其核心是DCP-Switch引入了一个简单却有效的无损控制平面，DCP-RNIC利用该平面增强对高速有损网络的可靠性支持，主要包括基于纯报头的重传和bitmap的数据包跟踪。我们使用P4交换机对DCP-Switch进行原型设计，并使用FPGA对DCP-RNIC进行原型设计。大量实验表明，与最先进的无损和有损RDMA解决方案相比，DCP的性能分别提升了1.6倍和2.1倍。

## Alibaba Stellar: A New Generation RDMA Network for Cloud AI

## 图片

## **第二篇来自阿里巴巴 Stellar 网络，Stellar 被定义为新一代面向云端 AI 的 RDMA 网络，其核心关键点包括虚拟化直接内存访问（PVDMA）、扩展内存转换表（eMTT）和 RDMA Packet Spray。**

## 

## 摘要：大语言模型（LLMs）在云环境中的快速应用，加剧了对高性能AI训练和推理的需求，而RDMA在其中发挥着关键作用。然而，现有的RDMA虚拟化解决方案，如SR-IOV，在可扩展性、性能和稳定性方面存在显著局限性。这些问题包括容器初始化时间过长、硬件资源受限以及流量传输效率低下等。为了应对这些挑战，我们提出了Stellar：一种新一代的云AI网络。 Stellar引入了三项关键创新：用于按需内存锁定的半虚拟化直接内存访问（PVDMA）、用于优化GPU Direct RDMA（GDR）性能的扩展内存转换表（eMTT），以及用于高效多路径利用的RDMA数据包喷洒技术。Stellar部署在我们的大规模AI集群中，能在几秒钟内启动虚拟设备，将容器初始化时间缩短15倍，并将大语言模型（LLM）的训练速度提升高达14%。我们的评估表明，Stellar的性能显著优于现有解决方案，为云AI提供了一个可扩展、稳定且高性能的RDMA网络。 Falcon: A Reliable, Low Latency Hardware Transport 图片 第三篇来自谷歌的 Falcon：一种可靠的低延迟硬件传输。 摘要：像RoCE之类的硬件传输技术能以极少的CPU占用实现高性能，但它们最适合于限制其使用场景的专用部署，例如后端网络或带有优先级流控制（PFC）的以太网。我们推出了Falcon，这是首款在通用以太网数据中心环境（存在丢包且无需特殊交换机支持）中支持多种上层协议（ULP）和异构应用工作负载的硬件传输技术。 其关键设计要素包括：具有多路径负载均衡的基于延迟的拥塞控制；采用简单请求-响应事务接口以支持多上层协议的分层设计；基于硬件的重传和错误处理以实现可扩展性；以及用于提升灵活性的可编程引擎。 首个Falcon硬件实现的峰值性能达到200Gbps、120Mops/秒，其近乎最优的操作完成时间在网络拥塞情况下比CX-7 RoCE低8倍，在有丢包的情况下吞吐量则高出多达65%。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fa6e3ccdd63f842108a2757589850854f?Expires=1780067024&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=oJhY2Tdj9FSQIlzD5XMN4EilXeE%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F8abe3ce296a481a96f1e4e024ac0cf83?Expires=1780067024&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=TQEJXspGYJFa1srtrGFpzwdYWgQ%3D)

[2024 SIGCOMM 论文导读](https://mp.weixin.qq.com/s?__biz=MzI5NzQxNDcxNw==&mid=2247484492&idx=1&sn=da837306583bf5e882732b9da46347f6&scene=21#wechat_redirect)

[Hot Chips 2025会议资料(全)下载](https://mp.weixin.qq.com/s?__biz=MzI5NzQxNDcxNw==&mid=2247485217&idx=2&sn=657c0aad637393474b3602a742787a1c&scene=21#wechat_redirect)

[超级以太网支持的三种网络类型](https://mp.weixin.qq.com/s?__biz=MzI5NzQxNDcxNw==&mid=2247485193&idx=1&sn=27fc9474f64e281b09997dc7d20b4cfe&scene=21#wechat_redirect)

[【2025】以太网发展路标解读](https://mp.weixin.qq.com/s?__biz=MzI5NzQxNDcxNw==&mid=2247485181&idx=1&sn=2c1fb5c9f8011286b2c9b6ec247785cd&scene=21#wechat_redirect)

[【Hot Chips 2025】NVIDIA 展示 CX-8 超级网卡](https://mp.weixin.qq.com/s?__biz=MzI5NzQxNDcxNw==&mid=2247485217&idx=1&sn=432ac457eb9ae86d64eb723d7de9167d&scene=21#wechat_redirect)

[RDMA网络消息率：重要性与测试解析（附测试程序）](https://mp.weixin.qq.com/s?__biz=MzI5NzQxNDcxNw==&mid=2247485170&idx=1&sn=0b4072a80e89b98228c53d714bcaf3f3&scene=21#wechat_redirect)

[Flowcut Switching，让自适应路由与按序传输兼得](https://mp.weixin.qq.com/s?__biz=MzI5NzQxNDcxNw==&mid=2247485145&idx=1&sn=1d95f8bc6fd0257b4997a3604284e9a9&scene=21#wechat_redirect)

[Meta基于RoCEv2构建的大规模AI网络](https://mp.weixin.qq.com/s?__biz=MzI5NzQxNDcxNw==&mid=2247485059&idx=1&sn=e7059c9aded3f2a04fdfa4a1df695957&scene=21#wechat_redirect)

[以太网RDMA网卡综述——国防科大杨惠团队](https://mp.weixin.qq.com/s?__biz=MzI5NzQxNDcxNw==&mid=2247485044&idx=1&sn=a25d601d441dd0aaf2f20af76edb1821&scene=21#wechat_redirect)

[字节跳动发布 GPU Scale-up 互联技术白皮书，并推出 EthLink 网络方案。（附下载）](https://mp.weixin.qq.com/s?__biz=MzI5NzQxNDcxNw==&mid=2247485030&idx=1&sn=e01627b4e1ac08401b7811feacf69f25&scene=21#wechat_redirect)

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 11:03*