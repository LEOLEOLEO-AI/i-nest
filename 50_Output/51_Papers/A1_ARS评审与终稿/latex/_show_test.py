with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\test_eq.tex", "r", encoding="utf-8") as f:
    tex = f.read()

print("test_eq.tex: " + str(len(tex)) + " chars")
print("=== PREAMBLE ===")
# Print preamble up to \begin{document}
idx = tex.find(r"\begin{document}")
print(tex[:idx])
print("\n=== CONTENT START (first 500 chars) ===")
content = tex[idx:]
print(content[:500])
print("\n=== CONTENT END (last 300 chars) ===")
print(content[-300:])
