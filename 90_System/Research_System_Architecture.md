---
provenance: external
---

# TCC + iNEST 实时研发系统架构

更新日期：2026-07-19

## 目标

系统的目标不是展示信息，而是把知识库更新持续转化为论文、专利、项目指南、仿真和代码的可验证产出。

## 单一事实源

| 数据 | 权威来源 | 消费者 |
|---|---|---|
| 知识库数量、服务状态、待处理量 | `99_Meta/research_state.json` | Home、看板、健康检查 |
| 今日任务 | `60_MOC/03_Daily_Action.md` + `60_MOC/04_Daily_Focus.md` | 看板、Home、Codex 执行 |
| 论文洞察 | `00_Inbox/_pipeline_insights/*.md` | 每日行动、看板、证据账本 |
| 管线进展 | `logs/pipeline_*.json` | 看板近三日、周度健康检查 |
| 成果状态 | `50_Output/` | 看板成果区、Home、Git 同步 |

## 唯一发布器

`90_System/scripts/research_publisher.py` 是唯一写入 `70_Dashboard/data.js` 的脚本。

旧入口 `daily_kanban_update.py`、`dashboard_data_v3.py`、`refresh_dashboard.py` 仅保留兼容调用，不能再写静态 HTML、旧日期、`localStorage` 或手工任务。

## 动态闭环

```text
来源剪藏 / 文献检索
  -> 00_Inbox/_pipeline_insights
  -> 相关性筛选与深度分析
  -> 03_Daily_Action + 04_Daily_Focus
  -> 研究执行：论文 / 专利 / 仿真 / 代码 / 项目指南
  -> 30_TCC / 40_iNEST / 50_Output 的证据与成果
  -> state_generator + research_publisher
  -> Home + 研发看板 + 周度健康检查
```

## 定时任务职责

| 时间 | 任务 | 允许写入 |
|---|---|---|
| 08:00 | `iNEST_Daily_Pipeline` | 论文洞察、每日行动、运行日志、状态、实时看板数据 |
| 08:30 | `iNEST_Daily_Kanban_Update` | 仅刷新实时看板数据 |
| 20:00 | `iNEST_Inbox_Afternoon` | 收件箱归类、双向链接、待验证项 |
| 21:00 | `iNEST_Daily_Sync` | GitHub/Gitee 同步 |
| 周六 22:30 | `iNEST_Knowledge_Evolution` | 证据账本、假设注册、状态、实时看板数据 |
| 周日 03:00 | `iNEST_Weekly_Health` | 健康报告与问题清单 |

## 研发产出规则

1. 论文洞察必须落到明确的论文、专利、仿真或代码任务，否则只保留在收件箱。
2. 每个任务必须关联来源、输出文件、验证方式和验收标准。
3. 指标必须标明 `[实测]`、`[仿真]`、`[引用]`、`[推导]` 或 `[待测]`。
4. 看板不维护独立静态任务；只展示知识库当前状态。


<!-- orphan-cleanup: no MOC found, tagged -->
