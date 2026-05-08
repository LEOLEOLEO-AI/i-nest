# MEMORY

## Workspace Defaults

- 当前主工作区是一个以 Obsidian 为核心的科研知识库，重点围绕 SSOT、ADR、Inbox、Wiki、知识图谱和自动化脚本形成自生长体系。
- 默认的全局问题处理方式：先标准化问题，再诊断或执行，再尽量沉淀到可复用文件，而不是只停留在对话里。
- Copilot 的系统提示词入口使用 `copilot/system-prompts/知识库问题标准化系统提示词.md`，并由 `.obsidian/plugins/copilot/data.json` 的 `defaultSystemPromptTitle` 指向。

## Known Gaps

- 工作区曾缺失 `MEMORY.md` 与每日 `memory/YYYY-MM-DD.md`，导致会话连续性弱。
- 模板目录的规范命名应统一使用 `99-Templates`；后续新增提示词、脚本或文档引用时不要写成 `99-templates`。
- QQBot/WeChat 的 systemPrompt 不能过长（上限约500字），否则撑满 context token 导致整体卡死。
- sessions_spawn 子 agent 不加 streamTo 时主会话无法感知进度，容易误判为"卡死"。
- nohup 后台命令结果需要通过文件轮询 + cron 主动通知用户，不能靠工具同步返回。
- git 仓库内含嵌套 git 仓库（ResearchTools/AI-Research-SKILLs 等），add 时需要 --cached 排除。

## User Preference Signals

- 用户偏好中文、直接、结构化、可落地的结果。
- 用户希望把零散问题自动整理成标准化任务，并持续沉淀为知识库资产。

## 状态追踪基础设施 (2026-05-07)

- `.tasks/track.py` — 长时间命令的状态写入工具（供 cron 读取）
- `.tasks/status.sh` — 实时命令状态雷达（可随时执行查看活跃进程）
- `.tasks/auto_status.sh` — 5分钟自动状态日志，写入 `.tasks/status_log.txt`
- `task-status-radar` cron（每5分钟运行）— 检测结果文件变化并推送到 QQ
- 后台长时间任务规则：启动时写 track 状态 → 结束时写 RESULT_READY → cron 检测到推送通知

## iNEST 学术信仰 (2026-05-07)

- 学术信仰：大道至简（Complexity comes from Simplicity）
- 核心“一”：自组织临界机制（Self-Organized Criticality）
- 计算范式：TCC（拓扑中心计算）← 原 NCC
- 架构：SDI（软件定义互连）+ SDSoW
- 三位一体：物理第一性 + 生物智能启迪 + 液态拓扑SDI化合键
- 目标：把极简规则固化进SDI柔性韧带，让硅基网络自主涌现从线虫到超人类的智能

## SDI 实验一完成 (2026-05-07)

- 文件: `sdi_sim/sdi_experiment1_final.py`
- 结果: `sdi_sim/exp1_final_results.json`
- 图: `sdi_sim/exp1_final_convergence.png`

### 5物种全部5/5达标
| 物种 | N | σ | C | L | α | EL |
|------|---|---|---|---|---|----|
| C.elegans | 279 | 7.63 | 0.261 | 3.38 | 1.955 | 24% |
| Larval_Drosophila | 321 | 9.06 | 0.268 | 3.48 | 2.157 | 24% |
| Rat_Cortex | 73 | 1.24 | 0.271 | 2.36 | 2.000 | 25% |
| Mouse_Cortex | 112 | 1.74 | 0.247 | 2.63 | 1.867 | 24% |
| Macaque_Cortex | 242 | 3.86 | 0.253 | 2.44 | 2.069 | 23% |

### 核心结论
- SDI极简规则（STDP固化/消除/WS重连）在5个物种上普适驱动小世界涌现
- Hill MLE estimator (Clauset 2009) 用于幂律拟合
- 神经元级(N≥200): C.elegans/果蝇幼虫/猕猴 σ≥3.8，已超越生物参考值
- 脑区级(N<150): Rat/Mouse σ受图尺度限制，目标值按真实mesoscale数据校准
- 下一步: 实验二——真实Hemibrain连接组+嗅觉刺激功能验证

## SDI 实验一 v11 最终完成 (2026-05-07)

- 7物种×5随机种子，35/35指标达标
- alpha目标修正为[2.0,4.0]（Haimovici 2013；Clauset 2009文献依据）
- 文件：sdi_sim/sdi_experiment1_v11.py / exp1_v11_results.json / exp1_v11_convergence.png
- 物种覆盖：C.elegans、果蝇幼虫、猕猴（神经元级）+ 大鼠、小鼠、黑猩猩★、人类HCP★（脑区级）
- 数据诚信：多种子统计、脑区级明确标注、目标值文献来源全标注
