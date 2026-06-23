---
title: "Genspark Claw Computer — Obsidian 同步指令"
date: 2026-06-20
type: instruction
target: Genspark Claw Computer Agent
---

# Genspark → Obsidian 同步指令

> 📋 将此文档全文发送给 Genspark Claw Computer，它可以直接执行每一条命令。

---

## 1. 仓库配置（一次性）

```bash
# 克隆仓库（如果还没克隆）
git clone https://iBrainNest:Liusansan%406363@gitee.com/iBrainNest/i-nest.git /workspace/i-nest
cd /workspace/i-nest

# 配置用户信息
git config user.name "Genspark"
git config user.email "genspark@inest.research"
```

---

## 2. 每次同步前（必须先执行）

```bash
cd /workspace/i-nest
git pull origin main
```

---

## 3. 写入内容 — 严格遵守以下规则

### 3.1 文件位置

**所有 Genspark 产出的笔记，只写入 `00_Inbox/_from_genspark/` 目录。**

```
✅ 正确: 00_Inbox/_from_genspark/2026-06-20_Genspark_突触可塑性最新进展.md
❌ 错误: 40_iNEST/xxx.md
❌ 错误: 30_TCC/xxx.md
```

### 3.2 文件命名

```
YYYY-MM-DD_Genspark_<简短主题>.md
```

示例：
- `2026-06-20_Genspark_忆阻器阵列容错路由算法.md`
- `2026-06-21_Genspark_自由能原理与主动推理综述.md`

### 3.3 文件格式（Frontmatter 必须包含）

每个文件开头必须有 YAML frontmatter：

```markdown
---
title: "文章标题"
date: 2026-06-20
source: genspark
track: TCC   # 或 iNEST — 由 Genspark 初步判断
tags: [genspark, 具体关键词]
---

# 文章标题

正文内容...
```

### 3.4 track 判断标准

| track | 关键词匹配 |
|:---|:---|
| `TCC` | 晶圆级集成、chiplet、片上网络、SDSoW、拓扑路由、variational free energy、互连架构 |
| `iNEST` | 神经形态、脉冲神经网络、忆阻器、自组织临界、涌现、类脑计算、主动推理 |

如果无法判断 → 写 `TCC`（后续 LLM 管道会重新分类）。

---

## 4. 提交与推送

```bash
cd /workspace/i-nest

# 只添加 Genspark 目录下的文件
git add 00_Inbox/_from_genspark/

# 提交
git commit -m "genspark: $(date +%Y-%m-%d) 自动同步 — <本次主题>"

# 推送
git push origin main
```

---

## 5. 完整单次同步脚本

```bash
#!/bin/bash
# genspark_sync.sh — Genspark 单次同步脚本

cd /workspace/i-nest
git pull origin main

# 在这里执行 Genspark 的内容生成逻辑
# 将产出的 .md 文件写入 00_Inbox/_from_genspark/

git add 00_Inbox/_from_genspark/
git commit -m "genspark: $(date +%Y-%m-%dT%H:%M) 自动同步"
git push origin main
echo "✅ Genspark sync done."
```

---

## 6. 冲突处理

如果 push 被拒绝（`rejected`）：

```bash
git pull --rebase origin main
git push origin main
```

---

## 7. 定时执行（可选）

在 Genspark 的 Linux 环境中添加 crontab：

```bash
# 每天 7:30, 12:30, 18:30 执行同步
30 7,12,18 * * * /workspace/i-nest/genspark_sync.sh >> /workspace/i-nest/logs/genspark_sync.log 2>&1
```

---

## 8. 注意事项

1. **绝不**直接编辑 `30_TCC/`、`40_iNEST/`、`50_Output/` 下的文件 — 由本地管道处理
2. 每次 push 前**必须**先 pull，防止冲突
3. 文件名**不要**含特殊字符（`/\:*?"<>|`）
4. 如果 Gitee 推送失败（超限），等待本地 GC 完成后重试

---

## 9. Obsidian 端自动处理

Genspark 推送后，Obsidian 端 `obsidian-git` 插件每 5 分钟自动 pull。

管道定时任务自动执行：
- **09:00** / **15:00**: `process_inbox.py` — LLM 分类 + 移动到对应目录
- **每周日 03:00**: 全量重组

Genspark 无需关心后续流程。

---

> 📤 将第 1 节命令执行一遍完成初始化，后续每次使用第 5 节的完整脚本即可。
