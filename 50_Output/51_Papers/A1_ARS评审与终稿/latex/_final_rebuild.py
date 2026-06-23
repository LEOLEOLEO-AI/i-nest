import re

# Rebuild from baseline with ALL proven fixes in one shot
with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\_BASELINE_A1_CST.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# 1. Remove fontspec
tex = tex.replace(r"\usepackage{fontspec}", "")

# 2. Unicode mapping
umap = {
    "\u03b1": "$\\alpha$", "\u03b2": "$\\beta$", "\u03b3": "$\\gamma$",
    "\u03b4": "$\\delta$", "\u03b5": "$\\epsilon$", "\u03b7": "$\\eta$",
    "\u03b8": "$\\theta$", "\u03bb": "$\\lambda$", "\u03bc": "$\\mu$",
    "\u03bd": "$\\nu$", "\u03c0": "$\\pi$", "\u03c1": "$\\rho$",
    "\u03c3": "$\\sigma$", "\u03c6": "$\\phi$",
    "\u03a6": "$\\Phi$", "\u03a8": "$\\Psi$", "\u0393": "$\\Gamma$",
    "\u0398": "$\\Theta$", "\u0394": "$\\Delta$",
    "\u00d7": "$\\times$", "\u00b7": "$\\cdot$",
    "\u2014": "---", "\u2013": "--",
    "\u2018": "'", "\u2019": "'", "\u201c": "``", "\u201d": "''",
    "\u00b1": "$\\pm$", "\u00b2": "$^2$", "\u00b3": "$^3$",
    "\u00a7": "\\S{}", "\u00b0": "$^\\circ$",
    "\u2264": "$\\leq$", "\u2265": "$\\geq$",
    "\u2248": "$\\approx$", "\u223c": "$\\sim$",
    "\u2212": "--", "\u2192": "$\\rightarrow$",
    "\u2208": "$\\in$", "\u2206": "$\\Delta$", "\u221a": "$\\sqrt{}$",
    "\u2020": "\\dag", "\u2074": "$^4$", "\u2075": "$^5$", "\u2076": "$^6$",
    "\u2077": "$^7$", "\u2079": "$^9$", "\u207b": "$^{-}$", "\u207f": "$^n$",
    "\u2081": "$_1$", "\u2082": "$_2$", "\u2083": "$_3$",
    "\u2085": "$_5$", "\u2093": "$_x$", "\u209b": "$_s$",
    "\u211d": "$\\mathbb{R}$", "\u2194": "$\\leftrightarrow$",
    "\u221d": "$\\propto$", "\u2245": "$\\cong$", "\u2713": "\\checkmark",
    "\u5218\u52e4\u8ba9": "Liu, Q.",
    "\u00e1": "\\\'{a}", "\u00e9": "\\\'{e}", "\u0151": "\\H{o}", "\u00b9": "$^1$",
}
for u, l in umap.items():
    tex = tex.replace(u, l)

# 3. Multi-letter subscripts: $X$_word → $X_{word}$
pat = re.compile(r'\$([^$]+)\$(_[a-zA-Z]+)')
n = 0
while pat.search(tex):
    tex, cnt = pat.subn(r'$\1_{\2}$', tex)
    n += cnt
    if n > 500: break
print("Subscripts: " + str(n))

# 4. Remove ALL stray $$
tex = tex.replace("$$", "")

# 5. Fix \dagGen, \dagNMH
tex = tex.replace("\\dagGen", "\\dag{}Gen")
tex = tex.replace("\\dagNMH", "\\dag{}NMH")

# 6. Fix \Gammast in equations ($ stripped)
# \Gammast → \Gamma_{st}
tex = tex.replace("\\Gammast", "\\Gamma_{st}")

# 7. Fix $\Gamma$st in text → $\Gamma_{st}$
pat2 = re.compile(r'\$(\\Gamma)\$([a-zA-Z]+)')
n2 = 0
while pat2.search(tex):
    tex, cnt = pat2.subn(r'$\1_{\2}$', tex)
    n2 += cnt
    if n2 > 200: break
print("Gamma_st: " + str(n2))

# 8. Fix escaped underscore: $X$\_word → $X_{word}$
pat3 = re.compile(r'\$([^$]+)\$\\_([a-zA-Z]+)')
n3 = 0  
while pat3.search(tex):
    tex, cnt = pat3.subn(r'$\1_{\2}$', tex)
    n3 += cnt
    if n3 > 200: break
print("Escaped _: " + str(n3))

# 9. Fix scattered math commands (ONLY in text mode, NOT in equations!)
# Find $X$\cmd$Y$ → $X \cmd Y$
for cmd in ['\\\\cdot', '\\\\approx', '\\\\neq', '\\\\times', '\\\\sim', 
            '\\\\geq', '\\\\leq', '\\\\in', '\\\\pm']:
    pat = re.compile(r'\$([^$]+)\$\s*(' + cmd + r')\s*\$([^$]+)\$')
    cnt = 0
    while pat.search(tex):
        tex, c = pat.subn(lambda m, c2=cmd: '$' + m.group(1) + ' ' + c2 + ' ' + m.group(3) + '$', tex)
        cnt += c
        if cnt > 100: break
    if cnt > 0:
        print("Scattered " + cmd + ": " + str(cnt))

# 10. Fix \text{norm$ → \text{norm}$
tex = tex.replace("\\text{norm$", "\\text{norm}$")

# Fix $^{-}^N → $^{-N}$
tex = tex.replace("$^{-}^6$", "$^{-6}$")
tex = tex.replace("$^{-}^7$", "$^{-7}$")

# Delete empty lines in equation envs
# (simplified: just compile and see)

# Count $
total = sum(line.count("$") - line.count("\\$") for line in tex.split("\n"))
print("Total $: " + str(total) + " (" + ("OK" if total % 2 == 0 else "UNBALANCED") + ")")

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("REBUILT: " + str(len(tex)) + " chars")
