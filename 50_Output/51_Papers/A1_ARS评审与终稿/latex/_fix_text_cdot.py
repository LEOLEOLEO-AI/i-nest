with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Fix: CST = (Sc \cdot Tc) \cdot exp(...) in text mode
# Wrap the entire mathematical expression in $...$
tex = tex.replace(
    "CST = (Sc  \\cdot  Tc)  \\cdot  exp($\\alpha$  \\cdot  $\\Gamma_{st}$)",
    "$CST = (S_c \\cdot T_c) \\cdot \\exp(\\alpha \\cdot \\Gamma_{st})$"
)

# Also fix similar patterns
tex = tex.replace("(Sc  \\cdot  Tc)", "$(S_c \\cdot T_c)$")
tex = tex.replace("Sc  \\cdot  Tc", "$S_c \\cdot T_c$")

# Fix any remaining isolated \cdot in text mode
# Find all \cdot NOT inside $...$ and wrap
import re
parts = re.split(r'(\$[^$]+\$)', tex)
for i in range(0, len(parts), 2):  # text mode parts only
    if '\\cdot' in parts[i]:
        # Wrap \cdot in $...$
        parts[i] = parts[i].replace('\\cdot', '$\\cdot$')

tex = ''.join(parts)

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Fixed text-mode \\cdot: " + str(len(tex)))
