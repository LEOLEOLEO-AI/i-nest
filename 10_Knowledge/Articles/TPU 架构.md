---
title: "TPU 架构"
source: "https://docs.cloud.google.com/tpu/docs/system-architecture-tpu-vm?hl=zh-cn"
author:
published:
created: 2026-07-20
description:
tags:
  - "clippings"
provenance: external
---
张量处理单元 (TPU) 是 Google 设计的应用专用集成电路 (ASIC)，用于加速机器学习工作负载。Cloud TPU 是一种 Google Cloud 服务，可将 TPU 用作可扩缩资源。

TPU 旨在快速执行矩阵运算，因此非常适合机器学习工作负载。您可以使用 [PyTorch](https://docs.cloud.google.com/tpu/docs/tutorials/pytorch-pod?hl=zh-cn) 和 [JAX](https://jax.readthedocs.io/en/latest/) 等框架在 TPU 上运行机器学习工作负载。

## TPU 的工作原理是什么？

为了理解 TPU 的工作原理，我们不妨了解一下其他加速器如何应对训练机器学习模型的计算挑战。

### CPU 的工作方式

CPU 是一种基于 [冯·诺依曼结构](https://en.wikipedia.org/wiki/Von_Neumann_architecture) 的通用处理器。这意味着 CPU 与软件和内存协同工作，如下所示：

![CPU 工作方式图示](https://docs.cloud.google.com/static/tpu/docs/images/image6.gif?hl=zh-cn)

CPU 最大的优点是它们的灵活性。您可以在 CPU 上为许多不同类型的应用加载任何类型的软件。例如，您可以使用 CPU 在 PC 上进行文字处理、控制火箭发动机、处理银行交易或通过神经网络对图片进行分类。

对于每次计算，CPU 从内存加载值，对值执行计算，然后将结果存储回内存中。与计算速度相比，内存访问速度较慢，并可能会限制 CPU 的总吞吐量。这通常称为 [冯·诺依曼瓶颈](https://en.wikipedia.org/wiki/Von_Neumann_architecture#von_Neumann_bottleneck) 。

### GPU 的工作方式

为了提高吞吐量，GPU 在单个处理器中包含数千个 [算术逻辑单元](https://en.wikipedia.org/wiki/Arithmetic_logic_unit) (ALU)。现代 GPU 通常包含 2500 - 5000 个 ALU。大量的处理器意味着您可以同时执行数千次乘法和加法运算。

![GPU 工作方式图示](https://docs.cloud.google.com/static/tpu/docs/images/image2.gif?hl=zh-cn)

这种 GPU 架构非常适合并行处理大量运算（例如神经网络中的矩阵运算）的应用。实际上，在用于深度学习的典型训练工作负载上，GPU 的吞吐量可比 CPU 高出一个数量级。

不过，GPU 仍然是一种通用处理器，必须支持许多不同应用和软件。因此，GPU 与 CPU 存在同样的问题。对于数千个 ALU 中的每一次计算，GPU 都必须访问寄存器或共享内存，以读取运算对象以及存储中间计算结果。

### TPU 的工作方式

Google 设计了 Cloud TPU，它们是专门用于神经网络工作负载的矩阵处理器。TPU 不能运行文字处理程序、控制火箭引擎或执行银行交易，但它们可以很快地处理神经网络中使用的大量矩阵运算。

TPU 的主要任务是矩阵处理，这是乘法和累加运算的组合。TPU 包含数千个乘法累加器，这些累加器彼此直接连接以形成大型物理矩阵。这称为 [脉动阵列](https://en.wikipedia.org/wiki/Systolic_array) 架构。Cloud TPU v3 包含两个 128 x 128 ALU 的脉动阵列，位于单个处理器上。

TPU 主机将数据流式传输到馈入队列中。TPU 从馈入队列加载数据，并将其存储在 HBM 内存中。计算完成后，TPU 会将结果加载到馈出队列中。然后，TPU 主机从馈出队列读取结果并将其存储在主机的内存中。

为了执行矩阵运算，TPU 将 HBM 内存中的参数加载到矩阵乘法单元 (MXU) 中。

![图示：TPU 如何从内存加载参数](https://docs.cloud.google.com/static/tpu/docs/images/image4_5pfb45w.gif?hl=zh-cn)

然后，TPU 从内存加载数据。每次执行乘法运算时，系统都会将结果传递给下一个乘法累加器。输出是数据和参数之间所有乘法结果的总和。在矩阵乘法过程中，不需要访问内存。

![图示：TPU 如何从内存加载数据](https://docs.cloud.google.com/static/tpu/docs/images/image1_2pdcvle.gif?hl=zh-cn)

因此，TPU 可以在神经网络计算中实现高计算吞吐量。

## TPU 系统架构

以下各部分介绍了 TPU 系统的关键概念。如需详细了解常见的机器学习术语，请参阅 [机器学习术语表](https://developers.google.com/machine-learning/glossary?hl=zh-cn) 。

如果您刚接触 Cloud TPU，请参阅 [TPU 文档首页](https://cloud.google.com/tpu/docs?hl=zh-cn) 。

### TPU 芯片

一个 TPU 芯片包含一个或多个 TensorCore。TensorCore 的数量取决于 TPU 芯片的版本。每个 TensorCore 由一个或多个矩阵乘法单元 (MXU)、一个向量单元和一个标量单元组成。如需详细了解 TensorCore，请参阅 [用于训练深度神经网络的领域专用超级计算机](https://dl.acm.org/doi/pdf/10.1145/3360307) 。

MXU 由 [脉动阵列](https://en.wikipedia.org/wiki/Systolic_array) 中的 256 x 256（TPU v6e 和 TPU7x \[[预览版](https://cloud.google.com/products?hl=zh-cn#product-launch-stages)\]）或 128 x 128（v6e 之前的 TPU 版本）乘法累加器组成。MXU 在 TensorCore 中提供大部分计算能力。每个 MXU 能够在每个周期中执行 16K 乘法累加运算。所有乘法都采用 [bfloat16](https://en.wikipedia.org/wiki/Bfloat16_floating-point_format) 输入，但所有累加运算均采用 FP32 数值格式。

向量单元用于常规计算，例如激活和 softmax。标量单元用于控制流、计算内存地址和执行其他维护操作。

### TPU Pod

TPU Pod 是一组连续的 TPU，通过专用网络组合在一起。TPU Pod 中的 TPU 芯片数量取决于 TPU 版本。

### 切片

切片是一组芯片，这些芯片都位于同一 TPU Pod 中，并通过高速芯片间互连 (ICI) 连接。切片通过芯片或 TensorCore 来描述，具体取决于 TPU 版本。

芯片形状和芯片拓扑也称为切片形状。

### 多切片与单切片

多切片是一组切片，可将 TPU 连接扩展到芯片间互连 (ICI) 连接之外，并利用数据中心网络 (DCN) 传送切片之外的数据。每个切片中的数据仍由 ICI 传送。借助这种混合连接，多切片可实现切片之间的并行性，并可让您为单个作业使用比单个切片可容纳的更多 TPU 核心。

TPU 可用于在单个切片或多个切片上运行作业。如需了解详情，请参阅 [多切片简介](https://docs.cloud.google.com/tpu/docs/multislice-introduction?hl=zh-cn) 。

### TPU 立方体

互连 TPU 芯片的 4x4x4 拓扑。这仅适用于 3D 拓扑（从 TPU v4 开始）。

### SparseCore

SparseCore 是数据流处理器，可利用稀疏运算来加速模型。主要应用场景是加速高度依赖嵌入的推荐模型。v5p 和 TPU7x（ [预览版](https://cloud.google.com/products?hl=zh-cn#product-launch-stages) ）的每个芯片包含四个 SparseCore，v6e 的每个芯片包含两个 SparseCore。如需深入了解如何使用 SparseCore，请参阅 [深入探究适用于大型嵌入模型 (LEM) 的 SparseCore](https://openxla.org/xla/sparsecore?hl=zh-cn) 。您可以使用 XLA 标志控制 XLA 编译器使用 SparseCore 的方式。如需了解详情，请参阅： [TPU XLA 标志](https://openxla.org/xla/flags_guidance?hl=zh-cn#tpu_xla_flags) 。

### Cloud TPU ICI 弹性

ICI 弹性有助于提高光学链路和光学电路开关 (OCS) 的容错能力，用于在 [立方体](#cube) 之间连接 TPU。（立方体内的 ICI 连接使用不受影响的铜链路）。借助 ICI 弹性，ICI 连接可绕过 OCS 和光学 ICI 故障。因此，虽然 ICI 性能会暂时下降，但 TPU 切片的调度可用性会得到提高。

对于 Cloud TPU v4、v5p 和 TPU7x（ [预览版](https://cloud.google.com/products?hl=zh-cn#product-launch-stages) ），如果切片大小为一个立方体或更大，ICI 弹性默认处于启用状态，例如：

- 指定加速器类型时为 v5p-128
- 指定加速器配置时为 4x4x4

### TPU 版本

TPU 芯片的确切架构取决于您使用的 TPU 版本。每个 TPU 版本还支持不同的切片大小和配置。如需详细了解系统架构和支持的配置，请参阅以下页面：

- [TPU7x (Ironwood)](https://docs.cloud.google.com/tpu/docs/tpu7x?hl=zh-cn) （ [预览版](https://cloud.google.com/products?hl=zh-cn#product-launch-stages) ）
- [TPU v6e](https://docs.cloud.google.com/tpu/docs/v6e?hl=zh-cn)
- [TPU v5p](https://docs.cloud.google.com/tpu/docs/v5p?hl=zh-cn)
- [TPU v5e](https://docs.cloud.google.com/tpu/docs/v5e?hl=zh-cn)
- [TPU v4](https://docs.cloud.google.com/tpu/docs/v4?hl=zh-cn)
- [TPU v3](https://docs.cloud.google.com/tpu/docs/v3?hl=zh-cn)
- [TPU v2](https://docs.cloud.google.com/tpu/docs/v2?hl=zh-cn)

## TPU 云架构

Google Cloud 可通过 TPU 虚拟机将 TPU 用作计算资源。您可以直接将 TPU VM 用于工作负载，也可以通过 Google Kubernetes Engine 或 Vertex AI 使用 TPU VM。以下部分介绍了 TPU 云架构的关键组成部分。

### TPU 虚拟机架构

借助 TPU 虚拟机架构，您可以使用 SSH 直接连接到与 TPU 设备物理连接的虚拟机。TPU 虚拟机（也称为工作器）是指运行 Linux 且可以访问底层 TPU 的虚拟机。您拥有虚拟机的根访问权限，因此可以运行任意代码。您可以访问编译器和运行时调试日志及错误消息。

![TPU 虚拟机架构](https://docs.cloud.google.com/static/tpu/docs/images/tpu-vm-architecture.png?hl=zh-cn)

### 单主机、多主机和子主机

TPU 主机是在连接到 TPU 硬件的物理计算机上运行的虚拟机。TPU 工作负载可以使用一个或多个主机。

单主机工作负载仅限于一个 TPU 虚拟机。多主机工作负载会在多个 TPU 虚拟机之间分布训练。子主机工作负载不会使用 TPU 虚拟机上的所有芯片。

### TPU 节点架构（已弃用）

TPU 节点架构包含一个通过 gRPC 与 TPU 主机通信的用户虚拟机。使用此架构时，您无法直接访问 TPU 主机，因此很难调试训练和 TPU 错误。

![TPU 节点架构](https://docs.cloud.google.com/static/tpu/docs/images/tpu-node-architecture.png?hl=zh-cn)

### 从 TPU 节点架构迁移到 TPU 虚拟机架构

如果您的 TPU 使用 TPU 节点架构，请按照以下步骤识别、删除这些 TPU，并将其重新预配为 TPU 虚拟机。

1. 前往 TPU 页面：
	[前往 TPU](https://console.cloud.google.com/compute/tpus?hl=zh-cn)
	在 **架构** 标题下找到您的 TPU 及其架构。如果架构是“TPU 虚拟机”，则无需执行任何操作。如果架构是“TPU 节点”，则需要删除并重新预配 TPU。
2. 删除并重新预配 TPU。
	如需了解如何 [删除](https://docs.cloud.google.com/tpu/docs/managing-tpus-tpu-vm?hl=zh-cn#tpu-delete) 和 [重新预配](https://docs.cloud.google.com/tpu/docs/managing-tpus-tpu-vm?hl=zh-cn#provision-tpu) TPU，请参阅 [管理 TPU](https://docs.cloud.google.com/tpu/docs/managing-tpus-tpu-vm?hl=zh-cn) 。

## 后续步骤

- [使用入门指南](https://docs.cloud.google.com/tpu/docs/quick-starts?hl=zh-cn)
- [教程](https://docs.cloud.google.com/tpu/docs/tutorials?hl=zh-cn)

## AI 閹芥顩n
该笔记摘录 Google Cloud 文档，介绍 TPU 通过面向矩阵运算的专用架构提升机器学习工作负载吞吐量，并与 CPU、GPU 的计算及内存访问模式进行对比。


<!-- orphan-cleanup: no MOC found, tagged -->
