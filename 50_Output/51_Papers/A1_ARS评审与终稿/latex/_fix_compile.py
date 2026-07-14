import subprocess

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Simple fixes for line 150 area - known patterns
fixes = [
    ("exp($\\alpha$ $\\cdot$ $\\Gamma_{st}$)", "$\\exp(\\alpha \\cdot \\Gamma_{st})$"),
    ("exp($\\alpha $\\cdot$ \\Gamma_{st}$)", "$\\exp(\\alpha \\cdot \\Gamma_{st})$"),
    ("$\\gamma$I -- q$\\Omega$)$^{-}^1$", "$\\gamma I - q\\Omega)^{-1}$"),
    ("$\\gamma$I -- q$\\Omega$)", "$\\gamma I - q\\Omega)$"),
    ("$A_{}$ $\\mu$", "$A_{\\mu}$"),
    ("A_$\\nu$", "A_{\\nu}$"),
    ("[A_$\\mu$", "$[A_{\\mu}$"),
    ("CST = Sc $\\cdot$ Tc", "$CST = S_c \\cdot T_c$"),
    ("\\approx  $\\gamma_{_CST}$", "\\approx \\gamma_{\\text{CST}}$"),
]

for old, new in fixes:
    if old in tex:
        tex = tex.replace(old, new)
        print("Fixed: " + old[:50])

# Also fix: [A_{} $\mu$, A_$\nu$] → $[A_{\mu}, A_{\nu}]$
tex = tex.replace("[A_{} $\\mu$, A_$\\nu$]", "$[A_{\\mu}, A_{\\nu}]$")

# Fix: q  \\approx  $\gamma_{_CST}$ → $q \approx \gamma_{\text{CST}}$
tex = tex.replace("q  \\approx  $\\gamma_{_CST}$", "$q \\approx \\gamma_{\\text{CST}}$")

# Fix: ($\gamma$I -- q$\Omega$)$^{-}^1$ 
tex = tex.replace("($\\gamma$I -- q$\\Omega$)$^{-}^1$", "$(\\gamma I - q\\Omega)^{-1}$")

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)

# Compile
result = subprocess.run([
    r"C:\Users\LEO\.codex\plugins\cache\openai-bundled\latex\0.2.3\bin\tectonic.exe",
    "-X", "compile", "--keep-intermediates",
    "--outdir", r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex",
    "--outfmt", "pdf", "--untrusted", out
], capture_output=True, text=True, timeout=60)

for line in result.stderr.split("\n"):
    if "error" in line.lower() or "warning" in line.lower() or "note:" in line:
        print(line)
print("RC:", result.returncode)
