# Genspark → Gitee → Obsidian 自动同步流程
## iNEST 研究知识库的 OpenClaw/Genspark 集成管道

**最后更新**：2026-06-20
**维护者**：Genspark Claw Computer
**同步周期**：实时 (push) + 5分钟 (pull) + 定时分类 (9:00/15:00)

---

## 【初始化（仅需一次）】

### 第一步：克隆 iNEST 知识库

```bash
# 使用带凭证的 HTTPS URL
git clone https://gitee.com/iBrainNest/i-nest.git /workspace/i-nest

# 进入工作目录
cd /workspace/i-nest

# 验证克隆成功
git status
```

**预期输出**：
```
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

---

## 【核心规则 - 3 条铁律】

### ⚠️ 规则 1：写入隔离（零容忍违规）

```
🟢 可以写：00_Inbox/_from_genspark/
✅ 示例：00_Inbox/_from_genspark/2026-06-20_Genspark_simulation_results.md

🔴 绝不写：
  ❌ TCC/      (理论库，本地维护)
  ❌ iNEST/    (实现库，本地维护)
  ❌ Output/   (输出库，本地维护)
  ❌ 任何其他目录

原因：
- 防止 Genspark 覆盖本地研究成果
- 收件箱作为中转站进行人工审查
- 每日 9:00/15:00 自动分类到正确位置
```

### ⚠️ 规则 2：Pull 优先（防止冲突）

```bash
# 每次 push 前必须先 pull
git pull origin main

# 如果有冲突，解决后再继续
# [解决冲突]

git add .
git commit -m "..."
git push origin main
```

**冲突处理**：
```
如果出现冲突提示：
CONFLICT (content): Merge conflict in [file]

✅ 保留本地版本（通常是本地更新）
✅ 然后重新提交
```

### ⚠️ 规则 3：文件命名规范

```
格式：YYYY-MM-DD_Genspark_<主题>.md

✅ 正确的名称：
  - 2026-06-20_Genspark_simulation_diagnostics.md
  - 2026-06-20_Genspark_neural_complexity.md
  - 2026-06-20_Genspark_connectome_analysis.md

❌ 错误的名称：
  - genspark_results.md (缺时间戳)
  - 2026-06-20_simulation.md (缺 Genspark 标记)
  - Genspark_20-06-2026.md (日期格式错)

Frontmatter 必须包含 track 标记：
---
title: Simulation Diagnostics from Genspark
date: 2026-06-20
track: TCC
source: Genspark
---
```

---

## 【完整单次同步流程】

### 第 1 步：进入仓库并更新本地

```bash
cd /workspace/i-nest

# 检查当前状态
git status

# 从远程拉取最新变更（防止推送冲突）
git pull origin main
```

### 第 2 步：生成内容并写入收件箱

```bash
# 创建带时间戳的文件
cat > 00_Inbox/_from_genspark/2026-06-20_Genspark_<主题>.md << 'EOF'
---
title: <标题>
date: 2026-06-20T00:31
track: TCC
source: Genspark
---

# <标题>

## 内容

[您生成的所有内容写在这里]

EOF
```

**每次同步可以包含多个文件**：
```bash
# 例：同时提交多个分析文件
cat > 00_Inbox/_from_genspark/2026-06-20_Genspark_methodology_audit.md << 'EOF'
...
EOF

cat > 00_Inbox/_from_genspark/2026-06-20_Genspark_scale_intelligence.md << 'EOF'
...
EOF

cat > 00_Inbox/_from_genspark/2026-06-20_Genspark_data_plan.md << 'EOF'
...
EOF
```

### 第 3 步：提交并推送到 Gitee

```bash
# 添加新文件到暂存区
git add 00_Inbox/_from_genspark/

# 提交（带时间戳和描述）
git commit -m "genspark: $(date +%Y-%m-%dT%H:%M) 自动同步 - 仿真实验诊断与改进规划"

# 推送到远程（主分支）
git push origin main
```

**成功推送的输出**：
```
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 2.50 KiB | 2.50 MiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), reused pack 0 (delta 0)
To gitee.com:iBrainNest/i-nest.git
   b2f1a3d..3e8f9c2  main -> main
```

---

## 【完整单次同步脚本（Copy & Paste）】

### 一键执行

```bash
#!/bin/bash
# iNEST Genspark 同步脚本
# 使用方式：./sync.sh "主题描述"

cd /workspace/i-nest || exit 1

echo "📥 Step 1: 拉取最新远程变更..."
git pull origin main

echo "📝 Step 2: 准备内容..."
# [内容生成步骤 - 参见下文示例]

echo "📤 Step 3: 提交内容..."
git add 00_Inbox/_from_genspark/
git commit -m "genspark: $(date +%Y-%m-%dT%H:%M) 自动同步 - $1"

echo "🚀 Step 4: 推送到 Gitee..."
git push origin main

echo "✅ 同步完成！"
echo "📋 Obsidian 将在 5 分钟内自动更新"
```

---

## 【后续自动化流程】

### 时间轴

```
Genspark 生成内容
    ↓
Push to Gitee (实时)
    ↓ 
Gitee 远程仓库更新
    ↓
Obsidian obsidian-git 插件检测 (每 5 分钟自动 pull)
    ↓
本地 Obsidian Vault 更新
    ↓
process_inbox.py 定时运行 (09:00 / 15:00 EDT)
    ↓
LLM 智能分类（DeepSeek）
    ↓
自动移动到：
  - 10_Library/   (通用知识)
  - 30_TCC/       (TCC 理论)
  - 40_iNEST/     (iNEST 实现)
  - 20_Ideas/     (想法备忘)
```

### 关键步骤详解

#### Obsidian 自动 Pull（5 分钟周期）

**前提**：必须已安装并配置 `obsidian-git` 插件

**配置检查**：
```
Obsidian Settings → Community Plugins → obsidian-git
启用自动拉取：✅
拉取间隔：300 秒 (5分钟)
```

**无需手动操作** - 插件自动执行

#### 收件箱分类流程（9:00 / 15:00 UTC-4）

**触发条件**：
- 每日 09:00 EDT (UTC-4)
- 每日 15:00 EDT (UTC-4)

**执行内容** (process_inbox.py):
```python
# 伪代码
for file in 00_Inbox/_from_genspark/:
    content = read(file)
    category = llm_classify(content)  # 使用 DeepSeek LLM
    
    if category == "TCC理论":
        move_to("30_TCC/")
    elif category == "iNEST实现":
        move_to("40_iNEST/")
    elif category == "通用知识":
        move_to("10_Library/")
    elif category == "灵感想法":
        move_to("20_Ideas/")
```

---

## 【Genspark 的职责范围】

### ✅ 应该做的

```
1. 生成诊断、分析、规划文档
2. 写入 00_Inbox/_from_genspark/
3. 按规范命名文件（带时间戳和 track 标记）
4. 执行 git 同步流程
5. 监控推送是否成功
```

### ❌ 不需要做的

```
✗ 不用关心文件最终去向（自动分类）
✗ 不用维护 TCC/iNEST/Output 目录
✗ 不用手动分类和组织文件
✗ 不用处理 Obsidian 本地同步
✗ 完全不用接触其他目录
```

### 📋 Genspark 只管收件箱，其他自动化

```
Genspark: 仅写入 00_Inbox/_from_genspark/ + git push
       ↓
Gitee:   远程存储
       ↓
Obsidian: 自动 pull (5分钟)
       ↓
LLM分类: 自动运行 (9:00/15:00)
       ↓
最终位置: 自动归档
```

---

## 【实际使用示例】

### 示例 1：提交仿真实验诊断

```bash
cd /workspace/i-nest
git pull origin main

# 创建诊断文件
cat > 00_Inbox/_from_genspark/2026-06-20_Genspark_methodology_diagnostics.md << 'EOF'
---
title: V25 仿真实验方法论完整诊断
date: 2026-06-20T00:31
track: TCC
source: Genspark
---

# iNEST v30 仿真实验方法论诊断

## 12 项关键问题

1. 数据源混淆
2. 公式完全缺失
...

## 改进行动计划

P0 (本周): 修改论文表述...
P1 (下周): 启动真实数据...
...

EOF

git add 00_Inbox/_from_genspark/
git commit -m "genspark: $(date +%Y-%m-%dT%H:%M) 自动同步 - V25 方法论诊断"
git push origin main
```

### 示例 2：批量提交多个分析

```bash
cd /workspace/i-nest
git pull origin main

# 文件 1：规模-智能诊断
cat > 00_Inbox/_from_genspark/2026-06-20_Genspark_scale_intelligence.md << 'EOF'
---
title: 规模-智能等级矛盾分析
date: 2026-06-20
track: TCC
---

# 核心问题

C.elegans (302 神经元) 只能支撑感知级智能
但论文声称验证了推理级的 TCC 范式
这是 3-4 个等级的范式外推错误

...
EOF

# 文件 2：真实数据计划
cat > 00_Inbox/_from_genspark/2026-06-20_Genspark_real_connectome_plan.md << 'EOF'
---
title: 真实连接组数据导入计划
date: 2026-06-20
track: iNEST
---

# 已有资源

✅ C.elegans (Varshney 2011)
✅ Hemibrain (FlyEM)
✅ neural_complexity_analyzer.py

...
EOF

# 一次提交
git add 00_Inbox/_from_genspark/
git commit -m "genspark: 2026-06-20T00:31 自动同步 - 规模分析 + 数据计划"
git push origin main
```

---

## 【故障排查】

### 问题 1：克隆失败 (401 Unauthorized)

```
❌ 错误信息：
fatal: could not read Username for 'https://gitee.com': No such file or directory

✅ 解决方案：
# 检查 URL 中的凭证格式
https://gitee.com/iBrainNest/i-nest.git

注意：
- 用户名：iBrainNest
- 密码：Liusansan%406363 (@ 需要 URL 编码为 %40)
```

### 问题 2：Push 被拒 (non-fast-forward)

```
❌ 错误信息：
! [rejected] main -> main (non-fast-forward)

✅ 解决方案：
git pull origin main  # 先拉取
# [解决任何冲突]
git push origin main  # 再推送

永远遵循规则 2：Pull 优先！
```

### 问题 3：文件丢失 (Directory not found)

```
❌ 错误信息：
No such file or directory: 00_Inbox/_from_genspark/

✅ 解决方案：
# 创建目录结构
mkdir -p /workspace/i-nest/00_Inbox/_from_genspark

# 或者在克隆后确认目录存在
ls -la /workspace/i-nest/00_Inbox/
```

---

## 【Genspark 的快速检查清单】

每次同步前：

- [ ] 进入正确目录：`cd /workspace/i-nest`
- [ ] 先拉取：`git pull origin main`
- [ ] 文件命名规范：`YYYY-MM-DD_Genspark_<主题>.md`
- [ ] Frontmatter 包含 `track:` 字段
- [ ] 写入正确位置：`00_Inbox/_from_genspark/` 只有这里
- [ ] 提交前再检查：`git status`
- [ ] 推送成功：检查返回信息中 `main -> main`

---

## 【联系与支持】

### iNEST 知识库详情

```
仓库：https://gitee.com/iBrainNest/i-nest
分支：main
更新周期：实时 + 自动化
维护：本地 Obsidian + LLM 分类
```

### 关键联系人

- **本地维护**：Obsidian Vault / process_inbox.py
- **Genspark 职责**：生成 + 推送内容到收件箱
- **自动化**：obsidian-git (pull) + DeepSeek (分类)

---

## 【版本历史】

| 版本 | 日期 | 更新 |
|-----|------|------|
| 1.0 | 2026-06-20 | 初始化完整流程 |

---

**最后说明**：

这个同步管道设计为**完全自动化**。
Genspark 只需按照规则写入收件箱 + 执行 git 同步。
其余所有工作（分类、整理、归档）都由自动化工具完成。

**有任何问题，检查这个文件的"故障排查"部分。**

