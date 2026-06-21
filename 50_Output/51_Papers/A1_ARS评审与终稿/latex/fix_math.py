import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_HAND_FIXED.tex", "r", encoding="utf-8") as f:
    tex = f.read()

original_len = len(tex)
fixes = 0

# Fix 1: $\alpha$\cdot$\Gamma_{st}$ -> $\alpha \cdot \Gamma_{st}$
# Pattern: $X$\math_cmd$Y$ -> $X \math_cmd Y$ (for inline math cmds)
math_cmds = [
    r'\\cdot', r'\\approx', r'\\neq', r'\\times', r'\\sim',
    r'\\in', r'\\leq', r'\\geq', r'\\rightarrow', r'\\leftarrow',
    r'\\alpha', r'\\beta', r'\\gamma', r'\\delta', r'\\Gamma',
    r'\\phi', r'\\Phi', r'\\pi', r'\\theta', r'\\lambda',
    r'\\sqrt', r'\\exp', r'\\log', r'\\ln', r'\\pm',
    r'\\eta', r'\\rho', r'\\sigma', r'\\mu', r'\\nu',
    r'\\rho', r'\\tau', r'\\omega', r'\\Omega', r'\\epsilon',
    r'\\Delta', r'\\Theta', r'\\Psi', r'\\Phi',
]
for cmd in math_cmds:
    # Pattern: $...$\cmd$...$ -> $... \cmd ...$
    pattern = re.compile(r'(\$[^$]+\$)\s*(' + re.escape(cmd) + r')\s*(\$[^$]+\$)')
    while pattern.search(tex):
        tex, n = pattern.subn(r'\1 \\2 \3', tex)
        fixes += n

# Fix 2: $X$,$Y$ -> $X, Y$ (comma between math blocks)
pattern = re.compile(r'(\$[^$]+\$)\s*,\s*(\$[^$]+\$)')
while pattern.search(tex):
    tex = pattern.sub(r'\1, \2', tex)

# Fix 3: $X$ text $Y$ where text is a single math symbol/word like =, +, -, etc
for op in [r'=', r'\+', r'-', r'<', r'>', r'\|']:
    pattern = re.compile(r'(\$[^$]+\$)\s*(' + op + r')\s*(\$[^$]+\$)')
    while pattern.search(tex):
        tex, n = pattern.subn(r'\1 \\2 \3', tex)
        fixes += n

# Fix 4: Collapse adjacent math blocks: $A$$B$ -> $A B$
pattern = re.compile(r'(\$[^$]+\$)\s*(\$[^$]+\$)')
# But need to be careful not to merge things that should stay separate
# Only merge if second block is short (likely a continuation)
while True:
    m = pattern.search(tex)
    if not m:
        break
    # Merge if the gap is small and second block is short
    merged = m.group(1)[:-1] + ' ' + m.group(2)[1:]
    if len(merged) < 150:  # Don't create overly long math blocks
        tex = tex[:m.start()] + merged + tex[m.end():]
        fixes += 1
    else:
        break

# Fix 5: Fix the specific pattern: $\Gamma_{st}$$ -> $\Gamma_{st}$
# stray double dollar signs
tex = re.sub(r'(\$[^$]+\$)\$', r'\1', tex)

# Fix 6: Remove empty math blocks
tex = re.sub(r'\$\$', '', tex)

# Fix 7: $gl(k$\mathbb{R}$)$ -> $gl(k, \mathbb{R})$
tex = re.sub(r'\$([^$]+)\$\(\$([^$]+)\$\)', r'$\1(\2)$', tex)

# Fix 8: $$...$$ empty lines
tex = re.sub(r'\n{3,}', '\n\n', tex)

# Write fixed version
out_path = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_AUTOFIX.tex"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(tex)

print(f"Original: {original_len} chars")
print(f"Fixed: {len(tex)} chars")
print(f"Fixes applied: {fixes}")
print(f"Written to: A1_CST_AUTOFIX.tex")
