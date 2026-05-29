---
title: "ClearSight：基于人类视觉启发的事件驱动运动去模糊研究"
source: "https://mp.weixin.qq.com/s/JoVOn3IwL_o46gEsEfMsuA"
created: 2025-09-21
note_id: "1888116591317561056"
tags:
  - "AI链接笔记"
  - "运动去模糊"
  - "事件相机"
  - "双驱动混合网络"
  - "get-笔记"
  - "科技资讯"
  - "重要"
---

# ClearSight：基于人类视觉启发的事件驱动运动去模糊研究

## 摘要

🔍 **研究背景与核心挑战**   - 传统RGB相机在快速运动或弱光条件下易产生模糊图像，事件相机通过高时间分辨率捕捉亮度变化，提供运动细节，但存在数据非均匀分布和冗余问题   - 跨模态特征融合（事件流+RGB图像）是提升去模糊性能的关键瓶颈    🧠 **核心创新：双驱动混合网络（BDHNet

## 正文

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F2a28d390232ce110d38f2d0fc24dd870?Expires=1780066700&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=HMyZGuUKX436ZwTg%2B3PrQ5GTE9I%3D)

好消息！加入知识星球，详细阅读本文PDF完整版

在计算机视觉的浩瀚领域中，运动去模糊一直是一项极具挑战性却又至关重要的任务。想象一下，当我们想要捕捉快速移动的物体或者在不稳定的拍摄条件下记录精彩瞬间时，相机常常会拍出模糊不清的照片。这种模糊不仅影响了我们对图像内容的清晰感知，也给后续的图像分析和处理带来了极大的困难。

## 论文信息

#### 题目： ClearSight: Human Vision-Inspired Solutions for Event-Based Motion Deblurring

#### 作者：Xiaopeng Lin, Yulong Huang, Hongwei Ren, Zunchang Liu, Yue Zhou, Haotian Fu, Bojun Cheng

## 事件相机：打破传统局限的新力量

传统的基于帧的相机在处理运动模糊问题时，往往显得力不从心。这是因为它们缺乏必要的运动信息，尤其是在不利的光照条件下或者捕捉快速移动物体时，性能更是大打折扣。为了解决这个难题，事件相机应运而生。事件相机以高时间分辨率捕捉亮度变化，自然地突出高对比度边缘，其事件流中明确的对比边缘信息和隐含的时间相关性，为恢复模糊图像中丢失的细节提供了新的可能。

![视觉刺激处理](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F6e3209a56ec11d30863d334dfb517b31?Expires=1780066700&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=W2%2FJRKt5KW3MOkVyE99BhfhChQw%3D)

视觉刺激处理

然而，事件相机也并非完美无缺。事件数据的非均匀分布和固有冗余性，使得现有的跨模态特征融合方法在处理事件流和基于帧的图像时存在一定局限性。如何有效地整合这两种数据，成为了提升运动去模糊性能的关键。

## 受生物启发的双驱动混合网络（BDHNet）：模仿人类视觉的智慧结晶

为了更好地利用多模态信息进行基于事件的运动去模糊，来自相关研究团队提出了一种受生物启发的双驱动混合网络——BDHNet。该网络巧妙地模仿了人类视觉系统的视觉注意力能力，通过结合基于神经元和增强型基于突触的注意力机制，有效整合了事件流与基于帧图像的信息，为运动去模糊带来了新的突破。

### 网络架构解析

BDHNet采用经典的编码器 -
解码器架构，主要包含基于ANN的图像分支和基于SNN的事件分支。多尺度模糊图像被输入到图像分支，使用基于MIMO的编码器提取相关特征；相应的事件流被整形为基于体素的表示后输入到事件分支，用于提取运动特征。

![网络总体框架](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F304c03abb88ee892cb8141803f6f03dc?Expires=1780066700&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=GbCtLUmH%2B4k2xbrUedMiiZzo7wU%3D)

网络总体框架

在两个分支的每一层之后，采用双驱动增强来模仿人类视觉系统中的视觉注意力。这一增强机制由神经元配置器模块（NCM）和模糊关注区域模块（RBAM）组成。

### 神经元配置器模块（NCM）：精准聚焦模糊区域

NCM旨在从图像数据到事件数据进行视觉增强，通过动态调节神经元响应，将注意力集中在关键区域。与传统方法不同，NCM根据输入刺激的特征，利用图像特征设置所有时间步的初始膜电位和神经元阈值，实现像素级的动态调整。

![NCM在SNN块中的应用](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F304c03abb88ee892cb8141803f6f03dc?Expires=1780066700&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=GbCtLUmH%2B4k2xbrUedMiiZzo7wU%3D)

NCM在SNN块中的应用

这种配置能够增强模糊区域中神经元的响应能力，提高从事件数据中提取运动特征的能力。通过可视化不同设置下神经元产生的脉冲输出，我们可以清晰地看到NCM方法能够更有效地将脉冲集中在模糊区域或引起运动的边缘上，从而提升去模糊效果。

### 模糊关注区域模块（RBAM）：精确提取运动线索

RBAM则从事件数据到图像数据进行视觉增强，利用来自ANN分支的图像特征和来自SNN分支的脉冲特征，生成一个描绘模糊区域的掩码。这个掩码用于从事件特征中捕获准确的运动线索，优化跨模态特征融合。

![RBAM模块生成掩码过程](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd71d0b49ea2aa8f68ac2099e664fb001?Expires=1780066700&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=MzU69m%2BZET%2F3ePtJ9E1UCiRgyNs%3D)

RBAM模块生成掩码过程

通过可变形滤波器对脉冲特征进行局部聚合，并结合图像特征生成的阈值图，RBAM能够无监督地识别模糊区域，显著增强跨模态特征融合的效果。

## 实验验证：卓越性能与泛化能力的有力证明

为了验证BDHNet的性能，研究团队使用了包含合成和真实场景的GoPro、REBlur和MS - RBD数据集进行评估。

### 数据集介绍

* **GoPro数据集**：是图像运动去模糊的基准数据集，包含3214对模糊和清晰图像，用于评估去模糊性能。
* **REBlur数据集**：由DAVIS捕获，用于基于真实事件的运动去模糊，包含各种线性和非线性室内运动。
* **MS - RBD数据集**：是在真实场景中捕获的多尺度模糊数据集，用于评估模型在真实场景中的泛化能力。

### 对比实验结果

研究团队将BDHNet与当前最先进的仅图像和基于事件的去模糊方法进行了比较。结果显示，BDHNet在各个数据集上均显著优于其他方法。在GoPro数据集上，BDHNet达到了最高性能指标，PSNR为37.04，SSIM为0.977；在REBlur数据集上，PSNR为38.50，SSIM为0.978。

![各方法在数据集上的性能对比](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3030aba33a654df7af15bacfcce2e48e?Expires=1780066700&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=AcSXvMmHz78C%2BP9e31ghb6kpni4%3D)

各方法在数据集上的性能对比

更值得一提的是，BDHNet在REBlur数据集上未经微调的情况下，也取得了最佳性能，这充分展示了其强大的泛化能力。

### 消融研究

通过在GoPro数据集上进行的消融研究，研究团队进一步验证了NCM和RBAM模块的有效性。实验结果表明，NCM模块能够提高PSNR 0.22
dB，RBAM模块通过无监督掩码生成和跨模态特征融合，分别使PSNR提高了0.33 dB和0.44 dB。

![消融研究中各模块有效性对比](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd71d0b49ea2aa8f68ac2099e664fb001?Expires=1780066700&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=MzU69m%2BZET%2F3ePtJ9E1UCiRgyNs%3D)

消融研究中各模块有效性对比

## 总结与展望

BDHNet的提出为基于事件的运动去模糊领域带来了新的希望。其受生物启发的架构和双驱动增强策略，有效地减轻了相机或场景运动导致的模糊影响，在合成和真实场景中均超越了现有技术。

随着计算机视觉技术的不断发展，我们相信BDHNet的应用前景将十分广阔。它不仅可以应用于摄影、视频监控等领域，还可以为自动驾驶、机器人视觉等新兴领域提供更清晰、准确的视觉信息。未来，我们期待更多基于生物启发的创新方法出现，为解决计算机视觉中的各种难题带来新的思路和解决方案。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F2f657fa63ba6b6e51e68804ebfd48aaf?Expires=1780066700&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hEaOHSu1EMh9wAjMZrPYJdH5eVA%3D)

**#论  文  推  广#**

**让你的论文工作被更多人看到**

你是否有这样的苦恼：自己辛苦的论文工作，几乎没有任何的引用。为什么会这样？主要是自己的工作没有被更多的人了解。

**计算机书童**为各位推广自己的论文搭建一个平台，让更多的人了解自己的工作，同时促使不同背景、不同方向的学者和学术灵感相互碰撞，迸发出更多的可能性。 **计算机书童**鼓励高校实验室或个人，在我们的平台上分享自己**论文****的介绍、解读**等。

**稿件基本要求：**

• 文章确系个人**论文的解读**，未曾在公众号平台标记原创发表，  

• 稿件建议以 **markdown** 格式撰写，文中配图要求图片清晰，无版权问题

**投稿通道：**

• 添加小编微信协商投稿事宜，备注：姓名-投稿

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F6803edfd55c998393535ac56782ec08f?Expires=1780066700&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=HC6x2VcBA0YWyhnYQeDzdW3Gt8M%3D)

**△长按添加****计算机书童****小编**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F24af5c31ad5fa6013caf2fa2116731bb?Expires=1780066700&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=iDRdauNR2kQM1OLcpew5zYmx6lw%3D)

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 10:58*