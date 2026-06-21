import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_BASELINE_FIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

fixes = {}

# Map every remaining Unicode
mappings = {
    "\u2020": r"\dag",           # dagger
    "\u2074": r"$^4$",           # superscript 4
    "\u2075": r"$^5$",           # superscript 5
    "\u2076": r"$^6$",           # superscript 6
    "\u2077": r"$^7$",           # superscript 7
    "\u2079": r"$^9$",           # superscript 9
    "\u207b": r"$^{-}$",         # superscript minus
    "\u207f": r"$^n$",           # superscript n
    "\u2081": r"$_1$",           # subscript 1
    "\u2082": r"$_2$",           # subscript 2
    "\u2083": r"$_3$",           # subscript 3
    "\u2085": r"$_5$",           # subscript 5
    "\u2093": r"$_x$",           # subscript x
    "\u209b": r"$_s$",           # subscript s
    "\u211d": r"$\mathbb{R}$",   # double-struck R
    "\u2194": r"$\leftrightarrow$",  # left-right arrow
    "\u221d": r"$\propto$",      # proportional to
    "\u2245": r"$\cong$",        # approximately equal / congruent
    "\u2713": r"\checkmark",     # check mark
    "\u5218\u52e4\u8ba9": r"Liu, Q.",  # replace Chinese name
}

for uchar, latex in mappings.items():
    count = tex.count(uchar)
    if count > 0:
        tex = tex.replace(uchar, latex)
        fixes[uchar] = count

for uchar, count in fixes.items():
    print(f"Fixed U+{ord(uchar):04X}: {count} occurrences")

# Verify
remaining = [c for c in tex if ord(c) > 127 and ord(c) < 0x2000]
if remaining:
    print(f"WARNING: {len(set(remaining))} chars remain!")
else:
    print("ALL CLEAN - no non-ASCII remaining!")

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_BASELINE_FIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print(f"Written: {len(tex)} chars")
