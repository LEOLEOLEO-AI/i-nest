---
title: "MiroThinker 1.5：开源搜索增强型推理模型深度解析"
source: "https://mp.weixin.qq.com/s/gRvKoSTpelsDLaUQJb0F3w"
created: 2026-01-10
note_id: "1898412129363695840"
tags:
  - "AI链接笔记"
  - "MiroThinker"
  - "开源AI模型"
  - "搜索增强型推理"
  - "get-笔记"
  - "AI研究"
---

# MiroThinker 1.5：开源搜索增强型推理模型深度解析

## 摘要

### **🔍 项目核心定位（概述）**  **MiroThinker**是一款**开源搜索增强型推理模型**，其核心能力在于模拟人类研究流程：通过自主调用搜索工具、运行代码，实现复杂问题的多步骤拆解与推理，突破普通聊天机器人依赖记忆回答的局限。官方目标是对标OpenAI Deep Research

## 正文

今天分享一个叫MiroThinker的开源项目，这是个「搜索增强型推理模型」——
简单来说，它能像人做研究那样，自己调用搜索工具、运行代码，一步步拆解复杂问题，而不是像普通聊天机器人那样只能凭记忆回答。

![alt](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb1417c5f118601558041cb27a2e063f6?Expires=1780061421&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=5uHQJOHEz85iq9DJdk5szoTQuM4%3D)

现在很多AI模型虽然能聊天，但碰到需要实时信息（比如查最新论文）、复杂计算（比如数据分析）或者多步骤推理（比如写行业报告）的任务就容易「卡壳」。MiroThinker的目标就是填补这个空白，官方说想对标OpenAI
Deep Research和Gemini Deep Research的深度研究能力，但关键是——它完全开源。

最新的1.5版本是2026年1月刚发的，核心改进叫「交互式扩展」（interactive
scaling），简单理解就是让模型更擅长和工具「互动」：比如搜索到信息后判断够不够，不够就继续搜；代码运行出错了能自己调试。具体看几个硬指标：

* **上下文窗口256K**：相当于能一次性处理几十万字的内容，长篇论文、多轮对话都没问题。
* **单次任务最多400次工具调用**：比早期版本翻了一倍，意味着能完成更复杂的研究流程，比如从搜索文献、数据爬取到代码分析一条龙。
* **性能数据**：在HLE-Text（一个综合研究能力测评集）上得分39.2%，BrowseComp（英文网页理解）69.8%，中文的BrowseComp-ZH更是到了71.5%，GAIA-Val-165（通用AI能力测评）80.8%。官方特别提到，30B参数的版本性能超过了Kimi-K2-Thinking，而参数规模只有对方的1/30，性价比挺高**。**

MiroThinker不只是一个模型，而是一套研究工具链：

* **MiroFlow框架**：开源的研究代理框架，能复现它在各种测评集上的成绩，开发者可以基于这个二次开发。
* **MiroVerse数据集**：14.7万条训练样本，包含中英文的工具使用案例，这对模型能力提升很关键。
* **MiroTrain/RL训练基建**：支持高效训练，所以模型迭代速度比较快，从v0.1到v1.5也就半年多。

官方提供了在线Demo（dr.miromind.ai），可以直接体验。如果想本地部署，需要准备几个API
key：Serper（谷歌搜索接口）、Jina（网页抓取）、E2B（代码沙箱），这些服务都有免费额度，倒不用花太多钱。不过技术门槛不算低，需要懂点Python环境配置。

作为开源项目，MiroThinker的优势很明显：透明、可定制，性能在同类开源模型里确实领先。尤其对中文任务的优化（BrowseComp-ZH得分71.5%），比很多只侧重英文的工具更接地气。但要说替代商业工具，可能还差点意思——比如OpenAI的Deep
Research背后有更强的算力和数据支撑，不过MiroThinker给了研究者一个「不被黑箱绑架」的选择。

仓库地址：

https://github.com/MiroMindAI/MiroThinker

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 09:30*

## Related Notes

- [[从器件特性到网络动力学演化机理研究]]
- [[2026年1月9号 日记]]
- [[智能本质新范式：高维几何结构与通用“心智”诞生猜想]]
