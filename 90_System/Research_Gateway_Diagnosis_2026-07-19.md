---
provenance: external
---

# 研究网关与自动化诊断 — 2026-07-19

## 结论

当前系统已经有统一状态总线和单一看板发布器，但还没有完全统一的研究入口。现状属于“主路径可运行，剪藏处理和消息入口存在旁路”，不能宣称所有管线已经不会空转或反复失败。

## 已确认问题

1. `[实测]` `logs/pipeline_20260719_1207.json` 记录 `new_papers=12`、`api_results=12`、`classified=0`。
2. `[代码审计]` `pipeline_v3.py` 原先以 `process_inbox(limit=0)` 调用分类阶段，循环在第一条输入前即退出。
3. `[代码审计]` 分类成功路径原先返回 `0`，导致日志即使移动了文件也会报告零分类。
4. `[代码审计]` `process_inbox.py` 仍保留直连 DeepSeek 和硬编码密钥的旧旁路，且对应计划任务按运行手册被禁用；不应重新启用。
5. `[实测]` 当前唯一发布路径是 `research_publisher.py`，主页、看板和 `research_state.json` 可以共享状态，但正式计划没有人工审批闸门。

## 已实施

- 修复 `pipeline_v3.py` 的分类上限和成功计数。
- 每次管线运行后生成 `99_Meta/research_task_proposals.json` 和 `60_MOC/05_Task_Review.md`。
- 候选任务默认是 `pending_review`，不会自动写入 `06_Task_Plan.md`。
- 只有将候选项改为 `approved` 并运行 `approve_research_tasks.py`，才会晋升为正式任务。
- `research_state.json` 增加 `task_review` 状态统计。

## 网关判断

- `[实测]` 研究脚本主路径通过 `D:\Obsidian\scripts\llm_router.py` 访问本地模型路由 `127.0.0.1:57321`。
- `[实测]` 旧 Inbox 分类器仍有独立直连路径，属于未统一旁路；目前保持禁用。
- `[实测]` `cc-connect` 本机版本为 `1.4.1`，其公开说明定位为 WeChat Work 等企业消息平台桥接，不等同于个人微信。
- `[实测]` `codex-wechat` 插件通过 Windows 微信桌面窗口、键盘和剪贴板工作，并使用 `--dangerously-bypass-approvals-and-sandbox` 启动 Codex；它适合人工辅助，不适合作为无人值守的稳定生产网关。

## 今日推荐闭环

`剪藏/论文 -> 00_Inbox -> 研究分析 -> 候选任务 -> 人工确认 -> 06_Task_Plan -> 执行证据 -> 状态/看板`

验收任务：

- `V-GW-01`: 一条剪藏在 `00_Inbox` 可被识别、生成来源和候选任务；验收为源文件、候选项、正式任务三者可互相追溯。
- `V-GW-02`: 分类失败进入 `20_Processing/21_Pending`，不得静默丢失；验收为失败计数和原文件均可见。
- `V-GW-03`: 看板只读取 `research_state.json` 和 `data.js`；验收为不存在第二个写看板入口。
- `V-GW-04`: 消息入口只保留一个生产网关；在个人微信和企业微信之间作出选择前，不同时启用多个桥接器。


<!-- orphan-cleanup: no MOC found, tagged -->
