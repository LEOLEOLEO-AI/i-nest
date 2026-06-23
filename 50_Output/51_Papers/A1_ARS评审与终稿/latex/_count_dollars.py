with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_FULLFIX.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Count $ on lines 28-32, also check for math commands
for i in range(26, 40):
    line = lines[i].rstrip()
    dollars = line.count("$") - line.count("\\$")
    if dollars > 0:
        print("L{}: {} $ signs | {}".format(i+1, dollars, line[:150]))

# Check entire file for $ imbalance
total_dollars = 0
for i, line in enumerate(lines):
    dollars = line.count("$") - line.count("\\$")
    total_dollars += dollars
    # If a line has odd $ count, it might span math across lines
    if dollars % 2 != 0:
        pass  # This is normal for multi-line math

print("\nTotal $ in file (odd=" + str(total_dollars % 2) + "): " + str(total_dollars))
print("(Even = balanced, Odd = unbalanced)")
