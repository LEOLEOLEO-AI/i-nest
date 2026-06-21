import re
with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_FINAL_ATTEMPT.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Check lines 30-40 with dollar counting
running = 0
with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\_L36_DEEP.txt", "w", encoding="utf-8") as out:
    for i in range(26, 45):
        line = lines[i]
        dollars = line.count("$") - line.count("\\$")
        running += dollars
        out.write("L{} (running={}): {}\n".format(i+1, running, repr(line[:400])))
        # Also check for _ or ^ in text mode (when running is even = in text mode)
        in_math = False
        j = 0
        txt_issues = []
        while j < len(line):
            if line[j:j+2] == "\\$":
                j += 2; continue
            if line[j] == "$":
                in_math = not in_math
                j += 1; continue
            if (line[j] == "_" or line[j] == "^") and not in_math and (j == 0 or line[j-1] != "\\"):
                ctx_start = max(0, j-15)
                ctx_end = min(len(line), j+15)
                txt_issues.append("pos {}: {}...".format(j, line[ctx_start:ctx_end].replace("\n"," ")))
            j += 1
        if txt_issues:
            for issue in txt_issues:
                out.write("  TXT ISSUE: {}\n".format(issue))

print("Written _L36_DEEP.txt")
