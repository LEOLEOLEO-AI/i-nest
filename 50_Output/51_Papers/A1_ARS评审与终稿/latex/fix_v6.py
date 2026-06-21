import re

# Start from V4 which didn't break \providecommand
with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_V4_TARGETED.tex", "r", encoding="utf-8") as f:
    tex = f.read()

print(f"V4 input: {len(tex)} chars, {len(tex.splitlines())} lines")

# Scan ALL \commands and determine which are math commands appearing in text mode
# Strategy: find every \word pattern, check context

MATH_ONLY_CMDS = {
    r"\alpha", r"\beta", r"\gamma", r"\delta", r"\epsilon", r"\zeta", r"\eta",
    r"\theta", r"\iota", r"\kappa", r"\lambda", r"\mu", r"\nu", r"\xi", r"\pi",
    r"\rho", r"\sigma", r"\tau", r"\upsilon", r"\phi", r"\chi", r"\psi", r"\omega",
    r"\Gamma", r"\Delta", r"\Theta", r"\Lambda", r"\Xi", r"\Pi",
    r"\Sigma", r"\Upsilon", r"\Phi", r"\Psi", r"\Omega",
    r"\cdot", r"\times", r"\approx", r"\sim", r"\simeq", r"\equiv",
    r"\propto", r"\pm", r"\mp",
    r"\leq", r"\geq", r"\neq", r"\ll", r"\gg",
    r"\in", r"\ni", r"\subset", r"\supset", r"\subseteq", r"\supseteq",
    r"\forall", r"\exists", r"\emptyset", r"\infty", r"\partial", r"\nabla",
    r"\rightarrow", r"\leftarrow", r"\Rightarrow", r"\Leftarrow",
    r"\longrightarrow", r"\mapsto", r"\to",
    r"\sum", r"\prod", r"\int", r"\oint",
    r"\sqrt", r"\mathbb", r"\mathcal",
}

# Build regex to find \cmd patterns
# We need to find \cmd that is NOT inside:
# 1. $...$ pairs (math mode)  
# 2. \providecommand{...}, \newcommand{...}, \renewcommand{...}, \def...
# 3. \begin{...}, \end{...}

def is_in_math(pos):
    """Check if position is inside $...$ pair"""
    before = tex[:pos]
    cleaned = before.replace(r"\$", "")
    return cleaned.count("$") % 2 == 1

def is_in_cmd_def(pos):
    """Check if position is inside brace group of \providecommand, \newcommand, etc."""
    before = tex[:pos]
    # Find last command definition start
    markers = [r"\providecommand", r"\newcommand", r"\renewcommand", r"\def "]
    last_start = -1
    for m in markers:
        idx = before.rfind(m)
        if idx > last_start:
            last_start = idx
    if last_start < 0:
        return False
    # Check if we're still inside the braces of this definition
    after_def = before[last_start:]
    depth = 0
    for c in after_def:
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
    return depth > 0

def is_in_begin_end(pos):
    """Check if position is inside \begin{...} or \end{...}"""
    before = tex[:pos]
    begin_idx = before.rfind(r"\begin{")
    end_idx = before.rfind(r"\end{")
    latest = max(begin_idx, end_idx)
    if latest < 0:
        return False
    # Check if we're inside the braces
    after = before[latest:]
    depth = 0
    for c in after:
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
    return depth > 0

# Build all matches first
matches = []
for cmd in MATH_ONLY_CMDS:
    esc = re.escape(cmd)
    # Match \cmd not followed by letter or { (to avoid partial matches)
    pattern = esc + r"(?![a-zA-Z{])"
    for m in re.finditer(pattern, tex):
        pos = m.start()
        if is_in_math(pos):
            continue
        if is_in_cmd_def(pos):
            continue
        if is_in_begin_end(pos):
            continue
        # Also skip if preceded by \ (double backslash - part of another command)
        if pos > 0 and tex[pos-1] == "\\":
            continue
        matches.append((pos, m.end(), cmd))

# Sort from end to start
matches.sort(key=lambda x: x[0], reverse=True)

# Remove overlapping matches (keep the longest/best one)
filtered = []
last_end = len(tex) + 1
for start, end, cmd in matches:
    if end <= last_end:
        filtered.append((start, end, cmd))
        last_end = start

filtered.sort(key=lambda x: x[0], reverse=True)

# Apply substitutions
for start, end, cmd in filtered:
    tex = tex[:start] + "$" + cmd + "$" + tex[end:]

print(f"Wrapped {len(filtered)} bare math commands (filtered from {len(matches)} raw matches)")

# Write
out_path = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_V6_SAFE.tex"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(tex)

print(f"V6_SAFE: {len(tex)} chars, {len(tex.splitlines())} lines")

# Quick sanity check - verify line 5 is intact
lines = tex.splitlines()
print(f"L5 check: {lines[4][:100]}")
