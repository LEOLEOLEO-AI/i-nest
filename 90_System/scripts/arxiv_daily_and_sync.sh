#!/bin/bash
# arXiv 日报 + genspark/sync 一体化脚本 v4.0
#
# 功能：
#   1. 爬取当日 arXiv 论文（gsk 三维分析）→ 直接写入 i-nest/20_Processing/20_KnowledgeBase/arxiv-auto/
#   2. 只把 arxiv-auto 目录 cherry-pick 到 genspark/sync（不做全量 merge，避免冲突）
#   3. push → genspark/sync 分支（Codex 每日 21:00 合并到 main）
#
# v4.0 改动：去掉 merge github/main，改用 cherry-pick 单目录推送，彻底避免冲突

set -e

TODAY=$(date '+%Y-%m-%d')
LOG="/tmp/arxiv_sync_${TODAY}.log"
DONE_FLAG="/tmp/arxiv_sync_${TODAY}.done"

ARXIV_SCRIPT="/home/work/.openclaw/workspace/scripts/arxiv_to_wiki.py"
REPO="/home/work/i-nest"
ARXIV_DIR="20_Processing/20_KnowledgeBase/arxiv-auto"
ARXIV_REPO="$REPO/$ARXIV_DIR"

# 防止重复触发
if [ -f "$DONE_FLAG" ]; then
  echo "[$TODAY] 今日已完成，跳过" && exit 0
fi

echo "[$(date '+%H:%M:%S')] === arXiv 日报 + sync v4.0 START ===" | tee "$LOG"

# ── 步骤 1：确保在 main 分支，爬取写入 ──────────────────────────────────
cd "$REPO"
git checkout main 2>/dev/null || true

echo "[$(date '+%H:%M:%S')] 爬取 arXiv 日报..." | tee -a "$LOG"
mkdir -p "$ARXIV_REPO"
python3 "$ARXIV_SCRIPT" >> "$LOG" 2>&1
added=$(ls "$ARXIV_REPO"/*${TODAY}*.md 2>/dev/null | wc -l | tr -d ' ')
echo "[$(date '+%H:%M:%S')] 爬取完成，今日新增: $added 篇" | tee -a "$LOG"

# ── 步骤 2：在 main 上 commit arxiv-auto ────────────────────────────────
git add "$ARXIV_DIR/" 2>/dev/null || true
if ! git diff --cached --quiet; then
  git commit -m "genspark: arXiv日报 $TODAY ${added}篇 → $ARXIV_DIR"
  MAIN_HASH=$(git rev-parse --short HEAD)
  echo "[$(date '+%H:%M:%S')] main commit: $MAIN_HASH" | tee -a "$LOG"
else
  MAIN_HASH=$(git rev-parse --short HEAD)
  echo "[$(date '+%H:%M:%S')] 无新内容，跳过 main commit ($MAIN_HASH)" | tee -a "$LOG"
fi

# ── 步骤 3：推送到 genspark/sync（只 cherry-pick arxiv commit）───────────
git fetch github 2>/dev/null || true

# 切到 genspark/sync，基于远程最新状态
git checkout genspark/sync 2>/dev/null || \
  git checkout -b genspark/sync github/genspark/sync 2>/dev/null || \
  git checkout -b genspark/sync

git reset --hard github/genspark/sync 2>/dev/null || true

# 只把 arxiv-auto 目录的文件直接复制过来，不做 merge/cherry-pick
git checkout main -- "$ARXIV_DIR/" 2>/dev/null || true
git add "$ARXIV_DIR/" 2>/dev/null || true

if ! git diff --cached --quiet; then
  git commit -m "genspark: arXiv日报 $TODAY ${added}篇 → $ARXIV_DIR"
  HASH=$(git rev-parse --short HEAD)
  echo "[$(date '+%H:%M:%S')] genspark/sync commit: $HASH" | tee -a "$LOG"
else
  HASH=$(git rev-parse --short HEAD)
  echo "[$(date '+%H:%M:%S')] genspark/sync 无变化 ($HASH)" | tee -a "$LOG"
fi

# 推送（只推 genspark/sync，永不推 main）
git push github genspark/sync 2>&1 | tee -a "$LOG"
PUSH_EXIT=${PIPESTATUS[0]}

# 切回 main
git checkout main 2>/dev/null || true

# ── 结果 ─────────────────────────────────────────────────────────────────
if [ $PUSH_EXIT -eq 0 ]; then
  touch "$DONE_FLAG"
  echo "[$(date '+%H:%M:%S')] === 全部完成 hash=$HASH ===" | tee -a "$LOG"
  exit 0
else
  echo "[$(date '+%H:%M:%S')] === 推送失败 exit=$PUSH_EXIT ===" | tee -a "$LOG"
  exit 1
fi
