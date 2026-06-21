with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Trace $ from line 1 to 20
running = 0
for i in range(0, 20):
    line = lines[i]
    dollars = line.count("$") - line.count("\\$")
    running += dollars
    if dollars > 0:
        print("L{}: +{} = {} | {}".format(i+1, dollars, running, line.rstrip()[:150]))
    if running % 2 != 0:
        print("  >>> UNBALANCED at L{} (running={})".format(i+1, running))

print("\nFinal running: " + str(running))
