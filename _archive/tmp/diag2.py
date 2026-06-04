fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

# Find DEFAULT_DATA
dd_idx = html.find("DEFAULT_DATA")
print(f"DEFAULT_DATA at: {dd_idx}")

# Find the last entry
# Look for patterns near the end of entries
for pattern in ['}]\\n  ]\\n}', '}]\\n    ]', '\\"priority\\":\\"中\\"']:
    idx = html.rfind(pattern)
    print(f"Last '{pattern[:30]}' at: {idx}")
    if idx > 0:
        print(f"  Context: ...{html[max(0,idx-50):idx+100]}...")
        break

# Check what the entries array closing looks like
entries_marker = html.find('"entries": [')
if entries_marker > 0:
    # Find the closing of the array
    # Count brackets
    depth = 0
    end = entries_marker
    for i in range(entries_marker, len(html)):
        if html[i] == '[':
            depth += 1
        elif html[i] == ']':
            depth -= 1
            if depth == 0:
                end = i
                break
    print(f"\nEntries array: {entries_marker} to {end}")
    print(f"  Last 100 chars before close: ...{html[max(0,end-100):end]}...")
