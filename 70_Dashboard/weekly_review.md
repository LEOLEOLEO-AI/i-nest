# 每周跟踪 · 截至 2026-09-25

> 统计窗口：2026-09-18 ~ 2026-09-25 · 由 `research_evolve.tracking` 生成

## 一、本周四个数

| 指标 | 本周 | 说明 |
|---|---|---|
| 入口新增论文 | **11** | 论文管线 new_papers 合计 |
| 自进化轮次 | **18** | 有记录的天数 |
| 候选开启 opened | 156 | 新进来的问题 |
| 候选关闭 closed | **62** | 给出裁决并出队 |
| 门禁新增违规 | 39 | 引用/证据标签 |
| 环节异常 | 5 | iNEST_Daily_Pipeline、iNEST_Daily_Sync、iNEST_Health_Watchdog、iNEST_Research_Evolve、iNEST_Inbox_Afternoon |

> ✅ 本周关闭了候选，构成真正的推进（进化 = 变异 + **选择** + 留存）。

## 二、五条工作流的推进

| 工作流 | 闭环定义 | 文件数 | 最近改动 |
|---|---|---|---|
| PAPER 论文与专利撰写 | 提交一次完整稿（含引用核验通过 + 数字全部带标签） | 683 | 09-19 22:32 |
| GUIDE 项目指南编写 | 产出一份可提交的指南/建议书，指标全部有验证方式 | 95 | 09-19 22:57 |
| READ 论文阅读与复现 | 一篇论文：笔记 + 可一键复现的脚本 + 与原报告指标的差异说明 | 138 | 09-19 22:40 |
| CODE 核心代码编写与验证 | 一个实验：单一规范脚本 + 可复现 manifest + 验收通过 | 2282 | 09-19 22:57 |
| SIM 复杂网络涌现智能仿真 | 一个仿真实验：登记 + 可复现 + 有基线对照 + 结论带 [仿真] 标签 | 2146 | 09-19 22:57 |

## 三、台账记录（ledger）

| 时间 | 环节 | 状态 | 指标 |
|---|---|---|---|
| 2026-09-20T08:14 | daily_review | ok | {"stages_bad": 9, "today_items": 119} |
| 2026-09-20T08:14 | weekly_review | ok | {"new_papers": 8, "opened": 149, "closed": 62, "bad_stages": 9} |
| 2026-09-20T08:14 | daily_review | ok | {"stages_bad": 2, "today_items": 119} |
| 2026-09-20T08:14 | weekly_review | ok | {"new_papers": 8, "opened": 149, "closed": 62, "bad_stages": 2} |
| 2026-09-20T08:16 | daily_review | ok | {"stages_bad": 2, "today_items": 119} |
| 2026-09-20T08:16 | weekly_review | ok | {"new_papers": 8, "opened": 150, "closed": 62, "bad_stages": 2} |
| 2026-09-21T06:00 | daily_review | ok | {"stages_bad": 2, "today_items": 126} |
| 2026-09-21T06:00 | weekly_review | ok | {"new_papers": 8, "opened": 151, "closed": 62, "bad_stages": 2} |
| 2026-09-22T04:30 | daily_review | ok | {"stages_bad": 3, "today_items": 124} |
| 2026-09-22T04:30 | weekly_review | ok | {"new_papers": 8, "opened": 152, "closed": 62, "bad_stages": 3} |
| 2026-09-23T04:30 | daily_review | ok | {"stages_bad": 2, "today_items": 126} |
| 2026-09-23T04:30 | weekly_review | ok | {"new_papers": 8, "opened": 153, "closed": 62, "bad_stages": 2} |
| 2026-09-24T06:44 | daily_review | ok | {"stages_bad": 3, "today_items": 124} |
| 2026-09-24T06:44 | weekly_review | ok | {"new_papers": 0, "opened": 154, "closed": 62, "bad_stages": 3} |
| 2026-09-25T08:47 | daily_review | ok | {"stages_bad": 5, "today_items": 130} |

## 四、下周优先级（按「卡点」排序）

1. 论文取数：arXiv API 已 406，确认多通道路径进入定时任务
2. 修复异常环节：iNEST_Daily_Pipeline、iNEST_Daily_Sync、iNEST_Health_Watchdog、iNEST_Research_Evolve、iNEST_Inbox_Afternoon
3. 推进已 accepted 的研究方向（见 research_evolve.md）

---

*每日跟踪见 `70_Dashboard/daily_review.md`。*
