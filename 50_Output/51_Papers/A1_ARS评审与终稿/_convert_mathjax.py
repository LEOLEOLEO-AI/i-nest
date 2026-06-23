import re
import os

file = r'D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\A1_CST_Theory_V32_MERGED_CLEAN.md'
with open(file, 'r', encoding='utf-8') as f:
    t = f.read()

log = []
log.append(f'Original size: {len(t)} chars')

# Helper: wrap display formula
def df(text, latex):
    return f'\$\\$\$'

# Helper: wrap inline math  
def im(latex):
    return f'\\$'

# Count replacements
count = 0

# ===== DISPLAY FORMULAS (key equations) =====
replacements = [
    # CST main formula (line 19, 92, 119)
    ('CST = ( Sc路Tc)路exp(伪路螕st),', df('CST = (S_c \\\\cdot T_c) \\\\cdot e^{\\\\alpha \\\\cdot \\\\Gamma_{st}}')),
    ('CST = ( Sc路Tc)路exp(伪路螕st).', df('CST = (S_c \\\\cdot T_c) \\\\cdot e^{\\\\alpha \\\\cdot \\\\Gamma_{st}}')),
    ('CST = ( Sc路Tc)路exp(伪路螕st) (1)', df('CST = (S_c \\\\cdot T_c) \\\\cdot e^{\\\\alpha \\\\cdot \\\\Gamma_{st}} \\\\quad (1)')),
    ('CST = ( Sc路Tc)路exp(伪路螕st)', df('CST = (S_c \\\\cdot T_c) \\\\cdot e^{\\\\alpha \\\\cdot \\\\Gamma_{st}}')),
]

for old, new in replacements:
    if old in t:
        t = t.replace(old, new)
        count += 1
        log.append(f'  Replaced: {old[:40]}...')

log.append(f'Total replacements: {count}')
log.append(f'Final size: {len(t)} chars')

# Write result
with open(file, 'w', encoding='utf-8') as f:
    f.write(t)

# Write log
log_path = r'D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\_mathjax_log.txt'
with open(log_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(log))

print('Done. See _mathjax_log.txt')
