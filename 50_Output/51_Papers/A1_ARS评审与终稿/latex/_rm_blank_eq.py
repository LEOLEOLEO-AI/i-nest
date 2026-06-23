import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Remove blank lines inside equation/align environments
# Pattern: \begin{equation}\n\n...\n\n...\n\end{equation}
def remove_blanks_in_env(tex, env_name):
    begin = "\\begin{" + env_name + "}"
    end = "\\end{" + env_name + "}"
    pos = 0
    while True:
        start = tex.find(begin, pos)
        if start < 0: break
        end_pos = tex.find(end, start)
        if end_pos < 0: break
        
        # Content between \begin and \end
        content_start = start + len(begin)
        content = tex[content_start:end_pos]
        
        # Remove blank lines (consecutive \n\n)
        fixed = re.sub(r'\n\s*\n', '\n', content)
        
        if fixed != content:
            tex = tex[:content_start] + fixed + tex[end_pos:]
            # Adjust end_pos
            end_pos = content_start + len(fixed) + len(end)
        
        pos = end_pos
    return tex

for env in ["equation", "align", "alignat", "gather"]:
    tex = remove_blanks_in_env(tex, env)

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)
print("Saved: " + str(len(tex)))
