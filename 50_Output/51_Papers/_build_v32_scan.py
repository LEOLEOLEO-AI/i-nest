import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

with open(r"D:\Obsidian\home\work\.openclaw\workspace\TCC_2_论文撰写\_pdf_v25_full.txt", "r", encoding="utf-8") as f:
    pdf_text = f.read()

# Quick scan
for keyword in ["CST =", "Triple Lock", "Table 2", "UCCP", "LLaMA", "η_I"]:
    count = pdf_text.count(keyword)
    print(f'  {keyword}: {count} occurrences')

print(f"\nTotal PDF chars: {len(pdf_text)}")
print("PDF ready for merge")
