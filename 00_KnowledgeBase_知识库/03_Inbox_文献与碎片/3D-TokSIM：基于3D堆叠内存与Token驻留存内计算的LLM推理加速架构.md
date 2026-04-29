---
title: "3D-TokSIM：基于3D堆叠内存与Token驻留存内计算的LLM推理加速架构"
source: "https://mp.weixin.qq.com/s/FCi1feyd6POY1SOiToqg2g"
created: 2025-12-08
note_id: "1895305012582679496"
tags:
  - "AI链接笔记"
  - "LLM推理加速"
  - "3D堆叠内存"
  - "存内计算(CIM)"
  - "get-笔记"
  - "AI研究"
---

# 3D-TokSIM：基于3D堆叠内存与Token驻留存内计算的LLM推理加速架构

## 摘要

### **🔍 核心背景与挑战**  **大语言模型(LLM)推理瓶颈**： - **存储墙问题**：自回归解码特性导致每生成1个token需从DRAM加载完整模型参数，GPU利用率不足25%。 - **架构失衡**：3D堆叠存储虽能提供TB/s级带宽，但逻辑层设计不当会导致计算能力成为新瓶颈。  

## 正文

今天来学习北京大学黄如院士、叶乐等人在2025设计自动化顶会DAC上发表的一篇论文： 3D-TokSIM: Stacking 3D Memory
with Token-Stationary Compute-in-Memory for Speculative LLM Inference
3D-TokSIM：基于3D堆叠内存与Token驻留存内计算的投机性LLM推理架构 DOI: 10.1109/DAC63849.2025.11132883

### ****需要做神经形态应用的老师欢迎后台获取联系方式，CNN/储备池/SNN/光谱仪/神经元/树突/轨迹衰减......各类任务均可实现****

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7d8dc46df4825ce0f3f784a7c0b87ebc?Expires=1780063514&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=jf7BT8bRdjoxtTtN%2BkpudF4G8GI%3D)

背景介绍

   
大语言模型推理面临严重的存储墙问题。由于自回归解码的特性，每生成一个token都需要从DRAM加载完整的模型参数，导致GPU这类计算密集型架构的利用率不到25%。虽然3D堆叠存储技术可以提供TB/s级带宽，但如果逻辑层设计不当，系统仍然会被计算能力限制。

一句话解释

   
提出了3D-TokSIM的跨层架构，通过混合Bonding将DRAM垂直堆叠在逻辑芯片上，并配合Token驻留存内计算数据流，专门加速大模型的投机解码推理。

创新点一：3D堆叠设计

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F2e4a1962b08cee559634d71aa7358603?Expires=1780063514&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=%2F3Jn6H9nWY%2B29dlzgjNFDebusyA%3D)

Fig. 1 从内存受限到平衡状态  

2D-Memory: 传统架构下，内存访问耗时极长（黄色柱子高），计算单元（蓝色柱子）在等待数据，这是典型的Memory Bound。 3D-PNM:
引入3D堆叠内存后，带宽提升，但如果只做近存计算（PNM），计算本身成了瓶颈。 PNM+SD+CIM:
这是本文方案。首先用投机解码（SD）减少了解码步数，然后用存内计算加速了SD带来的并行验证计算量，最终实现了平衡。  

创新点二：推测策略

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F742a31dffeb2e67122a479799dc412fc?Expires=1780063514&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Kb29r0MImujXxD1qfqQbzdabgJg%3D)

Fig. 2  推测解码机制对比

上半部分的传统流程展示了逐步生成的串行特性，每个step只能产出一个token，t0→t1→t2→t3。这种依赖关系导致模型参数必须反复加载。下半部分的推测解码打破了这种串行依赖。高效的drafter一次性生成k个候选tokens（t1到tk），然后LLM模型并行验证这k+1个tokens（包括t0）。原本需要k步的解码被压缩成1步，代价是单步计算量变为k+1倍。

创新点三：TS存内计算数据流

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb0b10f3273ca86d8a82d1f767635fdd7?Expires=1780063514&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=d7sV%2BDtdm%2Bt1%2BGbvEK1rv%2BuGK1o%3D)

Fig. 3  Token驻留数据流逻辑差异

传统AI芯片多用权重驻留（Weight Stationary,
WS），即把权重存在SRAM里复用。但在LLM中，权重太大存不下。本文将用户输入的Token（t\_0, t\_1...t\_k）
锁在CIM阵列里。DRAM源源不断地把权重送入CIM，与驻留在里面的Token进行矩阵乘法。由于3D连接带宽极大且功耗低，这种流权重的方式反而比频繁读写SRAM更省电。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F222d5b7708e05eec4a7d83656fc0eefd?Expires=1780063514&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=YBmjLlk6tjT1%2Fnu8rdEHyc4TFkk%3D)

Fig. 8 TS与WS数据流能效对比

在投机步长k=2到10的范围内，TS相比WS始终保持更低的归一化能耗。这是因为TS避免了逻辑芯片上SRAM的频繁读写，直接利用了低功耗的3D DRAM传输。

点评：

    除了上面的创新，文章还做了比较多的工作，包括Output Buffer消除优化，Residual
Buffer优化，平衡DRAM带宽和CIM算力。目前主要限制还是基于Post-Layout Simulation，没有实际制造，缺少端到端的大模型部署验证。

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 10:05*