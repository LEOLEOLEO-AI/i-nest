import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\test_eq.tex", "r", encoding="utf-8") as f:
    test_eq = f.read()

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    dd = f.read()

# Extract abstract from test_eq
m_test = re.search(r'(\\begin\{abstract\}.*?\\end\{abstract\})', test_eq, re.DOTALL)
test_abs = m_test.group(1) if m_test else ""

# Replace in dd
dd_new = re.sub(r'\\begin\{abstract\}.*?\\end\{abstract\}', test_abs, dd, flags=re.DOTALL)

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "w", encoding="utf-8") as f:
    f.write(dd_new)

print("Abstract replaced. Length: " + str(len(test_abs)) + " -> " + str(len(dd_new)))
