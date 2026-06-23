with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(54, 68):
    if i < len(lines):
        print("L{}: {}".format(i+1, lines[i].rstrip()[:200]))
