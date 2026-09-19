---
direction: both
category: 资料
tags: [connectome, neuroscience, LIF, spiking-neural-network, drosophila]
summary: "果蝇完整中枢神经连接组MaleCNS v1.0解析，含LIF神经元建模方法"
quality: high
processed: 2026-09-17 19:54
---
---
title: "果蝇大脑连接组 MaleCNS v1.0 深度解析：把真实脑神经做成神经网络"
tags:
  - neural
  - design
  - top-journal
  - research
  - connectome
  - architecture
  - network
  - paper
  - neuroscience
  - simulation
date: 2026-09-16 21:00
source: GetNotes
score: 13
---

## Original Note

---
note_id: 1921487048394152280
title: "果蝇大脑连接组 MaleCNS v1.0 深度解析：把真实脑神经做成神经网络"
type: link
created: 2026-09-16 10:04:25
source: getnote
kb: 
---

# 果蝇大脑连接组 MaleCNS v1.0 深度解析：把真实脑神经做成神经网络

### 🧠 这次发布的是什么成果？

Google 联合 HHMI Janelia 等机构，**首次完成成年雄性果蝇完整中枢神经连接图谱**。
- **成果名称**：MaleCNS v1.0
- **研究主体**：成年雄性果蝇的**完整中枢神经系统**
- **能力表现**：该神经网络可完成**玩魔方、打游戏**等任务

### 🔗 果蝇脑神经网络和深度学习架构有什么不一样？

果蝇脑是**大量循环反馈**的结构，不是深度学习那种单向流动。
- **基本单元**：每个节点 = 一个**真实神经元**；有突触连接就有一条有向边
- **权重定义**：边的权重 ≈ 两个神经元之间的**突触数量**
- **存储形式**：计算机中表现为一个巨大的**稀疏邻接矩阵**
- **信号流向**：感觉器官 → 大量局部回路 ↔ 高级脑区 ↔ 反馈回路 → 下行神经元 → 腹神经索 ↔ 身体感觉反馈 → 运动神经元
  说白了，深度学习像一条单向流的河，果蝇脑里到处都是回头路和环路。

### ⚡ 果蝇脑里的神经元是怎么工作的？

采用 **Leaky Integrate and Fire（漏积分放电）** 模型，像个会漏电的小杯子。
- **核心变量**：膜电位
- **工作流程**：
  1. 读取哪些神经元刚刚 spike（放电）
  2. 沿真实果蝇连接图传播信号
  3. 根据突触数 + 兴奋/抑制性质，改变下游神经元电压
  4. 电压超过阈值 → 发 spike → 继续传播；没超过 → 继续积分
- **关键特性**：电压会自然泄漏，不是一直累加

### 📊 突触数量和权重怎么对应？

权重直接由**真实果蝇中观测到的突触数量**近似得出。
- 常用连接组模拟中，突触数量可直接作为连接强度的粗略指标
- 连接强度 = 突触数 × 突触的兴奋/抑制性质

### 📝 补充细节
- 果蝇脑计算模型参考 **Shiu 等人发表在 Nature** 的工作
- 论文链接：https://www.nature.com/articles/s41586-024-07763-9
- 图片来源：x.com @nickwalton00

---
*getnote | 2026-09-16 21:00*


---

## Related Notes

[[iNEST-MOC]]
[[paper1_iNEST_core_architecture]]
[[v28多尺度仿真结果]]
[[Papers-MOC]]
