# 神经形态脉冲大语言模型（NSLLM）：连接AI与神经科学的突破性研究

- **类型**: link
- **时间**: 2025-12-18 07:40:41
- **标签**: AI链接笔记, 神经形态计算, 脉冲大语言模型（NSLLM）, 低功耗AI
- **来源**: https://mp.weixin.qq.com/s/HSg8wSXYM97KsHlhzLvcUA

## 内容

### **🔬 研究背景与核心突破**

#### **(一) 传统LLMs的局限性**

大型语言模型（LLMs）作为人工通用智能（AGI）的关键工具，面临两大核心挑战：
- **能效问题**：部署成本高，计算和内存消耗巨大，限制基础设施化潜力。
- **可解释性不足**：决策过程不透明，高风险领域（医疗、金融）应用可靠性受限。

#### **(二) 创新解决方案：神经形态脉冲大语言模型（NSLLM）**

中国科学院自动化研究所**李国齐、徐波团队**在《国家科学评论》（*National Science Review*, NSR）提出**NSLLM框架**，通过以下方式突破瓶颈：
- **跨学科融合**：借鉴人脑神经科学原理（功耗<20瓦且高透明），将传统LLMs转化为脉冲神经模型。
- **核心技术**：整数脉冲计数-二值脉冲转换、脉冲线性注意力机制，实现能效与可解释性双重提升。

### **🤝 研究团队与合作机构**

该研究由**17家国内外机构**联合完成，核心单位包括：
- 中国科学院自动化研究所（主导）
- 天桥脑科学研究院尖峰智能实验室
- 北京智源人工智能研究院
- 加利福尼亚大学、悉尼大学、香港理工大学
- 清华大学、北京大学、中国科学院大学
- 陆兮科技、超威半导体公司（产业界合作）

### **⚙️ NSLLM技术架构与实现**

#### **(一) 理论框架：从连续值到脉冲域的转换**

通过**学科统一框架**实现LLMs向神经形态模型的转化：
1. **整数训练-二值推理**：标准LLM输出转化为脉冲格式，使神经科学工具可分析信息处理过程。
2. **脉冲线性注意力机制**：优化注意力计算，降低复杂度。
3. **神经动力学映射**：将模型行为转化为脉冲列，支持神经元动态分析（如Kolmogorov-Sinai熵、Shannon熵）。

#### **(二) 超低功耗硬件实现：MatMul-Free架构**

在**VCK190 FPGA平台**上定制十亿参数量级无矩阵乘法计算架构，关键指标：
- **动态功耗**：仅13.849W
- **吞吐量**：161.8 token/s
- **核心优化策略**：
  - 逐层量化与层级灵敏度度量，配置混合时间步脉冲模型
  - 量化辅助稀疏策略，调整膜电位分布降低脉冲发放率

#### **(三) 性能对比：能效革命性提升**

| 指标        | NSLLM（FPGA） | 传统方案（A800 GPU） | 提升倍数 |
|-------------|---------------|----------------------|----------|
| **能效**    | -             | -                    | **19.8倍** |
| **内存效率**| -             | -                    | **21.3倍** |
| **推理吞吐量** | 161.8 token/s | -                    | **2.2倍** |

### **🧠 可解释性增强：神经动力学分析**

通过NSLLM框架将模型行为转化为神经动力学模型，揭示信息处理机制：

#### **(一) 关键发现**
1. **歧义文本处理差异**：中间层处理歧义文本时归一化互信息更高。
2. **层功能分化**：
   - **AS层**：独特动态特征，主导稀疏信息处理。
   - **FS层**：Shannon熵更高，信息传递能力更强。
3. **信息度量相关性**：互信息与Shannon熵正相关，表明高信息容量层更擅长保留关键输入。

#### **(二) 神经科学工具应用**
- **Kolmogorov-Sinai熵**：度量神经元动态随机性。
- **Shannon熵**：评估信息编码容量。
- **互信息**：分析层间信息传递效率。

### **📝 补充细节**
- **论文信息**：标题《Neuromorphic spike-based large language model》，2025年12月4日发表于NSR，DOI: 10.1093/nsr/nwaf551。
- **技术转化价值**：为下一代神经形态芯片设计提供理论基础，推动低功耗AI硬件发展。
- **潜在应用**：边缘计算、可穿戴设备、脑机接口等资源受限场景。

## 原文

[![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1b3c280377ba3201b7e6d06636b8ec95?Expires=1776346077&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=RYXzemsIrd7eyCvA%2FgjpgahZ2gU%3D)](https://www.scichina.com/meeting-intro)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe2bfdae2ae97b6d0714de01fae7edb31?Expires=1776346077&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=u71bnOVeGgQTVtsT6N4ru3pF%2BqY%3D)

近日，中国科学院自动化研究所**李国齐**、**徐波****团队**在**《国家科学评论》**（*National Science Review*,
NSR）上发表论文，**提出了一种神经形态脉冲大语言模型（NSLLM）**，通过借鉴神经科学原理，提升了大型语言模型（LLMs）的能效和可解释性。此项研究不仅为高效AI的发展开辟了新方向，还为下一代神经形态芯片的设计提供了宝贵的见解。

该研究由多个国内外科研机构合作完成，包括中国科学院自动化研究所、天桥脑科学研究院尖峰智能实验室、北京智源人工智能研究院、北京中关村学院、加利福尼亚大学、清华大学、北京大学、陆兮科技、悉尼大学、香港理工大学、超威半导体公司、中国科学院大学、宁波大学等。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fab72de259b9c42f986a44682c362e0bd?Expires=1776346077&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=%2FAdwBKKCZ9hvOM%2FBOx8CYJ594kM%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7e3b00a96a8df59c7ce9e69fd786f77d?Expires=1776346077&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Ig0NKXAhyb4UvtoDbRhl9aEmqIY%3D)

**NSLLM联系大模型与神经科学**

LLMs已成为实现人工通用智能（AGI）的关键工具。然而，随着用户群体的规模扩大及使用频率增加，这些模型的部署带来了显著的计算和内存成本，限制其作为人类社会基础设施的潜力。此外，现有LLMs普遍缺乏可解释性，决策和优化过程的不透明使得其在医疗和金融等高风险领域的应用难以保证可靠性和公平性。

相比之下，人脑在执行复杂任务时的功耗不足20瓦，且展现出惊人的透明度。这一对比凸显了LLMs与人类认知之间的差距，带来了双重挑战：一方面，亟需提升LLMs的计算效率，以提升能效并节约资源；另一方面，需提升模型的可解释性，从而加深对大规模系统中各组件相互作用和功能的理解。

为突破上述跨学科交叉瓶颈，该研究提出了一种学科统一的框架，**通过执行整数脉冲计数-二值脉冲转换和脉冲线性注意力机制，将传统LLMs转化为NSLLMs，从而链接神经科学与大语言模型**，为将神经科学工具应用于LLMs提供了平台。通过引入整数训练二值推理，标准LLM的输出被转化为脉冲格式，这使得神经科学工具能够分析信息处理过程。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0c467711219ab06bc912fa8cfd7a5e8c?Expires=1776346077&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=qDogH39UWGw2IoO0VYJdO08n3Lw%3D)

NSLLM：从大语言模型到神经形态架构的高效处理框架

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7e3b00a96a8df59c7ce9e69fd786f77d?Expires=1776346077&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Ig0NKXAhyb4UvtoDbRhl9aEmqIY%3D)

**超低功耗软硬协同定制MatMul-Free LLM**

为验证能效，该研究在FPGA平台上定制了十亿参数量级的无矩阵乘法（MatMul-Free）计算架构。

具体地，该研究通过逐层量化策略和层级灵敏度度量，评估层级对模型量化损失的影响，从而配置最优混合时间步脉冲模型，在低比特模型中实现了竞争力的性能；通过引入量化辅助稀疏策略，调整膜电位分布，将量化映射概率向较低整数值移动，从而显著降低脉冲发放率，进一步提升模型效率。

在VCK190
FPGA上，该研究设计了MatMul-Free硬件核心，实现了在NSLLM中矩阵乘法操作的完全消除，将动态功耗降至13.849W，吞吐量提升至161.8
token/s。与A800 GPU相比，该方法的**能效、内存和推理吞吐量分别提高了19.8****、21.3****和2.2倍****。**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe80b9c57d8c29369386360de58f1a559?Expires=1776346077&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=zat%2FmjkZCK5zSj2tISBG2%2BYnq78%3D)

NSLLM在FPGA平台上的硬件核心设计

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7e3b00a96a8df59c7ce9e69fd786f77d?Expires=1776346077&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Ig0NKXAhyb4UvtoDbRhl9aEmqIY%3D)

**脉冲神经群体增强可解释性**

通过NSLLM框架将LLMs的行为转化为神经动力学模型（例如，脉冲列），可以分析其神经元的动态（如通过Kolmogorov-Sinai熵度量的随机性）以及信息处理的过程（如Shannon熵和互信息）。这有助于解释NSLLM的计算角色。

实验结果表明，在处理无歧义文本时，模型能够更有效地进行信息编码，从而区分含歧义文本与无歧义文本。例如，中间层在处理含歧义文本时呈现更高的归一化互信息；AS 层表现出独特的动态特征，显示其在稀疏信息处理中的作用；FS 层的 Shannon 熵更高，表明其具备更强的信息传递能力。此外，互信息与 Shannon 熵的正相关也说明，高信息容量的层更擅长保留输入的关键信息。

**因此，通过将神经动力学与信息度量相结合，该框架为LLM机制提供了生物学上可解释的见解，同时有效减少了数据需求。**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff35c940bc7cc2d455fd337b9fbc971d4?Expires=1776346077&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=0ehJbb7SLz0fuW53C1RgoPmxLD0%3D)

NSLLM的神经动力学分析

神经科学的研究表明，人脑通过稀疏和事件驱动计算优化能耗，促进信息传递，并增强系统的可解释性。基于这一思路，该团队构建了一个跨学科的统一框架，提出了能够替代传统 LLMs 的神经形态方案，并在常识推理以及更复杂的大模型任务中（如阅读理解、世界知识问答、数学等）保持了与主流同规模模型相当的性能表现。**所提出的框架不仅推动了高效AI的前沿发展，为大语言模型的可解释性提供了新视角，并为未来神经芯片的设计提供了宝贵的见解。**

---

了解详情，请阅读原文

 [点击下方链接或阅读原文] ▼

Neuromorphic spike-based large language model

National Science Review, nwaf551,  

<https://doi.org/10.1093/nsr/nwaf551>

[![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0b926e489f3862a6979b8d0094c07b79?Expires=1776346077&OSSAccessKeyId=LTAI5t7toTp72R3Tvd

---
**Tags:** [[BrainInspired]] [[Chiplet]]
