---
title: 全球首款大规模类脑脉冲大模型SpikingBrain1.0发布
tags:
- ai-ml
- artificial-intelligence
- brain
- chiplet
- large-language-model
- neuron
- neuroscience
- transformer
---
- **类型**: link
- **时间**: 2025-09-25 06:54:17
- **标签**: AI链接笔记, 类脑脉冲大模型, SpikingBrain1.0, 混合线性注意力架构
- **来源**: https://mp.weixin.qq.com/s/87jInA6dOg4FScJkFwhTyw

## 内容

🧠 **核心突破：类脑机制重构AI效率**  
- **灵感来源**：模拟人脑神经元工作方式（20瓦功耗驱动千亿神经元），提出"基于内生复杂性"理念  
- **架构革新**：采用"混合线性注意力架构"，将传统Transformer二次方复杂度降至线性O(n)  
- **关键机制**：引入"自适应阈值脉冲神经元"，事件驱动激活模式实现69.15%计算稀疏度  

🚀 **性能指标：效率与能力的双重飞跃**  
- **速度提升**：处理400万token超长文本速度超主流Transformer模型100多倍  
- **数据效率**：仅需2%数据量即可完成训练（传统模型需大量数据）  
- **模型版本**：提供SpikingBrain-7B（70亿参数）和SpikingBrain-76B（760亿参数）两个版本  

🔄 **技术创新：降低落地门槛**  
- **转换技术**：支持现有Transformer模型直接转化为SpikingBrain架构，大幅降低训练成本  
- **开源生态**：所有技术细节和代码已在GitHub（https://github.com/BICLab/SpikingBrain-7B）及魔搭平台开源  
- **硬件适配**：支持非NVIDIA GPU集群，开发CUDA/Triton算子及并行通信策略  

📊 **应用价值：长文本处理与AGI探索**  
- **解决痛点**：突破传统模型在长篇小说、法律文书等超长文本处理中的效率瓶颈  
- **未来方向**：为通用人工智能（AGI）提供低能耗、高效率的新路径

## 原文

近日，中国科学院自动化研究所的李国齐与徐波团队联合发布了全球首款大规模类脑脉冲大模型
——SpikingBrain1.0。该模型在处理长文本时展现出惊人的速度，能够以超过当前主流 Transformer 模型100多倍的速度处理400万
token 的超长文本，且仅需2% 的数据量。

![image.png](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F15cd8912368a5a43c64f71f984a111be?Expires=1776346134&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=T%2BpD1%2BhQnNFiKAvjsmLVnyiqcvg%3D)

当前主流的大语言模型，如  GPT 系列，普遍基于 Transformer 架构。尽管 Transformer
 以其强大的自注意力机制而闻名，但其计算复杂度却是一个致命的短板。在文本长度增加时，计算量呈现出平方级别的暴涨，使得长文本的处理变得异常耗时和耗能。这一现象让
 AI 在分析长篇小说或法律文书时显得力不从心。

为了寻求新的解决方案，研究团队将目光投向了自然界最为高效的智能系统 —— 人脑。人脑由千亿神经元构成，功耗却仅为20瓦。团队提出了 “基于内生复杂性”
的理念，旨在提升模型内部单元的效率与智能。

SpikingBrain  模型通过全新的架构模拟了人脑神经元的工作方式，分为两个版本:SpikingBrain-7B（70亿参数）和
 SpikingBrain-76B(760亿参数)。首先，该模型抛弃了传统 Transformer 的二次方复杂度自注意力机制，采用了
 “混合线性注意力架构”，将计算复杂度降至线性(O (n))，显著提高了处理长文本的效率。

其次，SpikingBrain 引入了
“自适应阈值脉冲神经元”，使神经元的激活与否取决于接收到的信号强度。通过动态调整阈值，模型确保神经元在高效能状态下工作，这种事件驱动的机制显著节省了能耗，计算稀疏度高达69.15%。

此外，团队还开发了一套高效的模型转换技术，能够将现有的 Transformer 模型直接转化为 SpikingBrain
架构，降低了训练成本。所有技术细节和代码已在 GitHub 及魔搭平台上开源，供全球研究人员使用。

此次 SpikingBrain 的问世，不仅在计算效率上取得了重大突破，也为未来的通用人工智能提供了一条新思路。

GitHub:

https://github.com/BICLab/SpikingBrain-7B

以上来源：AIbase，由人工智能行动信息港AI HUB分享阅读

---
**Tags:** [[BrainInspired]] [[Chiplet]]

---
## 相关笔记 (AI 自动关联)
- [[全球首款大规模类脑脉冲大模型SpikingBrain1.0发布]]
- [[SpikingBrain-1_0_类脑脉冲大模型的革命性突破__]]
- [[中科院类脑脉冲大模型SpikingBrain-1_0技术解析]]

> [!note]- 可能重复: [[全球首款大规模类脑脉冲大模型SpikingBrain1.0发布]] (相似度: 94%)
