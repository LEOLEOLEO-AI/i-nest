with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_BASELINE_FIX.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\_L30_40.txt", "w", encoding="utf-8") as out:
    for i in range(28, 45):
        line = lines[i]
        out.write(f"L{i+1} len={len(line)}: {repr(line[:300])}\n")
        out.write(f"  TEXT: {line.rstrip()[:300]}\n\n")
print("Written _L30_40.txt")
