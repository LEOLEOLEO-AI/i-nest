with open(r'D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html', 'r', encoding='utf-8') as f:
    ls = f.readlines()

# Remove extra } at line 406 (0-based 405)
new_ls = ls[:405] + ls[406:]

with open(r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html", "w", encoding="utf-8", newline="") as f:
    f.write(''.join(new_ls))

print('OK')