---
title: Codex Agents 与 Skills 诊断报告
date: 2026-09-06
reviewed: 2026-09-06
status: completed
domain: TCC+iNEST
verification_task: V-OPS01
---

# Codex Agents 与 Skills 诊断报告

## 1. 诊断结论

当前 Codex 已形成“研究路由 + 证据契约 + 阶段工作流 + 显式运维技能”的基本架构，适合继续作为 TCC+iNEST 科研智能体的中枢。

本轮已完成配置、技能、领域知识边界和离线护栏的收敛。复核了治理矩阵、模板、离线路由边界与 passport 迁移行为；未执行 Git push、知识库同步、自动化任务或破坏性 Git 操作。

## 2. 问题分级

### P0：数据真实性边界

已修复：

- CST/代码仿真不再被表述为实验事实。
- 研究结论统一要求证据标签、来源或方法、`V-*` 验证任务、验收标准和局限。
- `[实测]`、`[仿真]`、`[引用]`、`[推导]`、`[假设]`、`[综合]`、`[待测]` 已纳入统一契约。
- TCC/SDI 与 iNEST 领域知识中的设计目标、项目愿景、工作假设和外部证据已分层；未经实验卡或来源支持的“已证明/已完成/已达标/唯一”等表述已移除。
- 两个领域文件新增 `V-SDI01`–`V-SDI05` 与 `V-iNEST01`–`V-iNEST06`，把原语表达能力、互连性能、连接组复核、临界性、因果对照和 FEP 理论审计转为可执行任务。

### P1：任务路由与技能重复

已修复：

- 统一任务类别：`RQ/LIT/TH/SIM/SYS/PAPER/OPS`。
- 新增并启用 TCC+iNEST 主路由技能 `tcc-inest-research-router`。
- 多阶段任务先建立最小任务卡，长任务恢复先读取状态、handoff 和 diff。
- 同步、收件箱管理和文献爬取均改为显式调用。
- 用户级路由文档补充 `m01`–`m17`、`a01`–`a10` 到真实技能目录名的唯一映射，降低别名漂移风险。
- passport 允许旧台账以历史别名读取并给出迁移警告，但新阶段追加历史别名会被拒绝；空阶段列表序列化也已修正为跨 YAML 解析后端一致的 `stages: []`。

### P1：路径和入口漂移

已修复：

- Vault 统一为 `D:\Obsidian\vault`。
- 收件箱统一为 `D:\Obsidian\vault\00_Inbox`。
- 文献管线统一使用 `D:\Obsidian\vault\90_System\scripts\pipeline_v3.py`。
- 移除爬虫技能中不存在的 `paper_atomizer.py`、旧 `10_Inbox` 输出假设和虚构的 `papers/` 目录。
- 健康检查、收件箱处理、增量整理和仪表盘入口均改为真实路径。

### P1：同步安全边界

已修复：

- `sync-inest` 与 `inest-knowledge-sync` 均为 `explicit` 调用。
- 仅允许按现有脚本执行 `-StatusOnly`、`-Publish`、`-SkipGetNotes`。
- 删除对不存在的 `-DryRun` 参数的依赖。
- 明确 GitHub-only，禁止 Gitee push、force push、未经检查的 stash/pull、历史重写和未审查覆盖。
- 外部材料必须先进入 Inbox，不得直接写入正式知识区。

## 3. 已修改工件

- `D:\Obsidian\AGENTS.md`
- `D:\Obsidian\.codex\research_agent_contract.yaml`
- `D:\Obsidian\.codex\codex_plus.yaml`
- `D:\Obsidian\.codex\workflows\research_router.md`
- `D:\Obsidian\.codex\workflows\cst_simulation.md`
- `D:\Obsidian\.codex\workflows\paper_pipeline.md`
- `C:\Users\LEO\.agents\skills\tcc-inest-research-router\SKILL.md`
- `C:\Users\LEO\.codex\skills\sync-inest\SKILL.md`
- `C:\Users\LEO\.codex\skills\obsidian-kb-manager\SKILL.md`
- `C:\Users\LEO\.codex\skills\iNEST-knowledge-sync\SKILL.md`
- `C:\Users\LEO\.codex\skills\iNEST-research-crawler\SKILL.md`
- `D:\Obsidian\.codex\skill_governance.yaml`
- `D:\Obsidian\.codex\validate_research_agent.py`
- `D:\Obsidian\.codex\templates\research\run_manifest.md`
- `D:\Obsidian\.codex\templates\research\claim_evidence_table.md`
- `D:\Obsidian\.codex\domain\sdi_knowledge.md`
- `D:\Obsidian\.codex\domain\inest_knowledge.md`
- `C:\Users\LEO\.agents\skills\light-orchestrator\scripts\passport.py`

2026-09-06 复核期间的治理修正：

- 每个阶段的 `primary` 强制为单一字符串，`primary_sequence` 必须存在且首项等于该主技能。
- `PAPER` 执行序列调整为“起草 → 引用核验 → 自审 → 数学核验”，避免把验证技能误标为阶段主技能。
- 校验器新增角色重叠、必需验证器、SIM 正式结论前置工件、Markdown/YAML 模板结构和显式调用策略检查。
- `SIM` 正式结论要求同时具备 `experiment_card.yaml`、`run_manifest.md` 和 `claim_evidence_table.md`。

说明：技能目录中部分历史目录名保留了大小写，以避免破坏现有引用；其 frontmatter 技能名已符合校验器要求。

## 4. 技能路由策略

| 用户目标 | 主类别 | 首个工件 | 后续阶段 |
|---|---|---|---|
| 判断想法是否值得做 | `RQ` | `question_card.md` | `LIT -> TH/SIM` |
| 查找和综合论文 | `LIT` | `evidence_ledger.md` | 题录核验 -> 证据综合 |
| 建立数学模型 | `TH` | `theory_scaffold.md` | 假设 -> 推导 -> 验证 |
| CST/代码/FPGA验证 | `SIM` | `experiment_card.yaml` | baseline -> 统计 -> 敏感性 |
| TCC/SDI系统设计 | `SYS` | `design_note.md` | 接口 -> 资源 -> 验证 |
| 论文、专利、基金交付 | `PAPER` | `deliverable_manifest.yaml` | 引用审计 -> 自审 |
| Inbox、健康、Git操作 | `OPS` | `ops_report.md` | 状态检查 -> 显式动作 |

## 5. 验证结果

- 技能格式校验：目标技能全部通过。
- YAML 解析：`research_agent_contract.yaml`、`research_keywords.yaml`、`codex_plus.yaml` 全部通过。
- 治理校验器：`research-agent validation: 0 error(s), 0 warning(s)`。
- 模板结构校验：所有阶段首个工件模板存在；SIM/PAPER 所需字段和正式结论工件存在。
- 离线路由演练：输入“评估可编程拓扑与物理储备池结合是否形成可证伪研究问题”应路由为 `tcc-inest-research-router → RQ`，首个工件为 `question_card.md`，验证任务为 `V-RQ01`；后续分支为 `LIT → TH/SIM`。本演练不写入 Vault。
- 真实入口检查：论文管线、Inbox 处理、增量整理、健康看门狗和同步脚本均存在。
- 同步参数核对：脚本实际支持 `-Publish`、`-StatusOnly`、`-SkipGetNotes`；未发现 `-DryRun` 参数。
- passport 离线自测：合法真实技能名、非法 gate、乱序阶段、缺字段、历史别名拒写、旧台账迁移警告和空列表往返均通过。
- 历史别名扫描：`m01`–`m17`、`a01`–`a10` 仅保留在兼容映射与迁移回归测试中，未进入正常阶段示例。
- Git 状态：Vault 存在用户或自动化产生的大量既有未提交变更，本轮未清理、回滚或覆盖。

## 6. 剩余风险

1. `.codex` 与用户级 skills 不在 `D:\Obsidian\vault` Git 仓库内，配置变更的版本保护依赖本机文件备份。
2. Vault 当前存在大量历史断链、缺少 frontmatter 和自动化生成变更；这些不属于本轮 agents/skills 配置修复，不能据此宣称知识库已健康。
3. `gitee_sync.ps1` 文件名仍是历史遗留名称；技能层已明确 GitHub-only，但后续维护者仍可能被文件名误导。
4. 文献爬取依赖外部来源和运行时依赖；检索结果只能作为候选材料，题录和论点仍需单独核验。
5. 技能路由规则目前是契约和文档层约束，不能替代每次任务中的实际证据审计。
6. 领域知识文件现在只提供研究边界和验证入口；`V-SDI*`、`V-iNEST*` 尚未因本次离线校验而产生新的实验结果。

## 7. 后续最小动作

### V-OPS01：配置与运维链路复核

- 方法：在不发布、不同步的前提下，重新运行技能格式校验、YAML 解析、入口存在性检查和同步脚本参数检查。
- 验收标准：所有目标技能通过校验；配置可解析；入口存在；脚本参数与技能文档一致；无自动 push 行为。
- 当前状态：通过。

### V-LIT01：文献候选核验

- 方法：对爬虫产生的候选逐条核验 DOI/arXiv ID、题名、作者、日期、来源和论点支撑关系。
- 验收标准：未核验候选保持 `unverified`；完成核验的题录才可标记 `[引用]`。
- 当前状态：待后续文献任务触发。

### V-SIM01：仿真可复现性

- 方法：按 `experiment_card.yaml` 登记参数、随机种子、baseline、统计方法、置信区间和敏感性分析。
- 验收标准：结果可复现，且不把仿真观察直接升级为实验事实或普适定律。
- 当前状态：待具体实验卡。

### V-RQ01：路由与问题卡闭环

- 方法：用 TCC+iNEST 路由回归样例检查领域入口、任务类别、首个工件、验证任务和下一阶段映射。
- 验收标准：不联网、不写 Vault 时，输出仍明确为 `tcc-inest-research-router → RQ`，且不把假设升级为事实。
- 当前状态：离线结构演练通过；真实问题仍需用户任务触发后填写问题卡。

### V-SDI01–V-SDI05 / V-iNEST01–V-iNEST06：领域证据闭环

- 方法：按两个领域文件中的任务定义，分别完成原语形式化、互连实验卡、拓扑规模推导、活性模型检查、同口径方案对比、连接组版本复核、替代分布分析、同步/信息效率对照、拓扑-动力学因果实验、跨尺度复核和 FEP 理论审计。
- 验收标准：每项数字和结论均可追溯到 `[实测]`、`[仿真]`、`[引用]`、`[推导]` 或 `[假设]`；未完成任务保持 `[待测]`，不得从配置校验结果升级为科学结论。
- 当前状态：验证任务框架已建立，具体实验与文献核验待后续研究任务触发。

## 8. 总体判定

状态：`完成（配置、路由与证据边界层，2026-09-06 复核通过）`

当前系统可以作为 TCC+iNEST 科研智能体使用。下一阶段重点不是继续增加技能数量，而是用真实任务检验路由是否正确、证据台账是否闭合、领域验证任务是否真正执行，并逐步淘汰重复或仅提供泛化提示的技能。文献检索、题录核验和科学结论仍需按用户明确任务执行，不能由本次离线配置校验代替。
