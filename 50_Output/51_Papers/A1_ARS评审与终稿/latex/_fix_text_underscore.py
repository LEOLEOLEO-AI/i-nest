import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Find ALL text-mode underscores (outside $...$ and outside equation/align envs)
lines = tex.split("\n")
fixes = 0

for i, line in enumerate(lines):
    in_math = False
    in_env = False  # inside \begin{equation} etc.
    
    # Simple check for \begin{equation}, \begin{align} etc.
    if "\\begin{equation}" in line or "\\begin{align}" in line:
        in_env = True
    
    # Process character by character
    j = 0
    while j < len(line):
        if line[j:j+2] == "\\$":
            j += 2; continue
        if line[j] == "$":
            in_math = not in_math
            j += 1; continue
        if line[j] == "\\" and j+1 < len(line):
            if line[j:j+16] == "\\begin{equation}":
                in_env = True
                j += 16; continue
            if line[j:j+14] == "\\end{equation}":
                in_env = False
                j += 14; continue
            if line[j:j+12] == "\\begin{align}":
                in_env = True
                j += 12; continue
            if line[j:j+10] == "\\end{align}":
                in_env = False
                j += 10; continue
        
        if line[j] == "_" and not in_math and not in_env and (j == 0 or line[j-1] != "\\"):
            # Found text-mode underscore!
            # Try to merge with adjacent math blocks
            # Look left for closest $...$ block
            left_dollar = line.rfind("$", 0, j)
            # Look right for closest $...$ block
            right_dollar = line.find("$", j+1)
            
            if left_dollar >= 0:
                # Check if there's a math block before this _
                # If so, merge the _text into that math block
                # Build the fixed line
                before = line[:left_dollar]  # everything before the math block
                math_block = line[left_dollar+1:j]  # math content to merge
                after_ = line[j+1:right_dollar] if right_dollar > j else line[j+1:]
                
                # Determine what to merge
                # _text where text continues until space, $, or punctuation
                subscript_end = j + 1
                while subscript_end < len(line) and line[subscript_end].isalnum():
                    subscript_end += 1
                subscript_text = line[j+1:subscript_end]
                
                # Build replacement
                replacement = "$" + math_block.strip() + "_{" + subscript_text + "}"
                if right_dollar > j:
                    replacement += " $" + line[right_dollar+1:].lstrip()
                else:
                    replacement += "$"
                
                line = before + replacement
                fixes += 1
                break  # Process one fix per line per pass
            
        j += 1
    
    lines[i] = line

tex = "\n".join(lines)
print("Text-mode underscore fixes: " + str(fixes))

# Also remove remaining stray $$
tex = tex.replace("$$", "")

# Fix common remaining issues
tex = tex.replace("\\_\n", "\n")  # stray escaped underscore at line end

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Saved: " + str(len(tex)) + " chars")
