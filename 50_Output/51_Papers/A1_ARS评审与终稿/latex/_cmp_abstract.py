with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\_BASELINE_A1_CST.tex", "r", encoding="utf-8") as f:
    baseline = f.read()

with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_DDFIX.tex", "r", encoding="utf-8") as f:
    dd = f.read()

# Extract abstracts
import re

def get_abstract(text):
    m = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', text, re.DOTALL)
    return m.group(1) if m else ""

abs_base = get_abstract(baseline)
abs_dd = get_abstract(dd)

print("Baseline abstract length: " + str(len(abs_base)))
print("DDFIX abstract length: " + str(len(abs_dd)))

# Show differences
if abs_base != abs_dd:
    # Show the first 300 chars of each
    print("\nBaseline (first 300):")
    print(abs_base[:300])
    print("\nDDFIX (first 300):")
    print(abs_dd[:300])
    
    # Count $ in each
    print("\nBaseline $ count: " + str(abs_base.count("$")))
    print("DDFIX $ count: " + str(abs_dd.count("$")))
