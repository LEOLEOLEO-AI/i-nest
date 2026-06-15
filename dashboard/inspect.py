import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Print the renderDaily and adjacent lines to understand structure
for i in range(228, 273):
    print(f"{i+1}: {lines[i].rstrip()}")