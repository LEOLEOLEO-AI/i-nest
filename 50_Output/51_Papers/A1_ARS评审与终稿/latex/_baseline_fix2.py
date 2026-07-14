with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_BASELINE_FIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Replace remaining Unicode
tex = tex.replace("\u00b9", "$^1$")       # superscript 1
tex = tex.replace("\u00e1", r"\'{a}")      # a acute
tex = tex.replace("\u00e9", r"\'{e}")      # e acute
tex = tex.replace("\u0151", r"\H{o}")      # o double acute

# Verify no remaining non-ASCII
remaining = [c for c in tex if ord(c) > 127 and ord(c) < 0x2000]
if remaining:
    unique = set(remaining)
    print(f"WARNING: {len(unique)} unique non-ASCII chars remain:")
    for c in sorted(unique):
        print(f"  U+{ord(c):04X}: x{tex.count(c)}")
else:
    print("ALL non-ASCII replaced!")

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_BASELINE_FIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print(f"Written: {len(tex)} chars")
