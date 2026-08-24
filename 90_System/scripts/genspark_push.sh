#!/bin/bash
# Genspark → GitHub/Gitee 安全同步脚本 v3.0
# 彻底解决方案：push 被拒时自动 rebase，永不 force push main
# 2026-07-14

set -e
REPO="/home/work/i-nest"
cd "$REPO"

TODAY=$(date '+%Y-%m-%d')
TIME=$(date '+%H:%M')
echo "[sync] 开始 $TODAY $TIME"

# ── 1. 确保在 main 分支 ──
git checkout main 2>/dev/null

# ── 2. stage 所有变更 ──
git add -A

# ── 3. 有变更才 commit ──
if ! git diff --cached --quiet; then
    git commit -m "daily sync: $TODAY $TIME"
    echo "[sync] 新增 commit"
else
    echo "[sync] 无新变更，跳过 commit"
fi

# ── 4. 推 GitHub：被拒则 rebase 后重推（最多3次，永不 force）──
push_with_rebase() {
    local remote=$1
    local branch=main
    for attempt in 1 2 3; do
        if git push "$remote" "$branch" 2>&1; then
            echo "[sync] $remote push 成功"
            return 0
        fi
        echo "[sync] $remote push 被拒（第${attempt}次），执行 rebase..."
        git fetch "$remote" "$branch" 2>/dev/null
        git rebase "$remote/$branch" 2>/dev/null || {
            # rebase 冲突：用我们的版本
            git rebase --strategy-option=ours --continue 2>/dev/null || \
            git rebase --abort 2>/dev/null && \
            git merge "$remote/$branch" -X ours --no-edit \
              -m "auto-merge: resolve conflict $TODAY $TIME"
        }
    done
    echo "[sync] ⚠ $remote 推送3次失败，放弃"
    return 1
}

push_with_rebase github || true

# ── 5. 推 Gitee（同样策略）──
push_with_rebase origin || true

echo "[sync] ✅ 完成 $(date '+%H:%M:%S')"
