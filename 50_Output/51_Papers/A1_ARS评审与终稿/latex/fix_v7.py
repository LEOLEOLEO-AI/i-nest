import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_V6_SAFE.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Remove $ signs inside math environments: equation, align, eqnarray, gather, etc.
MATH_ENVS = [
    r"\begin{equation}", r"\begin{align}", r"\begin{alignat}",
    r"\begin{eqnarray}", r"\begin{gather}", r"\begin{multline}",
    r"\begin{displaymath}", r"\begin{math}",
]

END_ENVS = [
    r"\end{equation}", r"\end{align}", r"\end{alignat}",
    r"\end{eqnarray}", r"\end{gather}", r"\end{multline}",
    r"\end{displaymath}", r"\end{math}",
]

def strip_dollars_in_envs(tex):
    """Remove $ signs inside math environments"""
    # Find all math environment blocks
    # Strategy: for each \begin{env}...\end{env}, remove $ signs in between
    for begin_tag, end_tag in zip(MATH_ENVS, END_ENVS):
        # Find all instances of this environment
        pos = 0
        while True:
            start = tex.find(begin_tag, pos)
            if start < 0:
                break
            end = tex.find(end_tag, start + len(begin_tag))
            if end < 0:
                break
            # Extract content inside the environment
            inner_start = start + len(begin_tag)
            inner = tex[inner_start:end]
            # Remove all $ signs (but keep escaped \$)
            inner_fixed = inner.replace("$", "")
            tex = tex[:inner_start] + inner_fixed + tex[end:]
            pos = inner_start + len(inner_fixed) + len(end_tag)
    return tex

tex = strip_dollars_in_envs(tex)

# Also fix $$...$$ display math (should be fine, but clean up)
# And fix \[...\] environments
def strip_dollars_in_display(tex):
    """Remove $ inside \[...\] blocks"""
    pos = 0
    while True:
        start = tex.find(r"\[", pos)
        if start < 0:
            break
        end = tex.find(r"\]", start + 2)
        if end < 0:
            break
        inner_start = start + 2
        inner = tex[inner_start:end]
        inner_fixed = inner.replace("$", "")
        tex = tex[:inner_start] + inner_fixed + tex[end:]
        pos = inner_start + len(inner_fixed) + 2
    return tex

tex = strip_dollars_in_display(tex)

# Also fix $$...$$ blocks
def strip_dollars_in_dd(tex):
    """Remove $ inside $$...$$ blocks"""
    pos = 0
    while True:
        start = tex.find("$$", pos)
        if start < 0:
            break
        end = tex.find("$$", start + 2)
        if end < 0:
            break
        inner_start = start + 2
        inner = tex[inner_start:end]
        inner_fixed = inner.replace("$", "")
        tex = tex[:inner_start] + inner_fixed + tex[end:]
        pos = inner_start + len(inner_fixed) + 2
    return tex

tex = strip_dollars_in_dd(tex)

# Count changes
dollar_count = tex.count("$")
print(f"Dollar signs remaining: {dollar_count}")

out_path = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_V7_NODOLLAR.tex"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(tex)

print(f"V7_NODOLLAR: {len(tex)} chars, {len(tex.splitlines())} lines")
