import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_V7_NODOLLAR.tex", "r", encoding="utf-8") as f:
    tex = f.read()

print(f"V7 input: {len(tex)} chars")

fixes = 0

# Fix 1: \Gamm → \Gamma (3 cases where Gamma lost its last 'a')
# These appear as \Gamm followed by 'a' which is actually part of Gamma
tex = tex.replace(r"\Gamm", r"\Gamma")
# But NOT in the 3 cases where \Gamm + a_{st}: the 'a' after \Gamm is the last char of Gamma
# So after replacement: \Gamma + a_{st}. But we want \Gamma_{st}
# Fix: \Gamma a_{st} → \Gamma_{st}  or  \Gamma$a$_{st} → \Gamma_{st}
# Pattern: \Gamma followed immediately by 'a' (the old trailing 'a')
# Actually after \Gamm→\Gamma, we get \Gammaa_{st} which is wrong
# But `\Gamm` was followed by `a` - let me just fix \Gammaa → \Gamma
tex = tex.replace(r"\Gammaa", r"\Gamma")

# Fix 2: Handle the 3 cases where \Gamma was scattered: $\Gamma$a$_{st}$ 
# These are now \Gamma a_{st} or \Gammaa_{st} after our fix
# Actually Fix 1 handles \Gammaa. But there might be $\Gamma$ a$_{st}$ patterns
# Let's merge them: $\Gamma$ a$_{st}$ → $\Gamma_{st}$
# First check if this pattern exists
pat = re.compile(r'\$\\Gamma\$a\$_\{st\}\$')
count = len(pat.findall(tex))
if count > 0:
    tex = pat.sub(r'$\Gamma_{st}$', tex)
    fixes += count
    print(f"Fixed {count} scattered $\Gamma$")

# Fix 3: \SData → \S{}Data
tex = tex.replace(r"\SData", r"\S{}Data")

# Fix 4: \dagGen → \dag{}Gen  
tex = tex.replace(r"\dagGen", r"\dag{}Gen")
tex = tex.replace(r"\dagNMH", r"\dag{}NMH")

# Fix 5: \T_{\text{c}} → T_{\text{c}} (inside math, just use T)
tex = tex.replace(r"\T_{\text{c}}", r"T_{\text{c}}")
tex = tex.replace(r"\T_", r"T_")

# Now verify
gamm_count = tex.count(r"\Gamm")
gamma_count = tex.count(r"\Gamma")
gammaa_count = tex.count(r"\Gammaa")
print(f"\\Gamm: {gamm_count}, \\Gamma: {gamma_count}, \\Gammaa: {gammaa_count}")

# Check remaining undefined
for bad in [r"\SData", r"\dagGen", r"\dagNMH"]:
    if bad in tex:
        print(f"WARNING: {bad} still present!")

out_path = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_V9_FINALFIX.tex"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(tex)

print(f"V9_FINALFIX: {len(tex)} chars, {len(tex.splitlines())} lines")
print(f"Total fixes: {fixes}")
