import os, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')

vault = r'D:\Obsidian\home\work\.openclaw\workspace'
old_dirs = ['03_Topics', '10_Library', '10_Knowledge', '20_Ideas', 'papers']
archive = os.path.join(vault, '99_Archive')

deleted_stubs = 0
archived_real = 0

for od in old_dirs:
    src_path = os.path.join(vault, od)
    if not os.path.exists(src_path):
        continue
    
    for root, dirs, files in os.walk(src_path):
        for f in files:
            if not f.endswith('.md'):
                continue
            full = os.path.join(root, f)
            size = os.path.getsize(full)
            rel = os.path.relpath(full, vault)
            
            if size < 600:
                # Stub - delete
                os.remove(full)
                deleted_stubs += 1
            else:
                # Real file - move to archive preserving path
                rel_to_old = os.path.relpath(full, vault)
                dst = os.path.join(archive, rel_to_old)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.move(full, dst)
                archived_real += 1
                print('ARCHIVE: %s -> %s' % (rel, os.path.relpath(dst, vault)))

# Delete empty dirs bottom-up
for od in old_dirs:
    src_path = os.path.join(vault, od)
    if os.path.exists(src_path):
        for root, dirs, files in os.walk(src_path, topdown=False):
            try:
                if not os.listdir(root):
                    os.rmdir(root)
            except:
                pass

print('')
print('Deleted stubs: %d' % deleted_stubs)
print('Archived real: %d' % archived_real)

# Check if old dirs are gone
for od in old_dirs:
    path = os.path.join(vault, od)
    if os.path.exists(path):
        print('STILL EXISTS: %s' % od)
    else:
        print('GONE: %s' % od)
