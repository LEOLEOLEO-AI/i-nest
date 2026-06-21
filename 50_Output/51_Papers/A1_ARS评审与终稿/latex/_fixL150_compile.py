import re, subprocess

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# The issue on L150 is the "Geometric mechanics" paragraph with text-mode math
# Find all text-mode math issues and wrap them
lines = tex.split("\n")

for i in range(147, 155):
    if i >= len(lines): break
    line = lines[i]
    # Replace text-mode math commands with $wrapped$ versions
    # But only if not already in $...$
    parts = re.split(r'(\$[^$]+\$)', line)
    for j in range(0, len(parts), 2):  # text parts
        # Replace standalone math commands
        for cmd in ['\\cdot', '\\approx', '\\neq', '\\times', '\\sim', '\\geq', '\\leq', '\\in', '\\pm', '\\propto', '\\cong', '\\exp']:
            parts[j] = re.sub(r'(?<!\$)' + re.escape(cmd) + r'(?!\$)', r'$' + cmd + r'$', parts[j])
    lines[i] = ''.join(parts)

tex = '\n'.join(lines)

# Also clean up any $$
tex = tex.replace("$$", "")

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

for line in result.stdout.split("\n")[-10:]:
    print(line)
for line in result.stderr.split("\n")[-10:]:
    print("STDERR:", line)
print("RC:", result.returncode)
