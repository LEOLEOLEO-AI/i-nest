import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_V9_FINALFIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

fixes = 0

# Fix 1: $X$_Y → $X_Y$ (subscript outside math after a math block)
# Pattern: $...$ followed by _... (subscript in text mode)
# We need to merge the subscript into the math block
pat = re.compile(r'(\$[^$]+\$)(_[a-zA-Z0-9{]+)')
while pat.search(tex):
    tex, n = pat.subn(lambda m: '$' + m.group(1)[1:-1] + m.group(2) + '$', tex)
    fixes += n
    if fixes > 500:  # safety
        break
print(f"Fixed {fixes} subscript-after-math patterns")

# Fix 2: $X$^Y → $X^Y$ (superscript outside math)  
pat2 = re.compile(r'(\$[^$]+\$)(\^[a-zA-Z0-9{]+)')
n2 = 0
while pat2.search(tex):
    tex, n = pat2.subn(lambda m: '$' + m.group(1)[1:-1] + m.group(2) + '$', tex)
    n2 += n
    if n2 > 500:
        break
print(f"Fixed {n2} superscript-after-math patterns")
fixes += n2

# Fix 3: $X$ a$_{Y}$ → $X_{Y}$ (scattered with 'a' as bridge)
# This is $...$ followed by letter 'a' followed by $_{...}$
# Actually more general: $X$<letter>$_{Y}$ → $X_{Y}$
# But too aggressive. Let me just fix the specific known case
# \Gamma a_{st} and similar
pat3 = re.compile(r'\$\\Gamma\$a\$_\{st\}\$')
n3 = len(pat3.findall(tex))
if n3 > 0:
    tex = pat3.sub(r'$\Gamma_{st}$', tex)
    fixes += n3
    print(f"Fixed {n3} scattered Gamma_st patterns")

# Fix 4: More general: find all $<cmd>$a$_{<text>}$ and merge
# This handles $\alpha$a$_{digital}$ and similar
pat4 = re.compile(r'(\$\\[a-zA-Z]+\$)a(\$_\{[^}]+\}\$)')
n4 = 0
while pat4.search(tex):
    tex, n = pat4.subn(lambda m: '$' + m.group(1)[1:-1] + '_' + m.group(2)[1:-1] + '$', tex)
    n4 += n
    if n4 > 200:
        break
print(f"Fixed {n4} scattered cmd_a_{} patterns")
fixes += n4

# Fix 5: Similarly for cmd$<number>$ patterns
# $\alpha$_digital → $\alpha_{\text{digital}}$
# Already handled by Fix 1

# Clean up
tex = re.sub(r'\n{3,}', '\n\n', tex)
# Remove empty math blocks
tex = re.sub(r'\$\$', '', tex)

out_path = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_V10_MERGED.tex"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(tex)

print(f"\nV10_MERGED: {len(tex)} chars, {len(tex.splitlines())} lines, total fixes: {fixes}")
