import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_V6_SAFE.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Search: dollar-Gamma-dollar followed by underscore
# This is the broken pattern: $\Gamma$_{st}
pattern = re.compile(r'\$\\Gamma\$\_')
matches = list(pattern.finditer(tex))
print(f"Scattered $\\Gamma$ followed by _: {len(matches)}")
for m in matches[:5]:
    ctx = tex[m.start()-10:m.end()+30].replace(chr(10), " ")
    print(f"  [{ctx}]")

# Check V7 for same
with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_V7_NODOLLAR.tex", "r", encoding="utf-8") as f:
    v7 = f.read()

# After stripping $ in equation envs, what happened?
# Search for \Gamma followed by a (not underscore)
pat2 = re.compile(r'\\Gammaa')
m2 = list(pat2.finditer(v7))
print(f"\nGammaa patterns in V7: {len(m2)}")
for m in m2[:5]:
    ctx = v7[m.start()-10:m.end()+30].replace(chr(10), " ")
    print(f"  [{ctx}]")

# Also check: what's between \Gamma and _ in V7?
# Search for \Gamma followed by non-underscore then underscore
pat3 = re.compile(r'\\Gamma([^_])_')
m3 = list(pat3.finditer(v7))
print(f"\nGamma followed by non-_ then _ in V7: {len(m3)}")
for m in m3[:10]:
    char_between = m.group(1)
    ctx = v7[m.start()-10:m.end()+30].replace(chr(10), " ")
    print(f"  char='{char_between}' [{ctx}]")
