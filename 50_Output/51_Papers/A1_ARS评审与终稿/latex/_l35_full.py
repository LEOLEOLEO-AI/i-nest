with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_FINAL_ATTEMPT.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Full content of line 35
line35 = lines[34]
print("L35 full length: " + str(len(line35)))
print("L35 tail (last 500 chars):")
print(repr(line35[-500:]))
