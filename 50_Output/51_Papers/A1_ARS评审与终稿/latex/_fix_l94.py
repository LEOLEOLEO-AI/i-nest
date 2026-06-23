with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Fix L94 specific issues
# 1. $\gamma$  \approx  0.5 → $\gamma \approx 0.5$
tex = tex.replace("$\\gamma$  \\approx  0.5", "$\\gamma \\approx 0.5$")

# 2. $\gamma$*_{CST}$$ = 0.486 → $\gamma^*_{\text{CST}} = 0.486$
tex = tex.replace("$\\gamma$*_{CST}$$ = 0.486", "$\\gamma^*_{\\text{CST}} = 0.486$")

# 3. Also fix any remaining $$
tex = tex.replace("$$", "")

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Fixed L94: " + str(len(tex)))
