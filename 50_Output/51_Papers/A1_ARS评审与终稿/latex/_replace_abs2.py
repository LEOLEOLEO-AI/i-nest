with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\test_eq.tex", "r", encoding="utf-8") as f:
    test_eq = f.read()

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    dd = f.read()

# Find abstract boundaries via string positions
abs_start = dd.find("\\begin{abstract}")
abs_end = dd.find("\\end{abstract}") + len("\\end{abstract}")

test_abs_start = test_eq.find("\\begin{abstract}")
test_abs_end = test_eq.find("\\end{abstract}") + len("\\end{abstract}")
test_abs = test_eq[test_abs_start:test_abs_end]

# Replace
dd_new = dd[:abs_start] + test_abs + dd[abs_end:]

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "w", encoding="utf-8") as f:
    f.write(dd_new)

print("Abstract replaced: " + str(len(dd_new)) + " chars")
