import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\_BASELINE_A1_CST.tex", "r", encoding="utf-8") as f:
    tex = f.read()

tex = tex.replace(r"\usepackage{fontspec}", "")

fixes = []

# Pattern: $X$_<word>$ → $X_{<word>}$
# E.g.: $\alpha$_digital → $\alpha_{digital}$
# The _<word> is in text mode, merge it into math block
# Handle: _<word> (multi-letter with no braces)  
pat_ml = re.compile(r'(\$[^$]+)\$(_[a-zA-Z]+)(?=\s|\$|[,.;:\)\]])')
n = 0
while pat_ml.search(tex):
    tex, cnt = pat_ml.subn(r'\1_{\2}$', tex)
    n += cnt
    if n > 500: break
fixes.append(("multi-letter subscripts", n))

# Pattern: $X$_{Y} → $X_{Y}$ (braced subscript merged)
pat_br = re.compile(r'(\$[^$]+)\$(_\{[^}]+\})')
n = 0
while pat_br.search(tex):
    tex, cnt = pat_br.subn(r'\1 \2$', tex)
    n += cnt
    if n > 500: break
fixes.append(("braced subscripts", n))

# Pattern: $X$_Y$$ → $X_Y$ (subscript then double dollar)
# Double dollar removed by treating _Y as part of math
# Already handled by pat_ml since $$ ends with $

# Pattern: Remove extra $$ after math blocks
# $$ that follows immediately after $...$ should be collapsed
tex = re.sub(r'(\$[^$]+\$)\$\$', r'\1', tex)
# Count
dd_after = len(re.findall(r'\$\$', tex))
fixes.append(("double-dollar cleanup", dd_after))

# Pattern: $X$_<letter>$Y$ → $X_letter Y$ (subscript between math blocks)
pat_between = re.compile(r'(\$[^$]+)\$(_[a-zA-Z]+)\$([^$]*)\$')
n = 0
while pat_between.search(tex):
    tex, cnt = pat_between.subn(r'\1_{\2} \3$', tex)
    n += cnt
    if n > 500: break
fixes.append(("between-math subscripts", n))

# Fix: \Gamm → \Gamma  
n = tex.count(r"\Gamm")
tex = tex.replace(r"\Gamm", r"\Gamma")
# But \Gamm is also substring of \Gamma, so check for standalone
# Actually just do it - the original has proper \Gamma

# Unicode mapping (comprehensive)
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
    "\u2020": "\\dag",
    "\u2074": "$^4$", "\u2075": "$^5$", "\u2076": "$^6$",
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

# Count remaining $ imbalance
total = sum(line.count("$") - line.count("\\$") for line in tex.split("\n"))
print("Fixes: " + ", ".join(["{}:{}".format(name, cnt) for name, cnt in fixes]))
print("Total $: " + str(total) + " (" + ("even=OK" if total % 2 == 0 else "ODD=UNBALANCED") + ")")

# Check remaining text-mode underscores
lines = tex.split("\n")
uc = 0
for line in lines:
    in_math = False
    in_equation = False
    j = 0
    while j < len(line):
        if line[j:j+2] == "\\$":
            j += 2
            continue
        if line[j] == "$":
            in_math = not in_math
        elif line.startswith("\\begin{equation}", j) or line.startswith("\\begin{align}", j):
            in_equation = True
        elif line.startswith("\\end{equation}", j) or line.startswith("\\end{align}", j):
            in_equation = False
        
        if line[j] == "_" and not in_math and not in_equation and (j == 0 or line[j-1] != "\\"):
            uc += 1
            if uc <= 8:
                ctx = line[max(0,j-25):j+25]
                print("  TXT_: [" + ctx + "]")
        j += 1
print("Text-mode underscores: " + str(uc))

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_TRY.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Output: " + str(len(tex)) + " chars")
