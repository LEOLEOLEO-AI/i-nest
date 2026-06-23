with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

import re
line = lines[155]
# Find ALL \commands
for m in re.finditer(r'\\([a-zA-Z@]+)', line):
    cmd = m.group(1)
    ctx_start = max(0, m.start()-10)
    ctx_end = min(len(line), m.end()+20)
    print("\\" + cmd + ": [" + line[ctx_start:ctx_end] + "]")
