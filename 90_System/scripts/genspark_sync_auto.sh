#!/bin/bash
# Genspark 每日自动同步 v5.0 — 直接 shell 执行，不依赖 LLM 解析
# 只推 genspark/sync，绝不碰 main
set -e

REPO="/home/work/i-nest"
WORKSPACE="/home/work/.openclaw/workspace"
TODAY=$(date '+%Y-%m-%d')
LOG="/tmp/genspark_sync_$(date '+%Y%m%d_%H%M%S').log"

echo "[$(date '+%H:%M:%S')] genspark sync v5.0 start" | tee "$LOG"

cd "$REPO"

# 1. 同步工作区内容（只同步文本文件）
rsync -a --include='*.md' --include='*.py' --include='*.sh' \
  --exclude='*' \
  "$WORKSPACE/TCC计算范式/" ./TCC计算范式/ 2>/dev/null || true

rsync -a --include='*.md' --exclude='*' \
  "$WORKSPACE/50_Output/Reports/" ./50_Output/Reports/ 2>/dev/null || true

rsync -a --include='*.md' --exclude='*' \
  "$WORKSPACE/00_KnowledgeBase_知识库/02_Analysis/arxiv-upgraded/" \
  ./00_KnowledgeBase/02_Analysis/arxiv-upgraded/ 2>/dev/null || true

rsync -a --include='*.md' --exclude='*' \
  "$WORKSPACE/memory/" ./memory/ 2>/dev/null || true

cp "$WORKSPACE/MEMORY.md" ./MEMORY.md 2>/dev/null || true

echo "[$(date '+%H:%M:%S')] rsync done" | tee -a "$LOG"

# 2. 先 add 所有未跟踪文件（避免 checkout 时报 untracked 冲突）
git add -A 2>/dev/null || true

# 3. 切换到 genspark/sync 分支
git stash 2>/dev/null || true
git checkout genspark/sync 2>/dev/null || \
  git checkout -b genspark/sync 2>/dev/null
git stash pop 2>/dev/null || true

# 4. 合并 main 最新内容
git merge main --no-edit -X ours \
  -m "auto: merge main into genspark/sync $TODAY" 2>/dev/null || true

# 5. Commit
git add -A
if ! git diff --cached --quiet; then
  git commit -m "genspark: auto sync $TODAY $(date '+%H:%M')"
  HASH=$(git rev-parse --short HEAD)
  echo "[$(date '+%H:%M:%S')] committed $HASH" | tee -a "$LOG"
else
  HASH=$(git rev-parse --short HEAD)
  echo "[$(date '+%H:%M:%S')] no changes, skip commit ($HASH)" | tee -a "$LOG"
fi

# 6. 推送（只推 genspark/sync，永不推 main）
git push github genspark/sync 2>&1 | tee -a "$LOG"
PUSH_EXIT=${PIPESTATUS[0]}

git checkout main 2>/dev/null

# 7. 结果
if [ $PUSH_EXIT -eq 0 ]; then
  echo "SUCCESS:$HASH" | tee -a "$LOG"
  exit 0
else
  echo "PUSH_FAILED:$PUSH_EXIT" | tee -a "$LOG"
  exit 1
fi
