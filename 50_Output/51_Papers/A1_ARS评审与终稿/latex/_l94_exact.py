with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

line94 = lines[93]
# Show around position 960-1000
print("Chars 960-1010:")
print(repr(line94[960:1010]))
print()
# Show full context  
idx = line94.find("gamma_{")
if idx >= 0:
    print("Context around gamma_: [" + line94[max(0,idx-20):idx+80] + "]")

# Look for any remaining _ in text mode
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
        ctx = line94[max(0,j-20):j+40]
        issues.append("pos " + str(j) + ": [" + ctx + "]")
    j += 1

for issue in issues:
    print("TEXT _ : " + issue)
