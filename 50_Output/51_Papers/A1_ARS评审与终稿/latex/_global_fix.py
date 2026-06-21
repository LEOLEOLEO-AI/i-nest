import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\_BASELINE_A1_CST.tex", "r", encoding="utf-8") as f:
    tex = f.read()

print(f"Input: {len(tex)} chars")

# Step 0: Remove fontspec
tex = tex.replace(r"\usepackage{fontspec}", "")

fixes = 0

# Step 1: Fix $X$_Y$Z$ → $X_Y Z$ (subscript between math blocks)
# Pattern: $<content>$ followed by _<subscript> then optionally $<more>$
# We need to merge _<subscript> into the preceding math block
pat1 = re.compile(r'(\$[^$]+)\$(_\{[^}]+\})\$([^$]*)\$')
n1 = 0
while pat1.search(tex):
    tex, n = pat1.subn(r'\1 \2 \3$', tex)
    n1 += n
    if n1 > 500: break
print(f"Fix1 ($X$_Y$Z$ -> $X_Y Z$): {n1}")
fixes += n1

# Step 1b: $X$_Y (without following $) → $X_Y$
pat1b = re.compile(r'(\$[^$]+)\$(_\{[^}]+\})')
n1b = 0
while pat1b.search(tex):
    tex, n = pat1b.subn(r'\1 \2$', tex)
    n1b += n
    if n1b > 500: break
print(f"Fix1b ($X$_Y -> $X_Y$): {n1b}")
fixes += n1b

# Step 1c: $X$_letter → $X_letter$ (single letter subscript, no braces)
# E.g., $\eta$_I → $\eta_I$
pat1c = re.compile(r'(\$[^$]+)\$(_[a-zA-Z])(?![a-zA-Z{])')
n1c = 0
while pat1c.search(tex):
    tex, n = pat1c.subn(r'\1 \2$', tex)
    n1c += n
    if n1c > 500: break
print(f"Fix1c ($X$_L -> $X_L$): {n1c}")
fixes += n1c

# Step 2: Fix $$...$$ (display math that should be inline)
# $$R_{sw}$$ → $R_{sw}$
pat2 = re.compile(r'\$\$([^$]+)\$\$')
n2 = len(pat2.findall(tex))
tex = pat2.sub(r'$\1$', tex)
print(f"Fix2 ($$...$$ -> $...$): {n2}")
fixes += n2

# Step 3: Fix \Gamm → \Gamma (Gamma truncation)
n3 = tex.count(r"\Gamm")
tex = tex.replace(r"\Gamm", r"\Gamma")
print(f"Fix3 (\\Gamm -> \\Gamma): {n3}")
fixes += n3

# Step 4: Fix $\Gamma$a$_{st}$ → $\Gamma_{st}$ (scattered Gamma)
pat4 = re.compile(r'\$\\Gamma\$a\$_\{st\}\$')
n4 = len(pat4.findall(tex))
tex = pat4.sub(r'$\Gamma_{st}$', tex)
print(f"Fix4 (Gamma scattered): {n4}")
fixes += n4

# Step 5: Fix $\Gamm$a_{st}$$ → $\Gamma_{st}$
pat5 = re.compile(r'\$\\Gamma\$a_\{st\}\$')
n5 = len(pat5.findall(tex))
if n5 == 0:
    pat5 = re.compile(r'\$\\Gamma a_\{st\}\$')
    n5 = len(pat5.findall(tex))
pat5b = re.compile(r'\$\\Gamma\$a_\{st\}\$\$')
n5b = len(pat5b.findall(tex))
tex = pat5.sub(r'$\Gamma_{st}$', tex)
tex = pat5b.sub(r'$\Gamma_{st}$', tex)
print(f"Fix5 (Gamma a_st): {n5}+{n5b}")
fixes += n5 + n5b

# Step 6: Merge remaining adjacent math blocks $...$$...$ → $... ...$
pat6 = re.compile(r'(\$[^$]+\$)\s*(\$[^$]+\$)')
n6 = 0
while pat6.search(tex):
    tex, n = pat6.subn(lambda m: '$' + m.group(1)[1:-1] + ' ' + m.group(2)[1:-1] + '$', tex)
    n6 += n
    if n6 > 200: break
print(f"Fix6 (adjacent $...$$...$ merge): {n6}")
fixes += n6

# Step 7: Unicode mapping
unicode_map = {
    "\u03b1": r"$\alpha$", "\u03b2": r"$\beta$", "\u03b3": r"$\gamma$",
    "\u03b4": r"$\delta$", "\u03b5": r"$\epsilon$", "\u03b7": r"$\eta$",
    "\u03b8": r"$\theta$", "\u03bb": r"$\lambda$", "\u03bc": r"$\mu$",
    "\u03bd": r"$\nu$", "\u03c0": r"$\pi$", "\u03c1": r"$\rho$",
    "\u03c3": r"$\sigma$", "\u03c6": r"$\phi$",
    "\u03a6": r"$\Phi$", "\u03a8": r"$\Psi$", "\u0393": r"$\Gamma$",
    "\u0398": r"$\Theta$", "\u0394": r"$\Delta$",
    "\u00d7": r"$\times$", "\u00b7": r"$\cdot$",
    "\u2014": "---", "\u2013": "--",
    "\u2018": "'", "\u2019": "'",
    "\u201c": "``", "\u201d": "''",
    "\u00b1": r"$\pm$", "\u00b2": r"$^2$", "\u00b3": r"$^3$",
    "\u00a7": r"\S{}", "\u00b0": r"$^\circ$",
    "\u2264": r"$\leq$", "\u2265": r"$\geq$",
    "\u2248": r"$\approx$", "\u223c": r"$\sim$",
    "\u2212": r"--", "\u2192": r"$\rightarrow$",
    "\u2208": r"$\in$", "\u2206": r"$\Delta$",
    "\u221a": r"$\sqrt{}$", "\u2020": r"\dag",
    "\u2074": r"$^4$", "\u2075": r"$^5$", "\u2076": r"$^6$",
    "\u2077": r"$^7$", "\u2079": r"$^9$",
    "\u207b": r"$^{-}$", "\u207f": r"$^n$",
    "\u2081": r"$_1$", "\u2082": r"$_2$", "\u2083": r"$_3$",
    "\u2085": r"$_5$", "\u2093": r"$_x$", "\u209b": r"$_s$",
    "\u211d": r"$\mathbb{R}$", "\u2194": r"$\leftrightarrow$",
    "\u221d": r"$\propto$", "\u2245": r"$\cong$",
    "\u2713": r"\checkmark",
    "\u5218\u52e4\u8ba9": r"Liu, Q.",
    "\u00e1": r"\'{a}", "\u00e9": r"\'{e}",
    "\u0151": r"\H{o}", "\u00b9": r"$^1$",
}
for uchar, latex in unicode_map.items():
    tex = tex.replace(uchar, latex)

# Cleanup
tex = re.sub(r"\n{3,}", "\n\n", tex)
tex = tex.replace("$$", "")  # remove any remaining empty $$

# Count remaining text-mode underscores
lines = tex.split("\n")
remaining_underscores = 0
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
            remaining_underscores += 1
            if remaining_underscores <= 10:
                ctx = line[max(0,j-20):j+20]
                print(f"  REMAINING: [{ctx}]")
        j += 1

print(f"\nRemaining text-mode underscores: {remaining_underscores}")

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_FULLFIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print(f"\nOutput: {len(tex)} chars, total fixes: {fixes}")
