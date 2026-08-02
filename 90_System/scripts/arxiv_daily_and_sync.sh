#!/bin/bash
# arXiv 日报 + genspark/sync 一体化脚本 v3.0
#
# 功能：
#   1. 爬取当日 arXiv 论文（gsk 三维分析）→ 直接写入 i-nest/20_Processing/20_KnowledgeBase/arxiv-auto/
#   2. commit + push → genspark/sync 分支（Codex 每日 21:00 合并到 main）
#
# 架构说明：
#   i-nest = Obsidian 知识库 + Git 仓库，二合一
#   写入地址：20_Processing/20_KnowledgeBase/arxiv-auto/
#   Genspark 只推 genspark/sync，Codex 合并到 main
#
# 触发方式：
#   cron 08:00 EDT 直接调用此脚本（nohup 后台，立即返回）
#   手动测试：bash /home/work/i-nest/90_System/scripts/arxiv_daily_and_sync.sh

set -e

TODAY=$(date '+%Y-%m-%d')
LOG="/tmp/arxiv_sync_${TODAY}.log"
DONE_FLAG="/tmp/arxiv_sync_${TODAY}.done"

ARXIV_SCRIPT="/home/work/.openclaw/workspace/scripts/arxiv_to_wiki.py"
REPO="/home/work/i-nest"
ARXIV_REPO="$REPO/20_Processing/20_KnowledgeBase/arxiv-auto"

# 防止重复触发
if [ -f "$DONE_FLAG" ]; then
  echo "[$TODAY] 今日已完成，跳过" && exit 0
fi

echo "[$(date '+%H:%M:%S')] === arXiv 日报 + sync v3.0 START ===" | tee "$LOG"

# ── 步骤 1：爬取 + gsk 分析，直接写入 i-nest ────────────────────────────
echo "[$(date '+%H:%M:%S')] 爬取 arXiv 日报..." | tee -a "$LOG"
mkdir -p "$ARXIV_REPO"
python3 "$ARXIV_SCRIPT" >> "$LOG" 2>&1
added=$(ls "$ARXIV_REPO"/*${TODAY}*.md 2>/dev/null | wc -l | tr -d ' ')
echo "[$(date '+%H:%M:%S')] 爬取完成，今日新增: $added 篇" | tee -a "$LOG"

# ── 步骤 1.5：质量校验（防止空白章节静默发布）──────────────────
echo "[$(date '+%H:%M:%S')] 校验今日生成文件..." | tee -a "$LOG"
EMPTY_N=0
for f in "$ARXIV_REPO"/*${TODAY}*.md; do
  [ -f "$f" ] || continue
  case "$f" in *-index.md) continue;; esac
  # 占位符“、”或空 answer 视为分析失败
  if grep -q '^、$' "$f" || grep -q '^answer:$' "$f"; then
    EMPTY_N=$((EMPTY_N+1))
    echo "  ⚠️ 分析不完整: $(basename "$f")" | tee -a "$LOG"
    # 在 frontmatter 闭合（第二个 ---）之后插入醒目警告，避免空章节被当作有效内容
    awk 'BEGIN{n=0} /^---$/{n++; if(n==2){print; print "> ⚠️ [自动校验] gsk 三维分析失败/不完整，含空章节，待重跑"; next}} {print}' "$f" > "$f.tmp" && mv "$f.tmp" "$f"
  fi
done
echo "[$(date '+%H:%M:%S')] 校验完成，不完整文件: $EMPTY_N 篇（已加警告标记）" | tee -a "$LOG"

# ── 步骤 2：推送到 genspark/sync ─────────────────────────────────────────
cd "$REPO"

# fetch 最新，避免 push 冲突
git fetch github 2>/dev/null || true

# 保存当前工作目录状态
git add -A 2>/dev/null || true
git stash 2>/dev/null || true

# 切换到 genspark/sync
if git show-ref --verify --quiet refs/heads/genspark/sync; then
  git checkout genspark/sync
else
  git checkout -b genspark/sync github/genspark/sync 2>/dev/null || \
  git checkout -b genspark/sync
fi

git stash pop 2>/dev/null || true

# 合并 github/main 最新（ours 策略，保留 genspark 修改）
git merge github/main --no-edit -X ours \
  -m "auto: merge github/main into genspark/sync $TODAY" 2>/dev/null || true

git add "$ARXIV_REPO/" 2>/dev/null || true
git add -A 2>/dev/null || true

if ! git diff --cached --quiet; then
  git commit -m "genspark: arXiv日报 $TODAY ${added}篇 → 20_Processing/20_KnowledgeBase/arxiv-auto"
  HASH=$(git rev-parse --short HEAD)
  echo "[$(date '+%H:%M:%S')] commit: $HASH" | tee -a "$LOG"
else
  HASH=$(git rev-parse --short HEAD)
  echo "[$(date '+%H:%M:%S')] 无新内容，跳过 commit ($HASH)" | tee -a "$LOG"
fi

# 推送 genspark/sync（永不推 main）
git push github genspark/sync 2>&1 | tee -a "$LOG"
PUSH_EXIT=${PIPESTATUS[0]}

# 切回 main
git checkout main 2>/dev/null || true

# ── 结果 ─────────────────────────────────────────────────────────────────
if [ $PUSH_EXIT -eq 0 ]; then
  touch "$DONE_FLAG"
  echo "[$(date '+%H:%M:%S')] === 全部完成 commit=$HASH ===" | tee -a "$LOG"
  exit 0
else
  echo "[$(date '+%H:%M:%S')] === 推送失败 exit=$PUSH_EXIT ===" | tee -a "$LOG"
  exit 1
fi
