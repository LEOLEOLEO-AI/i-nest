import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_HAND_FIXED.tex", "r", encoding="utf-8") as f:
    tex = f.read()

fixes = 0

# Pattern: $X$\cmd$Y$ -> $X \cmd Y$
cmds = [
    (r"\cdot", r"\cdot"), (r"\approx", r"\approx"), (r"\neq", r"\neq"),
    (r"\times", r"\times"), (r"\sim", r"\sim"), (r"\geq", r"\geq"),
    (r"\leq", r"\leq"), (r"\in", r"\in"), (r"\pm", r"\pm"),
    (r"\Gamma", r"\Gamma"), (r"\alpha", r"\alpha"), (r"\beta", r"\beta"),
    (r"\gamma", r"\gamma"), (r"\delta", r"\delta"), (r"\phi", r"\phi"),
    (r"\pi", r"\pi"), (r"\theta", r"\theta"), (r"\lambda", r"\lambda"),
    (r"\rho", r"\rho"), (r"\sigma", r"\sigma"), (r"\mu", r"\mu"),
    (r"\Phi", r"\Phi"), (r"\Psi", r"\Psi"), (r"\eta", r"\eta"),
    (r"\rightarrow", r"\rightarrow"),
]

for cmd_esc, cmd_clean in cmds:
    pat = re.compile(r"(\$[^$]+\$)\s*(" + re.escape(cmd_esc) + r")\s*(\$[^$]+\$)")
    count = 0
    while pat.search(tex):
        tex = pat.sub(lambda m: "$" + m.group(1)[1:-1] + " " + cmd_clean + " " + m.group(3)[1:-1] + "$", tex)
        count += 1
        if count > 100:
            print(f"WARNING: Loop for {cmd_clean}")
            break
    fixes += count

print(f"Fix1 (scattered math merge): {fixes}")

# Fix $X$ = $Y$
pat2 = re.compile(r"(\$[^$]+\$)\s*=\s*(\$[^$]+\$)")
n = 0
while pat2.search(tex):
    tex = pat2.sub(lambda m: "$" + m.group(1)[1:-1] + " = " + m.group(2)[1:-1] + "$", tex)
    n += 1
    if n > 100: break
fixes += n
print(f"Fix2 (= merge): {n}")

# Fix $X$,$Y$
pat3 = re.compile(r"(\$[^$]+\$)\s*,\s*(\$[^$]+\$)")
n = 0
while pat3.search(tex):
    tex = pat3.sub(lambda m: "$" + m.group(1)[1:-1] + ", " + m.group(2)[1:-1] + "$", tex)
    n += 1
    if n > 100: break
fixes += n
print(f"Fix3 (, merge): {n}")

# Cleanup
tex = re.sub(r"\n{3,}", "\n\n", tex)
tex = re.sub(r"(?<!\n)\$\$(?!\n)", "", tex)

out_path = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_V4_TARGETED.tex"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(tex)

print(f"Total fixes: {fixes}")
print(f"Output: {len(tex)} chars, {len(tex.splitlines())} lines")
print("V4_TARGETED written")
