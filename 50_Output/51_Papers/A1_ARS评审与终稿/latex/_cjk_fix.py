with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_BASELINE_FIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Fix CJK name that was missed
tex = tex.replace("\u5218\u52e4\u8ba9", "Liu, Q.")

# Verify
remaining = set()
for c in tex:
    if ord(c) > 127 and ord(c) < 0x2000:
        remaining.add(c)

if remaining:
    for c in sorted(remaining):
        print(f"REMAINING: U+{ord(c):04X} x{tex.count(c)}")
else:
    print("ALL CLEAN!")

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_BASELINE_FIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print(f"Final: {len(tex)} chars")
