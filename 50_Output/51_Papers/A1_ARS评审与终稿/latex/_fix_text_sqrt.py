with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

import re

# Fix text-mode \sqrt, \phi, \pi, \delta, etc. in the "Level" descriptions
# These appear in patterns like: Level I (1/\sqrt{2} \& 1):
# Need: Level I ($1/\sqrt{2}$ \& 1):

# Wrap unescaped \sqrt{...} in text mode with $...$
# But need to be careful about context - these are the ONLY text-mode sqrts
# All equation-sqrts are already in math mode

# Pattern: (1/\sqrt{2} → ($1/\sqrt{2}$
tex = tex.replace("(1/\\sqrt{2}", "($1/\\sqrt{2}$")

# Pattern: (\phi - → ($\phi$ -  
tex = tex.replace("(\\phi -", "($\\phi$ -")

# Pattern: (e): → $(e)$:  -- actually e is just 'e' in text, fine
# But: \& should be \& -- it's already escaped

# Pattern: (\pi): → ($\pi$):
tex = tex.replace("(\\pi):", "($\\pi$):")

# Pattern: (\delta - → ($\delta$ -
tex = tex.replace("(\\delta -", "($\\delta$ -")

# Also fix in other contexts
tex = tex.replace(" 1/\\sqrt{2} ", " $1/\\sqrt{2}$ ")
tex = tex.replace(" \\phi ", " $\\phi$ ")
tex = tex.replace(" \\pi ", " $\\pi$ ")
tex = tex.replace(" \\delta ", " $\\delta$ ")

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Saved")
