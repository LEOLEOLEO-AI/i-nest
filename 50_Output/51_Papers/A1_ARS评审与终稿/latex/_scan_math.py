with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_BASELINE_FIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

import re

# Find ALL underscore characters NOT inside $...$ or \begin{equation}...\end{equation}
# This catches subscript in text mode
parts = re.split(r"(\$[^$]+\$|\\begin\{equation\}.*?\\end\{equation\})", tex, flags=re.DOTALL)
for i, part in enumerate(parts):
    if i % 2 == 0:  # text mode
        if "_" in part:
            # Find the context
            for m in re.finditer(r"_", part):
                pos_in_part = m.start()
                ctx = part[max(0,pos_in_part-30):pos_in_part+30].replace(chr(10), " ")
                print(f"UNDERSCORE in text: [{ctx}]")

# Also find ^ in text mode
for i, part in enumerate(parts):
    if i % 2 == 0:
        if "^" in part:
            for m in re.finditer(r"\^", part):
                pos_in_part = m.start()
                ctx = part[max(0,pos_in_part-30):pos_in_part+30].replace(chr(10), " ")
                print(f"CARET in text: [{ctx}]")

print("Scan complete")
