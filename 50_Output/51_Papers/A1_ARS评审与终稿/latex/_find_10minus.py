with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Find the actual pattern around "10^{-}"
import re
for m in re.finditer(r'10.*?\^6', tex):
    ctx = tex[max(0,m.start()-10):m.end()+20]
    print("Pattern: [" + ctx + "]")
    print("  Repr: " + repr(ctx))

# Also find ALL $^{-} patterns
for m in re.finditer(r'\$\^\{-\}\$', tex):
    idx = m.start()
    ctx = tex[max(0,idx-30):idx+50]
    print("$^{-}$: [" + ctx.replace(chr(10),' ') + "]")
