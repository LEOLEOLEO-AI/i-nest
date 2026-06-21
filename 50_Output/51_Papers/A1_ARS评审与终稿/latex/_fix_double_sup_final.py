with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

import re

# Fix: $\times$10$^{-}^6$ → $\times 10^{-6}$
# The pattern is: \times in one math block, 10 in text, then ^{-}^6 in another math block
# Fix: merge all into one math block

# Pattern: $\times$ followed by digits, then $^{-}^N$
pat = re.compile(r'\$\\times\$\s*([0-9.]+)\s*\$\\^\{-\}\\^([0-9n]+)\$')
n = 0
while pat.search(tex):
    tex = pat.sub(r'$\times \1^{-}\2}$', tex)
    n += 1
    if n > 50: break
print("Fixed $\\times$N$^{-}^M$: " + str(n))

# Check remaining $^{-}^ patterns
remaining = len(re.findall(r'\$\\^\{-\}\\^', tex))
print("Remaining $^{-}^ patterns: " + str(remaining))

# If any remain, show them
if remaining > 0:
    for m in re.finditer(r'.\$\\^\{-\}\\^.', tex):
        ctx = tex[max(0,m.start()-20):m.end()+20].replace(chr(10),' ')
        print("  [" + ctx + "]")

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Saved: " + str(len(tex)))
