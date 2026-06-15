with open(r'D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html', 'r', encoding='utf-8') as f:
    ls = f.readlines()

# Print around lines 399-410 (1-based)
for i in range(398, 410):
    print(f'{i+1}: {ls[i].rstrip()}')