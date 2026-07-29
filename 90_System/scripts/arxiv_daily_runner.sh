#!/bin/bash
# arXiv 日报触发器 v1.0
# cron 调用此脚本后立即返回，真正任务在后台跑
# 结果写入 LOG，完成后通过 QQ 通知

TODAY=$(date '+%Y-%m-%d')
LOG="/tmp/arxiv_daily_${TODAY}.log"
SCRIPT="/vault/scripts/arxiv_to_wiki.py"
REPO="/home/work/i-nest"
WORKSPACE="/vault"

# 如果今天已经跑过，跳过（防止重复触发）
if [ -f "/tmp/arxiv_daily_${TODAY}.done" ]; then
  echo "今日已完成，跳过" && exit 0
fi

# 后台启动完整任务
nohup bash -c "
set -e
echo '[\$(date +%H:%M:%S)] arXiv 日报开始' >> $LOG

# 1. 爬取 + gsk 分析
python3 $SCRIPT >> $LOG 2>&1
PAPERS=\$(grep '✅ 完成' $LOG | tail -1 | grep -oE '[0-9]+' | head -1)
echo '[\$(date +%H:%M:%S)] 爬取完成：\${PAPERS:-0}篇' >> $LOG

# 2. 复制到 i-nest
rsync -a --include='*.md' --exclude='*' \
  $WORKSPACE/00_KnowledgeBase_知识库/literature/arxiv-auto/ \
  $REPO/00_KnowledgeBase/literature/arxiv-auto/ 2>>$LOG || true

# 3. git commit + push genspark/sync
cd $REPO
git add -A 2>>$LOG
if ! git diff --cached --quiet; then
  git stash 2>/dev/null || true
  git checkout genspark/sync 2>>$LOG
  git stash pop 2>/dev/null || true
  git merge main --no-edit -X ours 2>/dev/null || true
  git add -A 2>>$LOG
  git commit -m 'genspark: arXiv日报 $TODAY' 2>>$LOG
  git push github genspark/sync 2>>$LOG
  git checkout main 2>>$LOG
  HASH=\$(git rev-parse --short github/genspark/sync)
  echo '[\$(date +%H:%M:%S)] 推送完成：\$HASH' >> $LOG
else
  echo '[\$(date +%H:%M:%S)] 无新内容，跳过推送' >> $LOG
fi

touch /tmp/arxiv_daily_$TODAY.done
echo '[\$(date +%H:%M:%S)] 全部完成' >> $LOG
" >> $LOG 2>&1 &

echo "arXiv 日报已后台启动 (PID=$!), 日志: $LOG"
exit 0
