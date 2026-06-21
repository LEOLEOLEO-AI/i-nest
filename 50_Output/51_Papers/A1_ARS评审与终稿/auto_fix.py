import re, subprocess, sys, os

TEX = r'D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_vFINAL.tex'
TECTONIC = r'C:\Users\LEO\.codex\plugins\cache\openai-bundled\latex\0.2.3\bin\tectonic.exe'
OUTDIR = r'D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex'

# Math commands that MUST be inside math mode
MATH_CMDS = [
    r'\\sqrt\b', r'\\frac\b', r'\\alpha\b', r'\\beta\b', r'\\gamma\b',
    r'\\delta\b', r'\\phi\b', r'\\Phi\b', r'\\pi\b', r'\\Pi\b',
    r'\\sigma\b', r'\\Gamma\b', r'\\Delta\b', r'\\Theta\b',
    r'\\lambda\b', r'\\mu\b', r'\\eta\b', r'\\cdot\b', r'\\approx\b',
    r'\\equiv\b', r'\\leq\b', r'\\geq\b', r'\\in\b', r'\\propto\b',
    r'\\times\b', r'\\rightarrow\b', r'\\Rightarrow\b',
    r'\\exp\b', r'\\ln\b', r'\\log\b'
]

def is_inside_math(line, pos):
    """Check if position pos is inside $...$ or \(...\) math mode"""
    in_math = False
    i = 0
    while i < pos:
        if line[i:i+2] == r'\(' and (i == 0 or line[i-1] != '\\'):
            in_math = True
            i += 2
        elif line[i:i+2] == r'\)' and (i == 0 or line[i-1] != '\\'):
            in_math = False
            i += 2
        elif line[i] == '$' and (i == 0 or line[i-1] != '\\'):
            in_math = not in_math
            i += 1
        else:
            i += 1
    return in_math

def fix_line(line):
    if not line.strip() or line.strip().startswith('%'):
        return line
    if '\\begin{equation}' in line or '\\end{equation}' in line:
        return line
    
    # Finding math commands outside math mode
    for cmd in MATH_CMDS:
        for m in re.finditer(cmd, line):
            pos = m.start()
            if not is_inside_math(line, pos):
                # Found math command outside math mode
                # Strategy: wrap the smallest segment containing the command in $...$
                # Find word boundaries
                segment = m.group()
                # Replace just this occurrence
                line = line[:pos] + '$' + line[pos:pos+len(segment)] + '$' + line[pos+len(segment):]
                return fix_line(line)  # Recurse to handle more
    return line

# Read
with open(TEX, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix each line
fixed = [fix_line(l) for l in lines]
content = ''.join(fixed)

OUT = TEX.replace('.tex', '_AUTOFIX.tex')
with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print(f'Wrote {OUT}')
print(f'Lines: {len(fixed)}')
