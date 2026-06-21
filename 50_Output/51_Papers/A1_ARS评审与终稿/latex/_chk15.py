with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_TRY.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\_L15.txt", "w", encoding="utf-8") as out:
    for i in range(0, 25):
        out.write("L{}: {}\n".format(i+1, repr(lines[i][:250])))

print("Written")
