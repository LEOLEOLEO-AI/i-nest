with open(r'D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find the exact line with 贽失败
import re
m = re.search(r'\u8bf7\u5230.*', c)
if m:
    print(repr(m.group()))
else:
    print('NOT FOUND')
