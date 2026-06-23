with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_FULLFIX.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

running = 0
for i, line in enumerate(lines):
    dollars = line.count("$") - line.count("\\$")
    running += dollars
    if running % 2 != 0:
        # We're in open math mode - but if running stays odd, that's the problem area
        pass

# Find the FIRST position where running becomes odd and find where it resolves
# Actually, let me find where running stays odd
running = 0
odd_start = -1
for i, line in enumerate(lines):
    dollars = line.count("$") - line.count("\\$")
    running += dollars
    if odd_start < 0 and running % 2 != 0:
        odd_start = i
        print("Math opens at L{} (running={}): {}".format(i+1, running, line.rstrip()[:200]))
    if odd_start >= 0 and running % 2 == 0:
        # Math resolved
        odd_start = -1

# If file ends with odd running, find the last odd-start
if running % 2 != 0:
    # Re-scan from end
    running = 0
    for i, line in enumerate(lines):
        dollars = line.count("$") - line.count("\\$")
        running += dollars

    # Binary search approach: find where it goes odd
    running = 0
    for i, line in enumerate(lines):
        dollars = line.count("$") - line.count("\\$")
        old = running
        running += dollars
        if old % 2 == 0 and running % 2 != 0:
            print("\n>>> UNMATCHED $ OPEN near L{}:".format(i+1))
            print("    " + line.rstrip()[:300])
            # Show surrounding lines
            for j in range(max(0,i-2), min(len(lines),i+3)):
                print("    L{}: {}".format(j+1, lines[j].rstrip()[:200]))
            break

    print("\nTotal running $: {} (odd = unbalanced)".format(running))
