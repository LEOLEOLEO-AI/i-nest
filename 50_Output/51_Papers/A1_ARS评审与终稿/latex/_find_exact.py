with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Find 10^{-} and show exact bytes
idx = tex.find("10$^{-}")
if idx >= 0:
    snippet = tex[idx:idx+20]
    print("Found at " + str(idx) + ": " + repr(snippet))
    print("  Exactly: [" + snippet + "]")
    
    # Now fix this specific pattern
    # Replace all instances of $^{-}^N$ with single superscript block
    import re
    
    # Manual fix: $^{-}^6$ → $^{-6}$
    n_before = tex.count("$^{-}^")
    tex = tex.replace("$^{-}^6$", "$^{-6}$")
    tex = tex.replace("$^{-}^7$", "$^{-7}$")
    
    # Also fix surrounding scattered math
    # 10$^{-6}$ → need to check if 10 should be in math too
    
    n_after = tex.count("$^{-}^")
    print("Fixed: " + str(n_before - n_after) + " of " + str(n_before))
else:
    print("Pattern not found with 10$^{-}")
    # Try broader search
    for m in re.finditer(r'\$\\^\{-\}', tex):
        idx = m.start()
        print("$^{-} at " + str(idx) + ": " + repr(tex[idx:idx+15]))

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Saved")
