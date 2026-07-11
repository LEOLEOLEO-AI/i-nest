---
title: "OpenAI 首款定制芯片 Jalapeño 发布：840mm² 巨 die、6 颗 HBM、9 个月流片"
source: "https://mp.weixin.qq.com/s/Zub0sS5HGkOPCqirCx70jQ"
author:
  - "[[Sven]]"
published:
created: 2026-07-05
description: "OpenAI首款自研AI芯片发布，840mm²巨die剑指NVIDIA"
tags:
  - "clippings"
---
Sven 有料文字 *2026年6月29日 22:49*

2026 年 6 月 24 日早上，OpenAI 不再只是一家模型公司了。

在 Greg Brockman 主持的官方播客里，OpenAI 正式揭晓了它的第一颗定制芯片—— **Jalapeño** （墨西哥辣椒）。这不是一个 PPT 概念，也不是一个"我们在考虑"的路线图条目。工程样片已经在实验室里跑着 GPT-5.3-Codex-Spark 的生产级推理负载，跑在目标频率上，跑在目标功耗范围内。

这颗芯片的使命非常明确： **让 ChatGPT 和 Codex 的推理成本降下来，同时摆脱对 NVIDIA GPU 的单一依赖。** 而它的硬件规格，比大多数人预想的要激进得多。

先从物理参数说起。\*

根据半导体分析机构对已公开的晶圆和封装图像的逆向分析，Jalapeño 的 compute die 面积约为 **840mm²** （25.46mm × 33mm）。这个数字什么概念？它几乎顶到了 EUV 光刻机的 reticle limit（约 858mm²）——也就是单次曝光能制造的最大芯片尺寸。

840mm² 是什么级别？NVIDIA H100 的 die 大约 814mm²，而 H100 是一颗训练+推理通吃的通用 GPU。Jalapeño 声称自己 **只做推理** ，却把 die 做到了训练芯片的规模。这不正常。一颗纯粹的推理 ASIC，理论上可以做得更小、更省电。OpenAI 为什么反其道而行之？

答案藏在它的封装里。

Jalapeño 的完整封装包含： **1 个大型 compute chiplet + 6 颗 HBM 内存堆叠（很可能是 HBM3E）+ 1 个 I/O die + 2 个结构性 dummy die** 。6 颗 HBM 的配置，意味着内存带宽的需求极为巨大——这恰恰是 LLM 推理的瓶颈所在。每个 token 的生成都需要在内存和计算单元之间搬运海量的模型权重。Jalapeño 把 die 做得巨大、把 HBM 堆到 6 颗，本质上是在说： **我们要让数据搬运的距离尽可能短，搬运的通道尽可能宽。**

这不是一颗"够用就行"的推理芯片。这是一颗按照 OpenAI 未来几年模型路线图的反向规格定制的芯片。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/xpUKMK417M1r2nJmHKjl1urYiby8eEbzllMGuuCRjd4UgVv07RMDWiazlUcQVlpKNGwd6Yv4Dmn9okUrGW0Gnn2pg4CTyatK7u9GmMSp9mCGs/640?from=appmsg&watermark=1#imgIndex=0)

## 9 个月，从设计到流片

更让人震惊的是时间线。

从设计启动到 tape-out（流片），Jalapeño 只用了 **9 个月** 。在高性能先进半导体领域，这被认为是"有史以来最快的 ASIC 开发周期"。作为对比，一颗典型的服务器级芯片从架构设计到流片通常需要 18-24 个月。

OpenAI 是怎么做到的？答案很讽刺： **用 AI 设计 AI 芯片。**

OpenAI 明确表示，他们自己的模型被大量用于芯片设计和优化的加速——从布局布线的自动化，到时序收敛的预测，再到功耗分布的分析。这形成了一个奇妙的闭环：OpenAI 的模型正在帮助设计下一代运行 OpenAI 模型的硬件。

还有一个原因：Jalapeño 是一颗"干净纸面设计"（blank-slate design），不是从某个已有的 GPU 或加速器架构魔改而来的。这意味着团队不用背负任何历史兼容包袱——不需要支持 CUDA，不需要兼容旧的指令集，不需要考虑图形渲染管线。他们只为一个目标优化： **Transformer 架构下的 LLM token 生成。**

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/xpUKMK417M1EANj6rPteoquuWKTwIbCYlS7XRCibLINLXtydaOOibo8LC7EmIgIRYNB8PJwcF4MBlTwKoNuHETLib10T0BC4edS1K4EVAHM7B4/640?from=appmsg&watermark=1#imgIndex=1)

## 架构哲学：让每一瓦特都花在推理上

OpenAI 在发布中强调了一个关键的设计理念： **"平衡资源"（Balanced Resources）。**

传统的 AI 芯片往往在某个维度上"瘸腿"——要么算力过剩但内存带宽跟不上，要么内存够大但互联延迟太高，导致真实利用率远低于理论峰值。Jalapeño 的设计目标是把三个维度拉到同一个水平线上：

1. 1\. **计算密度** ：针对 Transformer 的矩阵乘法和注意力机制做硬件级优化，大概率采用类 systolic array 的大规模脉动阵列架构
2. 2\. **内存带宽** ：6 颗 HBM 堆叠，为模型权重的流式读取提供足够宽的通道
3. 3\. **网络互联** ：集成了 Broadcom 的 Tomahawk 交换芯片技术，在数据中心级别做高带宽低延迟的跨芯片通信

OpenAI 声称，这种平衡设计能实现 **"真实利用率远更接近理论峰值"** 。翻译成人话就是：同样标称的算力，Jalapeño 实际能多跑出不少有效吞吐。

此外还有一条令人印象深刻的声明：Jalapeño 的设计目标之一，是 **把模型计算过程中的数据移动降到最低** 。数据搬运是 AI 推理最大的能耗来源之一——从 HBM 搬到计算单元，从计算单元搬回 HBM，每一步都在烧电。Jalapeño 的做法可能是把更多计算逻辑物理上靠近内存控制器，减少往返路径。

## 性能：谨慎承诺，但数字诱人

目前披露的性能数据不多，但已有的声明值得认真对待：

- • **每瓦性能** ："显著优于当前最先进的替代方案"（指 NVIDIA GPU 和 Google TPU）
- • **单位 token 成本** ：比标准 AI GPU 降低约 50%
- • **延迟表现** ：目标是在保持接近 NVIDIA Blackwell 级别吞吐量的同时，把延迟降到专用推理系统的水平
- • Broadcom CEO Hock Tan 更直接："性能匹敌 NVIDIA Blackwell 芯片和 Google TPU"

这些数字目前都没有独立第三方的基准测试佐证——OpenAI 表示详细的技术报告将在"未来几个月内"发布。但"单位 token 成本降低 50%"这个说法值得关注。如果属实，这意味着 ChatGPT 和 Codex 的运营利润可以直接翻倍，或者降价一半仍维持当前利润。

还有一个小道消息不容忽视：工程样片已经在跑的负载不是随便一个老模型，而是 **GPT-5.3-Codex-Spark** ——这是 OpenAI 最新的面向代码和智能体工作负载的模型。这意味着 Jalapeño 的架构至少已经经过了一轮真实场景验证，不是只在仿真器里跑过一个矩阵乘法。

## 战略逻辑：垂直整合的终极形态

Jalapeño 的意义不止于一颗芯片。它代表 OpenAI 走到了一条不归路上： **全栈垂直整合。**

OpenAI 自己的话讲得很清楚：他们"不仅在开发前沿模型或在其上构建产品；还在设计其下方的完整基础设施"。这句话里的每一个词都在生效——芯片架构、内核驱动、内存系统、网络调度、部署系统、产品体验，全部自研。

这是一条只有极少数公司走过的路。Apple 走了（A 系列、M 系列芯片），Google 走了（TPU），Amazon 走了（Trainium、Graviton）。但 OpenAI 的不同之处在于：它的时间窗口极其紧迫。它不是一家成立了 20 年的消费电子巨头，也不是一家有云计算现金流做后盾的互联网公司。它是一家规模疯狂增长的 AI 公司，burn rate 让硅谷都瞠目结舌。它必须尽快让推理成本降下来。

Jalapeño 是这条路上的第一步，但绝不是最后一步。OpenAI 已经明确表示这是"多代路线图"的第一代，后续加速器已经在规划中。

合作伙伴的选择也很微妙。 **Broadcom** 负责设计协作， **Celestica** 负责制造， **Microsoft** 是首期规模部署的合作伙伴。这个三角关系里有太多值得玩味的地方——特别是 Microsoft 的角色。Microsoft 是 OpenAI 最大的投资人和云基础设施提供方，但它自己也在自研 AI 芯片。未来 Microsoft 会选择在数据中心部署 OpenAI 的 Jalapeño 还是自己的芯片？或者两者兼而有之？这个问题目前没有答案。

## NVIDIA 会慌吗？

最直接受到冲击的无疑是 NVIDIA。

OpenAI 一直是 NVIDIA 最大的单一 GPU 客户之一。如果 OpenAI 开始大规模在自己的推理负载中部署自研芯片，这意味着 NVIDIA 失去了一个超级大客户的部分订单——而且是最具利润空间的推理订单。

但说"NVIDIA 完了"是幼稚的。目前来看，Jalapeño 只覆盖推理环节，而 GPU 预训练这一块——需要极高的通用计算能力和成熟的软件生态——仍然是 NVIDIA 的绝对主场。OpenAI 自己也承认，计算密集型的预训练工作"可能会继续依赖 NVIDIA 硬件"。

更关键的是 CUDA 生态的护城河。NVIDIA 花了 15 年建立的开发者生态、库、编译器、优化工具链，不是一颗芯片就能替代的。OpenAI 可以为自己优化芯片，但全球成千上万的 AI 公司和研究机构不会一夜之间抛弃 CUDA。

但这确实是一个信号。当最大的 GPU 买家开始自己做芯片，而且做出来的东西至少账面参数不输 Blackwell，整个行业的采购策略都会重新评估。Jalapeño 更像是一个 **"存在性证明"** ——证明"AI 公司自研推理芯片"这条路是走得通的。一旦 OpenAI 证明了，Anthropic 会不会跟进？Midjourney 会不会？Runway 会不会？

## 风险：过度优化的陷阱

Jalapeño 最大的风险不在硬件本身，而在它的设计哲学： **为今天的架构高度优化，可能成为明天的包袱。**

Transformer 架构是当前 LLM 的基础，但整个行业都在疯狂探索后 Transformer 的可能性——状态空间模型（SSM）、RWKV、RetNet、Liquid Neural Networks……如果 3 年后的主流模型架构不再是 Transformer，一颗深度绑定 Transformer 推理的 ASIC 会面临严重的灵活性危机。

Google TPU 走过类似的路。第一代 TPU 只做推理，后来的版本才逐步加入训练能力和通用性。OpenAI 能不能复制这条路线，在第一代推理芯片成功之后迅速迭代出更有弹性的架构？答案取决于它能不能留住顶级的芯片设计人才——在硅谷半导体圈，这个竞争不比 AI 研究圈轻松。

另一个风险是供应链。一颗 840mm² 的巨 die 在先进制程上的良率不会太好看。即使采用 chiplet 设计分摊了部分风险，核心 compute die 仍然是巨大的单体芯片。一旦良率或产能出问题，OpenAI 没有任何自研芯片的"备胎"——NVIDIA 还是会接到加急订单。

## 结语

OpenAI 发布第一款芯片这件事，放在两年前是不可想象的。那时人们还在争论"AI 公司应该专注于模型还是应该垂直整合"。今天回头看，这个争论已经被 Sam Altman 和 Greg Brockman 的决心彻底终结了。

Jalapeño 的 840mm² die、6 颗 HBM、9 个月的流片速度、AI 辅助设计的完整闭环——每一项都在告诉行业： **AI 公司的竞争已经卷到了硅片层面。** 谁能控制芯片，谁就控制了推理成本；谁控制了推理成本，谁就抓住了 AI 规模化盈利的关键钥匙。

但这把钥匙能不能真打开盈利的大门，需要等到 2026 年底首批部署后才能知道答案。在此之前，Jalapeño 是一个引人入胜的故事——关于一家软件公司如何学习制造硬件，关于一个行业如何在神经网络和硅晶体管之间架起桥梁。

而这可能只是 AI 芯片大战的真正序章。

## AI 摘要

OpenAI releases its first custom chip, Jalapeño, with an 840mm² die, 6 HBM stacks, and 9-month production cycle.
