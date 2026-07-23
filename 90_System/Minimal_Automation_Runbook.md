# TCC + iNEST 最小自动化运行规范

> 生效日期：2026-07-19。目标是以最少的常驻进程和定时任务，维持知识库访问、研究管线、实时发布、演化与同步。

## 登录后只做两件事

`TCC_iNEST_Linkage` 是唯一保留的登录任务：启动 Obsidian 和本地预览守护。

- 预览地址：[主页](http://127.0.0.1:8899/home/work/.openclaw/workspace/Home.md)
- 预览地址：[研发看板](http://127.0.0.1:8899/home/work/.openclaw/workspace/70_Dashboard/index.html)
- 守护范围：只保证 `8899` 预览服务可用。
- 明确不在登录时执行：爬取、LLM 分类、Git 同步、DDNS、模型池刷新、微信桥接。

## 保留的定时任务

| 任务 | 时间 | 唯一职责 | 是否调用模型 |
|---|---|---|---|
| `iNEST_Daily_Pipeline` | 每日 08:00 | 文献获取、证据分析、状态与看板发布 | 按管线策略 |
| `iNEST_Daily_Sync` | 每日 21:00 | 得到大脑、Genspark 分支和 GitHub/Gitee 单写者同步 | 否 |
| `iNEST_Knowledge_Evolution` | 每周六 22:30 | 证据账本、假设注册、状态和看板刷新 | 否 |
| `iNEST_Weekly_Health` | 每周日 03:00 | 服务、管线数据鲜度和链接健康检查 | 否 |

## 管线时限

`iNEST_Daily_Pipeline` 通过 `pipeline_guard.py` 运行。实际运行上限为 20 分钟，任务计划程序另设 25 分钟兜底。

- 超时后守卫会终止整个子进程树，并暂停后续自动运行。
- 状态与日志链接写入 [管线状态](http://127.0.0.1:8899/home/work/.openclaw/workspace/60_MOC/07_Pipeline_Status.md)。
- 审阅后，在 Codex 对话中输入“继续科研管线”即可用新的受控窗口恢复；不会续接已终止的旧进程。

## 已禁用的重复任务

- 登录启动文件夹中的 `iNEST_Daily.lnk`：曾在每次登录时完整运行主管线，与 08:00 任务重复。
- `iNEST_Inbox_Afternoon` 和 `vault_watcher.py`：旧收件箱脚本会自动调用带硬编码凭据的 DeepSeek，已禁止常驻触发；后续仅可在统一、安全的收件箱处理器完成改造后再启用。
- `iNEST_Daily_Kanban_Update`：管线完成后由 `research_publisher.py` 发布，独立运行是重复写入。
- `iNEST_FreeModelPool_Refresh`、`iNEST_DDNS_Update`：不属于研究闭环。
- `cc-connect`、`JOJO_Fixer_AutoStart`：移动端/模型桥接为按需功能，不能占用登录资源。
- 所有旧 Preview Server/Watchdog 任务：由 `TCC_iNEST_Linkage` 的单一守护取代。

## 新增自动任务的准入条件

必须在启用前明确记录：触发时间、数据来源、唯一写入对象、是否调用模型、失败处理和与现有任务的重复关系。禁止新增直接写入 `Home.md`、看板、研究状态或 `main` 分支的旁路任务。

## 手动维护

```powershell
# 不调用模型，只刷新状态、证据与看板
powershell -NoProfile -ExecutionPolicy Bypass -File D:\Obsidian\scripts\research_evolution_refresh.ps1

# 检查预览服务
Test-NetConnection 127.0.0.1 -Port 8899
```
