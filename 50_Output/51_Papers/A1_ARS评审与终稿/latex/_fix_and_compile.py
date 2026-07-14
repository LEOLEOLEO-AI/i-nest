with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex", "r", encoding="utf-8") as f:
    tex = f.read()

tex = tex.replace("(\\pi):*", "($\\pi$):*")
tex = tex.replace("(\\delta", "($\\delta$")

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)

# Compile inline
import subprocess
result = subprocess.run([
    r"C:\Users\LEO\.codex\plugins\cache\openai-bundled\latex\0.2.3\bin\tectonic.exe",
    "-X", "compile", "--keep-intermediates",
    "--outdir", r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex",
    "--outfmt", "pdf", "--untrusted", out
], capture_output=True, text=True, timeout=60)

print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
if result.stderr:
    print("STDERR:", result.stderr[-300:])
print("Return code:", result.returncode)
