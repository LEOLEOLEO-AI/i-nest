with open(r"D:\Obsidian\vault\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

line35 = lines[34]
# Show around positions 440-500
print(repr(line35[430:510]))
