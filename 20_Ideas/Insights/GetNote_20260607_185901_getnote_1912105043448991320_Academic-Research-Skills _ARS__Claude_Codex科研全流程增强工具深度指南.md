---
category: Tools-Tutorials
date: 2026-06-07 18:59
entities:
- ARS工具
- 科研全流程增强
processed: '2026-06-08T10:45:37.017037'
score: 9
source: GetNotes
source_file: GetNote_20260607_185901_getnote_1912105043448991320_Academic-Research-Skills
  _ARS__Claude_Codex科研全流程增强工具深度指南.md
summary: 介绍ARS科研增强插件的四大核心能力、13条命令及全流程调度，提升学术效率。
tags:
- 全流程调度
- 学术写作
- 科研工具
- paper
- research
title: getnote_1912105043448991320_Academic-Research-Skills _ARS__Claude_Codex科研全流程增强工具
---

## Original Note

---
note_id: 1912105043448991320
title: "Academic-Research-Skills (ARS)：Claude/Codex科研全流程增强工具深度指南"
type: link
created: 2026-06-07 06:56:32
source: getnote
kb: 
---

# Academic-Research-Skills (ARS)：Claude/Codex科研全流程增强工具深度指南

### **🔍 核心概述（背景）**

**工具定位**：ARS（Academic-Research-Skills）是基于Claude/Codex平台的科研增强插件，通过**四大核心能力**（研究、写作、评审、全流程调度）覆盖科研全链路，包含20+工作模式、近40个agent及学术诚信验证系统。  
**开发背景**：作者结合自身科研经验，旨在解决文献检索、论文撰写、审稿修改等流程中**重复性劳动**问题，提升科研效率。

### **🚀 快速部署与基础使用**

#### **(一) 安装步骤**
- **Claude Code版**：通过2行命令完成安装  
  ```bash
  /plugin marketplace add Imbad0202/academic-research-skills  
  /plugin install academic-research-skills
  ```
- **Codex版**：使用姐妹仓库`Imbad0202/academic-research-skills-codex`，提供`$academic-research-suite`技能包及`ars-*`别名。

#### **(二) 核心命令示例**
- **全流程启动**：`/ars-full`（10阶段一条龙调度）  
- **论文规划**：`/ars-plan`（苏格拉底式对话生成章节结构）  
- **文献综述**：`/ars-lit-review "研究主题"`（快速生成综述章节）

### **📋 13条核心命令速查表**

| 命令 | 调用skill | mode | 一句话用途 |
| :--- | :--- | :--- | :--- |
| `/ars-full` | academic-pipeline | 全流程编排 | 从研究到定稿，10阶段一条龙（旗舰命令） |
| `/ars-plan` | academic-paper | plan | 苏格拉底式对话，逐章规划论文结构 |
| `/ars-outline` | academic-paper | outline-only | 生成详细大纲+证据地图（不写全文） |
| `/ars-lit-review` | academic-paper | lit-review | 整理已有文献为综述章节 |
| `/ars-reviewer` | academic-paper-reviewer | full/quick等 | 模拟5人同行评审 |
| `/ars-revision` | academic-paper | revision | 按审稿意见生成修改稿+逐点回复 |
| `/ars-revision-coach` | academic-paper | revision-coach | 解读审稿意见，输出修改路线图 |
| `/ars-abstract` | academic-paper | abstract-only | 生成双语摘要+关键词 |
| `/ars-citation-check` | academic-paper | citation-check | 检查引用规范及文内列表匹配性 |
| `/ars-disclosure` | academic-paper | disclosure | 生成符合期刊规范的AI使用声明 |
| `/ars-format-convert` | academic-paper | format-convert | 格式转换（MD/LaTeX/DOCX/PDF+引用格式互换） |
| `/ars-mark-read` | 脚本 | 无 | 标记文献「已亲自读过并核实」 |
| `/ars-unmark-read` | 脚本 | 无 | 撤销已读标记 |

### **💡 四大核心能力解析**

#### **(一) deep-research：文献检索与研究**
- **13个agent的研究团队**，支持7种模式，覆盖从快速概览到系统性回顾：  
  | 模式 | 核心功能 | 输出规模 | 典型场景 |
  | :--- | :--- | :--- | :--- |
  | full | 完整研究六阶段 | 3,000–8,000词 | 从零开始的研究项目 |
  | quick | 主题概览简报 | 500–1,500词 | 快速了解领域动态 |
  | fact-check | 声明验证（VERIFIED/PLAUSIBLE等4级裁决） | 逐条验证报告 | 防AI编假文献 |
  | socratic | 5层提问引导（澄清→假设→证据→视角→后果） | 聚焦研究问题 | 模糊想法转化为具体课题 |
  | systematic-review | PRISMA 2020规范 Meta分析 | 5,000–15,000词 | 临床/循证决策研究 |

- **核心机制**：通过Semantic Scholar API+OpenAlex+Crossref三重验证文献可信度，自动检测掠夺性期刊。

#### **(二) academic-paper：论文撰写与优化**
- **12个agent的写作团队**，10种模式覆盖写作全流程：  
  - **风格校准**：上传3篇以上个人论文生成「风格档案」，避免AI腔  
  - **质量检查**：限制26个AI高频词（如delve/tapestry）、破折号≤3个、删除冗余开头  
  - **关键模式分工**：  
    - `revision`：直接修改稿件生成修订追踪  
    - `revision-coach`：仅输出修改策略，不动稿件  
    - `lit-review`：将deep-research检索结果整理为综述章节  

#### **(三) academic-paper-reviewer：多视角同行评审**
- **7个agent的评审团**（主编+3位审稿人+魔鬼代言人+综合编辑），6种模式：  
  - **评分体系**：0-100分（原创性20%/方法严谨性25%/证据充分性25%/论证连贯性15%/写作质量15%）  
  - **决策映射**：≥80接受/65-79小修/50-64大修/<50拒稿  
  - **魔鬼代言人机制**：对核心论点（假设可证伪/结论推导/数据矛盾/替代解释）拥有**一票否决权**  

#### **(四) academic-pipeline：10阶段全流程调度**
- **旗舰功能**（对应`/ars-full`），串联前三大skill，包含**两道强制学术诚信验证**：  
  | 阶段 | 名称 | 调用模块 | 核心产物 |
  | :--- | :--- | :--- | :--- |
  | 1 | 研究 | deep-research | 研究问题简报+文献分析 |
  | 2 | 撰写 | academic-paper | 论文草稿 |
  | **2.5** | **完整性验证** | integrity agent | 不可跳过的验证报告 |
  | 3 | 审稿 | reviewer | 5份审稿意见+修改路线图 |
  | 4 | 修改 | academic-paper | 修改稿+逐点回复 |
  | **4.5** | **最终验证** | integrity agent | 100%通过方可定稿 |
  | 5 | 定稿 | academic-paper | 多格式输出（MD/DOCX/LaTeX/PDF） |

### **📝 推荐工作流**

#### **场景一：从零写完整论文**

`/ars-plan`（结构规划）→ `/ars-outline`（大纲确认）→ `/ars-full`（全流程执行）→ `/ars-citation-check`（引用检查）→ `/ars-abstract`（双语摘要）→ `/ars-disclosure`（AI声明）  

#### **场景二：已有草稿准备投稿**

`/ars-reviewer`（自审挑错）→ `/ars-citation-check`（引用完整性）→ `/ars-format-convert`（期刊格式转换）  

#### **场景三：收到审稿意见大修**

`/ars-revision-coach`（解读意见）→ 人工确认策略 → `/ars-revision`（生成修改稿）→ `/ars-reviewer`（re-review模式验证）  

### **🔑 补充细节**
- **数据访问层级标注**：v3.3.2+版本声明`data_access_level`（raw/redacted/verified_only），由`check_data_access_level.py`强制执行，防止数据滥用。  
- **可复现性LockFile**：v3.3.5+通过Material Passport添加`repo_lock`子区块，确保配置文件可追溯（非逐字节复现）。  
- **ARS与传统工具差异**：不替代研究者判断，聚焦解放机械性劳动（文献检索/格式转换/引用核对等），将精力集中于问题设计与结果解读。

---
*getnote | 2026-06-07 18:58*


---

## Related Notes

[[Papers-MOC]]
[[iNEST-MOC]]