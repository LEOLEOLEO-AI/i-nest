with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Show FULL line 150
line = lines[149]
print("L150 FULL:")
print(line)
print()
# Scan for ALL _
import re
for m in re.finditer(r'_', line):
    ctx = line[max(0,m.start()-15):m.end()+15]
    print("_ at " + str(m.start()) + ": [" + ctx + "]")
# Scan for ALL ^
for m in re.finditer(r'\^', line):
    ctx = line[max(0,m.start()-15):m.end()+15]
    print("^ at " + str(m.start()) + ": [" + ctx + "]")
# Scan for ALL \ in text  
parts = re.split(r'(\$[^$]+\$)', line)
for i in range(0, len(parts), 2):
    for m in re.finditer(r'\\([a-zA-Z]+)', parts[i]):
        print("CMD " + m.group(1) + " in text at " + str(m.start()) + " (part " + str(i) + ")")
