with open(r'D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('resolvePath(linky{', 'resolvePath(link){')

with open(r'D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html', 'w', encoding='utf-8', newline='') as f:
    f.write(c)

print('OK')
