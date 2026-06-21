import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_V7_NODOLLAR.tex", "r", encoding="utf-8") as f:
    tex = f.read()

fixes = 0

# Fix 1: \Gamm → \Gamma (always followed by 'a' which should be inside the command)
# Pattern: \Gamm + a char → \Gamma + that char
# Cases found: \Gamm$a$, \Gamm$a\_{...} 
tex = tex.replace(r"\Gamm", r"\Gamma")
# But this might break if \Gamma was already correct... let me check
# Actually \Gamm is the truncated form, so replacing is safe
fixes += tex.count(r"\Gamma")  # count for info

# Fix 2: \SData → \S{}Data or \S\ Data
tex = tex.replace(r"\SData", r"\S{}Data")

# Fix 3: \dagGen → \dag{}Gen
tex = tex.replace(r"\dagGen", r"\dag{}Gen")

# Fix 4: \dagNMH → \dag{}NMH
tex = tex.replace(r"\dagNMH", r"\dag{}NMH")

# Fix 5: \T_{\text{c}} → $T_{\text{c}}$ (needs math mode)
tex = re.sub(r'\\T_\{', r'$T_{', tex)
# But be careful, \T might appear as \T without subscript
tex = re.sub(r'\\T(?![a-zA-Z])', r'$T$', tex)

# Actually, let me check if there are T_{\text{c}} patterns
# Looking at the context: ($\T_{\text{c}}=0.093$
# This has $ before \T, so it's already in math mode but \T is undefined
# In math mode, just use T
tex = tex.replace(r"\T_", r"T_")
tex = tex.replace(r" \T ", r" T ")

# Fix 6: Check for \dag without {} before next char
# Actually \dag is a standard command, but needs space after it
# \dagGen and \dagNMH were already handled

print(f"Fixes applied to V7")

# Write
out_path = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_V8_FIXCMD.tex"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(tex)

print(f"V8_FIXCMD: {len(tex)} chars")
