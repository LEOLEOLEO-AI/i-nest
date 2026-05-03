# MEMORY

## Workspace Defaults

- 当前主工作区是一个以 Obsidian 为核心的科研知识库，重点围绕 SSOT、ADR、Inbox、Wiki、知识图谱和自动化脚本形成自生长体系。
- 默认的全局问题处理方式：先标准化问题，再诊断或执行，再尽量沉淀到可复用文件，而不是只停留在对话里。
- Copilot 的系统提示词入口使用 `copilot/system-prompts/知识库问题标准化系统提示词.md`，并由 `.obsidian/plugins/copilot/data.json` 的 `defaultSystemPromptTitle` 指向。

## Known Gaps

- 工作区曾缺失 `MEMORY.md` 与每日 `memory/YYYY-MM-DD.md`，导致会话连续性弱。
- 模板目录的规范命名应统一使用 `99-Templates`；后续新增提示词、脚本或文档引用时不要写成 `99-templates`。

## User Preference Signals

- 用户偏好中文、直接、结构化、可落地的结果。
- 用户希望把零散问题自动整理成标准化任务，并持续沉淀为知识库资产。
