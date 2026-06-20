import re

with open(r'latex\A1_CST.tex', 'r', encoding='utf-8') as f:
    tex = f.read()

# Complete Unicode math character replacement
replacements = {
    # Greek
    '\u0391': '$A$', '\u0392': '$B$', '\u0393': '$\Gamma$',
    '\u0394': '$\Delta$', '\u0395': '$E$', '\u0396': '$Z$',
    '\u0397': '$H$', '\u0398': '$\Theta$', '\u0399': '$I$',
    '\u039a': '$K$', '\u039b': '$\Lambda$', '\u039c': '$M$',
    '\u039d': '$N$', '\u039e': '$\Xi$', '\u039f': '$O$',
    '\u03a0': '$\Pi$', '\u03a1': '$P$', '\u03a3': '$\Sigma$',
    '\u03a4': '$T$', '\u03a5': '$\Upsilon$', '\u03a6': '$\Phi$',
    '\u03a7': '$X$', '\u03a8': '$\Psi$', '\u03a9': '$\Omega$',
    '\u03b1': '$\\alpha$', '\u03b2': '$\\beta$', '\u03b3': '$\\gamma$',
    '\u03b4': '$\\delta$', '\u03b5': '$\\epsilon$', '\u03b6': '$\\zeta$',
    '\u03b7': '$\\eta$', '\u03b8': '$\\theta$', '\u03b9': '$\\iota$',
    '\u03ba': '$\\kappa$', '\u03bb': '$\\lambda$', '\u03bc': '$\\mu$',
    '\u03bd': '$\\nu$', '\u03be': '$\\xi$', '\u03bf': '$o$',
    '\u03c0': '$\\pi$', '\u03c1': '$\\rho$', '\u03c2': '$\\varsigma$',
    '\u03c3': '$\\sigma$', '\u03c4': '$\\tau$', '\u03c5': '$\\upsilon$',
    '\u03c6': '$\\phi$', '\u03c7': '$\\chi$', '\u03c8': '$\\psi$',
    '\u03c9': '$\\omega$',
    # Math operators
    '\u2200': '$\\forall$', '\u2201': '$\\complement$',
    '\u2202': '$\\partial$', '\u2203': '$\\exists$',
    '\u2204': '$\\nexists$', '\u2205': '$\\emptyset$',
    '\u2207': '$\\nabla$', '\u2208': '$\\in$',
    '\u2209': '$\\notin$', '\u220b': '$\\ni$',
    '\u220f': '$\\prod$', '\u2211': '$\\sum$',
    '\u2212': '$-$', '\u2213': '$\\mp$',
    '\u2214': '$\\dotplus$', '\u2215': '$/$',
    '\u2217': '$\\ast$', '\u2218': '$\\circ$',
    '\u2219': '$\\bullet$', '\u221a': '$\\sqrt{}$',
    '\u221d': '$\\propto$', '\u221e': '$\\infty$',
    '\u2220': '$\\angle$', '\u2221': '$\\measuredangle$',
    '\u2225': '$\\parallel$', '\u2227': '$\\land$',
    '\u2228': '$\\lor$', '\u2229': '$\\cap$',
    '\u222a': '$\\cup$', '\u222b': '$\\int$',
    '\u222c': '$\\iint$', '\u222e': '$\\oint$',
    '\u2234': '$\\therefore$', '\u2235': '$\\because$',
    '\u223c': '$\\sim$', '\u2243': '$\\simeq$',
    '\u2245': '$\\cong$', '\u2248': '$\\approx$',
    '\u224d': '$\\asymp$', '\u2260': '$\\neq$',
    '\u2261': '$\\equiv$', '\u2264': '$\\leq$',
    '\u2265': '$\\geq$', '\u226a': '$\\ll$',
    '\u226b': '$\\gg$', '\u227a': '$\\prec$',
    '\u227b': '$\\succ$', '\u2282': '$\\subset$',
    '\u2283': '$\\supset$', '\u2286': '$\\subseteq$',
    '\u2287': '$\\supseteq$', '\u2295': '$\\oplus$',
    '\u2297': '$\\otimes$', '\u22a5': '$\\bot$',
    '\u22c5': '$\\cdot$', '\u22ee': '$\\vdots$',
    '\u22ef': '$\\cdots$', '\u22f0': '$\\ddots$',
    '\u2308': '$\\lceil$', '\u2309': '$\\rceil$',
    '\u230a': '$\\lfloor$', '\u230b': '$\\rfloor$',
    '\u27e8': '$\\langle$', '\u27e9': '$\\rangle$',
    # Arrows
    '\u2190': '$\\leftarrow$', '\u2191': '$\\uparrow$',
    '\u2192': '$\\rightarrow$', '\u2193': '$\\downarrow$',
    '\u2194': '$\\leftrightarrow$', '\u21d0': '$\\Leftarrow$',
    '\u21d1': '$\\Uparrow$', '\u21d2': '$\\Rightarrow$',
    '\u21d3': '$\\Downarrow$', '\u21d4': '$\\Leftrightarrow$',
    '\u27f5': '$\\longleftarrow$', '\u27f6': '$\\longrightarrow$',
    # Misc
    '\u00b1': '$\\pm$', '\u00b7': '$\\cdot$',
    '\u00d7': '$\\times$', '\u00f7': '$\\div$',
    '\u2020': '$\\dagger$', '\u2021': '$\\ddagger$',
    '\u2113': '$\\ell$', '\u2118': '$\\wp$',
    '\u2111': '$\\Im$', '\u211c': '$\\Re$',
    '\u2135': '$\\aleph$', '\u2190': '$\\leftarrow$',
    '\u2980': '$\\vert$', '\u00ac': '$\\neg$',
}

for old, new in replacements.items():
    tex = tex.replace(old, new)

# Fix natbib: use numbers style
tex = tex.replace(r'\usepackage{natbib}', r'\usepackage[numbers]{natbib}')

# Fix duplicate dollar signs from multiple passes
tex = re.sub(r'\$\$\$', '$', tex)
tex = re.sub(r'\$\$', '$', tex)
# Fix things like $$\alpha$ -> $\alpha$
tex = re.sub(r'\$(\$\\[a-z]+\$)\$', r'\1', tex)
# Fix empty sqrt
tex = tex.replace(r'$\sqrt{}$', r'$\sqrt{\ }$')

with open(r'latex\A1_CST.tex', 'w', encoding='utf-8') as f:
    f.write(tex)

# Count remaining non-ASCII
remaining = sum(1 for ch in tex if ord(ch) > 127)
print(f'Remaining non-ASCII chars: {remaining}')
