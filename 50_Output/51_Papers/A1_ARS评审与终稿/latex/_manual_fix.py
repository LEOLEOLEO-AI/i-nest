with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Manual fix: replace the mangled pattern with correct LaTeX
# Original was: ($\gamma$*_{CST} = 0.486)
# Now is: ($\gamma$*_{}$
# Should be: ($\gamma^*_{\text{CST}} = 0.486)$
tex = tex.replace(
    "($\\gamma$*_{}$\n\n\nThe critical coefficient",
    "($\\gamma^*_{\\text{CST}} = 0.486)$\n\n\nThe critical coefficient"
)

# Fix other empty subscript patterns
tex = tex.replace("_{}$\n", "_{\\text{CST}}$\n")

# Count remaining empty subscripts
import re
remaining = len(re.findall(r'_\{}\$', tex))
print("Remaining empty subscripts: " + str(remaining))

# Fix: \text{norm$ -> \text{norm}$
tex = tex.replace("\\text{norm$", "\\text{norm}$")

# Fix: T$_{species}$ → $T_{\text{species}}$
tex = re.sub(r'T\$_\{species\}\$', r'$T_{\text{species}}$', tex)
tex = re.sub(r'CS\$T_\{emergent\}\$', r'$CST_{\text{emergent}}$', tex)
tex = re.sub(r'CS\$T_\{func\}\$', r'$CST_{\text{func}}$', tex)

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Saved: " + str(len(tex)))
