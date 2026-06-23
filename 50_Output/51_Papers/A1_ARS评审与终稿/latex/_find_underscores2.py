import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_CLEAN.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Find all unescaped underscores and show context + whether they're inside $
lines = tex.split("\n")
for i, line in enumerate(lines):
    in_math = False
    j = 0
    while j < len(line):
        if line[j:j+2] == "\\$":
            j += 2
            continue
        if line[j] == "$":
            in_math = not in_math
            j += 1
            continue
        if line[j] == "_" and not in_math and (j == 0 or line[j-1] != "\\"):
            # Found underscore in text mode
            ctx = line[max(0,j-30):j+30]
            print(f"L{i+1}:{j}: [{ctx}]")
        j += 1

print("Done")
