import re
with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Find ALL broken patterns from the scattered math fix
# The fix creates: $X \cdot Y$ — but if X or Y already has $ inside, it breaks
# Pattern: $X \cdot $Y$ — double $ issue

# Check for common corruption patterns
corruptions = [
    (r'\$\$', 'Double $$ (stray)'),
    (r'\$[^$]*\$\s*\$', 'Adjacent math blocks'),
    (r'\$[^$]*\\cdot\s*\$[^$]*\$', 'cdot with 3 $ blocks'),
]

for pattern, desc in corruptions:
    matches = list(re.finditer(pattern, tex))
    if matches:
        print(desc + ": " + str(len(matches)))
        for m in matches[:3]:
            ctx = tex[max(0,m.start()-20):m.end()+30].replace(chr(10),' ')
            print("  [" + ctx + "]")

# Also check $ balance
total = sum(line.count("$") - line.count("\\$") for line in tex.split("\n"))
print("\nTotal $: " + str(total) + " (" + ("OK" if total % 2 == 0 else "UNBALANCED!") + ")")
