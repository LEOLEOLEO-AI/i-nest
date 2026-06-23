with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

line = lines[140]
in_math = False
j = 0
while j < len(line):
    if line[j:j+2] == "\\$": j += 2; continue
    if line[j] == "$": in_math = not in_math; j += 1; continue
    if line[j] == "_" and not in_math and (j==0 or line[j-1]!="\\"):
        print("TXT_ at " + str(j) + ": [" + line[max(0,j-30):j+30] + "]")
    if line[j] == "\\" and not in_math:
        end = j+1
        while end < len(line) and line[end].isalpha(): end += 1
        cmd = line[j:end]
        if cmd in ["\\alpha","\\Gamma","\\cdot","\\approx","\\sim","\\geq","\\leq","\\neq","\\in","\\pm","\\sqrt","\\times","\\phi","\\pi","\\delta","\\theta","\\lambda","\\exp"]:
            print("TXT_CMD " + cmd + " at " + str(j) + ": [" + line[max(0,j-20):j+30] + "]")
    j += 1

print("\nL141: " + line.rstrip()[:250])
