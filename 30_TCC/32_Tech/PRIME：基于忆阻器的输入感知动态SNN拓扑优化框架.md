---
title: "PRIME：基于忆阻器的输入感知动态SNN拓扑优化框架"
source: "https://mp.weixin.qq.com/s/a0tIpq8TYwd3iX4PzZyd0w"
created: 2025-12-04
note_id: "1894983906869018904"
tags:
  - "AI链接笔记"
  - "忆阻器"
  - "脉冲神经网络(SNN)"
  - "PRIME框架"
  - "get-笔记"
  - "AI研究"
---

# PRIME：基于忆阻器的输入感知动态SNN拓扑优化框架

## 摘要

🧠 **研究背景：AI与大脑的能效鸿沟** - 人类大脑仅需20瓦功率完成复杂认知任务，传统AI依赖冯·诺依曼架构存在"存储-计算分离"瓶颈 - 主流AI需精细调节突触权重，难以适配忆阻器随机特性，限制能效提升 - 香港大学、中科院微电子所等团队受大脑结构可塑性启发，研发PRIME框架  🔬 **核

## 正文

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F00bbc3cd7e39b1bb6887812f3686e650?Expires=1780063533&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=OGyNw06y8JKaE90xOkZSVGV57eQ%3D)

近日，一项发表于《Science Advances》的研究推出了名为 PRIME
的新型神经网络框架，通过硬件软件协同设计，成功弥合了人工智能与人类大脑在能效、适应性上的差距。该模型基于忆阻器的脉冲神经网络（SNN），借助拓扑优化与动态计算机制，在图像分类、图像修复等任务中展现出卓越性能，为低功耗、高高效的神经形态计算开辟了新路径。

## 一、研究背景：AI 与大脑的核心差距亟待突破

当前，以 GPT-4、SORA 为代表的人工智能模型虽展现出强大能力，但在能效和动态适应性上远不及人类大脑。人类大脑仅需 20
瓦功率即可完成复杂认知任务，而传统 AI 依赖冯・诺依曼架构，存在存储与计算分离、数据传输能耗高、计算深度固定等问题。此外，主流 AI
依赖精细调节突触权重优化网络，难以适配新兴忆阻器等突触器件的随机特性，进一步限制了能效提升。

为解决这些痛点，香港大学、中国科学院微电子研究所、北航大学等机构的研究团队，受人类大脑结构可塑性和动态计算机制启发，研发了
PRIME（输入感知动态忆阻脉冲神经网络拓扑优化）框架。

## 二、核心创新：四大脑启发设计重塑神经网络

PRIME 的突破源于对人类大脑工作机制的精准复刻与技术转化，核心创新集中在四方面：

### 1. 拓扑优化替代权重微调，化随机为优势

不同于传统 AI 对突触权重的精细调节，PRIME 借鉴大脑发育中的 “结构可塑性”——
初期大量随机突触连接会通过优胜劣汰保留关键连接。研究团队利用忆阻器编程的固有随机性生成初始权重，再通过拓扑修剪优化，保留高价值突触、剔除冗余连接，彻底避免了忆阻器电导微调的高能耗问题。

### 2. 输入感知动态早停，适配任务难度

受大脑动态分配计算资源的启发，PRIME
引入输入感知动态早停机制。在推理过程中，模型通过计算输出置信度，为不同难度的输入动态调整计算步长：简单输入提前终止计算，复杂输入则完整执行流程。这一机制在保证性能的同时，大幅降低了计算延迟与能耗。

### 3. 忆阻器存内计算，突破冯・诺依曼瓶颈

PRIME 采用忆阻器交叉阵列实现存内计算，将突触权重存储与信号计算集成于同一物理位置，无需数据在存储与计算单元间往返传输。这种架构完美复刻了大脑突触 “存储
- 计算合一” 的特性，显著提升了并行度并降低能耗。

### 4. 抗噪声鲁棒性，适配硬件特性

忆阻器的编程与读取噪声是神经形态硬件的关键挑战，而 PRIME
巧妙利用其编程随机性初始化网络权重，通过拓扑优化使模型对噪声具备天然抗性。实验表明，即使在高噪声环境下，模型性能仍能保持稳定。

## 三、实验验证：双重任务彰显性能与能效优势

研究团队在 40 纳米工艺、256K 忆阻器宏芯片上对 PRIME 进行了全面验证，涵盖两大核心任务：

在神经形态图像分类任务中（N-MNIST 数据集），PRIME 达到与软件基线相当的分类准确率（最高 97.6%），同时实现 37.8 倍的能效提升，计算量减少
77%；在更复杂的图像修复任务中（MNIST 数据集），模型重建质量与 inception 分数（IS）媲美软件基线，能效提升高达 62.5 倍，计算量减少
12.5%，且生成图像的多样性与高质量得到充分保障。

进一步的扩展性测试显示，PRIME 在更大规模的脉冲 VGG-11 网络（DVS128 Gesture 数据集）和 Fashion-MNIST
图像修复任务中，仍能保持性能稳定，相比 RTX 4090 GPU 能效提升超 200 倍，展现出强大的规模化应用潜力。

## 四、研究意义：开启神经形态计算新篇章

PRIME
通过硬件软件协同设计，首次将大脑的结构可塑性、动态计算深度、存内计算三大核心特性融入神经网络框架，不仅解决了忆阻器等新兴器件的应用瓶颈，更提供了一种兼顾性能、能效与鲁棒性的计算范式。

未来，PRIME 有望广泛应用于边缘 AI、可穿戴设备、物联网终端等低功耗场景，为人工智能的 “轻量化”“绿色化”
发展提供核心技术支撑。该研究团队已开源相关代码，助力全球科研人员进一步推进神经形态计算的研究与应用。

这项研究由香港大学、中国科学院微电子研究所、北京航空航天大学、香港科技园区 ACCESS AI
芯片中心等机构联合完成，得到国家重点研发计划、国家自然科学基金等项目支持，相关成果以 “Topology optimization of random
memristors for input-aware dynamic SNN” 为题发表于《Science Advances》（DOI:
10.1126/sciadv.ads5340）。

五、图文导读

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F2e0f687f5268d941f1156d479f14dacf?Expires=1780063533&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=82UnXx9JS30sqye2pQqmp46Dxfc%3D)

# 图 1 基于忆阻器的输入感知动态脉冲神经网络（SNN）的脑启发拓扑优化

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F056c6ded83c92718ba95c68249a4a700?Expires=1780063533&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=TM%2BurfivoVOcWY4EiVKKh2gIpKg%3D)

# 图 2 PRIME 框架概述

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc2c975064c0ae83033ba72f1607c018a?Expires=1780063533&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=N%2BGVAJV4PcHmADN2GZqzvjp43uY%3D)

# 图 3 基于 PRIME 的 N-MNIST 数据集图像分类实验

# 

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fde6c8969f0d299763b2f339bcc623104?Expires=1780063533&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=IqyIDJCIloRC0dEycAAD2n0qfcA%3D)

# 图 4 基于 PRIME 的 MNIST 数据集图像修复实验

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd71d35fa72e00d96701389fe7bc4ac01?Expires=1780063533&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=5zjFSDUKS40LXeDwmwPVZi8L1%2Bk%3D)

# 图 5 忆阻器噪声及其对 PRIME 的影响

# 

文献链接：https://www.science.org/doi/10.1126/sciadv.ads5340

本公众号发布的内容（包括但不限于文字、图片、视频、音频及设计素材等），如有侵权，请联系删除。我们始终尊重知识产权，严格遵守《中华人民共和国著作权法》等相关法律法规，致力于维护健康的内容创作环境。

提供基于忆阻器的储备池计算，神经形态视觉系统等应用的设计与实现；承接忆阻器仿真电路开发，以及忆阻器的测试、表征工作；提供忆阻器机理相关的专项设计与技术咨询服务；忆阻器器件的3D建模。

欢迎大家投稿与咨询，联系邮箱：scientists2025@163.com，私信也行

#

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 10:05*

## Related Notes

- [[基于模拟忆阻器的Actor-Critic网络：类脑奖励学习的硬件实现突破]]
- [[晶圆级忆阻器无源交叉阵列制造技术：脑规模神经形态计算突破 🧠]]
- [[生物启发的脉冲神经网络（SNN）设计与研究进展]]
