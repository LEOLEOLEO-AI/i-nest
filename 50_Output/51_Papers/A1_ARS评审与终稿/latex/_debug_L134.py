with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_V9_FINALFIX.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Check lines 130-140 in detail
for i in range(127, 145):
    line = lines[i].rstrip()
    print(f"L{i+1}: [{line[:300]}]")

# Also search for problematic patterns around line 134
# Missing $ usually from _ or ^ in text mode
import re
line134 = lines[133] if len(lines) > 133 else ""
print(f"\n--- Line 134 full ---")
print(repr(line134[:500]))
