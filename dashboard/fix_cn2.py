import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html", "r", encoding="utf-8") as f:
    c = f.read()

# Fix the corrupted "\u8bf7\u5230\u65b0" -> should be "\u8bf7\u5230\u65b0" (shuaxin, not daoxin)
c = c.replace('\u8bf7\u5230\u65b0', '\u8bf7\u5230\u65b0')

with open(r'D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html', 'w', encoding='utf-8', newline='') as f:
    f.write(c)

print('OK')
