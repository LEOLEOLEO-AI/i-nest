---
provenance: external
---

# Git 同步策略 v2.0（2026-07-05）

## 双仓库主备架构

### GitHub（主仓库）- ⭐ 优先级最高
```
URL: git@github.com:LEOLEOLEO-AI/i-nest.git
用户: LEOLEOLEO-AI
用途: 学术论文发布、算法代码开源
保留策略: 精简版（不含大数据文件）
推送频率: 每日一次（自动）
访问权限: 公开
```

### Gitee（备份镜像）- ⭐⭐ 次优先级
```
URL: git@gitee.com:iBrainNest/i-nest.git
用户: iBrainNest
用途: 完整数据备份、内部知识库
保留策略: 完整版（含所有历史数据）
推送频率: 实时同步（跟随本地更新）
访问权限: 内部
```

## 推送优先级规则

### 规则 1：本地更新流程
```
本地代码更新
    ↓
git add / commit
    ↓
git push github main   （推送到 GitHub - 主）
    ↓
git push origin main   （推送到 Gitee - 备）
```

### 规则 2：冲突解决
```
如果 GitHub 冲突：
  → 用本地版本覆盖（git push -f github main）
  
如果 Gitee 冲突：
  → 用本地版本覆盖（git push -f origin main）
  
原因：本地版本始终是最新的，包含所有改进
```

### 规则 3：每日自动推送
```
时间：每天 23:00 EDT（晚上 11 点）
任务：Daily Papers Auto Push
目标：GitHub main（主要）+ Gitee origin（备份）
```

## 具体配置命令

### 已执行的配置
```bash
# GitHub 主仓库
git remote set-url github git@github.com:LEOLEOLEO-AI/i-nest.git
git remote set-url --push github git@github.com:LEOLEOLEO-AI/i-nest.git

# Gitee 备份仓库
git remote set-url origin git@gitee.com:iBrainNest/i-nest.git
git remote set-url --push origin git@gitee.com:iBrainNest/i-nest.git

# 推送策略
git config --global push.default simple
```

### 验证配置
```bash
git remote -v
# 应显示：
# github: fetch/push → LEOLEOLEO-AI/i-nest
# origin: fetch/push → iBrainNest/i-nest
```

## Genspark/Codex 集成

### 需要修改的文件
```
路径: ~/.openclaw/workspace/90_System/scripts/Genspark_gitee_sync.md

修改项:
1. 添加 GitHub 推送 step
2. 调整推送顺序为：本地 → GitHub → Gitee
3. 标记 GitHub 为主推送目标
```

### 推荐的新脚本逻辑
```bash
# Genspark 每日推送流程

if [ daily_trigger ]; then
  # 第一步：获取本地最新
  git fetch --all
  
  # 第二步：推送到 GitHub（主）
  git push github main
  echo "✅ GitHub 推送完成"
  
  # 第三步：推送到 Gitee（备）
  git push origin main
  echo "✅ Gitee 推送完成"
  
  # 第四步：记录日志
  git log -1 --oneline >> /tmp/daily_push.log
fi
```

## 优先级判定

### GitHub 优先级更高的原因
```
1. 学术发布：论文需要在 GitHub 先发表
2. 开源社区：GitHub 是行业标准
3. 引用追踪：引用通常指向 GitHub URL
4. 并发访问：GitHub 更稳定，CDN 覆盖全球
```

### Gitee 的作用
```
1. 数据备份：完整历史保留
2. 国内加速：面向中文用户
3. 内部知识库：研究过程文档存储
4. 容灾备份：GitHub 故障时的恢复源
```

## 注意事项

### 严格禁止
```
❌ 直接在两个仓库上修改（会导致分支分歧）
❌ 跳过本地提交直接推送（会丢失历史）
❌ 用 Gitee 作为主推送目标（应该用 GitHub）
❌ 忘记同时推送两个远程（会导致不同步）
```

### 强制执行
```
✅ 所有本地更新必须 git commit
✅ 所有 commit 后必须推送两个远程
✅ GitHub 推送失败则暂停 Gitee 推送
✅ 每周检查两个仓库是否同步
```

## 同步状态检查命令

```bash
# 查看本地与 GitHub 的差异
git rev-list --count main..github/main  # GitHub 领先提交数
git rev-list --count github/main..main  # 本地领先提交数

# 查看本地与 Gitee 的差异
git rev-list --count main..origin/main  # Gitee 领先提交数
git rev-list --count origin/main..main  # 本地领先提交数

# 同步所有远程
git fetch --all

# 查看所有远程的最新提交
git log --oneline github/main -1
git log --oneline origin/main -1
git log --oneline main -1
```

## 日期与版本

```
创建日期：2026-07-05 00:15 EDT
版本：v2.0（双仓库主备策略）
维护者：OpenClaw 自动同步系统
最后修改：自动配置生成
```

---

**本文档自动生成，不需手动编辑**
**所有配置通过 Git 命令行完成**
