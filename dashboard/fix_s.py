with open(r'D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('\u8bf7\u5230\u65b0', '\u8bf7\u5237\u65b0')

with open(r'D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html', 'w', encoding='utf-8', newline='') as f:
    f.write(c)

print('OK')
