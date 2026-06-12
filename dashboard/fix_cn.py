import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html", "r", encoding="utf-8") as f:
    c = f.read()

# Replace corrupted Chinese in renderDaily function
# Line with "最近 N 天"
c = c.replace('"\n\u6807\u8fd120 "+days.length+" \u5929"', '"\u6700\u8fd1 "+days.length+" \u5929"')
# Line with "\u6628\u5929" (versus date)
c = c.replace('"\n\u6807\u8fd112\u5929"', '"\u6628\u5929"')
# Line with "[\u8fdb\u5c55]"
c = c.replace('"\n\u6807\u8fd11\u8fdb\u5c55]"', '"[\u8fdb\u5c55]"')
# Error message "\u52a0\u8f7d\u5931\u8d25\uff0c\u8bf7\u5230\u65b0"
c = c.replace('"\n\u6807\u8fd11\u52a0\u8f7d\u5931\u8d25\uff0c\u8bf7\u5230\u65b0"', '"\u52a0\u8f7d\u5931\u8d25\uff0c\u8bf7\u5230\u65b0"')

with open(r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html", "w", encoding="utf-8", newline="") as f:
    f.write(c)

print("OK")
