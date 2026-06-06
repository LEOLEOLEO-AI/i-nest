
import os

tex = r'''\documentclass[review,3p,twocolumn]{elsarticle}
% Engineering — v3.0 Paradigm Innovation Focus
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage[numbers,sort&compress]{natbib}
\journal{Engineering}
\begin{document}
\begin{frontmatter}
\title{From Node-Centric to Network-Centric: The Computing Paradigm Shift Driven by the Data Movement Wall}
\author[1]{Qinrang Liu\corref{cor1}}
\ead{liuqinrang@tju.edu.cn}
\address[1]{TCC iNEST Research Group, Tianjin University, Tianjin 300072, China}
\cortext[cor1]{Corresponding author.}
\begin{abstract}
Computing stands at a paradigm boundary. For eight decades, the von Neumann architecture has defined computation as operations executed on a centralized processor—a node-centric model. Three converging forces now make this model architecturally obsolete: (1) the data movement wall, where memory access energy exceeds computation energy by 350--700$\times$ at 45nm and the gap widens at each process node; (2) the collapse of operator diversity across domains, with the union of x86-64, ARMv9, RISC-V, CUDA PTX, and Hexagon ISAs converging to exactly ten primitives; and (3) the emergence of runtime-reconfigurable interconnects that dissolve the design-time topology constraint. This paper marshals evidence from 62 systematically reviewed papers and 10 commercial interconnects to argue a central thesis: \emph{the fundamental unit of computation is shifting from the processor node to the network topology itself.} We formalize this through (i) an ISA-verified proof that all computation reduces to ten operators and eleven data-movement meta-primitives; (ii) an analytical model showing that topology reconfiguration yields 20--35\% throughput improvement at $N\geq64$ nodes; and (iii) the Liquid Unified Architecture, which synthesizes fixed operators with programmable interconnect to realize network-centric computing. We conclude with a 15-year roadmap for the paradigm transition.
\end{abstract}
\begin{keyword}
computing paradigm shift \sep network-centric computing \sep data movement wall \sep software-defined interconnect \sep operator-data movement decomposition \sep liquid hardware architecture
\end{keyword}
\end{frontmatter}
'''

with open(r'D:\Obsidian\home\work\.openclaw\workspace\submission\manuscript_v3_p1.tex', 'w', encoding='utf-8') as f:
    f.write(tex)
print('Part 1 written')
