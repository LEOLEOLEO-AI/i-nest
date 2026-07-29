import os, json, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')

vault = r'D:\Obsidian\vault'

with open(os.path.join(vault, '90_System/scripts/classify_clear.json'), 'r', encoding='utf-8') as f:
    to_move = json.load(f)

moved = 0
conflicts = 0

for rel, target_dir in to_move:
    src = os.path.join(vault, rel)
    fname = os.path.basename(rel)
    dst_dir = os.path.join(vault, target_dir)
    dst = os.path.join(dst_dir, fname)
    
    if not os.path.exists(src):
        continue
    
    os.makedirs(dst_dir, exist_ok=True)
    
    # Handle target conflict
    if os.path.exists(dst):
        src_size = os.path.getsize(src)
        dst_size = os.path.getsize(dst)
        if src_size > dst_size:
            # Source is larger, replace target but keep backup
            shutil.move(dst, dst + '.bak')
            shutil.move(src, dst)
        else:
            # Target is larger/better, just stub source
            pass
        conflicts += 1
    else:
        shutil.move(src, dst)
    
    # Create redirect stub
    stub = '---\nmoved_to: "' + target_dir.replace('\\','/') + '/' + fname + '"\nmoved_date: 2026-07-03\n---\n\n> [Moved] -> [[' + target_dir.replace('\\','/') + '/' + fname + ']]'
    os.makedirs(os.path.dirname(src), exist_ok=True)
    with open(src, 'w', encoding='utf-8') as fh:
        fh.write(stub)
    moved += 1

print('Moved: %d files, Conflicts: %d' % (moved, conflicts))
