---
title: Workspace Heartbeat
tags:
- project-management
---
- 检查 `copilot/system-prompts/知识库问题标准化系统提示词.md` 是否存在，且 `.obsidian/plugins/copilot/data.json` 的 `defaultSystemPromptTitle` 与之保持一致。
- 检查 `10_Knowledge/00_导航/Wiki` 是否需要重新生成，重点关注主干目录变更、失效链接、最近新增笔记是否进入 Wiki。
- 检查 `MEMORY.md` 与当日 `memory/YYYY-MM-DD.md` 是否存在；缺失时补建最小文件。
- 若发现 `99-Templates` 与 `99-templates` 混用，优先修复并重新生成 Wiki。
- 若没有新的异常、风险或重要事件，回复 `HEARTBEAT_OK`。

## Related Notes

- [[00_ADR_决策记录]]
- [[00_Inbox 使用说明]]
- [[ADR]]
