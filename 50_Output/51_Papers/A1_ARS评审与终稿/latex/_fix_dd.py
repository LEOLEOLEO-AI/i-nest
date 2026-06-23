import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_FINAL_ATTEMPT.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Count $$ occurrences
dd_count = tex.count("$$")
print("$$ occurrences: " + str(dd_count))

# Show contexts of $$
for m in re.finditer(r'\$\$', tex):
    start = max(0, m.start()-30)
    end = min(len(tex), m.end()+30)
    ctx = tex[start:end].replace("\n", " ")
    print("  [" + ctx + "]")

# Remove ALL standalone $$ (they're all errors)
# But preserve $$ that are inside valid display math environments
# Actually, just remove all occurrences of $$
tex = tex.replace("$$", "")

# Fix: $M$\_eff pattern → $M_{\text{eff}}$ (escaped underscore)
# Pattern: $X$\_<word> → $X_{<word>}$ 
pat = re.compile(r'\$([^$]+)\$\\_([a-zA-Z]+)')
n = 0
while pat.search(tex):
    tex, cnt = pat.subn(r'$\1_{\2}$', tex)
    n += cnt
    if n > 200: break
print("Escaped underscore merges: " + str(n))

# Fix: $\Gamma$st → $\Gamma_{st}$ (Gamma followed by text)
# Actually this is: $\Gamma$ followed by st
# Fix: \Gamma in $...$ followed by letters → merge
pat2 = re.compile(r'\$(\\Gamma)\$([a-zA-Z]+)')
n2 = 0
while pat2.search(tex):
    tex, cnt = pat2.subn(r'$\1_{\2}$', tex)
    n2 += cnt
    if n2 > 200: break
print("Gamma_st merges: " + str(n2))

# Similar for other Greek letters: $\alpha$digital → $\alpha_{digital}$
# Already handled by the multi-letter subscript fix
# But check for $\alpha$ followed by text (no underscore)
# Pattern: $\<greek>$ followed by lowercase letters without _ 
# This is harder to detect because the letters after could be regular text
# Let me just focus on known patterns

# Verify $ balance
total = sum(line.count("$") - line.count("\\$") for line in tex.split("\n"))
print("Total $: " + str(total) + " (" + ("OK" if total % 2 == 0 else "UNBALANCED!") + ")")

# Check remaining $$
remaining_dd = tex.count("$$")
print("Remaining $$: " + str(remaining_dd))

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Output: " + str(len(tex)) + " chars")
