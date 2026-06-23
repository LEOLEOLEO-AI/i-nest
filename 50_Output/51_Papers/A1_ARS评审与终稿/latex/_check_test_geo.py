with open(r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\test_eq.tex", "r", encoding="utf-8") as f:
    test_eq = f.read()

# Check if test_eq has geometric mechanics section
if "Geometric mechanics" in test_eq:
    print("test_eq has geometric mechanics section!")
else:
    print("test_eq does NOT have geometric mechanics")
    # Show last 200 chars
    print("Last 200: " + test_eq[-200:])
