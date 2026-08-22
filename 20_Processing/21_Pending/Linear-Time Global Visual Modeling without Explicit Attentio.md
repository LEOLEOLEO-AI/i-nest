---
title: "Linear-Time Global Visual Modeling without Explicit Attentio"
tags:
  - research
  - design
  - architecture
  - paper
date: 2026-08-19 00:18
source: GetNotes
score: 8
---

## Original Note

---
note_id: 1918830443617714824
title: "Linear-Time Global Visual Modeling without Explicit Attention 论文核心解读"
type: link
created: 2026-08-18 18:48:29
source: getnote
kb: 
---

# Linear-Time Global Visual Modeling without Explicit Attention 论文核心解读

### **这篇论文提出了什么新技术？**

提出 **Memory Caching 记忆缓存技术**，核心是**缓存循环模型分段记忆状态**。
- **技术本质**：通过缓存分段记忆状态，让 RNN 获得**随序列增长的有效记忆**。
- **复杂度折中**：在 RNN **线性复杂度** 与 Transformer **二次复杂度** 之间实现灵活折中。
- **设计细节**：设计了**多种聚合变体**，适配不同循环架构。

### **这项技术能带来哪些效果？**

可提升循环模型性能，**缩小与 Transformer 召回能力差距**。
- **性能提升**：在多种循环架构与长上下文任务上验证有效。
- **效率优势**：长序列下**推理效率优于 Transformer**。
- **额外用途**：可直接用于预训练模型**推理阶段**，提升长度外推能力。

### **📝 补充细节**
- 论文地址：https://arxiv.org/pdf/2602.24281
- 技术聚焦**视觉建模**领域，实现线性时间复杂度且无需显式注意力机制。

---
*getnote | 2026-08-19 00:18*


---

## Related Notes

[[iNEST-MOC]]
[[Papers-MOC]]
