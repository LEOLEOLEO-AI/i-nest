with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_BASELINE_FIX.tex", "r", encoding="utf-8") as f:
    tex = f.read()

# Find ALL non-ASCII chars
import unicodedata
non_ascii = {}
for i, c in enumerate(tex):
    if ord(c) > 127:
        if c not in non_ascii:
            non_ascii[c] = {"count": 0, "first_pos": i, "ctx": ""}
        non_ascii[c]["count"] += 1
        if non_ascii[c]["count"] == 1:
            start = max(0, i-20)
            end = min(len(tex), i+40)
            non_ascii[c]["ctx"] = tex[start:end].replace("\n", " ")

report = []
for c in sorted(non_ascii, key=lambda x: ord(x)):
    info = non_ascii[c]
    report.append(f"U+{ord(c):04X} ({unicodedata.name(c, 'UNKNOWN')}): x{info['count']} first at pos {info['first_pos']}")
    report.append(f"  Context: [{info['ctx'][:120]}]")

report_text = "\n".join(report)

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\_unicode_final.txt", "w", encoding="utf-8") as f:
    f.write(report_text)

print(f"Found {len(non_ascii)} unique non-ASCII chars")
