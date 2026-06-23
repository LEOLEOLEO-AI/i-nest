import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\_BASELINE_A1_CST.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Remove fontspec (not compatible with Tectonic)
tex = tex.replace(r"\usepackage{fontspec}", "")

# Map all Unicode chars to LaTeX equivalents
unicode_map = {
    "\u03b1": r"\alpha", "\u03b2": r"\beta", "\u03b3": r"\gamma",
    "\u03b4": r"\delta", "\u03b5": r"\epsilon", "\u03b7": r"\eta",
    "\u03b8": r"\theta", "\u03bb": r"\lambda", "\u03bc": r"\mu",
    "\u03bd": r"\nu", "\u03c0": r"\pi", "\u03c1": r"\rho",
    "\u03c3": r"\sigma", "\u03c6": r"\phi",
    "\u03a6": r"\Phi", "\u03a8": r"\Psi", "\u0393": r"\Gamma",
    "\u0398": r"\Theta", "\u0394": r"\Delta",
    "\u00d7": r"\times", "\u00b7": r"\cdot",
    "\u2014": "---", "\u2013": "--",
    "\u2018": "'", "\u2019": "'",
    "\u201c": "``", "\u201d": "''",
    "\u00b1": r"\pm", "\u00b2": r"$^2$", "\u00b3": r"$^3$",
    "\u00a7": r"\S{}",
    "\u00b0": r"$^\circ$",
    "\u2264": r"$\leq$", "\u2265": r"$\geq$",
    "\u2248": r"$\approx$", "\u223c": r"$\sim$",
    "\u2212": r"--",
    "\u2192": r"$\rightarrow$",
    "\u2208": r"$\in$",
    "\u2206": r"$\Delta$",
    "\u221a": r"$\sqrt{}$",
}

for uchar, latex_cmd in unicode_map.items():
    tex = tex.replace(uchar, latex_cmd)

# Remove the now-unsupported Unicode chars that don't have simple mappings
# Any remaining non-ASCII that's not part of LaTeX commands
# Let's just check what's left
remaining = set()
for c in tex:
    if ord(c) > 127 and ord(c) < 0x2000:
        remaining.add(c)

report_lines = []
for c in sorted(remaining):
    report_lines.append(f"U+{ord(c):04X}: x{tex.count(c)}")
report_lines.append(f"Total remaining: {len(remaining)}")
report = "\n".join(report_lines)

# Write output
out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_BASELINE_FIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)

# Write report
report_out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\_unicode_report.txt"
with open(report_out, "w", encoding="utf-8") as f:
    f.write(report + f"\nOutput: {len(tex)} chars, {len(tex.splitlines())} lines")

print("Done - see _unicode_report.txt")
