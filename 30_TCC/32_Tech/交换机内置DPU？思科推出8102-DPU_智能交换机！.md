---
title: 交换机内置DPU？思科推出8102-DPU 智能交换机！
tags:
- chip-hardware
- semiconductor
---
> 笔记本: 我的剪贴板  
> 创建时间: 2024-10-14  

---

原文链接: [https://mp.weixin.qq.com/s/3ZX7jSJqJFZfiT3rs2ubOg](https://mp.weixin.qq.com/s/3ZX7jSJqJFZfiT3rs2ubOg)


在上周的 AMD Advancing AI 活动中，除了AMD发布的一系列令人瞩目的新产品，如Instinct MI325X、EPYC 9005 Turin、Pensando Pollara 400和Salina DPU等，思科也展示了其8102-DPU 12.8T交换机。尽管在速度上，这款交换机并不及市场上最新一代的51.2T交换机，但它引入了一种特别的设计理念——内置DPU卡。

**思科8102-DPU 12.8T交换机搭载AMD Pensando DPU**

通常情况下，DPU 主要部署在服务器级别，以提供存储加速、网络配置优化以及其他数据处理服务。但与其在每个服务器上都配备昂贵的DPU，不如在交换机层面实施网络策略。这样，DPU就可以直接与交换机协同工作。

在Cisco Live 2024大会上，思科、微软和AMD共同展示了一个案例研究，他们表示，使用加速基础设施可以节省多达22个CPU核心的资源，并且还能够减少网络延迟波动，提高网络性能。

会上，还将 AMD DPU“Elba”系列与 AWS Nitro v5 和 v4 进行了对比。在某些方面，AMD的性能表现非常出色。

具体来说，思科 8102-28FH-DPU 交换机基于思科 Silicon One Q200L，配备了28个400G QSFP-DD56端口，支持 SONiC 以及 RDMA，以满足高性能工作负载的需求。

在交换机顶部，有四个DPU托架。每个托架配备两个 DPU，最多可容纳 8 个 AMD Elba 代 DPU，可提供高达 1.6Tbps 的 DPU 服务。

思科并不是第一家将DPU内置在交换机的公司。
2022年，HPE Aruba 与AMD合作开发了业界首款具备DPU功能的分布式服务交换机——HPE Aruba Networking CX 10000交换机，内部集成了两块完全可编程的Pensando Elba DPU处理器，利用DPU接管更多状态化数据处理任务，从而得到更多资源应对业务需求。CX 10000 提供3.6 Tbps的标准线速交换，并支持提供1、10和25 GbE服务器接入端口和40/100 GbE上行链路。

在交换机中内置DPU的做法打破了传统的网络设计观念，提出了一种全新的设计理念。这种方式不仅帮助用户在性能、功能和成本之间找到新的平衡点，同时也为数据中心的网络性能优化提供了新的方向。
参考链接：
https://www.servethehome.com/cisco-8102-dpu-12-8t-switch-with-amd-pensando/
https://weibo.com/2455370150/NyjKFcigH

【活动专栏】

【投稿】：[**SDNLAB原创文章奖励计划**](http://mp.weixin.qq.com/s?__biz=MzAxMDA1NjMwMQ==&mid=2651802677&idx=1&sn=f3c8f1950ed3eb46c50b9e4646050c71&chksm=80adcb37b7da422197eec0562ccf1f1273628dd2454a13b039231ee3ba64a7f1c3336255bfeb&scene=21#wechat_redirect)

## Related Notes

- [[(Nat. Commun. 综述) | 基于忆阻器的人工神经网络硬件实现 (第二期)]]
- [[(南加州大学，Nat. Electron.) 紧凑三元件人工神经元实现 多种 类脑脉冲发放]]
- [[10万级 H100 集群：能源、网络拓扑、以太网与 InfiniBand、可靠性、故障、检查点]]
