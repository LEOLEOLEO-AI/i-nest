import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\_BASELINE_A1_CST.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Remove fontspec first
tex = tex.replace(r"\usepackage{fontspec}", "")

fixes = 0

# Fix 1: R\_{sw} -> $R_{sw}$
n = tex.count(r"R\_{sw}")
tex = tex.replace(r"R\_{sw}", r"$R_{sw}$")
fixes += n
print(f"R_sw: {n}")

# Fix 2: \_{eff} -> $_{\text{eff}}$ or $_{eff}$
n = tex.count(r"\_{eff}")
tex = tex.replace(r"\_{eff}", r"$_{\text{eff}}$")
fixes += n
print(f"_eff: {n}")

# Fix 3: \_{CST}
n = tex.count(r"\_{CST}")
tex = tex.replace(r"\_{CST}", r"$_{\text{CST}}$")
fixes += n
print(f"_CST: {n}")

# Fix 4: \_{env}  
n = tex.count(r"\_{env}")
tex = tex.replace(r"\_{env}", r"$_{\text{env}}$")
fixes += n
print(f"_env: {n}")

# Fix 5: \_{expertise}
n = tex.count(r"\_{expertise}")
tex = tex.replace(r"\_{expertise}", r"$_{\text{expertise}}$")
fixes += n
print(f"_expertise: {n}")

# Fix 6: \_{species} 
n = tex.count(r"\_{species}")
tex = tex.replace(r"\_{species}", r"$_{\text{species}}$")
fixes += n
print(f"_species: {n}")

# Fix 7: \_{task}
n = tex.count(r"\_{task}")
tex = tex.replace(r"\_{task}", r"$_{\text{task}}$")
fixes += n
print(f"_task: {n}")

# Fix 8: \_{FC}
n = tex.count(r"\_{FC}")
tex = tex.replace(r"\_{FC}", r"$_{\text{FC}}$")
fixes += n
print(f"_FC: {n}")

# Fix 9: Other patterns
# \_{norm
tex = tex.replace(r"\_{\text{norm}", r"$_{\text{norm}$")

# Fix 10: L\_{task}, T\_{species}, E\_{env}, a\_{expertise} 
tex = tex.replace(r"L\_{task}", r"$L_{\text{task}}$")
tex = tex.replace(r"T\_{species}", r"$T_{\text{species}}$")
tex = tex.replace(r"E\_{env}", r"$E_{\text{env}}$")
tex = tex.replace(r"a\_{expertise}", r"$a_{\text{expertise}}$")
fixes += 4

# Fix 11: Remaining bare _ patterns
# \_I -> $_{\text{I}}$ if in text mode
tex = re.sub(r'(?<!\$)\\_(?![a-zA-Z])', r'$\_$', tex)

# Fix 12: \_{geo} -> $_{\text{geo}}$
tex = tex.replace(r"\_{geo}", r"$_{\text{geo}}$")

# Fix 13: \_{emergent} -> $_{\text{emergent}}$
tex = tex.replace(r"\_{emergent}", r"$_{\text{emergent}}$")

# Fix 14: _c$...$ patterns - these actually need to have the _ inside the math block
# \_c$ -> $_{c}$
tex = tex.replace(r"\_c$", r"$_{c}$")

# Handle Unicode
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
    "\u00a7": r"\S{}",
    "\u00b0": r"$^\circ$",
    "\u2264": r"$\leq$", "\u2265": r"$\geq$",
    "\u2248": r"$\approx$", "\u223c": r"$\sim$",
    "\u2212": r"--",
    "\u2192": r"$\rightarrow$",
    "\u2208": r"$\in$",
    "\u2206": r"$\Delta$",
    "\u221a": r"$\sqrt{}$",
    "\u2020": r"\dag",
    "\u2074": r"$^4$", "\u2075": r"$^5$", "\u2076": r"$^6$",
    "\u2077": r"$^7$", "\u2079": r"$^9$",
    "\u207b": r"$^{-}$", "\u207f": r"$^n$",
    "\u2081": r"$_1$", "\u2082": r"$_2$", "\u2083": r"$_3$",
    "\u2085": r"$_5$", "\u2093": r"$_x$", "\u209b": r"$_s$",
    "\u211d": r"$\mathbb{R}$",
    "\u2194": r"$\leftrightarrow$",
    "\u221d": r"$\propto$",
    "\u2245": r"$\cong$",
    "\u2713": r"\checkmark",
    "\u5218\u52e4\u8ba9": r"Liu, Q.",
    "\u00e1": r"\'{a}", "\u00e9": r"\'{e}",
    "\u0151": r"\H{o}", "\u00b9": r"$^1$",
}

for uchar, latex in unicode_map.items():
    tex = tex.replace(uchar, latex)

# Verify no residuals
remaining = [c for c in tex if ord(c) > 127 and ord(c) < 0x2000]
if remaining:
    print(f"WARNING: {len(set(remaining))} Unicode chars remain")

# Check remaining _ in text mode (simplified check)
parts = re.split(r"(\$[^$]+\$)", tex)
text_underscores = 0
for i, part in enumerate(parts):
    if i % 2 == 0:  # text mode
        for m in re.finditer(r"(?<!\\)_", part):
            text_underscores += 1
            ctx = part[max(0,m.start()-20):m.end()+20].replace(chr(10), " ")
            if text_underscores <= 5:
                print(f"TEXT UNDERSCORE: [{ctx}]")

if text_underscores == 0:
    print("NO text-mode underscores remaining!")
else:
    print(f"WARNING: {text_underscores} text-mode underscores still present")

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_CLEAN.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print(f"\nWritten: {len(tex)} chars, total fixes: {fixes}")
