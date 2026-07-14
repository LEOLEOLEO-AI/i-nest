with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

line108 = lines[107]
# Find all ^ on this line
for i, ch in enumerate(line108):
    if ch == "^":
        ctx = line108[max(0,i-20):i+20]
        print("^ at pos " + str(i) + ": [" + ctx + "]")

# Find double superscript pattern
import re
for m in re.finditer(r'\^[^a-zA-Z{]*\^', line108):
    ctx = line108[max(0,m.start()-20):m.end()+20]
    print("DOUBLE ^ : [" + ctx + "]")

# Also check for \^{...} which is a text accent (not superscript)
for m in re.finditer(r'\\\^', line108):
    ctx = line108[max(0,m.start()-20):m.end()+20]
    print("TEXT ACCENT \\^: [" + ctx + "]")
