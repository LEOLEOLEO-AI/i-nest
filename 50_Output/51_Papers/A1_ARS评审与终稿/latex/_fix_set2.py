with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Fix the set notation properly: wrap entire thing in $...$ with escaped braces
# Original: {1/\sqrt{2}, 1, $\phi$, e, $\pi$, $\delta$}
# Fixed: $\{1/\sqrt{2}, 1, \phi, e, \pi, \delta\}$

# But the text currently has been partially modified. Let me check
idx = tex.find("$\\{1/\\sqrt{2}")
if idx >= 0:
    # Find where this math block should end
    snippet = tex[idx:idx+100]
    print("Current snippet: " + snippet[:100])
    
    # The pattern should end with \delta\} and then continue as text
    # Let me find the closing point
    end_idx = tex.find("\\delta\\}", idx)
    if end_idx >= 0:
        # Replace the whole fragment
        old = tex[idx:end_idx+8]  # +8 for \delta\}
        new = "$\\{1/\\sqrt{2}, 1, \\phi, e, \\pi, \\delta\\}$"
        tex = tex.replace(old, new)
        print("Fixed full set notation")

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Saved")
