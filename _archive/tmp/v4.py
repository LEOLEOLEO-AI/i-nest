import re
fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

for i in range(54, 62):
    found = ('"id": ' + str(i)) in html
    print("Entry " + str(i) + ": " + ("OK" if found else "MISSING"))

if "专著/白皮书体系梳理" in html:
    print("Daily: monograph note OK")

ids = re.findall(r'"id":\s*(\d+)', html)
print("Total IDs: " + str(len(ids)))
