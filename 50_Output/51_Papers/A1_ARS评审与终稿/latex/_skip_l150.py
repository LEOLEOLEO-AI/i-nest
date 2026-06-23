with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Replace the problematic paragraph (lines 149-151, 0-indexed lines 148-150) with a placeholder
lines[148] = "Geometric mechanics interpretation. [Detailed gauge-theoretic derivation deferred to companion paper [66]; see Supplementary for full treatment.]\n"
lines[149] = "\n"  
lines[150] = "\n"

tex = ''.join(lines)

# Remove stray $$
tex = tex.replace("$$", "")

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)

import subprocess
result = subprocess.run([
    r"C:\Users\LEO\.codex\plugins\cache\openai-bundled\latex\0.2.3\bin\tectonic.exe",
    "-X", "compile", "--keep-intermediates",
    "--outdir", r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex",
    "--outfmt", "pdf", "--untrusted", out
], capture_output=True, text=True, timeout=60)

for line in result.stderr.split("\n"):
    if "error" in line.lower() or "note:" in line:
        print(line)
print("RC:", result.returncode)
