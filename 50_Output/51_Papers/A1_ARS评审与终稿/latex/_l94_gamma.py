with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

line94 = lines[93]
# Find the problem area
import re
# Search for gamma CST pattern
idx = line94.find("gamma")
while idx >= 0:
    ctx = line94[max(0,idx-20):idx+80]
    print("Found gamma: [" + ctx + "]")
    idx = line94.find("gamma", idx+1)

# Also search for _{CST
for m in re.finditer(r'_\{?[A-Z]', line94):
    ctx = line94[m.start()-10:m.end()+40]
    print("Found subscript: [" + ctx + "]")
