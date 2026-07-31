---
provenance: external
---

# Genspark Git 工作流规范 v2.0 - 含强制验证机制

## 【核心原则】

**永不信任推送命令的成功消息。必须验证文件实际在远程可访问。**

---

## 【完整工作流（带验证）】

### 阶段 1：开始工作

**触发词**："同步"

```bash
cd ~/i-nest && git pull github main
# 或 (GitHub 不可达时)：
cd ~/i-net && git pull origin master

# 验证
git status  # 工作区应该干净
```

**检查清单**：
- [ ] 工作区干净（无未提交文件）
- [ ] 本地分支 = 远程最新

---

### 阶段 2：任务执行

**在指定目录编辑和生成文件**：

```
目录分配：
  00_Inbox/       → 共享临时文件
  papers/         → 论文和文献
  50_Output/      → 【新】诊断报告和最终输出
  simulation/     → 仿真代码
  40_iNEST/       → iNEST 相关研究
  30_TCC/         → TCC 计算范式
```

**特别关注**：OpenClaw 生成的诊断报告需要复制到 50_Output/

```bash
# 从 OpenClaw 复制诊断报告到 Genspark
cp /vault/research/*.md ~/i-nest/50_Output/
```

---

### 阶段 3：提交和推送

**触发词**："推送"

```bash
cd ~/i-nest

# 1️⃣ 添加所有变更
git add -A

# 2️⃣ 创建提交
git commit -m "genspark: $(date +%Y-%m-%d_%H:%M:%S)"

# 3️⃣ 推送到 GitHub main
git push github master:main

# 4️⃣ 推送到 Gitee master
git push origin master

# 5️⃣ 【关键】验证推送成功
echo "=== Verification ==="
git push --dry-run github master:main 2>&1 | grep -i "up to date\|error\|reject" || echo "✓ GitHub ready"
git push --dry-run origin master 2>&1 | grep -i "up to date\|error\|reject" || echo "✓ Gitee ready"
```

**状态检查**：
```bash
# 确保工作区干净
git status
# 输出应为：On branch master, nothing to commit, working tree clean
```

---

### 阶段 4：【新增】强制验证阶段

**这是最关键的新增步骤 - 推送后必须验证文件实际在远程可访问**

#### ✅ 验证 1：检查远程提交

```bash
# 获取最新的远程提交 ID
GITHUB_HEAD=$(git ls-remote github main | awk '{print $1}')
GITEE_HEAD=$(git ls-remote origin master | awk '{print $1}')
LOCAL_HEAD=$(git rev-parse HEAD)

echo "本地提交：$LOCAL_HEAD"
echo "GitHub 最新：$GITHUB_HEAD"
echo "Gitee 最新：$GITEE_HEAD"

# 验证三方一致
if [ "$LOCAL_HEAD" = "$GITHUB_HEAD" ] && [ "$LOCAL_HEAD" = "$GITEE_HEAD" ]; then
    echo "✅ 远程同步成功"
else
    echo "❌ 远程同步失败！"
    echo "需要重新推送或诊断问题"
    exit 1
fi
```

#### ✅ 验证 2：检查文件在远程存在

```bash
# 对于关键文件（如诊断报告），检查文件在远程的实际存在

# GitHub
if git ls-tree -r github/main | grep "50_Output/2026-06-23-comprehensive_diagnosis.md"; then
    echo "✅ 诊断报告已在 GitHub"
else
    echo "❌ 诊断报告未在 GitHub！"
    exit 1
fi

# Gitee
if git ls-tree -r origin/master | grep "50_Output/2026-06-23-comprehensive_diagnosis.md"; then
    echo "✅ 诊断报告已在 Gitee"
else
    echo "❌ 诊断报告未在 Gitee！"
    exit 1
fi
```

#### ✅ 验证 3：检查文件内容完整性

```bash
# 对于诊断报告，验证行数和大小
REMOTE_SIZE=$(git show github/main:50_Output/2026-06-23-comprehensive_diagnosis.md 2>/dev/null | wc -c)
LOCAL_SIZE=$(cat ~/i-nest/50_Output/2026-06-23-comprehensive_diagnosis.md | wc -c)

if [ "$REMOTE_SIZE" -gt 0 ] && [ "$REMOTE_SIZE" -eq "$LOCAL_SIZE" ]; then
    echo "✅ GitHub 文件内容完整 ($REMOTE_SIZE 字节)"
else
    echo "❌ GitHub 文件内容不完整或不存在！"
    echo "本地：$LOCAL_SIZE 字节，GitHub：$REMOTE_SIZE 字节"
    exit 1
fi
```

#### ✅ 验证 4：最终报告

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "【推送验证完成】"
echo "✅ GitHub master → main    推送成功"
echo "✅ Gitee master            推送成功"
echo "✅ 诊断报告文件已验证      在线可访问"
echo "✅ 工作流完成              所有检查通过"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

---

## 【冲突处理规范】

```bash
# 如果推送遇到冲突

git stash                    # 保存本地改动
git pull github main         # 拉取最新（或 git pull origin master）
git stash pop                # 恢复改动

# 【关键】解决冲突后重新验证
git add .
git commit -m "merge: resolve conflicts"
git push github master:main
git push origin master

# 重新执行验证流程
```

---

## 【检查清单】

### 推送前
- [ ] 所有新文件已添加（git add -A）
- [ ] 提交信息已创建（git commit）
- [ ] 本地分支最新（git pull 已执行）

### 推送中
- [ ] GitHub 推送成功（无错误）
- [ ] Gitee 推送成功（无错误）
- [ ] 工作区干净

### 推送后（验证）
- [ ] 远程提交 ID 一致
- [ ] 关键文件在 GitHub 存在
- [ ] 关键文件在 Gitee 存在
- [ ] 文件内容完整（大小一致）
- [ ] 在线 URL 可访问（可选：curl 验证）

### 最终确认
- [ ] 所有验证通过 ✅
- [ ] 可发送成功报告给用户

---

## 【自动化验证脚本】

### 创建 verify_push.sh

```bash
#!/bin/bash
set -e

cd ~/i-nest

echo "【推送后验证脚本】"
echo "================================"

# 1. 检查工作区
echo "1️⃣ 检查工作区..."
git status
if [ "$(git status --porcelain | wc -l)" -gt 0 ]; then
    echo "❌ 工作区有未提交的文件！"
    exit 1
fi
echo "✅ 工作区干净"

# 2. 检查远程同步
echo ""
echo "2️⃣ 检查远程同步..."
GITHUB_HEAD=$(git ls-remote github main | awk '{print $1}')
GITEE_HEAD=$(git ls-remote origin master | awk '{print $1}')
LOCAL_HEAD=$(git rev-parse HEAD)

echo "本地: $LOCAL_HEAD"
echo "GitHub: $GITHUB_HEAD"
echo "Gitee: $GITEE_HEAD"

if [ "$LOCAL_HEAD" != "$GITHUB_HEAD" ]; then
    echo "❌ GitHub 同步失败！"
    exit 1
fi

if [ "$LOCAL_HEAD" != "$GITEE_HEAD" ]; then
    echo "❌ Gitee 同步失败！"
    exit 1
fi
echo "✅ 远程同步成功"

# 3. 检查关键文件
echo ""
echo "3️⃣ 检查关键文件..."

# 诊断报告检查
if git ls-tree -r github/main | grep -q "50_Output/2026-06-23-comprehensive_diagnosis.md"; then
    echo "✅ 诊断报告已在 GitHub"
else
    echo "⚠️  诊断报告未在 GitHub（可能是新文件）"
fi

if git ls-tree -r origin/master | grep -q "50_Output/2026-06-23-comprehensive_diagnosis.md"; then
    echo "✅ 诊断报告已在 Gitee"
else
    echo "⚠️  诊断报告未在 Gitee（可能是新文件）"
fi

# 4. 最终报告
echo ""
echo "================================"
echo "✅ 推送验证完成"
echo "================================"
echo ""
echo "在线访问地址："
echo "GitHub: https://github.com/LEOLEOLEO-AI/i-nest"
echo "Gitee: https://gitee.com/iBrainNest/i-nest"
```

### 使用方法

```bash
# 使脚本可执行
chmod +x ~/verify_push.sh

# 推送后执行验证
~/verify_push.sh
```

---

## 【新的触发词规范】

### "同步" (git pull + verify)
```
执行：git pull github main (或 origin master)
验证：git status（工作区干净）
```

### "推送" (git push + full verify)
```
执行：git add -A && commit && push github && push origin
验证：
  1. 远程提交 ID 一致
  2. 关键文件存在
  3. 文件内容完整
  4. 最终报告
```

---

## 【推荐的工作流图】

```
任务开始
  ↓
"同步"  ← 拉取最新
  ↓
编辑文件
  ↓
生成诊断报告 (OpenClaw)
  ↓
复制到 50_Output/ (Genspark)
  ↓
"推送"  ← git add + commit + push
  ↓
验证 1：远程提交 ID 一致 ✅
  ↓
验证 2：文件在远程存在 ✅
  ↓
验证 3：文件内容完整 ✅
  ↓
验证 4：最终报告 ✅
  ↓
任务完成
```

---

## 【关键原则（黄金规则）】

### ⚠️ 永远不要相信推送命令的成功消息

```
❌ 错误做法：
git push github master:main
echo "推送成功！"  ← 不验证，直接报告

✅ 正确做法：
git push github master:main
git ls-remote github main | grep $(git rev-parse HEAD) && echo "推送成功！" || echo "推送失败，检查原因"
```

### ⚠️ 验证 > 报告

```
不能这样：
  git push
  报告用户"推送成功"
  
应该这样：
  git push
  验证文件实际在远程
  验证通过后才报告"推送成功"
```

### ⚠️ 建立反馈环

```
推送 → 验证 → 反馈 → 确认

如果验证失败：
  诊断原因
  重新推送
  再次验证
  不通过则报告错误，不隐瞒
```

---

**规范版本**：v2.0（含强制验证机制）
**生效时间**：2026-06-23 08:28 EDT
**强制执行**：所有推送操作必须包含验证步骤

