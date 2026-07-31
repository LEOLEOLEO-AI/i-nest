---
provenance: external
---

﻿# Obsidian 同步指令 v2.0

## 方式 A：Git 插件（推荐日常使用）

Obsidian Git 插件已配置双远程：

| 远程 | 地址 | 角色 |
|------|------|------|
| `github` | https://github.com/LEOLEOLEO-AI/i-nest.git | 主仓库 |
| `origin` | https://gitee.com/iBrainNest/i-nest.git | 备份镜像 |

### 手动同步步骤
1. `Ctrl+Shift+G` → 打开 Git 面板
2. 先 Pull（拉取远程更新）
3. Commit 本地变更
4. Push `github`（主仓库，优先）
5. Push `origin`（Gitee 备份）

## 方式 B：终端命令

```powershell
# 完整同步（含得到大脑拉取）
powershell -NoProfile -File "D:\Obsidian\scripts\gitee_sync.ps1"

# 仅 Git 同步（跳过得到大脑）
powershell -NoProfile -File "D:\Obsidian\scripts\gitee_sync.ps1" -SkipGetNotes
```

## 方式 C：Codex 触发

在 Codex 对话中输入 `同步gitee`，自动执行完整同步脚本。

## 推送顺序（强制）

```
本地 commit → ① push github (主) → ② push origin / Gitee (备)
                ↓ 失败
           暂停 Gitee 推送
```
