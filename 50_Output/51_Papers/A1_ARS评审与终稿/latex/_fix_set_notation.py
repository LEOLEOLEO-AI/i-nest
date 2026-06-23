import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Fix: {1/\sqrt{2}, ...} in text mode → $\{1/\sqrt{2}, ...\}$
# Find set notation with math inside
pat = re.compile(r'\{1/\\sqrt\{2\},\s*1,\s*\$?\\phi\$?,\s*e,\s*\$?\\pi\$?,\s*\$?\\delta\$?\}')
n = len(pat.findall(tex))
tex = pat.sub(r'$\{1/\\sqrt{2}, 1, \\phi, e, \\pi, \\delta\}$', tex)
print("Fixed set notation: " + str(n))

# Also fix any remaining text-mode \sqrt
# Find \sqrt not inside $...$
parts = re.split(r'(\$[^$]+\$)', tex)
for i in range(0, len(parts), 2):  # text mode parts
    if '\\sqrt' in parts[i]:
        # Wrap in $...$
        parts[i] = parts[i].replace('\\sqrt', '$\\sqrt')
        # Need to handle the closing brace too
        # This is too complex. Let me just fix known patterns.

# Better: find \sqrt{...} in text mode and wrap
# But simpler: just fix the specific patterns I know exist

# Fix: {1/\sqrt{2} → $\{1/\sqrt{2}
tex = tex.replace("{1/\\sqrt{2}", "$\\{1/\\sqrt{2}")

# Fix: \delta\} → \delta\}$ 
tex = tex.replace("\\delta\\}", "\\delta\\}$")

# Fix: \delta} are not → \delta\}$ are not
tex = tex.replace("\\delta\\} are not empirically", "\\delta\\}$ are not empirically")

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Saved: " + str(len(tex)))
