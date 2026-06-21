import re

v29 = r'D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_CST_Theory_V29_FROM_PDF.md'
with open(v29, 'r', encoding='utf-8') as f:
    t = f.read()

changes = 0

# KEY FORMULA 1: CST = (S_c * T_c) * e^{alpha * Gamma_st}
old = t
t = t.replace('CST = (S_c * T_c) * e^{', '$CST = (S_c \cdot T_c) \cdot e^{')
if t != old: changes += 1
# Close the dollar
# This is complex because the pattern spans multiple lines in the abstract
# Let's handle it differently - find and replace the whole abstract formula

# Replace common inline math patterns (safe, no side effects)
pairs = [
    # Subscript patterns
    ('S_c', '$S_c$'),
    ('T_c', '$T_c$'),
    ('M_eff', '$M_{eff}$'),
    ('P_norm', '$P_{norm}$'), 
    ('alpha_digital', r'$\alpha_{digital}$'),
    ('alpha_cortical', r'$\alpha_{cortical}$'),
    # Greek + subscripts
    ('Gamma_st', r'$\Gamma_{st}$'),
    ('eta_I', r'$\eta_I$'),
    ('rho = 0', r'$\rho = 0'),
    ('Spearman rho', 'Spearman $\\rho$'),
    # Mathematical expressions
    ('ln(M_eff)', r'$\ln(M_{eff})$'),
]

for old_pat, new_pat in pairs:
    old = t
    t = t.replace(old_pat, new_pat)
    if t != old:
        changes += 1
        # Print only first few
        if changes <= 5:
            print(f'  Replaced: {old_pat[:30]} -> {new_pat[:30]}')

# Handle the abstract CST formula specially  
# Find it and wrap the whole thing
idx = t.find('$CST = (S_c')
if idx >= 0:
    # Find the end of this formula (look for -- or . or newline)
    end_idx = t.find(' -- ', idx)
    if end_idx < 0:
        end_idx = t.find('\n', idx)
    formula_part = t[idx:end_idx].strip()
    if not formula_part.endswith('$'):
        t = t[:end_idx] + '$' + t[end_idx:]
        changes += 1
        print(f'  Closed CST formula at offset {end_idx}')

with open(v29, 'w', encoding='utf-8') as f:
    f.write(t)

print(f'Total changes: {changes}')
print(f'New size: {len(t)}')
