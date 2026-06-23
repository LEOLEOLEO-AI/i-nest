fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

# Check format of new entries
idx = html.find('"id": 48')
if idx > 0:
    print(f"Found id:48 with space at {idx}")
    print(html[idx:idx+150])
else:
    idx = html.find('"id":48')
    if idx > 0:
        print(f"Found id:48 without space at {idx}")
        print(html[idx:idx+150])
    else:
        print("id:48 not found at all")

# Check if new patent entries are there
if 'P0优先级' in html:
    print("Patent entries found!")
    idx = html.find('P0优先级')
    print(html[max(0,idx-30):idx+100])

# Check 6/5 daily content
idx = html.find('2026-06-05')
if idx > 0:
    chunk = html[idx:idx+400]
    print(f"\n6/5 daily:")
    print(chunk)
