import re

c = open(r'D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html', 'r', encoding='utf-8').read()
links = re.findall(r'"link": "([^"]+)"', c)
for l in links:
    print(l)