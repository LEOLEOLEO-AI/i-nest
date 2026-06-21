with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Fix \Gammast → \Gamma_{st}
n = tex.count("\\Gammast")
tex = tex.replace("\\Gammast", "\\Gamma_{st}")
print("\\Gammast -> \\Gamma_{st}: " + str(n))

# Fix \Gammaa → \Gamma (if any remain)
n2 = tex.count("\\Gammaa")
# Actually \Gammaa is \Gamma followed by 'a' in text. Let me check contexts.
import re
for m in re.finditer(r'\\Gammaa', tex):
    ctx = tex[m.start():m.end()+10]
    print("  Gammaa: " + ctx)

# Also check for other \Gamma patterns that are wrong
for pat in [r'\\Gammaa(?=[^a-zA-Z])', r'\\Gamma_a', r'\\Gamma\{st']:
    count = len(re.findall(pat, tex))
    if count > 0:
        print(pat + ": " + str(count))

# Clean up any remaining $$
tex = tex.replace("$$", "")

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Fixed and saved: " + str(len(tex)) + " chars")
