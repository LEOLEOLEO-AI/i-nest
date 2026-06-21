import subprocess

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Fix \Gamm → \Gamma (but \Gamm is also substring of \Gamma!)
# Need to fix only standalone \Gamm (not inside \Gamma)
# Strategy: \Gamma is 6 chars, \Gamm is 5 chars
# \Gamm appears as standalone when NOT followed by 'a' as part of the command
# But the issue is: \Gamm followed by 'a' in text: $\Gamm$a_{st}
# This should become $\Gamma_{st}$
tex = tex.replace("$\\Gamm$a_{st}", "$\\Gamma_{st}$")

# Also fix any \Gamm at beginning of line or after space
# But \Gamm is also substring of \Gamma! So let me be careful
# Search for \Gamm NOT followed by letter 'a'
import re
# \Gamm(?!a) — stand-alone \Gamm without the 'a' that would make it \Gamma
pat = re.compile(r'\\Gamm(?!a)')
count = len(pat.findall(tex))
if count > 0:
    tex = pat.sub(r'\\Gamma', tex)
    print("Fixed standalone \\Gamm: " + str(count))

# Also check for \Gammaa (created by earlier bad fix)
pat2 = re.compile(r'\\Gammaa')
count2 = len(pat2.findall(tex))
if count2 > 0:
    tex = pat2.sub(r'\\Gamma', tex)
    print("Fixed \\Gammaa: " + str(count2))

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_REBUILT.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write(tex)

result = subprocess.run([
    r"C:\Users\LEO\.codex\plugins\cache\openai-bundled\latex\0.2.3\bin\tectonic.exe",
    "-X", "compile", "--keep-intermediates",
    "--outdir", r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex",
    "--outfmt", "pdf", "--untrusted", out
], capture_output=True, text=True, timeout=60)

for line in result.stderr.split("\n"):
    if "error" in line.lower() or "note:" in line:
        print(line)
# Check if PDF was written
if "A1_CST_REBUILT.pdf" in result.stdout:
    print("PDF WRITTEN!")
print("RC:", result.returncode)
