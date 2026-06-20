---
title: "动态自适应激活神经元晶体管（DAA-NT）在自动驾驶辅助系统中的应用研究"
source: "https://mp.weixin.qq.com/s/diaV0rlHzpD66T8HECzvKQ"
created: 2025-09-23
note_id: "1888261684976573696"
tags:
  - "AI链接笔记"
  - "动态自适应激活神经元晶体管（DAA-NT）"
  - "动态稀疏神经网络（DS-SNN）"
  - "自动驾驶辅助系统"
  - "get-笔记"
  - "AI研究"
---

# 动态自适应激活神经元晶体管（DAA-NT）在自动驾驶辅助系统中的应用研究

## 摘要

📄 **研究背景与创新点**   - **传统局限**：神经形态计算面临冯·诺依曼瓶颈，静态阈值激活难以模拟生物神经元特性，全连接神经网络存在超90%计算冗余   - **核心突破**：提出基于不对称电极和铟镓锌氧化物（IGZO）薄膜的DAA-NT器件，实现类似生物神经元的动态稀疏激活，过滤冗余信息

## 正文

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc1d9d2b403a799137f636ad4cb9e2910?Expires=1780066679&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=OSzNJyQosCCGbl9ifoneApRNo40%3D)

大家好，今天为大家分享一篇2025年发表在Advanced Functional Materials的文献，题目为“A Dynamic Adaptive
Activation Neuron-Transistor for Dynamic Sparse Neural Networks in Advanced
Driving Assistance System”。本文的第一作者是Changsong Gao,本文的通讯作者是Jinshun Bi。

神经形态计算虽能解决冯·诺依曼瓶颈，但传统器件受限于静态阈值激活，难以模拟生物神经元特性，且全连接神经网络架构存在超90%计算冗余，而生物神经元动态稀疏激活能力可有效过滤冗余信息、提高决策准确性。本文提出基于不对称电极和铟镓锌氧化物（IGZO）薄膜的动态自适应激活神经元-晶体管（DAA-NT），以克服传统神经形态器件静态激活局限，实现类似生物神经元的动态稀疏激活特性。

DAA-NT器件采用IGZO薄膜作有源层，利用其n型半导体特性增强电子传输和氧空位松弛；源/漏电极分别用银（Ag）和金（Au）形成纳米电池效应，模拟生物神经元膜间动作电位；通过门电压或紫外光照射调节激活时间和阈值，实现动态稀疏激活，还利用低电压偏置下的电化学金属化实现非易失性突触权重存储。经测试，该器件表现出优异场效应行为、记忆行为，门电压和紫外光照射可显著调制激活时间和阈值，还能处理时空脉冲信号。

利用DAA-NT构建动态稀疏脉冲神经网络（DS-SNN），通过门电压或紫外光照射实现突触权重原位剪枝与再生，将其应用于自动驾驶目标检测，实现85%的准确性和42%的稀疏性，优于传统密集卷积神经网络（Dense-CNN）和密集脉冲神经网络（Dense-SNN）。机制上，利用COMSOL
Multiphysics软件建立物理场模拟模型，门电压和紫外光照射通过调节通道内电位分布和电子浓度，实现器件动态激活和稀疏编码。

DS-SNN在保持高准确性同时，显著减少参数数量和计算量，降低功耗、提高能效。本文提出的DAA-NT为构建高效能边缘计算电子产品提供新范式，未来将探索大规模神经形态处理器的3D集成。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe3b945adc03cb3b1ab0c94465867500e?Expires=1780066679&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=dluDPWYiBEhfee9twQyM22iAywI%3D)

图1 动态稀疏神经形态网络与器件设计。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb4db82bcce1d14367a266e8763272f05?Expires=1780066679&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=yZXzdL7WBKsmk2hFmEzcIVn30hk%3D)

图2 器件的电学响应特性。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5ebf19fc36a2e1884125499ee3ac860c?Expires=1780066679&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=OGs0XW12Yi%2FrTAO6OBgBD71s14E%3D)

图3 器件的动态自适应激活特性。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9d18de1e77c08940bf14813d5ae0e82b?Expires=1780066679&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=KaEz8nZP7634dm%2FZTpYRg7Hn74o%3D)

图4 器件工作机理分析。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1bd2bdf7dbfe4d6adc60890125a90b1b?Expires=1780066679&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=bOYI9V%2F6n51ikenTDtxD3IeoRzE%3D)

图5 基于器件的DS-SNN用于高效交通检测。

**Comments**

1. 本文开发了一种基于不对称电极和铟镓锌氧化物（IGZO）薄膜的动态自适应激活神经元晶体管（DAA-NT），通过门电压或紫外光照射，DAA-NT实现了动态自适应激活，具备广泛的激活时间（65ms–13.5s）和可调的激活阈值（2.5–7.7V）。
2. 研究提出了DAA-NT器件，通过不对称电极设计和IGZO薄膜的电子弛豫效应，实现了神经元激活时间和阈值的动态调节。这种机制模仿了生物神经元的动态稀疏编码特性，有效解决了传统神经形态器件中静态阈值导致的计算
3. 该研究提出了一种新的动态自适应激活机制，为开发高效、低功耗的神经形态器件提供了理论基础和技术路径。并通过硬件-算法协同设计，实现了动态稀疏脉冲神经网络，为解决传统神经网络中的计算冗余问题提供了有效方案。最后，该研究在自动驾驶领域的应用展示，证明了神经形态计算技术在现实世界中的潜力和价值。

**原文链接：https://doi.org/10.1002/adfm.202517785**

**FOLLOW US**

**投稿，推荐，合作请联系我们！**

**|| 微信公众号：微纳智能传感器**

**|| 微信号：successplus999**

**微纳传感器行业研究**

**学术前沿研究报道**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F75672f4eb486821bd63ea86acbaa449a?Expires=1780066679&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=jK%2BChm6F5xZHF767ezbRgREBqBM%3D)

声明  ————

本文仅供科研分享，不做盈利使用，如有侵权，请联系后台人员删除。

因学识有限，难免有所疏漏和谬误，恳请批评指正。

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 10:57*

## Related Notes

- [[AgentEvolver vs AlphaEvolve：AI自我进化的两条核心路线对比 🧠]]
- [[AI编码代理的质的飞跃：v3.3透明化与v3.4连续性技术解析]]
- [[DARPA人工智能与自主系统项目深度研究报告：以“第三波AI”为核心的军事智能革命]]
