import os, json, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')

vault = r'D:\Obsidian\home\work\.openclaw\workspace'
with open(os.path.join(vault, '90_System/scripts/classify_llm.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

moved = 0
for rel, target_dir in data.items():
    if target_dir == 'SKIP':
        continue
    src = os.path.join(vault, rel)
    if not os.path.exists(src):
        continue
    fname = os.path.basename(rel)
    dst_dir = os.path.join(vault, target_dir)
    dst = os.path.join(dst_dir, fname)
    os.makedirs(dst_dir, exist_ok=True)
    
    if os.path.exists(dst):
        src_sz = os.path.getsize(src)
        dst_sz = os.path.getsize(dst)
        if src_sz > dst_sz:
            shutil.move(src, dst)
    else:
        shutil.move(src, dst)
    
    tdir_fwd = target_dir.replace('\\', '/')
    stub = '---\nmoved_to: \"' + tdir_fwd + '/' + fname + '\"\nmoved_date: 2026-07-03\n---\n\n> [Moved] -> [[' + tdir_fwd + '/' + fname + ']]'
    with open(src, 'w', encoding='utf-8') as fh:
        fh.write(stub)
    moved += 1
    print('%s -> %s' % (rel, target_dir))

print('Moved: %d' % moved)
