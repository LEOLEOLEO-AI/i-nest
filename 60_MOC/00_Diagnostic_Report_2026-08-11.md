---
title: 知识库系统诊断报告 2026-08-11
date: 2026-08-11
status: review
---

# Obsidian 知识库系统诊断报告（2026-08-11）

> 诊断目标：为什么知识库“没有自我进化、总结输出不达预期”，如何用 GitHub 开源工具修复，如何改 AGENTS.md 以省 token。

## 一、结论摘要

知识库不是“没在跑”，而是**跑偏了**：输入正常、自进化脚本正常，但**加工-输出闭环断裂、管线被暂停卡死、wiki 自动生成的内容与研究推进脱节**。

三个最致命的问题：

1. **管线暂停后无人恢复**：08-09 12:04 起 `pipeline_guard` 将管线置为 `paused`，之后 08:00 每日任务一进来就退出。Home 看板显示“管线 paused”与此一致。
2. **加工积压、输出过期**：`20_Processing/` 积压 567 篇（最后处理 08-04），`00_Inbox/` 217 篇；`60_MOC/02_Research_Insights.md` 停在 07-26（0 篇），`02_DeepSeek_Insights.md` 停在 07-15。
3. **自进化产出是“概念卡片”，不是“研究推进”**：`wiki/` 已有 4199 个自动生成文件（3204 概念），每天仍在生成新概念页和 backlinks，但与论文、专利、仿真、IP 的主线任务没有形成闭环。

## 二、现状关键数字

| 指标 | 数值 | 评价 |
|---|---|---|
| Markdown 总数 | 10,086 | 偏大，检索/索引负担重 |
| wiki/ 自动生成 | 4,199 | 最大目录，超过 30_TCC(1,871)+40_iNEST(1,427) |
| 20_Processing 积压 | 567 | 自 08-04 起未处理 |
| 00_Inbox 待处理 | 217 | 含 08-10 新增 getnote |
| 80_Archive | 1,186 | 去重归档较多 |
| 定时任务 | 12+ 个 | 存在重复入口和已禁用任务 |
| Git | 22+ 未提交；GitHub ahead 1 commit | 自动提交/同步有中断 |
| 最大文件 | wiki/backlinks.md 2.35MB | 每天重写，token/索引黑洞 |

## 三、问题清单（按优先级）

### P0-1 管线被“暂停”卡死（根因）
- `state/pipeline_guard_status.json`：`status=paused, requires_confirmation=false`，两者矛盾；timeout 后守卫永远停在 paused，“继续科研管线”指令也无法恢复。
- 08:00 有两个重复入口：`iNEST_Daily_Pipeline`（Python310 跑 `pipeline_guard.py`）和 `ObsidianVaultPipeline`（workbuddy Python 3.13.12 直接跑 `pipeline_v3.py`），可能互踩状态。
- `iNEST_S_Tier_Daily` 被禁用；`iNEST_Preview_Server/Watchdog` 被禁用（有 `linkage_daemon.py` 替代，尚可）。

### P0-2 加工→输出闭环断裂
- `20_Processing` 567 篇积压一周；`process_inbox.py --limit 20` 任务在跑但产出没进洞察。
- 洞察文件过期：`02_Research_Insights`（07-26，0 篇）、`02_DeepSeek_Insights`（07-15）。
- Home“今日行动”仍指向 8 月初旧任务，没有随管线刷新。

### P1-1 结构混乱
- 根目录 15 个探针脚本（`.probe_*.py`、`.check_*.py`、`.get_*.py`）和 6 个误生成文件（`31_Theory.md`、`32_Tech.md`、`34_Projects.md`、`41_Theory.md` 为 0 字节；`20_Processing.md`、`50_Output.md` 为说明文件）。
- 多套“规则大脑”：`D:\Obsidian\AGENTS.md` + vault 下 `RULES.md`、`MEMORY.md`、`SOUL.md`、`USER.md`、`schema.md`，内容重叠且部分过时（RULES.md 仍写“exec 工具损坏待修”）。
- `wiki/backlinks.md` 2.35MB、`wiki/index.md` 118KB、`00_Dedup_Log.md` 344KB、`conflict-files-obsidian-git.md` 208KB 均为 token/索引黑洞。

### P1-2 插件与索引负担
- 17 个社区插件，Smart Connections + Omnisearch 对 10,086 文件全量建索引，是启动卡顿和“建立索引不结束”的主因。
- 之前遇到“卡死在某 MD 建立索引”多与 Smart Connections/Omnisearch 扫描大文件有关。

### P2-1 Git/同步小病
- obsidian-git 自动提交 4 小时一次（`autoSaveInterval=14400`），但当前 22+ 未提交变更，说明自动提交被占用或中断。
- `sync_log.txt`：`GitHub main is ahead by 1 commit`，需要一次手动 merge。
- `.gitignore` 排除 `*.js/*.html`，导致 `70_Dashboard/index.html`、`data.js` 不进 Git，Genspark/其他机器拉下来看板为空。

## 四、开源工具方案（按问题匹配）

### 4.1 恢复管线与调度（P0）
| 工具 | GitHub | 作用 | 安装后状态 |
|---|---|---|---|
| 修复 pipeline_guard.py（自研小改） | 无 | 修 `requires_confirmation=false` 状态机 bug；增加“超时后自动降级为下次重试 1 次再暂停” | 08:00 管线能连续运行 |
| 去重入口 | 无 | 08:00 只保留 `iNEST_Daily_Pipeline`，禁用 `ObsidianVaultPipeline` | 不再双跑互踩 |
| QuickAdd | chhoumann/quickadd | Obsidian 内一键宏：处理 Inbox、跑脚本、刷新看板 | 点按钮即触发管线，不再依赖纯命令行 |

### 4.2 总结/洞察输出（核心需求）
| 工具 | GitHub | 作用 | 安装后状态 |
|---|---|---|---|
| Obsidian Text Generator | nhaouari/obsidian-textgenerator | 在 Obsidian 内用 DeepSeek API 对选中笔记批量总结、打标、生成洞察 | 每日 Inbox/Processing 内容可一键生成结构化洞察 |
| Obsidian Auto Linker | farling42/obsidian-auto-linker | 文本自动匹配并生成 `[[]]` 链接，零 LLM 成本 | wiki 概念与正文互链率提升，补足“双向链接” |
| Obsidian Linter | platers/obsidian-linter | 自动统一 frontmatter、标点、空行、标签 | 新入库内容元数据一致，减少去重噪声 |

### 4.3 去重与整理（P1）
| 工具 | GitHub | 作用 | 安装后状态 |
|---|---|---|---|
| dupeGuru | arsemetar/dupeguru | 内容哈希跨目录查重，中文支持好 | 复核 80_Archive 与 20_Processing 重复 |
| rmlint | sahib/rmlint | 高速重复/空文件检测（Windows exe） | 秒级扫出 0 字节与完全重复文件 |
| Obsidian Linter | 同上 | 格式化 | 见上 |

### 4.4 索引与 token 控制（P1）
| 工具 | 配置动作 | 安装后状态 |
|---|---|---|
| Smart Connections（已有） | 只索引 `30_TCC/40_iNEST/50_Output/60_MOC`，排除 `wiki/80_Archive/20_Processing/90_System/99_Attachments` | 索引体积下降约 60%，启动不再卡 |
| Omnisearch（已有） | 排除 `wiki/`、`80_Archive/`、`90_System/99_Attachments/` | 搜索快，结果噪声少 |
| 手动/脚本 | `wiki/backlinks.md`、`wiki/index.md` 移出索引或改为按需生成 | 消除 2.35MB token 黑洞 |

### 4.5 工具/能力冷库（可选，承接上轮讨论）
| 工具 | GitHub | 作用 | 安装后状态 |
|---|---|---|---|
| Table-GitHub-Capability-Router | duoduoler-ops/Table-GitHub-Capability-Router | GitHub 项目/能力入库、去重、路由表 | 已评估的科研智能体/Skill/插件有单一登记处 |

## 五、安装后预期状态（两小时工程）

1. 08:00 管线每日正常跑完并写状态：`completed`，不再停在 `paused`。
2. 20:00 处理 Inbox/Processing 前 20 篇 → 产出当日 `60_MOC/02_Research_Insights_YYYY-MM-DD.md`，Home 今日行动随之刷新。
3. 洞察文件按日期命名、可追溯，不再“0 篇空壳”。
4. 启动时间明显缩短：Smart Connections/Omnisearch 只索引核心目录。
5. 0 字节文件和探针脚本清理，规则文件收敛为单一 AGENTS.md。
6. 看板数据（`70_Dashboard/data.js`）纳入 Git，Genspark 侧也能看到。

## 六、AGENTS.md 修改指导意见（节省 token 关键）

### 6.1 原则
1. **单一规则文件**：只保留 `D:\Obsidian\AGENTS.md` 为 Codex 自动加载规则；`RULES.md/SOUL.md/USER.md` 合并进 AGENTS.md 或降级为参考文档，`MEMORY.md` 只保留 30 条以内短记忆。
2. **大文件门禁**：AGENTS.md 内明确“禁止读取”清单，防止 agent 一次吸入 2.35MB。
3. **检索代替全量扫描**：要求 agent 用 Omnisearch/目录限定 rg，禁止无界 `rg` 全库。
4. **修复状态机命令**：把“继续科研管线”写成真实解除 pause 的命令（修 guard bug），而不是口头指令。
5. **每日四数闭环**：每天必须在看板写 `输入数 / 处理数 / 输出数 / 拒绝数`，缺一视为管线失败。

### 6.2 推荐结构草稿（替换 v4.5）
```markdown
# Codex SuperAgent — TCC + iNEST 研发中枢（v5.0）
## 0 数据真实性铁律（保留，勿删）
- [实测]/[仿真]/[引用]/[推导]/[待测] 五类标注；禁止无来源数字。

## 1 身份
- TCC + iNEST 研发中枢智能体；优先推进科研产出。

## 2 单写者架构（保留）
- Codex 唯一 main 推送者；Genspark 走 genspark/sync 分支；
- obsidian-git 4h 自动提交保留；冲突先停，人工裁决。

## 3 管线（v3.5 → v4.0）
| 时间 | 任务 | 产出 |
|---|---|---|
| 08:00 | pipeline_v3（唯一入口，guard 保护） | 新文献 → Inbox，写 pipeline_guard_status |
| 20:00 | process_inbox --limit 20 | 20_Processing 消化 → 30/40 分类 |
| 20:30 | gen_insights | 60_MOC/02_Research_Insights_当日.md |
| 21:00 | gitee 同步（得到大脑+Genspark 合并+push） | sync_log |
| 周日 03:00 | 周度重组+去重+weekly_health | 健康报告 |
- 状态机：running/completed/failed/timeout(自动重试1次后暂停)/paused(仅用户确认解除)
- “继续科研管线”= 运行 `90_System/scripts/pipeline_guard.py --resume`

## 4 Token 铁律（新增，最高优先级）
- 禁止读取：wiki/backlinks.md、wiki/index.md 全文、>200KB 的 .md、*.json>100KB
- 检索：先 Omnisearch 或限定目录；禁止无界 rg 全库
- 引用笔记：只摘取 frontmatter + 标题 + 关键段落，禁止整篇复制
- 处理 20_Processing 每批 ≤20 篇，单篇输出 ≤500 字总结

## 5 目录与命名（保留三定律）
- 10_Inbox→20_Processing→30_TCC/40_iNEST→50_Output→80_Archive
- {序号}_{英文}；Git 白名单：.md/.py/.yaml

## 6 每日四数
- 输入数/处理数/输出数/拒绝数 必须写入 70_Dashboard/data.js，缺一视为失败。

## 7 快速命令
- 继续科研管线 / 同步gitee / 健康检查(check_sync_health.ps1) / 周度重组
```

### 6.3 具体减 token 动作清单
1. 删除 AGENTS.md 中重复的“零、数据真实性质保铁律”标题（当前重复两遍）。
2. 把 `wiki/index.md`（118KB）的引用改为“按需用 Omnisearch 查概念”，不整篇读。
3. 把 `wiki/backlinks.md`（2.35MB）移出索引并禁止 agent 读取全文。
4. `00_Dedup_Log.md`（344KB）改存 `80_Archive/` 或压缩为摘要，禁止常驻 60_MOC。
5. 探针脚本（`.probe_*.py` 等 15 个）移入 `90_System/99_Attachments/` 或删除，减少扫描噪声。
6. Smart Connections/Omnisearch 排除目录配置一次到位。
7. 规则文件收敛：RULES.md 里过时内容（“exec 工具损坏待修”）删除或更新。

## 七、建议执行顺序

| 阶段 | 内容 | 预计 |
|---|---|---|
| P0 | 修 guard 状态机 + 清暂停 + 去重 08:00 入口 + 手动 git merge | 30 分钟 |
| P0 | 恢复 20:00 process_inbox + 当日洞察生成 | 30 分钟 |
| P1 | 清理 0 字节/探针/误生成文件 + 规则文件收敛 + AGENTS.md v5 | 40 分钟 |
| P1 | 配置 Smart Connections/Omnisearch 排除目录 | 10 分钟 |
| P1 | 安装 Linter/Auto-Linker/Text Generator 并配置 DeepSeek | 30 分钟 |
| P2 | 20_Processing 567 篇分批消化（每日 20 篇） | 2-4 周持续 |
| P2 | dupeGuru/rmlint 复核去重 | 30 分钟 |
| P2 | 看板 data.js 纳入 Git | 10 分钟 |

## 八、判定标准（两周后）

- 连续 14 天 `pipeline_guard_status=completed`（或明确 failed+日志），无人工干预。
- 每日都有非空 `02_Research_Insights_日期.md`，且关联具体论文/专利/仿真任务。
- 20_Processing 从 567 降到 200 以下。
- Obsidian 启动到工作区加载 ≤30 秒。
- AGENTS.md 单文件可被 Codex 完整理解，无重复指令。
