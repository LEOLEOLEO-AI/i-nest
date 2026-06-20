---
title: Domain-specific互联网络
tags:
- large-language-model
- software-defined
- tcc-sdi
- topology
---
> 笔记本: 我的剪贴板  
> 创建时间: 2024-09-05  

---

原文链接: [https://mp.weixin.qq.com/s/dMMvxoV1-4I27tjeMTD-7g](https://mp.weixin.qq.com/s/dMMvxoV1-4I27tjeMTD-7g)


这次带来APNET23上John Kim关于**领域特定AI超级计算机时代下的领域特定互连网络**的主题分享，
- 
介绍了架构视角下的网络互联
- 
互联网络构成：微架构、拓扑、路由及流控
- 
领域特定网络的特点：
- 
低延迟 & 高带宽
- 
自定义通信协议
- 
探索NN/LLM通信模式做优化，方便做软件调度网络
- 
低成本
- 
主要分享了两个领域特定网络案例：
- 
Groq软件调度网络，没有交换机，直接用软件调度网络拓扑，更详情参考之前分享
- 
研究AllReduce通信模式，探索不可靠网络中，gradient稀疏做丢弃及skip allreduce对整体性能及模型准确率影响


最后分享了常见的网络物理拓扑、ring/tree结构逻辑拓扑，同时介绍网络中的detour route（即非最小路径路由）。一般根据通信模式设置备用路径提高容错，以及在HPC及领域特定网络中特意设置，以此减少拥塞提高网络整体性能。

---
**Tags:** [[NaaS]]
