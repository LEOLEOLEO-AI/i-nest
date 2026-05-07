# 知识库健康诊断 (Self-Health Dashboard)

> 自动维护 | 每周运行 `python3 ~/workspace/scripts/wiki_health.py`
> 上次诊断：**2026-05-07** | 综合评分：🔴 **50/100**

---

## 📊 健康指标

| 检查项 | 标准 | 当前 | 状态 |
|---|---|---|---|
| 总笔记数 | — | 1402 篇 | ℹ️ |
| 孤岛笔记（无链接） | < 10% | 823 篇 | 🔴 |
| 空文件 | = 0 | 5 篇 | 🔴 |
| 断链 | = 0 | 3598 处 | 🟡 |
| arXiv 高分未精读 | 每周清零 | 0 篇 | 🟢 |
| Fleeting 滞留 >7天 | = 0 | 0 篇 | 🟢 |
| 核心概念笔记缺失 | = 0 | 0 个 | 🟢 |

---

## ⚠️ 待处理问题

### 孤岛笔记（无链接）
- Projects/[V3] 项目布局_双轨战略框架.md
- Projects/项目布局汇总.md
- Projects/DARPA网络、信息战与通信领域项目深度分析报告（下册）：以体系化创新锻造未来信息战优势_18961842.md
- Projects/美国DARPA电子复兴计划2.0(ERI 2.0)深度解析：重塑微电子技术的国家战略.md
- Projects/美国DARPA生物技术与人类增强领域深度研究报告：从战场医疗到认知决胜的战略布局.md
- Projects/美国DARPA网络、信息战与通信领域战略布局深度研究报告（上册）.md
- Projects/休假事项.md
- Projects/光电混合晶圆级互连系统.md
- Projects/偏头痛止痛药.md
- Projects/美国DARPA材料科学与先进制造领域深度研究报告：战略、技术与未来展望.md

### 空文件或过短笔记
- Journal/2026-04-17.md
- Inbox/待分类/00-索引/Wiki/SSOT.md
- Inbox/待分类/00-索引/Wiki/ADR.md
- 05_Fleeting/待分类/00-索引/Wiki/SSOT.md
- 05_Fleeting/待分类/00-索引/Wiki/ADR.md

### 断链（目标笔记不存在）
- 00_MOC/TCC-MOC.md → [[01_Concepts/SOC-自组织临界]]
- 00_MOC/TCC-MOC.md → [[01_Concepts/TCC-拓扑中心计算]]
- 00_MOC/TCC-MOC.md → [[01_Concepts/SDI-软件定义互连]]
- 00_MOC/TCC-MOC.md → [[01_Concepts/SDSoW]]
- 00_MOC/TCC-MOC.md → [[01_Concepts/小世界网络]]
- 00_MOC/TCC-MOC.md → [[01_Concepts/神经雪崩]]
- 00_MOC/TCC-MOC.md → [[01_Concepts/自由能原理]]
- 00_MOC/TCC-MOC.md → [[01_Concepts/元拓扑]]
- 00_MOC/TCC-MOC.md → [[03_Projects/TCC计算范式/README]]
- 00_MOC/TCC-MOC.md → [[03_Projects/iNEST/README]]
- 00_MOC/TCC-MOC.md → [[03_Projects/TCC计算范式/01_论文/SDI-CC论文框架_拓扑即计算新范式]]
- 00_MOC/TCC-MOC.md → [[03_Projects/TCC计算范式/01_论文/P-Theory_v2_MetaTopology_SDI_Bond_Draft]]
- 00_MOC/TCC-MOC.md → [[04_Research/SDI-v31/README]]
- 00_MOC/TCC-MOC.md → [[04_Research/Hemibrain/README]]
- 00_MOC/TCC-MOC.md → [[02_Papers/arxiv-auto/]]

---

## 🏗️ 目录结构规范（卡帕西法则）

```
obsidian-vault/
├── 00_MOC/          ← 入口地图，不放内容只放索引
├── 01_Concepts/     ← 原子概念笔记（一文一概念）
├── 02_Papers/       ← 文献（arxiv-auto 自动 + manual 手动）
├── 03_Projects/     ← 项目文档（TCC计算范式 / iNEST）
├── 04_Research/     ← 实验数据与结果
├── 05_Fleeting/     ← 临时捕获（7天内处理）
├── Journal/         ← 日志
├── 99-Templates/    ← 模板
└── 99-Attachments/  ← 附件
```

**原则：** 扁平 · 原子 · 链接>分类 · MOC驱动 · Inbox临时缓冲

---

## 🔄 进化机制

- **每日 08:00** arXiv 自动追踪 → `02_Papers/arxiv-auto/`
- **每周** 运行本脚本 → 更新健康报告
- **每周** 把 05_Fleeting 中想法升级为 01_Concepts 原子笔记
- **每月** 检查项目进展，更新 MOC

---
*自动生成于 2026-05-07 | iNEST Wiki Health Bot*