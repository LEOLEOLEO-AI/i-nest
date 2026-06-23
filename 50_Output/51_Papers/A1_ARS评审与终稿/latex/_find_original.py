with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\_BASELINE_A1_CST.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the original line with "CST = 0.486"  
for i, line in enumerate(lines):
    if "CST = 0.486" in line:
        print("Original L{}: {}".format(i+1, line[:500]))
    if "gamma_{_geo}" in line or "gamma$*" in line:
        print("Original L{}: {}".format(i+1, line[:500]))
