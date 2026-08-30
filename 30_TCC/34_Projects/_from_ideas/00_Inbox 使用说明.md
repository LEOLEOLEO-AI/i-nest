---
title: 00_Inbox 使用说明
tags:
- paper
- patent
- project
- project-management
provenance: own
---
生成时间：2026-05-02 22:41:46 · 更新：2026-08-31（统一收件箱 v2）

## 统一收件箱（所有外部输入先入 Inbox）

| 来源 | 收件位置 | 入口链路 |
|---|---|---|
| 得到大脑 GetNotes | `01_GetNotes/` | `pull_getnotes.py` → `getnotes_importer.py`（每日 21:00 自动） |
| 网页剪藏（微信/Clipper） | `02_网页剪藏/` | Obsidian 插件 `wechat-inbox-sync`（微信收件箱）等剪藏工具 |
| Genspark（arXiv 日报等） | `03_Genspark/` | `gitee_sync.ps1` 每日 21:00 从 `genspark/sync` 分支自动提取 |

## 二级入口

- `01_GetNotes`：得到大脑（GetNotes）导入的笔记（原 GetNotes_Inbox 导入产物）
- `02_网页剪藏`：网页/阅读过程中的轻量剪藏（微信剪藏、Clipper、浏览器剪藏）
- `03_Genspark`：Genspark 云端 arXiv 日报（每篇对应一个 arXiv ID 的 `.md` + 每日 `-index.md`）
- `01_PDF_Source`：PDF 文献源文件
- `13_Codex`：Codex 联动产物
- `_imports`：其他脚本/外部批量导入材料
- `_pipeline_insights`：pipeline 自动采集的前沿洞察

## 原则

- Inbox 只做暂存，不做终态归档
- 真正稳定的概念转入 `10_Knowledge`
- 真正推进中的事项转入 `20_Projects`
- 形成论文或专利后转入 `30_Outputs`
- 所有子目录均被 `process_inbox.py`（`rglob("*.md")`）与 21:00 白名单同步自动纳入整理流程

---
## 相关笔记 (AI 自动关联)
- [[最简知识库目录说明]]
