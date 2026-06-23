with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Lines 30-42
for i in range(28, 45):
    if i < len(lines):
        line = lines[i]
        # Check for issues: _ ^ or \cmd in text mode
        in_math = False
        issues = []
        j = 0
        while j < len(line):
            if line[j:j+2] == "\\$": j += 2; continue
            if line[j] == "$": in_math = not in_math; j += 1; continue
            if line[j] == "_" and not in_math and (j==0 or line[j-1]!="\\"):
                issues.append("TXT_ at " + str(j))
            if line[j] == "^" and not in_math:
                issues.append("TXT^ at " + str(j))
            if line[j] == "\\" and not in_math:
                end = j+1
                while end < len(line) and line[end].isalpha(): end += 1
                cmd = line[j:end]
                if cmd in ["\\alpha","\\beta","\\gamma","\\delta","\\Gamma","\\Phi","\\Psi","\\Theta","\\Omega","\\cdot","\\times","\\approx","\\sim","\\geq","\\leq","\\neq","\\in","\\pm","\\sqrt","\\frac"]:
                    issues.append("TXT_CMD " + cmd + " at " + str(j))
            j += 1
        
        tag = " *** " + ",".join(issues) if issues else ""
        print("L{}: {} {}".format(i+1, line.rstrip()[:200], tag))
