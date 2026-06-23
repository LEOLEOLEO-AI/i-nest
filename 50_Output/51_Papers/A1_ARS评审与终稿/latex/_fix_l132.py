with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Fix all text-mode math in Level descriptions
tex = tex.replace("(1/\\sqrt{2} \\& 1)", "($1/\\sqrt{2}$ \\& 1)")
tex = tex.replace("(1/\\sqrt{2} \\& 1):", "($1/\\sqrt{2}$ \\& 1):")
tex = tex.replace("(1/\\sqrt{2}", "($1/\\sqrt{2}$")

# Fix \phi, \pi, \delta, e in text mode 
tex = tex.replace("(\\phi -", "($\\phi$ -")
tex = tex.replace("(e):", "(e):")  # e is just a letter
tex = tex.replace("(\\pi:", "($\\pi$:")
tex = tex.replace("(\\delta -", "($\\delta$ -")

# Also fix Level descriptions with bare Greek
tex = tex.replace(" \\phi ", " $\\phi$ ")
tex = tex.replace(" \\pi ", " $\\pi$ ")
tex = tex.replace(" \\delta ", " $\\delta$ ")

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Fixed L132+ Greek chars: " + str(len(tex)))
