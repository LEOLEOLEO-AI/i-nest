---
title: "教训库（失败案例与规则修订记忆）"
created: 2026-08-22
provenance: meta_evolution
---

# 教训库

> 用途：记录"规则层进化"的历史教训——每次失败/误配/断更的根因与修复。
> 维护者：科研智能体（提案）+ 刘勤让教授（审批入库）。
> 这是 AGENTS.md 规则修订的可追溯记忆，防止同类问题重复发生。

## 教训条目模板

```markdown
### L-编号 YYYY-MM-DD：一句话标题
- **现象**：发生了什么
- **根因**：为什么发生
- **修复**：改了什么（AGENTS.md 条款/技能/脚本）
- **验证**：如何确认修复有效
- **提案来源**：evolution_proposals/日期.md
```

## 已入库教训

### L-001 2026-08-11：TCC 检索词被误配为可信计算方向
- **现象**：Katz Centrality 安全论文误入 TCC 文献库
- **根因**：检索词 "TCC" 被理解为 Trusted Computing Cloud；interconnect 词边界匹配缺失
- **修复**：AGENTS.md §6.1 明确定义 TCC=拓扑中心计算 + §6.3 词边界匹配规则；pipeline_v3.py 实现排除词过滤
- **验证**：2026-08-11 后 pipeline 检索无安全方向误检
- **提案来源**：人工修订（Codex 记录）

### L-002 2026-06-23：旧平台每日管线静默失败 23 天
- **现象**：iNEST-Daily-Research-Pipeline 08:00 连续失败无告警
- **根因**：daily_pipeline.py GBK 编码 © 无 encoding 声明 + 路径指向已删除的 D:\Agent + 无健康监控
- **修复**：2026-08-21 考古审计定位；现行管线（pipeline_guard.py 06:30）替换；register_scheduled_task.ps1 废弃存档
- **验证**：现行定时任务全部 Ready，计费低谷期运行
- **提案来源**：2026-08-21 审计报告

### L-003 2026-08-21：SDI 仿真结果文件与运行日志数值不符
- **现象**：exp1 v16/v17 results.json 的 σ/SCORE/elapsed 与 run.log 不一致（elapsed 差 30 倍）
- **根因**：结果文件可能被改写或与运行版本不对应；合成网络冒充真实连接组
- **修复**：43 个不可信结果隔离至 data_local/_unverified；论文引用需"三证据"（run.log+seed+代码版本）
- **验证**：审计报告 00_数据真实性审计报告_20260821.md；VERSION_LOCK + SHA256 校验方案已写入
- **提案来源**：2026-08-21 数据真实性审计

### L-004 2026-08-21：去重指纹失效导致 79% 冗余
- **现象**：Agent/01-Theory-Research 76MB 中 60MB 是重复副本（同一 PDF 9 份）
- **根因**：入库脚本指纹去重失效，同一文件 4 轮导入生成不同指纹
- **修复**：SA-A 全库扫描（40,523 重名文件）；tmp_gh 归档；55_Guides 15 变体去重；建议 _dup_scan_v2.py 升级为 MD5 二次校验常驻脚本
- **验证**：版本治理台账 00_版本治理台账_20260821.md
- **提案来源**：2026-08-21 重组审计

### L-005 2026-08-22：GitHub 分叉 307/167 持续多日
- **现象**：本地 main 与 github/main 长期分叉，21:00 自动同步 push 被拒
- **根因**：7 月历史线未合并 + genspark/sync 远端更新未拉取
- **修复**：merge -s ours 合并历史线（内容以本地为准）+ 合并 genspark arXiv 日报 73 篇 + force-with-lease 推送
- **验证**：2026-08-22 全部远端 0/0 分叉清零
- **提案来源**：2026-08-22 同步执行

## 待确认教训（由元进化提案提升）

（此处由 meta_evolution.py 生成的提案审批通过后填充）


<!-- orphan-cleanup: no MOC found, tagged -->
