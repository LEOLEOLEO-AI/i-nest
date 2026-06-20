# iNEST/TCC 超级研发流水线 v3.0

> Codex 为中枢，六工具协同。让每个工具各司其职，月费不白花。

---

## 一、工具定位矩阵

| 工具 | 角色 | 核心优势 | 月费价值 |
|---|---|---|---|
| **Codex** | 🧠 中枢大脑 | 任务编排、论文/专利撰写、数据分析、多步执行 | ⭐⭐⭐⭐⭐ |
| **得到大脑** | 📥 信息摄入官 | 专业剪藏、AI摘要、跨平台采集 | ⭐⭐⭐⭐⭐ |
| **Genspark** | 🔍 深度研究员 | 多步搜索、结构化报告、复杂问题拆解 | ⭐⭐⭐⭐ |
| **Obsidian** | 📚 知识中枢 | 双向链接、图谱、本地化、插件生态 | ⭐⭐⭐⭐⭐ |
| **Trae Solo** | ⌨️ 代码工坊 | 实时编辑、快速调试、IDE 体验 | ⭐⭐⭐ |
| **印象笔记** | 🗄️ 遗产归档 | 历史笔记迁移后停用 | ⭐ |

---

## 二、数据流向图

```
                    ┌──────────────┐
        微信/浏览器  │  得到大脑     │  AI摘要 + 分类
       ──────────→  │  (信息摄入官) │──────┐
                    └──────────────┘      │
                                          │ 导出 MD
                    ┌──────────────┐      │
        深度搜索     │  Genspark    │      │
       ──────────→  │  (深度研究员) │──────┤
                    └──────────────┘      │
                                          ↓
              ┌───────────────────────────────────┐
              │          Obsidian 知识中枢          │
              │                                    │
              │  00_Inbox/    ← 待处理入口          │
              │  TCC_1_项目策划/ ← TCC 研究        │
              │  iNEST_Research/ ← iNEST 研究      │
              │  Papers/       ← 论文草稿          │
              │  Patents/      ← 专利草稿          │
              │  Literature/   ← 文献笔记          │
              │                                    │
              └──────────┬──────────────┬──────────┘
                         │              │
                    ┌────▼────┐    ┌───▼──────┐
                    │  Codex  │    │Trae Solo │
                    │ (中枢)  │◄──►│ (代码IDE) │
                    └────┬────┘    └──────────┘
                         │
              ┌──────────┼──────────┐
              │          │          │
        论文撰写    专利撰写    实验分析
```

---

## 三、各工具 SOP

### 3.1 得到大脑 — 信息摄入官

**日常操作：**
1. 微信看到好文章 → 转发/分享到得到大脑
2. 浏览器文章 → 得到大脑插件一键剪藏
3. 得到大脑自动 AI 摘要 + 标签分类

**导出到 Obsidian：**
- 每周五下午，批量导出本周剪藏为 Markdown
- 放入 `00_Inbox/` → Codex 进一步分类到 TCC/iNEST 目录

**月费价值：** 每天 3-5 篇文章 × AI 摘要 = 省 1-2 小时阅读筛选时间

### 3.2 Genspark — 深度研究员

**使用场景（不是日常剪藏！）：**
- "帮我在 arXiv 上找 2025 年关于 neuromorphic interconnect 的最新 10 篇论文，总结趋势"
- "对比 Intel、AMD、NVIDIA 在 chiplet 互联标准上的技术路线"
- "搜索 consciousness emergence in neural networks 的理论框架"

**输出格式：**
- Genspark 生成结构化研究报告 → 复制到 Obsidian `Literature/` 或 `Research/`
- 关键发现用 `## Highlights` 标注 → Codex 后续深入分析

**月费价值：** 每月 4-6 次深度研究 → 每次省半天手动搜索整理

### 3.3 Obsidian — 知识中枢

**目录结构：**
```
D:\Obsidian\home\work\.openclaw\workspace\
├── 00_Inbox/           # 得到大脑/Genspark 导入入口
├── TCC_1_项目策划/      # TCC 拓扑中心计算
├── iNEST_Research/     # iNEST 涌现智能研究
├── Papers/             # 论文草稿
├── Patents/            # 专利草稿
├── Literature/         # 文献笔记
├── dashboard/          # 研发看板
└── scripts/            # 自动化脚本
```

**核心原则：**
- 所有信息先进 Obsidian，不直接进 Codex
- 用 `[[双向链接]]` 建立知识图谱
- 看板可视化项目进度

### 3.4 Codex — 中枢大脑

**作为调度中心，通过 Obsidian 的 AGENTS.md + CC-Connect 驱动：**

**论文撰写流程：**
1. 在 Obsidian `Papers/` 创建论文目录
2. Codex 读取 Literature 笔记 → 生成文献综述
3. Codex 生成论文大纲 → 用户确认
4. Codex 逐节撰写 → Trae Solo 可辅助代码块编辑
5. Codex 格式化为目标期刊模板

**专利撰写流程：**
1. 在 Obsidian `Patents/` 创建专利目录
2. Codex 读取技术方案 → 生成权利要求书
3. Codex 生成说明书 + 附图描述

**数据/实验分析：**
1. Codex 编写 Python 仿真脚本
2. 生成图表存入 `assets/`
3. 分析结果写入 Obsidian 笔记

### 3.5 Trae Solo — 代码工坊

**定位：Codex 的 IDE 伴侣，不要替代 Codex**

**使用场景：**
- Codex 写出代码后 → Trae 打开、可视化编辑、调试
- 需要快速改一个小函数 → 直接在 Trae 里改
- 查看大型代码库结构 → Trae 的项目浏览

**不要用 Trae 做的事：**
- 多文件重构（交给 Codex）
- 论文撰写（交给 Codex）
- 复杂任务编排（交给 Codex）

### 3.6 印象笔记 → 停用

**行动计划：**
1. 导出所有笔记为 ENEX
2. 用工具转为 Markdown
3. 导入 Obsidian `Archive/印象笔记/`
4. **取消续费**

---

## 四、典型一天

| 时段 | 动作 | 工具 |
|---|---|---|
| 08:00 通勤 | 微信文章转发到得到大脑 | 得到大脑 |
| 09:00 到岗 | 得到大脑导出 MD → Obsidian | Obsidian |
| 09:30 | 让 Codex 处理 Inbox，分类到 TCC/iNEST | Codex |
| 10:00 | 深度搜索：chiplet 互联最新进展 | Genspark |
| 10:30 | Genspark 报告 → Obsidian Literature | Obsidian |
| 11:00 | Codex 撰写论文 Methodology 章节 | Codex |
| 14:00 | Codex 生成仿真代码 → Trae 调试 | Codex→Trae |
| 16:00 | iNEST 流水线运行，更新看板 | scripts |
| 17:00 | 整理当天笔记，建立双向链接 | Obsidian |
| 通勤中 | 微信指挥 Codex 改论文 | CC-Connect |

---

## 五、关键原则

1. **Codex 是唯一中枢** — 所有复杂任务通过 Codex 编排，其他工具是它的手脚
2. **Obsidian 是唯一真相源** — 所有知识产出进 Obsidian，不在工具间复制
3. **信息摄入走得到大脑 / Genspark** — 不进 Codex 沙箱（没网）
4. **Trae 只做 IDE 的事** — 不要让它替代 Codex 做复杂任务
5. **印象笔记 → 立即停用** — 迁移后取消续费，省一笔月费

---

*Created: 2026-06-19 | Codex + Obsidian*