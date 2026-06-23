with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

line94 = lines[93]
print("L94 full length: " + str(len(line94)))
print("L94 full text:")
print(line94)

# Check for any _ or ^ or \commands not in math mode
import re
in_math = False
j = 0
issues = []
while j < len(line94):
    if line94[j:j+2] == "\\$":
        j += 2; continue
    if line94[j] == "$":
        in_math = not in_math
        j += 1; continue
    if line94[j] == "_" and not in_math and (j == 0 or line94[j-1] != "\\"):
        ctx = line94[max(0,j-20):j+20]
        issues.append("TXT_ at pos " + str(j) + ": [" + ctx + "]")
    if line94[j] == "^" and not in_math:
        ctx = line94[max(0,j-20):j+20]
        issues.append("TXT^ at pos " + str(j) + ": [" + ctx + "]")
    # Check for \commands in text mode
    if line94[j] == "\\" and not in_math and j+1 < len(line94):
        end = j+1
        while end < len(line94) and line94[end].isalpha():
            end += 1
        cmd = line94[j:end]
        if len(cmd) > 1:
            issues.append("TXT_CMD at pos " + str(j) + ": " + cmd)
        j = end - 1
    j += 1

for issue in issues:
    print(issue)
if not issues:
    print("No text-mode issues found on L94")
