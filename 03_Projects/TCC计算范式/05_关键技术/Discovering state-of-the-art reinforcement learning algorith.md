---
title: "Discovering state-of-the-art reinforcement learning algorithms：算法基因演化框架"
source: "https://mp.weixin.qq.com/s/zoMxF2u44Wdt8rFNbHCYNw"
created: 2025-12-19
note_id: "1896334961846350680"
tags:
  - "AI链接笔记"
  - "强化学习（RL）"
  - "算法基因演化"
  - "AutoML"
  - "get-笔记"
  - "技术实践"
---

# Discovering state-of-the-art reinforcement learning algorithms：算法基因演化框架

## 摘要

### **🏆 核心创新点**  #### **(一) 算法-即-基因（Algorithm-as-Gene）** - **核心思想**：将整套强化学习（RL）更新规则编码为一段可微分的「伪代码向量」，包含**损失函数、超参数、梯度组合、目标网络、正则项**等50余个算子，作为「DNA」进行变异、重组

## 正文

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F04061a5af3bdff8b708be774f931c8b3?Expires=1780062440&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=XMDVI1wzeCiDvy2tXiPGarBb8Ck%3D)

题目：Discovering state-of-the-art reinforcement learning algorithms

论文地址：https://doi.org/10.1038/s41586-025-09761-x![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff1578d07f542a2d56ff61d5870dc8a95?Expires=1780062440&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=JoliiOd6UZvfSpWO0EycTdrBOO4%3D)

# 创新点：

• 算法-即-基因把整套 RL 更新规则写成一段可微分的「伪代码向量」——包括损失函数、超参数、梯度组合、目标网络、正则项等 50 余个算子——直接当 DNA
进行变异、重组与选择。传统 AutoML 只搜超参，这里连「公式本身」都进化。

• 快速「胚胎」淘汰 + 精确「成体」评估 先用 3×10⁵ 步的廉价环境（Brax 物理引擎）把 10⁴ 条基因过滤到 10² 条，再把幸存者放到完整
Atari 100k 与 DMControl 上跑 5×10⁷ 步做最终遴选，兼顾搜索广度与精度，总计算量控制在 5k
TPU-days（比蛮力搜索低两个数量级）。

# 方法：

本文采用“算法即基因”的双层演化框架：先把整个强化学习更新规则编码成一段可微分的伪代码向量，再在第一层用廉价模拟环境对上万条基因做快速胚胎淘汰，第二层把幸存者送入完整任务做精确成体评估，通过可微分变异算子在嵌入空间里不断重组、突变与选择，最终让算法自己把自己进化成新的
SOTA，而人类只提供最小限度的算子库和评估协议。整个流程中初代基因池完全随机，几十代后就能自动拼出 SAC 的温度调节、DrQ 的数据增强、DDPG
的双网络，还能长出人类从未想到的双时间尺度 Q-target 平滑与熵门控停止梯度。

## 「算法基因」双层演化流程图：从伪代码向量到 SOTA 强化学习

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbde96242a495ce303e6d07986cd7b9f2?Expires=1780062440&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=jpN6s%2FexzRpaOiMonZ5tXTj4SBc%3D)

本图整个研究流程最左侧是把 RL 更新规则拆成 50 余个可微算子并编码成一条“算法基因”向量；接着这条基因被送入快速胚胎层——在 Brax 廉价物理引擎上只跑
30 万步，对 10⁴ 条基因做并行筛选，存活率约 1 %；幸存基因进入右侧成体评估层，在完整 Atari 100k 与 DMControl 上跑 5 000
万步，真实性能被写回“适应度”；中央用渐变色箭头表示可微分变异算子在嵌入空间里对父代基因做梯度插值与噪声扰动，生成子代；整个循环用螺旋箭头包回起点，暗示多代演化后自动涌现的更新规则已包含人类
SOTA 的组件组合。

## 「算法基因组」可视化：进化自动重拼人类模块并诞生两种全新结构

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1dfbe570d599d3aba5c107bee62bdbbf?Expires=1780062440&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=S%2FOFXDO7Q%2BGRrYdRwxMV1oSsqKI%3D)

本图最终选出的 NGA-Nature“算法基因”展开最上行是按执行顺序排列的 50 余个算子嵌入向量，颜色深浅表示该算子在历代中的保留频率，可见 SAC
温度调节、DrQ 数据增强、DDPG
双网络等人类熟悉模块被原样保留但位置被重新排序；中间两行高亮两段之前未出现的连续片段——一段是“快-慢双指数移动平均”组成的 Q-target
平滑器，另一段是以策略熵为门的“自适应停止梯度”开关，二者在右侧热图里显示对最终性能贡献最大；最下行把基因序列直接映射回可执行伪代码，证明进化结果不仅是数值权重，而是可读、可迁移的结构性创新，任何人都可以把这两段新片段剪贴到现有算法中获得一致提升。

## 「零人类先验」跨域泛化：同一副进化出的算法在 Atari、连续控制、Procgen、真机四足上全面碾压人工 SOTA

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F28153ac96a0b30f8b0bec717e02b07ee?Expires=1780062440&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=1hNcPgXw4vBYh2aHqBQ2D9wE8xk%3D)

本图把 NGA-Nature 与 SAC、DrQ、DreamerV3 等人类调参冠军同时放进离散 Atari100k、连续 DMControl、程序化
Procgen 以及真实 Unitree A1 四足机器人四个完全不同模态的任务集合，所有轴统一用人类标准化得分百分比标示，结果 NGA-Nature
的封闭面积在每一块雷达图里都几乎填满外圈，而人类算法出现明显凹陷；下方嵌入的两张小实拍照片显示作者把进化代码直接烧进机器人树莓派，不做任何现场微调就能在草地、斜坡、石子路三种地形上把平均前进速度提高
18 %，从而用图证明：演化出的更新规则不是过拟合某个benchmark的“实验室怪物”，而是真正跨任务、跨实现、跨物理世界的通用强化学习新范式。

## 实验

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb47fa434721d7d0c7fde4a06b1d7cf9f?Expires=1780062440&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=JPDjb4clDreJQke7H4u%2FF6rFrjY%3D)

该表格把 NGA-Nature 拆成“基因片段”做外科手术式消融：从左到右依次剃掉双时间尺度 Q-target 平滑、熵门控停止梯度、DrQ 式数据增强、SAC
温度调节、双网络结构等组件，再于 Atari100k、DMControl、Procgen 三大基准重训，结果人类熟悉的“经典模块”一旦移除分数仅掉 1–3
分，而两项进化才发现的新机制只要缺一个，人类标准化得分立刻掉 12–15 分，直接跌出 SOTA 梯队；最后一行把这两项新片段单独嫁接到原始 SAC
身上，立刻在 26 个任务里平均提升 7.8 %，证明表格里的数字不是算法整体的笼统优势，而是精确指向进化自动发现且可即插即用的结构性创新。

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 09:47*