import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Count functions as sanity check
for i, l in enumerate(lines):
    if 'function render' in l or 'function resolvePath' in l or 'function openDetail' in l:
        print(f"{i+1}: {l.rstrip()}")