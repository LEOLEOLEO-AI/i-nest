import re, os

# Read the working test_eq.tex to get preamble
with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\test_eq.tex", "r", encoding="utf-8") as f:
    test_tex = f.read()

# Extract preamble (up to \begin{document})
preamble_end = test_tex.find("\\begin{document}")
preamble = test_tex[:preamble_end].strip()
print(f"Preamble: {len(preamble)} chars")

# Read V32 content
with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\A1_CST_FromPDF_CLEAN.md", "r", encoding="utf-8") as f:
    text = f.read()

print(f"Source: {len(text)} chars, {len(text.splitlines())} lines")

# Unicode -> LaTeX mapping table
unicode_to_latex = {
    "\u03b1": "$\\alpha$", "\u03b2": "$\\beta$", "\u03b3": "$\\gamma$",
    "\u03b4": "$\\delta$", "\u03b5": "$\\epsilon$", "\u03b7": "$\\eta$",
    "\u03b8": "$\\theta$", "\u03bb": "$\\lambda$", "\u03bc": "$\\mu$",
    "\u03bd": "$\\nu$", "\u03c0": "$\\pi$", "\u03c1": "$\\rho$",
    "\u03c3": "$\\sigma$", "\u03c6": "$\\phi$",
    "\u03a6": "$\\Phi$", "\u03a8": "$\\Psi$", "\u0393": "$\\Gamma$",
    "\u0398": "$\\Theta$", "\u0394": "$\\Delta$",
    "\u221a": "$\\sqrt{}$",
    "\u223c": "$\\sim$", "\u2248": "$\\approx$",
    "\u2264": "$\\leq$", "\u2265": "$\\geq$",
    "\u2208": "$\\in$", "\u2192": "$\\rightarrow$",
    "\u00d7": "$\\times$", "\u00b7": "$\\cdot$",
    "\u2014": "---", "\u2013": "--",
    "\u2018": "'", "\u2019": "'",
    "\u201c": "``", "\u201d": "''",
    "\u00b1": "$\\pm$",
    "\u0338": "",
}

def clean_unicode(t):
    for u, l in unicode_to_latex.items():
        t = t.replace(u, l)
    return t

text = clean_unicode(text)

lines = text.splitlines()
output = []

# Preamble + begin
output.append(preamble)
output.append("\\begin{document}")
output.append("\\maketitle")
output.append("")

in_abstract = False
in_section = True
skip_toc = False
found_results = False
found_discussion = False
found_methods = False

i = 0
para_lines = []

def flush_para():
    global para_lines
    if para_lines:
        p = " ".join(para_lines).strip()
        if p:
            output.append(p)
            output.append("")
        para_lines = []

for line in lines:
    s = line.strip()
    
    # Skip empty lines between paragraphs (will handle with flush_para)
    if not s:
        flush_para()
        continue
    
    # Skip TOC
    if s == "Contents":
        skip_toc = True
        continue
    if skip_toc:
        if s.startswith("1 Introduction") or s.startswith("1"):
            continue
        if re.match(r"^(###|#)\s", s):
            skip_toc = False
        else:
            continue
    
    # Title
    if s.startswith("# ") and not s.startswith("## "):
        continue  # already in preamble
    if s.startswith("From Compute to Complexity") or s.startswith("A Physical"):
        continue
    
    # Author info
    if "Qinrang Liu" in s and "@" not in s and len(s) < 80:
        continue
    if s.startswith("School of") or s.startswith("Tianjin") or s.startswith("* Correspondence"):
        continue
    if s.startswith("Draft:") or s.startswith("40-system"):
        continue
    
    # Abstract
    if s == "## Abstract":
        flush_para()
        output.append("\\begin{abstract}")
        in_abstract = True
        continue
    
    if in_abstract and s.startswith("Keywords:"):
        flush_para()
        kw = s.replace("Keywords:", "").strip()
        output.append(f"\\noindent\\textbf{{Keywords:}} {kw}")
        output.append("\\end{abstract}")
        output.append("")
        in_abstract = False
        continue
    
    if in_abstract:
        para_lines.append(s)
        continue
    
    # Sections
    if s.startswith("# ") and "Introduction" in s:
        flush_para()
        output.append("\\section{Introduction}")
        output.append("")
        continue
    if s.startswith("# ") and "Results" in s:
        flush_para()
        output.append("\\section{Results}")
        output.append("")
        found_results = True
        continue
    if s.startswith("# ") and "Discussion" in s:
        flush_para()
        output.append("\\section{Discussion}")
        output.append("")
        found_discussion = True
        continue
    if s.startswith("# ") and "Methods" in s:
        flush_para()
        output.append("\\section{Methods}")
        output.append("")
        found_methods = True
        continue
    if s.startswith("# ") and "References" in s:
        flush_para()
        output.append("\\section*{References}")
        output.append("")
        continue
    
    # Subsections
    if s.startswith("### "):
        flush_para()
        sub = s[4:].strip()
        output.append(f"\\subsection{{{sub}}}")
        output.append("")
        continue
    
    # Sub-subsections
    if s.startswith("#### "):
        flush_para()
        subsub = s[5:].strip()
        output.append(f"\\subsubsection{{{subsub}}}")
        output.append("")
        continue
    
    # Skip reference bracket numbers at line start
    if re.match(r"^\[\d+\]", s):
        continue
    
    # Regular paragraph text
    para_lines.append(s)

flush_para()

# Add \end{document}
output.append("\\end{document}")

# Join and write
result = "\n".join(output)

# Fix common issues
# Fix scattered math mode: $X$\cdot$Y$ -> $X \cdot Y$
result = re.sub(r'\$(\w+)\$\\cdot\$(\w+)\$', r'$\1 \\cdot \2$', result)
result = re.sub(r'\$(\w+)\$\\cdot\$(\w+)\$', r'$\1 \\cdot \2$', result)

# Clean up double spaces
result = re.sub(r'  +', ' ', result)

# Fix line length - wrap at ~500 chars
wrapped = []
for line in result.split("\n"):
    if len(line) <= 500:
        wrapped.append(line)
    else:
        # Try to break at spaces
        while len(line) > 500:
            break_point = line.rfind(" ", 0, 500)
            if break_point < 100:
                break_point = line.find(" ", 400)
            if break_point < 0:
                break_point = 500
            wrapped.append(line[:break_point])
            line = line[break_point:].strip()
        if line:
            wrapped.append(line)

result = "\n".join(wrapped)

out_path = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_CLEAN_v1.tex"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(result)

print(f"Output: {len(result)} chars, {len(result.splitlines())} lines")
print(f"Written to: A1_CST_CLEAN_v1.tex")
