---
title: "Compute-in-memory implementation of state space models for event sequence processing（事件序列处理的存算一体状态空间模型实现）"
source: "https://mp.weixin.qq.com/s/wgKxlazWTLRKIfOytYSCmw"
created: 2026-01-13
note_id: "1898668869624797432"
tags:
  - "AI链接笔记"
  - "存算一体"
  - "状态空间模型"
  - "事件序列处理"
  - "get-笔记"
  - "AI研究"
---

# Compute-in-memory implementation of state space models for event sequence processing（事件序列处理的存算一体状态空间模型实现）

## 摘要

### **📋 研究背景与核心问题**  长序列建模是人工智能与神经形态计算的核心任务。**传统卷积与Transformer在事件驱动数据处理上存在架构不匹配与能效瓶颈**。密歇根大学（University of Michigan）卢伟教授团队提出一种**在存算一体硬件上实现状态空间模型的策略**，

## 正文

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5788a32604e1faf4bcf3fbd8be4830b3?Expires=1780061401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=y%2BW0dzcK0WEC53zEixQINuy7xZ8%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9e7e3f6c23ede198cd685afee24d47dc?Expires=1780061401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=RU%2BQt%2BArpieR97Ufz8aD3ZZ5spo%3D)

长序列建模是人工智能与神经形态计算的核心任务。传统卷积与 Transformer 在事件驱动数据处理上存在架构不匹配与能效瓶颈。密歇根大学（University
of
Michigan）卢伟教授团队提出一种 **在存算一体硬件上实现状态空间模型的策略**，通过重新参数化为实数系数与共享衰减常数，结合忆阻器的短时记忆效应，实现异步事件驱动的实时处理。该方法在语音与视觉事件流任务中表现出高精度与高能效，展示了事件序列处理的新路径。

**⚡ 一句话**

通过 **状态空间模型与存算一体硬件的协同设计**，本文实现了事件驱动的高效序列处理。**关键认知在于：利用器件的物理衰减特性即可原生实现状态演化，从而突破传统算法与硬件的耦合瓶颈**。

**🔑 研究亮点**

* **方法突破**：将状态空间模型重新参数化为实数系数与共享衰减常数，简化硬件实现。
* **硬件创新**：利用 RRAM 芯片执行向量矩阵乘法，WOₓ 忆阻器实现短时记忆衰减。
* **性能提升**：在语音与视觉事件流任务中达到高精度与高能效。
* **异步处理**：完全事件驱动，无需时钟同步，保持稀疏性与低延迟。
* **应用潜力**：为实时事件流处理与神经形态计算提供新架构。

**📊 图示要点**

* **图 1｜事件驱动状态空间模型架构** 
  展示整体网络架构，包括通道嵌入层与堆叠的状态空间模块。嵌入层将输入事件映射到高维状态空间，单个模块通过状态节点的指数衰减与输入投影实现异步处理，只有事件到来时才触发计算。

  ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F14be608191f933e82e4df0ff3901e12d?Expires=1780061401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=bUxW7scpHp%2FzJeC6FJj%2Fj5%2BDJE4%3D)
* **图 2｜状态空间模块的硬件实现**  展示基于 RRAM 存算一体芯片的向量矩阵乘法，以及 WOₓ
  忆阻器的短时记忆衰减行为。实验结果表明，硬件能够准确实现状态更新方程，验证了物理器件在异步状态演化中的可行性。

  ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F06083c439f0fe9f868723a985cd581eb?Expires=1780061401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=j6%2FAjSvaFuOugrCIdMQ%2BGg4e33c%3D)
* **图 3｜模型深度与衰减参数对性能的影响** 
  展示不同数量的状态空间模块在多类事件驱动数据集上的分类准确率变化，以及固定与自由学习衰减参数的对比。结果表明，合理的深度与衰减配置能显著提升模型性能。

  ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fdd3e7754b05c60e7036275760948bf7f?Expires=1780061401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=SoGwZREcYPYl3JeupcVj7DoO%2Frc%3D)
* **图 4｜硬件架构与功耗分布**  展示在语音事件数据集上的硬件实现架构，包含 LUT、RRAM
  阵列、ADC、状态节点与加法器等组件，并给出各部分功耗分布，说明系统的能效优势。

  ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff5b238a474935ea9c74e341e8e93edfb?Expires=1780061401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=MGxbTAzAwiTAGUB5Z5GC3fi5UZM%3D)

**🧠 结论与展望**

本文提出的存算一体状态空间模型实现，充分利用器件物理特性完成状态演化，突破了传统卷积与 Transformer 在事件驱动处理上的限制。未来方向包括：

* **更大规模集成**：扩展至更复杂的事件流与多模态任务。
* **跨领域应用**：在智能视觉、语音识别与传感器数据处理中的推广。
* **能效优化**：进一步提升器件设计与电路协同，降低功耗。

这一成果为事件序列处理与神经形态计算提供了新范式，展示了存算一体硬件在下一代人工智能中的巨大潜力。

文章信息：

Zhang, X., Hu, M., Lu, S. *et al.* Compute-in-memory implementation of state space models for event sequence processing. *Nat Commun* (2026).

https://doi.org/10.1038/s41467-025-68227-w

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1b819bcf5e43a566001c2468534ad0f9?Expires=1780061401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=RpfeAVAuMzFAgysjR361ST4fD8o%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fef98d0fb6f868bf8a2542eec274ed0be?Expires=1780061401&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=qbxkHU1EYXCqYOrNXKXxCEWWueU%3D)

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 09:30*

## Related Notes

- [[AgentEvolver vs AlphaEvolve：AI自我进化的两条核心路线对比 🧠]]
- [[AI编码代理的质的飞跃：v3.3透明化与v3.4连续性技术解析]]
- [[DARPA人工智能与自主系统项目深度研究报告：以“第三波AI”为核心的军事智能革命]]
