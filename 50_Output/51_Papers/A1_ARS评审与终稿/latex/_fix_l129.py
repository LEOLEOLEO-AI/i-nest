with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Fix set notation: {1/\sqrt{2}, 1, $\phi$, e, $\pi$, $\delta$} 
# → $\{1/\sqrt{2}, 1, \phi, e, \pi, \delta\}$
# The current has mix of math and text: {1/\sqrt{2} (text), 1 (text), $\phi$ (math), e (text), $\pi$ (math), $\delta$ (math)}
# Fix: entire thing in one math block with escaped braces

tex = tex.replace(
    "{1/\\sqrt{2}, 1, $\\phi$, e, $\\pi$, $\\delta$}",
    "$\\{1/\\sqrt{2}, 1, \\phi, e, \\pi, \\delta\\}$"
)

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Fixed L129 set notation")
