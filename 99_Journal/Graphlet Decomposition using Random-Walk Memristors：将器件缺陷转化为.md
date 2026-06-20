---
title: "Graphlet Decomposition using Random-Walk Memristors：将器件缺陷转化为计算优势"
source: "https://mp.weixin.qq.com/s/ogf6S4f9Jvzl8Snz_hW8TA"
created: 2026-01-07
note_id: "1898137694911999672"
tags:
  - "AI链接笔记"
  - "忆阻器"
  - "Graphlet分解"
  - "随机游走"
  - "get-笔记"
  - "会议记录"
  - "重要"
---

# Graphlet Decomposition using Random-Walk Memristors：将器件缺陷转化为计算优势

## 摘要

### **📌 研究背景与核心突破**  忆阻器交叉阵列因其**高密度**与**并行处理能力**，被视为后CMOS时代的潜在计算平台。然而，**串扰电流**与**随机开关**一直是阻碍其应用的关键难题。本文提出创新方法： - 将**串扰路径**用于表示graphlet（图小体，网络中的小型连通子图）

## 正文

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5788a32604e1faf4bcf3fbd8be4830b3?Expires=1780061745&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=eYdVuojyWFRyX3ILx1sk6zvF7H4%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe092404c980dbee09fe87de9af942518?Expires=1780061745&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=t72KwRx6LtjoFI6aRT7seXYgBP4%3D)

忆阻器交叉阵列因其高密度与并行处理能力，被视为后 CMOS
时代的潜在计算平台。然而，串扰电流与随机开关一直是阻碍其应用的难题。本文提出一种新方法，将串扰路径用于表示 graphlet，将随机开关用于模拟随机游走，实现
graphlet 分解与分析。这一方法不仅解决了忆阻器固有问题，还为社交网络、生物信息学等复杂网络分析提供了硬件加速的新途径，该文发表于IEEE
International Electron Devices Meeting （IEDM）国际顶尖电子器件学术会议上。

**⚡ 一句话**

随机游走忆阻器通过利用串扰与随机性，实现高效 graphlet 分解，关键认知是 **将器件缺陷转化为计算优势**。

**🔑 研究亮点**

* **器件创新**：双层 HfO₂‑x 结构，兼具混合与非易失开关特性。
* **方法突破**：利用串扰路径与随机阈值实现 graphlet 分解。
* **度量方式**：提出度量与距离两种方法避免同构。
* **随机游走**：通过随机阈值分布驱动节点采样，提升大规模网络分析效率。
* **网络对比**：在 Facebook 用户网络与理论 Barabasi Albert 网络中验证差异。

**📊 图示要点**

* **图 1｜Graphlet 分析概念**  展示利用忆阻器交叉阵列进行 graphlet 分解的基本思路与常见 graphlet 列表。

  ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff68a69e7454e670b89fc018c98b7946b?Expires=1780061745&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=IZIcLQM%2BkJBB77A4xSuIx72Yga0%3D)
* **图 2｜Hybrid memristor 特性**  展示器件结构、XPS 分析、混合与非易失开关曲线及开关机制。

  ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F668b276a14f6ad2e515e6fffda5b9c2d?Expires=1780061745&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=JwQtjk7Wg4FhRALXIVbHkyUwxXQ%3D)
* **图 3｜Graphlet counter**  展示度量与距离方法的示意及热成像实验结果。

  ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe8a8329a3625ba75dd2379db237a49ff?Expires=1780061745&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=%2B1jdFu9r7OPX4YURNKl5%2B8ZCMY8%3D)
* **图 4｜Graphlet 指纹**  展示通过度量与距离方法获取 graphlet 结构指纹的流程。

  ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fca0ce97a3c539cbf9bc7cbaeb243fba0?Expires=1780061745&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=yNBKZWNvyBJQrLAAUcW6zAIVN40%3D)
* **图 5｜边缘器件随机性**  展示边缘器件在多次循环下的阈值电压随机变化与分布。

  ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4ca44e2269aaaf22d21f79f2d1d3c4c7?Expires=1780061745&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ao%2Bj7sVUuXKQp7zqu2HqRtgPuSc%3D)
* **图 6｜随机游走流程**  展示基于随机游走的 graphlet 分析流程图。

  ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc2e6f4b808a62730625d235501215651?Expires=1780061745&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=fmhhjSkTcAXt35hg%2FYiVcB2X4P4%3D)
* **图 7｜随机游走网络分析**  展示 1000 节点网络的随机游走结果、分布与误差分析。

  ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F18f9c923d2b49a6f64bba75edf56ab92?Expires=1780061745&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ghMlTlPwEzmRd9EnE9j86LSVLQ0%3D)
* **图 8｜网络对比分析**  展示三种网络的 graphlet 分布、雷达图与相关系数。

  ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1bbc8c56407bf2de1e31632e59b4ea3a?Expires=1780061745&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=DUu0C1PV33AZ9r0NrDf8Nh7rbyU%3D)

**🧠 结论与展望**

本文展示了如何利用忆阻器交叉阵列的串扰与随机性实现 graphlet
分解与分析。该方法不仅解决了器件固有问题，还为大规模网络分析提供了硬件加速的新途径。未来方向包括：

* **扩展至更复杂网络**：如基因组切片与社交网络。
* **优化器件结构**：提升随机游走的稳定性与采样效率。
* **结合其他计算框架**：推动忆阻器在图计算与人工智能中的应用。

这一工作为忆阻器在复杂网络分析中的应用开辟了新路径。

文章信息：

Woo, K. S., Ghenzi, N., Talin, A. A. *et al.* Graphlet Decomposition Using Random-Walk Memristors. *IEDM (2024).*

https://doi.org/10.1109/IEDM50854.2024.10873438

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1b819bcf5e43a566001c2468534ad0f9?Expires=1780061745&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=7o1I35qd4%2FCJaJJw1MgzyYcV%2Bqs%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fef98d0fb6f868bf8a2542eec274ed0be?Expires=1780061745&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=BQTnt0wAFsgGJIQmBvmo8UQPHnM%3D)

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 09:35*