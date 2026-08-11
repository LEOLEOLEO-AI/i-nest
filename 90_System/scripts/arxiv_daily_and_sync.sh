#!/bin/bash
# arXiv 日报 + genspark/sync 一体化脚本 v5.0
# v5.0: 去掉 set -e，屏蔽 git 警告，确保 isolated agent 退出码可靠
TODAY=$(date '+%Y-%m-%d')
LOG="/tmp/arxiv_sync_${TODAY}.log"
DONE_FLAG="/tmp/arxiv_sync_${TODAY}.done"
ARXIV_SCRIPT="/home/work/.openclaw/workspace/scripts/arxiv_to_wiki.py"
REPO="/home/work/i-nest"
ARXIV_DIR="20_Processing/20_KnowledgeBase/arxiv-auto"
ARXIV_REPO="$REPO/$ARXIV_DIR"
if [ -f "$DONE_FLAG" ]; then echo "[$TODAY] 今日已完成，跳过"; exit 0; fi
echo "[$(date '+%H:%M:%S')] === arXiv 日报 + sync v5.0 START ===" | tee "$LOG"
cd "$REPO"
git checkout main 2>/dev/null || true
echo "[$(date '+%H:%M:%S')] 爬取 arXiv 日报..." | tee -a "$LOG"
mkdir -p "$ARXIV_REPO"
python3 "$ARXIV_SCRIPT" >> "$LOG" 2>&1
added=$(ls "$ARXIV_REPO"/*${TODAY}*.md 2>/dev/null | wc -l | tr -d ' ')
echo "[$(date '+%H:%M:%S')] 爬取完成，今日新增: $added 篇" | tee -a "$LOG"
git add "$ARXIV_DIR/" 2>/dev/null || true
if git diff --cached --quiet 2>/dev/null; then
  MAIN_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
  echo "[$(date '+%H:%M:%S')] 无新内容，跳过 main commit ($MAIN_HASH)" | tee -a "$LOG"
else
  git commit -m "genspark: arXiv日报 $TODAY ${added}篇 → $ARXIV_DIR" 2>/dev/null || true
  MAIN_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
  echo "[$(date '+%H:%M:%S')] main commit: $MAIN_HASH" | tee -a "$LOG"
fi
git fetch github 2>/dev/null || true
if git show-ref --verify --quiet refs/heads/genspark/sync; then
  git checkout genspark/sync 2>/dev/null || true
else
  git checkout -b genspark/sync github/genspark/sync 2>/dev/null || git checkout -b genspark/sync 2>/dev/null || true
fi
git reset --hard github/genspark/sync 2>/dev/null || true
git checkout main -- "$ARXIV_DIR/" 2>/dev/null || true
git add "$ARXIV_DIR/" 2>/dev/null || true
if git diff --cached --quiet 2>/dev/null; then
  HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
  echo "[$(date '+%H:%M:%S')] genspark/sync 无变化 ($HASH)" | tee -a "$LOG"
else
  git commit -m "genspark: arXiv日报 $TODAY ${added}篇 → $ARXIV_DIR" 2>/dev/null || true
  HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
  echo "[$(date '+%H:%M:%S')] genspark/sync commit: $HASH" | tee -a "$LOG"
fi
PUSH_OUT=$(git push github genspark/sync 2>&1)
PUSH_EXIT=$?
echo "[$(date '+%H:%M:%S')] push: $PUSH_OUT" | tee -a "$LOG"
git checkout main 2>/dev/null || true
if [ $PUSH_EXIT -eq 0 ] || echo "$PUSH_OUT" | grep -q "Everything up-to-date"; then
  touch "$DONE_FLAG"
  echo "[$(date '+%H:%M:%S')] === 成功完成 hash=$HASH added=$added ===" | tee -a "$LOG"
  exit 0
else
  echo "[$(date '+%H:%M:%S')] === 推送失败 exit=$PUSH_EXIT ===" | tee -a "$LOG"
  exit 1
fi
