---
direction: both
category: 项目
tags: [FPGA, CNN加速器, DE1-SoC, 卷积神经网络, 并行计算]
summary: "康奈尔大学FPGA课程项目：可参数化卷积加速器设计"
quality: medium
processed: 2026-08-11 21:18
---
---
title: "国外大学生都用FPGA做什么项目（二十一）"
source: "https://mp.weixin.qq.com/s/x11HWflEw4Eeum8Cbyu3_Q"
author:
  - "[[碎碎思]]"
published:
created: 2026-07-30
description:
tags:
  - "clippings"
provenance: external
---
碎碎思 OpenFPGA *2026年7月30日 08:30*

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBhvhXHTsmnWtDBWlY718OZcgwLssBl1w2BmTN04Jn9fnvsp9FfCc2nABViahEos6iaJssBRFIjXhBz5xMW96KjIVBicMHtWw9Pib4U/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

## 小引：

据我了解，目前国内很多大学是没有开设FPGA相关课程的，所以很多同学都是自学，但是自学需要一定的目标和项目，今天我们就去看看常春藤盟校Cornell University 康奈尔大学开设的FPGA项目课程，大部分课程是有源码的，而且和国内使用习惯类似都是Verilog开发，还是很有借鉴意义的。

## 项目链接

> https://people.ece.cornell.edu/land/courses/ece5760/FinalProjects/

## 项目介绍

2024年春季 开发板：CycloneV DE1-SoC

## 可参数化卷积加速器设计

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBjPvc8dmkgE1bY8rJrsKeBthKwHLk4lkqHHNiby5nicbctayFsyicAmH9vPaT5PicalBa5wsLRntvU1r9U2cgrgRtf97iafCsPrfepI/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1)

### 概述

卷积神经网络（CNN）广泛应用于图像处理领域，例如分类和目标识别。许多此类应用都采用 CNN 作为骨干网络，其中多个卷积层堆叠在一起。有时，即使只使用单个卷积层也能提取图像的特定信息，例如颜色、纹理、边缘等。FPGA 强大的并行计算能力和相对较低的功耗使其成为部署 CNN 的热门平台。因此，项目并非在 FPGA 上针对特定应用实现完整的 CNN 模型，而是专注于实现一种高度并行化的微架构，该微架构专为卷积层的推理而设计，并且可以配置 CNN 层的一些相关参数。在 DE1-Soc 开发板上，FPGA 负责 CNN 推理，而 HPS 则负责控制和调度 FPGA 上的推理过程，并将输入特征图和权重馈送到 FPGA。

### 背景数学

如图 1 所示，典型的 CNN 层主要由卷积运算、激活函数和池化运算组成。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBia1NpTspqp6yDNXnIhSNnLjtToFbPt45z0SYbTzricLIsQaTqw8uKg4aLuV9PXmgSIySAaqkZia5icp0EXG1rvpmMsb7EhHUNtzFw/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=2)

图 1：典型的卷积层结构 \[1\]

如图 2 所示，卷积运算是 CNN 层中最关键的步骤。输出特征图 O *O 的大小与单个卷积层的多个参数相关，包括输入通道数 N、输出通道数 M、输入特征图大小 L* L、卷积核大小 K\*K、填充数 P 和卷积步长 S。基于以上表示，卷积层遵循以下公式：

在许多情况下，卷积核的大小为 3\*3，卷积步长为 1，并且 P 将被设置为 1，以保持输出特征图的大小不变。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_gif/TsrAtX2ibWBiaKEzeBE1ibnmaUKc0LeGOeEbl0w53s7PEJnLpl8CVSsaMs65Zr6Vyy3GcRGbYib2CLUoL3L0wUuoic03fO2Htmib9MJMEPCVmPSbM/640?wx_fmt=gif&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=4)

图 2：卷积运算 \[2\]

池化操作主要有两种方法：最大池化和平均池化。最大池化比平均池化应用更为广泛，它能降低特征图的空间维度，使网络对输入数据的微小平移更具不变性。在最大池化中，一个滑动窗口（或池化窗口）在输入特征图上移动，窗口的每个位置都取窗口内的最大值作为输出。如图3所示，池化操作实际上可以看作是步长为2且无填充的卷积操作的特例，因此输出特征图的尺寸会缩小一半。

![图片](https://mmbiz.qpic.cn/mmbiz_gif/TsrAtX2ibWBial40DFgDam3329WcQgakicq0aicKyZvaoicx6TRIEsib4nB75jD5xKq9ibgBQ7Lk90xR2BXJFUIcuRc6z7p09cNnuhCiad1sicrW0ldg/640?wx_fmt=gif&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=5)

图 3：最大池化操作 \[3\]

神经网络中的激活函数是一个非线性函数，应用于每个神经元的输出。激活函数的主要目的是为模型引入非线性，使网络能够学习和建模数据中的复杂模式。修正线性单元（ReLU）是神经网络中最常用的激活函数之一，尤其是在卷积神经网络（CNN）中。由于其简单易用，ReLU 在嵌入式系统的 CNN 部署中也非常流行。ReLU 函数的定义如下：

在FPGA上实现CNN层时，需要引入一些额外的步骤，例如量化模块。在该模块中，将数据表示从32位浮点数转换为8位整数，并调整特征图的像素，以在保持较高精度的同时降低资源占用。具体来说，我们实现了训练后静态量化（PTSQ）。如图4所示，通过缩放和平移，PTSQ可以将原始数据范围映射到(0, 255)，从而降低数据表示所需的资源，使在FPGA上部署CNN更加可行。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBhPTzKicGGCxfEyKDKdAwjvTicv2IeqiaI1LI7JRn4GFWxRFOcMsVdDgiaXZzJ8BAI60FPT4r7jLs0pV6oicF43BT870ngXtsRwyjjE/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=7)

图 4：PTSQ \[4\]

### 逻辑结构

#### 平行结构

图 5 展示了高层设计架构。首先，如前所述，FPGA 非常适合并行计算，因此制定一个详细定义并行策略的合适方案至关重要。考虑到 DE1-SoC 板的资源有限，特别是block存储器和 DSP 的资源，无法像预期那样大幅提高并行度。因此，决定在卷积核内并行化 9 次乘法运算和 8 个输入通道，这意味着在一个周期内可以实现的乘加运算 (MAC) 次数为 2 *8* 9 = 144 次。

#### ARM

对于 ARM 端，HPS 将按顺序发送 8 个通道的相应输入特征图和权重，然后控制加速器开始 CNN 的推理；当一个输出特征图完成后，加速器将通过高级可扩展接口 (AXI) 将相应的输出特征图发送回 HPS。

#### 加速器设计与权衡

对于FPGA架构，有四种不同的缓冲区用于存储中间数据，包括：

- IFM\_Buffer：存储8个输入通道的输入特征图。
- Weight\_Buffer：存储8个输入通道的权重。
- ACC\_Buffer：存储一个输出通道的累加数据。
- OFM\_Buffer：存储一个输出通道的输出特征图。

对于加速器的主干网，首先，加速器会根据HPS端发送的读取地址访问IFM\_Buffer。然后，访问到的数据会被加载到一个长度为当前层填充后的输入特征图两倍的行缓冲区中，加载前会从中减去输入数据的量化零点。当行缓冲区完成预热阶段后，会从权重缓冲区中取出相应的3×3权重窗口，与行缓冲区生成的3×3 IFM窗口进行乘加运算。最后，将8个输入通道的MAC结果相加，这里使用了两个加法器树。此时，8个输入通道的卷积结果将临时存储在ACC\_Buffer中，待接下来的8个输入通道完成卷积后，才会从中取出。在“累加”阶段，只有当最后一组输入通道完成卷积后，累加结果才有效。当累加结果有效时，经过量化和ReLU模块处理后的数据才能写入OFM\_Buffer。但是，如果当前层需要进行最大池化操作，加速器会在写入OFM\_Buffer之前进入“池化层”。因此，这里使用了一个2对1的多路复用器，根据是否执行池化操作来选择写入OFM\_Buffer的数据。最后，当一个输出通道的所有数据都写入OFM\_Buffer后，加速器会将该输出通道的输出特征图发送回HPS，用于下一层的推理。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBgb2o9foU60J8bz7PHAkCchQEmx8j1wINmQs9U0vshNb8oF6TicicyicNNLjrZNwSI0VKFJKGb1WkMuZvYlUEgwz2UcEmq7YuXwyw/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=8)

图 5：高级系统架构

### 硬件设计

#### 控制逻辑

每个完整的卷积层包含五个连续阶段，由 ARM 内核提供输入通道信息和相关参数启动，最终将输出结果发送回 ARM 内核：RECV、LOAD、CALC、WRITE 和 SEND。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBhfwU8F1BkCzKm92FcnqGhJYPTtHA3tnw3Q1fjCSZAibMw1VG78RatrEftwu6NXlWTia0QHdwtM22Q3EkwOibwSWjflxKqOIRPNjg/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=9)

图 6：控制逻辑

该图展示了整个 Modelsim 仿真过程。在本测试平台中，将输入通道数设置为 16，这意味着转换层会重复执行一次，因为它能够同时处理 8 个通道。如状态变量所示，该过程从 RECV（阶段 1）开始，然后进入 LOAD（阶段 2），最后进入 CALC（阶段 3）。由于有 16 个输入通道，转换阶段会重复执行。最后，该过程进入 WRITE（阶段 4），所有数据都会被写入 ofm\_Buffer。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBjYJ493AZ0nh2mWvB1mYpmicHgCibxUo0DicWV8uSzxqkic9lKSVW3MapAaicYuk3dUFKfL9Coz9drvJ2VtEgUL5z7biatmCD1GicaWoo/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=10)

图 7：Modelsim 整体仿真

#### RECV

- 通过 AXI 通道从 ARM 内核接收输入特征图 (IFM) 和权重数据流。
- 将数据和权重分别存储在 IFM\_Buffer 和 Weight\_Buffer 中。
- 由于我们只有一个 64 位数据通路，RECV 控制模块会先写入 IFM\_Buffer，然后再写入 Weight\_Buffer。我们从 ARM 内核接收一个输入信号，用于告知 RECV 控制模块当前正在写入 IFM\_Buffer 还是 Weight\_Buffer 的数据。
- write\_enable、write\_address 和 write\_data 信号直接来自 ARM 内核。

Modelsim（阶段 1）：在此阶段，测试平台持续向 ifm\_buffer 写入数据，导致 ifm\_address\_write 递增，直至达到 899，表示所有 ifm 数据已写入 ifm\_buffer。随后，权重数据被写入权重缓冲区。如图所示，当 ifm\_address\_write 达到 899 后，weight\_address\_write 开始计数。当收到来自测试平台的 rec\_done 信号时，该阶段转换。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBg4cibEVpYD4oeuibhLNytS37jtef0xPaIEsn7GjG5DvE9bMDDicabz2QLfB12luwyxLtyMOHWTokGYw6phT4ic1E5q8fo9kzGSo9o/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=11)

图 8：第一阶段 Modelsim 仿真

#### 加载

- 将数据预加载到 3 *3 的 Linbuffer 缓冲区中，待 Linbuffer 完成预热并产生正确的 3* 3 窗口输出后，再将其传输到下一阶段。
- 由于 Linbuffer 作为数据流工作，LOAD 控制模块不会对数据通路造成任何干扰。它仅判断当前 3\*3 窗口的数据是否有效，并根据缓冲区计数器的值决定是否进入下一阶段。

Modelsim（第二阶段）：当 linebuf\_load\_done 信号置高时，表示窗口缓冲区已准备好接收转换层输入。因此，linebuffer\_load\_count 递增至 65，其中包含了缓冲区预热时间和流水线转换延迟。总耗时计算公式为：Time\_taken = size\_fm\_in \* 2 + 3。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBjHtRRLZUGGfuoEXUaIlyxQ4Nzy0Or48ibpYDxicHVnEHMiczdycd7UDUDDcziacONhrA71Lp1YiaRRenhSb8VUXn8n5Y3WMXD27VFE/640?wx_fmt=webp&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=12)

图 9：第二阶段 Modelsim 仿真

#### 计算

- 执行卷积计算。将当前 8 个通道的卷积结果临时存储在 ACC\_buffer 中。
- 检查所有输入通道是否已处理完毕；如果已处理完毕，则进入 WRITE 阶段；否则，返回 RECV 阶段以接收接下来的 8 个输入通道。
- CALC 控制模块根据此内部计数器向 ACC\_Buffer 发送关于 write\_enable、write\_address 和 write\_data 的控制信号。

Modelsim（阶段 3）：由于转换操作，数据会延迟几个周期，之后才会写入 acc\_buffer。但是，由于每行包含 28 个数据点，转换层输出的数据每 28 个周期会失效两个周期。失效原因将在下文的 linebuffer 3x3 部分进行解释。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBjNiaZA2OuBX4C7RwGPEl16NgUWZbS3Ol84U7O3UqrsOq6tPiaXej66vVZzgiawWVhCbib3Kbazuo8RZK7DCo2ruAPxrp4bHFxFeNY/640?wx_fmt=webp&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=13)

图 10：第三阶段 Modelsim 仿真

#### WRITE

- 确定此层是否需要池化。如果需要，则执行池化操作；否则，将数据直接写入 OFM\_Buffer。
- 池化操作还需要一个 2 *2 的行缓冲区，因此需要等待一段时间，直到行缓冲区预热完毕并能够生成正确的 2* 2 窗口。
- 池化操作完成后，将数据写回 OFM\_Buffer。
- 量化、ReLU 和池化的数据路径不受 WRITE 控制模块的控制，它像流水线一样工作，始终有数据流在其中流动。
- WRITE 控制模块负责告知 FPGA 是否需要执行池化操作，以及何时所有正确的数据都已写入 OFM\_Buffer。

模型模拟（阶段 4）：在此阶段开始时，所有输入通道都在执行计算，并将数据写入 acc\_buffer。经过流水线（包括量化层和 ReLU 层）的 write\_state\_count 几个周期的延迟后，我们开始将数据写入 ofm\_buffer。与 3x3 行缓冲区类似，在池化操作期间，当填充下一个 2x2 窗口时，2x2 窗口缓冲区的输出将失效。这就是为什么我们使用 linbuffer\_row 和 linbuffer\_col 来跟踪行缓冲区的位置。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBia2UPhUfpEVW0cIeicSayMDn7tR2Z1aSPHst0ZibtdcJEuIBdiaTToiaFo2TmSrYytu5Dicw9hmoEWgsJXApK7P4EpwObrcbZykXDfQ/640?wx_fmt=webp&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=14)

图 11：第四阶段 Modelsim 仿真

#### 发送

- 将数据传输回 ARM 内核。此操作完成后，一个完整的卷积层就完成了。
- 重置到 RECV 阶段，以处理来自下一层的信息。

#### 3×3 行缓冲区卷积

为什么 Linbuffer 是 3\*3？

在图像处理中，3x3窗口行缓冲区临时存储三行像素数据，以便高效访问每个像素周围3x3的邻域。它使用两个行缓冲区来保存最后两行数据，并使用移位寄存器来处理当前行。每处理完一个像素，窗口就会向右移动，通过更新移位寄存器来存储该行中的下一个像素。一旦某一行数据被完全处理，行缓冲区就会更新以包含下一行数据，从而保持3x3窗口，直到整幅图像处理完毕。这种设置对于卷积滤波和特征检测等操作至关重要。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBj5Me3z0L3tKZSQCLgLLVk8vH5icreQbo1hYMtxnNQjPPnnBoP47M70qoaQyVEXdIqY11bdcGDsyFM0PZ4PUHskuzkHwTUOHImw/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=15)

图 12：3\*3 行缓冲区 \[5\]

#### 控制逻辑是如何工作的？

图 13 左侧展示了一幅 7x8 像素的图像，窗口大小为 3x3。左侧窗口演示了如何将第一条数据加载到行缓冲区，而右侧窗口则展示了如何将最后一位数据写入行缓冲区。此时，由于缓冲区尚未被图像数据填充，因此窗口缓冲区的输出无效。

如图 13 右侧所示，持续填充行缓冲区，直至其完全填满。此时，填充行缓冲区需要 2 \* 行大小 + 3 个周期。现在，窗口缓冲区已生效，可以向下一个转换层输出数据。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBiaB4rRfAIPOfyW8LY5DmJOFfuf4OZsJWpDMib9BibuzEXALuOhsiaNjYsqkWEia8DhbVKgNI4C1VxS37hPP0WN4vGXmgPbRwhJbichI/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=16)

图 13：3\*3 线缓冲区工作流程：阶段 1（左），阶段 2（右）

然而，当行缓冲区填满后，每行到达末尾会发生什么？窗口缓冲区在后续循环中是否仍然有效？如图 14 所示，蓝色窗口内的数据仍然有效。但是，随着继续向行缓冲区插入数据，窗口缓冲区在接下来的两个循环中失效，如图中红色和绿色方框所示。此示例表明，将数据加载到缓冲区后，每行到达末尾时，窗口缓冲区就会失效。这可以通过以下方式计算：

```
if(((linbuffer_count + 2) % size_row == 0) || ((linbuffer_count + 1) % size_row == 0)) begin
    linebuffer_valid <= 0;
```

如果 linbuffer\_countof 不是 row\_size 及其下一个周期的倍数，则认为行缓冲区输出有效。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBjOAAUup3PIAEMkOt6GMNjzwE6gK2XHvniatvueyzA2ETYJibGQo6c24x0QKPibD2E5IicTU0EB2l7ibeicAQIlZZzvnydyZ0doJricgE/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=17)

图 14：填充的行缓冲区

#### 2\*2 行缓冲区最大轮询

最大轮询在特征图的 2x2 网格上进行操作，并从中选择该网格中的最大值。此过程降低了输入的空间维度，有助于对数据进行下采样，从而提高模型的计算效率，同时保留重要特征。

2x2 行缓冲区的运行方式与 3x3 行缓冲区类似，但它不会输出用于转换操作的有效窗口缓冲区，而是将蓝色 2x2 窗口向右移动，到达红色窗口的位置，如图 15(a) 所示。步长设置为 2，且缓冲区每个时钟周期捕获一个数据元素，则需要两个时钟周期才能产生下一个有效输出。完成一行有效的 2x2 窗口输出后，写入行缓冲区的下一行数据将变为无效，如图 15(b) 所示。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBghCkr3fRzn9Eiay5nSickLCNjpyka3XXwljcsqvc26EwD7JG6t6efBwBicqZqOD8sMTLEeKTIFN6UYPAiaPQfXbamXKUadBaSLh80/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=18)

图 15：（a）2x2 行缓冲区工作流程；（b）无效状态

如图 16 所示，窗口缓冲区必须等待接下来的两行数据完全写入缓冲区后才能输出有效数据。图中绿色窗口表示红色窗口之后数据再次有效的时间点。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBiayn9oXegwKIWH6Fic5dSGQ5l1A484G0ykcuXmMjV122FKibicLlqqDLpVSZbCZDXtqsya3fyfpwg9XUJeLDiciabX9hZPX3E5jbF2U/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=19)

图 16：2x2 行缓冲区工作流程问题

为了解决这个问题并控制窗口缓冲区何时生效，可以实现两个计数器：行计数器 (row\_counter) 和列计数器 (column\_counter)。当行缓冲区完全加载后，这两个计数器将同时启动。列计数器会在 0 和 1 之间循环计数。同时，行计数器会在处理完一行数据后切换其值。如图 17 所示，只有当行计数器和列计数器同时达到 1 时，窗口缓冲区才会输出有效数据。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBgafv0BSdOEsMep4wkRyIibicv6fX2F2H9u2aHntpBXL5yjRA2x3H5O6wtGualgSNCUAGm8PMaH3Lqg3OuqHia2B0PuaBlGujwkFI/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=20)

图 17：2x2 行缓冲区工作流程解决方案

### 软件设计

在 HPS（硬处理器系统）方面，实现了每个卷积层的输入特征图的预处理和传输、控制信号的生成和传输，以及 FPGA 输出特征图的接收和存储。

#### 预处理

在Linux系统下使用C语言实现了PNG输入图像的灰度处理，并将数据存储在IFM的4D数组中。该4D数组的结构由组、通道以及每个通道特征图的x、y坐标构成。通道元素的大小为8，因为这是HPS端在输入通道维度上实现的最大并行度。组的计算方法是用输入通道的大小除以最大通道数，即8。我们还负责将预训练的权重文本文件读取并存储到4D权重数组中。该数组的结构与IFM数组相同。此外，由于对于受限于特定数组大小的FPGA程序来说，填充IFM数组的过程较为繁琐，因此我们使用ARM架构来处理IFM数组的填充。由于FPGA程序是为8通道并行输入设计的，需要以8通道为一组传输数据（如图18所示），因此HPS还实现了IFM数组和权重4D数组的数据拼接。由于 PIO 端口的最大位宽为 32 位，我们使用了两个完整的 AXI PIO 端口来传输输入数据。此外，我们还利用了一些轻量级 AXI 总线上的 PIO 端口来传输相应的控制信号，包括指示当前传输的是 IFM 数据还是权重数据、IFM 缓冲区的地址、权重缓冲区的地址、IFM 和权重数据 8 个通道全部传输完毕等。实际测量表明，当完整的 AXI 总线空闲时，无需延迟，FPGA 即可有效接收所有数据。因此，没有设计双向握手协议。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBjUBSBLnGW9Rlnqkiaa9lIGic5cT2BO34MgnHonKJeKYD5WFC9DxMKmIBcDgJDZefsUnG01v50pCZxzzicdlwGibpVPia8Z6ibE0SmXc/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=21)

图 18：HPS 输出结构

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBh6p4o1tgibEuStvghibI3AW3x4qhecWUm8aWWAqNrh6KEJiaqC5rT4HS2yOD2e6K0ibCaIj7vWdAJHKuBLqicQMtAuZ1Ubzv6icCAGg/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=22)

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBgKsGY1ibj66BTBje1ic4sWRGWxImDQ77b8GD5DIPlJwLjXDPfwzFZah6LyQFC0Md1Dfye21r0MibAEPvaick0YjPSabDriaux1CG78/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=23)

图 19：设计中的 QSYS

#### 可用性

为了增强可用性和可配置性，在 ARM 端实现了参数配置，包括每个卷积层的输入通道数、输入特征图像的大小、输出通道数、是否执行最大池化、填充大小、量化输入和输出零点以及阈值。这些参数将通过轻量级 AXI 总线上的 PIO 传输到 FPGA。用户可以在程序启动时通过命令行输入配置这些设置。

### 设计结果

该项目开发了一种灵活且可参数化的卷积加速器，易于扩展以处理复杂的图像处理任务。实现了一个卷积层，其输入通道数和输入特征图大小均可修改，并可选配池化层和动态阈值调整功能。

为了展示加速器的参数化功能，展示了一个具有 16 个输入通道的配置，每个通道的大小为 28x28。如下所述，对该卷积层应用了图像融合、边缘检测或动态阈值处理等特定处理任务：

- 静态场景：

输入包含两组共 8 个通道。第一组的第一个通道显示左侧太极图，第二组的第一个通道显示右侧太极图，如图 20 所示。其余通道均为黑色。输出包括一个显示合并图像的通道和一个显示边缘检测结果的通道。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBhqzu7ftNibEhmXO6lQpBBrxEyUlLmicSw3TwicJNRNVOEQWMCPBO9gaoJ0hlS7YhWdCPdo9oRg9X2BZ4t1KH7ahnibyk9SCeTQH0o/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=24)

图 20：静态场景结果

  - 动态场景：

此设置与静态场景在输入和输出方面完全相同，但由于输入阈值会变化，因此它是动态的。这展示了加速器在调整阈值以优化边缘检测方面的灵活性。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBjGB31oFlL7Jg6BubKxqnFGvicEMdcdjFjSXoSCibEbqB1dkibhaGjl1GdrY1sLSsOwoL28SW8rxWmk8yDkTJRL4wllOomI6KmIwg/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=25)

图 21：动态场景结果

- 池化场景：

类似于静态场景，但增加了在图像处理序列中实现池化的功能。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBjKH8donckDLAU5uPRClnXa6ZdLbNhDqfh5Nozs2WK0hDmpuYBtAPFEN5rqhwiafBmUOsTf6Wqkw8vbjMavcnbSuicelzCAibmvmQ/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=26)

图 22：池化场景结果

下面 ModelSim 演示显示了 OFM 缓冲区的内容，然后根据用户使用情况，将其作为下一层的 IFM 传输到 HPS。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBjL7tRsuzgrmHicdmyg9GEEd5Ve4EuoIjj82d0ZSzK0oK1JkBiaeZrjZFUVmM161km2ZM4QuOgib8h70bIujCwcYqvgElQJLPVyGY/640?wx_fmt=webp&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=27)

图 23：OFM 缓冲区中的数据

用户可以通过命令行输入控制阈值变化速率，从而帮助找到合适的边缘检测阈值。程序首次运行时，用户还可以输入图像和其他控制参数。此外，只需稍作修改 C 代码，即可连接多个卷积层，构建多层卷积神经网络 (CNN)。该加速器具有高度可参数化的特性，能够适应各种处理需求和环境，并且易于扩展新功能。

### 结论

在这个项目中，成功实现了一种高度并行化和可参数化的微架构，专门用于卷积神经网络（CNN）层的推理。在上述测试用例中，展示了如何设置单个卷积层的相关参数，以及其高度的功能可扩展性。

### 项目链接

> https://people.ece.cornell.edu/land/courses/ece5760/FinalProjects/s2024/yx623\_jz2275\_sl2874\_NEW/yx623\_jz2275\_sl2874/yx623\_jz2275\_sl2874\_main.html

### 代码链接

> https://github.com/yibinpeter/ECE5760-Final-Project.git

### 视频链接

> https://youtu.be/PFNU4NQrzBU?si=3F8yNN8THKA86uhD

## Chirikov 标准映射

### 介绍

在 DE1-SoC 上实现了标准映射（也称为 Chirikov 标准映射）的求解器。标准映射由 Boris Chirikov 于 1969 年首次提出 \[1\]，它是一个离散时间哈密顿动力系统，由以下方程组描述：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBiaPXqaZahytXtZVGS6L12NmR1xEUe6ibK2mD29LejiaSkX5tbW9ibU3YX9cmxTHZy5NkZBICSqxqcvE8TPQibwTLlMnOE68pcvm80M/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=28)

其中方程取模 2π，使得 2π×2π 正方形上的所有输入都映射到同一区域。变量 x 和 p 分别表示系统的角位置和角动量（因此有时 x 会被 θ 代替）。

标准映射可用于描述受击转子这一物理系统；其方程刻画的是一根无重力作用、可自由旋转的摆，该摆会周期性受到大小为K的瞬时冲量。该系统的相空间呈柱面结构，对坐标x取模运算对应摆锤旋转越过最高点后循环折返。此相空间在动量维度上同样具有周期性，因此只需考察动量p的取值区间(\[0,2\\pi))；基于上述性质，我们可将该映射的相空间视作环面。

随着 K 值的增大，轨道开始瓦解，并“混沌地”填充整个空间区域。在本项目中，使用可综合的 Verilog 语言创建了一个用于标准映射的迭代器。然后，使用一个交互式的点击式 HPS 小程序渲染标准映射，类似于 James Meiss 的 StdMap 应用程序 \[3\]。我们还编写了一个 C 程序来遍历 K 值并导出每个相图。下图是整理的 K 值在 \[0,5\] 范围内以 0.025 为增量的标准映射渲染结果：

图 1：标准地图（鼠标悬停激活）

尽管该映射是混沌的，但由于其保面积特性（即，每个唯一的 (xn, pn ) 对都有一个唯一的 (xn+1, pn+1 ) 输出），因此它是可逆的。求解前一个时间步即可得到逆映射（注意，这不需要任何除法运算）：

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBj8ibc74bzI9NbEjo4tRHMbmMia67ppBaxpd3GW8axwqsNicbp3JYhMCkajTL9IFicxpCTOs5T1NxiaNic0dXBebGcNQKkYXJalDrPWQ/640?wx_fmt=webp&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=29)

这种可逆性使我们能够利用标准映射进行加密/解密。对于任意 K 值，可以通过将每个像素映射到新位置来加密图像 \[4\]。映射对 K 的依赖性（以及 K 值较大时的混沌特性）为我们提供了一个二值密钥：K 和迭代次数 n。在项目的第三部分也是最后一部分中，实现了 320x320 像素 8 位彩色图像的加密和解密机制，并用它来加密和解密 Bruce Land 的图像（此处 K = 5，n = 1）：

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBhDnDqicUL5ThBS2pmjibNHf19PVIkeDMW7aN5Gs1AO4GWltGKmNctkYuOiaASep5nricH8JfaT3sWKVZh9OG4T6Lwl3LgafUXDkQM/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=30)

图2：原版布鲁斯

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBiab55GWcwHDmMhHaAtvujx8fPpUreDs7Jcth6sicsMcer9WE7CfnPVDr5OPhzQV3iaoHOK3Jk8WHIibtkq4Z4ZiajH7haqoNX3aTKw/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=31)

图 3：加密的布鲁斯

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBgq23zt0w7ibiaIRzR0RsoY1O5ez5xM8CLFLVNAvh1OFWwVhY2A8jD9MljhV7tibEEq2Vras15sv1fbHgP2oar6l1FQBruXaABwfQ/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=32)

图 4：解密后的布鲁斯

### 高层设计

迭代器位于 FPGA 上，因为这种计算可以轻松映射到状态机。通过提供 xn和 pn 来设置迭代器的初始条件，插入一个 K，并允许它运行 n 次迭代。顶层的第二个状态机连接到一个 640x480 像素、8 位宽的 M10k 块，用于 VGA 内存。该状态机控制迭代器并按指示写入内存。在我们的加密演示中，实现了一个用于标准映射逆运算的迭代器，将内存划分为 3 个独立的 320x320 M10k 块，分别用于左帧缓冲区、 右帧缓冲区和临时帧缓冲区，并修改状态机以允许将某些缓冲区复制到其他缓冲区。 VGA 屏幕驱动程序由 V. Hunter Adams \[5\] 提供。

使用 HPS（ARM Cortex-A9 硬 IP）通过 PIO 通道来控制顶层状态机。为三个演示分别编写了专用的 C 程序。前两个程序允许实时选择输入坐标，选择 VGA 内存块的写入数据（8 位颜色），并触发迭代器。第一个程序包含一个用于轮询鼠标输入的线程，允许用户为给定的 K 值选择轨道。第二个程序通过选择 100 个随机点并将数据从转储 PIO 通道写入 CSV 文件来自动执行此过程，然后再针对另一个 K 值重复此过程。第三个程序将位图图像复制到左右帧缓冲区（用于加密 FPGA 程序），并设置迭代器和逆迭代器的 K 和 n 值。

### FPGA设计

#### 不动点

在本项目中，最终决定采用 10.17 定点格式来表示所有算术和乘法运算中使用的数值。在这种二进制补码格式中，有一个符号位，9 位用于表示整数，17 位用于表示十进制。虽然并非不能使用更大的定点格式，但选择 10.17 格式是因为它具有前瞻性，能够有效地利用 DSP 内核并促进未来的扩展。选择 9 位整数位，是因为它允许表示高达 511 (2^ 9 - 1) 的整数，这是一个我们希望在密码方案中使用的混沌因子，并且与文献中的相关内容相符。剩余的 17 位用于表示十进制，提供了足够的精度，可以与使用浮点类型的模拟结果进行精确匹配，并且在可接受的迭代次数内不会出现偏差。

#### 迭代器

项目的核心是迭代器模块。该模块接收时钟信号、复位信号、触发信号、初始条件和混沌因子，并输出新的迭代点和一个周期完成信号。复位后，迭代器加载初始条件，并在时钟信号提供的情况下开始计算标准映射的下一个时间步。计算完下一次迭代后，迭代器会保持暂停状态，直到下一次迭代被触发。这种调用-响应机制是必要的，因为迭代器并非单周期迭代器，实例化迭代器的模块需要控制请求的周期数，并且还需要给实例化器留出时间来保存这些值。

对于映射，按特定顺序进行计算，以减少每次迭代所需的循环次数，相比之下，直接计算 xn+1和 pn+1的方法则更为高效 。尽管上面展示的是简化形式，但标准映射作为因果系统的显式形式如下：

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBjTgl9YcQ2vViaPZiaPjGRcrBRve4BVy2Z8WxkgsraswwRbOuNOtylecUps2KAiclnxghBVJdM3g4XJoYfK6fiaeTZn3oqJianQc3jc/640?wx_fmt=webp&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=33)

注意，通过在计算 x n+1时 重新使用新计算出的 p n+1项，可以消除不必要的重复。这使得每次迭代的乘法次数和正弦表查找次数从 2 次减少到 1 次。

### 正弦实现

由于正弦函数不能直接综合，而且对本项目进行泰勒近似计算将是一项艰巨的任务，因此选择了正弦查找表（LUT）。使用全部 17 位十进制精度需要 2^ 17个条目，因此选择只使用 12 位十进制（加上 2π 的整数部分的 3 位）；

对于任何介于 0 和 2π 之间的 xn值，此查找表 (LUT) 接收定点值，提取第 19 位到第 5 位（对应于上一节所述内容），并查找该值。这将得到 sin(xn) 的近似值。

### 模运算符

还必须记住，这些项都是对 2π 取模的。诚然，取模实现并非最佳，但已足够。我们对初始结果 pn+1进行重复的加法或减法运算，使其进入合适的 \[0, 2π) 范围。由于 pn和 xn始终在此范围内，因此 循环次数取决于混沌因子K。

对于小于等于 2π 的 K，只需要一个周期。对于更大的 K，则需要额外的周期才能将其减去到合适的范围内。这可以通过添加额外的逻辑来解决，该逻辑检查 pn+1的值在哪个范围内，然后减去相应的量，我们没有严格的时序要求来实现这一点。由于 p n+1首先被取模，因此 pn+1的计算保证只需一个周期，因为它始终在 (-2π, 4π) 范围内，并且从这里执行一次加法或减法非常简单。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBhKtdtQlL2vMQELRgBoyrzzbHU0aDGLjh3WnYjhCYhCH8ibrhicOzVacC48mAkicGLtEnSrat5KxlYgrWWFoianzz0GsIBpPicFB8p8/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=34)

图 5：迭代器有限状态机

同样的信息也适用于逆映射，但运算顺序相反。这里，先用单循环模运算计算 xn-1 ，然后用多循环模 运算计算 pn-1。

### 标量

由于标准映射操作是在 2π 方格上进行的，需要将这些值缩放到 480x480 整数网格（或密码演示中的 320x320 网格）才能在 VGA 显示器上正确显示。为此，开发了 4 个额外的模块，分别用于从 2π→480、2π→320、480→2π 和 320→2π 进行缩放。每个模块都包含一个硬编码的 OUT/IN 值作为参数（采用 10.17 格式），并将其作为乘法器的输入之一。这样，编译器就可以决定是将操作编码为大规模的移位加法还是真正的乘法。

### 交互式演示

为了向之前提到的 StdMap 程序致敬，制作了一个交互式演示。首先，实例化了一个 307,200 地址 x 8 位宽的 M10k 块作为显存，并实例化了 Hunter Adams 的 VGA 驱动程序。本次演示仅使用中心 480x480 网格，但根据驱动程序提供的说明，创建一个“全尺寸”的 VRAM 缓冲区最为简便。有一个主状态机，在复位时首先进入清屏例程，将整个 VRAM 缓冲区写入零，以便为绘制轨道提供一个干净的界面。该例程完成后，状态机进入一个条件，此时写入 VRAM 的数据来自迭代器的输出。

绘制轨道的过程如下：PIO 线上的一个位指示初始点已被选中，并且包含所选 480x480 像素的 PIO 线有效。这些以 480 为基数的值随后由相应的缩放模块缩放到 2π，并输入到迭代器中。PIO 线上的另一个位提供所需的触发脉冲数，该数量等于我们希望在给定轨道上绘制的点数。每次触发时，还会保存迭代器中的值，将其缩放回相应的 VRAM 缓冲区，然后仅提取整数位将其转换为整数。通过 PIO 传递的颜色用作写入值，坐标用于计算 VRAM 中的相应索引。

演示中最后一个硬件支持的功能是帧保存。当提供合适的“转储”信号（同样通过 PIO）时，会绕过通常提供 VRAM 读取地址的 VGA 驱动程序。取而代之的是，通过 PIO 获取地址，并将读取到的数据发送回 HPS。在转储帧时，由于绕过了 VGA 读取地址，因此会出现明显的图像瑕疵。VGA 驱动程序仍在读取的数据会输出乱码到显示器上。

自动绘图仪和帧保存器使用相同的 HDL，但所有控制都是在软件中提供的，并通过相关的 PIO 信号传递。

### 密码学演示

在加密部分，定义了三个 320x320 的帧缓冲区，分别用于存储基础图像、加密/解密后的图像以及一个临时缓冲区。由于内存限制，我们将帧缓冲区从 480x480 降低到了 320x320。不再使用 PIO 来访问 M10k 进行帧转储，而是将其用于将图像数据写入基础帧。然后，该基础帧的数据会被复制到加密/解密帧，成为其默认图像。这有助于调试和演示，因为加密帧可以在无需 HPS 干预的情况下重置。

硬件复位后，所有缓冲区都会被清空，系统进入稳定状态（STEADY）。从这里，可以进入写入状态（WRITE），如前所述，将图像复制到写入状态；或者进入加密状态（ENCRYPT）或解密状态（DECRYPT）。xCRYPT 状态的执行过程如下：对于每个像素，结合确定的混沌参数和迭代次数，将像素坐标从 320 空间转换为 2π 空间，使用迭代器（或逆迭代器）运行 N 个周期，将结果坐标从 2π 空间转换回 320 空间，并将像素颜色保存到暂存缓冲区中的新地址。所有像素都经过迭代并保存到暂存内存后，系统进入保存暂存状态（SAVE\_SCRATCH），将图像复制回 xcrypt 缓冲区。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBhQ3xEC3nsJ7MPsn5zCQtjiabeqSwjniczicnzB2fRuRIeZmM2OlSdicH0TicfQx5hUnvSkvTgc3aFj6ms59riawHgrWkRWUlMA9Dum4/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=35)

图 6：密码学有限状态机

### HPS 设计

在HPS平台上，主要使用ARM来控制迭代器的输入和输出。在交互式演示中，使用线程程序轮询鼠标输入并触发迭代器。在自动化演示中，移除了鼠标事件轮询，并用一组自动化的嵌套循环来遍历K值并选择100个伪随机点。此外，还添加了一个线程，用于通过PIO接收像素信息并将数据保存到CSV文件中。在加密演示中，我们精简了C程序，使其仅向FPGA发送像素数据以写入图像。该程序使用命令行参数来设置K和n。

### 交互式演示

#### 用户模式

C 程序首先初始化与 PIO 线关联的内存映射，打开路径 /dev/input/event0 以读取鼠标事件，并启动一个名为 trigger\_thread 的 pthread。main 函数中的 while 循环处理从 event0 流读取的数据，并累加鼠标坐标值，因为该流仅提供相对更新。trigger\_routine 线程仅触发 1000 次迭代。它还将鼠标坐标保持在 480x480 网格的范围内（向左偏移 80 个像素以确保坐标位于显示屏的中心方格内），并通过 PIO 发送新的 FPGA 控制数据。下图示展示了接下来的四个 PIO 通道及其使用的位：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBh5qiaq3ibQa15UKYibaaykh49TfvESZEwaEJlua7UDETEqbkxiaJRUq5YeuhXfOxpDIcomYiavvRokx5GDCy1Y4UsJoEkK189oNrV4/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=36)

图 7：按位 PIO 分解

#### 自动模式

在自动化模式下，将鼠标事件输入流替换为嵌套循环。外层 while 循环递增 K 值并更新其关联的 PIO 通道。内层 for 循环选择 n 个起始 x 和 y 坐标点，并让 trigger\_thread 触发迭代器进行 1000 次迭代。需要注意的是，尽管选择的 x 和 y 输入点是通过 rand() 函数确定的，但始终会为每次新的 K 值重置随机种子，从而确保这 n 个轨道每次都相同。对于给定的 x 和 y 值，颜色也是确定性的。这些选择使得 GIF 动画能够非常流畅地展现轨道随 K 值变化的演变过程。

```
float k = 0.0;

while(1) {

 //开始生成随机点

 *k_fix_addr = fl2fix(k_float);

 for(int i = 0; i < n; i++) {

  // 设置随机 x 和 y
  坐标 X_pos = rand() % 480 + 79;
  Y_pos = rand() % 480 - 1;

  // 确定性（伪随机）颜色 = f(x,y)
  color = (48199 * X_track + 12417 * Y_track) % 256;

  [在此处重置迭代器]
 }

[在此处转储 VGA 缓冲区]

k += 0.025;

}
```

鉴于 HPS 端控制机制和 FPGA 端迭代器未同步，必须通过频繁调用 usleep() 来降低 ARM 的运行速度。具体来说，在选择新的 x、y 坐标之前会休眠 20μs，并且每次转储 VGA 缓冲区时都会休眠 2s（尽管这可以优化）。当标志被激活时， dump\_routine pthread 会遍历 640x480 地址空间，将该地址分配给 P2H\_CTRL PIO 通道，并通过新的 DUMP PIO 通道接收像素数据。因此，进行了以下修改/添加：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBia2L8bxQrJVuJ6k6cYuyBsWpN8zF9GfBI0gFTxibiclibrAaoRxyL4pIdGzibggY9pqF0jAOiaKpLZpvjVL2bApYIIjklwRXbj0fvPE/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=37)

图 8：演示 2 的按位 PIO 修改

### 密码学演示

加密演示程序使用 C 语言编写，由于所有计算都在 FPGA 上进行，因此程序本身要简单得多。该程序从命令行参数读取 K 和 n（默认值为 K = 0.5 和 n = 1）。使用 Python 脚本将.bmp 图像转换为一个常量整数数组，该数组对应于像素数据。该数组保存在一个头文件中，并在编译时包含。C 程序循环遍历该数组，并将像素数据写入 PIO 通道。 P2H\_CTRL 通道现在如下所示：

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBhGzUqF3sFEtmp4ReJibIpv9nuNgYekzPbCNEI2icX7dlhb7KK4Ym4n394xVPPBXccuptLfKUAZZGDQZ8EljV2INAKicIG9hMf4ic8/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=38)

图 9：演示 3 的按位 PIO 修改

### 测试

让迭代器达到完整且可正常运行的状态比最初预想的更具挑战性。遇到了几个问题，从正弦表的精度到 Verilog 默认未显式声明的连线有符号性。因此，不得不显式地指出哪些连线需要带符号。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBjN9H3QauSDGjOxBth7jgz9e3xHBI2IFuTCZvcRKiaWZ6X0z1JjApu11LZNHNpXDY5lwxLclvic1xKZiaFoXl4Dia3M9JzG1lbDvUM/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=39)

图 10：迭代器的 ModelSim 测试平台

首先使用 ModelSim 对轨道进行可视化评估。上图所示为一个 x 轴方向振荡而不发生循环，而 p 轴方向发生循环的轨道。在可视化验证这些轨道后，将其提取为表格格式，并将其放置在散点图上：

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBg3FP6t1UnYauyCw57Z8sPo1byqcoxGu8XYlRrkp8Ayntc93dDIyib17iaHt5uNHZ1NThkm2AfcFqpBcTfE5EtZ3DRAHUu1gUKPo/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=40)

图 11：5 位与 12 位精度对比

此时，“模糊”的轨道表明正弦查找表深度不够。随意选择了一个 12 位精度的查找表，并编写了一个 Python 脚本来打印一系列赋值语句。将这种大小的查找表适配到 FPGA 上没有任何问题。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBiaD57zwpgmGLZK4VDQdJVtBD5VV2XHeNQJa46ibF2WtttxIWic4wryqPFNw5gPFcWV4Vxzf17kQlnsjFACxxDE9hLicWIk3ibtseNE/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=41)

图 12：5 位正弦 LUT，宽轨道

在确认正向映射成功后，按照FPGA设计部分所述进行了逆向操作。在ModelSim中，选取任意点，执行N次正向映射，然后执行N次逆向映射。验证了逆向映射的性质，因为两次操作后的结果坐标与初始坐标相同。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBiaktufpKB7ayqGl2rZBNwaKm7iaRcjLcf2KsOdweAeMVnExyEm38rnrkkK2pdH3Hkdofl8q9DRLiaKXAIG8OQfPUlIbfWuRlvDn8/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=42)

图 13：正向映射和反向映射的重叠

为了验证加密算法是否按预期工作，用 Python 和浮点运算编写了相同的算法。这验证了在 VGA 显示器上看到的变换，并增强了对状态机设计的信心。下图是 Bruce Land 的 320x320 像素 24 位彩色图像。这里，设置 k = 0.5，N = 1。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBjYj2LRiaQM0EEeY0meRaOxF70RBE9NjSMiaUfx9E6vwNq5Qkevh0reJZT0CQQhoeKElhUknEibKf2ycxBv1LSu6jxeNcUc93P5Z0/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=43)

图 14：24 位 Bruce

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBj4InzAQibuQS4M9YbcoPYRPGibDbSDN77Satw7SQn2LqVEXIGoUtaLqmaic4yZ7HJw4FNVKCrG9Whicp5N4g7kqGcsCCBX4wNQWo8/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=44)

图 15：FP Encr. Bruce

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBgf8n3XsCnvicf9QW6UTnrQdUkQ1yVoibic2LQ7eyAOgN3Tib5iaWV3H9dcejhOWnzG8xA1K6qGiaFmENRv39wqkuGW4qutN8iaLeTdo4/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=45)

图 16：FP Decr. Bruce

### 结果

#### 交互式演示

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBiaEs8Micpib4oGlFIdmwzhztKOqicRoF8ybFE6UsVMoNoXTHkzicZibyfL06yRFyJakx5xjJ6wtPR1gFYOE1GeG31zfrfSPbXmsDsV8/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=46)

k = 0.0

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBhh2O4ibJFTHYtD59ZeVUHWj0qzwsBk4jYVaTKI5D2pXB8WNKBJnP4rx653r41Ut5zhRh1enw5emDFqCTMOFLkzTzluR3fYawuQ/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=47)

k = 0.5

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBhWzJLx7dY7rgg2d4pnqjuRztSSvXibEu8C5SFibLicDIDokWCB7UnZcOmONVFFKPY0amA81s0QWSNXKzlauL1s6MPxj9DQcobCCE/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=48)

k = 1.0

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBhhlPtUAibnHZUftoe8JUAlXNibiaAWHw82I2T1GicoOFMwgebck9sxmOKAYe2LaarWRZfFExqmDF8YOtvQvHa5uSfU56joKicVicMCE/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=49)

k = 2.0

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBjP3josR70lj36F6rE3NliatCj474Io9icGIwE8YU66cfwdCxutSglLvNA1AQhdvbnf8okqhYYceftTBuRakJUcibHia6QTjuq9XQA/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=50)

k = 5.0

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBiaTS6yUJ0C7vrfleeic2Dou6wYgtagCqph8WstrtXjsA5rgjMnHDpiaic6upjkTHOJDYYEjiaibDMwiaTg9uTup4HcuQmkKdecg8AP0Y/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=51)

k = 15.0

图 17：交互式演示轮播图

请注意，虚线并非错误，而是由于每次迭代仅绘制有限数量的点所致。经过足够多的迭代后，这些虚线会闭合，而虚线的斑点是由于每次迭代在 x 方向上的增量很小造成的。在混沌因子较低的情况下，它们应该在整个空间中形成闭合回路。

#### 密码学演示

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBiaz2KibJ9Kf7rpeeLnysdMntm45JF6FQov5yCwlbMUGkRpAHib7ufsapGRnC0w99NrUsKo9bRJ2z8Gm9OyMqxWqYzcLd6G38heQM/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=52)

k = 0.5，N = 1，加密

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBgSrnukv3icO2LNwiaKSBNEjF5gWA39zFtBYqSer9lWdzXDYkDbWnnq5TfZia6vPz9kMPwPcruQcv3fdKLGV1sD151EDiaF0Vuj1ok/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=53)

k = 0.5，N = 2，加密

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBiaHZPneBFAk3syTzYx0AQQnRKZZxn30loBANbJWGv2haEt9oS09GQjtPK2vncUkrlNY2emuqRBom7ibyuPsxSJwMV4sJdwMkknI/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=54)

k = 5.0，N = 1，已加密

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBgXIa2C6MxlyP6Rt17T9Clt69GOmcvAbtfI9eO33elCObedeo6vehMBEbLeLjjWlL8U1Ym3za4Y7LLk12wAyy4zyeUYicNocexs/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=55)

k = 50.0，N = 1，已加密

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBgILZp52Rw2gSzV6kQHIdGpufW1ic7X7rXFHicNiaGGH4aay2f4mbI5O3X6Cf0oUDbyGCfsdInHgt5qopNkyABoyM2SNb9aeBt498/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=56)

k = 0.5，N = 1，已解密

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/TsrAtX2ibWBg0IQ9Fdw6MvsIGUQkmS0qE4MFfehEYbojeCeOZ44yN1icLBQPaNUBKuQH63olXmbNs7DMn4riaZNibUew3UDIIRIRrianB1OC3g44/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=57)

k = 0.5，N = 2，已解密

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBgHhYwBIIShZzN1FLRNbaIQ2I6iaZia5RJia75fItuKfCahgotUZHPhPmwQQBib30cJ6yDBZ6A5tM0R7iarNtD2G2iaCsnxiak43fqNLM/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=58)

k = 5.0，N = 1，已解密

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/TsrAtX2ibWBgocQl041S8YngZ8xVJFgFgwB874FHwicvm6G5HUl3ZjibTEKWicgjpEwTt709J93bwUbXZyNfabKGxTkuLEYQIUhY8vdmdKCY8q0/640?wx_fmt=webp&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=59)

k = 50.0，N = 1，已解密

图 18：密码学轮播图

会注意到加密和解密后的图像中存在许多黑色像素和奇怪的伪影。这是由于在 2π 空间内外移动时精度损失造成的，导致舍入误差。如果保存的是完整的定点数据，则可以进行无损解密，但当缩放到 320 空间时，并非所有生成的点都能与像素空间对齐。许多像素最终会与其他绘制的像素重叠，导致颜色伪影，以及在映射不完美的地方出现黑色区域。正如“测试”部分所示，在浮点计算中仍然可以看到一些类似的问题。

如果时间允许，将研究使用极大混沌因子处理图像时出现的图像扭曲现象，因为在浮点模拟和文献综述中均未发现这种现象。此外，也可以通过将映射直接调整到 320 空间来解决这个问题，而不是在不同空间之间来回转换。

### 结论

最终，成功地在DE1-SoC上用可综合的Verilog语言实现了Chirikov标准映射的迭代器，并将其应用于图像加密和解密的概念验证。成功地将工作与Python脚本进行了比较，并对密码学进行了定性分析。

尽管Chirikov标准映射背后的理论浩瀚无垠，但对于像我们这样的学生来说，它仍然充满魅力。人们可以花费数年时间学习该映射、其可积性、流形、对称性以及柯尔莫哥洛夫-阿诺德-莫泽（KAM）理论。对我们而言，正是工作背后无穷无尽的信息宝库，才使得首次涉足标准映射领域显得如此特别。

### 项目链接

> https://people.ece.cornell.edu/land/courses/ece5760/FinalProjects/s2024/hwm44\_mck65/index.html

### 代码链接

> https://people.ece.cornell.edu/land/courses/ece5760/FinalProjects/s2024/hwm44\_mck65/index.html

### 视频链接

> https://youtu.be/n0\_R8OV8T1A?si=sCZVNwdnNpQWf8qz

## 总结

本文整理了康奈尔大学 2024 年春季 ECE5760 课程基于 CycloneV DE1-SoC 开发板的 2 个 FPGA 实战项目，全部采用 Verilog 开发，具体项目如下：

- 可参数化卷积加速器设计：

该项目在 DE1-SoC FPGA 平台上实现了一种面向卷积神经网络（CNN）推理的可参数化卷积加速器，将 ARM(HPS) 与 FPGA 协同设计相结合，由 HPS 负责数据预处理、参数配置及任务调度，FPGA 负责高并行卷积计算。硬件采用 8 输入通道并行、3×3 卷积窗口、行缓冲（Line Buffer）及流水线架构，集成卷积、量化、ReLU、最大池化等功能，并通过 IFM、Weight、ACC、OFM 四级缓冲区实现数据复用，有效降低外部存储访问开销。整个系统支持输入通道数、特征图尺寸、池化、填充、量化参数等灵活配置，可扩展构建多层 CNN，在资源受限的 FPGA 上兼顾了计算性能、资源利用率和可扩展性，并成功完成图像融合、边缘检测及动态阈值处理等应用验证。

- Chirikov 标准映射实现：

该项目在 DE1-SoC 上利用可综合 Verilog 实现了 Chirikov 标准映射（Standard Map）迭代器，并结合 HPS 构建了交互式混沌轨迹可视化和图像加密系统。设计采用 10.17 定点运算、正弦查找表（LUT）、有限状态机和 FPGA 并行计算，实现标准映射及其逆映射的高速迭代，同时支持 VGA 实时轨迹绘制、参数扫描以及基于混沌映射的图像加密/解密。项目验证了标准映射在混沌动力学可视化和图像置乱加密方面的应用可行性，并分析了定点量化与空间映射带来的精度损失及图像伪影问题，为 FPGA 实现非线性动力系统计算、科学可视化和轻量级混沌密码算法提供了完整的硬件设计方案。

**微信扫一扫赞赏作者**

开源项目 · 目录

## 相关链接
- [[台积电：Chiplets和3D封装_(47页PPT）]]
- [[82岁江泽民在2008年发表论文指出：发展智能化，机器学习将有所作为……]]
- [[军事智能化的5个主要方向]]
- [[跟我学强化学习之四——神经网络]]
- [[Science重磅综述：深度解析超表面正在从“光学元件”变成“器件架构” 1]]
