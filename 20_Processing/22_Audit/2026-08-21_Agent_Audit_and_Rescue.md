---
direction: processing
title: "Agent 目录考古审计与抢救执行报告"
created: 2026-08-21
provenance: dsh-audit
---

# Agent 目录考古审计与抢救执行报告（2026-08-21）

> 审计执行方：DSH 审计代理（4 并行子代理 + 主代理复核），全程只读；抢救执行为受控写入。
> 关联纪律：AGENTS.md §0 数据真实性铁律、§1.4 目录管理三定律、§5 Git 白名单与配额。

## 一、审计对象与结论（TL;DR）

**对象**：`D:\Obsidian\Agent\`（275 个非 venv 文件 ≈ 90MB）+ 关联验证（`vault\` 仓库、`scripts\`、`tmp_gh\`、git 状态）。

**一句话结论**：`Agent\` 是 2026-03 搭建、06-23 "猝死"的科研 Agent 平台快照——平台外壳（ToolUniverse 生态叙事）是死代码，内核有两处真实遗产（DAC 任务管理方法论 + 单文件科研管线实现），真正高价值的理论资产在目录外（handoff、tmp_gh/sdi_sim），且存在密钥泄露与核心实验数据游离版本控制两类风险。

**两代平台进化史**：
| 代际 | 时间 | 框架 | 结局 |
|---|---|---|---|
| 第一代 | 03-12~03-15 | ToolUniverse（Harvard Zitnik Lab）+ DAC 三角色 | 90% mock 适配器，3 月检索结果关键词污染 |
| 第二代 | 05-30~06-23 | 自研 Python 每日管线（SiliconFlow DeepSeek） | 06-23 断更，唯一成功运行 05-30（10 篇/374s） |

**断更根因（已定位）**：`daily_pipeline.py` 自 05-31 起连续 SyntaxError（line 330 unmatched ')' → line 31 GBK '©' 无 encoding 声明），Windows 计划任务硬编码指向已删除的 `D:\Agent\` 路径；06-23 08:00 最后一次尝试后任务废弃。23 天静默失败无告警——脚本级自动化的典型死法。现行管线（`vault\90_System\scripts\pipeline_v3.py` + `scripts\iNEST_pipeline.ps1`）不受影响，仍在演进。

## 二、资产清单与处置（10 项可复用）

### 🟢 抢救入库（已完成）
| # | 资产 | 去向 |
|---|---|---|
| 1 | tmp_gh/sdi_sim 全套（304 文件/76.6MB）快照 | `_backups/sdi_sim_snapshot_20260820/`（字节校验一致） |
| 2 | sdi 独有代码/文档 49 个（.py/.md） | `vault/40_iNEST/45_Simulation/sdi_sim/`（未覆盖 vault 新版同名文档） |
| 3 | sdi 独有数据 75 个（.json/.png/.log） | `vault/40_iNEST/45_Simulation/data_local/sdi_sim_results_snapshot_20260820/`（git 忽略，落盘不落库） |

### 🟡 待迁移（未执行）
| # | 资产 | 建议去向 |
|---|---|---|
| 4 | `02-Simulation-Platform/handoff/theory_handoff_latest.json`（5 条 CLM 命题） | 转 DSH 仿真任务单 |
| 5 | `Snapshots/web/20260313/` 4 份全文快照（iNEST理论.md 必抢救） | 40_iNEST 理论区 |
| 6 | `generated_docs/llm_analysis_20260530.json` + results_20260530_* | 转 Obsidian 文献笔记 |
| 7 | 基类文献 API 适配器 4 个 + 手稿数学验证引擎 | 提炼为脚本/技能 |
| 8 | DAC 模板三件套 | 去 ToolUniverse 化后并入编排层 |
| 9 | scripts 工具链 6 个（daily_pipeline/llm_paper_analysis/knowledge_base_ingest/pdf_to_markdown/evernote_share_export/link_import_mvp） | 复制到 `D:\Obsidian\scripts\` 改 AGENT_ROOT |
| 10 | `iNEST理论.html`（300KB 最新版）+ literature_index 字段设计 | 40_iNEST + 新索引模板 |

### 🔴 归档/清理建议（未执行，待用户确认）
- 归档：execution_log 52 份、3 月 results_* 44 份（过程证据勿入文献库）、8 份 3/12 交付文档、ObsidianVault 24 个 LIT 副本、48 个 stub
- 清理：_skills/_specialized_modules 空目录、03/04 空目录、__pycache__、0 字节日志、.bak

## 三、风险与待办（按严重度）

1. **🔴 密钥泄露**：`Agent/scripts/register_scheduled_task.ps1:9` 硬编码真实 SiliconFlow API Key（sk-ewvmx…）。**请立即在硅基流动控制台轮换该 Key**；密钥今后只走环境变量。
2. **🟠 论文数据保全（已解决）**：tmp_gh/sdi_sim 58+ 结果文件曾游离版本控制——现已快照至 _backups 并落盘 data_local。
3. **🟠 数据真实性**：SDI 论文草稿数字需按 §0.1 标注 [实测] 来源；VERSION_LOCK + run logs 提供追溯链，需链接进论文草稿。
4. **🟡 git 卫生**：`D:\Obsidian\.git` 是空壳目录（真仓库在 vault/）；WorkBuddy 记录 github/main 分叉 296 ahead/167 behind 持续数日，需人工解决。
5. **🟡 敏感文件**：`Agent/Resume.docx` 为真实具名个人推荐材料（含军职履历），按隐私单独处置勿入库。

## 四、教训资产（对现行管线设计）

- Task-01 "平台空转"标本：目标宏大（500+ 论文）无分阶段验收、评审清单从未填写 → 任何任务必须有分阶段可验证中间产物。
- 去重指纹失效产生 79% 冗余（60.42MB）→ 现行 dedup_* 脚本家族由此而来。
- 旧文献数据不清洗直接重跑（违反 §6.1/6.2 检索语义与 §0.x 铁律）。
- 静默失败 23 天 → 自动化必须有健康监控与告警（对照 AUTOSTART_RUNBOOK 的健康检查制度）。

## 五、审计方法记录

- 4 并行子代理分区审计：01-Theory-Research / execution_log+generated_docs+scripts+apps / _core_framework+_dac_templates+_docs+agent-research / 杂项+空目录
- 复核手段：git ls-files/check-ignore、哈希比对（MD5）、robocopy 校验、live 插件清单 RPC 核查
- 全程只读审计；抢救写入均在上述清单内


<!-- orphan-cleanup: no MOC found, tagged -->
