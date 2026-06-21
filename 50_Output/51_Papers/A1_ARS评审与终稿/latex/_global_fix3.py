import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\_BASELINE_A1_CST.tex", "r", encoding="utf-8") as f:
    tex = f.read()

print("Input: " + str(len(tex)) + " chars")
tex = tex.replace(r"\usepackage{fontspec}", "")
fixes = 0

# Fix 1: $X$_letter -> $X_letter$  
pat = re.compile(r'(\$[^$]+)\$(_[a-zA-Z])(?![a-zA-Z{])')
while pat.search(tex):
    tex, n = pat.subn(r'\1 \2$', tex)
    fixes += n
    if fixes > 500: break
print("1-letter subscripts: " + str(fixes))

# Fix 2: $X$_{Y} -> $X_{Y}$
n2 = 0
pat2 = re.compile(r'(\$[^$]+)\$(_\{[^}]+\})')
while pat2.search(tex):
    tex, n = pat2.subn(r'\1 \2$', tex)
    n2 += n
    if n2 > 500: break
print("_{...} subscripts: " + str(n2))
fixes += n2

# Fix 3: Clean up triple+ $
tex = re.sub(r'\$\$\$+', r'$$', tex)

# Fix 4: Short single-line $$X$$ -> $X$
def fix_dd(m):
    content = m.group(1)
    if len(content) < 200 and "\n" not in content:
        return "$" + content + "$"
    return m.group(0)
tex = re.sub(r'\$\$([^$]+?)\$\$', fix_dd, tex)
print("Short $$...$$ fixed")

# Fix 5: Specific \Gamma a_{st} patterns
tex = tex.replace("$\\Gamma$a$_{st}$", "$\\Gamma_{st}$")
tex = tex.replace("$\\Gamma$a$_\\{st\\}$", "$\\Gamma_{st}$")
tex = tex.replace("$\\Gamma$ a$_{st}$", "$\\Gamma_{st}$")

# Fix 6: Unicode
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
    "\u2208": "$\\in$", "\u2206": "$\\Delta$",
    "\u221a": "$\\sqrt{}$", "\u2020": "\\dag",
    "\u2074": "$^4$", "\u2075": "$^5$", "\u2076": "$^6$",
    "\u2077": "$^7$", "\u2079": "$^9$",
    "\u207b": "$^{-}$", "\u207f": "$^n$",
    "\u2081": "$_1$", "\u2082": "$_2$", "\u2083": "$_3$",
    "\u2085": "$_5$", "\u2093": "$_x$", "\u209b": "$_s$",
    "\u211d": "$\\mathbb{R}$", "\u2194": "$\\leftrightarrow$",
    "\u221d": "$\\propto$", "\u2245": "$\\cong$",
    "\u2713": "\\checkmark",
    "\u5218\u52e4\u8ba9": "Liu, Q.",
    "\u00e1": "\\\'{a}", "\u00e9": "\\\'{e}",
    "\u0151": "\\H{o}", "\u00b9": "$^1$",
}
for u, l in umap.items():
    tex = tex.replace(u, l)

# Check remaining Unicode
ru = set()
for c in tex:
    if ord(c) > 127 and ord(c) < 0x2000:
        ru.add(c)
print("Remaining Unicode: " + str(len(ru)))

# Count text-mode underscores
lines = tex.split("\n")
uc = 0
for line in lines:
    in_math = False
    j = 0
    while j < len(line):
        if line[j:j+2] == "\\$":
            j += 2
            continue
        if line[j] == "$":
            in_math = not in_math
            j += 1
            continue
        if line[j] == "_" and not in_math and (j == 0 or line[j-1] != "\\"):
            uc += 1
            if uc <= 10:
                ctx = line[max(0,j-30):j+30]
                print("  TXT_: [" + ctx + "]")
        j += 1
print("Text-mode underscores: " + str(uc))

# Cleanup
tex = re.sub(r"\n{3,}", "\n\n", tex)

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_FULLFIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Output: " + str(len(tex)) + " chars, fixes: " + str(fixes))
