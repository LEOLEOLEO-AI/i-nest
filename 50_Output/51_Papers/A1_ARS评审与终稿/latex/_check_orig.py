import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\_BASELINE_A1_CST.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Check if \_{xxx} appears in the original
underscore_braces = re.findall(r'\\_\{[^}]+\}', tex)
print(f"Total \\_{{xxx}} in original: {len(underscore_braces)}")
unique = set(underscore_braces)
for u in sorted(unique):
    print(f"  {u}: x{underscore_braces.count(u)}")

# Check surrounding context for one example
for m in re.finditer(r'\\_\{eff\}', tex):
    ctx = tex[max(0,m.start()-50):m.end()+50].replace(chr(10), " ")
    print(f"\nContext for \\_eff: [{ctx}]")
    break
