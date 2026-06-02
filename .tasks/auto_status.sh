#!/bin/bash
# Auto-status: runs every 5 minutes, logs state changes
TRACK=/home/work/.openclaw/workspace/.tasks/active.json
LOG=/home/work/.openclaw/workspace/.tasks/status_log.txt
TMP=$(mktemp)

# Gather status
echo $(date +%Y-%m-%d\/%H:%M) > $TMP
ps aux | grep -E 'python.*sdi|python.*hemibrain' | grep -v grep | wc -l | xargs echo 'compute_procs:' >> $TMP
ls -t /home/work/.openclaw/workspace/sdi_sim/*.json 2>/dev/null | head -3 | while read f; do
    echo $(basename $f):$(stat -c%s $f) >> $TMP
done

# Compare with last
if [ -f $LOG ]; then
    if ! diff $LOG $TMP > /dev/null 2>&1; then
        echo CHANGED >> $TMP
    fi
fi
mv $TMP $LOG
