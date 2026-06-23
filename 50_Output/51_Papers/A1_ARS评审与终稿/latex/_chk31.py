with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_FULLFIX.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\_L31_check.txt", "w", encoding="utf-8") as out:
    for i in range(26, 38):
        line = lines[i]
        out.write("L{}: {}\n".format(i+1, repr(line[:400])))

print("Written")
