import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Fix: $X$\cdot$Y$ → $X \cdot Y$ (scattered cdot)
pat = re.compile(r'\$([^$]+)\$\\cdot\$([^$]+)\$')
n = 0
while pat.search(tex):
    tex, cnt = pat.subn(r'$\1 \\cdot \2$', tex)
    n += cnt
    if n > 100: break
print("Scattered \\cdot fixes: " + str(n))

# Fix other scattered math commands: \times, \approx, \sim, \Gamma, \alpha, etc.
for cmd in ['\\\\approx', '\\\\neq', '\\\\times', '\\\\sim', '\\\\geq', '\\\\leq', '\\\\in', '\\\\pm']:
    pat = re.compile(r'\$([^$]+)\$\s*(' + cmd + r')\s*\$([^$]+)\$')
    cnt = 0
    while pat.search(tex):
        tex, c = pat.subn(lambda m, cmd2=cmd: '$' + m.group(1) + ' ' + cmd2 + ' ' + m.group(3) + '$', tex)
        cnt += c
        if cnt > 100: break
    if cnt > 0:
        print("Scattered " + cmd + " fixes: " + str(cnt))

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Saved: " + str(len(tex)))
