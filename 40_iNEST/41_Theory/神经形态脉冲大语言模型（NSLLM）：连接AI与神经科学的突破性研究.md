---
title: "神经形态脉冲大语言模型（NSLLM）：连接AI与神经科学的突破性研究"
source: "https://mp.weixin.qq.com/s/HSg8wSXYM97KsHlhzLvcUA"
created: 2025-12-18
note_id: "1896243996586601648"
tags:
  - "AI链接笔记"
  - "神经形态计算"
  - "脉冲大语言模型（NSLLM）"
  - "低功耗AI"
  - "get-笔记"
  - "学术论文"
  - "重要"
---

# 神经形态脉冲大语言模型（NSLLM）：连接AI与神经科学的突破性研究

## 摘要

### **🔬 研究背景与核心突破**  #### **(一) 传统LLMs的局限性**  大型语言模型（LLMs）作为人工通用智能（AGI）的关键工具，面临两大核心挑战： - **能效问题**：部署成本高，计算和内存消耗巨大，限制基础设施化潜力。 - **可解释性不足**：决策过程不透明，高风险领

## 正文

[![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1b3c280377ba3201b7e6d06636b8ec95?Expires=1780062447&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=iGGv50anvz%2FI8rsDwhjIWqTpfdg%3D)](https://www.scichina.com/meeting-intro)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe2bfdae2ae97b6d0714de01fae7edb31?Expires=1780062447&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=SBPb%2FdeqWidIh1RIVOADacIckwE%3D)

近日，中国科学院自动化研究所**李国齐**、**徐波****团队**在**《国家科学评论》**（*National Science Review*,
NSR）上发表论文，**提出了一种神经形态脉冲大语言模型（NSLLM）**，通过借鉴神经科学原理，提升了大型语言模型（LLMs）的能效和可解释性。此项研究不仅为高效AI的发展开辟了新方向，还为下一代神经形态芯片的设计提供了宝贵的见解。

该研究由多个国内外科研机构合作完成，包括中国科学院自动化研究所、天桥脑科学研究院尖峰智能实验室、北京智源人工智能研究院、北京中关村学院、加利福尼亚大学、清华大学、北京大学、陆兮科技、悉尼大学、香港理工大学、超威半导体公司、中国科学院大学、宁波大学等。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fab72de259b9c42f986a44682c362e0bd?Expires=1780062447&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ASFrOVQ%2BPRqWhTYw9B1xEw1Yj9o%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7e3b00a96a8df59c7ce9e69fd786f77d?Expires=1780062447&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=y6%2BUSP2BbSNr3m13e%2Fu832CoQKs%3D)

**NSLLM联系大模型与神经科学**

LLMs已成为实现人工通用智能（AGI）的关键工具。然而，随着用户群体的规模扩大及使用频率增加，这些模型的部署带来了显著的计算和内存成本，限制其作为人类社会基础设施的潜力。此外，现有LLMs普遍缺乏可解释性，决策和优化过程的不透明使得其在医疗和金融等高风险领域的应用难以保证可靠性和公平性。

相比之下，人脑在执行复杂任务时的功耗不足20瓦，且展现出惊人的透明度。这一对比凸显了LLMs与人类认知之间的差距，带来了双重挑战：一方面，亟需提升LLMs的计算效率，以提升能效并节约资源；另一方面，需提升模型的可解释性，从而加深对大规模系统中各组件相互作用和功能的理解。

为突破上述跨学科交叉瓶颈，该研究提出了一种学科统一的框架，**通过执行整数脉冲计数-二值脉冲转换和脉冲线性注意力机制，将传统LLMs转化为NSLLMs，从而链接神经科学与大语言模型**，为将神经科学工具应用于LLMs提供了平台。通过引入整数训练二值推理，标准LLM的输出被转化为脉冲格式，这使得神经科学工具能够分析信息处理过程。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0c467711219ab06bc912fa8cfd7a5e8c?Expires=1780062447&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=f%2B4DErpB5mmxLLQmBDZT8%2BtQwUc%3D)

NSLLM：从大语言模型到神经形态架构的高效处理框架

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7e3b00a96a8df59c7ce9e69fd786f77d?Expires=1780062447&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=y6%2BUSP2BbSNr3m13e%2Fu832CoQKs%3D)

**超低功耗软硬协同定制MatMul-Free LLM**

为验证能效，该研究在FPGA平台上定制了十亿参数量级的无矩阵乘法（MatMul-Free）计算架构。

具体地，该研究通过逐层量化策略和层级灵敏度度量，评估层级对模型量化损失的影响，从而配置最优混合时间步脉冲模型，在低比特模型中实现了竞争力的性能；通过引入量化辅助稀疏策略，调整膜电位分布，将量化映射概率向较低整数值移动，从而显著降低脉冲发放率，进一步提升模型效率。

在VCK190
FPGA上，该研究设计了MatMul-Free硬件核心，实现了在NSLLM中矩阵乘法操作的完全消除，将动态功耗降至13.849W，吞吐量提升至161.8
token/s。与A800 GPU相比，该方法的**能效、内存和推理吞吐量分别提高了19.8****、21.3****和2.2倍****。**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe80b9c57d8c29369386360de58f1a559?Expires=1780062447&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=w3P92a26Uclvhzsj3O71U63vjGg%3D)

NSLLM在FPGA平台上的硬件核心设计

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7e3b00a96a8df59c7ce9e69fd786f77d?Expires=1780062447&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=y6%2BUSP2BbSNr3m13e%2Fu832CoQKs%3D)

**脉冲神经群体增强可解释性**

通过NSLLM框架将LLMs的行为转化为神经动力学模型（例如，脉冲列），可以分析其神经元的动态（如通过Kolmogorov-Sinai熵度量的随机性）以及信息处理的过程（如Shannon熵和互信息）。这有助于解释NSLLM的计算角色。

实验结果表明，在处理无歧义文本时，模型能够更有效地进行信息编码，从而区分含歧义文本与无歧义文本。例如，中间层在处理含歧义文本时呈现更高的归一化互信息；AS 层表现出独特的动态特征，显示其在稀疏信息处理中的作用；FS 层的 Shannon 熵更高，表明其具备更强的信息传递能力。此外，互信息与 Shannon 熵的正相关也说明，高信息容量的层更擅长保留输入的关键信息。

**因此，通过将神经动力学与信息度量相结合，该框架为LLM机制提供了生物学上可解释的见解，同时有效减少了数据需求。**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff35c940bc7cc2d455fd337b9fbc971d4?Expires=1780062447&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=V2xvOC0q0kHgoFjeW5vKgpgttEA%3D)

NSLLM的神经动力学分析

神经科学的研究表明，人脑通过稀疏和事件驱动计算优化能耗，促进信息传递，并增强系统的可解释性。基于这一思路，该团队构建了一个跨学科的统一框架，提出了能够替代传统 LLMs 的神经形态方案，并在常识推理以及更复杂的大模型任务中（如阅读理解、世界知识问答、数学等）保持了与主流同规模模型相当的性能表现。**所提出的框架不仅推动了高效AI的前沿发展，为大语言模型的可解释性提供了新视角，并为未来神经芯片的设计提供了宝贵的见解。**

---

了解详情，请阅读原文

 [点击下方链接或阅读原文] ▼

Neuromorphic spike-based large language model

National Science Review, nwaf551,  

<https://doi.org/10.1093/nsr/nwaf551>

[![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0b926e489f3862a6979b8d0094c07b79?Expires=1780062447&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=v82bVl3zBE6llaU7XgjyeqGl8vA%3D)](https://shop139094451.m.youzan.com/wscgoods/detail/1y4l4zr3sh5zv5r?banner_id=f.129815130%7Etag_list_top.9%7E1.3%7EJXuXMnq3&slg=tagGoodList-default%2COpSortBottom%2C408491578%2CabTraceId&components_style_layout=undefined&reft=1710136839552&spm=f.129815130&sf=qq_sm&form=kdt)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F968953184ccc907b921d4b11a647c419?Expires=1780062447&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=uX9c%2FcBX8sICqzeoFn17k8KaPN0%3D)

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 09:47*

---
## 相关笔记 (AI 自动关联)
- [[神经形态脉冲大语言模型_NSLLM__连接AI与神经科学的突破性研究]]
- [[神经形态脉冲大语言模型（NSLLM） 李国齐、徐波等NSR]]

> [!note]- 可能重复: [[神经形态脉冲大语言模型_NSLLM__连接AI与神经科学的突破性研究]] (相似度: 96%)
