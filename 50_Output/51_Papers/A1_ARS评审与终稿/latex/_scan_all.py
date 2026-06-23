with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Quick scan: find ALL remaining text-mode issues
import re

# Split into lines and scan for issues
lines = tex.split("\n")
issues = []
for i, line in enumerate(lines):
    # Skip equation environments
    if "\\begin{equation}" in line or "\\begin{align}" in line:
        continue
    if "\\end{equation}" in line or "\\end{align}" in line:
        continue
    
    in_math = False
    j = 0
    while j < len(line):
        if line[j:j+2] == "\\$":
            j += 2; continue
        if line[j] == "$":
            in_math = not in_math
            j += 1; continue
        if line[j] == "_" and not in_math and (j == 0 or line[j-1] != "\\"):
            ctx = line[max(0,j-20):min(len(line),j+40)]
            issues.append(("TXT_", i+1, j, ctx))
        if line[j] == "^" and not in_math:
            ctx = line[max(0,j-20):min(len(line),j+40)]
            issues.append(("TXT^", i+1, j, ctx))
        # Check for \math_commands in text mode
        if line[j] == "\\" and not in_math:
            # Peek ahead for known math commands
            for cmd in ["\\alpha", "\\beta", "\\gamma", "\\delta", "\\epsilon",
                        "\\theta", "\\lambda", "\\mu", "\\sigma", "\\phi", "\\pi",
                        "\\Gamma", "\\Delta", "\\Theta", "\\Phi", "\\Psi", "\\Omega",
                        "\\cdot", "\\times", "\\approx", "\\sim", "\\geq", "\\leq",
                        "\\neq", "\\in", "\\pm", "\\rightarrow", "\\propto", "\\cong"]:
                if line[j:j+len(cmd)] == cmd:
                    ctx = line[max(0,j-20):min(len(line),j+len(cmd)+20)]
                    issues.append(("TXT_MATHCMD", i+1, j, cmd + ": " + ctx))
                    break
        j += 1

# Print first 20 issues
for issue_type, line_no, pos, details in issues[:20]:
    print("L{} {}: {}".format(line_no, issue_type, details))

print("\nTotal issues: " + str(len(issues)))
