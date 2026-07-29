import re

with open(r"D:\Obsidian\vault\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

fixes = 0

# Fix 1: $10$^{-}^6$ → $10^{-6}$ (double superscript from Unicode mapping)
# Pattern: $X$^{-}^Y$ → $X^{-Y}$
pat = re.compile(r'(\$[^$]+\$)\\^\{-\}\\^(\$?[0-9n]+\$?)')
while pat.search(tex):
    tex = pat.sub(r"\1^{-\\2}", tex)
    fixes += 1
    if fixes > 50: break

# Fix 2: $X$^Y$ → $X^Y$ (single superscript merge)
pat2 = re.compile(r'(\$[^$]+\\$)\\^\{([^}]+)\}\\$')
# Actually this is more complex. Let me just fix known patterns.
# $10$^{-}$ → $10^{-}$ (merge superscript into math)
n1 = 0  
pat2a = re.compile(r'\\$10\\$\\^\\{-\\}\\$')
n1 = len(pat2a.findall(tex))
tex = pat2a.sub(r'$10^{-}$', tex)
print("Fixed $10^{-}$: " + str(n1))

# $^{-}^6$ → $^{-6}$ (merge consecutive superscripts)
pat3 = re.compile(r'\\$\\^\\{-\\}\\$\\^([0-9n])\\$')
n3 = len(pat3.findall(tex))
tex = pat3.sub(r'$^{-\1}$', tex)
print("Fixed $^{-}^N$: " + str(n3))

# Fix: $10$$^{-}$$^6$ → $10^{-6}$
tex = tex.replace("$10$$^{-}$$^6$", "$10^{-6}$")

# General fix: $$^{-}$$^N$ → $^{-N}$ 
for digit in ['1','2','3','4','5','6','7','8','9','n']:
    pat = re.compile(r'\\$\\^\\{-\\}\\$\\^' + digit + r'\\$')
    tex = pat.sub(r'$^{-' + digit + '}$', tex)

# General fix: $^{-}$$^N$ → $^{-N}$
pat4 = re.compile(r'\\$\\^\\{-\\}\\$\\^\\{([0-9n]+)\\}\\$')
n4 = len(pat4.findall(tex))
tex = pat4.sub(r'$^{-\\1}$', tex)
print("Fixed $^{-}$$^N$ patterns: " + str(n4))

out = r"D:\Obsidian\vault\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Saved: " + str(len(tex)))
