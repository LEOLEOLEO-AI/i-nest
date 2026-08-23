# 系统全面诊断报告 2026-08-23

> 诊断范围: 科研智能体管线 (pipeline v3.3) + 定时任务 + Git 同步 + wiki 知识库
> 诊断方式: 只读检查, 未修改任何文件

## 总体结论

GitHub 主同步链路可用, 但 **研究摄入已失效两天**、**21:00 每日同步从未真正发布**、**Gitee 备份链路自 7/23 起被弃用**、**Git 白名单与命名规范大面积失守**。整体健康度: **C+ (能跑, 但三条关键保障线全部带伤)**。

## P0 — 关键功能失效

### 1. 文献摄入连续空转 (最影响科研产出)
- 8/21、8/23 两次运行 `new_papers=0, api_results=0, classified=0`
- 日志显示 Semantic Scholar 首查即 429, arXiv 21 组查询几乎全部 429/读超时 (经代理), 无一组成功
- 8/20 尚有 7 篇入库, 说明并非关键词问题, 是出口 IP 被 arXiv/S2 限流
- 建议: 更换/轮换代理出口, 或降低查询频率并错峰至半价时段之外; S2 加 API key

### 2. iNEST_Daily_Sync 从不发布 (audit-only 缺陷)
- 任务动作为 `gitee_sync.ps1` 且未传 `-Publish`, 脚本第 126 行直接走 audit 分支 exit 0
- 结果: 每晚只审计不提交不推送, 当前积压 18 项未提交变更
- 任务 LastTaskResult=1 (疑似 pull_getnotes/importer 抛错)
- 同步白名单 `$AllowedRoots` 写的是 `10_Inbox/`, 实际目录是 `00_Inbox/`; 且缺 `20_Processing/ 80_Archive/ 99_Meta/ wiki/` → 即使加 -Publish 也几乎什么都不同步

### 3. Gitee 备份链路已被静默弃用
- gitee_sync.ps1 第 142-151 行: 只推 GitHub, 状态写死 `gitee = "disabled"`
- 实测 `gitee/main` 落后本地 main **6 commits**; dry-run 推送 Gitee 可成功, **不是配额问题**, 是没人推
- 违反 AGENTS.md "每日 21:00 先 GitHub 后 Gitee" 的规则

## P1 — 规范失守 (数据真实性/白名单铁律)

### 4. Git 白名单大面积失守
AGENTS.md 白名单仅 .md/.py/.yaml(<5MB), 但当前跟踪文件含:
json×290, png×176, jpg×118, woff2×89, log×82, nml×43, txt×24, jsx×20, html×13, ps1×12, js×11, bat×10, ts×8, docx×8 等, 合计约 900 个非白名单文件 — 均为 2026-08-11 瘦身后重新引入。
典型: [70_Dashboard/data.js](http://127.0.0.1:8899/70_Dashboard/data.js)、99_Meta/*.json(运行时状态不该进库)、30_TCC 下大量 png/docx。

### 5. 两级命名规范失守
`{序号}_{英文}` 规则下实测 **2879 个中文文件名** 分布在 00_Inbox/20_Processing/30_TCC/40_iNEST/50_Output。

### 6. 知识图谱质量退化
- wiki/health.md: 概念 5140, 文章 1006, **孤儿概念 3004 (58%)**
- Research Gaps 一节为空 (gap 发现环节没产出)
- 图节点 10368→10515→12228 (+1860) 发生在连续 0 新论文期间 — self-evolve 在无新证据情况下自我膨胀概念, 有"概念通胀"风险

## P2 — 卫生与可观测性

| # | 问题 | 位置 |
|---|------|------|
| 7 | 根目录 `.git` 是**空目录**, 导致 D:\Obsidian 下任何 git 命令报 not a repository; 真仓库在 vault/ | D:\Obsidian\.git |
| 8 | AGENTS.md 与实际结构漂移: 规则写 `10_Inbox`, 实际 `00_Inbox`; AGENTS.md 本身在 vault 仓库外不受版本控制 | D:\Obsidian\AGENTS.md |
| 9 | pipeline_guard 子进程读取线程 UnicodeDecodeError (GBK 输出按 UTF-8 解码); task_recommender.py 固定 30s 超时被打断 | logs/pipeline_guard_*.log |
| 10 | check_sync_health.ps1 的"最后同步"读过期 sync_state.json (显示 953h 前, 实际 GitHub 今天已推), 且完全不检查 Gitee | scripts/check_sync_health.ps1 |
| 11 | 本地残留 master 分支 (远端已于 8/11 清理) | vault 本地分支 |
| 12 | 8/22 管线缺日志 (当日未跑); iNEST_Daily_Pipeline LastTaskResult=267014 (任务曾被终止) | 计划任务 |
| 13 | DS_API_KEY 在本会话环境缺失 (管线近两日未走到 LLM 分类路径, 无法证实密钥可用性) | 环境变量 |

## 正常项 (无需处理)

- ✅ GitHub main 与 genspark/sync 双双一致 (self_evolve 09:53 已推 f8e956f5b)
- ✅ 仓库 pack 体积 146.29 MiB, 远低于 Gitee 1GB 配额
- ✅ .gitignore 一行一模式合规
- ✅ GetNotes 拉取正常 (最近 8/22 21:00)
- ✅ wiki 编译器/Homepage/Dashboard 生成环节正常运行 (~50min 全流程跑完)
- ✅ 周度知识进化/元进化/健康检查任务均 Ready 且近期成功

## 各区规模快照

| 目录 | 文件数 | .md | 体积 |
|---|---|---|---|
| 00_Inbox | 182 | 179 | 2.3MB |
| 20_Processing | 727 | 650 | 19.4MB |
| 30_TCC | 2259 | 1894 | 145.9MB |
| 40_iNEST | 3284 | 1415 | 193.9MB |
| 50_Output | 1035 | 458 | 81.8MB |
| wiki | 6153 | 6153 | 10.1MB |
| 80_Archive | 1410 | 1308 | 10.9MB |

## 建议修复顺序

1. **修摄入**: 处理 arXiv/S2 限流 (换出口/降频/S2 key) — 否则管线是空转
2. **修 21:00 同步**: 任务加 `-Publish`, 修正 `$AllowedRoots` (`00_Inbox` + 补 4 个根), 恢复 Gitee push
3. **清库合规**: 决定 json/png/js/docx 等是补进白名单还是移出 Git; 批量重命名中文文件名
4. **图谱瘦身**: 孤儿概念回收 (orphan_cleanup.py 已有), 给 self-evolve 增加"无新论文则不新增概念"闸门
5. **卫生项**: 删空 .git、删 master、health check 补 Gitee 检查、guard 日志编码修复
