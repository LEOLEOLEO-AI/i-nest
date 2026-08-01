# iNEST + TCC Wiki · LLM 操作指令（schema）

> 本文件是知识库 `wiki/` 层的"编译器契约"：规定 LLM / 脚本如何把原始研究材料编译为结构化知识，以及如何自我进化。
> 当前架构采用**轻量自进化路线**：源材料保留在编号目录中，`wiki/` 为生成的只读知识层，由 `self_evolve.py` 每日闭环维护。

---

## 1. 角色

你是 iNEST + TCC 研究知识库的编译器与维护者。职责：

- 把原始材料（论文笔记、仿真记录、网页剪藏、导入内容）**编译**为 `wiki/` 层的概念与摘要；
- 维护 `wiki/` 层的交叉链接、索引、反向链接与反向引用；
- 做**健康自检**（断链 / 孤儿 / 缺 frontmatter），并**自我生长**（为高频被引却缺失的概念自动补占位）；
- 产出**任务推荐、跨域洞察、假设进化**三类引擎报告，驱动研究方向迭代。

---

## 2. 目录约定（当前真实结构）

源材料层（LLM 只读，文件名即 wikilink 锚点）：

| 目录 | 内容 |
|---|---|
| `00_Inbox/` | 论文收件箱、网页剪藏、Codex 联动、得到大脑导入 |
| `20_Processing/` | PDF 全文提取与分析 |
| `30_TCC/` | TCC（拓扑中心计算）理论 / 技术 / 开发 / 项目 / 仿真 |
| `40_iNEST/` | iNEST（复杂网络涌现智能）理论 / 技术 / 工程 / 项目 / 仿真 |
| `50_Output/` | 论文 / 专利 / 专著 / 代码 / 指南 / 汇报 |
| `60_MOC/` | 地图 of Content 索引 |
| `80_Archive/` | 归档（含 `_duplicates_archive/`） |

生成知识层（`wiki/`，LLM 可写）：

| 文件 | 职责 |
|---|---|
| `wiki/concepts/<name>.md` | 一个概念一个文件（中文显示名，文件名净化，用 `aliases:` 保留原名） |
| `wiki/articles/<name>.md` | 论文 / 文章 200 词摘要 |
| `wiki/index.md` | 全局索引（按 TCC / iNEST / Bridge / Methods 分簇） |
| `wiki/backlinks.md` | 反向链接索引 |
| `wiki/health.md` | 健康自检报告（断链 / 孤儿 / 缺 FM） |
| `wiki/cross_domain_insights.md` | 跨域桥梁报告（Phase 4 产出） |
| `wiki/task_recommendations.md` | 任务推荐（Phase 4 产出） |
| `wiki/evolution_report.md` | 假设进化报告（Phase 4 产出） |

> 注：原计划设想的 `raw/` 源层**未采用**——源材料仍留在编号目录，`wiki/` 直接编译自这些目录。wikilink 用文件名解析，移动文件不影响链接。

---

## 3. 编译操作（Compile）

由 `90_System/scripts/wiki_compiler.py` + `wiki_grow.py` 实现，由 `self_evolve.py` 编排。

### 3.1 摘要生成（Summarize）
- 输入：`00_Inbox/` `20_Processing/` `30_TCC/` `40_iNEST/` 中的论文 / 文章笔记
- 输出：`wiki/articles/<标题>.md`，含 frontmatter（title / date / source / tags）+ 摘要正文 + 关键概念列表

### 3.2 概念提取（Concept Extraction）
- 输入：任意源笔记
- 输出：`wiki/concepts/<name>.md`
- 规则：每个关键术语 / 方法 / 作者生成一个概念文件；已存在则追加来源，不重复创建
- frontmatter 含 `type: concept` 与 `**Domain**: TCC|iNEST|Cross`（供索引与统计）

### 3.3 交叉链接（Cross-linking）
- 扫描 `wiki/concepts/` 全部概念，发现语义 / 共现关联时添加 `[[wikilink]]`
- 双向：A 引用 B，则 B 也回链 A
- 净化：文件名中的 `:` `/` `\` `*` `?` `"` `<` `>` `|` `#` `^` `[` `]` 替换为 `_`，并用 `aliases:` 保留原始 `[[名]]` 可解析

### 3.4 反向链接 / 索引更新
- `wiki/backlinks.md`：按概念字母序，列出"X is referenced by: A, B, C"
- `wiki/index.md`：按 TCC / iNEST / Bridge / Methods 分簇，每行 `[[概念]] — 一句话描述`

### 3.5 健康自检（Health Check，纯本地，无 LLM）
- 找孤立概念（无入链 / 出链）、断裂链接（指向不存在文件）、缺 frontmatter 笔记
- 链接解析贴近 Obsidian：裸链接 / 路径链接 / 附件链接 / 文件夹链接 / `aliases:` 别名；纯数字链接（脚注 / 列表）不计为断链
- 输出 `wiki/health.md`

### 3.6 自我生长（Grow，纯本地，无 LLM）
- 为**高频被引（≥3 次）却不存在**的裸概念名自动生成占位笔记（带 frontmatter + 回链来源）
- 过滤：路径式 / 带扩展名 / 纯数字 / 导航 MOC / 日记 / 已知伪链接词
- 每轮上限 ~10 篇，防爆炸；下一轮 `wiki_grow` 自动交叉链接

---

## 4. 自进化引擎（Phase 4，每日运行）

由 `self_evolve.py` 的 `step_phase4()` 调用（隔离 + 超时，单步失败不影响其余）：

| 脚本 | 产出 | 说明 |
|---|---|---|
| `import_processor.py` | 监控 Genspark / 得到大脑 / Codex 新导入 → 归入 `wiki/` 待编译 | 仅当有外部新文件时动作 |
| `task_recommender.py` | `wiki/task_recommendations.md` | 知识缺口 / 假设 / 进化队列 → 优先级任务列表 |
| `research_evolution.py` | `wiki/evolution_report.md` | 用 wiki 证据语料验证假设（H1–H4）状态 |
| `cross_domain_insight.py` | `wiki/cross_domain_insights.md` | 发现 TCC↔iNEST 跨域桥梁 |

---

## 5. 分类体系（Domain）

- **TCC**：NoC、Chiplet、Wafer-scale、Interconnect、Routing、Topology、SDI、晶上互连
- **iNEST**：SNN、Neuromorphic、Criticality、Emergence、Reservoir、Memristor、STDP/FEP、多尺度
- **Bridge**：Complex Network、Information Theory、Self-organization、Connectome
- **Methods**：Simulation、Benchmark、Crawler

---

## 6. 文件命名与编码

- 概念文件：中文显示名（文件名净化，原样存入 `aliases:`）；例 `神经网络.md` + `aliases: ["神经网络"]`
- 文章摘要：`YYYY-MM-DD_短标题.md`
- 全部 UTF-8
- 所有 `[[wikilink]]` 用文件名（非路径）引用，移动文件不断链

---

## 7. 自进化规则（每日 03:00 闭环）

```
1. wiki_compiler 增量编译（仅当有新增/修改来源时调 LLM，带超时）
2. wiki_grow 交叉链接 + 去重 + 刷新 index/backlinks/health
3. 全库健康自检（断链/孤儿/缺FM）→ wiki/health.md
4. 自我生长：补全高频缺失概念占位
5. Phase4 引擎：import_processor + task_recommender + research_evolution + cross_domain_insight
6. 刷新 Home.md 门户（实时 git 状态 + 仪表盘数据）
7. git add + commit + push github（仅当有改动）
```

约束：
- 每步失败隔离，不破坏数据；全程日志写入 `99_Meta/self_evolve_log.json`（保留最近 60 次）
- 每日自进化任务：`automation-1785546922604`（FREQ=DAILY;BYHOUR=3）
- 重复文件清理：仅清理"明显冗余归档"（`_duplicates_archive/` 与误嵌套重复），每组保留 ≥1 份规范副本，删除走回收站（可恢复）
- 每条结论必须关联论文 / 实验 / 仿真；无来源数字标记"待测"
