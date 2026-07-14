with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Check if $\gamma$*_{}$ still exists
if "$\\gamma$*_{}$" in tex:
    print("BUG STILL EXISTS: $\\gamma$*_{}$")
    idx = tex.find("$\\gamma$*_{}$")
    print("Context: " + tex[max(0,idx-40):idx+80])
else:
    print("OK: $\\gamma$*_{}$ fixed")

# Check for _{}$
if "_{}$" in tex:
    count = tex.count("_{}$")
    print("Empty subscripts still present: " + str(count))
    idx = tex.find("_{}$")
    print("First: " + tex[max(0,idx-40):idx+40])
else:
    print("OK: No empty subscripts")
