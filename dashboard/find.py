import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html", "r", encoding="utf-8") as f:
    c = f.read()

# FIND boundaries
fnstart = c.find('function renderDaily(){')
kanstart = c.find('function renderKanban(){')
rstart = c.find('function resolvePath(link){')
rend = c.find('function openDetail(id){')

print(f"renderDaily: {fnstart}, renderKanban: {kanstart}")
print(f"resolvePath: {rstart}, openDetail: {rend}")
