with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_FULLFIX.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

running = 0
for i in range(0, 65):
    line = lines[i]
    dollars = line.count("$") - line.count("\\$")
    old = running
    running += dollars
    if old % 2 == 0 and running % 2 != 0:
        print(">>> IMBALANCE starts at L{} (running {}->{}):".format(i+1, old, running))
        print("    " + line.rstrip()[:300])
    if running % 2 != 0:
        print("  L{}: running={} | {}".format(i+1, running, line.rstrip()[:150]))
