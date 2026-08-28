---
title: 知识库与科研智能体诊断报告 2026-08-27（对照 Hermes Agent 理念）
date: 2026-08-27
status: review
provenance: codex-agent
---

# 知识库与科研智能体诊断报告（2026-08-27）

> 触发：用户分享得到笔记"Hermes agent 比 Claude(Claw/OpenClaw) 更好"，要求据此对知识库与科研智能体再次诊断。
> 诊断方式：只读检查 + 今日管线日志/看板实测 [实测] + 既往三份诊断对照（08-11 / 08-23 / 08-26）。
> 数据真实性：本报告所有数值标注来源；Hermes 相关论断均为 [引用] 公开来源，未经实测。

## 〇、分享内容还原（诚实声明）

- 分享链接 `biji.com/note/share_note/6gBRB9LPOlr52` 为得到笔记分享页。本地沙箱无外网、得到大脑 21:00 才同步新笔记，**未能直接读取原文**。
- 按主题检索到的公开同源材料（"Hermes Agent 比 Claude Code / OpenClaw 更好"）：[澎湃·爱马仕联合创始人Karan访谈](https://m.thepaper.cn/newsDetail_forward_33716739)、[36氪·全面超越"龙虾"的"爱马仕"](https://www.36kr.com/p/3885672353659781)、[腾讯云·Hermes 与 Claude Code、OpenClaw 三角博弈](https://cloud.tencent.cn/developer/article/2658963)、[官方文档](https://hermes-agent.nousresearch.com/docs/zh-Hans/)。
- Hermes Agent 核心卖点（[引用]）：① 失败复盘→自动沉淀**技能**；② **三层记忆**（工作/短期/长期+向量检索）；③ **MoA 多模型协作**；④ **上下文压缩/缓存**省 token；⑤ 开源可控、数据本地；⑥ Atropos RL 运行时调优。反面意见：写代码能力弱、自建技能缺正确性保障（[GitHub #25833](https://github.com/NousResearch/hermes-agent/issues/25833)）、"更好"缺系统对照评测。

## 一、总体判定：B−（基建已跑通，产出闭环仍缺最后一公里）

对照 08-11（管线暂停卡死）与 08-23（C+，摄入空转/同步不发布），**基建层已修复**：

- ✅ 管线每日 06:30 运行并 `completed`（今日 new_papers=7，exit 0）[实测]
- ✅ 健康看门狗 CRIT=0 WARN=0 [实测]（[health_watchdog](http://127.0.0.1:8899/vault/70_Dashboard/health_watchdog.md)）
- ✅ 21:00 同步正常（上次 13.9h 前完成）；GetNotes 拉取正常（434 条）[实测]
- ✅ 洞察文件每日生成（02_DeepSeek_Insights 质量优秀，能映射 TCC/iNEST 并产出论文 idea）[实测]

但**加工→产出闭环未通**，且与 Hermes 理念对照存在 5 项结构性差距：

| # | Hermes 能力 | 用户现状 [实测] | 差距 |
|---|---|---|---|
| 1 | 技能沉淀（失败→技能） | 有 `99_Meta/lessons_learned.md`（L-001~005，结构化教训），但**GBK 编码损坏**、教训只改规则不产技能；`90_System/skills/` 仅 1 个 gsk-outlook-email 占位 | 有教训库，无技能库，无自动调用 |
| 2 | 分层记忆 | 有状态文件群（hypothesis_registry / evolution_ledger / research_state），但分散无统一 schema、无跨会话必读机制；.neural_memory/.claudian/.openclaw 均为空壳（1 文件） | 有数据，无"记忆" |
| 3 | MoA 多模型路由 | 有 `scripts/llm_config.json` 四路供应商（jojo/nvidia/gemini/cc_switch），但管线单模型；`model_switch.json`(glm-5.2, 07-19) 与 `llm_config.json`(active=nvidia) 与 `llm_model_registry.json` **三处漂移** | 有路由器，无路由策略 |
| 4 | 上下文/Token 治理 | AGENTS.md 有 token 铁律（08-11 已落地），但 `wiki/backlinks.md` 已膨胀到 **4.3MB**（08-11 时 2.35MB），wiki compiler 今日 **60s 超时** | 有禁令，无机制 |
| 5 | 自进化闭环 | self_evolve/meta_evolution 在跑，但 wiki 概念从 08-23 的 6153 → 今日 **6258**（无新论文也涨），孤儿概念 58% 未回收 | 进化≠产出，有通胀风险 |

## 二、实测问题清单（按优先级）

### P0（直接卡科研产出）

- **P0-1 分类环节失效——积压净零的根因**：今日管线日志 `[Process] Classified: 0`（limit=20 全未分类）[实测]。结果：00_Inbox **215 篇**、20_Processing **561 篇**，与 08-11（217/567）几乎相同——**16 天净零消化**。新论文无法路由进 30/40 结构。
- **P0-2 arXiv 洞察模板化**：今日 `02_Research_Insights.md` 5 条洞察全部是"建议阅读全文,评估方法论借鉴价值"复读 + 2 条截断标题（"with Distillation Ass"）[实测]。与同目录 `02_DeepSeek_Insights.md`（能提炼机理、映射 TCC、给出目标期刊）形成鲜明反差——**同一库内两种产出质量**。
- **P0-3 wiki 通胀失控**：wiki 6258 个 md；backlinks.md 4.3MB（git 已排除但仍在本地被反复编译）；wiki compiler 60s 超时 [实测]。

### P1（卫生与可观测）

- **P1-1 摄入源单一化**：今日 S2=0（无 key 或仍 429）、GN=0（Google News RSS 超时 WinError 10060），仅 arXiv 7 篇 [实测]。08-23 的限流问题只解决了一半。
- **P1-2 AGENTS.md 未版本化**：位于 `D:\Obsidian\AGENTS.md`，在 vault git 仓库之外（08-23 项 #8 未修复）[实测]——智能体"宪法"不受版本控制。
- **P1-3 lessons_learned.md GBK 编码损坏**：meta_evolution 写出的文件非 UTF-8，Obsidian/agent 读为乱码 [实测]。
- **P1-4 配置三处漂移**：llm_config.json（active=nvidia）/ model_switch.json（glm-5.2）/ llm_model_registry.json 互不一致 [实测]。
- **P1-5 命名与整洁失守**：中文文件名大量存在（08-23 实测 2879 个）；90_System 内 484 个文件含大量 MD5 jpg 附件 [实测]。

### P2（承接 08-26 诊断，科研主线）

- 稿件线三线并存（ASPLOS v4.0 / Universal / Physical Limits）+ genspark 双版本；USL 论文全部预测仍为 [S]/[M] 标注、**无一张 [仿真] 图**；P3 仿真最小闭环未启动。

## 三、改进建议（对照 Hermes，可直接执行）

### A. 建立"技能库"层（Hermes Skills 简化版）——P0
1. 把 `99_Meta/lessons_learned.md` 升级为**技能注册表** `90_System/skills/registry.md`：每技能 = 触发条件 / 步骤 / 验收标准 / 版本 / 来源教训编号。
2. 新增自动管线：watchdog 连续 2 次同类失败 → 生成教训条目（L-编号）→ meta_evolution 提炼为技能草案 → 人工审核入库。
3. 首批沉淀 5 个高频技能：文献分类（修复 P0-1）、arXiv 洞察生成（修复 P0-2）、公式核验、引用核验、CST 仿真验收——每个技能挂到对应管线环节，agent 按技能调用而非每次重写 prompt。

### B. 记忆分层 + 会话必读清单（Hermes 三层记忆）——P0
1. 短期：保留 `research_state.json`（当日状态）。
2. 中期：60_MOC 洞察/任务，强制"每日四数"（输入/处理/输出/拒绝）写入 `70_Dashboard/data.js`——当前 `data.json` 仅 704B，四数缺失 [实测]。
3. 长期：统一 99_Meta 注册表群 schema（id/版本/updated/证据标注），限定 agent 会话开始只读 ≤5 个状态文件，其余按需检索（Omnisearch 限定目录）。
4. 清理空壳记忆目录（.neural_memory/.neural_db/.claudian/.openclaw），避免误导。

### C. 管线分级模型路由（MoA 简化版）——P1
1. 分类环节用便宜模型（gemini-2.0-flash 或 deepseek fast 档）；洞察/综述生成用强模型（deepseek-v4-pro / glm-5.2）；数学与公式核验走专用技能或 reasoning 档（nvidia nemotron）。
2. 统一三份配置：`llm_config.json` 为 SSOT，`model_switch.json` 降级为覆盖层，删除 registry 冗余。

### D. 洞察质量门——P0（最影响科研价值）
1. 重写 arXiv 洞察生成器：7 篇/日必须输出"该文与 TCC/iNEST 的关联、可借鉴方法、应写入哪个 30/40 主题、建议行动"四项，**禁止**"建议阅读全文"句式。
2. 接 `quality_gate.py`：检出模板句/截断标题 → 判失败重试。
3. 洞察强制双向链接到库内已有笔记，并落盘到对应主题目录（不只写 MOC）。

### E. wiki 瘦身与索引——P1
1. backlinks.md 按月归档截断（4.3MB 持续膨胀）；wiki compiler 改增量编译（今日 60s 超时）。
2. 执行 08-23 已建议未执行的闸门：**self_evolve 无新论文则冻结新增概念**；孤儿概念按周回收。

### F. 科研产出闭环（对接 08-26 诊断）——P1/P2
1. 最高优先：P3 仿真最小闭环，产出第一张 [仿真] 图（验证 ĥτc=O(1)），USL 论文标注从 [S]/[M] 升级。
2. 稿件线 SSOT 裁定（沿用 08-26 裁定流程）合并 ASPLOS/Universal/Physical Limits。
3. 每周一产出回顾：论文/专利/仿真各线进展 vs 计划，写入看板。

### G. 治理卫生——P1
1. AGENTS.md 纳入版本控制（根目录建 git 或移入 vault 并软链）。
2. lessons_learned.md 转 UTF-8（meta_evolution 输出编码统一）。
3. 中文文件名分批重命名（新文件先行，存量按目录分批）。

## 四、执行顺序与两周验收

| 阶段 | 动作 | 验收 |
|---|---|---|
| 第 1 周 | A(技能库) + B(记忆schema) + D(洞察质量门) + P0-1 分类修复 | Inbox ≤150、Processing ≤450；洞察无模板句；wiki 停止净增 |
| 第 2 周 | C(路由) + E(wiki瘦身) + F(P3 仿真图) + G(治理) | 产出首张 [仿真] 图；backlinks ≤2MB；AGENTS.md 入 git |

## 五、一句话结论

**基建已从"跑不起来"修到"跑得动"，但知识库正以"输入 7 篇/日、消化 0 篇/日、wiki 空转膨胀"的方式空转；对照 Hermes，最短路径不是换工具，而是把已有的教训库/状态文件/多模型路由器升级为"技能+记忆+路由+质量门"四件套，并让 arXiv 洞察从模板复读变成可入库、可链接、可行动的研究推进。**
