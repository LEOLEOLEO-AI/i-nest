# 2026-06-23 07:25 EDT - Genspark 双远程同步配置完成

## 【配置指令】

**时间**：Tue 2026-06-23 07:25 EDT
**指令**：建立 GitHub (主) ←→ Gitee (备) 的双远程同步架构

---

## 【执行结果】✅ 完全成功

### 步骤 1：仓库现状
```
位置：~/i-nest
状态：已存在且初始化
当前 origin：git@gitee.com:iBrainNest/i-nest.git (SSH)
```

### 步骤 2：GitHub 远程添加
```bash
git remote add github https://github.com/LEOLEOLEO-AI/i-nest.git
```

**结果**：✅ GitHub 已添加为 `github` 远程

### 步骤 3：双远程配置验证
```
github   https://github.com/LEOLEOLEO-AI/i-nest.git (HTTPS，主仓库)
origin   git@gitee.com:iBrainNest/i-nest.git (SSH，备份)
```

**分支状态**：
- 本地：master (与 Gitee 同步)
- GitHub：main
- Gitee：master, main, develop, main-new

**工作区**：✅ 干净，无冲突

### 步骤 4：双向同步测试
```
Gitee：git pull origin master → Already up to date
GitHub：git fetch github → 成功拉取 github/main
最终状态：✅ 工作区干净
```

---

## 【新架构】

```
GitHub (主仓库)
  ↑
  │ (git pull/push)
  │
Genspark (日常工作)
  │
  ↓ (git pull/push)
  │
Gitee (备份)
  ↑
  │ (自动同步)
  │
Obsidian / OpenClaw
```

---

## 【日常工作流规范】

### 触发词：**"同步"**
优先从 GitHub 拉取，如不可达则从 Gitee 拉取：
```bash
cd ~/i-nest && git pull github main
# 若 GitHub 不可达：
cd ~/i-nest && git pull origin master
```

### 触发词：**"推送"**
同时推送到 GitHub 和 Gitee：
```bash
cd ~/i-nest
git add -A
git commit -m "genspark: $(date +%Y-%m-%d)"
git push github master:main      # 推送到 GitHub main
git push origin master           # 推送到 Gitee master
```

### 冲突处理流程
禁止 `--force`，使用标准三步走：
```bash
git stash                        # 保存本地改动
git pull github main (或 origin master)  # 拉取最新
git stash pop                    # 恢复本地改动，处理冲突
```

---

## 【分支对应关系】

⚠️ **重要**：GitHub 和 Gitee 默认分支名不同

| 平台 | 主分支 | 说明 |
|------|--------|------|
| GitHub | `main` | 新项目标准 |
| Gitee | `master` | 旧项目沿用 |
| 本地 | `master` | 与 Gitee 同步 |

**推送时的映射**：
```bash
git push github master:main   # 本地 master → GitHub main
git push origin master        # 本地 master → Gitee master
```

---

## 【目录权限分配（确认）】

```
00_Inbox/              → 所有平台可读写（优先推送源）
papers/                → 所有平台可读写
knowledge_graph/       → 所有平台可读写
simulation/            → Obsidian + Genspark
iNEST_4/               → Obsidian + OpenClaw
TCC_4/                 → Obsidian + OpenClaw
research/              → 所有平台可读写（诊断报告等）
```

---

## 【同步行为规则】

### 任务开始前
```
必须执行："同步"
目的：拉取最新代码，确保工作基线
```

### 任务执行中
```
在指定目录（00_Inbox/ 或 simulation/ 等）编辑文件
保存产出到对应目录
```

### 任务完成后
```
必须执行："推送"
目的：提交到 GitHub + Gitee，保持双向同步
```

---

## 【系统验证清单】

- ✅ GitHub 远程已添加（HTTPS）
- ✅ Gitee 远程已存在（SSH）
- ✅ 双向同步已测试
- ✅ 分支对应关系已明确
- ✅ 冲突处理流程已规范
- ✅ 日常触发词已准备
- ✅ 工作流规范已定
- ✅ 目录权限已分配

**全部就绪**

---

## 【立即可执行】

Genspark 现已完全就绪：

1️⃣ **任务分配**
   - 描述任务
   - 触发词："同步"（拉取最新）

2️⃣ **工作执行**
   - 在 ~/i-nest 编辑
   - 产出到指定目录

3️⃣ **提交完成**
   - 触发词："推送"（提交到两个平台）

---

## 【与诊断报告的协作】

**诊断报告位置**：
```
本地：/vault/research/2026-06-23-comprehensive_diagnosis.md
GitHub：可通过 git add/commit/push 推送
Gitee：可通过 git push 同步
```

**推送流程**：
1. OpenClaw 生成诊断报告
2. Genspark 拉取（"同步"）
3. Genspark 编辑/补充后推送（"推送"）
4. GitHub 和 Gitee 同时更新

---

**配置完成时间**：2026-06-23 07:25-07:27 EDT
**配置版本**：v1.0 双远程标准配置
**状态**：✅ 完全就绪，可日常使用

