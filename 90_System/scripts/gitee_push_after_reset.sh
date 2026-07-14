#!/bin/bash
# 用于 Gitee 仓库重建后的首次推送
# 执行前提：已在 Gitee 网页删除并重建 iBrainNest/i-nest 仓库

set -e

REPO_DIR="/tmp/i-nest-fresh"

echo "[$(date)] 开始推送到 Gitee..."
cd "$REPO_DIR"

# 确认 SSH 连通
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 -T git@gitee.com 2>&1 | grep -q "successfully" && \
  echo "✅ Gitee SSH 认证正常" || { echo "❌ SSH 认证失败"; exit 1; }

# 推送
git remote remove origin 2>/dev/null || true
git remote add origin git@gitee.com:iBrainNest/i-nest.git

echo "开始推送 main 分支..."
GIT_SSH_COMMAND="ssh -o ServerAliveInterval=15 -o ServerAliveCountMax=20" \
  git push origin main --force

echo "[$(date)] ✅ Gitee 推送完成"
