import os, re, sys

paper_path = sys.argv[1]
out_path = sys.argv[2]
figures_dir = sys.argv[3]

with open(paper_path, 'r', encoding='gbk') as f:
    content = f.read()

# Remove YAML frontmatter
content = re.sub(r'^---\n.*?---\n', '', content, flags=re.DOTALL)

lines = content.split('\n')

# Extract header info
title = ""
author = ""
email = ""
abstract_lines = []
keywords = ""

in_abstract = False
in_header = True
i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith('# ') and not title:
        title = line[2:].strip()
    elif line.startswith('**') and 'Correspondence' not in line and not author:
        m = re.match(r'\*\*(.+?)\*\*', line)
        if m:
            author = m.group(1).strip()
    elif 'Correspondence:' in line and not email:
        email = re.search(r'[\w.]+@[\w.]+', line)
        if email:
            email = email.group(0)
    elif line.startswith('## Abstract'):
        in_abstract = True
    elif in_abstract and line.startswith('## '):
        in_abstract = False
    elif in_abstract:
        abstract_lines.append(line)
    elif '**Keywords:**' in line:
        keywords = line.replace('**Keywords:**', '').strip()
    i += 1

abstract = ' '.join(abstract_lines).strip()

# Build LaTeX
latex = []
latex.append(r'\documentclass[a4paper,12pt]{article}')
latex.append(r'\usepackage[utf8]{inputenc}')
latex.append(r'\usepackage[T1]{fontenc}')
latex.append(r'\usepackage{amsmath,amssymb,amsfonts}')
latex.append(r'\usepackage{graphicx}')
latex.append(r'\usepackage{hyperref}')
latex.append(r'\usepackage{geometry}')
latex.append(r'\usepackage{natbib}')
latex.append(r'\usepackage{booktabs}')
latex.append(r'\usepackage{array}')
latex.append(r'\usepackage{float}')
latex.append(r'\geometry{margin=2.5cm}')
latex.append(r'')
latex.append(r'\title{' + title + '}')
latex.append(r'\author{' + author + r'\\')
latex.append(r'\texttt{' + email + r'}}')
latex.append(r'\date{June 19, 2026}')
latex.append(r'')
latex.append(r'\begin{document}')
latex.append(r'\maketitle')
latex.append(r'')
latex.append(r'\begin{abstract}')
latex.append(abstract)
latex.append(r'\end{abstract}')
latex.append(r'')

# Process body sections
current_section = None
in_figure = False
skip_until_section = False
body_start = False

for line in lines:
    stripped = line.strip()
    
    # Skip until after abstract and keywords
    if not body_start:
        if stripped.startswith('## 1. Introduction') or stripped.startswith('## Introduction'):
            body_start = True
        else:
            continue
    
    # Handle sections
    if stripped.startswith('## References'):
        break
    if re.match(r'^##\s+\d+\.\s+', stripped):
        sec_title = re.sub(r'^##\s+\d+\.\s+', '', stripped)
        latex.append(r'\section{' + sec_title + '}')
        current_section = 'section'
        continue
    if re.match(r'^###\s+\d+\.\d+\s+', stripped):
        sub_title = re.sub(r'^###\s+\d+\.\d+\s+', '', stripped)
        latex.append(r'\subsection{' + sub_title + '}')
        current_section = 'subsection'
        continue
    if stripped.startswith('## '):
        sec_title = re.sub(r'^##\s+', '', stripped)
        latex.append(r'\section{' + sec_title + '}')
        current_section = 'section'
        continue
    if stripped.startswith('### '):
        sub_title = re.sub(r'^###\s+', '', stripped)
        latex.append(r'\subsection{' + sub_title + '}')
        current_section = 'subsection'
        continue
    
    # Handle figures
    if '<img src="figures_cst/' in stripped:
        m = re.search(r'figures_cst/(.+)\.png"', stripped)
        if m:
            fig_file = m.group(1)
            latex.append(r'\begin{figure}[H]')
            latex.append(r'\centering')
            latex.append(r'\includegraphics[width=0.95\textwidth]{' + figures_dir.replace('\\', '/') + '/' + fig_file + '.png}')
        in_figure = True
        continue
    
    if in_figure and '<p align="center"><b>' in stripped:
        caption = re.sub(r'<[^>]+>', '', stripped)
        caption = caption.replace('<b>', '').replace('</b>', '')
        latex.append(r'\caption{' + caption + '}')
        latex.append(r'\label{fig:' + fig_file + '}')
        latex.append(r'\end{figure}')
        latex.append(r'')
        in_figure = False
        continue
    
    # Handle math
    stripped_math = re.sub(r'\$\$(.+?)\$\$', r'\\[\1\\]', stripped)
    stripped_math = re.sub(r'\$(.+?)\$', r'$\1$', stripped_math)
    
    # Handle bold/italic
    stripped_math = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', stripped_math)
    
    # Skip empty lines and metadata lines
    if not stripped_math:
        latex.append('')
        continue
    if stripped_math.startswith('**Version') or stripped_math.startswith('**Target') or stripped_math.startswith('**Status'):
        continue
    
    # Regular paragraph
    latex.append(stripped_math)
    latex.append('')

# Add references
latex.append(r'\section*{References}')
latex.append(r'\begin{thebibliography}{99}')

ref_lines = []
in_refs = False
for line in lines:
    if '## References' in line:
        in_refs = True
        continue
    if in_refs:
        if line.startswith('## '):
            break
        ref_lines.append(line)

# Process references
for ref_line in ref_lines:
    ref_line = ref_line.strip()
    if not ref_line:
        continue
    # Format: [1] Author et al. Title. Journal, Year.
    m = re.match(r'\[(\d+)\]\s+(.+)', ref_line)
    if m:
        num = m.group(1)
        text = m.group(2)
        # Escape special LaTeX chars
        text = text.replace('&', '\\&').replace('%', '\\%').replace('#', '\\#')
        text = text.replace('_', '\\_')
        latex.append(r'\bibitem{ref' + num + '} ' + text)

latex.append(r'\end{thebibliography}')
latex.append(r'')

# Author Contributions (if present after References)
in_ac = False
ac_lines = []
for line in lines:
    if '## Author Contributions' in line:
        in_ac = True
        continue
    if in_ac:
        if line.startswith('## '):
            break
        if line.strip():
            ac_lines.append(line.strip())

if ac_lines:
    latex.append(r'\section*{Author Contributions}')
    latex.append(' '.join(ac_lines))
    latex.append('')

# Competing Interests
in_ci = False
ci_lines = []
for line in lines:
    if '## Competing Interests' in line:
        in_ci = True
        continue
    if in_ci:
        if line.startswith('## '):
            break
        if line.strip():
            ci_lines.append(line.strip())

if ci_lines:
    latex.append(r'\section*{Competing Interests}')
    latex.append(' '.join(ci_lines))
    latex.append('')

# Data Availability
in_da = False
da_lines = []
for line in lines:
    if '## Data Availability' in line:
        in_da = True
        continue
    if in_da:
        if line.startswith('## '):
            break
        if line.strip():
            da_lines.append(line.strip())

if da_lines:
    latex.append(r'\section*{Data Availability}')
    latex.append(' '.join(da_lines))
    latex.append('')

# AI Declaration
in_ai = False
ai_lines = []
for line in lines:
    if '## AI-Assistance Declaration' in line:
        in_ai = True
        continue
    if in_ai:
        if line.strip():
            ai_lines.append(line.strip())

if ai_lines:
    latex.append(r'\section*{AI-Assistance Declaration}')
    latex.append(' '.join(ai_lines))
    latex.append('')

latex.append(r'\end{document}')

# Write output
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(latex))

print(f'LaTeX written to: {out_path}')
print(f'Total lines: {len(latex)}')
