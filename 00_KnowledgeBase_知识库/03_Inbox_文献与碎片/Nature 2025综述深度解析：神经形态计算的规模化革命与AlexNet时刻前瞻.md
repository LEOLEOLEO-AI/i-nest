---
title: "Nature 2025综述深度解析：神经形态计算的规模化革命与"AlexNet时刻"前瞻"
source: "https://mp.weixin.qq.com/s/JX9FgYctgrZPklfFK2IGbg"
created: 2026-01-20
note_id: "1899300991099034488"
tags:
  - "AI链接笔记"
  - "神经形态计算"
  - "脉冲神经网络(SNN)"
  - "大规模扩展"
  - "get-笔记"
  - "学术论文"
---

# Nature 2025综述深度解析：神经形态计算的规模化革命与"AlexNet时刻"前瞻

## 摘要

### **🧠 研究背景与核心问题**  **神经形态计算的现状**   - **定义**：模仿大脑结构和功能的计算范式，核心优势为**极高能效**和**实时处理能力**。   - **瓶颈**：尽管Loihi、SpiNNaker等芯片不断迭代，但长期停留在实验室阶段，缺乏类似深度学习中**Alex

## 正文

这里是类脑智能计算，今天带大家解读一篇2025年发表在 Nature 上的重磅综述（Review）。 论文题目： Neuromorphic computing at scale

DOI: 10.1038/s41586-024-08253-8 关键词： 神经形态计算 / 大规模扩展 / AlexNet时刻 / 软硬协同 / 脉冲神经网络(SNN)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff009c7395bc0d0456902bd5e66c59423?Expires=1780061063&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=PlsMzpjlE570ROmiA1a10%2BefVoQ%3D)

# 背景介绍

神经形态计算（Neuromorphic Computing）模仿大脑的结构和功能，承诺了极高的能效和实时处理能力。然而，尽管Loihi、SpiNNaker等芯片层出不穷，该领域长期以来仍停留在实验室的“小打小闹”阶段，缺乏像深度学习中“AlexNet”那样让全世界震惊的杀手级应用。 随着SpiNNaker2（50亿神经元）和Loihi 2（10亿+神经元）等系统的问世，我们正站在一个临界点上。来自Intel Labs、Google DeepMind、曼彻斯特大学等全球顶尖机构的20多位学者联合撰文，试图回答一个关键问题：如何让类脑计算真正实现“规模化”（At Scale），从而引发下一场AI革命？

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd5ac16f84869188294659cda75d9218d?Expires=1780061063&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=w%2BPOfVYodqNGwFfmIWi1MxZgw2s%3D)

图1：神经形态计算系统的演进史

---

**图注解读：**

**指数级增长：** 纵轴是神经元数量（对数坐标）。从1960年的感知机（Perceptron, 520个神经元）到2025年的 **SpiNNaker2 (52亿)** 和 **Loihi 2 (11.5亿)**，硬件规模呈现出类似摩尔定律的爆发式增长。

**里程碑：** 图中标记了各个时代的代表作，如 IBM TrueNorth (2014, 6700万)、Tianjic (天机芯, 400万) 等。这预示着硬件已经为“大模型”做好了准备。

# 一句话解释

这篇综述为神经形态计算的规模化指明了方向，定义了从稀疏性、异步通信到异构集成的关键特征，揭示了当前软件生态系统的巨大断层，并呼吁通过建立统一的标准和大规模测试平台，迎接类脑计算的“AlexNet时刻”。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F2bd18c5a2a59cc72a5a042629a6c2350?Expires=1780061063&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vkNqELu9DYPGfvzIzbbsWCcO%2BNI%3D)

图2：神经形态计算生态系统

---

**图注解读：**

这是一个分层的金字塔结构。

**底层（硬件）：** 涵盖了从数字/模拟电路到新兴器件（如 **RRAM、忆阻器**）的各种物理实现。

**中间层（软件）：** 这里的断层最大。需要从低级汇编语言向上发展到像 PyTorch 那样的高级框架（High-level software）。

**顶层（社区）：** 最终目标是服务于开发者和用户，通过传感器输入（如DVS）和执行器输出（机器人），解决实际问题。

# 核心观点

## 1. 稀疏性与异步通信 (Sparsity & Asynchrony)

大脑是极其稀疏的（并非所有神经元同时放电）。

机制：硬件必须利用稀疏连接和事件驱动（Event-driven）通信。只有当有事件（Spike）发生时才消耗能量，这与时刻都在消耗大量能源的GPU形成了鲜明对比。

## 2. 分布式与分层架构 (Distributed & Hierarchical)

不要试图造一个巨大的单体处理器。

策略：像大脑皮层一样，系统应是分层的、模块化的。这种结构不仅利于扩展，还能让系统处理不同抽象层级的信息（从边缘检测到物体识别）。

## 3. 动态重构与异构集成 (Reconfigurability & Heterogeneity)

动态重构：神经连接不是完全固定的。系统应支持在运行时改变路由和连接，模拟大脑的可塑性。

异构集成：未来的类脑系统不会是孤岛，而是要与传统CPU、FPGA、各种新型传感器（如事件相机）以及忆阻器（RRAM）深度融合。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F977fc9d5fe36577e9631dadeea491ede?Expires=1780061063&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=NOhQWodC9CVQqv4aEmsRqtEnPVI%3D)

图3：规模化系统的关键特征成熟度

**图注解读：**

**成熟度时间轴：** 绿色箭头表示特征的成熟过程。

**早期成熟：****稀疏性 (Sparsity)** 和 **资源感知 (Resource-aware)** 是最早被掌握的特征。

**中期：****可扩展性 (Scalable)** 和 **异步通信 (Asynchronous)** 正在成为主流。

**未来挑战（右侧）：****异构集成 (Heterogeneous)** 和 **动态重构 (Reconfigurable)** 是目前最难的挑战，也是通往类脑智能的必经之路。

# 展望与未来

大脑级模拟 (Brain-scale Simulations)： 随着SpiNNaker2等系统的出现，我们终于有能力实时模拟类似人脑规模的神经网络，这对于理解阿尔茨海默病等脑部疾病至关重要。

打破“硬件彩票” (The Hardware Lottery)： 现有的AI算法之所以流行，往往是因为它们适合在GPU上跑（赢了硬件彩票）。大规模神经形态硬件的普及，可能会催生出一套完全不同的、基于脉冲和时序的新一代AI算法。

终身学习 (Lifelong Learning)：利用存内计算和在线可塑性，未来的设备可以在部署后持续学习，不再需要云端重新训练。

# 讨论

## Q1: 既然硬件规模已经上去了（几十亿神经元），为什么还没出现“AlexNet时刻”？

软件拖了后腿。 正如图4所示，我们缺乏像 PyTorch 这样统一、好用的编程框架。现在的开发者想要用神经形态芯片，往往需要懂底层硬件电路，门槛太高。只有当软件栈（Software Stack）标准化，让普通程序员也能“一键部署”SNN时，爆发才会真正到来。

## Q2: 神经形态计算真的能取代 GPU 吗？

不是取代，是互补。 论文强调了异构集成。GPU 擅长稠密的矩阵乘法（如现在的 Transformer），而神经形态芯片擅长稀疏的、事件驱动的处理（如极低功耗的边缘唤醒、极速的机器人控制）。未来可能是“CPU + GPU + NPU（类脑）”共存的时代。

## Q3: 对于普通研究者，机会在哪里？

算法与编译。 硬件造价昂贵，是巨头的游戏。但中间件（Compiler/Middleware） 和 算法（Algorithm）
是一片蓝海。如何设计一种算法，既能利用SNN的稀疏性，又能保持高精度？如何设计一个编译器，把 PyTorch 代码自动转成脉冲形式跑在 Loihi
上？这些都是顶刊级别的课题。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F09a98a76154a159281695f444c8ec590?Expires=1780061063&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=61RXrjGSTYnTXld2ksrIXTT6k1Q%3D)

图4：软件生态系统的巨大鸿沟 (The Gap)

**图注解读：**

**对比惨烈：** 上方是主流AI（Mainstream AI）的工具链，从 PyTorch 到 TensorRT 再到 GPU，无缝衔接。

**下方现状：** 下方是神经形态（Neuromorphic）工具链。可以看到大量的 **"Missing neuromorphic software"（缺失的软件模块）**，比如缺乏统一的中间表示层（IR）、缺乏跨硬件的编译器。

**结论：** 硬件已经跑得很快了，但软件仍然缺失。没有好用的软件，开发者就无法利用这些强大的硬件。

本文基于Nature综述论文[10.1038/s41586-024-08253-8]解读，仅供学术交流。

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 09:24*