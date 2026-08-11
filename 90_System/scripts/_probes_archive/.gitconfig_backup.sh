#!/bin/bash
# Auto-backup critical files before every git push
CRITICAL_FILES=(
    SOUL.md USER.md MEMORY.md IDENTITY.md HEARTBEAT.md
    KB/01_Atlas_SDSoW-NCC/iNEST_Academic_Belief_Core.md
    NCC计算范式/
    memory/
)

BACKUP_DIR=/tmp/auto_backup_$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

echo -n > $BACKUP_DIR/changed_files.txt
for f in /vault/SOUL.md /vault/USER.md /vault/MEMORY.md /vault/IDENTITY.md /vault/HEARTBEAT.md; do
    if [ -f $f ]; then
        dir=$BACKUP_DIR/$(dirname $f)
        mkdir -p $dir
        cp -f $f $dir/
        echo $(basename $f) >> $BACKUP_DIR/changed_files.txt
    fi
done

# Commit all changes before pushing
cd /vault
git add -A
git commit -m 'auto-backup sync: '$(date +%Y-%m-%d_%H:%M) 2>/dev/null

echo PRE_PUSH_BACKUP: $(cat $BACKUP_DIR/changed_files.txt | wc -l) files saved to $BACKUP_DIR
