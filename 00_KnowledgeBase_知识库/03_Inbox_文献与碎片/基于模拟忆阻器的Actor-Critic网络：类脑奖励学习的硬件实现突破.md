---
title: "基于模拟忆阻器的Actor-Critic网络：类脑奖励学习的硬件实现突破"
source: "https://mp.weixin.qq.com/s/uXyTkDWi9yLLxDEQs2m-Vg"
created: 2025-12-21
note_id: "1896510006459824768"
tags:
  - "AI链接笔记"
  - "类脑计算"
  - "忆阻器"
  - "Actor-Critic网络"
  - "get-笔记"
  - "AI研究"
---

# 基于模拟忆阻器的Actor-Critic网络：类脑奖励学习的硬件实现突破

## 摘要

### **📚 研究背景与核心问题**  人脑的高效学习依赖于**奖励调控的三因子学习规则**，而传统人工智能强化学习系统存在显著瓶颈： - **计算开销巨大**：依赖软件实现时间差分（TD）学习算法 - **能耗过高**：数据在存储器与处理器间频繁移动导致能效低下 - **生物模拟差距**：难以复

## 正文

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5788a32604e1faf4bcf3fbd8be4830b3?Expires=1780062432&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=XXigg4QdQFeW6pNIn4EIFKCAIcI%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fa508a26cf98fcc271bb69f973d1f84dc?Expires=1780062432&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=0x87isFgHYVKsPC2WIeg3SE2ioQ%3D)

人脑的高效学习依赖于奖励调控的三因子学习规则，而传统人工智能强化学习系统往往依赖软件实现，计算开销巨大且能耗高。本研究提出了一种基于模拟忆阻器的
Actor–Critic
网络，直接在硬件中实现时间差分（TD）学习算法，模拟生物大脑的奖励预测误差机制。忆阻器在该框架中承担多重角色：既作为可在线训练的突触权重，又直接在存储器中完成权重更新计算，并决定智能体的行为选择。通过这种全硬件在线学习方式，数据移动被彻底消除，显著提升了处理速度与能效。研究在
T 迷宫与 Morris 水迷宫两类导航任务中进行了验证，展示了忆阻器在类脑奖励学习中的应用潜力。

**⚡ 一句话**

该研究在模拟忆阻器中实现了类脑 **Actor–Critic 时间差分学习**，忆阻器同时承担突触权重存储、奖励预测误差计算与在线更新，完成全硬件、全内存的强化学习循环，并在 **T 迷宫与 Morris 水迷宫导航任务**中验证了奖励驱动的路径优化能力，展示了面向高效类脑智能硬件的突破性方案。

**🔑 研究亮点**

* **三因子学习规则硬件化**：忆阻器直接实现奖励调控的时间差分学习，模拟生物多巴胺信号。
* **忆阻器多功能角色**：既存储权重，又计算动作与权重更新，实现全硬件在线学习。
* **消除数据移动**：训练过程完全在存储器中进行，提升能效与速度。
* **类脑架构验证**：在 Actor–Critic 网络中实现奖励预测误差驱动的学习。
* **导航任务测试**：在 T 迷宫与 Morris 水迷宫中展现出逐步优化的路径选择能力。
* **误差自校正机制**：忆阻器的非理想更新误差在迭代中被自动修正，保证学习稳定性。

**📊 图示要点**

* **图 1｜类脑强化学习框架**  展示 T 迷宫与 Morris 水迷宫实验示意，Actor–Critic
  网络结构，忆阻器作为人工突触的角色，以及硬件/软件分工的流程图。

  ![Fig.
  1](https://mmbiz.qpic.cn/sz_mmbiz_png/KP8HqeN567jfqNFWoKOxxalX2Iu9HKZDmkCI5uVvGo4NueOKt5RHVT5x4xtQyGYZwKRh19k6qqvlUI0EUGA39w/640?wx_fmt=png&from=appmsg)
* **图 2｜模拟忆阻器的结构与特性**  展示忆阻器材料堆栈与偏置方式，SEM 与 FIB 截面图，电阻–电压特性曲线，以及脉冲下的增强/抑制行为与噪声统计。

  ![Fig.
  2](https://mmbiz.qpic.cn/sz_mmbiz_png/KP8HqeN567jfqNFWoKOxxalX2Iu9HKZDGErK7qViceO6aFcV2tjCuGb5wnFCXDJiadX1nVibhLnib6HRgib5gYyS37g/640?wx_fmt=png&from=appmsg)
* **图 3｜存储器内学习循环**  展示忆阻器在内存中完成权重更新的流程，实验测量与理论计算的对比，以及误差校正机制对权重稳定性的提升。

  ![Fig.
  3](https://mmbiz.qpic.cn/sz_mmbiz_png/KP8HqeN567jfqNFWoKOxxalX2Iu9HKZDOibEjSZFDvY63iazF0IMeZ9VxecFbFYMm6Z91x8ckASClBXUPicrEg47g/640?wx_fmt=png&from=appmsg)
* **图 4｜T 迷宫导航任务验证**  展示智能体在 T 迷宫中的状态编码、Actor–Critic 权重分布与学习结果，体现奖励驱动的路径优化过程。

  ![Fig.
  4](https://mmbiz.qpic.cn/sz_mmbiz_png/KP8HqeN567jfqNFWoKOxxalX2Iu9HKZDvVrKDeiaA5zCDp0icm8EoCfpjcRKowe7Ts4CbNIA0VsibsP6t4WGfsvibg/640?wx_fmt=png&from=appmsg)
* **图 5｜Morris 水迷宫任务验证**  展示智能体在水迷宫中的路径学习过程，逐步从随机游走转向直接到达平台，体现奖励学习的效率提升。

  ![Fig.
  5](https://mmbiz.qpic.cn/sz_mmbiz_png/KP8HqeN567jfqNFWoKOxxalX2Iu9HKZDqzX1SRSASTDZsQxyfQN10bMRIzG2h5XsnEFyicbywwKwZU3MrwIArqA/640?wx_fmt=png&from=appmsg)

**🧠 结论与展望**

本研究提出的模拟忆阻器 Actor–Critic 网络在硬件中实现了奖励驱动的 TD
学习，展示了类脑学习的可行性与高效性。忆阻器的多功能角色使得训练过程完全在存储器中进行，消除了传统架构中的数据移动瓶颈。

未来发展方向包括：

* **扩展至复杂任务**：在更大规模环境与多维任务中验证硬件强化学习能力。
* **多模态集成**：结合视觉、听觉等输入，实现更接近生物智能的学习。
* **类脑智能硬件平台**：推动全硬件在线学习引擎在机器人、自主系统与智能交互中的应用。

该成果为构建高效、类脑的强化学习硬件提供了新路径，推动下一代神经形态计算的发展。

文章信息：

Portner, K., Zellweger, T., Martinelli, F. *et al.* Actor–critic networks with analogue memristors mimicking reward-based learning. *Nat Mach Intell* (2025).

https://doi.org/10.1038/s42256-025-01149-w

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1b819bcf5e43a566001c2468534ad0f9?Expires=1780062432&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=lsbALJstIUNyq05f2PcMldMSQPU%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fef98d0fb6f868bf8a2542eec274ed0be?Expires=1780062432&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=BYVa43U3%2FWJYqsoFQ37TW2B1OTo%3D)

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 09:47*