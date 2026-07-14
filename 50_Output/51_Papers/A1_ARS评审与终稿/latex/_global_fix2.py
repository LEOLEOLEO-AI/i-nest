import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\_BASELINE_A1_CST.tex", "r", encoding="utf-8") as f:
    tex = f.read()

print(f"Input: {len(tex)} chars")

# Remove fontspec
tex = tex.replace(r"\usepackage{fontspec}", "")
fixes = 0

# Fix 1: $X$_letter$ -> $X_letter$ (single letter subscript)
pat = re.compile(r'(\$[^$]+)\$(_[a-zA-Z])(?![a-zA-Z{])')
while pat.search(tex):
    tex, n = pat.subn(r'\1 \2$', tex)
    fixes += n
    if fixes > 500: break
print(f"1-letter subscript merge: {fixes}")

# Fix 2: $X$_Y$ -> $X_Y$ (subscript with no following $)
# This handles $\alpha$_digital -> $\alpha_digital$ where digital is plain text
# Wait, _digital has no braces, so it's just _d+i+g+i+t+a+l
# But in LaTeX, only the first char after _ is subscripted
# The original had $\alpha$_digital where the _ was in text mode - ERROR
# We need to merge into the math block: $\alpha_{digital}$
# But this requires adding braces
# Better approach: for _{...} patterns:
pat2 = re.compile(r'(\$[^$]+)\$(_\{[^}]+\})')
n2 = 0
while pat2.search(tex):
    tex, n = pat2.subn(r'\1 \2$', tex)
    n2 += n
    if n2 > 500: break
print(f"_{xxx} subscript merge: {n2}")
fixes += n2

# Fix 3: $$$ -> $$ (excess dollar signs)
tex = re.sub(r'\$\$\$+', r'$$', tex)

# Fix 4: $$X$$ -> $X$ for inline math (but keep display math $$...$$ that spans lines)
# Only fix $$...$$ that are on a single line and short
def fix_double_dollar(m):
    content = m.group(1)
    if len(content) < 200 and '\n' not in content:
        return '$' + content + '$'
    return m.group(0)

pat4 = re.compile(r'\$\$([^$]+?)\$\$')
tex = pat4.sub(fix_double_dollar, tex)
n4 = len(pat4.findall(tex))
# Count actual single-line short replacements
short_dd = len([m for m in re.finditer(r'\$\$([^$\n]{1,199})\$\$', tex)])
print(f"Fixed short $$...$$ to $...$: approx {short_dd}")

# Fix 5: $\Gamma$a_{st} -> $\Gamma_{st}$ (specific scattered pattern)
tex = tex.replace(r"$\Gamma$a_{st}$", r"$\Gamma_{st}$")
tex = tex.replace(r"$\Gamma$a$_\{st\}$", r"$\Gamma_{st}$")
tex = tex.replace(r"$\Gamma$ a$_{st}$", r"$\Gamma_{st}$")
n5 = tex.count(r"$\Gamma_{st}$")
print(f"Gamma_st contexts: {n5}")

# Fix 6: Unicode mapping
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

# Verify Unicode clean
remaining_unicode = [c for c in tex if ord(c) > 127 and ord(c) < 0x2000]
print(f"Remaining Unicode: {len(set(remaining_unicode))}")

# Count text-mode underscores
lines = tex.split("\n")
underscore_count = 0
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
            underscore_count += 1
            if underscore_count <= 15:
                ctx = line[max(0,j-30):j+30]
                print(f"  TXT_: [{ctx}]")
        j += 1

print(f"Text-mode underscores: {underscore_count}")

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_FULLFIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print(f"\nOutput: {len(tex)} chars, fixes: {fixes}")
