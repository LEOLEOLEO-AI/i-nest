---
direction: both
category: 技术
tags: [AI芯片设计, 强化学习, AlphaChip, 芯片布局, 神经形态计算]
summary: "前Google Brain成员创立Ricursive，用AI将芯片设计周期从数年压缩至数天"
quality: high
processed: 2026-09-25 22:39
---
---
title: "Ricursive Intelligence：用AI重构芯片设计的40亿美元初创公司"
tags:
  - hardware
  - research
  - chip
  - neural
  - architecture
  - network
  - paper
  - neuroscience
  - design
  - top-journal
  - semiconductor
date: 2026-09-25 22:39
source: GetNotes
score: 13
---

## Original Note

---
note_id: 1922329454689014976
title: "Ricursive Intelligence：用AI重构芯片设计的40亿美元初创公司"
type: link
created: 2026-09-25 12:00:17
source: getnote
kb: 
---

# Ricursive Intelligence：用AI重构芯片设计的40亿美元初创公司

### 🏢 这家公司是谁，凭什么刚成立就估值40亿？

两位前Google Brain成员创办，**成立仅数月**就拿下**3.35亿美元融资**，估值达**40亿美元**。
- **核心创始人**：
  - **Anna Goldie** = CEO
  - **Azalia Mirhoseini** = CTO
- **投资方阵容**：英伟达投资部门 + 红杉资本 + Lightspeed 等
- **业务定位**：不造芯片，做**AI芯片设计工具**，帮芯片企业提速设计流程
  说白了，不是下场做新芯片，而是给所有芯片厂当"AI设计顾问"。

### 🧪 两位创始人之前在Google做出了什么成果？

在Google期间开发出**AlphaChip**，用AI把芯片布局从**一年压缩到几小时**。
- **过往身份**：Google AI 核心研究员 + Google Brain 早期成员
- **核心突破**：
  - 传统芯片布局 = 工程师花**1年以上**排布数十亿个逻辑组件
  - AlphaChip = 强化学习驱动，**几小时**生成高质量布局
- **学术与落地**：
  - **2021年**在《Nature》发表强化学习芯片布局论文
  - 技术已用于设计**多代Google TPU**芯片
- **技术特点**：能通过设计反馈不断调整神经网络，训练数千次后效果和速度同步提升

### 🎯 这家公司现在要做什么，目标客户是谁？

把AlphaChip商业化，目标是把芯片设计周期从**几年缩短到几天**。
- **产品方向**：开发自动化芯片设计平台，让芯片**适配AI模型需求**，而非反过来
- **覆盖范围**：定制芯片 + 传统芯片，全类型支持
- **目标客户**：英伟达、AMD、英特尔等所有芯片厂商
- **团队背景**：成员来自 Google DeepMind、Anthropic、NVIDIA、Cadence、Apple、斯坦福、MIT、哈佛 等机构
- **过往项目经验**：参与过 AlphaChip、RL-CCD、Insta、C3PO，以及 Gemini、Claude、TPU、Apple Silicon 开发

### 🔄 为什么说AI设计芯片会形成正向循环？

AI设计更好的芯片 → 更强芯片反推AI进步 → 形成**自我改进的闭环**。
- **核心逻辑**：芯片是AI的燃料，设计速度正限制AI发展速度
- **未来方向**：AI模型与芯片实现**快速共同进化**，针对特定模型定制计算架构，提升性能与成本效率
- **行业进展**：几乎所有大型芯片公司都已接触，尚未公布早期客户名单

### 📝 补充细节
- 公司名称原文为 **Ricursive Intelligence**（注意拼写非"Recursive"）
- 融资金额换算：3.35亿美元 ≈ **22亿元人民币**，40亿美元估值 ≈ **279亿元人民币**

---
*getnote | 2026-09-25 22:38*


---

## Related Notes

[[FPGA原型]]
[[Papers-MOC]]
[[SDI化合物键_四型架构]]
[[iNEST-MOC]]
[[paper1_iNEST_core_architecture]]
