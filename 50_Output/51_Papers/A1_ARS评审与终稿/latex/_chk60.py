with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Lines 55-70 with dollar tracking
running = 0
with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\_L60.txt", "w", encoding="utf-8") as out:
    for i in range(50, 75):
        if i >= len(lines): break
        line = lines[i]
        dollars = line.count("$") - line.count("\\$")
        running += dollars
        out.write("L{} (running={} dollars={}): {}\n".format(i+1, running, dollars, line.rstrip()[:300]))

print("Written")
