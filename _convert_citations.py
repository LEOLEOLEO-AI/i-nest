import json, re, os

v29=r'D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_CST_Theory_V29_FROM_PDF.md'
t=open(v29,encoding='utf-8').read()

map_path=r'D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\ref_key_map.json'
with open(map_path, encoding='utf-8') as f:
    key_map = json.load(f)

# Replace citation references [1] -> [@key]
# But be CAREFUL: [1] appears in many contexts (figure refs, numbers, etc.)
# Only replace [n] where n is 1-69 and it's used as a citation

# Strategy: Replace [n] that follow text (not standalone numbers)
# Pattern: text[1] -> text[@key]
count = 0
for num, key in key_map.items():
    old = '[' + num + ']'
    new = '[@' + key + ']'
    # Only replace when preceded by non-digit, non-bracket
    t = re.sub(r'(?<!\d|\])' + re.escape(old), new, t)
    count += 1

# Save as new version: V30 with citation keys
out_path = v29.replace('V29_FROM_PDF.md', 'V30_CITEKEYS.md')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(t)

# Also preserve reference section with keys
# Replace [n] at start of reference lines
lines = t.split('\n')
new_lines = []
for l in lines:
    m = re.match(r'^\[(\d+)\]', l.strip())
    if m and m.group(1) in key_map:
        key = key_map[m.group(1)]
        l = l.replace('[' + m.group(1) + ']', '@' + key, 1)
    new_lines.append(l)

t2 = '\n'.join(new_lines)
out_path2 = v29.replace('V29_FROM_PDF.md', 'V30_CITEKEYS_FULL.md')
with open(out_path2, 'w', encoding='utf-8') as f:
    f.write(t2)

print(f'V30 created with citation keys')
print(f'Citation version: {out_path}')
print(f'Full reference version: {out_path2}')
print(f'Total conversions: {count}')
