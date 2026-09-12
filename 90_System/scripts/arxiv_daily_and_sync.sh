#!/bin/bash
# arXiv 日报 + sync + 发QQ 全自动脚本 v6.0
# 存放：/home/work/scripts/arxiv_daily_and_sync.sh
# 完全不依赖 isolated agent，crontab 08:00 直接调用
# 爬取 → git push genspark/sync → openclaw message send 发QQ

TODAY=$(date '+%Y-%m-%d')
LOG="/tmp/arxiv_sync_${TODAY}.log"
DONE_FLAG="/tmp/arxiv_sync_${TODAY}.done"

ARXIV_SCRIPT="/home/work/.openclaw/workspace/scripts/arxiv_to_wiki.py"
REPO="/home/work/i-nest"
ARXIV_DIR="20_Processing/20_KnowledgeBase/arxiv-auto"
ARXIV_REPO="$REPO/$ARXIV_DIR"
QQ_TARGET="qqbot:c2c:C0E7CE3C0D30622B00A13113B1692B13"

if [ -f "$DONE_FLAG" ]; then
  echo "[$TODAY] 今日已完成，跳过"
  exit 0
fi

echo "[$(date '+%H:%M:%S')] === arXiv 日报 v6.0 START ===" | tee "$LOG"

# ── 步骤 1：爬取 ─────────────────────────────────────────────────────────
cd "$REPO"
git checkout main 2>/dev/null || true
mkdir -p "$ARXIV_REPO"
python3 "$ARXIV_SCRIPT" >> "$LOG" 2>&1
added=$(ls "$ARXIV_REPO"/*${TODAY}*.md 2>/dev/null | wc -l | tr -d ' ')
echo "[$(date '+%H:%M:%S')] 爬取完成，今日新增: $added 篇" | tee -a "$LOG"

# ── 步骤 2：main commit ──────────────────────────────────────────────────
git add "$ARXIV_DIR/" 2>/dev/null || true
if git diff --cached --quiet 2>/dev/null; then
  MAIN_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
  echo "[$(date '+%H:%M:%S')] 跳过 main commit ($MAIN_HASH)" | tee -a "$LOG"
else
  git commit -m "genspark: arXiv日报 $TODAY ${added}篇 → $ARXIV_DIR" 2>/dev/null || true
  MAIN_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
  echo "[$(date '+%H:%M:%S')] main commit: $MAIN_HASH" | tee -a "$LOG"
fi

# ── 步骤 3：推 genspark/sync ─────────────────────────────────────────────
git fetch github 2>/dev/null || true
if git show-ref --verify --quiet refs/heads/genspark/sync; then
  git checkout genspark/sync 2>/dev/null || true
else
  git checkout -b genspark/sync github/genspark/sync 2>/dev/null || \
  git checkout -b genspark/sync 2>/dev/null || true
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

# ── 步骤 4：发 QQ 摘要 ───────────────────────────────────────────────────
INDEX_FILE="$ARXIV_REPO/${TODAY}-index.md"
paper_count=$(grep -c '^\| [0-9]' "$INDEX_FILE" 2>/dev/null || echo "0")

if [ "$paper_count" -eq 0 ]; then
  MSG="📅 $TODAY 今日无新论文"
else
  SYNC_STATUS="✅ 已同步到 genspark/sync"
  if ! ([ $PUSH_EXIT -eq 0 ] || echo "$PUSH_OUT" | grep -q "Everything up-to-date"); then
    SYNC_STATUS="⚠️ 同步失败，查看 $LOG"
  fi

  # 先发汇总头条
  HEADER_MSG="📅 $TODAY arXiv日报 共${paper_count}篇
$SYNC_STATUS (commit: $HASH)"
  openclaw message send --channel qqbot -t "$QQ_TARGET" -m "$HEADER_MSG" >> "$LOG" 2>&1

  # 逐篇发送：题目 + 摘要前180字 + 链接
  idx=1
  for md_file in "$ARXIV_REPO/${TODAY}-"*.md; do
    [[ "$md_file" == *"-index.md" ]] && continue
    [ -f "$md_file" ] || continue

    # 提取题目
    title=$(grep '^title:' "$md_file" | head -1 | sed 's/^title: *"//;s/"$//')
    [ -z "$title" ] && title=$(basename "$md_file" .md)

    # 提取原始摘要（> 开头行）
    abstract=$(awk '/^## 原始摘要/{found=1; next} found && /^> /{sub(/^> /,""); print; exit}' "$md_file")
    abstract="${abstract:0:180}"

    # arxiv 链接
    arxiv_id=$(grep '^arxiv_id:' "$md_file" | head -1 | sed 's/^arxiv_id: *"//;s/"$//')
    link="https://arxiv.org/abs/${arxiv_id}"

    PAPER_MSG="[${idx}/${paper_count}] ${title}

摘要: ${abstract}...

🔗 ${link}"
    openclaw message send --channel qqbot -t "$QQ_TARGET" -m "$PAPER_MSG" >> "$LOG" 2>&1
    idx=$((idx+1))
    sleep 0.5
  done

  QQ_EXIT=$?
  echo "[$(date '+%H:%M:%S')] QQ逐篇发送完成 $((idx-1)) 篇" | tee -a "$LOG"
  MSG=""
fi

# 只有 MSG 非空才发（有论文时已逐篇发过，MSG已清空）
if [ -n "$MSG" ]; then
  openclaw message send \
    --channel qqbot \
    -t "$QQ_TARGET" \
    -m "$MSG" >> "$LOG" 2>&1
  QQ_EXIT=$?
else
  QQ_EXIT=0
fi
echo "[$(date '+%H:%M:%S')] QQ发送 exit=$QQ_EXIT" | tee -a "$LOG"

# ── 结束 ─────────────────────────────────────────────────────────────────
if ([ $PUSH_EXIT -eq 0 ] || echo "$PUSH_OUT" | grep -q "Everything up-to-date") && [ $QQ_EXIT -eq 0 ]; then
  touch "$DONE_FLAG"
  echo "[$(date '+%H:%M:%S')] === 成功完成 ===" | tee -a "$LOG"
else
  echo "[$(date '+%H:%M:%S')] === 完成（部分步骤失败，push=$PUSH_EXIT qq=$QQ_EXIT）===" | tee -a "$LOG"
  # 即使QQ发送失败也标记done，避免重复爬取
  touch "$DONE_FLAG"
fi
exit 0
