import subprocess

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Fix: $X_{_Y}$ → $X_{\text{Y}}$ (double subscript)
import re
pat = re.compile(r'_\{_([^}]+)\}')
n = 0
while pat.search(tex):
    tex = pat.sub(r'_{\\text{\1}}', tex)
    n += 1
    if n > 200: break
print("Fixed double subscripts: " + str(n))

# Also fix patterns like $X_{_c}$ → $X_{c}$
pat2 = re.compile(r'_\{_([a-zA-Z])\}')
n2 = 0
while pat2.search(tex):
    tex = pat2.sub(r'_{\1}', tex)
    n2 += 1
    if n2 > 200: break
print("Fixed single-char double subs: " + str(n2))

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)

result = subprocess.run([
    r"C:\Users\LEO\.codex\plugins\cache\openai-bundled\latex\0.2.3\bin\tectonic.exe",
    "-X", "compile", "--keep-intermediates",
    "--outdir", r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex",
    "--outfmt", "pdf", "--untrusted", out
], capture_output=True, text=True, timeout=60)

for line in result.stderr.split("\n"):
    if "error" in line.lower():
        print(line)
print("RC:", result.returncode)
