---
title: "MiroThinker 1.5深度解析：AI从"秒回"到"慢思考"的范式转型"
source: "https://mp.weixin.qq.com/s/lCvA_otmzzieKvcSI4-JNg"
created: 2026-01-06
note_id: "1898029309264822536"
tags:
  - "AI链接笔记"
  - "MiroThinker 1.5"
  - "深度思考型AI"
  - "搜索智能体"
  - "get-笔记"
  - "AI研究"
---

# MiroThinker 1.5深度解析：AI从"秒回"到"慢思考"的范式转型

## 摘要

### **🔍 AI搜索的进化与MiroThinker的定位（背景）**  #### **(一) 行业发展阶段** - **2024年**：AI搜索（如Perplexity）爆发，核心特征是**快速响应**。 - **2026年**：进入**深度思考型搜索智能体**时代，MiroMind团队开源的*

## 正文

如果说 2024 年是 AI 搜索（如 Perplexity）的爆发之年，那么 2026 年的开局，我们似乎迎来了一个全新的物种
— **深度思考型搜索智能体**。

我们也许早已习惯了 AI 秒回消息。如果你问
AI *“今天天气怎么样”*，它秒回是应该的。但如果你问的是一个极度复杂的商业决策、学术难题或者深度调研任务，“秒回”往往意味着不可信。

就在昨天，`MiroMind` 团队开源了他们的最新力作 — **MiroThinker 1.5**。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe82faf7f9c7130082d1500c20fd8cfdc?Expires=1780061751&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=cEp22YnOHtwOJt9uasO8lXsVNu4%3D)

它是一款超强的搜索智能体模型，至少在同类AI模型中可以说是当下最强了。

它不是那种“秒回型 AI”，而是真的会花几分钟做研究的模型。它会搜各种信息，打开几十个网页，阅读几万字的
PDF，梳理来龙去脉，最后给你一份带引用、带数据、带逻辑的完整研报。

更令人震惊的是，凭借这种“慢思考”机制，它仅用 30B 的参数量，就在深度任务上击败了庞大的 `GPT-5-High` 模型。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F870ef2a01ad7ef2fc46eb1241e424d8e?Expires=1780061751&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=7j%2FaDuUAeuZSm14pqiZ0QF3ri0Y%3D)

其 235B 版本更是跻身第一梯队。

#### 行为模式

你可以把它理解为：**一个会主动做文献综述的搜索智能体。**

它的行为模式大概是：

1. 1. 拆解问题背景
2. 2. 主动全网搜索
3. 3. 优先查阅顶级机构/权威来源
4. 4. 打开、阅读、比对多篇资料
5. 5. 交叉验证信息
6. 6. 最后才输出结论

而不是：

搜两条 → 编一段 → 直接给答案

#### 如何使用？

目前 30B、235B 模型权重已开源，并且在 Web 端可以免费体验。

Web 体验地址：https://miromind.ai

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb39d4f95f818f9f5a884b52cfdb1e2a1?Expires=1780061751&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=B41a%2FYjqbl6xJ8BkOYw47RPXjVw%3D)

大家可以尝试去问一些比较复杂甚至高深的问题，看看它的回答效果。

我这里就问一个现实的病理方面的问题，因为家里父母长时间在纺织厂上班，身体上明显出现了一些变化，所以想到这个。

*比如：长达十几年在纺织厂工作，手指经常麻木伸不开，是什么原因，有什么好的补救治疗方案？*

它会提取主要的关键要素，去全网搜索🔍（主要还是一些权威的官方的信息源）

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4074de8fd28267b880840058faba4c56?Expires=1780061751&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=jSd%2FKHcGBpl3SQHp0BhqKMQ986s%3D)

然后根据全网搜索的庞大内容，筛选和整合最有用的信息。再进一步去搜索🔍更加精准的内容。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd81bedb62b73922de05e424207ccd6e3?Expires=1780061751&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=MRH1TWkECZXdTm0a1d4Fp87TaYw%3D)

其他内容截图省略，罗列了下面的一些查找信息：

* • 纺织工人手麻的具体原因和治疗方案，特别是涉及职业病鉴定方面的信息；
* • 以及搜索职业病鉴定和赔偿相关的政策信息；
* • 查找纺织工人的具体职业病诊断标准；
* • 查找纺织厂手部职业病相关的医学文献和具体案例；
* • 还要查找一些临床案例和治疗方案
* • ...
* • 最终整合总结原因与综合治疗方案。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1b7ea9a116ea1ac66260a0a9d27f3d86?Expires=1780061751&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=qhXqk2UrRm7va68E33fnotKMaVI%3D)

整个过程起码搜索了 15 次，每一次搜索都比上一次要更加精准，越来越贴合你所想要的东西。

大家也可以前去体验试试，虽然整个过程需要好几分钟，但结果确是真实有用的。

#### 主要特点

* • MiroThinker v1.5 支持 256K 上下文窗口、长时域推理和深度多步骤分析。
* • 每个任务最多可处理 400 次工具调用。
* • 以 300 亿和 2350 亿参数规模发布，并附带一套全面的工具和工作流程，可灵活支持各种研究环境和计算预算。
* • 与外部工具和 API 无缝集成

MiroThinker v1.5 在广泛的基准测试中展现出强大的通用研究性能，在 HLE-Text、BrowseComp、BrowseComp-ZH 和
GAIA-Val-165 测试中分别取得了 39.2%、69.8%、71.5% 和 80.8% 的准确率。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbe7a80095318cc99fe41f0bbfbfc22c1?Expires=1780061751&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=XNUReFlCu1lLblbgxQ%2FPDLjsy7M%3D)

这些结果超越了以往的开源智能体，并创造了 BrowseComp 测试的世界领先性能新纪录。

总结一句，MiroThinker 1.5 的核心特点只有一个：**慢，但严谨。**

#### 写在最后

MiroThinker 1.5 的出现，标志着 AI 从 Chatbot（聊天机器人）向 Research Agent（调研智能体）的正式转型。

它不是让 AI 更会说话，而是让 AI 更像一个认真查资料的人。

MiroThinker 1.5 不会成为“全民对话模型”，但它极有可能成为搜索智能体领域的范式参考。

至少在做研究这件事上，MiroMind 给出了一个非常坚定、也非常罕见的答案。

资源链接：

> 体验地址：miromind.ai  
> GitHub：https://github.com/MiroMindAI/MiroThinker  
> 模型：htts://huggingface.co/miromind-ai/MiroThinker-v1.5-235B

 

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F2b3e4b5aea83072fe7c90de7c0586fd7?Expires=1780061751&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=YJOJqlhS4zYmnWAgrA5k273QD08%3D)

如果本文对您有帮助，也请帮忙点个 赞👍 + 在看 哈！❤️

**在看你就赞赞我！**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb4426263fc1730070f48aa41665abd4b?Expires=1780061751&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=4Moq69q67DrWzWqorFu4WvrIm1s%3D)

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 09:35*

---
## 相关笔记 (AI 自动关联)
- [[MiroThinker 1.5：开源搜索增强型推理模型深度解析]]
