import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Fix: $\cdot$ inside equation/align environments → \cdot
# Find all equation/align blocks and remove $ signs from \cdot
def fix_eq_content(tex):
    result = []
    i = 0
    while i < len(tex):
        # Find next equation block
        eq_start = -1
        eq_tag = ""
        for tag in ["\\begin{equation}", "\\begin{align}"]:
            idx = tex.find(tag, i)
            if idx >= 0 and (eq_start < 0 or idx < eq_start):
                eq_start = idx
                eq_tag = tag
        
        if eq_start < 0:
            result.append(tex[i:])
            break
        
        # Copy content before equation
        result.append(tex[i:eq_start])
        
        # Find matching end
        end_tag = eq_tag.replace("\\begin", "\\end")
        eq_end = tex.find(end_tag, eq_start + len(eq_tag))
        if eq_end < 0:
            result.append(tex[eq_start:])
            break
        
        # Extract equation content and fix
        content_start = eq_start + len(eq_tag)
        content = tex[content_start:eq_end]
        
        # Remove $ signs around \cdot, \times, \approx, etc.
        for cmd in ["\\cdot", "\\times", "\\approx", "\\sim", "\\geq", "\\leq", "\\neq", "\\in", "\\pm"]:
            content = content.replace("$" + cmd + "$", cmd)
        
        result.append(eq_tag)
        result.append(content)
        result.append(end_tag)
        
        i = eq_end + len(end_tag)
    
    return ''.join(result)

tex = fix_eq_content(tex)

# Count remaining $\cdot$ in equation envs
import re
remaining = len(re.findall(r'\$\\cdot\$', tex))
print("Remaining $\\cdot$ in equations: " + str(remaining))

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Saved: " + str(len(tex)))
