with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Fix specific broken pattern: $\gamma$*_{}$ → $\gamma^*_{CST}$
# This was mangled by a previous fix
import re

# Pattern: $\gamma$*_{}$ followed by newline or after
# The original was: ($\gamma$*_{CST} = 0.486)
tex = tex.replace("$\\gamma$*_{}$\n", "$\\gamma^*_{\\text{CST}}$ = 0.486)\n")

# Also handle similar pattern with different context  
tex = tex.replace("$\\gamma$*_{}$ ", "$\\gamma^*_{\\text{CST}}$ = 0.486) ")

# Find any other empty subscripts _{}$
pat = re.compile(r'_\{}\$')
count = len(pat.findall(tex))
tex = pat.sub(r'_\{CST}\$', tex)  # assume all empty subscripts are CST
print("Fixed empty subscripts: " + str(count))

# Also fix $\gamma_{_geo}$ → $\gamma_{\text{geo}}$ (double subscript)
tex = tex.replace("\\gamma_{_geo}", "\\gamma_{\\text{geo}}")
tex = tex.replace("\\gamma\\_{_geo}", "\\gamma_{\\text{geo}}")

# Fix $\gamma$_{CST} → $\gamma_{CST}$ (subscript outside math)
tex = re.sub(r'\$\\gamma\$\s*_\{CST\}', r'$\gamma_{CST}$', tex)

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Saved: " + str(len(tex)))
