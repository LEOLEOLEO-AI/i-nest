with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_TRY.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Find ALL unique \commands in the file
import re
cmds = set(re.findall(r"\\[a-zA-Z@]+", tex))

# Known standard LaTeX commands
standard = {
    "documentclass", "usepackage", "title", "author", "date",
    "begin", "end", "maketitle", "section", "subsection", "subsubsection",
    "textbf", "textit", "texttt", "textsc", "textsf", "textrm",
    "emph", "cite", "ref", "label", "caption", "centering",
    "hline", "toprule", "midrule", "bottomrule",
    "item", "enumerate", "itemize",
    "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta",
    "theta", "iota", "kappa", "lambda", "mu", "nu", "xi", "pi",
    "rho", "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega",
    "Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi",
    "Sigma", "Upsilon", "Phi", "Psi", "Omega",
    "cdot", "times", "approx", "sim", "simeq", "equiv",
    "propto", "pm", "mp",
    "leq", "geq", "neq", "ll", "gg",
    "in", "ni", "subset", "supset", "subseteq", "supseteq",
    "forall", "exists", "emptyset", "infty", "partial", "nabla",
    "rightarrow", "leftarrow", "Rightarrow", "Leftarrow",
    "longrightarrow", "mapsto", "to",
    "sum", "prod", "int", "oint",
    "sqrt", "frac", "mathbb", "mathcal", "mathbf", "mathit",
    "text", "textsubscript", "textsuperscript",
    "exp", "log", "ln", "sin", "cos", "tan", "max", "min",
    "left", "right", "big", "Big", "bigg", "Bigg",
    "langle", "rangle", "lbrace", "rbrace",
    "tag", "nonumber",
    "ensuremath",
    "hbox", "noindent", "newpage",
    "hspace", "vspace", "hfill", "vfill",
    "textwidth", "textheight",
    "newtheorem", "newcommand", "renewcommand", "providecommand",
    "input", "include",
    "setcounter", "addtocounter",
    "bibliography", "bibliographystyle",
    "multicolumn", "multirow", "cline",
    "footnote", "thanks",
    "textasciitilde", "textasciicircum", "textbackslash",
    "dag", "ddag", "S", "P", "copyright",
    "dots", "ldots", "cdots", "vdots", "ddots",
    "hat", "tilde", "bar", "vec", "dot", "ddot",
    "checkmark",
    "cong",
    "leftrightarrow",
    "checkmark",
    "acro",
    "acs",
    "H",
    "emph",
    "bf", "it", "rm", "sf", "tt", "sc",
    "bfseries", "itshape", "mdseries", "scshape",
    "large", "Large", "LARGE", "huge", "Huge", "small",
    "clearpage", "cleardoublepage", "appendix",
    "medskip", "bigskip", "smallskip",
    "par", "protect", "global", "long", "relax",
    "if", "else", "fi",
    "pagestyle", "thispagestyle", "pagenumbering",
    "def", "edef", "gdef",
    "let", "futurelet",
    "makeatletter", "makeatother",
    "ref", "pageref", "cite",
    "over", "atop", "choose",
    "rm", "bf", "it", "sl",
    "cal", "mit",
    "textregistered", "texttrademark",
    "url", "href", "hyperref",
}

unknown = cmds - standard
print("Unknown commands:")
for cmd in sorted(unknown):
    count = len(re.findall(re.escape(cmd), tex))
    # Show first occurrence context
    idx = tex.find(cmd)
    ctx = tex[max(0,idx-10):idx+len(cmd)+30].replace("\n", " ")
    print("  {} ({}x): ...{}...".format(cmd, count, ctx))
print("\nTotal unknown: {}".format(len(unknown)))
