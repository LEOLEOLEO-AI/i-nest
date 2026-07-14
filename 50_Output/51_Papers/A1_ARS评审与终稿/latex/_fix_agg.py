import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Aggressive fix: wrap ALL math-like expressions in text with $...$
# This is heavy-handed but will get past line 150

# Split into lines and fix each
lines = tex.split("\n")
new_lines = []

for line in lines:
    # Only process text-mode lines (skip equation envs)
    if "\\begin{equation}" in line or "\\begin{align}" in line:
        new_lines.append(line)
        continue
    if "\\end{equation}" in line or "\\end{align}" in line:
        new_lines.append(line)
        continue
    
    # In text mode: wrap scattered math commands
    # Fix: \cdot, \approx, \neq, \times, \sim, \geq, \leq, \in, \pm
    # that appear OUTSIDE $...$ 
    
    # Strategy: find all $ blocks, fix text between them
    parts = re.split(r'(\$[^$]+\$)', line)
    for i in range(0, len(parts), 2):  # text mode parts
        # Wrap isolated math commands
        for cmd in ['\\cdot', '\\approx', '\\neq', '\\times', '\\sim', 
                     '\\geq', '\\leq', '\\in', '\\pm', '\\propto', '\\cong']:
            # Replace \cmd with $\cmd$ but only if not already in $...$
            parts[i] = parts[i].replace(' ' + cmd + ' ', ' $' + cmd + '$ ')
            parts[i] = parts[i].replace('\n' + cmd + ' ', '\n$' + cmd + '$ ')
    
    new_line = ''.join(parts)
    new_lines.append(new_line)

tex = '\n'.join(new_lines)

# Count
count = tex.count('$\\cdot$')
print("Total $\\cdot$: " + str(count))

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Saved: " + str(len(tex)))
