with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_V9_FINALFIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# \Gamm is a SUBSTRING of \Gamma. Need to search for \Gamm NOT followed by 'a'
# Actually \Gamm should NOT exist at all in the fixed file
# Count actual \Gamm (not as substring of \Gamma)
import re
# \Gamm not followed by 'a'
gamm_standalone = len(re.findall(r'\\Gamm(?!a)', tex))
# \Gamma (the full command)
gamma_full = len(re.findall(r'\\Gamma', tex))
print(f"Standalone \\Gamm: {gamm_standalone}")
print(f"Full \\Gamma: {gamma_full}")

# Show a few \Gamma examples
for m in re.finditer(r'\\Gamma', tex):
    ctx = tex[m.start():m.end()+30].replace(chr(10), " ")
    print(f"  [{ctx[:80]}]")
    break  # just show first

# Check undefined commands
for bad in [r"\SData", r"\dagGen", r"\dagNMH", r"\T_"]:
    if bad in tex:
        print(f"STILL PRESENT: {bad}")
    else:
        print(f"OK: {bad} removed")
