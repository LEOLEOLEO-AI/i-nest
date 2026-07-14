import re, os

TEX = r'D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_vFINAL.tex'

# Math commands that MUST be inside math mode
MATH_CMDS = r'\\(?:sqrt|frac|alpha|beta|gamma|delta|phi|Phi|pi|Pi|sigma|Gamma|Delta|Theta|lambda|mu|eta|cdot|approx|equiv|leq|geq|in|propto|times|rightarrow|Rightarrow|exp|ln|log)\b'

with open(TEX, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Determine which lines are inside equation/align blocks
in_display_math = False
display_math_envs = ['equation', 'align', 'equation*', 'align*', 'gather', 'gather*']

fixed = []
for i, line in enumerate(lines):
    stripped = line.strip()
    
    # Track display math environments
    for env in display_math_envs:
        if f'\\\\begin{{{env}}}' in stripped:
            in_display_math = True
        if f'\\\\end{{{env}}}' in stripped:
            in_display_math = False
    
    if in_display_math or stripped.startswith('%') or not stripped:
        fixed.append(line)
        continue
    
    # For text lines, find math commands outside $...$ blocks
    # Split the line by existing $...$ blocks
    result = []
    pos = 0
    in_inline_math = False
    
    while pos < len(line):
        if line[pos] == '$' and (pos == 0 or line[pos-1] != '\\\\'):
            in_inline_math = not in_inline_math
            result.append(line[pos])
            pos += 1
            continue
        
        if not in_inline_math:
            # Check if next few chars match a math command
            m = re.match(MATH_CMDS, line[pos:])
            if m:
                # Insert a $ before the command
                cmd = m.group()
                result.append('$' + cmd + '$')
                pos += len(cmd)
                continue
        
        result.append(line[pos])
        pos += 1
    
    fixed.append(''.join(result))

OUT = TEX.replace('.tex', '_AUTOFIX2.tex')
with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write(''.join(fixed))
print(f'Wrote {OUT}')
print(f'Lines: {len(fixed)}')
