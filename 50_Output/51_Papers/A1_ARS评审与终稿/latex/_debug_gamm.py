with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_V7_NODOLLAR.tex", "r", encoding="utf-8") as f:
    v7 = f.read()

# Find \Gamm in V7
import re
for m in re.finditer(r"\\Gamm", v7):
    ctx = v7[m.start()-10:m.end()+30].replace(chr(10), " ")
    print(f"\\Gamm at {m.start()}: [{ctx}]")

# Now check the replacement effect
# \Gamm -> \Gamma, but what comes after \Gamm in V7?
for m in re.finditer(r"\\Gamm", v7):
    after = v7[m.end():m.end()+5]
    print(f"  after '\\Gamm': [{after}]")
