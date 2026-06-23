with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(144, 158):
    if i < len(lines):
        line = lines[i]
        # Highlight issues
        in_math = False
        j = 0
        issues = []
        while j < len(line):
            if line[j:j+2] == "\\$": j += 2; continue
            if line[j] == "$": in_math = not in_math; j += 1; continue
            if line[j] == "_" and not in_math and (j==0 or line[j-1]!="\\"):
                issues.append("_@" + str(j))
            if line[j] == "\\" and not in_math:
                end = j+1
                while end < len(line) and line[end].isalpha(): end += 1
                cmd = line[j:end]
                if cmd in ["\\alpha","\\Gamma","\\cdot","\\approx","\\sim","\\geq","\\leq","\\neq","\\in","\\pm","\\sqrt","\\times","\\phi","\\pi","\\delta","\\theta","\\lambda","\\mu","\\sigma","\\exp"]:
                    issues.append(cmd + "@" + str(j))
            j += 1
        
        tag = " *** " + ",".join(issues) if issues else ""
        print("L{}: {}{}".format(i+1, line.rstrip()[:250], tag))
