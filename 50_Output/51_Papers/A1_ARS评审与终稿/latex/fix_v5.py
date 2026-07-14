import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_V4_TARGETED.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# List of math commands that should ALWAYS be in math mode
MATH_CMDS = [
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
    r"\mathbb", r"\mathcal", r"\mathbf", r"\mathit",
    r"\sqrt",
]

def is_in_math_mode(text, pos):
    """Check if position pos is inside math mode ($...$)"""
    # Count unescaped $ signs before pos
    before = text[:pos]
    # Remove escaped $
    before_clean = before.replace(r"\$", "")
    dollars = before_clean.count("$")
    return dollars % 2 == 1

def is_inside_command_def(text, pos):
    """Check if pos is inside a command definition like \providecommand{...}"""
    before = text[:pos]
    # Look for \providecommand, \newcommand, \renewcommand, \def before pos
    # without matching closing brace
    cmd_start = max(before.rfind(r"\providecommand"), before.rfind(r"\newcommand"),
                    before.rfind(r"\renewcommand"), before.rfind(r"\def"))
    if cmd_start < 0:
        return False
    # Check that we're inside the braces of this command
    after_cmd = before[cmd_start:]
    open_braces = after_cmd.count("{") - after_cmd.count(r"\{")
    close_braces = after_cmd.count("}") - after_cmd.count(r"\}")
    return open_braces > close_braces

fixes = 0
# Process from end to start so positions stay valid
matches = []
for cmd in MATH_CMDS:
    for m in re.finditer(re.escape(cmd), tex):
        if is_in_math_mode(tex, m.start()):
            continue
        if is_inside_command_def(tex, m.start()):
            continue
        # Also skip if part of \begin{...} or \end{...}
        before = tex[max(0,m.start()-20):m.start()]
        if r"\begin" in before[-15:] or r"\end" in before[-13:]:
            continue
        matches.append((m.start(), m.end(), cmd))

# Process from end to start
matches.sort(key=lambda x: x[0], reverse=True)

for start, end, cmd in matches:
    # Wrap in $...$
    tex = tex[:start] + "$" + cmd + "$" + tex[end:]
    fixes += 1

print(f"Wrapped {fixes} bare math commands")

# Cleanup: remove triple+ newlines
tex = re.sub(r"\n{3,}", "\n\n", tex)

out_path = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_V5_FULLFIX.tex"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(tex)

print(f"Output: {len(tex)} chars")
print("V5_FULLFIX written")
