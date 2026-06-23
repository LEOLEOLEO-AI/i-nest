with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\_L94.txt", "w", encoding="utf-8") as out:
    for i in range(85, 105):
        if i < len(lines):
            line = lines[i]
            # Count $ on this line
            dollars = line.count("$") - line.count("\\$")
            out.write("L{} ($={}): {}\n".format(i+1, dollars, line.rstrip()[:300]))

print("Written")
