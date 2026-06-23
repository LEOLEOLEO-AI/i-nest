---
title: "TCC iNEST 论文撰写可追溯管线（基于 Research Units Pipeline 重构）"
date: 2026-06-17
version: 2.0
framework: "Zotero 存证据 + Codex 跑流程 + Skills 做工序"
---

# TCC iNEST 论文撰写可追溯管线

> **核心原则：** 每一步都产出可追溯的中间产物，存入知识库而非散落在对话记录中。
> **框架来源：** 微信文章《用 AI 写论文的人，很多人都经历过同一种尴尬》— 科研技能流程

---

## 一、管线总览：8 步可追溯流程

```
[1.检索] → [2.筛选] → [3.选题] → [4.结构] → [5.草稿] → [6.正文] → [7.数据] → [8.交付]
   ↓          ↓          ↓          ↓          ↓          ↓          ↓          ↓
 文献夹     主题简报    方向文档    章节框架    综述草稿    正文终稿    统计图表    LaTeX/PDF
 (Zotero)   (1页笔记)  (3-5选题)  (证据映射)  (源标注)   (润色后)   (可复现)   (投稿版)
```

每一阶段的产物都是独立的 MD 文件或 Zotero 条目，导师可追溯、审稿人可验证。

---

## 二、8 步工序详述

### 工序 1：检索（Search & Import）

| 项目 | 内容 |
|------|------|
| **工具** | `paper-search-mcp`（openags）+ Semantic Scholar / arXiv / Crossref |
| **输入** | 研究方向关键词（如 "software-defined interconnect", "data movement energy", "CST complexity threshold"） |
| **输出** | 结构化文献列表（标题、作者、年份、DOI、来源、已读/未读标记） |
| **存储** | 导入 Zotero 的 `TCC_论文` 分类文件夹 |
| **检查点** | 能否说出每篇文献为什么入选？ |

**当前 TCC 项目状态：**
- P1（TCC-SDI）：文献检索基本完成（43篇参考文献），待补充2025-2026最新CXL/NoC文献
- P2（CST-A1）：文献检索完成（50篇），已通过27轮修订验证

### 工序 2：筛选与阅读（Screen & Brief）

| 项目 | 内容 |
|------|------|
| **工具** | `research-brief`（research-units-pipeline-skills） |
| **输入** | 工序1的文献列表 |
| **输出** | 一页主题简报：研究空白、争议焦点、方法学趋势、关键论文矩阵 |
| **存储** | 保存为 `01_Literature_Brief.md` |
| **检查点** | 能否用一段话说清"已有研究做了什么、没做什么"？ |

**当前 TCC 项目状态：**
- P1：⬜ 待生成 `P1_Literature_Brief.md`
- P2：⬜ 待生成 `P2_Literature_Brief.md`（可基于 v28 的 Introduction 反向提取）

### 工序 3：选题收敛（Topic & Question）

| 项目 | 内容 |
|------|------|
| **工具** | `idea-brainstorm`（research-units-pipeline-skills） |
| **输入** | 工序2的主题简报 |
| **输出** | 3-5个候选研究方向，每个含：研究问题、创新点、可行性评估 |
| **存储** | 保存为 `02_Research_Questions.md` |
| **检查点** | 研究问题是"可回答的"还是"太宽泛的"？ |

**当前 TCC 项目状态：**
- P1：⬜ 研究问题已隐含在论文中，需显式化为 RQ 文档
- P2：✅ 研究问题明确（CST能否统一量化智能涌现？）

### 工序 4：结构验证（Structure & Argument）

| 项目 | 内容 |
|------|------|
| **工具** | `strategist`（research-units-pipeline-skills / ARS structure_architect） |
| **输入** | 工序3的选定研究方向 + 工序2的证据矩阵 |
| **输出** | 章节框架 + 证据→章节映射表 + 字数分配 |
| **存储** | 保存为 `03_Paper_Outline.md` |
| **检查点** | 每个章节是否有明确的论证任务和支撑证据？ |

**当前 TCC 项目状态：**
- P1：✅ 7章结构已完成（见论文 v1.0）
- P2：✅ IMRaD 结构已完成（见论文 v28）

### 工序 5：综述草稿（Literature Review Draft）

| 项目 | 内容 |
|------|------|
| **工具** | `literature-review` 或 `arxiv-survey`（research-units-pipeline-skills） |
| **输入** | 工序4的章节框架 + 工序1的文献 |
| **输出** | 综述草稿：每一段标注证据来源（`[来源: Author Year, DOI]`） |
| **存储** | 保存为 `04_Literature_Review_Draft.md` |
| **检查点** | 每个论断是否可追溯到具体文献？是否有跳步论证？ |

**当前 TCC 项目状态：**
- P1：✅ 综述部分已完成（第2-4节），但源标注格式可增强
- P2：✅ 综述+验证+讨论全部完成，源标注规范

### 工序 6：正文撰写（Scientific Writing）

| 项目 | 内容 |
|------|------|
| **工具** | `scientific-writing` 或 `composer`（K-Dense-AI/claude-scientific-writer）+ ARS `draft_writer_agent` |
| **输入** | 工序5的综述草稿 + 工序4的结构 |
| **输出** | 完整论文正文（IMRaD 格式），经润色 |
| **存储** | 保存为 `05_Manuscript_Draft.md` |
| **检查点** | 语言是否符合目标期刊的语域（register）？术语是否统一？ |

**当前 TCC 项目状态：**
- P1：✅ 正文已完成（v1.0，~9,200字），待语言润色
- P2：✅ 正文已完成（v28，~3,500词），Nature 格式合规

### 工序 7：数据与图表（Data & Visualization）

| 项目 | 内容 |
|------|------|
| **工具** | `statistical-analysis` / `xlsx` + ARS `visualization_agent` |
| **输入** | 论文中的定量数据 |
| **输出** | 统计检验结果 + 发表级配图（≥300 dpi，色盲友好） |
| **存储** | 图片存入 `figures/` 目录，数据存入 `data/` 目录 |
| **检查点** | 图表是否自包含（不依赖正文即可理解）？误差线和p值是否标注？ |

**当前 TCC 项目状态：**
- P1：✅ 5张配图已完成（`figures/`），⬜ 统计检验形式化待补充
- P2：✅ 6张配图已完成（`figures_cst/`），✅ 统计检验完整（Spearman ρ + Fisher exact + Bonferroni）

### 工序 8：交付排版（Format & Submit）

| 项目 | 内容 |
|------|------|
| **工具** | `latex-document-skill` / `docx` / `pdf` / `pptx` + ARS `formatter_agent` |
| **输入** | 工序6的正文 + 工序7的配图 |
| **输出** | 投稿版本（LaTeX + PDF + Cover Letter + SI） |
| **存储** | `06_Submission/` 目录 |
| **检查点** | 字数/图数/引用格式是否符合期刊规定？Cover Letter 是否写清创新点？ |

**当前 TCC 项目状态：**
- P1：⬜ LaTeX 格式排版待进行，⬜ Cover Letter 待撰写
- P2：⬜ Nature LaTeX 模板适配，⬜ SI 待撰写，⬜ Cover Letter 待撰写

---

## 三、当前项目工序进度矩阵

| 工序 | P1 (TCC-SDI) | P2 (CST-A1) |
|------|-------------|-------------|
| 1. 检索 | ✅ 43篇 | ✅ 50篇 |
| 2. 筛选 | ⬜ 待生成简报 | ⬜ 待生成简报 |
| 3. 选题 | ⬜ 待显式化RQ | ✅ RQ明确 |
| 4. 结构 | ✅ 7章 | ✅ IMRaD |
| 5. 草稿 | ✅ 完成 | ✅ 完成 |
| 6. 正文 | ✅ v1.0 | ✅ v28 |
| 7. 数据 | ✅ 5图 / ⬜ 统计 | ✅ 6图+统计 |
| 8. 交付 | ⬜ LaTeX+Cover | ⬜ LaTeX+SI+Cover |

---

## 四、关键习惯：每步产物归库

> **最重要的习惯只有一个：每跑完一步，把产出存进知识库，不要留在对话窗口里。**

| 工序产物 | 存入位置 | 文件名规范 |
|----------|----------|-----------|
| 文献列表 | Zotero `TCC_论文` 文件夹 | — |
| 主题简报 | `TCC_2_论文撰写/` | `[项目编号]_01_Literature_Brief.md` |
| 选题文档 | `TCC_2_论文撰写/` | `[项目编号]_02_Research_Questions.md` |
| 章节框架 | `TCC_2_论文撰写/` | `[项目编号]_03_Paper_Outline.md` |
| 综述草稿 | `TCC_2_论文撰写/` | `[项目编号]_04_Literature_Review.md` |
| 正文终稿 | `TCC_2_论文撰写/` | `[项目编号]_05_Manuscript.md` |
| 配图数据 | `TCC_2_论文撰写/figures[_cst]/` | `FigN_Description.png` |
| 投稿包 | `TCC_2_论文撰写/[项目编号]_Submission/` | `main.tex`, `cover_letter.pdf`, `si.pdf` |

---

> **版本：** v2.0 | 2026-06-17 | 基于 Research Units Pipeline 框架重构
