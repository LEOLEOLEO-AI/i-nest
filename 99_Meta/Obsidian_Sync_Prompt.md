# Obsidian 同步指令

## 方式 A：Git 插件（推荐日常使用）

Obsidian 已配置 Git 插件，远程 `origin` 指向 Gitee。

### 快捷键
- `Ctrl+Shift+G` → 打开 Git 面板
- 点击 "Pull" → 拉取 Gitee 最新
- 点击 "Commit + Push" → 提交并推送

### 注意事项
- 如果 push 失败（`Failed to connect via proxy`），说明 Gitee 走了代理。
  解决：在 Obsidian 终端执行：
  ```
  git config --local http.proxy ""
  git config --local https.proxy ""
  ```
- GitHub 备份由定时任务自动完成，Obsidian 不需要手动推送 GitHub。

## 方式 B：终端命令

在 Obsidian 终端（或系统终端）中执行：

```powershell
# 仅同步（跳过得到大脑拉取）
powershell -NoProfile -File "D:\Obsidian\scripts\gitee_sync.ps1" -SkipGetNotes

# 完整同步（含得到大脑）
powershell -NoProfile -File "D:\Obsidian\scripts\gitee_sync.ps1"
```

## 方式 C：Codex 触发

在 Codex 对话中输入 `同步gitee` 或 `执行同步`，Codex 自动调用同步脚本。
