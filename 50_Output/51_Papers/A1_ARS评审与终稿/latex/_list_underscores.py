import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_CLEAN.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Show ALL remaining text-mode underscores with context
parts = re.split(r"(\$[^$]+\$|\\begin\{equation\}.*?\\end\{equation\})", tex, flags=re.DOTALL)
count = 0
for i, part in enumerate(parts):
    if i % 2 == 0:
        for m in re.finditer(r"[^\\]_", part):
            count += 1
            ctx = part[max(0,m.start()-40):m.end()+40].replace(chr(10), " ")
            if count <= 30:
                print(f"[{count}] ...{ctx}...")

print(f"\nTotal: {count}")
