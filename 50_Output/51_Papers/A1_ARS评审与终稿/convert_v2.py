import re, os, sys

# Read paper
with open('A1_CST_Theory_V32_MERGED.md', 'r', encoding='gbk') as f:
    content = f.read()

# Remove YAML
content = re.sub(r'^---\n.*?---\n', '', content, flags=re.DOTALL)
lines = content.split('\n')

# Build body lines (skip preamble metadata)
body_start = False
body_lines = []
ref_lines = []
post_lines = []
in_refs = False
in_post = False

for line in lines:
    s = line.strip()
    
    # Detect section starts
    if s.startswith('## References'):
        in_refs = True
        continue
    if in_refs:
        if s.startswith('## '):
            in_refs = False
            in_post = True
            post_lines.append(s)
        elif s:
            ref_lines.append(s)
        continue
    if in_post:
        if s:
            post_lines.append(s)
        continue
    
    if not body_start:
        if s.startswith('## 1. Introduction') or s.startswith('## Introduction'):
            body_start = True
        else:
            continue
    
    body_lines.append(line)

# Now convert to LaTeX
def esc(s):
    """Escape LaTeX special chars in regular text"""
    # Protect math first
    parts = re.split(r'(\$[^$]+\$)', s)
    result = []
    for i, part in enumerate(parts):
        if part.startswith('$') and part.endswith('$'):
            result.append(part)
        else:
            part = part.replace('\\', '\\textbackslash{}')
            part = part.replace('&', '\\&')
            part = part.replace('%', '\\%')
            part = part.replace('#', '\\#')
            part = part.replace('_', '\\_')
            part = part.replace('{', '\\{')
            part = part.replace('}', '\\}')
            part = part.replace('~', '\\textasciitilde{}')
            part = part.replace('^', '\\textasciicircum{}')
            # Unicode chars
            part = part.replace('\u2014', '---')
            part = part.replace('\u2013', '--')
            part = part.replace('\u2018', "'")
            part = part.replace('\u2019', "'")
            part = part.replace('\u201c', "``")
            part = part.replace('\u201d', "''")
            part = part.replace('\u2026', '...')
            part = part.replace('\u00d7', '$\\times$')
            part = part.replace('\u00b1', '$\\pm$')
            part = part.replace('\u2192', '$\\rightarrow$')
            part = part.replace('\u03b1', '$\\alpha$')
            part = part.replace('\u03b2', '$\\beta$')
            part = part.replace('\u03b3', '$\\gamma$')
            part = part.replace('\u0393', '$\\Gamma$')
            part = part.replace('\u03b4', '$\\delta$')
            part = part.replace('\u03b7', '$\\eta$')
            part = part.replace('\u03c1', '$\\rho$')
            part = part.replace('\u03c6', '$\\phi$')
            part = part.replace('\u03c0', '$\\pi$')
            part = part.replace('\u03a9', '$\\Omega$')
            part = part.replace('\u221e', '$\\infty$')
            part = part.replace('\u2248', '$\\approx$')
            part = part.replace('\u2264', '$\\leq$')
            part = part.replace('\u2265', '$\\geq$')
            result.append(part)
    return ''.join(result)

latex = []
latex.append('\\documentclass[a4paper,12pt]{article}')
latex.append('\\usepackage{fontspec}')
latex.append('\\usepackage{amsmath,amssymb}')
latex.append('\\usepackage{graphicx}')
latex.append('\\usepackage[hidelinks]{hyperref}')
latex.append('\\usepackage[margin=2.5cm]{geometry}')
latex.append('\\usepackage{natbib}')
latex.append('\\usepackage{booktabs,array,float}')
latex.append('')
latex.append('\\title{From Compute to Complexity: A Physical Theory of Intelligence Emergence}')
latex.append('\\author{Qinrang Liu\\\\\\texttt{qinrangliu@fudan.edu.cn}}')
latex.append('\\date{June 19, 2026}')
latex.append('')
latex.append('\\begin{document}')
latex.append('\\maketitle')

# Abstract (roughly lines 24-30 in original)
latex.append('')
latex.append('\\begin{abstract}')
abstract = 'The rapid scaling of large language models has delivered remarkable functional capabilities yet produced exponentially growing energy costs with sub-linear returns. We argue that this trajectory pursues the wrong variable: compute rather than complexity. Von Neumann identified in 1948 that intelligence requires a complexity threshold; here we quantify that threshold through a framework grounded in thermodynamic phase transitions, renormalization group theory, and complex network science. The result is the Coordination Spatiotemporal Complexity theorem: CST = (S\\_c $\\cdot$ T\\_c) $\\cdot$ exp($\\alpha$ $\\cdot$ $\\Gamma$\\_st), where structural integration, dynamical richness, and their physical coupling jointly determine emergent intelligence potential. We derive six universal thresholds and validate across 40 biological and artificial systems (Spearman $\\rho$ = 0.976). Intelligence Efficiency $\\eta$\\_I reveals an approximately six-order-of-magnitude gap between brains and current AI, and a four-generation hardware roadmap identifies the physically necessary path from present systems to general intelligence.'
latex.append(esc(abstract))
latex.append('\\end{abstract}')
latex.append('')

# Process body sections
fig_count = 0

for line in body_lines:
    s = line.strip()
    
    if not s:
        latex.append('')
        continue
    
    # Skip metadata lines
    if s.startswith('**Version') or s.startswith('**Target') or s.startswith('**Status'):
        continue
    
    # Section headers
    m = re.match(r'^##\s+(\d+)\.\s+(.+)', s)
    if m:
        latex.append('\\section{' + esc(m.group(2)) + '}')
        continue
    
    m = re.match(r'^###\s+(\d+\.\d+)\s+(.+)', s)
    if m:
        latex.append('\\subsection{' + esc(m.group(2)) + '}')
        continue
    
    m = re.match(r'^###\s+(.+)', s)
    if m and not s.startswith('### The '):
        latex.append('\\subsection{' + esc(m.group(1)) + '}')
        continue
    
    # Figures
    if '<img src="figures_cst/' in s:
        m = re.search(r'figures_cst/(.+?)\.png', s)
        if m:
            fig_count += 1
            fn = m.group(1)
            latex.append('\\begin{figure}[H]')
            latex.append('\\centering')
            latex.append('\\includegraphics[width=0.95\\textwidth]{../figures_cst/' + fn + '.png}')
        continue
    
    if '<p align="center"><b>' in s:
        caption = re.sub(r'<[^>]+>', '', s)
        caption = caption.replace('<b>', '').replace('</b>', '')
        latex.append('\\caption{' + esc(caption) + '}')
        latex.append('\\label{fig:' + str(fig_count) + '}')
        latex.append('\\end{figure}')
        latex.append('')
        continue
    
    # Bold
    s = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', s)
    
    # Display math $$...$$ -> \[...\]
    s = re.sub(r'\$\$(.+?)\$\$', r'\\[\1\\]', s)
    
    # Regular text
    latex.append(esc(s))
    latex.append('')

# References
latex.append('\\begin{thebibliography}{99}')
for r in ref_lines:
    m = re.match(r'\[(\d+)\]\s+(.+)', r)
    if m:
        num = m.group(1)
        text = m.group(2)
        text = text.replace('&', '\\&').replace('%', '\\%').replace('#', '\\#')
        text = text.replace('_', '\\_').replace('$', '\\$').replace('^', '\\textasciicircum{}')
        text = text.replace('\u2013', '--').replace('\u2014', '---')
        latex.append('\\bibitem{ref' + num + '} ' + esc(text))
latex.append('\\end{thebibliography}')
latex.append('')

# Post sections
for line in post_lines:
    s = line.strip()
    if not s:
        continue
    m = re.match(r'^##\s+(.+)', s)
    if m:
        latex.append('\\section*{' + esc(m.group(1)) + '}')
        continue
    latex.append(esc(s))
    latex.append('')

latex.append('\\end{document}')

with open('latex\\A1_CST.tex', 'w', encoding='utf-8') as f:
    f.write('\n'.join(latex))

print(f'Written: {len(latex)} lines')
