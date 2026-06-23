import re
# Run the fix 3 more times to catch remaining issues
for iteration in range(3):
    with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
        tex = f.read()
    
    # Simple regex: $_ followed by letters in text mode
    # Find all $_<letters> patterns and wrap in $...$
    # This is a more aggressive fix
    pat = re.compile(r'\$([^$]+)\$\s*_\s*([a-zA-Z]+)')
    fixes = 0
    while pat.search(tex):
        tex, cnt = pat.subn(r'$\1_{\2}$', tex)
        fixes += cnt
        if fixes > 50: break
    
    # Also find $...$_{...} patterns
    pat2 = re.compile(r'\$([^$]+)\$\s*_\{([^}]+)\}')
    f2 = 0
    while pat2.search(tex):
        tex, cnt = pat2.subn(r'$\1_{\2}$', tex)
        f2 += cnt
        if f2 > 50: break
    
    # Clean up $$
    tex = tex.replace("$$", "")
    
    with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "w", encoding="utf-8") as f:
        f.write(tex)
    
    print("Pass " + str(iteration+1) + ": " + str(fixes + f2) + " fixes")

print("Done")
