import re

with open(r'latex\A1_CST.tex', 'r', encoding='utf-8') as f:
    tex = f.read()

replacements = {
    '\u2014': '---', '\u2013': '--',
    '\u2018': "'", '\u2019': "'",
    '\u201c': '``', '\u201d': "''",
    '\u2026': '...', '\u2212': '-',
    '\u00d7': '$\\times$', '\u00b1': '$\\pm$',
    '\u2192': '$\\rightarrow$', '\u2190': '$\\leftarrow$',
    '\u21d2': '$\\Rightarrow$',
    '\u03b1': '$\\alpha$', '\u03b2': '$\\beta$',
    '\u03b3': '$\\gamma$', '\u0393': '$\\Gamma$',
    '\u03b4': '$\\delta$', '\u0394': '$\\Delta$',
    '\u03b5': '$\\epsilon$', '\u03b7': '$\\eta$',
    '\u03b8': '$\\theta$', '\u03bc': '$\\mu$',
    '\u03bd': '$\\nu$', '\u03c0': '$\\pi$',
    '\u03c1': '$\\rho$', '\u03c3': '$\\sigma$',
    '\u03c4': '$\\tau$', '\u03c6': '$\\phi$',
    '\u03a6': '$\\Phi$', '\u03c8': '$\\psi$',
    '\u03a9': '$\\Omega$', '\u03c9': '$\\omega$',
    '\u2264': '$\\leq$', '\u2265': '$\\geq$',
    '\u2248': '$\\approx$', '\u2260': '$\\neq$',
    '\u221e': '$\\infty$', '\u2202': '$\\partial$',
    '\u2207': '$\\nabla$', '\u2211': '$\\sum$',
    '\u220f': '$\\prod$', '\u222b': '$\\int$',
    '\u221a': '$\\sqrt{}$', '\u2282': '$\\subset$',
    '\u2208': '$\\in$', '\u2209': '$\\notin$',
    '\u22c5': '$\\cdot$', '\u2022': '$\\bullet$',
    '\u00b7': '$\\cdot$', '\u0398': '$\\Theta$',
    '\u03be': '$\\xi$', '\u039e': '$\\Xi$',
    '\u03b6': '$\\zeta$', '\u0396': '$\\Zeta$',
}

for old, new in replacements.items():
    tex = tex.replace(old, new)

# Fix bad edits from earlier
tex = tex.replace(r'\usepackage{fontspec}\n\setmainfont{Latin Modern Roman}\n\documentclass', r'\documentclass')
tex = tex.replace(r'% \usepackage[utf8]{inputenc}', r'\usepackage{fontspec}')
tex = tex.replace(r'% \usepackage[T1]{fontenc}', '')
tex = tex.replace(r'% \usepackage{fontenc}', '')

# Remove empty fontenc lines
lines = tex.split('\n')
lines = [l for l in lines if l.strip() != r'\usepackage{fontenc}' and l.strip() != r'% \usepackage{fontenc}']
tex = '\n'.join(lines)

with open(r'latex\A1_CST.tex', 'w', encoding='utf-8') as f:
    f.write(tex)

# Report
problematic = []
for i, ch in enumerate(tex):
    if ord(ch) > 127:
        problematic.append(f'  Line ~{tex[:i].count(chr(10))+1}: U+{ord(ch):04X} ({ch})')

print(f'Written. Non-ASCII chars: {len(problematic)}')
if problematic:
    for p in problematic[:15]:
        print(p)
